# Current validation — website launch candidate, 3 November 2026 UTC

**Prepublication checkpoint: live AWS backend PASS; production browser checks PASS.** The containing commit is the tested production candidate for PR #2. GitHub Pages publication and the direct public-site signup check follow this checkpoint; their exact merge/deployment identifiers and cleanup result belong in the PR/task receipt, not in a self-referential commit hash.

## Authority and bounded scope

Remote PR #2 was verified as draft/open at `6132039239d8096c13669d7163fe700dd647a8b2`, with main `363f79ea5e8c0cf2687879963fe33e7bf1fdd5db`, before work and again immediately before preparing this commit. No unknown remote changes were present. The founder explicitly authorized the website stack, fictional tests and cleanup, and publication after the focused checks pass.

The deployed template is byte-for-byte the reviewed template at that head. SHA-256: `8fb567b355441f711d36f4e1f3fbc6c9ec79709833a59ff207d63511cdca7e23` (12,701 bytes). The AWS Console Template Studio export was compared byte-for-byte before submission. The console validated the unedited template. No AWS CLI/SDK credential grant, permanent key, new IAM user, SSO-assignment change, CloudShell deployment or global logging change was used.

## Actual live AWS evidence

Account **156397421775**, region **ca-central-1**. Stack **ioleia-website-early-access: CREATE_COMPLETE**. Stack ID: `arn:aws:cloudformation:ca-central-1:156397421775:stack/ioleia-website-early-access/73e91520-d71b-11f1-a8f4-021b346e2433`.

Before creation, the authenticated console showed no colliding stack, table, Lambda, log group or KMS alias/key. API Gateway had no existing APIs; account logging role was unset. CloudTrail trails/Lake stores and CloudWatch pipelines were empty, with resource discovery/enablement rules not enabled. No enabled inspected configuration was found that would record raw signup request bodies. These were bounded read-only checks, not a claim to have audited every AWS service.

Resources: KMS key and alias `alias/ioleia-website-early-access`; retained, deletion-protected pay-per-request DynamoDB table `ioleia-website-early-access`; Lambda and its scoped execution role; HTTP API, integration, POST route, default stage and invoke permission; 7-day Lambda log group `/aws/lambda/ioleia-website-early-access`. Runtime permissions are limited to this table's PutItem, this key's Encrypt, and this log group's CreateLogStream/PutLogEvents. No decrypt/read/delete/SES/Cognito runtime access.

Endpoint: `https://ymcj9la56g.execute-api.ca-central-1.amazonaws.com/early-access`.
KMS ARN: `arn:aws:kms:ca-central-1:156397421775:key/3a9e232c-cce1-41a7-ac2e-1800ff64a89a`.
Only POST /early-access; allowed browser origin https://ioleia.com; throttle 1 request/second, burst 5. API access logging is disabled.

[Live backend record](live-aws-2026-11-03/backend-pass.json) and [stack outputs](live-aws-2026-11-03/stack-outputs.json):

- Certificate-validated real POST with the website's Origin, JSON content type, email and consent version returned HTTP 200 and `Thanks. Your early-access request has been received.`
- Exactly one item held only `email_key`, `email_ciphertext`, `created_at`, `status`, `source`, `consent_version`. The stored email was Binary KMS ciphertext, not plaintext, and was never decrypted. Consent was exactly v4 below.
- A duplicate returned the identical generic response. There was still one item; creation time and ciphertext were unchanged.
- Malformed input returned HTTP 400. Approved-origin preflight returned 204 with the exact allow-origin; an unapproved origin received no allow-origin header. A real localhost browser cross-origin request was rejected with TypeError.
- The first ten actual Lambda log events contained only INIT_START/START/END/REPORT metadata, no raw email or request body. A follow-up inspection after the preview request found 14 events, still only runtime metadata and no raw email. The console confirmed one-week retention and no subscription filters. API access logging was explicitly disabled.
- The first fictional record was deleted through the authenticated admin console; a refreshed scan returned/scanned zero items. A second reserved preview record was also inspected and deleted; a fresh completed scan again returned/scanned zero. No real contacts were used.

