# Website intake — prepared, NOT deployed

AWS changes were put on hold by the founder on 2 November 2026. Do not execute deployment or merge the website until that hold is lifted and the focused live checks pass.

This is a public website contact register, not God Agent admission or a CRM. `real_data_admission=false`. No Alpha gate, protected inference, Cognito, SES, Apple, hosting, or DNS resource is in this template.

## Prepared design

Use account **156397421775**, region **ca-central-1** only. Before any mutation, verify the authenticated caller, region and absence of colliding website resources. Do not use another existing profile: the old local bootstrap profile is for a different account. CloudShell currently reports account verification in progress. The proposed local SSO client was denied; no grant was accepted.

One HTTP API route (`POST /early-access`), one Python Lambda and dedicated least-privilege role, one on-demand DynamoDB table, one dedicated rotating KMS key/alias, and one seven-day Lambda log group. The Lambda can insert a record and encrypt its email; it has no email-decrypt, table-read, table-update, table-delete, SES, Cognito or core-system permission. Standard account administrators retain administrative access; this is not the protected-inference architecture.

The address is encrypted with the dedicated KMS key before insertion. DynamoDB additionally uses server-side encryption with its AWS-managed KMS key. No private data appears in KMS encryption context. Table/key deletion is retained/protected; no backups, streams or exports are configured by this template. Existing account-level audit configuration must be inspected before deployment; do not weaken or change it. Confirm that no service data-event configuration records sensitive payloads.

CORS allows only `https://ioleia.com`; `www.ioleia.com` did not resolve during this task. An explicit backend Origin check also rejects other origins. These are browser protections, not authentication: a script can forge Origin. The route target is one request/second, burst five, best effort. No CAPTCHA, tracker, IP logging or profile collection.

API access logs are not enabled. The handler never logs the request, address, lookup key, exception or stack trace. Lambda platform logs can contain only invocation metadata. HTTP query strings are rejected, email goes only in the HTTPS JSON body, and the browser omits cookies and referrer. Verify these claims against the deployed service before launch; local tests cannot prove provider behavior.

## Record and consent

Only `email_key` (SHA-256), `email_ciphertext` (KMS ciphertext), `created_at` (UTC), `status` (`active` initially), `source` (`ioleia.com`), and `consent_version` are inserted. Hashes are pseudonymous, not anonymous; known candidate addresses can be guessed. The lookup hash remains private.

Trim whitespace and lowercase the domain only. Preserve local-part case, plus addressing and dots. Validate ASCII dot-atom email addresses, ordinary DNS domains, a 64-character local part and 254-character total limit. Internationalized or quoted addresses are intentionally rejected rather than reinterpreted.

An atomic conditional insert preserves the first record and its consent. A duplicate gives the same friendly response and does not overwrite timestamps, ciphertext or an unsubscribed status. No email is sent. A third party can submit another person's address; these intake records are not proof of mailbox ownership or a legal determination of valid consent.

Exact disclosure/version are in `docs/signup-consent-contract.json`. The privacy contact is the already-public `heather@ioleia.com`. Withdrawal requests can be handled by an authenticated administrator against the private register; preserve an `unsubscribed` suppression state when needed. Do not reactivate suppression through repeated anonymous submissions. Do not put a real address in shell arguments/history or exported logs.

**Before any commercial sending:** counsel must review CASL/privacy sufficiency (including required mailing/contact details and the form of consent), and a working unsubscribe/suppression mechanism must be verified. This task supplies no sender, campaign, admin dashboard, or marketing-email permission. Existing SES production-access work is for transactional authentication mail and must remain separate.

## Release procedure for the next authorized continuation

Deploy only this reviewed template after account/region verification and inspection of account-level logging. Preserve the resource receipt. Test the API using a reserved example-domain address, confirm one encrypted minimal item and identical duplicate response, invalid-input rejection, CORS behavior, and no raw email in relevant logs. Remove the fictional record and verify absence.

Build to a fresh directory with `tools/build-production.py --endpoint <verified-endpoint> --output <new-directory>`. The build removes draft labels and noindex, writes the exact endpoint config and CSP origin, and copies only the public assets. This command does not deploy or attest that the endpoint works. Replace the branch's public files with the verified build only when ready; then validate desktop/mobile, failure retention, motion/focus, reduced motion, cookies/storage and network traffic. Update current evidence and PR metadata, confirm the expected remote head, mark PR #2 ready, merge, and verify the actual GitHub Pages HTTPS deployment. No DNS change is expected.

Preserve separate offline preview artifacts; they must never be mistaken for the published build.
