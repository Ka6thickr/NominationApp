# Validate the manual build before sharing

The documentation and generated formula structure can be checked locally, but Canvas Studio compilation, connector schemas, permissions and runtime behavior must be tested in the target environment. No live app test is claimed by this package. Check each stage before duplicating a broken pattern across six forms.

## 1. Studio construction checks

1. Confirm Ka6thickMSFT and the correct AISite connections/environment variables.
2. Resolve every red formula error in App checker. Verify control names, classic-control properties, generated DataField strings, lookup `.Id`, choice `.Value`, person record shapes and TeamMembers table shape. Keep the schema fixed; correct formulas against actual generated metadata.
3. Run App.OnStart, then Preview from Home. Check signed-in name/email and the all-zero admin placeholder (admin UI hidden until configured).
4. Verify Native Attachment control lives inside its own typed Edit form, Items references the generated card Default, Update returns `.Attachments`, and it has not been replaced with a generic file-upload control.
5. Inspect delegation warnings separately from syntax errors. Do not fix warnings by collecting all nomination records or setting the data row limit to2000 and assuming completeness.
6. Save app version “Manual build — before runtime tests” (or an equivalent clear version note).

## 2. Layout and accessibility matrix

Test browser zoom100%, widths about1366,1024,760,390 and the actual intended Power Apps player(s).

| Check | Expected |
|---|---|
| Header/nav | Contoso retained; current signed-in person; no prototype names |
| Page shell | Centered content, white cards, neutral page background, no horizontal overflow |
| Stepper | Step1 green / step2 current / step3–4 pending matches the supplied example; all four current states tested |
| Stepper return | Revisiting a completed stage highlights the current stage without implying submission |
| Mobile | Category cards stack; details fields stack; progress appears above form; buttons remain reachable |
| Questions | Long headings/guidance wrap; inputs have usable height; character counters correct |
| Review | Full2,000-character answers visible; no five-line clipping; no missing optional/required markers |
| Files | Long filenames readable; file editor remains operable; mobile upload behavior verified |
| Keyboard | Logical tab order, visible focus, native buttons activate, no hidden overlay traps |
| Screen reader | Meaningful field labels, required meaning announced, current stage/state text available |
| Colors | Current/completed/errors have text/icon meaning as well as color |

Use the original CSS as the initial dimensions/color baseline. The screenshot/CSS accent discrepancy is a visual review item; change the single theme definition after choosing the desired accent. Native shadows and text metrics need visual adjustment.

## 3. Per-category functional acceptance

Run every row for **all six codes**, using synthetic test nominations and a small harmless test attachment. Record the reference, source list and result; do not put personal nomination content into a public test report.

| Test | Expected |
|---|---|
| No published category | Clear no-active-categories message; no hardcoded fallback questions |
| Valid version | Exactly3–6 current questions loaded in Q1..QN order; malformed set blocked |
| Incomplete step1 | Continue permits category selection; incomplete draft can then save |
| First Save draft | One Draft item, captured category/version/count/snapshots, no SubmittedOn/declaration |
| Subsequent draft save | Same ID; no duplicate; data and files updated |
| Reopen draft | Saved snapshot wording and required flags restored; same ID; native files visible |
| Directory people | Valid person claims save; TeamMembers saves as multi-person; duplicates prevented locally |
| Whitespace response | Required answer containing only spaces, tabs or line breaks is rejected |
| Length limit | Input/counter enforce configured2,000-character maximum; existing unusual data handled explicitly |
| Unsaved review | Most recent focused text and attachment additions/removals shown correctly |
| Edit after review | Declaration resets; original form/file state remains intact |
| Submit | Draft/files save first; same item gets Submitted, declaration true and timestamp; confirmation after success |
| Reopen submitted | View mode, file download available, no save/edit/submit controls |
| New after submit | Fresh blank form; no old answers, category, people or files leaked into next nomination |
| Unsaved category change | Confirmation; decline preserves data; confirm loads valid new set and clears answers/files |
| Saved category | Cannot change category/type/version |
| Cancel/navigation | Warns about unsaved changes; abandoning then reopening restores server data |

## 4. Failure and concurrency tests

Use a development/test environment and controlled permission/network conditions; do not delete production data to simulate errors.

- Block form save: no false success, no confirmation, busy clears, user input retained. If the server outcome is unknown, inspect My nominations before retrying.
- Allow draft save but deny/fail the final status update: saved ID remains available; confirmation does not show; refresh determines whether the server still has Draft or already Submitted. Retry uses the saved item after status/Modified checks.
- Open a draft in two sessions; save one, then attempt save from the other. Detected Modified change blocks overwrite and tells the user to reopen. The preflight check is not atomic; document the remaining race if stronger locking is required.
- Change current published questions while an old draft is open. The old draft keeps its snapshots/version; a fresh nomination gets the new version.
- Try malformed question configurations (gaps,duplicate order,blank prompt,wrong key). Category loading blocks them.
- Fail one admin question save. Old published pointer remains usable; partial new rows do not become visible to employees. Retry same rows or allocate a fresh version if edited.
- Simulate a competing publisher. Pointer change is detected where checks run. Do not claim atomic concurrency protection; use coordinated single publication until a backend mechanism is agreed.

## 5. Delegation and performance

In a test list with records beyond the app's nondelegation row limit, verify an older matching own record is found using the selected category/status/ID filters. Test a low development row limit (for example1) as an additional way to expose accidentally local operations, but do not confuse that with a full load test. Verify Monitor/network calls and Studio's delegation analysis. Category/question collections are bounded configuration; nomination galleries remain directly bound to their lists. The highest-version administrator query must use server-side category filtering and descending version order.

## 6. Permissions and production handover

1. Create/identify approved groups for nominators, configuration managers and awards administrators. Actual group identities have not been supplied in the source specification.
2. Config lists: nominators read only; configuration managers may maintain approved questions. Restrict direct editing so published rows are not casually overwritten. The app's object-ID UI allowlist does not secure the lists.
3. Six nomination lists: verify the provisioned own-item read/edit settings with a normal non-owner account. Create a custom permission level without Delete Items if ordinary nominators must not delete; list owners/admins can bypass own-item restrictions, so test actual roles.
4. Decide submitted-item enforcement. Current Canvas formulas only make Submitted read-only in the app. A user with underlying edit permission may still use SharePoint/API. An asynchronous permission flow has a delay; do not represent it as instantaneous locking. Implement/test the agreed policy before claiming immutable submissions.
5. Confirm seed wording, category titles, L1–L6 values, attachment size/count policy and declaration wording for the intended release. Nothing in this manual silently supplies those business approvals.
6. Confirm every target environment has the same internal column schema and correct list lookup targets. Set the site/list environment-variable values during solution import and verify all six saves target the correct environment.
7. Publish an approved question version, then publish/share the Canvas app only after acceptance. Share connector access as appropriate; never share app owners' credentials.
8. Record app URL/version, environment ID, solution version, source list GUIDs, permissions, known limitations and acceptance results. The app URL is not yet available because no app has been authored/deployed by this package.

## Suggested test log

| Date / tester | Code | Reference | Test | Expected / observed | Pass/fail / follow-up |
|---|---|---|---|---|---|
| | | | | | |

Do not mark a stage complete merely because the Markdown formula was generated. Completion means the corresponding Studio/runtime checks above have passed.
