# Ioleia website — single-scene founder preview

One continuous scene with the approved A2.1 geometry, the approved rich/wispy orb visual language, a slow Light Field, three gently changing messages, and one constant email signup. **Preview only. Keep PR #2 draft; do not merge or deploy until founder visual approval.**

Open `index.html` locally in a browser. All runtime assets are relative local files; no build, server, font service, or internet connection is required.

## Current visual treatment

The website no longer uses the thin deterministic luminous SVG as the displayed hero/header treatment.

Instead, the approved luminous orb artwork from `assets/reference/approved-light-field-board.png` supplies the light texture, depth, colour blending, and internal wisps, while the unchanged canonical A2.1 master at `docs/brand/ioleia-a2-1-master-monochrome.svg` is used as the CSS mask.

This keeps:
- exact A2.1 outer geometry and negative space;
- the approved richer internal light behaviour;
- the same orb appearance in the header and hero.

The existing `assets/ioleia-a2-1-luminous.svg` is retained for provenance/history but is no longer the visible website orb.

Rejected `colour-v1` assets remain unused.

## Message and interaction behavior

Moments 1, 2, and 3 dwell for 16, 20, and 14 seconds, followed by 1.2-second opacity crossfades. The sequence loops. A shared grid reserves the tallest message height so the orb and signup stay in place. Three small indicators provide direct nonanimated access.

Pause Motion freezes both Light Field and message rotation. Focusing the form pauses both. Typing, invalid submission, or completed preview submission keeps motion paused until explicit resume. Hidden pages pause. Reduced Motion starts at Moment 1 with no animation; all three messages remain accessible through the indicators.

## Signup boundary

There is exactly one email input and one **Join early access** button. There is no first-name field, checkbox, or second marketing CTA.

This draft form is intentionally fake:
- nothing transmitted;
- nothing persisted;
- no endpoint;
- no analytics;
- no cookies;
- no storage.

The visible labels **“Design preview · Signups are not live”** and **“Preview only. Nothing is sent or saved.”** are draft-only safeguards. They are marked `preview-only` in the HTML and must be removed/disabled in the production build once the real signup backend is approved and working.

The production site must not show those preview notices.

## Deployment boundary

This branch adds no deployment workflow or production integration. `CNAME`, live GitHub Pages, hosting, DNS, email records, AWS, SES, Cognito, Apple, and other production systems remain untouched.
