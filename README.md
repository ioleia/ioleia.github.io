# Ioleia website — single-scene founder preview

One continuous scene with:
- the original approved A2.1 raster artwork beside `ioleia` in the top-left header;
- the approved luminous orb artwork as the centre visual;
- a plain midnight-indigo background;
- three gently changing messages;
- one constant email signup.

**Preview only. Keep PR #2 draft; do not merge or deploy until founder visual approval.**

## Brand hierarchy

The header logo and centre orb are intentionally different roles:

### Header
The small mark beside `ioleia` uses the original approved source crop, without tracing, recolouring, filters, or opacity changes:
`assets/ioleia-a2-1-approved-symbol.png`.
It is byte-identical to `ioleia/god-agent`'s `docs/brand/a2-1-master/reference/approved-symbol-crop.png`, retaining the source's black symbol and pale panel.

### Centre
The large centre orb is a square, unscaled crop of the approved luminous artwork:
`assets/ioleia-luminous-orb-centered.png`, from `assets/reference/approved-light-field-board.png` at `(120, 19, 504, 403)` (right/bottom exclusive).

It is displayed without stretching, colour filters, or an A2.1 vector mask. A centered radial fade softens only the surrounding glow. The board is retained as provenance; the website no longer loads or displays its Light Field.

See [the versioned visual-fix record](docs/brand/FOUNDER-VISUAL-FIXES-2026-11-02-v2.md) for source fidelity and validation. Earlier brand and review documents remain historical evidence.

A2.1 remains the canonical logo geometry for the actual brand mark and app-icon geometry. The luminous centre orb is the expressive visual object used by the website.

Rejected `colour-v1` assets remain unused.

## Preview notices

The visible labels:
- `Design preview · Signups are not live`
- `Preview only. Nothing is sent or saved.`

are draft-only safety labels. They remain visible while the signup is fake.

They are marked `preview-only` in HTML and must be removed/disabled in the production build once the real signup backend is approved and working.

The live production website must not show those preview labels.

## Message and signup behavior

Moments 1, 2, and 3 dwell for 16, 20, and 14 seconds with 1.2-second opacity crossfades. The sequence loops.

Pause Motion, form focus, typing/submission, hidden-page behavior, reduced-motion handling, and the one constant email signup remain unchanged.

## Deployment boundary

This branch remains draft-only. Do not merge or deploy until founder visual approval. Live site, DNS, email, AWS, SES, Cognito, Apple, and production systems remain untouched.
