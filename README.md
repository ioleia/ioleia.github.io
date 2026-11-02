# Ioleia website — founder review preview

A buildless, one-page founder-review preview. **Signups are not live. Do not merge or deploy this branch yet.**

## Current direction

The page is intentionally minimal:

1. Meet Ioleia and understand the core promise.
2. See the honesty/difference statement.
3. Join the early-access list.

There are no section tabs, feature grids, Light Field explanations, product jargon, or competing marketing calls to action.

The only marketing action is **Join early access**, with the email field available in the hero and repeated at the bottom for visitors who decide after scrolling.

Public copy is first-person Ioleia voice, short and plain-language. It does not use “Alpha” or “AI companion” as marketing positioning.

## Signup boundary

Both email forms are **preview-only**.

- email only;
- no first-name field;
- no consent checkbox in the founder-approved UX direction;
- no network request;
- no storage;
- no cookies;
- no analytics;
- no endpoint;
- CSP blocks connections and form submission;
- JavaScript-disabled state leaves submit controls disabled.

The production signup flow still requires the separately approved backend, unsubscribe handling, final disclosure text, and legal/CASL review. This preview does not claim legal sufficiency.

## Brand and motion

The page continues to use the approved luminous orb and wispy Light Field reference. A2.1 remains the canonical geometry authority. Rejected `colour-v1` assets are not used.

The Light Field is visual only; the page does not explain it. Motion is slow and decorative, pauses when hidden/offscreen, includes a pause control, and respects reduced-motion preferences.

The permanent wordmark typeface remains unapproved. The current Georgia/system-serif treatment is provisional.

## Review and validation

See `docs/review/VALIDATION-2026-11-02.md`.

The older screenshot files under `docs/review/` are retained as historical evidence from the earlier, more complex layout. They do **not** represent this final simplified copy/layout and must not be used as founder visual approval.

## Live boundary

The public rollback remains GitHub Pages on `main` at the existing live site. This draft branch contains no deployment workflow or production integration.

Do not merge, deploy, switch hosting, or change DNS/email records until founder visual approval and the separately authorized hosting/signup work are complete.
