"""Focused offline tests. AWS clients are fakes; these are not live service tests."""
import contextlib, copy, importlib.util, io, json, os, sys, types, unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('signup',ROOT/'deployment/early-access/handler.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
ADDRESS='Case.Sensitive+tag@EXAMPLE.COM'
NORMAL='Case.Sensitive+tag@example.com'
def event(**overrides):
    v={'headers':{'origin':h.ORIGIN,'content-type':'application/json'},'requestContext':{'http':{'method':'POST','sourceIp':'192.0.2.1','userAgent':'fictional'}},'rawPath':'/early-access','rawQueryString':'','body':json.dumps({'email':ADDRESS,'consent_version':h.CONSENT_VERSION}),'isBase64Encoded':False}
    v.update(overrides);return v
class Duplicate(Exception):
    response={'Error':{'Code':'ConditionalCheckFailedException'}}
class FakeDB:
    def __init__(self):self.items={};self.calls=[]
    def put_item(self,**kw):
        self.calls.append(kw);key=kw['Item']['email_key']['S']
        if key in self.items:raise Duplicate()
        self.items[key]=copy.deepcopy(kw['Item'])
class FakeKMS:
    def __init__(self):self.calls=[]
    def encrypt(self,**kw):self.calls.append(kw);return {'CiphertextBlob':b'fictional-ciphertext-not-real-encryption'}
class SignupTests(unittest.TestCase):
    def setUp(self):self.db=FakeDB();self.kms=FakeKMS()
    def invoke(self,e):
        boto=types.SimpleNamespace(client=lambda name,**kw:self.db if name=='dynamodb' else self.kms)
        config=types.SimpleNamespace(Config=lambda **kw:kw)
        with patch.dict(sys.modules,{'boto3':boto,'botocore.config':config}),patch.dict(os.environ,{'CONTACTS_TABLE':'fictional-table','EMAIL_KEY_ID':'fictional-key'}):
            return h.lambda_handler(e,None)
    def test_conservative_normalization(self):self.assertEqual(h.normalize_email(' \t'+ADDRESS+' \n'),NORMAL)
    def test_case_dots_and_plus_stay_distinct(self):
        values=['A.B+tag@example.com','a.b+tag@example.com','AB+tag@example.com','A.B@example.com']
        self.assertEqual(len(set(h.normalize_email(v) for v in values)),4)
    def test_invalid_address_matrix(self):
        for address in ['',None,123,'a@b','a..b@example.com','.a@example.com','a.@example.com','a b@example.com','a@-host.example','a@host-.example','a@@example.com','é@example.com','a\nb@example.com','a'*65+'@example.com','a@'+('x'*64)+'.com']:
            with self.subTest(address=repr(address)):
                with self.assertRaises(ValueError):h.normalize_email(address)
    def test_total_length_boundary(self):
        valid='a'*64+'@'+'b'*63+'.'+'c'*63+'.'+'d'*57+'.com'
        self.assertEqual(len(valid),254);self.assertEqual(h.normalize_email(valid),valid)
        with self.assertRaises(ValueError):h.normalize_email(valid.replace('d'*57,'d'*58))
    def test_valid_request(self):self.assertEqual(h.parse_request(event()),NORMAL)
    def test_unapproved_or_missing_origin(self):
        for origin in ['', 'null','https://www.ioleia.com','https://example.org','https://ioleia.com.attacker.example']:
            self.assertEqual(self.invoke(event(headers={'origin':origin,'content-type':'application/json'}))['statusCode'],400)
        self.assertFalse(self.db.calls);self.assertFalse(self.kms.calls)
    def test_malformed_and_extra_input_fails_closed(self):
        bodies=['{','[]','null','{"email":"a@example.com","email":"b@example.com","consent_version":"'+h.CONSENT_VERSION+'"}',json.dumps({'email':ADDRESS,'consent_version':h.CONSENT_VERSION,'name':'Not collected'}),json.dumps({'email':ADDRESS,'consent_version':'wrong'}),'x'*1025]
        for body in bodies:self.assertEqual(self.invoke(event(body=body))['statusCode'],400)
        self.assertFalse(self.db.calls)
    def test_transport_rejections(self):
        bad=[event(rawQueryString='email=fictional@example.com'),event(isBase64Encoded=True),event(rawPath='/'),event(requestContext={'http':{'method':'GET'}}),event(headers={'origin':h.ORIGIN,'content-type':'text/plain'})]
        for e in bad:self.assertEqual(self.invoke(e)['statusCode'],400)
        self.assertFalse(self.db.calls)
    def test_one_minimal_record_and_constant_encryption_context(self):
        self.assertEqual(self.invoke(event())['statusCode'],200)
        item=next(iter(self.db.items.values()))
        self.assertEqual(set(item),{'email_key','email_ciphertext','created_at','status','source','consent_version'})
        self.assertEqual(item['email_key']['S'],h.hashlib.sha256(NORMAL.encode()).hexdigest())
        self.assertEqual(item['status'],{'S':'active'});self.assertEqual(item['source'],{'S':'ioleia.com'})
        self.assertEqual(item['consent_version'],{'S':h.CONSENT_VERSION});self.assertTrue(item['created_at']['S'].endswith('Z'))
        self.assertNotIn(NORMAL,repr(item))
        self.assertEqual(self.kms.calls[0]['EncryptionContext'],{'purpose':'ioleia-early-access-email'})
        self.assertEqual(self.kms.calls[0]['Plaintext'],NORMAL.encode())
    def test_duplicate_preserves_record_and_response(self):
        first=self.invoke(event());before=copy.deepcopy(self.db.items);second=self.invoke(event())
        self.assertEqual(first,second);self.assertEqual(self.db.items,before);self.assertEqual(len(self.db.items),1)
    def test_duplicate_preserves_unsubscribed_suppression(self):
        first=self.invoke(event());next(iter(self.db.items.values()))['status']={'S':'unsubscribed'}
        second=self.invoke(event());self.assertEqual(first,second)
        self.assertEqual(next(iter(self.db.items.values()))['status'],{'S':'unsubscribed'})
    def test_kms_failure_does_not_write_or_log_email(self):
        self.kms.encrypt=lambda **kw:(_ for _ in ()).throw(RuntimeError('provider error '+NORMAL))
        output=io.StringIO()
        with contextlib.redirect_stdout(output),contextlib.redirect_stderr(output):res=self.invoke(event())
        self.assertEqual(res['statusCode'],503);self.assertFalse(self.db.calls);self.assertEqual(output.getvalue(),'');self.assertNotIn(NORMAL,str(res))
    def test_database_failure_is_generic_and_not_logged(self):
        self.db.put_item=lambda **kw:(_ for _ in ()).throw(RuntimeError('provider error '+NORMAL))
        output=io.StringIO()
        with contextlib.redirect_stdout(output),contextlib.redirect_stderr(output):res=self.invoke(event())
        self.assertEqual(res['statusCode'],503);self.assertEqual(output.getvalue(),'');self.assertNotIn(NORMAL,str(res))
    def test_consent_matches_page_and_contract(self):
        contract=json.loads((ROOT/'docs/signup-consent-contract.json').read_text())
        self.assertEqual(contract['consent_version'],h.CONSENT_VERSION);self.assertEqual(contract['text'],h.CONSENT_TEXT)
        self.assertIn(h.CONSENT_TEXT,(ROOT/'index.html').read_text())
    def test_template_scope_and_cors(self):
        resources=json.loads((ROOT/'deployment/early-access/template.json').read_text())['Resources']
        self.assertEqual(resources['SignupApi']['Properties']['CorsConfiguration']['AllowOrigins'],[h.ORIGIN])
        self.assertNotIn('AccessLogSettings',resources['SignupStage']['Properties'])
        statements=resources['SignupRole']['Properties']['Policies'][0]['PolicyDocument']['Statement']
        actions=set(a for s in statements for a in (s['Action'] if isinstance(s['Action'],list) else [s['Action']]))
        self.assertEqual(actions,{'dynamodb:PutItem','kms:Encrypt','logs:CreateLogStream','logs:PutLogEvents'})
        self.assertEqual(resources['SignupFunction']['Properties']['Code']['ZipFile'],(ROOT/'deployment/early-access/handler.py').read_text())
        self.assertNotIn('AWS::Route53',json.dumps(resources));self.assertNotIn('AWS::SES',json.dumps(resources));self.assertNotIn('AWS::Cognito',json.dumps(resources))
if __name__=='__main__':unittest.main(verbosity=2)
