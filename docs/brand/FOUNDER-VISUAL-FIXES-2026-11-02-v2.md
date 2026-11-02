> Historical record. This describes an earlier preview, not the current implementation. See [current validation](../review/CURRENT-VALIDATION.md).

# Founder visual fixes — 2 November 2026, v2

Draft PR #2 only. Started from verified head `ef6a7a0f0dacfdc026e9f767e2acae6dd51bba6f`. This record supersedes earlier descriptions of the website's displayed artwork and background; earlier documents and assets remain preserved as history.

## Approved scope

- Plain `#09092b` midnight-indigo background. All Light Field markup, background layers, and drift animation were removed.
- Copyright-only footer: `© 2026 Ioleia Inc.` remains at the right.
- Original approved A2.1 PNG crop in the header beside the unchanged `ioleia` wordmark, and as the favicon.
- Centered square crop of the existing approved luminous orb artwork. No generation, tracing, recolouring, or substitute artwork.

## Header authority and fidelity

Source: `ioleia/god-agent`, `docs/brand/a2-1-master/reference/approved-symbol-crop.png`.

The website's `assets/ioleia-a2-1-approved-symbol.png` is byte-identical to that source (Git blob `5539fc96163108d080fcf261237cc4805d7f8fc1`). SHA-256: `bd5d4bf145f3245ddcaf07ae32197c2ae91a11e1e353fff5010a026e8dde0caa`.

Pixel comparison also confirms the source crop equals `(770, 100, 1120, 450)` of `ioleia-a2-1-approved-final-candidate.png`, whose SHA-256 is `f2259727a4926afd49f01936d8ed01609b34a6c6f6f7710fee17621f69fafccf`. Right and bottom are exclusive. Original black artwork and pale panel are retained, with no CSS colour filter or opacity treatment. The previous traced white SVG is no longer displayed.

## Centre orb fidelity and alignment

Source: unchanged `assets/reference/approved-light-field-board.png`, SHA-256 `c143c55fabaefd0a22cdbdb6876f356275cba61ed2d65a617daa229557252511`.

`assets/ioleia-luminous-orb-centered.png` is the exact 384 × 384 pixel crop `(120, 19, 504, 403)`. SHA-256: `db8fe7749e9014be21113e16bb4cef612187b02c84b81463e5c50053dfb0ea7f`. A full pixel comparison found no differences from that source rectangle. There is no resampling, stretching, repainting, or colour adjustment in the asset.

A centered radial CSS fade leaves the inner 90% radius opaque and fades the surrounding glow to transparent at 96%, avoiding board text and a visible square edge. The source board remains provenance only and is not requested by the page.

The luminous rim diagnostic (`max RGB > 220`, `max RGB - min RGB > 50`) has exclusive bounds `(21, 22, 363, 363)` in the square crop: left/top/right/bottom margins of 21/22/21/21 source pixels. This is a measurement of raster artwork, not an alteration to its shape. Browser measurements confirm a square display centered on the page at all reviewed widths. Desktop and mobile screenshots were visually inspected for extraction seams and clipping.

## Verification

- Existing browser suite: 77 passing assertions on the repository page, then the same 77 on the self-contained preview. Viewports: 1440×900, 1440×768, 768×1024, 390×844, 390×667, 320×740, 320×568; all three messages checked. No horizontal overflow or orb/text/form overlap; short screens scroll naturally.
- Offline preview: 20 additional checks at 1440×900, 390×844 and 320×740 verify original embedded PNGs, centered square orb, solid background, no clipped text, copyright-only footer, both draft notices, and no secondary file/network dependencies.
- Zero console or page errors and zero external requests. Screenshots include all three messages at desktop, 390px and 320px.
- Three-message crossfade, dwell times, fixed form position, pause/resume, focus/typing/submission pause, keyboard access, reduced motion, and no-JavaScript fallback remain functional. `preview.js` is byte-identical to the verified starting head (SHA-256 `864035cb2fe16757e630352b3b60b4142369d61adac9b0d1e007613b2aa8ea5a`).
- Both preview-only labels remain. The form has no endpoint and sends/saves nothing. CSP continues to block connections and form actions. The portable HTML permits its exact inline CSS/JS by SHA-256 hashes.

Browser checks use local headless Chrome, not physical-device certification. Hidden-page behavior uses the existing controlled visibility test. Founder visual review remains outstanding.

## Boundary

Keep PR #2 draft, unmerged and undeployed. No production changes, hosting changes, DNS, email, AWS, SES, Cognito, or Apple actions are included.
