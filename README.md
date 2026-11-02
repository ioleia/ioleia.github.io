# Ioleia website — single-scene founder preview

One continuous scene with a fixed A2.1 orb, a slow Light Field, three gently changing messages, and one constant email signup. **Preview only. Keep PR #2 draft; do not merge or deploy.**

Open `index.html` locally in a browser. All runtime assets are relative local files; no build, server, font service, or internet connection is required. Keep `styles.css`, `preview.js`, and `assets/` beside the page. The supplied offline review bundle contains the same runtime files from the final PR head.

## Message and interaction behavior

The approved copy is unchanged. Moments 1, 2, and 3 dwell for 16, 20, and 14 seconds, followed by 1.2-second opacity crossfades. The sequence loops. A shared grid reserves the tallest message's height, so the orb and signup stay in place. Three small indicators offer direct, nonanimated access to the messages and stop automatic motion.

Pause Motion freezes both the Light Field and message rotation, including an in-progress fade. Focusing the form also freezes both. Leaving an untouched, empty form resumes with a full reading interval. Typing, an invalid submission, or a completed preview submission keeps motion paused until an explicit Resume Motion action. Hidden pages pause timers and running animations; returning preserves the remaining dwell or fade.

Reduced motion starts at Moment 1 with no animation. All three messages remain accessible through the labelled indicators without animation. With JavaScript disabled, all messages are readable in normal document flow; the form is disabled and explains its preview status. Small or short screens may scroll naturally; content is never clipped to a fixed screen height.

## Signup boundary

There is exactly one email input and one **Join early access** button. There is no first-name field, checkbox, or second marketing CTA. Supporting copy remains “Coming first to iPhone.” and “I’ll email you when Ioleia is ready to try. Unsubscribe anytime.”

The form uses native email validation. Valid submission only shows “Preview complete. Nothing was sent or saved, and you have not joined a list.” It clears the field and focuses that confirmation. No email is transmitted, persisted, logged, or echoed. Autocomplete is disabled in this preview. There is no endpoint, network API, analytics, cookie, or storage access. CSP blocks connections and all form submissions even if the script fails. Future production subscription work remains separate; `docs/signup-consent-contract.json` is still a proposal, not an implemented service.

## Brand and review evidence

The hero and favicon use the exact canonical A2.1 path with a deterministic luminous treatment. See `docs/brand/PROVENANCE-SINGLE-SCENE-2026-11-02.md`. The generated board is used only for the approved atmospheric Light Field. Rejected colour-v1 assets are absent. Permanent wordmark typography remains undecided.

See `docs/review/VALIDATION-SINGLE-SCENE-2026-11-02.md`. Earlier review documents and screenshots are preserved as history; they are not evidence for this scene. Fresh screenshots and an offline bundle are captured from the exact final PR head and delivered separately to avoid a self-referential screenshot commit.

To run browser checks, use an installed Playwright package: `node tests/scene.spec.cjs`. `PLAYWRIGHT_MODULE`, `BROWSER_PATH`, and `QA_OUTPUT` may select local tooling and output paths. No dependencies are loaded by the website.

## Deployment boundary

This branch adds no deployment workflow or production integration. `CNAME`, main, hosting, DNS, email records, AWS, SES, Cognito, Apple, and other production systems are outside this refinement and must remain untouched.
