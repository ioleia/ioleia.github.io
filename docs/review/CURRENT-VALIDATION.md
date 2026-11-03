# Current validation — public website preparation, 2 November 2026

**Status: prepared and tested offline; NOT deployed. PR #2 remains draft. AWS changes are pending at the founder’s explicit request.** This record applies to the source manifest in this directory and the commit that contains it. The verified final branch SHA is recorded in PR #2’s description and the external task receipt; a document cannot contain its own commit hash.

## Starting authority and scope

Verified remote PR #2 head before edits: `4acee64ef24a5885caafb51f327b62d4f5b8b99d`. Base/main: `363f79ea5e8c0cf2687879963fe33e7bf1fdd5db`. No unexpected delta was present.

The plain `#09092b` background, centered luminous orb and its crop/CSS, and all three approved message sections are unchanged. The header/favicon are now the exact-source-derived transparent ivory treatment. The page has one email input, no first name, no checkbox, one signup CTA, three-message crossfades and a copyright-only footer. One consent statement and a small adjacent Early Access Privacy link were added.

The source draft keeps both preview notices because no backend exists. It disables the form instead of faking success. The production-build fixture removes both notices and noindex, configures an exact endpoint origin in CSP, and exercises the real POST code through intercepted responses. **The fixture is not a live build or a deployable API endpoint.** Screenshots named `proposed-*` show this intended production appearance; they are not screenshots of ioleia.com.

## Artwork evidence

- Approved source PNG SHA-256: `bd5d4bf145f3245ddcaf07ae32197c2ae91a11e1e353fff5010a026e8dde0caa`.
- Original board SHA-256: `f2259727a4926afd49f01936d8ed01609b34a6c6f6f7710fee17621f69fafccf`. The crop `(770,100,1120,450)` is pixel-identical to the approved source.
- Output: `assets/ioleia-a2-1-header-ivory.png`, 350×350. No resizing, tracing, smoothing, dilation, erosion or substitute geometry. Every output alpha value is mapped directly from the source pixel’s luminance; foreground is `#f8f1e8`.
- Visible contour mask: zero changed pixel coordinates at the inclusive 128 source-luminance boundary. Bounds `(21,16,334,339)`. Seven additional checks verify the saved alpha thresholds against the direct mapping; these are representation checks, not seven independent geometry tests.
- The source is flattened RGB. Recovering its unknown authoring alpha is mathematically underdetermined; the derived matte must not be called recovery of that latent alpha. Source edge gradations are mapped directly, pale background is removed, and the right-side handoff and negative space were visually inspected.
- [Mask/paint comparison](../brand/header-matte-comparison.png) and [machine record](../brand/HEADER-MATTE-2026-11-02-v1.json).

## Focused checks completed

**15 Python test cases passed**, using fake AWS clients. They cover conservative normalization, syntax/length boundaries, duplicate and unsubscribed-record preservation, constant response, malformed/extra/duplicate JSON rejection, wrong consent/origin/transport rejection, exactly six record fields, KMS-before-insert ordering, generic errors and no stdout/stderr email leakage, and the template’s limited IAM/CORS scope. These do not demonstrate real AWS encryption or persistence.

**82 browser assertions passed** against the local production-build fixture. This count includes repeated viewport/message assertions, not 82 independent product tests. Viewports: 1440×900, 1440×768, 768×1024, 390×844, 390×667, 320×740 and 320×568. No overflow or orb/text/form overlap; the signup position stays stable across messages. Short screens scroll naturally. The 16/20/14-second dwell sequence, 1.2-second crossfade, focus/typing/submission pause, pause/resume, keyboard access, reduced motion and no-JavaScript fallback passed. The hidden-document test is controlled, not physical-device certification.

The intercepted success request used POST with email and consent version only, no address in its URL. Success clears the field; failure retains it and restores the controls. The draft’s missing-endpoint path stays disabled. No cookies, local storage, session storage, unexpected requests or unexpected console/page errors were observed. The expected simulated HTTP 503 is excluded from unexpected console errors. These results apply only to the tested build and isolated browser.

Static comparisons also confirm frozen message markup, orb bytes/style and CNAME unchanged, no tracking/storage code, one field/CTA, correct footer, and exact production CSP origin. Desktop/390/320 screenshots were visually reviewed. The in-app browser cannot open local `file:` previews under its URL policy; the local artifact and screenshots remain available.

## AWS and live checks — NOT completed

The authenticated AWS browser session was verified as account **156397421775**, **ca-central-1**, role `AWSReservedSSO_AdministratorAccess_19cd19193fd5f22f/heather.scott`, after founder-completed MFA.

CloudShell reported that account verification is in progress. Automatic approval review rejected the new local AWS SSO client grant because it could expose all assigned roles. The grant was denied and its login process canceled. The founder then chose **“Keep AWS changes pending.”** No CloudFormation stack, API, Lambda, role, key, table, contact record or mail sender was created by this task.

Normal certificate-valid HTTPS returned HTTP 200 for the existing `https://ioleia.com` company page. `www.ioleia.com` did not resolve, so it is not in the proposed CORS list. No DNS, GitHub Pages settings, email or hosting changes were made.

Live signup success, one encrypted database item, duplicate idempotence, server rejection, browser CORS, actual AWS logs, and test-record deletion remain **pending**. No test records exist from this task, so there was nothing to delete. Do not infer live functionality from the offline tests.

## Consent and sending boundary

Prepared version: **`ioleia-early-access-v4-2026-11-02`**.

> By joining, you agree to receive launch updates from Ioleia Inc. You can unsubscribe at any time.
>
> Ioleia Inc. · 532 Montreal Rd, Unit 383, Ottawa, ON K1K 4R4 · heather@ioleia.com

This keeps the founder-approved no-checkbox opt-in and adds the company mailing address plus email contact beside the consent request, aligning the prepared form with current CRTC guidance on identification/contact information. No separate checkbox. Each proposed record stores the server-recognized version; the exact text is preserved in the contract and handler. It is **not live** and is **not a legal-sufficiency determination**.

The privacy notice is limited to this register. The already-public contact `heather@ioleia.com` is the withdrawal/contact route. Before commercial launch messages, counsel must review consent/privacy sufficiency, including mailing/contact information, and a working unsubscribe/suppression mechanism must be verified. CRTC guidance includes contact information in requests for consent: [CRTC 2012-548](https://crtc.gc.ca/eng/archive/2012/2012-548.htm). No marketing sending is built or authorized; existing SES work concerns transactional auth mail only.

## Historical evidence

All earlier review documents, browser JSON, contrast data, screenshots, consent proposal and obsolete tooling are scoped under [history](history/pre-public-launch-2026-11-02/README.md). Older brand documents carry explicit historical banners. They may refer to an aurora, SVG hero, first name, checkbox or obsolete form; those are not current requirements or proof.

The historical “97 checks” means **77 repository/browser checks + 20 self-contained-preview checks**, with some repetitions across preview forms. It never meant 97 independent product tests or live signup validation.

`real_data_admission=false`. God Agent protected processing, inference, Cognito qualification, transactional SES, Apple/company verification and all core Alpha gates remain untouched.
