# Ioleia website — founder review preview

A buildless, local-only website preview. **Signups are not live. Do not merge or deploy this branch.**

## Review

- [Desktop](docs/review/desktop.jpg), [tablet](docs/review/tablet.jpg), [phone](docs/review/phone.jpg)
- [Validation record](docs/review/VALIDATION-2026-11-02.md)
- [Brand provenance and limits](docs/brand/PROVENANCE-2026-11-02.md)
- [Future consent contract](docs/signup-consent-contract.json)

Run `python3 -m http.server 8765 --bind 127.0.0.1` from this directory and open `http://127.0.0.1:8765`. No installation, build, third-party font, API key, or backend is needed. `index.html` also works directly from disk.

## Scope and continuity

The branch descends from `website/full-site-2026-11-02` at `e1a3245f3136fda6571ebe0d6e0c51c4106991ab`. That branch and its earlier commits are preserved. The buildless HTML/CSS structure, shell layout, anchor navigation, headline, company facts, contact links, and development-stage framing were retained or adapted. The generic orb/rings and unapproved marks were removed from this branch; their history remains available.

The public rollback is GitHub Pages on `main` at `363f79ea5e8c0cf2687879963fe33e7bf1fdd5db`. Pages settings were inspected read-only and showed `main` / root as the publishing source. `CNAME` remains byte-identical. This branch adds no deployment workflow, hosting configuration, or production integration.

## Preview behavior

The page contains the hero, continuity/truthfulness/agency/privacy principles, a Light Field study, Ioleia Inc. company information, and the prelaunch form. Product language describes intentions and work in development; it does not assert that production privacy or Alpha admission gates have passed.

The Light Field uses CSS windows onto the untouched approved reference image, with static atmospheric overlays and slow transform/opacity animation (23–43 seconds). The orb is not animated. No WebGL, canvas render loop, hue cycling, or animated blur is used. Motion pauses outside the viewport and in hidden tabs. A visible pause control is supplied; reduced-motion preferences remove all animations and transitions. The study's response button shows one small, locally brightened area. It is labeled as a visual study, not an AI interaction or product screenshot.

The form requires email and an unchecked consent checkbox; first name is optional. It only validates locally, clears the fields, and announces that nothing was sent or saved. There are no network calls, storage writes, cookies, analytics, or signup endpoint. CSP disallows connections and form submission, and the button is disabled when JavaScript is unavailable. The consent version is attached to the form; the proposed future record is documentation only.

## Before any live deployment

Founder visual review is required. The remaining identity decision is approval/licensing of the permanent wordmark typography; the current Georgia/system-serif treatment is provisional. The A2.1 geometry decision is closed.

Technical launch work remains separate: faithful production artwork export/geometry qualification, an approved subscription backend with consent and unsubscribe handling, final privacy/contact disclosures, removal of preview-only/noindex behavior only when appropriate, and a separately authorized hosting cutover. Do not infer permission to perform those steps from this preview. Alpha privacy/authentication/inference gates are unchanged.
