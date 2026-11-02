# Single-scene validation — 2 November 2026

This report applies to the single-scene refinement of Draft PR #2, starting from verified head `dc62ddf507981e7e7164004c1de924b4dfa2cffb`. Previous reports and screenshots remain historical evidence. A final-head receipt, fresh screenshots, and offline files are supplied separately after publication to the draft branch.

## Browser checks

77 assertions passed in local Chrome, using Playwright with controlled dwell timers and real browser animation frames. Zero page errors, console errors, or external network requests were observed.

- 1440×900, 1440×768, 768×1024, 390×844, 390×667, 320×740, and 320×568. Each of the three messages was checked at every size. No horizontal overflow or orb/text/signup overlap. The signup position is identical across messages at each size. Inputs remain at least 200px wide and buttons at least 44px tall.
- Desktop and tablet show the whole scene without scrolling at tested sizes. At 390×844 and 320×740 the email and button are within the screen. Shorter mobile viewports use normal vertical scrolling without clipping; the form remains reachable when the virtual keyboard reduces available height. These are browser viewport checks, not physical iPhone acceptance.
- Real 1.2-second opacity overlap was observed, with 16/20/14-second dwell timers, order 1→2→3→1, and a stable signup position.
- Focusing the form freezes both CSS motion and text. Typing remains paused after blur. Explicit resume works. Pause Motion freezes both systems. Invalid and successful submissions stay paused. An untouched empty form may resume with a fresh full dwell after blur.
- Native missing-value and email-format validation focus the field. Enter submission shows only the truthful preview confirmation, clears the email, and focuses the live status. One form, one email input, one signup CTA. No cookie creation.
- Keyboard skip link, message controls, and visible focus outlines work. Labelled controls offer access to each message; automatic messages do not announce repeatedly through a live region. Inactive visual messages are inert and excluded from the accessibility tree.
- Changing to reduced motion selects Moment 1, removes every animation, and prevents automatic rotation. Other messages remain available through static labelled controls.
- Hidden-document state freezes the timer and an in-progress fade; foreground state resumes it. The controlled visibility test covers an in-progress fade; physical tab switching is not part of the automated viewport suite.
- With JavaScript disabled, all three approved messages are readable in order, with no horizontal overflow. The input and button are disabled and the fallback says the form is off.

## Geometry, privacy, and integrity

`tests/geometry.py` validates the canonical file checksum, exact path attributes and geometry checksum, unchanged viewBox, even-odd clipping, no transforms or additional paths, and the hero/favicon references. A 700px browser raster comparison found zero pixels outside the canonical shape and zero missing opaque interior pixels. The side-by-side comparison was visually reviewed; two fields, negative space and handoff match the master. See the new brand provenance document for the rendering method and its review status.

JavaScript syntax and `git diff --check` pass. The runtime contains no external URLs, endpoint, network API, analytics, storage API, cookie API, or third-party font. All files needed for an offline preview are local. CSP defaults to none, allows only local styles/scripts/images plus data images, and blocks connections and form actions. Input has no submission name. The new rendering contains no raster logo or colour-v1 asset.

The static SVG's filters render once as an image. Three slow transform-only background layers are animated. There is no requestAnimationFrame loop, WebGL, animated filter, or hidden-page timer churn.

## Limits and deployment boundary

This is focused browser and keyboard validation, not a full screen-reader certification, physical-device test, or final founder approval of the new rendering. System Georgia remains the provisional wordmark/heading font.

No production integration or deployment workflow is added. CNAME is unchanged. The work updates the existing draft branch only; no merge, GitHub Pages or Amplify deployment, DNS/email-record change, AWS/SES/Cognito/Apple action, or other production change is part of this task.
