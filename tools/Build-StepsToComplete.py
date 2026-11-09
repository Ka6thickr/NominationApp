"""Assemble an ordered continuation guide from the reviewed production recipes."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
prod = (ROOT/'Prod.md').read_text(encoding='utf-8')
rows = [
    ('II','BestInnovatorIndividual','IND_INNOVATION'),
    ('IC','MDAward','IND_CUSTOMER'),
    ('IE','TrendMarcherAward','IND_EXCELLENCE'),
    ('TC','BestInnovatorTeam','TEAM_COLLAB'),
    ('TI','MDAwardTeam','TEAM_IMPACT'),
    ('TT','SpecialTeamAward','TEAM_TRANSFORM')]
parts = ['''# Steps to complete the Nomination App

## Start here — your current checkpoint

You confirmed the latest corrections to the two existing forms are complete. Continue from the scrolling-container step. Do not recreate frmBestInnovatorIndividual or frmMDAward, or overwrite their corrected cards. The exact MD screen name is **scrMDAward**, not scrnMDAwards.

This guide preserves the original Contoso design and current list mapping. It contains an ordered checklist followed by the complete current property/formula reference, so you can continue manually without another chat. Written recipes and user-confirmed changes are not proof of Studio compilation or runtime success.

## How to use the guide

1. Complete one numbered stage at a time and save the app.
2. Use the exact control names shown. Search this file for a property such as `frmMDAward.OnSuccess` when applying its full formula.
3. Keep properties that already match. Copy only the formula for the selected property, not an entire Markdown section.
4. All controls must have unique app-wide names. II, IC, IE, TC, TI and TT identify the six distinct form families.
5. Create referenced controls before pasting formulas that use them. Do not run App.OnStart while a nomination has unsaved changes.
6. Use one scroll viewport below the fixed header/navigation/stepper. Form height alone does not make a screen scroll.

<a id="build-sequence-for-all-13-screens"></a>
## Completion order

| Stage | Work | Checkpoint |
|---|---|---|
| 1 | Confirm connections, screen/form names and initialization prerequisites | Correct target site and typed sources |
| 2 | Finish scrBestInnovatorIndividual shell | Form, errors, evidence and actions fit a scrolling page |
| 3 | Finish scrMDAward shell | Same visual structure; IC formulas only |
| 4 | Build the four remaining award forms and shells | Six distinct typed destinations |
| 5 | Apply App.Formulas and App.OnStart; create reusable stepper | Theme/state initialize without unresolved dependencies |
| 6 | Complete scrHome, scrNomineeDetails and scrCategorySelection | Real dynamic questions load into first form |
| 7 | Complete scrMyNominations and test draft save/reopen | Same source and ID restored with evidence |
| 8 | Complete scrReview and scrConfirmation | Validated submission and view-only reopening |
| 9 | Complete scrQuestionAdministration | New question versions saved and verified before publication |
| 10 | Run acceptance tests and release preparation | No unresolved App Checker errors; tested user access |

## Stage 1 — prerequisites, without resetting your work

- [ ] Open your existing app in the actual new environment. Do not create a duplicate solution/app.
- [ ] Connect AwardCategories, AwardQuestions and the six nomination lists below from the actual destination site.
- [ ] Add Office365Users.
- [ ] Verify all 13 screens exist, including the six below and scrHome, scrNomineeDetails, scrCategorySelection, scrReview, scrConfirmation, scrMyNominations and scrQuestionAdministration.
- [ ] Keep the two corrected forms. Create the other four named classic Edit forms if absent, each bound to its own source. Their complete field recipes are included later.
- [ ] Confirm Display settings: Scale to fit off; Lock aspect ratio off. Use responsive containers.
- [ ] If Theme is undefined, apply the complete App.Formulas block in the reference once its named dependencies exist. Defer running OnStart until all required sources and controls exist. Temporary unresolved references must be fixed before testing.

| Category | Data source | Screen | Form |
|---|---|---|---|
''']
for p,n,c in rows:
    parts.append(f'| `{c}` | `{n}` | `scr{n}` | `frm{n}` |')
for index,(p,n,c) in enumerate(rows,2):
    parts.append(f'''
## Award screen checklist — scr{n}

{'Continue the corrected existing form.' if p in ('II','IC') else 'Create the form from its actual data source and apply its complete field recipe before testing.'} Use prefix **{p}**, source **{n}**, form **frm{n}**, record **varRecord{p}** and category code **{c}**.

### A. Create the scroll viewport

1. Select scr{n}. Insert a **Vertical container directly on the screen**, named `cntScroll{p}`.
2. Apply these properties. If already created, verify rather than duplicate it.

| Property | Value |
|---|---|
| X | `0` |
| Y | `If(App.Width<=760,200,206)` — temporary reservation for the top shell |
| Width | `Parent.Width` |
| Height | `Max(0,Parent.Height-Self.Y)` |
| LayoutOverflowY / LayoutOverflowX | `LayoutOverflow.Scroll` / `LayoutOverflow.Hide` |
| LayoutDirection | `LayoutDirection.Vertical` |
| LayoutGap and all four paddings | `0` |

### B. Create the growing content container

Inside cntScroll{p}, insert a **manual-layout container**, named `cntPage{p}`.

| Property | Value |
|---|---|
| Width | `Min(1180,Parent.Width)` |
| AlignInContainer | `AlignInContainer.Center` |
| FillPortions | `0` — turn Flexible height off |
| LayoutMinWidth / LayoutMinHeight | `0` / `0` |
| Height | `800` temporarily; replace in step E below |

### C. Move the existing form into the page

1. Save a checkpoint. In Tree view move frm{n} inside cntPage{p}. If using cut/paste, select the page container before pasting. Do not insert a second copy.
2. Verify its name is still frm{n}, DataSource is {n}, Item is varRecord{p}, and all child card names/bindings/events remain intact.
3. Verify its form Height still sums Q1–Q6 response-card heights plus dc{p}Attachments.Height +24.
4. Keep OnVisible=`Set(varCurrentStep,3)` on the screen. Do not reset the form here.

### D. Add the page content around the form

Inside cntPage{p}, create these siblings in this order. Use the exact `scr{n} — placement` table in the reference below for every coordinate and dimension.

| Control | Type / purpose |
|---|---|
| lblHeading{p} | Classic Label; criteria/evidence or view title |
| lblSubtitle{p} | Classic Label; Text=`varCategory.Title` |
| cntSummary{p} | Manual container; nominee/reference summary and Edit details button |
| cntProgress{p} | Manual container; desktop sidebar, stacked above form on mobile |
| frm{n} | Your existing native form |
| lblSaveError{p} | Classic Label; Text=`frm{n}.Error`; AutoHeight=true; visible only when error exists |
| cntActions{p} | Manual container; Back, Save draft, Review buttons |

Use the original visual styling reference for heading, summary, progress and button styling. Summary text uses NomineeDisplay, varAwardType and NominationReference. Progress text counts nonblank active responses from colAnswers. Do not hardcode question wording.

### E. Apply final placement and page height

1. Apply the complete `scr{n} — placement` table included below, replacing the temporary page Height. It defines form width beside the 260-unit sidebar on desktop and full inner width on mobile.
2. Set cntPage{p}.Height to `cntActions{p}.Y+cntActions{p}.Height+If(App.Width<=760,40,56)`.
3. Keep errors between the form and actions. The action-row Y formula in that table includes the error label and sidebar bottom.
4. Verify native attachments remain inside dc{p}Attachments, which remains inside frm{n}.

### F. Add action buttons and wire events

Inside cntActions{p}, create btn{p}Back, btn{p}SaveDraft and btn{p}Review. Apply the shared responsive action-row positions from the visual reference. Set Visible=`!varReadOnly`; disable actions while varIsBusy. Copy each complete OnSelect block from the **{n}: {c} / {p}** recipe below.

- btn{p}Back: use that form's **Back to details** block, capturing current input before navigation.
- btn{p}SaveDraft: use its full draft handler, including preflight and SubmitForm.
- btn{p}Review: capture the current answers and pending evidence filenames, validate and navigate.
- frm{n}.OnSuccess and OnFailure: use the full matching event recipes. Never put the Submitted Patch directly after SubmitForm in a button.
- Add btn{p}BackToMine, Visible=`varReadOnly`, OnSelect=`Navigate(scrMyNominations,ScreenTransition.None)`; position it in the action row when editable buttons are hidden.
- Edit details inside cntSummary{p} uses the same capture/navigation action as btn{p}Back.

### G. Complete the fixed top shell

Create `cntHeader{p}`, `cntNav{p}` and `cntStepperStrip{p}` as **manual containers directly on the screen**, outside cntScroll{p}.

| Control | X | Y | Width | Height |
|---|---|---|---|---|
| cntHeader{p} | `0` | `0` | `Parent.Width` | `If(App.Width<=760,58,64)` |
| cntNav{p} | `0` | `cntHeader{p}.Y+cntHeader{p}.Height` | `Parent.Width` | `48` |
| cntStepperStrip{p} | `0` | `cntNav{p}.Y+cntNav{p}.Height` | `Parent.Width` | `94` |

Replace cntScroll{p}.Y with `cntStepperStrip{p}.Y+cntStepperStrip{p}.Height`. Keep its Height based on the remaining screen space. Populate the header/nav using the shared design reference. Add the cmpStepper component instance inside the strip after creating the component in Stage 5. Prefix copied child names with {p} to avoid duplicates.

### H. Checkpoint before proceeding

- [ ] Form appears once, inside cntPage{p}, inside cntScroll{p}.
- [ ] Header/nav/stepper stay above the scrolling viewport.
- [ ] Desktop has a sidebar; mobile stacks progress above the form.
- [ ] All active questions, attachment control, error text and actions can be reached by scrolling.
- [ ] Returning from Review does not clear answers/files.
- [ ] {'Configure only Q1–Q3 rows for the active Team question version; keep all six column slots.' if p in ('TC','TI','TT') else 'The active category version supplies its actual question count.'}
- [ ] Save the development app. Runtime checks follow after shared screens/state are ready.
''')
parts.append('''
## Stage 5 — shared state and process stepper

1. Verify all six forms have their exact names and sources from Stage 1.
2. Set App.StartScreen=`scrHome`.
3. Apply the complete **App.Formulas** block in the reference. This supplies Theme and validation/display named formulas.
4. Apply the complete **App.OnStart** block. Configure the approved admin IDs; the all-zero placeholder intentionally allows no admin UI access. This is separate from SharePoint permissions.
5. Resolve missing source/control names. Run OnStart only when no unsaved nomination is in progress.
6. Create cmpStepper using the embedded component guide. Create its custom input properties first, then its Image control and SVG formula. Use the HTML alternative only if chosen intentionally; neither approach handles app navigation.
7. Add an instance to each Details, Category, six award and Review screen. Bind CurrentStep and Steps to the shared state as specified. Confirm completed/current/pending colors.

## Stage 6 — scrHome, scrNomineeDetails, scrCategorySelection

### scrHome

- [ ] Follow **scrHome — explicit starting screen** below: header/nav, no stepper; New nomination, My nominations and admin buttons.
- [ ] New nomination uses the complete **New nomination action after any required discard confirmation** block.
- [ ] Implement the documented discard dialog before allowing navigation that would replace unsaved input.

### scrNomineeDetails

- [ ] Build the standard 1030-wide content shell; show stepper and set OnVisible=`Set(varCurrentStep,1)`.
- [ ] Follow **2. scrNomineeDetails** in the reference to create the type controls, directory pickers, team fields, role and level inputs in order.
- [ ] Connect each Default/OnChange/Items property exactly as supplied. Normal edits must invalidate response/declaration completion.
- [ ] Apply the complete **Details Continue button OnSelect** block.
- [ ] Test Individual and Team visibility and required detail validation.

### scrCategorySelection

- [ ] Build the standard shell; follow **3. scrCategorySelection** for the active category gallery and selection handling.
- [ ] Load only the selected award type's active categories and their published question versions.
- [ ] Apply **Category load action after selection/discard checks**. It routes to the exact new screen/form names.
- [ ] Ensure a valid approved category/question version exists before testing. Empty inactive configuration correctly produces no selectable categories.
- [ ] Verify selection creates snapshots and varQuestionCount, then opens the matching form.

## Stage 7 — scrMyNominations and first complete draft test

1. Follow **3. scrMyNominations** below. Use the shell without a stepper.
2. Add category/status/ID filters and six typed galleries. Show only the gallery for the selected category; do not merge unbounded lists into one collection.
3. Apply each **My nominations gallery galMineII/IC/IE/TC/TI/TT** recipe from its form section. Each item opens the matching source, record variable and screen.
4. Test with a synthetic nomination: Home → Details → Category → Best Innovator Individual → partial answer → attach a test file → Save draft.
5. Record the item ID, reopen from My nominations, edit and save. Confirm the same ID and saved attachment remain. Never retry an uncertain new-item timeout before checking server state.
6. Repeat the draft check for MDAward, then the other four sources.

## Stage 8 — scrReview and scrConfirmation

### scrReview

- [ ] Use maximum content width 960 with the standard header/nav/stepper; set current step to 4 as specified.
- [ ] Follow **1. scrReview**: details summary, six expanding answer blocks, evidence filenames, declaration and actions.
- [ ] Apply **Six expanding review question blocks** exactly. Unused slots have zero height and no trailing gaps.
- [ ] Back uses **Return to the existing active form without resetting it**.
- [ ] Submit uses the complete **Review screen Submit button OnSelect** block. It validates and saves through the matching native form.

### scrConfirmation

- [ ] Follow **2. scrConfirmation**; shell without a stepper, success/reference text from saved state.
- [ ] Navigate here only after successful final Submitted status update in form OnSuccess.
- [ ] Add My nominations and New nomination actions as documented.
- [ ] Test declaration invalidation after changing answers/evidence; submission failure retains inputs and ID; successful records reopen with ViewForm.

## Stage 9 — scrQuestionAdministration

1. Follow **4. scrQuestionAdministration** below. Use the shell without a stepper and the approved admin visibility/entry checks.
2. Create category selection, version controls, editable question gallery, preview and publish controls in the stated order.
3. Apply **Question administration copy/load button OnSelect** and **Question administration Publish button OnSelect** in full.
4. For Team categories configure three active questions. Retain all six supported slots and old published versions.
5. Verify new rows are saved/read back before the category version pointer changes. Do not edit old published rows.
6. Test permissions with a normal user; hiding admin controls alone does not protect the configuration lists.

## Stage 10 — final acceptance and takeover log

Run the **Release verification checklist** at the end. Resolve App Checker errors, test desktop/mobile scrolling, drafts, files, review, submission, failure/retry, concurrent modification and normal-user permissions. Preserve the fixed schema. Publish/share only after these checks pass and content/roles are configured.

Record progress here as you work:

| Stage / screen | Done | Evidence / issue | Next action |
|---|---|---|---|
| Existing II/IC card corrections | User-confirmed | Not runtime-tested | Complete page shells |
| Connections and six form scaffolds | Pending verification | | |
| Award page shells | Pending | | |
| State and stepper | Pending | | |
| Details/category flow | Pending | | |
| Draft/save/reopen | Pending | | |
| Review/submission | Pending | | |
| Admin/security/responsive tests | Pending | | |

---

# Complete property and Power Fx reference

The following recipes are included from Prod.md so this continuation guide is self-contained. The earlier numbered checklist determines work order. Keep already-corrected properties. The exact per-screen placement tables override generic example coordinates. References to .fx filenames mean the corresponding complete formula block embedded below; do not enter a filename as a formula.

''')
reference=prod[prod.index('# Solution, state and navigation setup'):]
parts.append(reference)
output='\n'.join(parts)
assert 'scrnMDAwards' not in output.replace('not scrnMDAwards','')
(ROOT/'stepstocomplete.md').write_text(output,encoding='utf-8')
# Validate all internal links after composition.
headings=re.findall(r'^#+ (.+)$',output,re.M)
anchors={re.sub(r'[^\w\- ]','',h.lower()).replace(' ','-') for h in headings}
anchors.update(re.findall(r'<a id="([^"]+)"',output))
for target in re.findall(r'\]\(([^)]+)\)',output):
    if target.startswith('#'): assert target[1:] in anchors,target
print('Built stepstocomplete.md: six explicit award-screen checklists, seven shared screens, complete embedded formulas; internal links verified.')
