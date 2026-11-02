"""Public intake only. Never log events, addresses, exceptions, or request metadata."""
import hashlib
import json
import os
import re
from datetime import datetime, timezone

ORIGIN = 'https://ioleia.com'
CONSENT_VERSION = 'ioleia-early-access-v3-2026-11-02'
CONSENT_TEXT = 'By joining, you agree to receive launch updates from Ioleia Inc. Unsubscribe anytime.'
SUCCESS = 'Thanks. Your early-access request has been received.'
_LOCAL = re.compile(r"[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*\Z", re.ASCII)
_LABEL = re.compile(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\Z', re.ASCII)


def normalize_email(value):
    if not isinstance(value, str):
        raise ValueError('Invalid input')
    value = value.strip()
    if not value.isascii() or not 3 <= len(value) <= 254 or value.count('@') != 1:
        raise ValueError('Invalid input')
    local, domain = value.split('@')
    labels = domain.split('.')
    if not 1 <= len(local) <= 64 or not _LOCAL.fullmatch(local):
        raise ValueError('Invalid input')
    if len(labels) < 2 or not all(_LABEL.fullmatch(label) for label in labels):
        raise ValueError('Invalid input')
    if not re.fullmatch(r'[A-Za-z]{2,63}', labels[-1], re.ASCII):
        raise ValueError('Invalid input')
    return local + '@' + domain.lower()


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Invalid input')
        result[key] = value
    return result


def parse_request(event):
    if not isinstance(event, dict):
        raise ValueError('Invalid input')
    headers = event.get('headers') or {}
    if not isinstance(headers, dict):
        raise ValueError('Invalid input')
    headers = {k.lower(): v for k, v in headers.items() if isinstance(k, str)}
    if headers.get('origin') != ORIGIN:
        raise ValueError('Invalid input')
    if event.get('requestContext', {}).get('http', {}).get('method') != 'POST':
        raise ValueError('Invalid input')
    if event.get('rawPath') != '/early-access' or event.get('rawQueryString'):
        raise ValueError('Invalid input')
    if headers.get('content-type', '').split(';')[0].strip().lower() != 'application/json':
        raise ValueError('Invalid input')
    body = event.get('body')
    if event.get('isBase64Encoded') or not isinstance(body, str) or len(body.encode('utf-8')) > 1024:
        raise ValueError('Invalid input')
    data = json.loads(body, object_pairs_hook=_unique_object)
    if not isinstance(data, dict) or set(data) != {'email', 'consent_version'}:
        raise ValueError('Invalid input')
    if data['consent_version'] != CONSENT_VERSION:
        raise ValueError('Invalid input')
    return normalize_email(data['email'])


def response(code, message):
    return {'statusCode': code, 'headers': {'Content-Type': 'application/json', 'Cache-Control': 'no-store'},
            'body': json.dumps({'message': message}, separators=(',', ':'))}


def store_contact(email, dynamodb, kms, table, key_id):
    lookup = hashlib.sha256(email.encode('utf-8')).hexdigest()
    # Never put personal data or the lookup hash in KMS encryption context (CloudTrail).
    encrypted = kms.encrypt(KeyId=key_id, Plaintext=email.encode('utf-8'),
                            EncryptionContext={'purpose': 'ioleia-early-access-email'})['CiphertextBlob']
    item = {
        'email_key': {'S': lookup},
        'email_ciphertext': {'B': encrypted},
        'created_at': {'S': datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')},
        'status': {'S': 'active'},
        'source': {'S': 'ioleia.com'},
        'consent_version': {'S': CONSENT_VERSION},
    }
    try:
        dynamodb.put_item(TableName=table, Item=item, ConditionExpression='attribute_not_exists(email_key)')
    except Exception as error:
        # Conditional insert is atomic: repeated signup cannot overwrite consent or suppression.
        if getattr(error, 'response', {}).get('Error', {}).get('Code') != 'ConditionalCheckFailedException':
            raise


def lambda_handler(event, context):
    try:
        email = parse_request(event)
    except Exception:
        return response(400, 'Please check your email and try again.')
    try:
        import boto3
        from botocore.config import Config
        config = Config(connect_timeout=2, read_timeout=3, retries={'mode': 'standard', 'total_max_attempts': 2})
        store_contact(email, boto3.client('dynamodb', config=config), boto3.client('kms', config=config),
                      os.environ['CONTACTS_TABLE'], os.environ['EMAIL_KEY_ID'])
    except Exception:
        # Do not emit exception text or stack traces: SDK errors can carry request data.
        return response(503, 'We couldn’t save that just now. Please try again.')
    return response(200, SUCCESS)
