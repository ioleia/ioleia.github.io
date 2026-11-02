# Ioleia website — single-scene founder preview

One continuous scene with:
- the real A2.1 logo mark beside `ioleia` in the top-left header;
- the approved luminous orb artwork as the centre visual;
- a slow Light Field;
- three gently changing messages;
- one constant email signup.

**Preview only. Keep PR #2 draft; do not merge or deploy until founder visual approval.**

## Brand hierarchy

The header logo and centre orb are intentionally different roles:

### Header
The small mark beside `ioleia` is the canonical A2.1 brand mark:
`assets/ioleia-a2-1-mark-dark.svg`.

### Centre
The large centre orb is the approved luminous orb artwork from:
`assets/reference/approved-light-field-board.png`.

It is displayed as the visual centerpiece and is no longer forced through the A2.1 vector mask. This preserves the richer internal light, dimensional depth, and softer colour flow the founder approved.

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