The Python HTTPS attempt failed before sending a request because its local certificate trust file was absent. Evidence was preserved and the test changed to the macOS system HTTPS client with certificate validation enabled. No verification bypass was used. Later the AWS browser session expired during a log read; it was renewed through the existing SSO portal without any new access grant.

## Production build and browser checks

The prepared production builder used the verified endpoint. The output removes both preview notices, noindex and the draft privacy notice, and configures CSP connect-src to only the exact API origin. The source served by Pages is now that production output.

One real frontend defect was found before publication: site.js still required consent v3 while the reviewed contract/config/backend had moved to v4. This disabled the initial production candidate. The failed artifact was preserved, and only the readiness constant and corresponding existing test expectation were aligned to v4. No backend-template correction was needed. The obsolete draft-disabled assertion was removed because the repository root is now the production build.

The plain midnight navy, transparent ivory A2.1 mark, centered orb, exact frozen message markup/copy, one CTA, no-checkbox consent and copyright-only footer are preserved. Artwork bytes, styles and CNAME are unchanged from the reviewed head. No aurora background was added.

Current checks used the actual browser through the supported computer interface:

- All three messages at 1440×900, 390×844 and 320×740: no horizontal overflow or orb/text/form overlap, stable signup position, usable controls. [Layout measurements](live-aws-2026-11-03/layouts.json), [desktop](live-aws-2026-11-03/layout-1440.jpg), [390px](live-aws-2026-11-03/layout-390.jpg), [320px](live-aws-2026-11-03/layout-320.jpg).
- The normal timer reached messages one, two and three; sampled fractional opacities proved real crossfades. Form focus paused motion. Chrome reduced-motion emulation kept the first message static beyond its normal dwell, hid motion controls and allowed static manual access to message three; emulation was restored afterward.
- The unmodified production HTML/CSS/client/config was checked locally. Chrome's native folder picker stalled, so local overrides were abandoned. For the prepublication live form check only, a separate test fixture added a local transport bridge and allowed its own origin in the fixture CSP. The exact production client/config/form sent to the real API through that bridge, with the approved Origin. The real HTTP 200 reached the UI and cleared the field. [Transport evidence](live-aws-2026-11-03/preview-live-response.json). This proves frontend/live-backend behavior through a test transport; the direct public-origin browser check remains the postpublication gate. No bridge or fixture CSP is in production.
- An intentional test-transport 503 produced the calm retry message, retained the visible fictional address and restored usable controls.
- Chrome Application inspection found zero local/session storage entries, zero site cookies and zero stored bytes. Network inspection after reload showed only the document, CSS, two scripts and the two local images (favicon reused). No analytics/tracking requests or raw email in URLs. The exact production CSP also blocked Chrome DevTools' own localhost discovery request, as expected.

The existing 15 fake-AWS tests and 82 intercepted-browser assertions are **earlier simulated evidence**, not newly run tests and not proof of live AWS. Their prior report and manifest are preserved at [pre-AWS history](history/pre-aws-console-2026-11-02/CURRENT-VALIDATION.md). The current live/browser evidence above is separate.

## Consent and sending boundary

Version: **ioleia-early-access-v4-2026-11-02**.

> By joining, you agree to receive launch updates from Ioleia Inc. You can unsubscribe at any time.
>
> Ioleia Inc. · 532 Montreal Rd, Unit 383, Ottawa, ON K1K 4R4 · heather@ioleia.com

No checkbox. The Early Access Privacy page describes this encrypted Canada Central register, its six fields and the public contact route for withdrawal/removal. Joining does not create a product account. No marketing email was sent or enabled. Counsel review and a working unsubscribe/suppression path remain required before launch messages; transactional-auth SES is not used for them.

`real_data_admission=false` remains unchanged. No unrelated God Agent infrastructure, Alpha gates, protected inference, Cognito, SES, DNS/email records or hosting settings were changed. Existing GitHub Pages remains the publication mechanism.
