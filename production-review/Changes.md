# Nomination app: environment migration and finalized form recipes

Updated: 9 November 2026.

## Reading this document

This is a sanitized implementation record and copy/paste guide, not an exported
Canvas app. Only fictional Contoso site URLs appear here. No actual tenant URL,
environment identifier, local machine path, account name, deployment report,
list GUID, or credential is included. The requested physical list names and
application control names are retained because the formulas requiret them.

Status terms:

- **Confirmed in exports:** observed in the two latest supplied form snapshots.
- **User-confirmed:** verified in Studio by the builder, rather than encoded
  explicitly in an export.
- **Remaining correction:** still needs to be applied manually in Studio.
- **Implementation recipe:** intended final configuration; not proof that the
  builder has already applied it.

The original AISite configuration is preserved. No live SharePoint change, Canvas
compilation, publication, or production readiness is claimed by this document.

### Contents

1. [Environment and list migration](#environment-and-list-migration)
2. [Finalized implementation decisions](#finalized-implementation-decisions)
3. [Review of the two supplied forms](#review-of-the-two-supplied-forms)
4. [Corrections to apply before copying](#corrections-to-apply-before-copying)
5. [Common form-building and scrolling rules](#common-form-building-and-scrolling-rules)
6. [Six explicit form recipes](#six-explicit-form-recipes)
7. [Shared app formulas and routed actions](#shared-app-formulas-and-routed-actions)
8. [Other shared screens](#other-shared-screens)
9. [Release verification checklist](#release-verification-checklist)

## Environment and list migration

### Fictional site references

| Purpose | Dummy reference only |
|---|---|
| Original site collection | `https://contoso.sharepoint.com/sites/AISite` |
| Separate destination site collection | `https://contoso.sharepoint.com/sites/RecognitionAwards` |
| Example destination configuration list | `https://contoso.sharepoint.com/sites/RecognitionAwards/Lists/AwardCategories` |
| Example destination nomination list | `https://contoso.sharepoint.com/sites/RecognitionAwards/Lists/MDAward` |

These are documentation placeholders, not actual endpoints or verified list
paths. A SharePoint list's actual root-folder URL can differ from its title.
Enter approved target connection values privately in the deployment environment.

### Original-to-destination mapping

Category codes remain unchanged. The destination app uses the imported source
identifiers exactly as listed, rather than trying to rename data sources.

| Logical key/category code | Original list | Destination list/source | Destination screen | Destination form | Prefix | Item |
|---|---|---|---|---|---|---|
| `Categories` | `AwardCategories` | `AwardCategories` | Shared configuration | Not a nomination form | - | - |
| `Questions` | `AwardQuestions` | `AwardQuestions` | Shared configuration | Not a nomination form | - | - |
| `IND_INNOVATION` | `Nom_IndividualInnovation` | `BestInnovatorIndividual` | `scrBestInnovatorIndividual` | `frmBestInnovatorIndividual` | `II` | `varRecordII` |
| `IND_CUSTOMER` | `Nom_IndividualCustomer` | `MDAward` | `scrMDAward` | `frmMDAward` | `IC` | `varRecordIC` |
| `IND_EXCELLENCE` | `Nom_IndividualExcellence` | `TrendMarcherAward` | `scrTrendMarcherAward` | `frmTrendMarcherAward` | `IE` | `varRecordIE` |
| `TEAM_COLLAB` | `Nom_TeamCollaboration` | `BestInnovatorTeam` | `scrBestInnovatorTeam` | `frmBestInnovatorTeam` | `TC` | `varRecordTC` |
| `TEAM_IMPACT` | `Nom_TeamImpact` | `MDAwardTeam` | `scrMDAwardTeam` | `frmMDAwardTeam` | `TI` | `varRecordTI` |
| `TEAM_TRANSFORM` | `Nom_TeamTransformation` | `SpecialTeamAward` | `scrSpecialTeamAward` | `frmSpecialTeamAward` | `TT` | `varRecordTT` |

### Provisioning and documentation changes already made

| Area | Finalized change |
|---|---|
| Environment configuration | Separate target configuration; preserve the original AISite configuration. |
| Provisioning output | Added `-ResultPath` so destination deployment results do not overwrite the original report. |
| Schema | Preserve fixed internal column names/types, person/lookup/choice shapes, native attachments, and versioned question snapshots. Do not rename columns to match control names. |
| Imported data sources | Formulas now directly reference the eight destination source identifiers above. A string variable cannot dynamically rebind a typed SharePoint form. |
| Form/screen naming | Six forms and their screens now use the exact destination list name after `frm`/`scr`. Internal prefixes and category codes remain stable. |
| Routing | Updated new/reset, category selection, return-to-form, browse/open, save, and final-submit branches for all six typed sources. |
| Recipe generation | Updated manual-guide generation, consolidation, and structural tests for the mappings and form names. |
| Local provisioning checks | Earlier validation reported 8 lists, 194 custom columns, 6 categories, and 21 seed questions. These are local schema/configuration results, not live read-back results. |
| Publication | Seed wording, level policy, category activation, permissions, and attachment limits still need business approval. This guide does not activate or publish them. |

For solution deployment, bind the SharePoint Site data-source environment
variable and eight List data-source environment variables to private approved
target values. List bindings use the correct target GUIDs, not merely title
strings. Keep source identifiers and schemas consistent after rebinding.
Office 365 Users is a separate connection used for directory lookup.

## Finalized implementation decisions

| Topic | Final decision |
|---|---|
| Screen inventory | 13 screens: Home, Details, Category Selection, six typed form screens, Review, Confirmation, My Nominations, Question Administration. |
| Read-only view | Reuse the matching typed form in `ViewForm` mode; no additional duplicate view screen. |
| Form settings | Classic Edit form; typed `DataSource`; corresponding record `Item`; `DefaultMode = FormMode.New`; one column; `SnapToColumns = false`. |
| Individual schema | 30 fields plus native Attachments: common metadata, `NominatedEmployee`, and six prompt/required/response triples. |
| Team schema | 32 fields plus native Attachments: replace `NominatedEmployee` with `TeamName`, `TeamPrimaryContact`, and `TeamMembers`. |
| Hidden metadata | Keep its cards in the form. `Visible = false`, `Height = 0`, `Required = false`; its `Update` still participates in saves. |
| Response slots | Six fixed response controls; only slots up to `varQuestionCount` are visible. Approved published question sets contain 3-6 questions. |
| Question layout | Response card contains a manual container with heading, prompt, classic text input, and counter label. |
| Question content | Load prompt, required flag, and response from the matching `colAnswers` slot. Do not hardcode award questions. |
| Nested input properties | Use the response card's explicit name for `Error`, `BorderColor`, and `DisplayMode`; the immediate `Parent` is now a container. |
| Input events | `DelayOutput = false`; `OnChange` patches the matching slot and clears response/declaration completion flags. |
| Draft requirements | Card `Required = false` permits incomplete drafts. Named validation formulas enforce submission requirements. |
| Attachments | Native nomination-level attachments, not one attachment control per question. Preserve generated connector properties and limits until policy approval. |
| Form height | Sum six response-card heights, attachment-card height, and 24. Scrolling must be provided separately. |
| Screen event | Each typed screen sets `varCurrentStep` to 3. Do not reset forms on every screen entry. |
| Save/submit | `SubmitForm` saves draft fields/files asynchronously. Final status changes only in the successful form event, retaining the saved ID. |
| Validation status | Formula structure can be checked locally; Studio types, connector behavior, layout, permissions, and runtime still require testing. |

### Complete screen inventory

| Screen | Purpose |
|---|---|
| `scrHome` | Entry, new nomination, and My nominations |
| `scrNomineeDetails` | Step 1: individual/team details |
| `scrCategorySelection` | Step 2: choose category and load questions |
| `scrBestInnovatorIndividual` | Step 3: Best Innovator Individual |
| `scrMDAward` | Step 3: MD Award individual |
| `scrTrendMarcherAward` | Step 3: Trend Marcher individual |
| `scrBestInnovatorTeam` | Step 3: Best Innovator Team |
| `scrMDAwardTeam` | Step 3: MD Award team |
| `scrSpecialTeamAward` | Step 3: Special Team Award |
| `scrReview` | Step 4: review current answers/evidence and declaration |
| `scrConfirmation` | Confirm a successful saved submission |
| `scrMyNominations` | Browse/open own drafts and submissions |
| `scrQuestionAdministration` | Restricted question-version administration |

## Review of the two supplied forms

The latest attachments contain 180 controls each, including 31 data cards each.
The first attachment is a form-only export; it does not contain its screen's
`OnVisible`. The second contains `scrMDAward` and its form.

### Confirmed fixes

| Check | Best Innovator Individual (`II`) | MD Award (`IC`) |
|---|---|---|
| Data source and form name | Correct | Correct |
| Record `Item` | `varRecordII` | `varRecordIC` |
| Overall form height | Correct sum + 24 | Correct sum + 24 |
| One column / no snap | Correct | Correct |
| Expected fields | All 31 cards present | All 31 cards present |
| All card `Update` formulas | Match the mapped recipe after ignoring comments/formatting | Match the mapped recipe, including corrected Q1 answer source |
| Response visibility / container-based heights | Correct for all six slots | Correct for all six slots |
| Input Default / OnChange | Matching slots | Matching slots |
| Input BorderColor / Tooltip / DisplayMode | Explicit, correct card/slot references | Explicit, correct card/slot references |
| Prompt Text slot | Correct for all six | Correct for all six |
| Counters | All six present; correct count text | All six present; correct count text |
| Attachments binding | Native DataField, Items, Update preserved | Native DataField, Items, Update preserved |
| Screen OnVisible | Previously verified; absent from this form-only snapshot | `Set(varCurrentStep, 3)` |
| DelayOutput | Builder previously confirmed `false`; omission from the export alone is not a failure | Confirm `false` in Studio; export does not explicitly serialize it |

### Remaining work, not yet performed in Studio

| Priority | Scope | Finding | Correction |
|---|---|---|---|
| Functional layout | II Q1-Q6 inputs | Their Y still uses the old generated field label, so inputs can overlap the new prompt. X/width are also inconsistent; no explicit responsive input Height. | Use the exact input layout table below. |
| Content accuracy | IC Q1-Q6 headings | Fallback text still says `Criterion n`; Q2-Q6 required markers still read slot 1. | Replace heading Text with the expanded formulas below. |
| Functional layout | IC Q2-Q6 counters | Counter Y still refers to Q1's input, so height/position can be wrong when prompts wrap differently. | Bind each counter to its own input. |
| Consistency | IC hidden cards | All 24 are hidden, but none explicitly sets Height to 0 in the export. | Explicitly set Height to 0; do not assume hidden cards currently occupy space. |
| Spacing | IC prompt labels | Height contains a heading-position expression while AutoHeight is true. | Keep AutoHeight true; use base Height 34. Position belongs in Y. |
| Alignment | IC inputs | X is 20 while labels/counters use 22. | Set X to 22. |
| Spacing | II Q6 | Counter Height and prompt Size are not explicit. | Set counter Height 18 and prompt Size 9.75. |
| Error presentation | Both sets of response cards | Generated error labels still use input-relative coordinates; can overlap counter/content. Generated field headings also remain beneath the new custom containers. | Keep error labels, position them below the container, allow room in the card, and hide only redundant generated field-heading labels. |
| Save lifecycle | Both forms | No explicit OnSuccess/OnFailure in the supplied export. | Wire the corresponding events in the full recipes before enabling saves. |
| Attachment dirty state | Both attachment controls | No explicit OnAddFile/OnRemoveFile/OnUndoRemoveFile actions. | Add the three state-flag actions described below without replacing native bindings. |
| Accessibility | II inputs | No explicit question-based AccessibleLabel in the snapshot. | Add the slot-specific AccessibleLabel from the full recipe. |
| Overall page | Both forms | Width/scrolling page layout is not explicit in these snapshots. | Complete a scrolling parent layout and test narrow screens before release. |

Uninitialized globals can explain many authoring errors, but not every error.
Wrong parent references, copied slots, missing controls, and invalid property
formulas must be corrected independently. Do not dismiss all remaining App
Checker errors as initialization issues.

## Corrections to apply before copying

### Best Innovator Individual input layout

Set these properties on the text inputs, not on the data cards.

| Input | X | Y | Width | Height |
|---|---|---|---|---|
| `txtIIQ1` | `22` | `lblIIQ1Prompt.Y + lblIIQ1Prompt.Height + 18` | `Parent.Width - 44` | `If(App.Width <= 760, 180, 142)` |
| `txtIIQ2` | `22` | `lblIIQ2Prompt.Y + lblIIQ2Prompt.Height + 18` | `Parent.Width - 44` | `If(App.Width <= 760, 180, 142)` |
| `txtIIQ3` | `22` | `lblIIQ3Prompt.Y + lblIIQ3Prompt.Height + 18` | `Parent.Width - 44` | `If(App.Width <= 760, 180, 142)` |
| `txtIIQ4` | `22` | `lblIIQ4Prompt.Y + lblIIQ4Prompt.Height + 18` | `Parent.Width - 44` | `If(App.Width <= 760, 180, 142)` |
| `txtIIQ5` | `22` | `lblIIQ5Prompt.Y + lblIIQ5Prompt.Height + 18` | `Parent.Width - 44` | `If(App.Width <= 760, 180, 142)` |
| `txtIIQ6` | `22` | `lblIIQ6Prompt.Y + lblIIQ6Prompt.Height + 18` | `Parent.Width - 44` | `If(App.Width <= 760, 180, 142)` |

### MD Award heading Text

| Control | Text formula |
|---|---|
| `lblICQ1Heading` | `With({p:LookUp(colAnswers,Slot=1,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 1")) & If(LookUp(colAnswers,Slot=1,Required)," *","")` |
| `lblICQ2Heading` | `With({p:LookUp(colAnswers,Slot=2,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 2")) & If(LookUp(colAnswers,Slot=2,Required)," *","")` |
| `lblICQ3Heading` | `With({p:LookUp(colAnswers,Slot=3,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 3")) & If(LookUp(colAnswers,Slot=3,Required)," *","")` |
| `lblICQ4Heading` | `With({p:LookUp(colAnswers,Slot=4,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 4")) & If(LookUp(colAnswers,Slot=4,Required)," *","")` |
| `lblICQ5Heading` | `With({p:LookUp(colAnswers,Slot=5,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 5")) & If(LookUp(colAnswers,Slot=5,Required)," *","")` |
| `lblICQ6Heading` | `With({p:LookUp(colAnswers,Slot=6,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 6")) & If(LookUp(colAnswers,Slot=6,Required)," *","")` |

### MD Award counter Y

| Counter | Y |
|---|---|
| `lblICQ1Counter` | `txtICQ1.Y + txtICQ1.Height + 6` |
| `lblICQ2Counter` | `txtICQ2.Y + txtICQ2.Height + 6` |
| `lblICQ3Counter` | `txtICQ3.Y + txtICQ3.Height + 6` |
| `lblICQ4Counter` | `txtICQ4.Y + txtICQ4.Height + 6` |
| `lblICQ5Counter` | `txtICQ5.Y + txtICQ5.Height + 6` |
| `lblICQ6Counter` | `txtICQ6.Y + txtICQ6.Height + 6` |

For the remaining properties and all other forms, use the complete expanded
recipes below. They include the error-label layout and explicit nested input
references; no substitution of a slot-number placeholder is needed.

## Common form-building and scrolling rules

1. Insert a fresh classic Edit form for each actual list. Do not merely copy a
   form and change DataSource; its generated cards can retain the wrong schema.
2. Add every field in that form's Update table plus native Attachments. Unlock
   cards as needed. Rename controls, not column internal names or DataField.
3. Keep each response card outside its manual container. Inside that container
   place three labels (heading, prompt, counter) and one classic text input.
4. Keep each generated response error label directly in its card. Rename it to
   the error-control name in that recipe. Preserve Text = Parent.Error and
   MetadataKey. Hide the redundant generated field-heading label for response
   cards only; do not hide the custom prompt or delete error feedback.
5. Apply all properties in each question table, then the input/error/attachment
   completion tables. Use explicit card references inside nested inputs.
6. Set each card DisplayMode to Parent.DisplayMode. Editors directly inside
   hidden cards can use If(varIsBusy, DisplayMode.Disabled, Parent.DisplayMode).
7. Put Q1Response-Q6Response first, Attachments next, metadata last. Response
   card X is 0 and Y is 0-5; Attachments Y is 6. Form Y is grid ordering here.
8. Formula examples use English Power Fx separators. Use classic Text inputs
   with Text, not a modern control with an incompatible value property.
9. Save development changes. Run app initialization only after the referenced
   connections, forms, screens, and shared controls exist; it resets local state.

### Scrolling layout

The form-height formula does not create scrolling. If a scrolling page shell
already exists, use it; do not add a second nested scrolling viewport.
Otherwise, use this minimal final layout for each typed screen:

| Control | Property | Value |
|---|---|---|
| Outer vertical auto-layout container | X / Y | `0` / `0` |
| Outer container | Width / Height | `Parent.Width` / `Parent.Height` |
| Outer container | LayoutDirection | `LayoutDirection.Vertical` |
| Outer container | LayoutOverflowY / LayoutOverflowX | `LayoutOverflow.Scroll` / `LayoutOverflow.Hide` |
| Outer container | PaddingLeft/Right/Top/Bottom / LayoutGap | `0` |
| Inner manual-layout content container | Width | `Min(1180, Parent.Width)` |
| Inner content container | AlignInContainer / FillPortions / LayoutMinHeight | `AlignInContainer.Center` / `0` / `0` |
| Form inside content container | X | `If(App.Width <= 760, 16, 24)` |
| Form | Y | `40` for the minimal shell; place after your summary if already added |
| Form | Width | `Parent.Width - 2 * Self.X` |
| Form | Height | The explicit per-form sum in its recipe |

The content container must grow through the last action button and any
form-level error label, plus at least 24 units bottom padding. Do not set its
Height to Parent.Height. Keep Save/Review/Back controls outside the form but
inside this content container. Move the form into the content container using
Tree view before using these parent-relative width formulas.

Error-aware card heights in the recipes reserve space for generated SharePoint
validation text only when a card has an error. With no error and container Y=0,
they reduce to the previously finalized container Height + 18. The overall
form-height sum stays unchanged.

### Not included as completed work

Live connector tests, permissions, administrator assignments, category/seed
approval and activation, final declaration wording, attachment policy, approved
branding, publishing, sharing, and runtime acceptance are still outstanding.
Do not include real values for these in a shared change log.

<!-- EXPANDED-RECIPES -->

## Six explicit form recipes

These are corrected target recipes for all six forms, including the two
already started. They are implementation instructions, not a claim that
the supplied snapshots already contain every property. All formulas are
expanded with actual control names and slot numbers.


- [BestInnovatorIndividual](#form-ii)
- [MDAward](#form-ic)
- [TrendMarcherAward](#form-ie)
- [BestInnovatorTeam](#form-tc)
- [MDAwardTeam](#form-ti)
- [SpecialTeamAward](#form-tt)

<a id="form-ii"></a>

### BestInnovatorIndividual: IND_INNOVATION / II

Use the common form-building and scrolling rules above. These formulas target classic controls and English Power Fx separators. They are not yet Studio-compiled or runtime-tested.

#### Controls to create

Screen `scrBestInnovatorIndividual`; Edit form `frmBestInnovatorIndividual`; saved-record variable `varRecordII`; latest-record variable `varLatestII`. Create six response text inputs `txtIIQ1` … `txtIIQ6` in the corresponding response cards, and keep native attachment input `attII` inside `dcIIAttachments`.

Form DataSource = `BestInnovatorIndividual`; Item = `varRecordII`; DefaultMode = `FormMode.New`; NumberOfColumns = `1`; SnapToColumns = `false`. See layout guide for X/Y/Width/Height. Use the form's generated cards and unlock them. Preserve generated DataField strings exactly; if the connector shows a display name with spaces, use Studio's actual generated identifier. Required = `false` on entry cards to allow incomplete drafts; submission requirements are enforced separately. Do not remove metadata cards just because they are hidden.

Response cards are `dcIIQ1Response` … `dcIIQ6Response`. The other Q cards hold snapshots/flags and are hidden. Do not rename a response card to its text input name.

#### scrBestInnovatorIndividual.OnVisible

```powerfx
Set(varCurrentStep, 3)
```

Do not call NewForm/ResetForm here: returning from review must preserve inputs and queued files.

#### All card Update properties

| SharePoint DataField / card | Update formula |
|---|---|
| `Title` / `dcIITitle` | `Left(varCategory.CategoryCode & " - " & If(varAwardType = "Individual", Coalesce(varEmployee.DisplayName, "Draft"), If(IsBlank(Trim(varTeamName)), "Draft", varTeamName)),255)` |
| `Category` / `dcIICategory` | `{Id: varCategory.ID, Value: varCategory.Title}` |
| `QuestionSetVersion` / `dcIIQuestionSetVersion` | `varQuestionVersion` |
| `QuestionCount` / `dcIIQuestionCount` | `varQuestionCount` |
| `NominatedBy` / `dcIINominatedBy` | `varNominator` |
| `NominatorEmail` / `dcIINominatorEmail` | `varUserEmail` |
| `EmployeeRole` / `dcIIEmployeeRole` | `Trim(varRole)` |
| `EmployeeLevel` / `dcIIEmployeeLevel` | `If(IsBlank(varLevel), Blank(), LookUp(Choices(BestInnovatorIndividual.EmployeeLevel), Value = varLevel))` |
| `NominationStatus` / `dcIINominationStatus` | `{Value: "Draft"}` |
| `DeclarationAccepted` / `dcIIDeclarationAccepted` | `false` |
| `SubmittedOn` / `dcIISubmittedOn` | `Blank()` |
| `NominatedEmployee` / `dcIINominatedEmployee` | `If(IsBlank(varEmployee.Claims), Blank(), varEmployee)` |
| `Q1PromptSnapshot` / `dcIIQ1PromptSnapshot` | `LookUp(colAnswers, Slot = 1, Prompt)` |
| `Q1RequiredSnapshot` / `dcIIQ1RequiredSnapshot` | `LookUp(colAnswers, Slot = 1, Required)` |
| `Q1Response` / `dcIIQ1Response` | `If(1 <= varQuestionCount, txtIIQ1.Text, "")` |
| `Q2PromptSnapshot` / `dcIIQ2PromptSnapshot` | `LookUp(colAnswers, Slot = 2, Prompt)` |
| `Q2RequiredSnapshot` / `dcIIQ2RequiredSnapshot` | `LookUp(colAnswers, Slot = 2, Required)` |
| `Q2Response` / `dcIIQ2Response` | `If(2 <= varQuestionCount, txtIIQ2.Text, "")` |
| `Q3PromptSnapshot` / `dcIIQ3PromptSnapshot` | `LookUp(colAnswers, Slot = 3, Prompt)` |
| `Q3RequiredSnapshot` / `dcIIQ3RequiredSnapshot` | `LookUp(colAnswers, Slot = 3, Required)` |
| `Q3Response` / `dcIIQ3Response` | `If(3 <= varQuestionCount, txtIIQ3.Text, "")` |
| `Q4PromptSnapshot` / `dcIIQ4PromptSnapshot` | `LookUp(colAnswers, Slot = 4, Prompt)` |
| `Q4RequiredSnapshot` / `dcIIQ4RequiredSnapshot` | `LookUp(colAnswers, Slot = 4, Required)` |
| `Q4Response` / `dcIIQ4Response` | `If(4 <= varQuestionCount, txtIIQ4.Text, "")` |
| `Q5PromptSnapshot` / `dcIIQ5PromptSnapshot` | `LookUp(colAnswers, Slot = 5, Prompt)` |
| `Q5RequiredSnapshot` / `dcIIQ5RequiredSnapshot` | `LookUp(colAnswers, Slot = 5, Required)` |
| `Q5Response` / `dcIIQ5Response` | `If(5 <= varQuestionCount, txtIIQ5.Text, "")` |
| `Q6PromptSnapshot` / `dcIIQ6PromptSnapshot` | `LookUp(colAnswers, Slot = 6, Prompt)` |
| `Q6RequiredSnapshot` / `dcIIQ6RequiredSnapshot` | `LookUp(colAnswers, Slot = 6, Required)` |
| `Q6Response` / `dcIIQ6Response` | `If(6 <= varQuestionCount, txtIIQ6.Text, "")` |
| Native Attachments / `dcIIAttachments` | `attII.Attachments` |

All cards except Q1–Q6 Response and Attachments: Visible = `false`, Height = `0`, Required = `false`. Set form-card DisplayMode to `Parent.DisplayMode`. Set each child editor DisplayMode to its card's DisplayMode, and disable it while varIsBusy. Hidden metadata's Update properties still participate in SubmitForm.

Keep native attachment Items = `Parent.Default` when directly inside its data card, and retain the generated attachment DataField (often `"{Attachments}"`). Do not type a guessed DataField. Preserve the other generated attachment properties, including MaxAttachments/MaxAttachmentSize, until an approved policy is chosen. Appending files does not save them until SubmitForm completes.

#### btnIISaveDraft.OnSelect

```powerfx
If(!varIsBusy && !varReadOnly && varCategoryComplete,
    ClearCollect(colCapturedAnswers, Table(
    {Slot: 1, Prompt: LookUp(colAnswers, Slot = 1, Prompt), Required: LookUp(colAnswers, Slot = 1, Required), Response: txtIIQ1.Text},
    {Slot: 2, Prompt: LookUp(colAnswers, Slot = 2, Prompt), Required: LookUp(colAnswers, Slot = 2, Required), Response: txtIIQ2.Text},
    {Slot: 3, Prompt: LookUp(colAnswers, Slot = 3, Prompt), Required: LookUp(colAnswers, Slot = 3, Required), Response: txtIIQ3.Text},
    {Slot: 4, Prompt: LookUp(colAnswers, Slot = 4, Prompt), Required: LookUp(colAnswers, Slot = 4, Required), Response: txtIIQ4.Text},
    {Slot: 5, Prompt: LookUp(colAnswers, Slot = 5, Prompt), Required: LookUp(colAnswers, Slot = 5, Required), Response: txtIIQ5.Text},
    {Slot: 6, Prompt: LookUp(colAnswers, Slot = 6, Prompt), Required: LookUp(colAnswers, Slot = 6, Required), Response: txtIIQ6.Text}
));
ClearCollect(colAnswers, colCapturedAnswers);
    If(CountIf(colAnswers, Len(Response) > varMaxResponseLength) > 0,
        Notify("A response exceeds the configured limit.", NotificationType.Warning),
        Set(varIsBusy, true);
Set(varPreflightOK, true);
If(!IsBlank(varNominationId),
    IfError(
        Refresh(BestInnovatorIndividual);
        Set(varLatestII, LookUp(BestInnovatorIndividual, ID = varNominationId));
        If(IsBlank(varLatestII.ID) ||
           varLatestII.NominationStatus.Value <> "Draft" ||
           varLatestII.Modified <> varLoadedModified,
            Set(varPreflightOK, false);
            Notify("This item changed or is no longer an editable draft. Keep a copy of your changes, then reopen it from My nominations.", NotificationType.Error)
        );
        true,
        Set(varPreflightOK, false);
        Notify("Could not check the saved draft. Your changes have been retained; try again when connected.", NotificationType.Error);
        false
    )
);
If(varPreflightOK,
    Set(varSaveIntent, "Draft");
    SubmitForm(frmBestInnovatorIndividual),
    Set(varIsBusy, false)
)
    )
)
```

#### btnIIReview.OnSelect

Set DisplayMode to `If(varIsBusy || varReadOnly, DisplayMode.Disabled, DisplayMode.Edit)`.

```powerfx
ClearCollect(colCapturedAnswers, Table(
    {Slot: 1, Prompt: LookUp(colAnswers, Slot = 1, Prompt), Required: LookUp(colAnswers, Slot = 1, Required), Response: txtIIQ1.Text},
    {Slot: 2, Prompt: LookUp(colAnswers, Slot = 2, Prompt), Required: LookUp(colAnswers, Slot = 2, Required), Response: txtIIQ2.Text},
    {Slot: 3, Prompt: LookUp(colAnswers, Slot = 3, Prompt), Required: LookUp(colAnswers, Slot = 3, Required), Response: txtIIQ3.Text},
    {Slot: 4, Prompt: LookUp(colAnswers, Slot = 4, Prompt), Required: LookUp(colAnswers, Slot = 4, Required), Response: txtIIQ4.Text},
    {Slot: 5, Prompt: LookUp(colAnswers, Slot = 5, Prompt), Required: LookUp(colAnswers, Slot = 5, Required), Response: txtIIQ5.Text},
    {Slot: 6, Prompt: LookUp(colAnswers, Slot = 6, Prompt), Required: LookUp(colAnswers, Slot = 6, Required), Response: txtIIQ6.Text}
));
ClearCollect(colAnswers, colCapturedAnswers);
Set(varDetailsComplete, DetailsValid);
Set(varResponsesComplete, ResponsesValid);
If(!DetailsValid,
    Notify("Complete nominee details, role and level before review.", NotificationType.Warning);
    Navigate(scrNomineeDetails, ScreenTransition.None),
    !ResponsesValid,
    Notify("Complete every required response before review.", NotificationType.Warning),
    Set(varDeclarationAccepted, false);
    ClearCollect(colReviewFiles, ForAll(attII.Attachments As file, {FileName: file.Name}));
    Set(varCurrentStep, 4);
    Navigate(scrReview, ScreenTransition.None)
)
```

`colCapturedAnswers` prevents clearing the source table while reading its snapshots. Review reads current text controls directly, so it does not depend on OnChange timing. If Studio exposes the native file-name column as DisplayName instead of Name, use that actual column in the one FileName projection above; do not change attachment Items/Update or collect file bodies.

#### frmBestInnovatorIndividual.OnSuccess

```powerfx
Set(varRecordII, frmBestInnovatorIndividual.LastSubmit);
Set(varNominationId, varRecordII.ID);
Set(varLoadedModified, varRecordII.Modified);
EditForm(frmBestInnovatorIndividual);
Set(varHasChanges, false);
If(varSaveIntent = "Submit",
    IfError(
        Set(varRecordII,
            Patch(BestInnovatorIndividual, varRecordII,
                {NominationStatus: {Value: "Submitted"},
                 DeclarationAccepted: true, SubmittedOn: Now()}
            )
        );
        Set(varLoadedModified, varRecordII.Modified);
        Set(varSubmittedOn, varRecordII.SubmittedOn);
        Set(varSubmissionComplete, true);
        Set(varReadOnly, true);
        Set(varIsBusy, false);
        ViewForm(frmBestInnovatorIndividual);
        Navigate(scrConfirmation, ScreenTransition.None);
        true,
        Set(varIsBusy, false);
        Set(varSubmissionComplete, false);
        Set(varSaveIntent, "Draft");
        Notify("Your draft save succeeded, but submission was not confirmed. Check My nominations before retrying. Your existing item ID is retained.", NotificationType.Error);
        false
    ),
    Set(varIsBusy, false);
    Notify("Draft saved. Reference: " & varCategory.CategoryCode & "-" & Text(varNominationId, "000000"), NotificationType.Success)
)
```

#### frmBestInnovatorIndividual.OnFailure

```powerfx
Set(varIsBusy, false);
Set(varSubmissionComplete, false);
Set(varHasChanges, true);
Notify("Save was not confirmed. Your inputs are retained. If the connection timed out, check My nominations before retrying because the server may have saved the item.", NotificationType.Error)
```

#### Back to details

Use a native button; Visible = `!varReadOnly`; DisplayMode disabled while varIsBusy. Its OnSelect:

```powerfx
ClearCollect(colCapturedAnswers, Table(
    {Slot: 1, Prompt: LookUp(colAnswers, Slot = 1, Prompt), Required: LookUp(colAnswers, Slot = 1, Required), Response: txtIIQ1.Text},
    {Slot: 2, Prompt: LookUp(colAnswers, Slot = 2, Prompt), Required: LookUp(colAnswers, Slot = 2, Required), Response: txtIIQ2.Text},
    {Slot: 3, Prompt: LookUp(colAnswers, Slot = 3, Prompt), Required: LookUp(colAnswers, Slot = 3, Required), Response: txtIIQ3.Text},
    {Slot: 4, Prompt: LookUp(colAnswers, Slot = 4, Prompt), Required: LookUp(colAnswers, Slot = 4, Required), Response: txtIIQ4.Text},
    {Slot: 5, Prompt: LookUp(colAnswers, Slot = 5, Prompt), Required: LookUp(colAnswers, Slot = 5, Required), Response: txtIIQ5.Text},
    {Slot: 6, Prompt: LookUp(colAnswers, Slot = 6, Prompt), Required: LookUp(colAnswers, Slot = 6, Required), Response: txtIIQ6.Text}
));
ClearCollect(colAnswers, colCapturedAnswers);
Set(varDeclarationAccepted, false);
Set(varCurrentStep, 1);
Navigate(scrNomineeDetails, ScreenTransition.None)
```

#### My nominations gallery galMineII

Visible = `varBrowseCode = "IND_INNOVATION"`. Items:

```powerfx
SortByColumns(
    Filter(BestInnovatorIndividual,
        NominatorEmail = varUserEmail,
        (varBrowseStatus = "All" || NominationStatus.Value = varBrowseStatus),
        (varBrowseId = 0 || ID = varBrowseId)
    ),
    "Modified", SortOrder.Descending
)
```

Use `ThisItem.ID`, `ThisItem.Modified`, `ThisItem.NominationStatus.Value`, and `ThisItem.NominatedEmployee.DisplayName` in native labels. Reference Text = `"IND_INNOVATION-" & Text(ThisItem.ID, "000000")`. An Open button inside this gallery uses the following OnSelect; it queries the clicked ID again before opening. Inactive/retired categories can still open historical records.

```powerfx
If(!varIsBusy,
    Set(varIsBusy, true);
    Set(varOpenOK, true);
    IfError(
        Refresh(BestInnovatorIndividual);
        Set(varRecordII, LookUp(BestInnovatorIndividual, ID = ThisItem.ID && NominatorEmail = varUserEmail));
        Refresh(AwardCategories);
        Set(varCategory, LookUp(AwardCategories, ID = varRecordII.Category.Id));
        true,
        Set(varOpenOK, false);
        false
    );
    If(!varOpenOK || IsBlank(varRecordII.ID) || varCategory.CategoryCode <> "IND_INNOVATION" ||
       IsBlank(varRecordII.QuestionSetVersion) || varRecordII.QuestionSetVersion < 1 ||
       IsBlank(varRecordII.QuestionCount) || varRecordII.QuestionCount < 3 || varRecordII.QuestionCount > 6 ||
       varRecordII.QuestionCount <> RoundDown(varRecordII.QuestionCount,0) ||
       IsBlank(varRecordII.Q1PromptSnapshot) || IsBlank(varRecordII.Q2PromptSnapshot) || IsBlank(varRecordII.Q3PromptSnapshot) ||
       (varRecordII.QuestionCount>=4 && IsBlank(varRecordII.Q4PromptSnapshot)) ||
       (varRecordII.QuestionCount>=5 && IsBlank(varRecordII.Q5PromptSnapshot)) ||
       (varRecordII.QuestionCount>=6 && IsBlank(varRecordII.Q6PromptSnapshot)) ||
       !(varRecordII.NominationStatus.Value in ["Draft", "Submitted"]),
        Set(varIsBusy, false);
        Notify("Unable to open this nomination. Check access and the saved category/question metadata.", NotificationType.Error),
        Set(varAwardType, "Individual");
        Set(varNominationId, varRecordII.ID);
        Set(varLoadedModified, varRecordII.Modified);
        Set(varQuestionVersion, varRecordII.QuestionSetVersion);
        Set(varQuestionCount, varRecordII.QuestionCount);
        Set(varRole, Coalesce(varRecordII.EmployeeRole, ""));
        Set(varLevel, Coalesce(varRecordII.EmployeeLevel.Value, ""));
        Set(varNominator, varRecordII.NominatedBy);
        Set(varEmployee, Coalesce(varRecordII.NominatedEmployee, varEmptyPerson));
        Set(varPrimaryContact, varEmptyPerson);
        Set(varTeamName, "");
        Clear(colTeamMembers);
        ClearCollect(colAnswers, Table(
    {Slot: 1, Prompt: Coalesce(varRecordII.Q1PromptSnapshot, ""), Required: Coalesce(varRecordII.Q1RequiredSnapshot, false), Response: Coalesce(varRecordII.Q1Response, "")},
    {Slot: 2, Prompt: Coalesce(varRecordII.Q2PromptSnapshot, ""), Required: Coalesce(varRecordII.Q2RequiredSnapshot, false), Response: Coalesce(varRecordII.Q2Response, "")},
    {Slot: 3, Prompt: Coalesce(varRecordII.Q3PromptSnapshot, ""), Required: Coalesce(varRecordII.Q3RequiredSnapshot, false), Response: Coalesce(varRecordII.Q3Response, "")},
    {Slot: 4, Prompt: Coalesce(varRecordII.Q4PromptSnapshot, ""), Required: Coalesce(varRecordII.Q4RequiredSnapshot, false), Response: Coalesce(varRecordII.Q4Response, "")},
    {Slot: 5, Prompt: Coalesce(varRecordII.Q5PromptSnapshot, ""), Required: Coalesce(varRecordII.Q5RequiredSnapshot, false), Response: Coalesce(varRecordII.Q5Response, "")},
    {Slot: 6, Prompt: Coalesce(varRecordII.Q6PromptSnapshot, ""), Required: Coalesce(varRecordII.Q6RequiredSnapshot, false), Response: Coalesce(varRecordII.Q6Response, "")}
));
        Set(varReadOnly, varRecordII.NominationStatus.Value = "Submitted");
        Set(varSubmissionComplete, varReadOnly);
        Set(varSubmittedOn, varRecordII.SubmittedOn);
        Set(varCategoryComplete, true);
        Set(varDetailsComplete, DetailsValid);
        Set(varResponsesComplete, ResponsesValid);
        Set(varDeclarationAccepted, false);
        Set(varHasChanges, false);
        Set(varSaveIntent, "Draft");
        ResetForm(frmBestInnovatorIndividual);
        If(varReadOnly, ViewForm(frmBestInnovatorIndividual), EditForm(frmBestInnovatorIndividual));
        Set(varIsBusy, false);
        Navigate(scrBestInnovatorIndividual, ScreenTransition.None)
    )
)
```

Submitted items reuse this same typed form in View mode, including native file download. Form entry actions are hidden. This is the read-only screen implementation; a separate duplicate scrViewNomination is unnecessary.

#### Check this category before continuing

Save an incomplete draft, retain its ID, attach a small synthetic file, save again, reopen it, complete required answers, review unsaved changes, and submit. Confirm one item, correct snapshots, declaration and SubmittedOn. Reopen read-only. Test failed save/retry and concurrent modification. Use the full acceptance checklist; no runtime results are claimed here.

#### Question control properties

Insert a manual container inside each response card. Keep these exact unique names. Set label Font to Segoe UI, heading Color to Theme.Heading, body/counter Color to Theme.Muted. All labels wrap. Use the common input styling from the layout guide.

##### Slot 1

| Control / property | Formula or value |
|---|---|
| `dcIIQ1Response.Visible` | `1 <= varQuestionCount` |
| `dcIIQ1Response.X` / Y | `0` / `0` |
| `dcIIQ1Response.Width` | `Parent.Width` |
| `dcIIQ1Response.Height` | `If(Self.Visible, cntIIQ1.Y + cntIIQ1.Height + If(IsBlank(Self.Error), 0, errIIQ1.Height + 8) + 18, 0)` |
| `cntIIQ1` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntIIQ1.Height` | `lblIIQ1Counter.Y + lblIIQ1Counter.Height + 14` |
| `lblIIQ1Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblIIQ1Heading.Text` | `With({p:LookUp(colAnswers,Slot=1,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 1")) & If(LookUp(colAnswers,Slot=1,Required)," *","")` |
| `lblIIQ1Prompt` | X `22`; Y `lblIIQ1Heading.Y+lblIIQ1Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblIIQ1Prompt.Text` | `With({p:LookUp(colAnswers,Slot=1,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtIIQ1` | X `22`; Y `lblIIQ1Prompt.Y+lblIIQ1Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtIIQ1.Default` | `LookUp(colAnswers,Slot=1,Response)` |
| `txtIIQ1.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtIIQ1.DelayOutput` | `false` |
| `txtIIQ1.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcIIQ1Response.DisplayMode)` |
| `txtIIQ1.AccessibleLabel` | `LookUp(colAnswers,Slot=1,Prompt) & If(LookUp(colAnswers,Slot=1,Required),". Required", ". Optional")` |
| `lblIIQ1Counter` | X `22`; Y `txtIIQ1.Y+txtIIQ1.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblIIQ1Counter.Text` | `Text(Len(txtIIQ1.Text)) & " / " & Text(varMaxResponseLength)` |

`txtIIQ1.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=1), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 2

| Control / property | Formula or value |
|---|---|
| `dcIIQ2Response.Visible` | `2 <= varQuestionCount` |
| `dcIIQ2Response.X` / Y | `0` / `1` |
| `dcIIQ2Response.Width` | `Parent.Width` |
| `dcIIQ2Response.Height` | `If(Self.Visible, cntIIQ2.Y + cntIIQ2.Height + If(IsBlank(Self.Error), 0, errIIQ2.Height + 8) + 18, 0)` |
| `cntIIQ2` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntIIQ2.Height` | `lblIIQ2Counter.Y + lblIIQ2Counter.Height + 14` |
| `lblIIQ2Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblIIQ2Heading.Text` | `With({p:LookUp(colAnswers,Slot=2,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 2")) & If(LookUp(colAnswers,Slot=2,Required)," *","")` |
| `lblIIQ2Prompt` | X `22`; Y `lblIIQ2Heading.Y+lblIIQ2Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblIIQ2Prompt.Text` | `With({p:LookUp(colAnswers,Slot=2,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtIIQ2` | X `22`; Y `lblIIQ2Prompt.Y+lblIIQ2Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtIIQ2.Default` | `LookUp(colAnswers,Slot=2,Response)` |
| `txtIIQ2.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtIIQ2.DelayOutput` | `false` |
| `txtIIQ2.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcIIQ2Response.DisplayMode)` |
| `txtIIQ2.AccessibleLabel` | `LookUp(colAnswers,Slot=2,Prompt) & If(LookUp(colAnswers,Slot=2,Required),". Required", ". Optional")` |
| `lblIIQ2Counter` | X `22`; Y `txtIIQ2.Y+txtIIQ2.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblIIQ2Counter.Text` | `Text(Len(txtIIQ2.Text)) & " / " & Text(varMaxResponseLength)` |

`txtIIQ2.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=2), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 3

| Control / property | Formula or value |
|---|---|
| `dcIIQ3Response.Visible` | `3 <= varQuestionCount` |
| `dcIIQ3Response.X` / Y | `0` / `2` |
| `dcIIQ3Response.Width` | `Parent.Width` |
| `dcIIQ3Response.Height` | `If(Self.Visible, cntIIQ3.Y + cntIIQ3.Height + If(IsBlank(Self.Error), 0, errIIQ3.Height + 8) + 18, 0)` |
| `cntIIQ3` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntIIQ3.Height` | `lblIIQ3Counter.Y + lblIIQ3Counter.Height + 14` |
| `lblIIQ3Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblIIQ3Heading.Text` | `With({p:LookUp(colAnswers,Slot=3,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 3")) & If(LookUp(colAnswers,Slot=3,Required)," *","")` |
| `lblIIQ3Prompt` | X `22`; Y `lblIIQ3Heading.Y+lblIIQ3Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblIIQ3Prompt.Text` | `With({p:LookUp(colAnswers,Slot=3,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtIIQ3` | X `22`; Y `lblIIQ3Prompt.Y+lblIIQ3Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtIIQ3.Default` | `LookUp(colAnswers,Slot=3,Response)` |
| `txtIIQ3.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtIIQ3.DelayOutput` | `false` |
| `txtIIQ3.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcIIQ3Response.DisplayMode)` |
| `txtIIQ3.AccessibleLabel` | `LookUp(colAnswers,Slot=3,Prompt) & If(LookUp(colAnswers,Slot=3,Required),". Required", ". Optional")` |
| `lblIIQ3Counter` | X `22`; Y `txtIIQ3.Y+txtIIQ3.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblIIQ3Counter.Text` | `Text(Len(txtIIQ3.Text)) & " / " & Text(varMaxResponseLength)` |

`txtIIQ3.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=3), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 4

| Control / property | Formula or value |
|---|---|
| `dcIIQ4Response.Visible` | `4 <= varQuestionCount` |
| `dcIIQ4Response.X` / Y | `0` / `3` |
| `dcIIQ4Response.Width` | `Parent.Width` |
| `dcIIQ4Response.Height` | `If(Self.Visible, cntIIQ4.Y + cntIIQ4.Height + If(IsBlank(Self.Error), 0, errIIQ4.Height + 8) + 18, 0)` |
| `cntIIQ4` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntIIQ4.Height` | `lblIIQ4Counter.Y + lblIIQ4Counter.Height + 14` |
| `lblIIQ4Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblIIQ4Heading.Text` | `With({p:LookUp(colAnswers,Slot=4,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 4")) & If(LookUp(colAnswers,Slot=4,Required)," *","")` |
| `lblIIQ4Prompt` | X `22`; Y `lblIIQ4Heading.Y+lblIIQ4Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblIIQ4Prompt.Text` | `With({p:LookUp(colAnswers,Slot=4,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtIIQ4` | X `22`; Y `lblIIQ4Prompt.Y+lblIIQ4Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtIIQ4.Default` | `LookUp(colAnswers,Slot=4,Response)` |
| `txtIIQ4.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtIIQ4.DelayOutput` | `false` |
| `txtIIQ4.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcIIQ4Response.DisplayMode)` |
| `txtIIQ4.AccessibleLabel` | `LookUp(colAnswers,Slot=4,Prompt) & If(LookUp(colAnswers,Slot=4,Required),". Required", ". Optional")` |
| `lblIIQ4Counter` | X `22`; Y `txtIIQ4.Y+txtIIQ4.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblIIQ4Counter.Text` | `Text(Len(txtIIQ4.Text)) & " / " & Text(varMaxResponseLength)` |

`txtIIQ4.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=4), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 5

| Control / property | Formula or value |
|---|---|
| `dcIIQ5Response.Visible` | `5 <= varQuestionCount` |
| `dcIIQ5Response.X` / Y | `0` / `4` |
| `dcIIQ5Response.Width` | `Parent.Width` |
| `dcIIQ5Response.Height` | `If(Self.Visible, cntIIQ5.Y + cntIIQ5.Height + If(IsBlank(Self.Error), 0, errIIQ5.Height + 8) + 18, 0)` |
| `cntIIQ5` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntIIQ5.Height` | `lblIIQ5Counter.Y + lblIIQ5Counter.Height + 14` |
| `lblIIQ5Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblIIQ5Heading.Text` | `With({p:LookUp(colAnswers,Slot=5,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 5")) & If(LookUp(colAnswers,Slot=5,Required)," *","")` |
| `lblIIQ5Prompt` | X `22`; Y `lblIIQ5Heading.Y+lblIIQ5Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblIIQ5Prompt.Text` | `With({p:LookUp(colAnswers,Slot=5,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtIIQ5` | X `22`; Y `lblIIQ5Prompt.Y+lblIIQ5Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtIIQ5.Default` | `LookUp(colAnswers,Slot=5,Response)` |
| `txtIIQ5.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtIIQ5.DelayOutput` | `false` |
| `txtIIQ5.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcIIQ5Response.DisplayMode)` |
| `txtIIQ5.AccessibleLabel` | `LookUp(colAnswers,Slot=5,Prompt) & If(LookUp(colAnswers,Slot=5,Required),". Required", ". Optional")` |
| `lblIIQ5Counter` | X `22`; Y `txtIIQ5.Y+txtIIQ5.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblIIQ5Counter.Text` | `Text(Len(txtIIQ5.Text)) & " / " & Text(varMaxResponseLength)` |

`txtIIQ5.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=5), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 6

| Control / property | Formula or value |
|---|---|
| `dcIIQ6Response.Visible` | `6 <= varQuestionCount` |
| `dcIIQ6Response.X` / Y | `0` / `5` |
| `dcIIQ6Response.Width` | `Parent.Width` |
| `dcIIQ6Response.Height` | `If(Self.Visible, cntIIQ6.Y + cntIIQ6.Height + If(IsBlank(Self.Error), 0, errIIQ6.Height + 8) + 18, 0)` |
| `cntIIQ6` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntIIQ6.Height` | `lblIIQ6Counter.Y + lblIIQ6Counter.Height + 14` |
| `lblIIQ6Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblIIQ6Heading.Text` | `With({p:LookUp(colAnswers,Slot=6,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 6")) & If(LookUp(colAnswers,Slot=6,Required)," *","")` |
| `lblIIQ6Prompt` | X `22`; Y `lblIIQ6Heading.Y+lblIIQ6Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblIIQ6Prompt.Text` | `With({p:LookUp(colAnswers,Slot=6,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtIIQ6` | X `22`; Y `lblIIQ6Prompt.Y+lblIIQ6Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtIIQ6.Default` | `LookUp(colAnswers,Slot=6,Response)` |
| `txtIIQ6.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtIIQ6.DelayOutput` | `false` |
| `txtIIQ6.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcIIQ6Response.DisplayMode)` |
| `txtIIQ6.AccessibleLabel` | `LookUp(colAnswers,Slot=6,Prompt) & If(LookUp(colAnswers,Slot=6,Required),". Required", ". Optional")` |
| `lblIIQ6Counter` | X `22`; Y `txtIIQ6.Y+txtIIQ6.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblIIQ6Counter.Text` | `Text(Len(txtIIQ6.Text)) & " / " & Text(varMaxResponseLength)` |

`txtIIQ6.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=6), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

#### BestInnovatorIndividual: form dimensions and missing-property completion

Set `frmBestInnovatorIndividual.Width` from its actual parent as described above. Set `frmBestInnovatorIndividual.Height` to:

```powerfx
dcIIQ1Response.Height +
dcIIQ2Response.Height +
dcIIQ3Response.Height +
dcIIQ4Response.Height +
dcIIQ5Response.Height +
dcIIQ6Response.Height +
dcIIAttachments.Height +
24
```


Rename each generated response error label as listed. Keep it directly inside the response card, not inside the question container. Set AutoHeight=true, Height=10, X=22, Width=Parent.Width-44, Text=Parent.Error, Visible=!IsBlank(Parent.Error), Color=Theme.Error, Size=9, Live=Live.Assertive. Hide only the redundant generated response field-heading labels.

| Error label | Parent card | Y |
|---|---|---|
| `errIIQ1` | `dcIIQ1Response` | `cntIIQ1.Y + cntIIQ1.Height + 4` |
| `errIIQ2` | `dcIIQ2Response` | `cntIIQ2.Y + cntIIQ2.Height + 4` |
| `errIIQ3` | `dcIIQ3Response` | `cntIIQ3.Y + cntIIQ3.Height + 4` |
| `errIIQ4` | `dcIIQ4Response` | `cntIIQ4.Y + cntIIQ4.Height + 4` |
| `errIIQ5` | `dcIIQ5Response` | `cntIIQ5.Y + cntIIQ5.Height + 4` |
| `errIIQ6` | `dcIIQ6Response` | `cntIIQ6.Y + cntIIQ6.Height + 4` |

Set these input properties in addition to the question tables:

| Input | BorderColor | Tooltip |
|---|---|---|
| `txtIIQ1` | `If(IsBlank(dcIIQ1Response.Error), dcIIQ1Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 1, Prompt)` |
| `txtIIQ2` | `If(IsBlank(dcIIQ2Response.Error), dcIIQ2Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 2, Prompt)` |
| `txtIIQ3` | `If(IsBlank(dcIIQ3Response.Error), dcIIQ3Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 3, Prompt)` |
| `txtIIQ4` | `If(IsBlank(dcIIQ4Response.Error), dcIIQ4Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 4, Prompt)` |
| `txtIIQ5` | `If(IsBlank(dcIIQ5Response.Error), dcIIQ5Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 5, Prompt)` |
| `txtIIQ6` | `If(IsBlank(dcIIQ6Response.Error), dcIIQ6Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 6, Prompt)` |

For all six inputs use Font=`Font.'Segoe UI'`, Size=`9.75`, Color=`Theme.Body`, Fill=`Theme.Surface`, BorderThickness=`1`, FocusedBorderColor=`Theme.Primary`, FocusedBorderThickness=`2`, PaddingLeft/Right=`11`, PaddingTop/Bottom=`9`, all corner radii=`4`, and TabIndex=`0`. Set heading Font=`Font.'Segoe UI'` and Color=`Theme.Heading`; prompt/counter Font=`Font.'Segoe UI'` and Color=`Theme.Muted`. Prompt AutoHeight=`true`, base Height=`34`, Size=`9.75`; counter AutoHeight=`false`, Height=`18`. All labels Wrap=`true`.


#### BestInnovatorIndividual: native attachments and form-level errors

Keep `attII` directly inside `dcIIAttachments`. Retain the generated DataField, Items, limits, and native binding settings. Do not replace an attachment control with a collection-backed file picker.

| Property | Value |
|---|---|
| `dcIIAttachments.Visible` | `true` |
| `dcIIAttachments.Width` | `Parent.Width` |
| `dcIIAttachments.Height` | `270` |
| `dcIIAttachments.Required` | `false` |
| `dcIIAttachments.Update` | `attII.Attachments` |
| `attII.Items` | `Parent.Default` |
| `attII.DisplayMode` | `If(varIsBusy, DisplayMode.Disabled, Parent.DisplayMode)` |

For `attII.OnAddFile`, `attII.OnRemoveFile`, and `attII.OnUndoRemoveFile`, use the same action:

```powerfx
Set(varHasChanges, true);
Set(varDeclarationAccepted, false);
Set(varResponsesComplete, false)
```

The attachment layout can retain the generated label/editor coordinates. If restyling it, keep the generated error label visible and reserve space for its complete text. Do not suppress native validation messages.

Add a classic label `lblSaveErrorII` immediately after the form in the scrolling content container. Use the same X and Width as the form, Y=`frmBestInnovatorIndividual.Y + frmBestInnovatorIndividual.Height + 8`, AutoHeight=`true`, Text=`frmBestInnovatorIndividual.Error`, Visible=`!IsBlank(frmBestInnovatorIndividual.Error)`, Color=`Theme.Error`, and Live=`Live.Assertive`. Place the action row after this label when visible so errors from hidden metadata cards are not lost. Do not reset inputs on failure.


#### BestInnovatorIndividual: action controls

| Control | Text | Visible | DisplayMode |
|---|---|---|---|
| `btnIISaveDraft` | `"Save draft"` | `!varReadOnly` | `If(varIsBusy \|\| varReadOnly \|\| !varCategoryComplete, DisplayMode.Disabled, DisplayMode.Edit)` |
| `btnIIReview` | `"Review"` | `!varReadOnly` | `If(varIsBusy \|\| varReadOnly, DisplayMode.Disabled, DisplayMode.Edit)` |
| `btnIIBack` | `"Back to details"` | `!varReadOnly` | `If(varIsBusy, DisplayMode.Disabled, DisplayMode.Edit)` |

Use the complete OnSelect blocks above for these controls. Do not append a status Patch directly after SubmitForm. A read-only Back to My nominations button can use `Navigate(scrMyNominations, ScreenTransition.None)` with Visible=`varReadOnly`.


<a id="form-ic"></a>

### MDAward: IND_CUSTOMER / IC

Use the common form-building and scrolling rules above. These formulas target classic controls and English Power Fx separators. They are not yet Studio-compiled or runtime-tested.

#### Controls to create

Screen `scrMDAward`; Edit form `frmMDAward`; saved-record variable `varRecordIC`; latest-record variable `varLatestIC`. Create six response text inputs `txtICQ1` … `txtICQ6` in the corresponding response cards, and keep native attachment input `attIC` inside `dcICAttachments`.

Form DataSource = `MDAward`; Item = `varRecordIC`; DefaultMode = `FormMode.New`; NumberOfColumns = `1`; SnapToColumns = `false`. See layout guide for X/Y/Width/Height. Use the form's generated cards and unlock them. Preserve generated DataField strings exactly; if the connector shows a display name with spaces, use Studio's actual generated identifier. Required = `false` on entry cards to allow incomplete drafts; submission requirements are enforced separately. Do not remove metadata cards just because they are hidden.

Response cards are `dcICQ1Response` … `dcICQ6Response`. The other Q cards hold snapshots/flags and are hidden. Do not rename a response card to its text input name.

#### scrMDAward.OnVisible

```powerfx
Set(varCurrentStep, 3)
```

Do not call NewForm/ResetForm here: returning from review must preserve inputs and queued files.

#### All card Update properties

| SharePoint DataField / card | Update formula |
|---|---|
| `Title` / `dcICTitle` | `Left(varCategory.CategoryCode & " - " & If(varAwardType = "Individual", Coalesce(varEmployee.DisplayName, "Draft"), If(IsBlank(Trim(varTeamName)), "Draft", varTeamName)),255)` |
| `Category` / `dcICCategory` | `{Id: varCategory.ID, Value: varCategory.Title}` |
| `QuestionSetVersion` / `dcICQuestionSetVersion` | `varQuestionVersion` |
| `QuestionCount` / `dcICQuestionCount` | `varQuestionCount` |
| `NominatedBy` / `dcICNominatedBy` | `varNominator` |
| `NominatorEmail` / `dcICNominatorEmail` | `varUserEmail` |
| `EmployeeRole` / `dcICEmployeeRole` | `Trim(varRole)` |
| `EmployeeLevel` / `dcICEmployeeLevel` | `If(IsBlank(varLevel), Blank(), LookUp(Choices(MDAward.EmployeeLevel), Value = varLevel))` |
| `NominationStatus` / `dcICNominationStatus` | `{Value: "Draft"}` |
| `DeclarationAccepted` / `dcICDeclarationAccepted` | `false` |
| `SubmittedOn` / `dcICSubmittedOn` | `Blank()` |
| `NominatedEmployee` / `dcICNominatedEmployee` | `If(IsBlank(varEmployee.Claims), Blank(), varEmployee)` |
| `Q1PromptSnapshot` / `dcICQ1PromptSnapshot` | `LookUp(colAnswers, Slot = 1, Prompt)` |
| `Q1RequiredSnapshot` / `dcICQ1RequiredSnapshot` | `LookUp(colAnswers, Slot = 1, Required)` |
| `Q1Response` / `dcICQ1Response` | `If(1 <= varQuestionCount, txtICQ1.Text, "")` |
| `Q2PromptSnapshot` / `dcICQ2PromptSnapshot` | `LookUp(colAnswers, Slot = 2, Prompt)` |
| `Q2RequiredSnapshot` / `dcICQ2RequiredSnapshot` | `LookUp(colAnswers, Slot = 2, Required)` |
| `Q2Response` / `dcICQ2Response` | `If(2 <= varQuestionCount, txtICQ2.Text, "")` |
| `Q3PromptSnapshot` / `dcICQ3PromptSnapshot` | `LookUp(colAnswers, Slot = 3, Prompt)` |
| `Q3RequiredSnapshot` / `dcICQ3RequiredSnapshot` | `LookUp(colAnswers, Slot = 3, Required)` |
| `Q3Response` / `dcICQ3Response` | `If(3 <= varQuestionCount, txtICQ3.Text, "")` |
| `Q4PromptSnapshot` / `dcICQ4PromptSnapshot` | `LookUp(colAnswers, Slot = 4, Prompt)` |
| `Q4RequiredSnapshot` / `dcICQ4RequiredSnapshot` | `LookUp(colAnswers, Slot = 4, Required)` |
| `Q4Response` / `dcICQ4Response` | `If(4 <= varQuestionCount, txtICQ4.Text, "")` |
| `Q5PromptSnapshot` / `dcICQ5PromptSnapshot` | `LookUp(colAnswers, Slot = 5, Prompt)` |
| `Q5RequiredSnapshot` / `dcICQ5RequiredSnapshot` | `LookUp(colAnswers, Slot = 5, Required)` |
| `Q5Response` / `dcICQ5Response` | `If(5 <= varQuestionCount, txtICQ5.Text, "")` |
| `Q6PromptSnapshot` / `dcICQ6PromptSnapshot` | `LookUp(colAnswers, Slot = 6, Prompt)` |
| `Q6RequiredSnapshot` / `dcICQ6RequiredSnapshot` | `LookUp(colAnswers, Slot = 6, Required)` |
| `Q6Response` / `dcICQ6Response` | `If(6 <= varQuestionCount, txtICQ6.Text, "")` |
| Native Attachments / `dcICAttachments` | `attIC.Attachments` |

All cards except Q1–Q6 Response and Attachments: Visible = `false`, Height = `0`, Required = `false`. Set form-card DisplayMode to `Parent.DisplayMode`. Set each child editor DisplayMode to its card's DisplayMode, and disable it while varIsBusy. Hidden metadata's Update properties still participate in SubmitForm.

Keep native attachment Items = `Parent.Default` when directly inside its data card, and retain the generated attachment DataField (often `"{Attachments}"`). Do not type a guessed DataField. Preserve the other generated attachment properties, including MaxAttachments/MaxAttachmentSize, until an approved policy is chosen. Appending files does not save them until SubmitForm completes.

#### btnICSaveDraft.OnSelect

```powerfx
If(!varIsBusy && !varReadOnly && varCategoryComplete,
    ClearCollect(colCapturedAnswers, Table(
    {Slot: 1, Prompt: LookUp(colAnswers, Slot = 1, Prompt), Required: LookUp(colAnswers, Slot = 1, Required), Response: txtICQ1.Text},
    {Slot: 2, Prompt: LookUp(colAnswers, Slot = 2, Prompt), Required: LookUp(colAnswers, Slot = 2, Required), Response: txtICQ2.Text},
    {Slot: 3, Prompt: LookUp(colAnswers, Slot = 3, Prompt), Required: LookUp(colAnswers, Slot = 3, Required), Response: txtICQ3.Text},
    {Slot: 4, Prompt: LookUp(colAnswers, Slot = 4, Prompt), Required: LookUp(colAnswers, Slot = 4, Required), Response: txtICQ4.Text},
    {Slot: 5, Prompt: LookUp(colAnswers, Slot = 5, Prompt), Required: LookUp(colAnswers, Slot = 5, Required), Response: txtICQ5.Text},
    {Slot: 6, Prompt: LookUp(colAnswers, Slot = 6, Prompt), Required: LookUp(colAnswers, Slot = 6, Required), Response: txtICQ6.Text}
));
ClearCollect(colAnswers, colCapturedAnswers);
    If(CountIf(colAnswers, Len(Response) > varMaxResponseLength) > 0,
        Notify("A response exceeds the configured limit.", NotificationType.Warning),
        Set(varIsBusy, true);
Set(varPreflightOK, true);
If(!IsBlank(varNominationId),
    IfError(
        Refresh(MDAward);
        Set(varLatestIC, LookUp(MDAward, ID = varNominationId));
        If(IsBlank(varLatestIC.ID) ||
           varLatestIC.NominationStatus.Value <> "Draft" ||
           varLatestIC.Modified <> varLoadedModified,
            Set(varPreflightOK, false);
            Notify("This item changed or is no longer an editable draft. Keep a copy of your changes, then reopen it from My nominations.", NotificationType.Error)
        );
        true,
        Set(varPreflightOK, false);
        Notify("Could not check the saved draft. Your changes have been retained; try again when connected.", NotificationType.Error);
        false
    )
);
If(varPreflightOK,
    Set(varSaveIntent, "Draft");
    SubmitForm(frmMDAward),
    Set(varIsBusy, false)
)
    )
)
```

#### btnICReview.OnSelect

Set DisplayMode to `If(varIsBusy || varReadOnly, DisplayMode.Disabled, DisplayMode.Edit)`.

```powerfx
ClearCollect(colCapturedAnswers, Table(
    {Slot: 1, Prompt: LookUp(colAnswers, Slot = 1, Prompt), Required: LookUp(colAnswers, Slot = 1, Required), Response: txtICQ1.Text},
    {Slot: 2, Prompt: LookUp(colAnswers, Slot = 2, Prompt), Required: LookUp(colAnswers, Slot = 2, Required), Response: txtICQ2.Text},
    {Slot: 3, Prompt: LookUp(colAnswers, Slot = 3, Prompt), Required: LookUp(colAnswers, Slot = 3, Required), Response: txtICQ3.Text},
    {Slot: 4, Prompt: LookUp(colAnswers, Slot = 4, Prompt), Required: LookUp(colAnswers, Slot = 4, Required), Response: txtICQ4.Text},
    {Slot: 5, Prompt: LookUp(colAnswers, Slot = 5, Prompt), Required: LookUp(colAnswers, Slot = 5, Required), Response: txtICQ5.Text},
    {Slot: 6, Prompt: LookUp(colAnswers, Slot = 6, Prompt), Required: LookUp(colAnswers, Slot = 6, Required), Response: txtICQ6.Text}
));
ClearCollect(colAnswers, colCapturedAnswers);
Set(varDetailsComplete, DetailsValid);
Set(varResponsesComplete, ResponsesValid);
If(!DetailsValid,
    Notify("Complete nominee details, role and level before review.", NotificationType.Warning);
    Navigate(scrNomineeDetails, ScreenTransition.None),
    !ResponsesValid,
    Notify("Complete every required response before review.", NotificationType.Warning),
    Set(varDeclarationAccepted, false);
    ClearCollect(colReviewFiles, ForAll(attIC.Attachments As file, {FileName: file.Name}));
    Set(varCurrentStep, 4);
    Navigate(scrReview, ScreenTransition.None)
)
```

`colCapturedAnswers` prevents clearing the source table while reading its snapshots. Review reads current text controls directly, so it does not depend on OnChange timing. If Studio exposes the native file-name column as DisplayName instead of Name, use that actual column in the one FileName projection above; do not change attachment Items/Update or collect file bodies.

#### frmMDAward.OnSuccess

```powerfx
Set(varRecordIC, frmMDAward.LastSubmit);
Set(varNominationId, varRecordIC.ID);
Set(varLoadedModified, varRecordIC.Modified);
EditForm(frmMDAward);
Set(varHasChanges, false);
If(varSaveIntent = "Submit",
    IfError(
        Set(varRecordIC,
            Patch(MDAward, varRecordIC,
                {NominationStatus: {Value: "Submitted"},
                 DeclarationAccepted: true, SubmittedOn: Now()}
            )
        );
        Set(varLoadedModified, varRecordIC.Modified);
        Set(varSubmittedOn, varRecordIC.SubmittedOn);
        Set(varSubmissionComplete, true);
        Set(varReadOnly, true);
        Set(varIsBusy, false);
        ViewForm(frmMDAward);
        Navigate(scrConfirmation, ScreenTransition.None);
        true,
        Set(varIsBusy, false);
        Set(varSubmissionComplete, false);
        Set(varSaveIntent, "Draft");
        Notify("Your draft save succeeded, but submission was not confirmed. Check My nominations before retrying. Your existing item ID is retained.", NotificationType.Error);
        false
    ),
    Set(varIsBusy, false);
    Notify("Draft saved. Reference: " & varCategory.CategoryCode & "-" & Text(varNominationId, "000000"), NotificationType.Success)
)
```

#### frmMDAward.OnFailure

```powerfx
Set(varIsBusy, false);
Set(varSubmissionComplete, false);
Set(varHasChanges, true);
Notify("Save was not confirmed. Your inputs are retained. If the connection timed out, check My nominations before retrying because the server may have saved the item.", NotificationType.Error)
```

#### Back to details

Use a native button; Visible = `!varReadOnly`; DisplayMode disabled while varIsBusy. Its OnSelect:

```powerfx
ClearCollect(colCapturedAnswers, Table(
    {Slot: 1, Prompt: LookUp(colAnswers, Slot = 1, Prompt), Required: LookUp(colAnswers, Slot = 1, Required), Response: txtICQ1.Text},
    {Slot: 2, Prompt: LookUp(colAnswers, Slot = 2, Prompt), Required: LookUp(colAnswers, Slot = 2, Required), Response: txtICQ2.Text},
    {Slot: 3, Prompt: LookUp(colAnswers, Slot = 3, Prompt), Required: LookUp(colAnswers, Slot = 3, Required), Response: txtICQ3.Text},
    {Slot: 4, Prompt: LookUp(colAnswers, Slot = 4, Prompt), Required: LookUp(colAnswers, Slot = 4, Required), Response: txtICQ4.Text},
    {Slot: 5, Prompt: LookUp(colAnswers, Slot = 5, Prompt), Required: LookUp(colAnswers, Slot = 5, Required), Response: txtICQ5.Text},
    {Slot: 6, Prompt: LookUp(colAnswers, Slot = 6, Prompt), Required: LookUp(colAnswers, Slot = 6, Required), Response: txtICQ6.Text}
));
ClearCollect(colAnswers, colCapturedAnswers);
Set(varDeclarationAccepted, false);
Set(varCurrentStep, 1);
Navigate(scrNomineeDetails, ScreenTransition.None)
```

#### My nominations gallery galMineIC

Visible = `varBrowseCode = "IND_CUSTOMER"`. Items:

```powerfx
SortByColumns(
    Filter(MDAward,
        NominatorEmail = varUserEmail,
        (varBrowseStatus = "All" || NominationStatus.Value = varBrowseStatus),
        (varBrowseId = 0 || ID = varBrowseId)
    ),
    "Modified", SortOrder.Descending
)
```

Use `ThisItem.ID`, `ThisItem.Modified`, `ThisItem.NominationStatus.Value`, and `ThisItem.NominatedEmployee.DisplayName` in native labels. Reference Text = `"IND_CUSTOMER-" & Text(ThisItem.ID, "000000")`. An Open button inside this gallery uses the following OnSelect; it queries the clicked ID again before opening. Inactive/retired categories can still open historical records.

```powerfx
If(!varIsBusy,
    Set(varIsBusy, true);
    Set(varOpenOK, true);
    IfError(
        Refresh(MDAward);
        Set(varRecordIC, LookUp(MDAward, ID = ThisItem.ID && NominatorEmail = varUserEmail));
        Refresh(AwardCategories);
        Set(varCategory, LookUp(AwardCategories, ID = varRecordIC.Category.Id));
        true,
        Set(varOpenOK, false);
        false
    );
    If(!varOpenOK || IsBlank(varRecordIC.ID) || varCategory.CategoryCode <> "IND_CUSTOMER" ||
       IsBlank(varRecordIC.QuestionSetVersion) || varRecordIC.QuestionSetVersion < 1 ||
       IsBlank(varRecordIC.QuestionCount) || varRecordIC.QuestionCount < 3 || varRecordIC.QuestionCount > 6 ||
       varRecordIC.QuestionCount <> RoundDown(varRecordIC.QuestionCount,0) ||
       IsBlank(varRecordIC.Q1PromptSnapshot) || IsBlank(varRecordIC.Q2PromptSnapshot) || IsBlank(varRecordIC.Q3PromptSnapshot) ||
       (varRecordIC.QuestionCount>=4 && IsBlank(varRecordIC.Q4PromptSnapshot)) ||
       (varRecordIC.QuestionCount>=5 && IsBlank(varRecordIC.Q5PromptSnapshot)) ||
       (varRecordIC.QuestionCount>=6 && IsBlank(varRecordIC.Q6PromptSnapshot)) ||
       !(varRecordIC.NominationStatus.Value in ["Draft", "Submitted"]),
        Set(varIsBusy, false);
        Notify("Unable to open this nomination. Check access and the saved category/question metadata.", NotificationType.Error),
        Set(varAwardType, "Individual");
        Set(varNominationId, varRecordIC.ID);
        Set(varLoadedModified, varRecordIC.Modified);
        Set(varQuestionVersion, varRecordIC.QuestionSetVersion);
        Set(varQuestionCount, varRecordIC.QuestionCount);
        Set(varRole, Coalesce(varRecordIC.EmployeeRole, ""));
        Set(varLevel, Coalesce(varRecordIC.EmployeeLevel.Value, ""));
        Set(varNominator, varRecordIC.NominatedBy);
        Set(varEmployee, Coalesce(varRecordIC.NominatedEmployee, varEmptyPerson));
        Set(varPrimaryContact, varEmptyPerson);
        Set(varTeamName, "");
        Clear(colTeamMembers);
        ClearCollect(colAnswers, Table(
    {Slot: 1, Prompt: Coalesce(varRecordIC.Q1PromptSnapshot, ""), Required: Coalesce(varRecordIC.Q1RequiredSnapshot, false), Response: Coalesce(varRecordIC.Q1Response, "")},
    {Slot: 2, Prompt: Coalesce(varRecordIC.Q2PromptSnapshot, ""), Required: Coalesce(varRecordIC.Q2RequiredSnapshot, false), Response: Coalesce(varRecordIC.Q2Response, "")},
    {Slot: 3, Prompt: Coalesce(varRecordIC.Q3PromptSnapshot, ""), Required: Coalesce(varRecordIC.Q3RequiredSnapshot, false), Response: Coalesce(varRecordIC.Q3Response, "")},
    {Slot: 4, Prompt: Coalesce(varRecordIC.Q4PromptSnapshot, ""), Required: Coalesce(varRecordIC.Q4RequiredSnapshot, false), Response: Coalesce(varRecordIC.Q4Response, "")},
    {Slot: 5, Prompt: Coalesce(varRecordIC.Q5PromptSnapshot, ""), Required: Coalesce(varRecordIC.Q5RequiredSnapshot, false), Response: Coalesce(varRecordIC.Q5Response, "")},
    {Slot: 6, Prompt: Coalesce(varRecordIC.Q6PromptSnapshot, ""), Required: Coalesce(varRecordIC.Q6RequiredSnapshot, false), Response: Coalesce(varRecordIC.Q6Response, "")}
));
        Set(varReadOnly, varRecordIC.NominationStatus.Value = "Submitted");
        Set(varSubmissionComplete, varReadOnly);
        Set(varSubmittedOn, varRecordIC.SubmittedOn);
        Set(varCategoryComplete, true);
        Set(varDetailsComplete, DetailsValid);
        Set(varResponsesComplete, ResponsesValid);
        Set(varDeclarationAccepted, false);
        Set(varHasChanges, false);
        Set(varSaveIntent, "Draft");
        ResetForm(frmMDAward);
        If(varReadOnly, ViewForm(frmMDAward), EditForm(frmMDAward));
        Set(varIsBusy, false);
        Navigate(scrMDAward, ScreenTransition.None)
    )
)
```

Submitted items reuse this same typed form in View mode, including native file download. Form entry actions are hidden. This is the read-only screen implementation; a separate duplicate scrViewNomination is unnecessary.

#### Check this category before continuing

Save an incomplete draft, retain its ID, attach a small synthetic file, save again, reopen it, complete required answers, review unsaved changes, and submit. Confirm one item, correct snapshots, declaration and SubmittedOn. Reopen read-only. Test failed save/retry and concurrent modification. Use the full acceptance checklist; no runtime results are claimed here.

#### Question control properties

Insert a manual container inside each response card. Keep these exact unique names. Set label Font to Segoe UI, heading Color to Theme.Heading, body/counter Color to Theme.Muted. All labels wrap. Use the common input styling from the layout guide.

##### Slot 1

| Control / property | Formula or value |
|---|---|
| `dcICQ1Response.Visible` | `1 <= varQuestionCount` |
| `dcICQ1Response.X` / Y | `0` / `0` |
| `dcICQ1Response.Width` | `Parent.Width` |
| `dcICQ1Response.Height` | `If(Self.Visible, cntICQ1.Y + cntICQ1.Height + If(IsBlank(Self.Error), 0, errICQ1.Height + 8) + 18, 0)` |
| `cntICQ1` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntICQ1.Height` | `lblICQ1Counter.Y + lblICQ1Counter.Height + 14` |
| `lblICQ1Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblICQ1Heading.Text` | `With({p:LookUp(colAnswers,Slot=1,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 1")) & If(LookUp(colAnswers,Slot=1,Required)," *","")` |
| `lblICQ1Prompt` | X `22`; Y `lblICQ1Heading.Y+lblICQ1Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblICQ1Prompt.Text` | `With({p:LookUp(colAnswers,Slot=1,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtICQ1` | X `22`; Y `lblICQ1Prompt.Y+lblICQ1Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtICQ1.Default` | `LookUp(colAnswers,Slot=1,Response)` |
| `txtICQ1.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtICQ1.DelayOutput` | `false` |
| `txtICQ1.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcICQ1Response.DisplayMode)` |
| `txtICQ1.AccessibleLabel` | `LookUp(colAnswers,Slot=1,Prompt) & If(LookUp(colAnswers,Slot=1,Required),". Required", ". Optional")` |
| `lblICQ1Counter` | X `22`; Y `txtICQ1.Y+txtICQ1.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblICQ1Counter.Text` | `Text(Len(txtICQ1.Text)) & " / " & Text(varMaxResponseLength)` |

`txtICQ1.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=1), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 2

| Control / property | Formula or value |
|---|---|
| `dcICQ2Response.Visible` | `2 <= varQuestionCount` |
| `dcICQ2Response.X` / Y | `0` / `1` |
| `dcICQ2Response.Width` | `Parent.Width` |
| `dcICQ2Response.Height` | `If(Self.Visible, cntICQ2.Y + cntICQ2.Height + If(IsBlank(Self.Error), 0, errICQ2.Height + 8) + 18, 0)` |
| `cntICQ2` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntICQ2.Height` | `lblICQ2Counter.Y + lblICQ2Counter.Height + 14` |
| `lblICQ2Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblICQ2Heading.Text` | `With({p:LookUp(colAnswers,Slot=2,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 2")) & If(LookUp(colAnswers,Slot=2,Required)," *","")` |
| `lblICQ2Prompt` | X `22`; Y `lblICQ2Heading.Y+lblICQ2Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblICQ2Prompt.Text` | `With({p:LookUp(colAnswers,Slot=2,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtICQ2` | X `22`; Y `lblICQ2Prompt.Y+lblICQ2Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtICQ2.Default` | `LookUp(colAnswers,Slot=2,Response)` |
| `txtICQ2.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtICQ2.DelayOutput` | `false` |
| `txtICQ2.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcICQ2Response.DisplayMode)` |
| `txtICQ2.AccessibleLabel` | `LookUp(colAnswers,Slot=2,Prompt) & If(LookUp(colAnswers,Slot=2,Required),". Required", ". Optional")` |
| `lblICQ2Counter` | X `22`; Y `txtICQ2.Y+txtICQ2.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblICQ2Counter.Text` | `Text(Len(txtICQ2.Text)) & " / " & Text(varMaxResponseLength)` |

`txtICQ2.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=2), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 3

| Control / property | Formula or value |
|---|---|
| `dcICQ3Response.Visible` | `3 <= varQuestionCount` |
| `dcICQ3Response.X` / Y | `0` / `2` |
| `dcICQ3Response.Width` | `Parent.Width` |
| `dcICQ3Response.Height` | `If(Self.Visible, cntICQ3.Y + cntICQ3.Height + If(IsBlank(Self.Error), 0, errICQ3.Height + 8) + 18, 0)` |
| `cntICQ3` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntICQ3.Height` | `lblICQ3Counter.Y + lblICQ3Counter.Height + 14` |
| `lblICQ3Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblICQ3Heading.Text` | `With({p:LookUp(colAnswers,Slot=3,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 3")) & If(LookUp(colAnswers,Slot=3,Required)," *","")` |
| `lblICQ3Prompt` | X `22`; Y `lblICQ3Heading.Y+lblICQ3Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblICQ3Prompt.Text` | `With({p:LookUp(colAnswers,Slot=3,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtICQ3` | X `22`; Y `lblICQ3Prompt.Y+lblICQ3Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtICQ3.Default` | `LookUp(colAnswers,Slot=3,Response)` |
| `txtICQ3.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtICQ3.DelayOutput` | `false` |
| `txtICQ3.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcICQ3Response.DisplayMode)` |
| `txtICQ3.AccessibleLabel` | `LookUp(colAnswers,Slot=3,Prompt) & If(LookUp(colAnswers,Slot=3,Required),". Required", ". Optional")` |
| `lblICQ3Counter` | X `22`; Y `txtICQ3.Y+txtICQ3.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblICQ3Counter.Text` | `Text(Len(txtICQ3.Text)) & " / " & Text(varMaxResponseLength)` |

`txtICQ3.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=3), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 4

| Control / property | Formula or value |
|---|---|
| `dcICQ4Response.Visible` | `4 <= varQuestionCount` |
| `dcICQ4Response.X` / Y | `0` / `3` |
| `dcICQ4Response.Width` | `Parent.Width` |
| `dcICQ4Response.Height` | `If(Self.Visible, cntICQ4.Y + cntICQ4.Height + If(IsBlank(Self.Error), 0, errICQ4.Height + 8) + 18, 0)` |
| `cntICQ4` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntICQ4.Height` | `lblICQ4Counter.Y + lblICQ4Counter.Height + 14` |
| `lblICQ4Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblICQ4Heading.Text` | `With({p:LookUp(colAnswers,Slot=4,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 4")) & If(LookUp(colAnswers,Slot=4,Required)," *","")` |
| `lblICQ4Prompt` | X `22`; Y `lblICQ4Heading.Y+lblICQ4Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblICQ4Prompt.Text` | `With({p:LookUp(colAnswers,Slot=4,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtICQ4` | X `22`; Y `lblICQ4Prompt.Y+lblICQ4Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtICQ4.Default` | `LookUp(colAnswers,Slot=4,Response)` |
| `txtICQ4.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtICQ4.DelayOutput` | `false` |
| `txtICQ4.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcICQ4Response.DisplayMode)` |
| `txtICQ4.AccessibleLabel` | `LookUp(colAnswers,Slot=4,Prompt) & If(LookUp(colAnswers,Slot=4,Required),". Required", ". Optional")` |
| `lblICQ4Counter` | X `22`; Y `txtICQ4.Y+txtICQ4.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblICQ4Counter.Text` | `Text(Len(txtICQ4.Text)) & " / " & Text(varMaxResponseLength)` |

`txtICQ4.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=4), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 5

| Control / property | Formula or value |
|---|---|
| `dcICQ5Response.Visible` | `5 <= varQuestionCount` |
| `dcICQ5Response.X` / Y | `0` / `4` |
| `dcICQ5Response.Width` | `Parent.Width` |
| `dcICQ5Response.Height` | `If(Self.Visible, cntICQ5.Y + cntICQ5.Height + If(IsBlank(Self.Error), 0, errICQ5.Height + 8) + 18, 0)` |
| `cntICQ5` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntICQ5.Height` | `lblICQ5Counter.Y + lblICQ5Counter.Height + 14` |
| `lblICQ5Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblICQ5Heading.Text` | `With({p:LookUp(colAnswers,Slot=5,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 5")) & If(LookUp(colAnswers,Slot=5,Required)," *","")` |
| `lblICQ5Prompt` | X `22`; Y `lblICQ5Heading.Y+lblICQ5Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblICQ5Prompt.Text` | `With({p:LookUp(colAnswers,Slot=5,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtICQ5` | X `22`; Y `lblICQ5Prompt.Y+lblICQ5Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtICQ5.Default` | `LookUp(colAnswers,Slot=5,Response)` |
| `txtICQ5.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtICQ5.DelayOutput` | `false` |
| `txtICQ5.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcICQ5Response.DisplayMode)` |
| `txtICQ5.AccessibleLabel` | `LookUp(colAnswers,Slot=5,Prompt) & If(LookUp(colAnswers,Slot=5,Required),". Required", ". Optional")` |
| `lblICQ5Counter` | X `22`; Y `txtICQ5.Y+txtICQ5.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblICQ5Counter.Text` | `Text(Len(txtICQ5.Text)) & " / " & Text(varMaxResponseLength)` |

`txtICQ5.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=5), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 6

| Control / property | Formula or value |
|---|---|
| `dcICQ6Response.Visible` | `6 <= varQuestionCount` |
| `dcICQ6Response.X` / Y | `0` / `5` |
| `dcICQ6Response.Width` | `Parent.Width` |
| `dcICQ6Response.Height` | `If(Self.Visible, cntICQ6.Y + cntICQ6.Height + If(IsBlank(Self.Error), 0, errICQ6.Height + 8) + 18, 0)` |
| `cntICQ6` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntICQ6.Height` | `lblICQ6Counter.Y + lblICQ6Counter.Height + 14` |
| `lblICQ6Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblICQ6Heading.Text` | `With({p:LookUp(colAnswers,Slot=6,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 6")) & If(LookUp(colAnswers,Slot=6,Required)," *","")` |
| `lblICQ6Prompt` | X `22`; Y `lblICQ6Heading.Y+lblICQ6Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblICQ6Prompt.Text` | `With({p:LookUp(colAnswers,Slot=6,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtICQ6` | X `22`; Y `lblICQ6Prompt.Y+lblICQ6Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtICQ6.Default` | `LookUp(colAnswers,Slot=6,Response)` |
| `txtICQ6.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtICQ6.DelayOutput` | `false` |
| `txtICQ6.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcICQ6Response.DisplayMode)` |
| `txtICQ6.AccessibleLabel` | `LookUp(colAnswers,Slot=6,Prompt) & If(LookUp(colAnswers,Slot=6,Required),". Required", ". Optional")` |
| `lblICQ6Counter` | X `22`; Y `txtICQ6.Y+txtICQ6.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblICQ6Counter.Text` | `Text(Len(txtICQ6.Text)) & " / " & Text(varMaxResponseLength)` |

`txtICQ6.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=6), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

#### MDAward: form dimensions and missing-property completion

Set `frmMDAward.Width` from its actual parent as described above. Set `frmMDAward.Height` to:

```powerfx
dcICQ1Response.Height +
dcICQ2Response.Height +
dcICQ3Response.Height +
dcICQ4Response.Height +
dcICQ5Response.Height +
dcICQ6Response.Height +
dcICAttachments.Height +
24
```


Rename each generated response error label as listed. Keep it directly inside the response card, not inside the question container. Set AutoHeight=true, Height=10, X=22, Width=Parent.Width-44, Text=Parent.Error, Visible=!IsBlank(Parent.Error), Color=Theme.Error, Size=9, Live=Live.Assertive. Hide only the redundant generated response field-heading labels.

| Error label | Parent card | Y |
|---|---|---|
| `errICQ1` | `dcICQ1Response` | `cntICQ1.Y + cntICQ1.Height + 4` |
| `errICQ2` | `dcICQ2Response` | `cntICQ2.Y + cntICQ2.Height + 4` |
| `errICQ3` | `dcICQ3Response` | `cntICQ3.Y + cntICQ3.Height + 4` |
| `errICQ4` | `dcICQ4Response` | `cntICQ4.Y + cntICQ4.Height + 4` |
| `errICQ5` | `dcICQ5Response` | `cntICQ5.Y + cntICQ5.Height + 4` |
| `errICQ6` | `dcICQ6Response` | `cntICQ6.Y + cntICQ6.Height + 4` |

Set these input properties in addition to the question tables:

| Input | BorderColor | Tooltip |
|---|---|---|
| `txtICQ1` | `If(IsBlank(dcICQ1Response.Error), dcICQ1Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 1, Prompt)` |
| `txtICQ2` | `If(IsBlank(dcICQ2Response.Error), dcICQ2Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 2, Prompt)` |
| `txtICQ3` | `If(IsBlank(dcICQ3Response.Error), dcICQ3Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 3, Prompt)` |
| `txtICQ4` | `If(IsBlank(dcICQ4Response.Error), dcICQ4Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 4, Prompt)` |
| `txtICQ5` | `If(IsBlank(dcICQ5Response.Error), dcICQ5Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 5, Prompt)` |
| `txtICQ6` | `If(IsBlank(dcICQ6Response.Error), dcICQ6Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 6, Prompt)` |

For all six inputs use Font=`Font.'Segoe UI'`, Size=`9.75`, Color=`Theme.Body`, Fill=`Theme.Surface`, BorderThickness=`1`, FocusedBorderColor=`Theme.Primary`, FocusedBorderThickness=`2`, PaddingLeft/Right=`11`, PaddingTop/Bottom=`9`, all corner radii=`4`, and TabIndex=`0`. Set heading Font=`Font.'Segoe UI'` and Color=`Theme.Heading`; prompt/counter Font=`Font.'Segoe UI'` and Color=`Theme.Muted`. Prompt AutoHeight=`true`, base Height=`34`, Size=`9.75`; counter AutoHeight=`false`, Height=`18`. All labels Wrap=`true`.


#### MDAward: native attachments and form-level errors

Keep `attIC` directly inside `dcICAttachments`. Retain the generated DataField, Items, limits, and native binding settings. Do not replace an attachment control with a collection-backed file picker.

| Property | Value |
|---|---|
| `dcICAttachments.Visible` | `true` |
| `dcICAttachments.Width` | `Parent.Width` |
| `dcICAttachments.Height` | `270` |
| `dcICAttachments.Required` | `false` |
| `dcICAttachments.Update` | `attIC.Attachments` |
| `attIC.Items` | `Parent.Default` |
| `attIC.DisplayMode` | `If(varIsBusy, DisplayMode.Disabled, Parent.DisplayMode)` |

For `attIC.OnAddFile`, `attIC.OnRemoveFile`, and `attIC.OnUndoRemoveFile`, use the same action:

```powerfx
Set(varHasChanges, true);
Set(varDeclarationAccepted, false);
Set(varResponsesComplete, false)
```

The attachment layout can retain the generated label/editor coordinates. If restyling it, keep the generated error label visible and reserve space for its complete text. Do not suppress native validation messages.

Add a classic label `lblSaveErrorIC` immediately after the form in the scrolling content container. Use the same X and Width as the form, Y=`frmMDAward.Y + frmMDAward.Height + 8`, AutoHeight=`true`, Text=`frmMDAward.Error`, Visible=`!IsBlank(frmMDAward.Error)`, Color=`Theme.Error`, and Live=`Live.Assertive`. Place the action row after this label when visible so errors from hidden metadata cards are not lost. Do not reset inputs on failure.


#### MDAward: action controls

| Control | Text | Visible | DisplayMode |
|---|---|---|---|
| `btnICSaveDraft` | `"Save draft"` | `!varReadOnly` | `If(varIsBusy \|\| varReadOnly \|\| !varCategoryComplete, DisplayMode.Disabled, DisplayMode.Edit)` |
| `btnICReview` | `"Review"` | `!varReadOnly` | `If(varIsBusy \|\| varReadOnly, DisplayMode.Disabled, DisplayMode.Edit)` |
| `btnICBack` | `"Back to details"` | `!varReadOnly` | `If(varIsBusy, DisplayMode.Disabled, DisplayMode.Edit)` |

Use the complete OnSelect blocks above for these controls. Do not append a status Patch directly after SubmitForm. A read-only Back to My nominations button can use `Navigate(scrMyNominations, ScreenTransition.None)` with Visible=`varReadOnly`.


<a id="form-ie"></a>

### TrendMarcherAward: IND_EXCELLENCE / IE

Use the common form-building and scrolling rules above. These formulas target classic controls and English Power Fx separators. They are not yet Studio-compiled or runtime-tested.

#### Controls to create

Screen `scrTrendMarcherAward`; Edit form `frmTrendMarcherAward`; saved-record variable `varRecordIE`; latest-record variable `varLatestIE`. Create six response text inputs `txtIEQ1` … `txtIEQ6` in the corresponding response cards, and keep native attachment input `attIE` inside `dcIEAttachments`.

Form DataSource = `TrendMarcherAward`; Item = `varRecordIE`; DefaultMode = `FormMode.New`; NumberOfColumns = `1`; SnapToColumns = `false`. See layout guide for X/Y/Width/Height. Use the form's generated cards and unlock them. Preserve generated DataField strings exactly; if the connector shows a display name with spaces, use Studio's actual generated identifier. Required = `false` on entry cards to allow incomplete drafts; submission requirements are enforced separately. Do not remove metadata cards just because they are hidden.

Response cards are `dcIEQ1Response` … `dcIEQ6Response`. The other Q cards hold snapshots/flags and are hidden. Do not rename a response card to its text input name.

#### scrTrendMarcherAward.OnVisible

```powerfx
Set(varCurrentStep, 3)
```

Do not call NewForm/ResetForm here: returning from review must preserve inputs and queued files.

#### All card Update properties

| SharePoint DataField / card | Update formula |
|---|---|
| `Title` / `dcIETitle` | `Left(varCategory.CategoryCode & " - " & If(varAwardType = "Individual", Coalesce(varEmployee.DisplayName, "Draft"), If(IsBlank(Trim(varTeamName)), "Draft", varTeamName)),255)` |
| `Category` / `dcIECategory` | `{Id: varCategory.ID, Value: varCategory.Title}` |
| `QuestionSetVersion` / `dcIEQuestionSetVersion` | `varQuestionVersion` |
| `QuestionCount` / `dcIEQuestionCount` | `varQuestionCount` |
| `NominatedBy` / `dcIENominatedBy` | `varNominator` |
| `NominatorEmail` / `dcIENominatorEmail` | `varUserEmail` |
| `EmployeeRole` / `dcIEEmployeeRole` | `Trim(varRole)` |
| `EmployeeLevel` / `dcIEEmployeeLevel` | `If(IsBlank(varLevel), Blank(), LookUp(Choices(TrendMarcherAward.EmployeeLevel), Value = varLevel))` |
| `NominationStatus` / `dcIENominationStatus` | `{Value: "Draft"}` |
| `DeclarationAccepted` / `dcIEDeclarationAccepted` | `false` |
| `SubmittedOn` / `dcIESubmittedOn` | `Blank()` |
| `NominatedEmployee` / `dcIENominatedEmployee` | `If(IsBlank(varEmployee.Claims), Blank(), varEmployee)` |
| `Q1PromptSnapshot` / `dcIEQ1PromptSnapshot` | `LookUp(colAnswers, Slot = 1, Prompt)` |
| `Q1RequiredSnapshot` / `dcIEQ1RequiredSnapshot` | `LookUp(colAnswers, Slot = 1, Required)` |
| `Q1Response` / `dcIEQ1Response` | `If(1 <= varQuestionCount, txtIEQ1.Text, "")` |
| `Q2PromptSnapshot` / `dcIEQ2PromptSnapshot` | `LookUp(colAnswers, Slot = 2, Prompt)` |
| `Q2RequiredSnapshot` / `dcIEQ2RequiredSnapshot` | `LookUp(colAnswers, Slot = 2, Required)` |
| `Q2Response` / `dcIEQ2Response` | `If(2 <= varQuestionCount, txtIEQ2.Text, "")` |
| `Q3PromptSnapshot` / `dcIEQ3PromptSnapshot` | `LookUp(colAnswers, Slot = 3, Prompt)` |
| `Q3RequiredSnapshot` / `dcIEQ3RequiredSnapshot` | `LookUp(colAnswers, Slot = 3, Required)` |
| `Q3Response` / `dcIEQ3Response` | `If(3 <= varQuestionCount, txtIEQ3.Text, "")` |
| `Q4PromptSnapshot` / `dcIEQ4PromptSnapshot` | `LookUp(colAnswers, Slot = 4, Prompt)` |
| `Q4RequiredSnapshot` / `dcIEQ4RequiredSnapshot` | `LookUp(colAnswers, Slot = 4, Required)` |
| `Q4Response` / `dcIEQ4Response` | `If(4 <= varQuestionCount, txtIEQ4.Text, "")` |
| `Q5PromptSnapshot` / `dcIEQ5PromptSnapshot` | `LookUp(colAnswers, Slot = 5, Prompt)` |
| `Q5RequiredSnapshot` / `dcIEQ5RequiredSnapshot` | `LookUp(colAnswers, Slot = 5, Required)` |
| `Q5Response` / `dcIEQ5Response` | `If(5 <= varQuestionCount, txtIEQ5.Text, "")` |
| `Q6PromptSnapshot` / `dcIEQ6PromptSnapshot` | `LookUp(colAnswers, Slot = 6, Prompt)` |
| `Q6RequiredSnapshot` / `dcIEQ6RequiredSnapshot` | `LookUp(colAnswers, Slot = 6, Required)` |
| `Q6Response` / `dcIEQ6Response` | `If(6 <= varQuestionCount, txtIEQ6.Text, "")` |
| Native Attachments / `dcIEAttachments` | `attIE.Attachments` |

All cards except Q1–Q6 Response and Attachments: Visible = `false`, Height = `0`, Required = `false`. Set form-card DisplayMode to `Parent.DisplayMode`. Set each child editor DisplayMode to its card's DisplayMode, and disable it while varIsBusy. Hidden metadata's Update properties still participate in SubmitForm.

Keep native attachment Items = `Parent.Default` when directly inside its data card, and retain the generated attachment DataField (often `"{Attachments}"`). Do not type a guessed DataField. Preserve the other generated attachment properties, including MaxAttachments/MaxAttachmentSize, until an approved policy is chosen. Appending files does not save them until SubmitForm completes.

#### btnIESaveDraft.OnSelect

```powerfx
If(!varIsBusy && !varReadOnly && varCategoryComplete,
    ClearCollect(colCapturedAnswers, Table(
    {Slot: 1, Prompt: LookUp(colAnswers, Slot = 1, Prompt), Required: LookUp(colAnswers, Slot = 1, Required), Response: txtIEQ1.Text},
    {Slot: 2, Prompt: LookUp(colAnswers, Slot = 2, Prompt), Required: LookUp(colAnswers, Slot = 2, Required), Response: txtIEQ2.Text},
    {Slot: 3, Prompt: LookUp(colAnswers, Slot = 3, Prompt), Required: LookUp(colAnswers, Slot = 3, Required), Response: txtIEQ3.Text},
    {Slot: 4, Prompt: LookUp(colAnswers, Slot = 4, Prompt), Required: LookUp(colAnswers, Slot = 4, Required), Response: txtIEQ4.Text},
    {Slot: 5, Prompt: LookUp(colAnswers, Slot = 5, Prompt), Required: LookUp(colAnswers, Slot = 5, Required), Response: txtIEQ5.Text},
    {Slot: 6, Prompt: LookUp(colAnswers, Slot = 6, Prompt), Required: LookUp(colAnswers, Slot = 6, Required), Response: txtIEQ6.Text}
));
ClearCollect(colAnswers, colCapturedAnswers);
    If(CountIf(colAnswers, Len(Response) > varMaxResponseLength) > 0,
        Notify("A response exceeds the configured limit.", NotificationType.Warning),
        Set(varIsBusy, true);
Set(varPreflightOK, true);
If(!IsBlank(varNominationId),
    IfError(
        Refresh(TrendMarcherAward);
        Set(varLatestIE, LookUp(TrendMarcherAward, ID = varNominationId));
        If(IsBlank(varLatestIE.ID) ||
           varLatestIE.NominationStatus.Value <> "Draft" ||
           varLatestIE.Modified <> varLoadedModified,
            Set(varPreflightOK, false);
            Notify("This item changed or is no longer an editable draft. Keep a copy of your changes, then reopen it from My nominations.", NotificationType.Error)
        );
        true,
        Set(varPreflightOK, false);
        Notify("Could not check the saved draft. Your changes have been retained; try again when connected.", NotificationType.Error);
        false
    )
);
If(varPreflightOK,
    Set(varSaveIntent, "Draft");
    SubmitForm(frmTrendMarcherAward),
    Set(varIsBusy, false)
)
    )
)
```

#### btnIEReview.OnSelect

Set DisplayMode to `If(varIsBusy || varReadOnly, DisplayMode.Disabled, DisplayMode.Edit)`.

```powerfx
ClearCollect(colCapturedAnswers, Table(
    {Slot: 1, Prompt: LookUp(colAnswers, Slot = 1, Prompt), Required: LookUp(colAnswers, Slot = 1, Required), Response: txtIEQ1.Text},
    {Slot: 2, Prompt: LookUp(colAnswers, Slot = 2, Prompt), Required: LookUp(colAnswers, Slot = 2, Required), Response: txtIEQ2.Text},
    {Slot: 3, Prompt: LookUp(colAnswers, Slot = 3, Prompt), Required: LookUp(colAnswers, Slot = 3, Required), Response: txtIEQ3.Text},
    {Slot: 4, Prompt: LookUp(colAnswers, Slot = 4, Prompt), Required: LookUp(colAnswers, Slot = 4, Required), Response: txtIEQ4.Text},
    {Slot: 5, Prompt: LookUp(colAnswers, Slot = 5, Prompt), Required: LookUp(colAnswers, Slot = 5, Required), Response: txtIEQ5.Text},
    {Slot: 6, Prompt: LookUp(colAnswers, Slot = 6, Prompt), Required: LookUp(colAnswers, Slot = 6, Required), Response: txtIEQ6.Text}
));
ClearCollect(colAnswers, colCapturedAnswers);
Set(varDetailsComplete, DetailsValid);
Set(varResponsesComplete, ResponsesValid);
If(!DetailsValid,
    Notify("Complete nominee details, role and level before review.", NotificationType.Warning);
    Navigate(scrNomineeDetails, ScreenTransition.None),
    !ResponsesValid,
    Notify("Complete every required response before review.", NotificationType.Warning),
    Set(varDeclarationAccepted, false);
    ClearCollect(colReviewFiles, ForAll(attIE.Attachments As file, {FileName: file.Name}));
    Set(varCurrentStep, 4);
    Navigate(scrReview, ScreenTransition.None)
)
```

`colCapturedAnswers` prevents clearing the source table while reading its snapshots. Review reads current text controls directly, so it does not depend on OnChange timing. If Studio exposes the native file-name column as DisplayName instead of Name, use that actual column in the one FileName projection above; do not change attachment Items/Update or collect file bodies.

#### frmTrendMarcherAward.OnSuccess

```powerfx
Set(varRecordIE, frmTrendMarcherAward.LastSubmit);
Set(varNominationId, varRecordIE.ID);
Set(varLoadedModified, varRecordIE.Modified);
EditForm(frmTrendMarcherAward);
Set(varHasChanges, false);
If(varSaveIntent = "Submit",
    IfError(
        Set(varRecordIE,
            Patch(TrendMarcherAward, varRecordIE,
                {NominationStatus: {Value: "Submitted"},
                 DeclarationAccepted: true, SubmittedOn: Now()}
            )
        );
        Set(varLoadedModified, varRecordIE.Modified);
        Set(varSubmittedOn, varRecordIE.SubmittedOn);
        Set(varSubmissionComplete, true);
        Set(varReadOnly, true);
        Set(varIsBusy, false);
        ViewForm(frmTrendMarcherAward);
        Navigate(scrConfirmation, ScreenTransition.None);
        true,
        Set(varIsBusy, false);
        Set(varSubmissionComplete, false);
        Set(varSaveIntent, "Draft");
        Notify("Your draft save succeeded, but submission was not confirmed. Check My nominations before retrying. Your existing item ID is retained.", NotificationType.Error);
        false
    ),
    Set(varIsBusy, false);
    Notify("Draft saved. Reference: " & varCategory.CategoryCode & "-" & Text(varNominationId, "000000"), NotificationType.Success)
)
```

#### frmTrendMarcherAward.OnFailure

```powerfx
Set(varIsBusy, false);
Set(varSubmissionComplete, false);
Set(varHasChanges, true);
Notify("Save was not confirmed. Your inputs are retained. If the connection timed out, check My nominations before retrying because the server may have saved the item.", NotificationType.Error)
```

#### Back to details

Use a native button; Visible = `!varReadOnly`; DisplayMode disabled while varIsBusy. Its OnSelect:

```powerfx
ClearCollect(colCapturedAnswers, Table(
    {Slot: 1, Prompt: LookUp(colAnswers, Slot = 1, Prompt), Required: LookUp(colAnswers, Slot = 1, Required), Response: txtIEQ1.Text},
    {Slot: 2, Prompt: LookUp(colAnswers, Slot = 2, Prompt), Required: LookUp(colAnswers, Slot = 2, Required), Response: txtIEQ2.Text},
    {Slot: 3, Prompt: LookUp(colAnswers, Slot = 3, Prompt), Required: LookUp(colAnswers, Slot = 3, Required), Response: txtIEQ3.Text},
    {Slot: 4, Prompt: LookUp(colAnswers, Slot = 4, Prompt), Required: LookUp(colAnswers, Slot = 4, Required), Response: txtIEQ4.Text},
    {Slot: 5, Prompt: LookUp(colAnswers, Slot = 5, Prompt), Required: LookUp(colAnswers, Slot = 5, Required), Response: txtIEQ5.Text},
    {Slot: 6, Prompt: LookUp(colAnswers, Slot = 6, Prompt), Required: LookUp(colAnswers, Slot = 6, Required), Response: txtIEQ6.Text}
));
ClearCollect(colAnswers, colCapturedAnswers);
Set(varDeclarationAccepted, false);
Set(varCurrentStep, 1);
Navigate(scrNomineeDetails, ScreenTransition.None)
```

#### My nominations gallery galMineIE

Visible = `varBrowseCode = "IND_EXCELLENCE"`. Items:

```powerfx
SortByColumns(
    Filter(TrendMarcherAward,
        NominatorEmail = varUserEmail,
        (varBrowseStatus = "All" || NominationStatus.Value = varBrowseStatus),
        (varBrowseId = 0 || ID = varBrowseId)
    ),
    "Modified", SortOrder.Descending
)
```

Use `ThisItem.ID`, `ThisItem.Modified`, `ThisItem.NominationStatus.Value`, and `ThisItem.NominatedEmployee.DisplayName` in native labels. Reference Text = `"IND_EXCELLENCE-" & Text(ThisItem.ID, "000000")`. An Open button inside this gallery uses the following OnSelect; it queries the clicked ID again before opening. Inactive/retired categories can still open historical records.

```powerfx
If(!varIsBusy,
    Set(varIsBusy, true);
    Set(varOpenOK, true);
    IfError(
        Refresh(TrendMarcherAward);
        Set(varRecordIE, LookUp(TrendMarcherAward, ID = ThisItem.ID && NominatorEmail = varUserEmail));
        Refresh(AwardCategories);
        Set(varCategory, LookUp(AwardCategories, ID = varRecordIE.Category.Id));
        true,
        Set(varOpenOK, false);
        false
    );
    If(!varOpenOK || IsBlank(varRecordIE.ID) || varCategory.CategoryCode <> "IND_EXCELLENCE" ||
       IsBlank(varRecordIE.QuestionSetVersion) || varRecordIE.QuestionSetVersion < 1 ||
       IsBlank(varRecordIE.QuestionCount) || varRecordIE.QuestionCount < 3 || varRecordIE.QuestionCount > 6 ||
       varRecordIE.QuestionCount <> RoundDown(varRecordIE.QuestionCount,0) ||
       IsBlank(varRecordIE.Q1PromptSnapshot) || IsBlank(varRecordIE.Q2PromptSnapshot) || IsBlank(varRecordIE.Q3PromptSnapshot) ||
       (varRecordIE.QuestionCount>=4 && IsBlank(varRecordIE.Q4PromptSnapshot)) ||
       (varRecordIE.QuestionCount>=5 && IsBlank(varRecordIE.Q5PromptSnapshot)) ||
       (varRecordIE.QuestionCount>=6 && IsBlank(varRecordIE.Q6PromptSnapshot)) ||
       !(varRecordIE.NominationStatus.Value in ["Draft", "Submitted"]),
        Set(varIsBusy, false);
        Notify("Unable to open this nomination. Check access and the saved category/question metadata.", NotificationType.Error),
        Set(varAwardType, "Individual");
        Set(varNominationId, varRecordIE.ID);
        Set(varLoadedModified, varRecordIE.Modified);
        Set(varQuestionVersion, varRecordIE.QuestionSetVersion);
        Set(varQuestionCount, varRecordIE.QuestionCount);
        Set(varRole, Coalesce(varRecordIE.EmployeeRole, ""));
        Set(varLevel, Coalesce(varRecordIE.EmployeeLevel.Value, ""));
        Set(varNominator, varRecordIE.NominatedBy);
        Set(varEmployee, Coalesce(varRecordIE.NominatedEmployee, varEmptyPerson));
        Set(varPrimaryContact, varEmptyPerson);
        Set(varTeamName, "");
        Clear(colTeamMembers);
        ClearCollect(colAnswers, Table(
    {Slot: 1, Prompt: Coalesce(varRecordIE.Q1PromptSnapshot, ""), Required: Coalesce(varRecordIE.Q1RequiredSnapshot, false), Response: Coalesce(varRecordIE.Q1Response, "")},
    {Slot: 2, Prompt: Coalesce(varRecordIE.Q2PromptSnapshot, ""), Required: Coalesce(varRecordIE.Q2RequiredSnapshot, false), Response: Coalesce(varRecordIE.Q2Response, "")},
    {Slot: 3, Prompt: Coalesce(varRecordIE.Q3PromptSnapshot, ""), Required: Coalesce(varRecordIE.Q3RequiredSnapshot, false), Response: Coalesce(varRecordIE.Q3Response, "")},
    {Slot: 4, Prompt: Coalesce(varRecordIE.Q4PromptSnapshot, ""), Required: Coalesce(varRecordIE.Q4RequiredSnapshot, false), Response: Coalesce(varRecordIE.Q4Response, "")},
    {Slot: 5, Prompt: Coalesce(varRecordIE.Q5PromptSnapshot, ""), Required: Coalesce(varRecordIE.Q5RequiredSnapshot, false), Response: Coalesce(varRecordIE.Q5Response, "")},
    {Slot: 6, Prompt: Coalesce(varRecordIE.Q6PromptSnapshot, ""), Required: Coalesce(varRecordIE.Q6RequiredSnapshot, false), Response: Coalesce(varRecordIE.Q6Response, "")}
));
        Set(varReadOnly, varRecordIE.NominationStatus.Value = "Submitted");
        Set(varSubmissionComplete, varReadOnly);
        Set(varSubmittedOn, varRecordIE.SubmittedOn);
        Set(varCategoryComplete, true);
        Set(varDetailsComplete, DetailsValid);
        Set(varResponsesComplete, ResponsesValid);
        Set(varDeclarationAccepted, false);
        Set(varHasChanges, false);
        Set(varSaveIntent, "Draft");
        ResetForm(frmTrendMarcherAward);
        If(varReadOnly, ViewForm(frmTrendMarcherAward), EditForm(frmTrendMarcherAward));
        Set(varIsBusy, false);
        Navigate(scrTrendMarcherAward, ScreenTransition.None)
    )
)
```

Submitted items reuse this same typed form in View mode, including native file download. Form entry actions are hidden. This is the read-only screen implementation; a separate duplicate scrViewNomination is unnecessary.

#### Check this category before continuing

Save an incomplete draft, retain its ID, attach a small synthetic file, save again, reopen it, complete required answers, review unsaved changes, and submit. Confirm one item, correct snapshots, declaration and SubmittedOn. Reopen read-only. Test failed save/retry and concurrent modification. Use the full acceptance checklist; no runtime results are claimed here.

#### Question control properties

Insert a manual container inside each response card. Keep these exact unique names. Set label Font to Segoe UI, heading Color to Theme.Heading, body/counter Color to Theme.Muted. All labels wrap. Use the common input styling from the layout guide.

##### Slot 1

| Control / property | Formula or value |
|---|---|
| `dcIEQ1Response.Visible` | `1 <= varQuestionCount` |
| `dcIEQ1Response.X` / Y | `0` / `0` |
| `dcIEQ1Response.Width` | `Parent.Width` |
| `dcIEQ1Response.Height` | `If(Self.Visible, cntIEQ1.Y + cntIEQ1.Height + If(IsBlank(Self.Error), 0, errIEQ1.Height + 8) + 18, 0)` |
| `cntIEQ1` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntIEQ1.Height` | `lblIEQ1Counter.Y + lblIEQ1Counter.Height + 14` |
| `lblIEQ1Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblIEQ1Heading.Text` | `With({p:LookUp(colAnswers,Slot=1,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 1")) & If(LookUp(colAnswers,Slot=1,Required)," *","")` |
| `lblIEQ1Prompt` | X `22`; Y `lblIEQ1Heading.Y+lblIEQ1Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblIEQ1Prompt.Text` | `With({p:LookUp(colAnswers,Slot=1,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtIEQ1` | X `22`; Y `lblIEQ1Prompt.Y+lblIEQ1Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtIEQ1.Default` | `LookUp(colAnswers,Slot=1,Response)` |
| `txtIEQ1.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtIEQ1.DelayOutput` | `false` |
| `txtIEQ1.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcIEQ1Response.DisplayMode)` |
| `txtIEQ1.AccessibleLabel` | `LookUp(colAnswers,Slot=1,Prompt) & If(LookUp(colAnswers,Slot=1,Required),". Required", ". Optional")` |
| `lblIEQ1Counter` | X `22`; Y `txtIEQ1.Y+txtIEQ1.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblIEQ1Counter.Text` | `Text(Len(txtIEQ1.Text)) & " / " & Text(varMaxResponseLength)` |

`txtIEQ1.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=1), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 2

| Control / property | Formula or value |
|---|---|
| `dcIEQ2Response.Visible` | `2 <= varQuestionCount` |
| `dcIEQ2Response.X` / Y | `0` / `1` |
| `dcIEQ2Response.Width` | `Parent.Width` |
| `dcIEQ2Response.Height` | `If(Self.Visible, cntIEQ2.Y + cntIEQ2.Height + If(IsBlank(Self.Error), 0, errIEQ2.Height + 8) + 18, 0)` |
| `cntIEQ2` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntIEQ2.Height` | `lblIEQ2Counter.Y + lblIEQ2Counter.Height + 14` |
| `lblIEQ2Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblIEQ2Heading.Text` | `With({p:LookUp(colAnswers,Slot=2,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 2")) & If(LookUp(colAnswers,Slot=2,Required)," *","")` |
| `lblIEQ2Prompt` | X `22`; Y `lblIEQ2Heading.Y+lblIEQ2Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblIEQ2Prompt.Text` | `With({p:LookUp(colAnswers,Slot=2,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtIEQ2` | X `22`; Y `lblIEQ2Prompt.Y+lblIEQ2Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtIEQ2.Default` | `LookUp(colAnswers,Slot=2,Response)` |
| `txtIEQ2.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtIEQ2.DelayOutput` | `false` |
| `txtIEQ2.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcIEQ2Response.DisplayMode)` |
| `txtIEQ2.AccessibleLabel` | `LookUp(colAnswers,Slot=2,Prompt) & If(LookUp(colAnswers,Slot=2,Required),". Required", ". Optional")` |
| `lblIEQ2Counter` | X `22`; Y `txtIEQ2.Y+txtIEQ2.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblIEQ2Counter.Text` | `Text(Len(txtIEQ2.Text)) & " / " & Text(varMaxResponseLength)` |

`txtIEQ2.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=2), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 3

| Control / property | Formula or value |
|---|---|
| `dcIEQ3Response.Visible` | `3 <= varQuestionCount` |
| `dcIEQ3Response.X` / Y | `0` / `2` |
| `dcIEQ3Response.Width` | `Parent.Width` |
| `dcIEQ3Response.Height` | `If(Self.Visible, cntIEQ3.Y + cntIEQ3.Height + If(IsBlank(Self.Error), 0, errIEQ3.Height + 8) + 18, 0)` |
| `cntIEQ3` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntIEQ3.Height` | `lblIEQ3Counter.Y + lblIEQ3Counter.Height + 14` |
| `lblIEQ3Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblIEQ3Heading.Text` | `With({p:LookUp(colAnswers,Slot=3,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 3")) & If(LookUp(colAnswers,Slot=3,Required)," *","")` |
| `lblIEQ3Prompt` | X `22`; Y `lblIEQ3Heading.Y+lblIEQ3Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblIEQ3Prompt.Text` | `With({p:LookUp(colAnswers,Slot=3,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtIEQ3` | X `22`; Y `lblIEQ3Prompt.Y+lblIEQ3Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtIEQ3.Default` | `LookUp(colAnswers,Slot=3,Response)` |
| `txtIEQ3.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtIEQ3.DelayOutput` | `false` |
| `txtIEQ3.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcIEQ3Response.DisplayMode)` |
| `txtIEQ3.AccessibleLabel` | `LookUp(colAnswers,Slot=3,Prompt) & If(LookUp(colAnswers,Slot=3,Required),". Required", ". Optional")` |
| `lblIEQ3Counter` | X `22`; Y `txtIEQ3.Y+txtIEQ3.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblIEQ3Counter.Text` | `Text(Len(txtIEQ3.Text)) & " / " & Text(varMaxResponseLength)` |

`txtIEQ3.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=3), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 4

| Control / property | Formula or value |
|---|---|
| `dcIEQ4Response.Visible` | `4 <= varQuestionCount` |
| `dcIEQ4Response.X` / Y | `0` / `3` |
| `dcIEQ4Response.Width` | `Parent.Width` |
| `dcIEQ4Response.Height` | `If(Self.Visible, cntIEQ4.Y + cntIEQ4.Height + If(IsBlank(Self.Error), 0, errIEQ4.Height + 8) + 18, 0)` |
| `cntIEQ4` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntIEQ4.Height` | `lblIEQ4Counter.Y + lblIEQ4Counter.Height + 14` |
| `lblIEQ4Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblIEQ4Heading.Text` | `With({p:LookUp(colAnswers,Slot=4,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 4")) & If(LookUp(colAnswers,Slot=4,Required)," *","")` |
| `lblIEQ4Prompt` | X `22`; Y `lblIEQ4Heading.Y+lblIEQ4Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblIEQ4Prompt.Text` | `With({p:LookUp(colAnswers,Slot=4,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtIEQ4` | X `22`; Y `lblIEQ4Prompt.Y+lblIEQ4Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtIEQ4.Default` | `LookUp(colAnswers,Slot=4,Response)` |
| `txtIEQ4.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtIEQ4.DelayOutput` | `false` |
| `txtIEQ4.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcIEQ4Response.DisplayMode)` |
| `txtIEQ4.AccessibleLabel` | `LookUp(colAnswers,Slot=4,Prompt) & If(LookUp(colAnswers,Slot=4,Required),". Required", ". Optional")` |
| `lblIEQ4Counter` | X `22`; Y `txtIEQ4.Y+txtIEQ4.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblIEQ4Counter.Text` | `Text(Len(txtIEQ4.Text)) & " / " & Text(varMaxResponseLength)` |

`txtIEQ4.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=4), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 5

| Control / property | Formula or value |
|---|---|
| `dcIEQ5Response.Visible` | `5 <= varQuestionCount` |
| `dcIEQ5Response.X` / Y | `0` / `4` |
| `dcIEQ5Response.Width` | `Parent.Width` |
| `dcIEQ5Response.Height` | `If(Self.Visible, cntIEQ5.Y + cntIEQ5.Height + If(IsBlank(Self.Error), 0, errIEQ5.Height + 8) + 18, 0)` |
| `cntIEQ5` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntIEQ5.Height` | `lblIEQ5Counter.Y + lblIEQ5Counter.Height + 14` |
| `lblIEQ5Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblIEQ5Heading.Text` | `With({p:LookUp(colAnswers,Slot=5,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 5")) & If(LookUp(colAnswers,Slot=5,Required)," *","")` |
| `lblIEQ5Prompt` | X `22`; Y `lblIEQ5Heading.Y+lblIEQ5Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblIEQ5Prompt.Text` | `With({p:LookUp(colAnswers,Slot=5,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtIEQ5` | X `22`; Y `lblIEQ5Prompt.Y+lblIEQ5Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtIEQ5.Default` | `LookUp(colAnswers,Slot=5,Response)` |
| `txtIEQ5.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtIEQ5.DelayOutput` | `false` |
| `txtIEQ5.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcIEQ5Response.DisplayMode)` |
| `txtIEQ5.AccessibleLabel` | `LookUp(colAnswers,Slot=5,Prompt) & If(LookUp(colAnswers,Slot=5,Required),". Required", ". Optional")` |
| `lblIEQ5Counter` | X `22`; Y `txtIEQ5.Y+txtIEQ5.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblIEQ5Counter.Text` | `Text(Len(txtIEQ5.Text)) & " / " & Text(varMaxResponseLength)` |

`txtIEQ5.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=5), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 6

| Control / property | Formula or value |
|---|---|
| `dcIEQ6Response.Visible` | `6 <= varQuestionCount` |
| `dcIEQ6Response.X` / Y | `0` / `5` |
| `dcIEQ6Response.Width` | `Parent.Width` |
| `dcIEQ6Response.Height` | `If(Self.Visible, cntIEQ6.Y + cntIEQ6.Height + If(IsBlank(Self.Error), 0, errIEQ6.Height + 8) + 18, 0)` |
| `cntIEQ6` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntIEQ6.Height` | `lblIEQ6Counter.Y + lblIEQ6Counter.Height + 14` |
| `lblIEQ6Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblIEQ6Heading.Text` | `With({p:LookUp(colAnswers,Slot=6,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 6")) & If(LookUp(colAnswers,Slot=6,Required)," *","")` |
| `lblIEQ6Prompt` | X `22`; Y `lblIEQ6Heading.Y+lblIEQ6Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblIEQ6Prompt.Text` | `With({p:LookUp(colAnswers,Slot=6,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtIEQ6` | X `22`; Y `lblIEQ6Prompt.Y+lblIEQ6Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtIEQ6.Default` | `LookUp(colAnswers,Slot=6,Response)` |
| `txtIEQ6.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtIEQ6.DelayOutput` | `false` |
| `txtIEQ6.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcIEQ6Response.DisplayMode)` |
| `txtIEQ6.AccessibleLabel` | `LookUp(colAnswers,Slot=6,Prompt) & If(LookUp(colAnswers,Slot=6,Required),". Required", ". Optional")` |
| `lblIEQ6Counter` | X `22`; Y `txtIEQ6.Y+txtIEQ6.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblIEQ6Counter.Text` | `Text(Len(txtIEQ6.Text)) & " / " & Text(varMaxResponseLength)` |

`txtIEQ6.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=6), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

#### TrendMarcherAward: form dimensions and missing-property completion

Set `frmTrendMarcherAward.Width` from its actual parent as described above. Set `frmTrendMarcherAward.Height` to:

```powerfx
dcIEQ1Response.Height +
dcIEQ2Response.Height +
dcIEQ3Response.Height +
dcIEQ4Response.Height +
dcIEQ5Response.Height +
dcIEQ6Response.Height +
dcIEAttachments.Height +
24
```


Rename each generated response error label as listed. Keep it directly inside the response card, not inside the question container. Set AutoHeight=true, Height=10, X=22, Width=Parent.Width-44, Text=Parent.Error, Visible=!IsBlank(Parent.Error), Color=Theme.Error, Size=9, Live=Live.Assertive. Hide only the redundant generated response field-heading labels.

| Error label | Parent card | Y |
|---|---|---|
| `errIEQ1` | `dcIEQ1Response` | `cntIEQ1.Y + cntIEQ1.Height + 4` |
| `errIEQ2` | `dcIEQ2Response` | `cntIEQ2.Y + cntIEQ2.Height + 4` |
| `errIEQ3` | `dcIEQ3Response` | `cntIEQ3.Y + cntIEQ3.Height + 4` |
| `errIEQ4` | `dcIEQ4Response` | `cntIEQ4.Y + cntIEQ4.Height + 4` |
| `errIEQ5` | `dcIEQ5Response` | `cntIEQ5.Y + cntIEQ5.Height + 4` |
| `errIEQ6` | `dcIEQ6Response` | `cntIEQ6.Y + cntIEQ6.Height + 4` |

Set these input properties in addition to the question tables:

| Input | BorderColor | Tooltip |
|---|---|---|
| `txtIEQ1` | `If(IsBlank(dcIEQ1Response.Error), dcIEQ1Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 1, Prompt)` |
| `txtIEQ2` | `If(IsBlank(dcIEQ2Response.Error), dcIEQ2Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 2, Prompt)` |
| `txtIEQ3` | `If(IsBlank(dcIEQ3Response.Error), dcIEQ3Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 3, Prompt)` |
| `txtIEQ4` | `If(IsBlank(dcIEQ4Response.Error), dcIEQ4Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 4, Prompt)` |
| `txtIEQ5` | `If(IsBlank(dcIEQ5Response.Error), dcIEQ5Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 5, Prompt)` |
| `txtIEQ6` | `If(IsBlank(dcIEQ6Response.Error), dcIEQ6Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 6, Prompt)` |

For all six inputs use Font=`Font.'Segoe UI'`, Size=`9.75`, Color=`Theme.Body`, Fill=`Theme.Surface`, BorderThickness=`1`, FocusedBorderColor=`Theme.Primary`, FocusedBorderThickness=`2`, PaddingLeft/Right=`11`, PaddingTop/Bottom=`9`, all corner radii=`4`, and TabIndex=`0`. Set heading Font=`Font.'Segoe UI'` and Color=`Theme.Heading`; prompt/counter Font=`Font.'Segoe UI'` and Color=`Theme.Muted`. Prompt AutoHeight=`true`, base Height=`34`, Size=`9.75`; counter AutoHeight=`false`, Height=`18`. All labels Wrap=`true`.


#### TrendMarcherAward: native attachments and form-level errors

Keep `attIE` directly inside `dcIEAttachments`. Retain the generated DataField, Items, limits, and native binding settings. Do not replace an attachment control with a collection-backed file picker.

| Property | Value |
|---|---|
| `dcIEAttachments.Visible` | `true` |
| `dcIEAttachments.Width` | `Parent.Width` |
| `dcIEAttachments.Height` | `270` |
| `dcIEAttachments.Required` | `false` |
| `dcIEAttachments.Update` | `attIE.Attachments` |
| `attIE.Items` | `Parent.Default` |
| `attIE.DisplayMode` | `If(varIsBusy, DisplayMode.Disabled, Parent.DisplayMode)` |

For `attIE.OnAddFile`, `attIE.OnRemoveFile`, and `attIE.OnUndoRemoveFile`, use the same action:

```powerfx
Set(varHasChanges, true);
Set(varDeclarationAccepted, false);
Set(varResponsesComplete, false)
```

The attachment layout can retain the generated label/editor coordinates. If restyling it, keep the generated error label visible and reserve space for its complete text. Do not suppress native validation messages.

Add a classic label `lblSaveErrorIE` immediately after the form in the scrolling content container. Use the same X and Width as the form, Y=`frmTrendMarcherAward.Y + frmTrendMarcherAward.Height + 8`, AutoHeight=`true`, Text=`frmTrendMarcherAward.Error`, Visible=`!IsBlank(frmTrendMarcherAward.Error)`, Color=`Theme.Error`, and Live=`Live.Assertive`. Place the action row after this label when visible so errors from hidden metadata cards are not lost. Do not reset inputs on failure.


#### TrendMarcherAward: action controls

| Control | Text | Visible | DisplayMode |
|---|---|---|---|
| `btnIESaveDraft` | `"Save draft"` | `!varReadOnly` | `If(varIsBusy \|\| varReadOnly \|\| !varCategoryComplete, DisplayMode.Disabled, DisplayMode.Edit)` |
| `btnIEReview` | `"Review"` | `!varReadOnly` | `If(varIsBusy \|\| varReadOnly, DisplayMode.Disabled, DisplayMode.Edit)` |
| `btnIEBack` | `"Back to details"` | `!varReadOnly` | `If(varIsBusy, DisplayMode.Disabled, DisplayMode.Edit)` |

Use the complete OnSelect blocks above for these controls. Do not append a status Patch directly after SubmitForm. A read-only Back to My nominations button can use `Navigate(scrMyNominations, ScreenTransition.None)` with Visible=`varReadOnly`.


<a id="form-tc"></a>

### BestInnovatorTeam: TEAM_COLLAB / TC

Use the common form-building and scrolling rules above. These formulas target classic controls and English Power Fx separators. They are not yet Studio-compiled or runtime-tested.

#### Controls to create

Screen `scrBestInnovatorTeam`; Edit form `frmBestInnovatorTeam`; saved-record variable `varRecordTC`; latest-record variable `varLatestTC`. Create six response text inputs `txtTCQ1` … `txtTCQ6` in the corresponding response cards, and keep native attachment input `attTC` inside `dcTCAttachments`.

Form DataSource = `BestInnovatorTeam`; Item = `varRecordTC`; DefaultMode = `FormMode.New`; NumberOfColumns = `1`; SnapToColumns = `false`. See layout guide for X/Y/Width/Height. Use the form's generated cards and unlock them. Preserve generated DataField strings exactly; if the connector shows a display name with spaces, use Studio's actual generated identifier. Required = `false` on entry cards to allow incomplete drafts; submission requirements are enforced separately. Do not remove metadata cards just because they are hidden.

Response cards are `dcTCQ1Response` … `dcTCQ6Response`. The other Q cards hold snapshots/flags and are hidden. Do not rename a response card to its text input name.

#### scrBestInnovatorTeam.OnVisible

```powerfx
Set(varCurrentStep, 3)
```

Do not call NewForm/ResetForm here: returning from review must preserve inputs and queued files.

#### All card Update properties

| SharePoint DataField / card | Update formula |
|---|---|
| `Title` / `dcTCTitle` | `Left(varCategory.CategoryCode & " - " & If(varAwardType = "Individual", Coalesce(varEmployee.DisplayName, "Draft"), If(IsBlank(Trim(varTeamName)), "Draft", varTeamName)),255)` |
| `Category` / `dcTCCategory` | `{Id: varCategory.ID, Value: varCategory.Title}` |
| `QuestionSetVersion` / `dcTCQuestionSetVersion` | `varQuestionVersion` |
| `QuestionCount` / `dcTCQuestionCount` | `varQuestionCount` |
| `NominatedBy` / `dcTCNominatedBy` | `varNominator` |
| `NominatorEmail` / `dcTCNominatorEmail` | `varUserEmail` |
| `EmployeeRole` / `dcTCEmployeeRole` | `Trim(varRole)` |
| `EmployeeLevel` / `dcTCEmployeeLevel` | `If(IsBlank(varLevel), Blank(), LookUp(Choices(BestInnovatorTeam.EmployeeLevel), Value = varLevel))` |
| `NominationStatus` / `dcTCNominationStatus` | `{Value: "Draft"}` |
| `DeclarationAccepted` / `dcTCDeclarationAccepted` | `false` |
| `SubmittedOn` / `dcTCSubmittedOn` | `Blank()` |
| `TeamName` / `dcTCTeamName` | `Trim(varTeamName)` |
| `TeamPrimaryContact` / `dcTCTeamPrimaryContact` | `If(IsBlank(varPrimaryContact.Claims), Blank(), varPrimaryContact)` |
| `TeamMembers` / `dcTCTeamMembers` | `colTeamMembers` |
| `Q1PromptSnapshot` / `dcTCQ1PromptSnapshot` | `LookUp(colAnswers, Slot = 1, Prompt)` |
| `Q1RequiredSnapshot` / `dcTCQ1RequiredSnapshot` | `LookUp(colAnswers, Slot = 1, Required)` |
| `Q1Response` / `dcTCQ1Response` | `If(1 <= varQuestionCount, txtTCQ1.Text, "")` |
| `Q2PromptSnapshot` / `dcTCQ2PromptSnapshot` | `LookUp(colAnswers, Slot = 2, Prompt)` |
| `Q2RequiredSnapshot` / `dcTCQ2RequiredSnapshot` | `LookUp(colAnswers, Slot = 2, Required)` |
| `Q2Response` / `dcTCQ2Response` | `If(2 <= varQuestionCount, txtTCQ2.Text, "")` |
| `Q3PromptSnapshot` / `dcTCQ3PromptSnapshot` | `LookUp(colAnswers, Slot = 3, Prompt)` |
| `Q3RequiredSnapshot` / `dcTCQ3RequiredSnapshot` | `LookUp(colAnswers, Slot = 3, Required)` |
| `Q3Response` / `dcTCQ3Response` | `If(3 <= varQuestionCount, txtTCQ3.Text, "")` |
| `Q4PromptSnapshot` / `dcTCQ4PromptSnapshot` | `LookUp(colAnswers, Slot = 4, Prompt)` |
| `Q4RequiredSnapshot` / `dcTCQ4RequiredSnapshot` | `LookUp(colAnswers, Slot = 4, Required)` |
| `Q4Response` / `dcTCQ4Response` | `If(4 <= varQuestionCount, txtTCQ4.Text, "")` |
| `Q5PromptSnapshot` / `dcTCQ5PromptSnapshot` | `LookUp(colAnswers, Slot = 5, Prompt)` |
| `Q5RequiredSnapshot` / `dcTCQ5RequiredSnapshot` | `LookUp(colAnswers, Slot = 5, Required)` |
| `Q5Response` / `dcTCQ5Response` | `If(5 <= varQuestionCount, txtTCQ5.Text, "")` |
| `Q6PromptSnapshot` / `dcTCQ6PromptSnapshot` | `LookUp(colAnswers, Slot = 6, Prompt)` |
| `Q6RequiredSnapshot` / `dcTCQ6RequiredSnapshot` | `LookUp(colAnswers, Slot = 6, Required)` |
| `Q6Response` / `dcTCQ6Response` | `If(6 <= varQuestionCount, txtTCQ6.Text, "")` |
| Native Attachments / `dcTCAttachments` | `attTC.Attachments` |

All cards except Q1–Q6 Response and Attachments: Visible = `false`, Height = `0`, Required = `false`. Set form-card DisplayMode to `Parent.DisplayMode`. Set each child editor DisplayMode to its card's DisplayMode, and disable it while varIsBusy. Hidden metadata's Update properties still participate in SubmitForm.

Keep native attachment Items = `Parent.Default` when directly inside its data card, and retain the generated attachment DataField (often `"{Attachments}"`). Do not type a guessed DataField. Preserve the other generated attachment properties, including MaxAttachments/MaxAttachmentSize, until an approved policy is chosen. Appending files does not save them until SubmitForm completes.

#### btnTCSaveDraft.OnSelect

```powerfx
If(!varIsBusy && !varReadOnly && varCategoryComplete,
    ClearCollect(colCapturedAnswers, Table(
    {Slot: 1, Prompt: LookUp(colAnswers, Slot = 1, Prompt), Required: LookUp(colAnswers, Slot = 1, Required), Response: txtTCQ1.Text},
    {Slot: 2, Prompt: LookUp(colAnswers, Slot = 2, Prompt), Required: LookUp(colAnswers, Slot = 2, Required), Response: txtTCQ2.Text},
    {Slot: 3, Prompt: LookUp(colAnswers, Slot = 3, Prompt), Required: LookUp(colAnswers, Slot = 3, Required), Response: txtTCQ3.Text},
    {Slot: 4, Prompt: LookUp(colAnswers, Slot = 4, Prompt), Required: LookUp(colAnswers, Slot = 4, Required), Response: txtTCQ4.Text},
    {Slot: 5, Prompt: LookUp(colAnswers, Slot = 5, Prompt), Required: LookUp(colAnswers, Slot = 5, Required), Response: txtTCQ5.Text},
    {Slot: 6, Prompt: LookUp(colAnswers, Slot = 6, Prompt), Required: LookUp(colAnswers, Slot = 6, Required), Response: txtTCQ6.Text}
));
ClearCollect(colAnswers, colCapturedAnswers);
    If(CountIf(colAnswers, Len(Response) > varMaxResponseLength) > 0,
        Notify("A response exceeds the configured limit.", NotificationType.Warning),
        Set(varIsBusy, true);
Set(varPreflightOK, true);
If(!IsBlank(varNominationId),
    IfError(
        Refresh(BestInnovatorTeam);
        Set(varLatestTC, LookUp(BestInnovatorTeam, ID = varNominationId));
        If(IsBlank(varLatestTC.ID) ||
           varLatestTC.NominationStatus.Value <> "Draft" ||
           varLatestTC.Modified <> varLoadedModified,
            Set(varPreflightOK, false);
            Notify("This item changed or is no longer an editable draft. Keep a copy of your changes, then reopen it from My nominations.", NotificationType.Error)
        );
        true,
        Set(varPreflightOK, false);
        Notify("Could not check the saved draft. Your changes have been retained; try again when connected.", NotificationType.Error);
        false
    )
);
If(varPreflightOK,
    Set(varSaveIntent, "Draft");
    SubmitForm(frmBestInnovatorTeam),
    Set(varIsBusy, false)
)
    )
)
```

#### btnTCReview.OnSelect

Set DisplayMode to `If(varIsBusy || varReadOnly, DisplayMode.Disabled, DisplayMode.Edit)`.

```powerfx
ClearCollect(colCapturedAnswers, Table(
    {Slot: 1, Prompt: LookUp(colAnswers, Slot = 1, Prompt), Required: LookUp(colAnswers, Slot = 1, Required), Response: txtTCQ1.Text},
    {Slot: 2, Prompt: LookUp(colAnswers, Slot = 2, Prompt), Required: LookUp(colAnswers, Slot = 2, Required), Response: txtTCQ2.Text},
    {Slot: 3, Prompt: LookUp(colAnswers, Slot = 3, Prompt), Required: LookUp(colAnswers, Slot = 3, Required), Response: txtTCQ3.Text},
    {Slot: 4, Prompt: LookUp(colAnswers, Slot = 4, Prompt), Required: LookUp(colAnswers, Slot = 4, Required), Response: txtTCQ4.Text},
    {Slot: 5, Prompt: LookUp(colAnswers, Slot = 5, Prompt), Required: LookUp(colAnswers, Slot = 5, Required), Response: txtTCQ5.Text},
    {Slot: 6, Prompt: LookUp(colAnswers, Slot = 6, Prompt), Required: LookUp(colAnswers, Slot = 6, Required), Response: txtTCQ6.Text}
));
ClearCollect(colAnswers, colCapturedAnswers);
Set(varDetailsComplete, DetailsValid);
Set(varResponsesComplete, ResponsesValid);
If(!DetailsValid,
    Notify("Complete nominee details, role and level before review.", NotificationType.Warning);
    Navigate(scrNomineeDetails, ScreenTransition.None),
    !ResponsesValid,
    Notify("Complete every required response before review.", NotificationType.Warning),
    Set(varDeclarationAccepted, false);
    ClearCollect(colReviewFiles, ForAll(attTC.Attachments As file, {FileName: file.Name}));
    Set(varCurrentStep, 4);
    Navigate(scrReview, ScreenTransition.None)
)
```

`colCapturedAnswers` prevents clearing the source table while reading its snapshots. Review reads current text controls directly, so it does not depend on OnChange timing. If Studio exposes the native file-name column as DisplayName instead of Name, use that actual column in the one FileName projection above; do not change attachment Items/Update or collect file bodies.

#### frmBestInnovatorTeam.OnSuccess

```powerfx
Set(varRecordTC, frmBestInnovatorTeam.LastSubmit);
Set(varNominationId, varRecordTC.ID);
Set(varLoadedModified, varRecordTC.Modified);
EditForm(frmBestInnovatorTeam);
Set(varHasChanges, false);
If(varSaveIntent = "Submit",
    IfError(
        Set(varRecordTC,
            Patch(BestInnovatorTeam, varRecordTC,
                {NominationStatus: {Value: "Submitted"},
                 DeclarationAccepted: true, SubmittedOn: Now()}
            )
        );
        Set(varLoadedModified, varRecordTC.Modified);
        Set(varSubmittedOn, varRecordTC.SubmittedOn);
        Set(varSubmissionComplete, true);
        Set(varReadOnly, true);
        Set(varIsBusy, false);
        ViewForm(frmBestInnovatorTeam);
        Navigate(scrConfirmation, ScreenTransition.None);
        true,
        Set(varIsBusy, false);
        Set(varSubmissionComplete, false);
        Set(varSaveIntent, "Draft");
        Notify("Your draft save succeeded, but submission was not confirmed. Check My nominations before retrying. Your existing item ID is retained.", NotificationType.Error);
        false
    ),
    Set(varIsBusy, false);
    Notify("Draft saved. Reference: " & varCategory.CategoryCode & "-" & Text(varNominationId, "000000"), NotificationType.Success)
)
```

#### frmBestInnovatorTeam.OnFailure

```powerfx
Set(varIsBusy, false);
Set(varSubmissionComplete, false);
Set(varHasChanges, true);
Notify("Save was not confirmed. Your inputs are retained. If the connection timed out, check My nominations before retrying because the server may have saved the item.", NotificationType.Error)
```

#### Back to details

Use a native button; Visible = `!varReadOnly`; DisplayMode disabled while varIsBusy. Its OnSelect:

```powerfx
ClearCollect(colCapturedAnswers, Table(
    {Slot: 1, Prompt: LookUp(colAnswers, Slot = 1, Prompt), Required: LookUp(colAnswers, Slot = 1, Required), Response: txtTCQ1.Text},
    {Slot: 2, Prompt: LookUp(colAnswers, Slot = 2, Prompt), Required: LookUp(colAnswers, Slot = 2, Required), Response: txtTCQ2.Text},
    {Slot: 3, Prompt: LookUp(colAnswers, Slot = 3, Prompt), Required: LookUp(colAnswers, Slot = 3, Required), Response: txtTCQ3.Text},
    {Slot: 4, Prompt: LookUp(colAnswers, Slot = 4, Prompt), Required: LookUp(colAnswers, Slot = 4, Required), Response: txtTCQ4.Text},
    {Slot: 5, Prompt: LookUp(colAnswers, Slot = 5, Prompt), Required: LookUp(colAnswers, Slot = 5, Required), Response: txtTCQ5.Text},
    {Slot: 6, Prompt: LookUp(colAnswers, Slot = 6, Prompt), Required: LookUp(colAnswers, Slot = 6, Required), Response: txtTCQ6.Text}
));
ClearCollect(colAnswers, colCapturedAnswers);
Set(varDeclarationAccepted, false);
Set(varCurrentStep, 1);
Navigate(scrNomineeDetails, ScreenTransition.None)
```

#### My nominations gallery galMineTC

Visible = `varBrowseCode = "TEAM_COLLAB"`. Items:

```powerfx
SortByColumns(
    Filter(BestInnovatorTeam,
        NominatorEmail = varUserEmail,
        (varBrowseStatus = "All" || NominationStatus.Value = varBrowseStatus),
        (varBrowseId = 0 || ID = varBrowseId)
    ),
    "Modified", SortOrder.Descending
)
```

Use `ThisItem.ID`, `ThisItem.Modified`, `ThisItem.NominationStatus.Value`, and `ThisItem.TeamName` in native labels. Reference Text = `"TEAM_COLLAB-" & Text(ThisItem.ID, "000000")`. An Open button inside this gallery uses the following OnSelect; it queries the clicked ID again before opening. Inactive/retired categories can still open historical records.

```powerfx
If(!varIsBusy,
    Set(varIsBusy, true);
    Set(varOpenOK, true);
    IfError(
        Refresh(BestInnovatorTeam);
        Set(varRecordTC, LookUp(BestInnovatorTeam, ID = ThisItem.ID && NominatorEmail = varUserEmail));
        Refresh(AwardCategories);
        Set(varCategory, LookUp(AwardCategories, ID = varRecordTC.Category.Id));
        true,
        Set(varOpenOK, false);
        false
    );
    If(!varOpenOK || IsBlank(varRecordTC.ID) || varCategory.CategoryCode <> "TEAM_COLLAB" ||
       IsBlank(varRecordTC.QuestionSetVersion) || varRecordTC.QuestionSetVersion < 1 ||
       IsBlank(varRecordTC.QuestionCount) || varRecordTC.QuestionCount < 3 || varRecordTC.QuestionCount > 6 ||
       varRecordTC.QuestionCount <> RoundDown(varRecordTC.QuestionCount,0) ||
       IsBlank(varRecordTC.Q1PromptSnapshot) || IsBlank(varRecordTC.Q2PromptSnapshot) || IsBlank(varRecordTC.Q3PromptSnapshot) ||
       (varRecordTC.QuestionCount>=4 && IsBlank(varRecordTC.Q4PromptSnapshot)) ||
       (varRecordTC.QuestionCount>=5 && IsBlank(varRecordTC.Q5PromptSnapshot)) ||
       (varRecordTC.QuestionCount>=6 && IsBlank(varRecordTC.Q6PromptSnapshot)) ||
       !(varRecordTC.NominationStatus.Value in ["Draft", "Submitted"]),
        Set(varIsBusy, false);
        Notify("Unable to open this nomination. Check access and the saved category/question metadata.", NotificationType.Error),
        Set(varAwardType, "Team");
        Set(varNominationId, varRecordTC.ID);
        Set(varLoadedModified, varRecordTC.Modified);
        Set(varQuestionVersion, varRecordTC.QuestionSetVersion);
        Set(varQuestionCount, varRecordTC.QuestionCount);
        Set(varRole, Coalesce(varRecordTC.EmployeeRole, ""));
        Set(varLevel, Coalesce(varRecordTC.EmployeeLevel.Value, ""));
        Set(varNominator, varRecordTC.NominatedBy);
        Set(varTeamName, Coalesce(varRecordTC.TeamName, ""));
        Set(varPrimaryContact, Coalesce(varRecordTC.TeamPrimaryContact, varEmptyPerson));
        Set(varEmployee, varEmptyPerson);
        ClearCollect(colTeamMembers, varRecordTC.TeamMembers);
        ClearCollect(colAnswers, Table(
    {Slot: 1, Prompt: Coalesce(varRecordTC.Q1PromptSnapshot, ""), Required: Coalesce(varRecordTC.Q1RequiredSnapshot, false), Response: Coalesce(varRecordTC.Q1Response, "")},
    {Slot: 2, Prompt: Coalesce(varRecordTC.Q2PromptSnapshot, ""), Required: Coalesce(varRecordTC.Q2RequiredSnapshot, false), Response: Coalesce(varRecordTC.Q2Response, "")},
    {Slot: 3, Prompt: Coalesce(varRecordTC.Q3PromptSnapshot, ""), Required: Coalesce(varRecordTC.Q3RequiredSnapshot, false), Response: Coalesce(varRecordTC.Q3Response, "")},
    {Slot: 4, Prompt: Coalesce(varRecordTC.Q4PromptSnapshot, ""), Required: Coalesce(varRecordTC.Q4RequiredSnapshot, false), Response: Coalesce(varRecordTC.Q4Response, "")},
    {Slot: 5, Prompt: Coalesce(varRecordTC.Q5PromptSnapshot, ""), Required: Coalesce(varRecordTC.Q5RequiredSnapshot, false), Response: Coalesce(varRecordTC.Q5Response, "")},
    {Slot: 6, Prompt: Coalesce(varRecordTC.Q6PromptSnapshot, ""), Required: Coalesce(varRecordTC.Q6RequiredSnapshot, false), Response: Coalesce(varRecordTC.Q6Response, "")}
));
        Set(varReadOnly, varRecordTC.NominationStatus.Value = "Submitted");
        Set(varSubmissionComplete, varReadOnly);
        Set(varSubmittedOn, varRecordTC.SubmittedOn);
        Set(varCategoryComplete, true);
        Set(varDetailsComplete, DetailsValid);
        Set(varResponsesComplete, ResponsesValid);
        Set(varDeclarationAccepted, false);
        Set(varHasChanges, false);
        Set(varSaveIntent, "Draft");
        ResetForm(frmBestInnovatorTeam);
        If(varReadOnly, ViewForm(frmBestInnovatorTeam), EditForm(frmBestInnovatorTeam));
        Set(varIsBusy, false);
        Navigate(scrBestInnovatorTeam, ScreenTransition.None)
    )
)
```

Submitted items reuse this same typed form in View mode, including native file download. Form entry actions are hidden. This is the read-only screen implementation; a separate duplicate scrViewNomination is unnecessary.

#### Check this category before continuing

Save an incomplete draft, retain its ID, attach a small synthetic file, save again, reopen it, complete required answers, review unsaved changes, and submit. Confirm one item, correct snapshots, declaration and SubmittedOn. Reopen read-only. Test failed save/retry and concurrent modification. Use the full acceptance checklist; no runtime results are claimed here.

#### Question control properties

Insert a manual container inside each response card. Keep these exact unique names. Set label Font to Segoe UI, heading Color to Theme.Heading, body/counter Color to Theme.Muted. All labels wrap. Use the common input styling from the layout guide.

##### Slot 1

| Control / property | Formula or value |
|---|---|
| `dcTCQ1Response.Visible` | `1 <= varQuestionCount` |
| `dcTCQ1Response.X` / Y | `0` / `0` |
| `dcTCQ1Response.Width` | `Parent.Width` |
| `dcTCQ1Response.Height` | `If(Self.Visible, cntTCQ1.Y + cntTCQ1.Height + If(IsBlank(Self.Error), 0, errTCQ1.Height + 8) + 18, 0)` |
| `cntTCQ1` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntTCQ1.Height` | `lblTCQ1Counter.Y + lblTCQ1Counter.Height + 14` |
| `lblTCQ1Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblTCQ1Heading.Text` | `With({p:LookUp(colAnswers,Slot=1,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 1")) & If(LookUp(colAnswers,Slot=1,Required)," *","")` |
| `lblTCQ1Prompt` | X `22`; Y `lblTCQ1Heading.Y+lblTCQ1Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblTCQ1Prompt.Text` | `With({p:LookUp(colAnswers,Slot=1,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtTCQ1` | X `22`; Y `lblTCQ1Prompt.Y+lblTCQ1Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtTCQ1.Default` | `LookUp(colAnswers,Slot=1,Response)` |
| `txtTCQ1.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtTCQ1.DelayOutput` | `false` |
| `txtTCQ1.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcTCQ1Response.DisplayMode)` |
| `txtTCQ1.AccessibleLabel` | `LookUp(colAnswers,Slot=1,Prompt) & If(LookUp(colAnswers,Slot=1,Required),". Required", ". Optional")` |
| `lblTCQ1Counter` | X `22`; Y `txtTCQ1.Y+txtTCQ1.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblTCQ1Counter.Text` | `Text(Len(txtTCQ1.Text)) & " / " & Text(varMaxResponseLength)` |

`txtTCQ1.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=1), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 2

| Control / property | Formula or value |
|---|---|
| `dcTCQ2Response.Visible` | `2 <= varQuestionCount` |
| `dcTCQ2Response.X` / Y | `0` / `1` |
| `dcTCQ2Response.Width` | `Parent.Width` |
| `dcTCQ2Response.Height` | `If(Self.Visible, cntTCQ2.Y + cntTCQ2.Height + If(IsBlank(Self.Error), 0, errTCQ2.Height + 8) + 18, 0)` |
| `cntTCQ2` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntTCQ2.Height` | `lblTCQ2Counter.Y + lblTCQ2Counter.Height + 14` |
| `lblTCQ2Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblTCQ2Heading.Text` | `With({p:LookUp(colAnswers,Slot=2,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 2")) & If(LookUp(colAnswers,Slot=2,Required)," *","")` |
| `lblTCQ2Prompt` | X `22`; Y `lblTCQ2Heading.Y+lblTCQ2Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblTCQ2Prompt.Text` | `With({p:LookUp(colAnswers,Slot=2,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtTCQ2` | X `22`; Y `lblTCQ2Prompt.Y+lblTCQ2Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtTCQ2.Default` | `LookUp(colAnswers,Slot=2,Response)` |
| `txtTCQ2.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtTCQ2.DelayOutput` | `false` |
| `txtTCQ2.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcTCQ2Response.DisplayMode)` |
| `txtTCQ2.AccessibleLabel` | `LookUp(colAnswers,Slot=2,Prompt) & If(LookUp(colAnswers,Slot=2,Required),". Required", ". Optional")` |
| `lblTCQ2Counter` | X `22`; Y `txtTCQ2.Y+txtTCQ2.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblTCQ2Counter.Text` | `Text(Len(txtTCQ2.Text)) & " / " & Text(varMaxResponseLength)` |

`txtTCQ2.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=2), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 3

| Control / property | Formula or value |
|---|---|
| `dcTCQ3Response.Visible` | `3 <= varQuestionCount` |
| `dcTCQ3Response.X` / Y | `0` / `2` |
| `dcTCQ3Response.Width` | `Parent.Width` |
| `dcTCQ3Response.Height` | `If(Self.Visible, cntTCQ3.Y + cntTCQ3.Height + If(IsBlank(Self.Error), 0, errTCQ3.Height + 8) + 18, 0)` |
| `cntTCQ3` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntTCQ3.Height` | `lblTCQ3Counter.Y + lblTCQ3Counter.Height + 14` |
| `lblTCQ3Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblTCQ3Heading.Text` | `With({p:LookUp(colAnswers,Slot=3,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 3")) & If(LookUp(colAnswers,Slot=3,Required)," *","")` |
| `lblTCQ3Prompt` | X `22`; Y `lblTCQ3Heading.Y+lblTCQ3Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblTCQ3Prompt.Text` | `With({p:LookUp(colAnswers,Slot=3,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtTCQ3` | X `22`; Y `lblTCQ3Prompt.Y+lblTCQ3Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtTCQ3.Default` | `LookUp(colAnswers,Slot=3,Response)` |
| `txtTCQ3.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtTCQ3.DelayOutput` | `false` |
| `txtTCQ3.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcTCQ3Response.DisplayMode)` |
| `txtTCQ3.AccessibleLabel` | `LookUp(colAnswers,Slot=3,Prompt) & If(LookUp(colAnswers,Slot=3,Required),". Required", ". Optional")` |
| `lblTCQ3Counter` | X `22`; Y `txtTCQ3.Y+txtTCQ3.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblTCQ3Counter.Text` | `Text(Len(txtTCQ3.Text)) & " / " & Text(varMaxResponseLength)` |

`txtTCQ3.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=3), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 4

| Control / property | Formula or value |
|---|---|
| `dcTCQ4Response.Visible` | `4 <= varQuestionCount` |
| `dcTCQ4Response.X` / Y | `0` / `3` |
| `dcTCQ4Response.Width` | `Parent.Width` |
| `dcTCQ4Response.Height` | `If(Self.Visible, cntTCQ4.Y + cntTCQ4.Height + If(IsBlank(Self.Error), 0, errTCQ4.Height + 8) + 18, 0)` |
| `cntTCQ4` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntTCQ4.Height` | `lblTCQ4Counter.Y + lblTCQ4Counter.Height + 14` |
| `lblTCQ4Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblTCQ4Heading.Text` | `With({p:LookUp(colAnswers,Slot=4,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 4")) & If(LookUp(colAnswers,Slot=4,Required)," *","")` |
| `lblTCQ4Prompt` | X `22`; Y `lblTCQ4Heading.Y+lblTCQ4Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblTCQ4Prompt.Text` | `With({p:LookUp(colAnswers,Slot=4,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtTCQ4` | X `22`; Y `lblTCQ4Prompt.Y+lblTCQ4Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtTCQ4.Default` | `LookUp(colAnswers,Slot=4,Response)` |
| `txtTCQ4.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtTCQ4.DelayOutput` | `false` |
| `txtTCQ4.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcTCQ4Response.DisplayMode)` |
| `txtTCQ4.AccessibleLabel` | `LookUp(colAnswers,Slot=4,Prompt) & If(LookUp(colAnswers,Slot=4,Required),". Required", ". Optional")` |
| `lblTCQ4Counter` | X `22`; Y `txtTCQ4.Y+txtTCQ4.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblTCQ4Counter.Text` | `Text(Len(txtTCQ4.Text)) & " / " & Text(varMaxResponseLength)` |

`txtTCQ4.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=4), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 5

| Control / property | Formula or value |
|---|---|
| `dcTCQ5Response.Visible` | `5 <= varQuestionCount` |
| `dcTCQ5Response.X` / Y | `0` / `4` |
| `dcTCQ5Response.Width` | `Parent.Width` |
| `dcTCQ5Response.Height` | `If(Self.Visible, cntTCQ5.Y + cntTCQ5.Height + If(IsBlank(Self.Error), 0, errTCQ5.Height + 8) + 18, 0)` |
| `cntTCQ5` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntTCQ5.Height` | `lblTCQ5Counter.Y + lblTCQ5Counter.Height + 14` |
| `lblTCQ5Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblTCQ5Heading.Text` | `With({p:LookUp(colAnswers,Slot=5,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 5")) & If(LookUp(colAnswers,Slot=5,Required)," *","")` |
| `lblTCQ5Prompt` | X `22`; Y `lblTCQ5Heading.Y+lblTCQ5Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblTCQ5Prompt.Text` | `With({p:LookUp(colAnswers,Slot=5,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtTCQ5` | X `22`; Y `lblTCQ5Prompt.Y+lblTCQ5Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtTCQ5.Default` | `LookUp(colAnswers,Slot=5,Response)` |
| `txtTCQ5.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtTCQ5.DelayOutput` | `false` |
| `txtTCQ5.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcTCQ5Response.DisplayMode)` |
| `txtTCQ5.AccessibleLabel` | `LookUp(colAnswers,Slot=5,Prompt) & If(LookUp(colAnswers,Slot=5,Required),". Required", ". Optional")` |
| `lblTCQ5Counter` | X `22`; Y `txtTCQ5.Y+txtTCQ5.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblTCQ5Counter.Text` | `Text(Len(txtTCQ5.Text)) & " / " & Text(varMaxResponseLength)` |

`txtTCQ5.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=5), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 6

| Control / property | Formula or value |
|---|---|
| `dcTCQ6Response.Visible` | `6 <= varQuestionCount` |
| `dcTCQ6Response.X` / Y | `0` / `5` |
| `dcTCQ6Response.Width` | `Parent.Width` |
| `dcTCQ6Response.Height` | `If(Self.Visible, cntTCQ6.Y + cntTCQ6.Height + If(IsBlank(Self.Error), 0, errTCQ6.Height + 8) + 18, 0)` |
| `cntTCQ6` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntTCQ6.Height` | `lblTCQ6Counter.Y + lblTCQ6Counter.Height + 14` |
| `lblTCQ6Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblTCQ6Heading.Text` | `With({p:LookUp(colAnswers,Slot=6,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 6")) & If(LookUp(colAnswers,Slot=6,Required)," *","")` |
| `lblTCQ6Prompt` | X `22`; Y `lblTCQ6Heading.Y+lblTCQ6Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblTCQ6Prompt.Text` | `With({p:LookUp(colAnswers,Slot=6,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtTCQ6` | X `22`; Y `lblTCQ6Prompt.Y+lblTCQ6Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtTCQ6.Default` | `LookUp(colAnswers,Slot=6,Response)` |
| `txtTCQ6.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtTCQ6.DelayOutput` | `false` |
| `txtTCQ6.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcTCQ6Response.DisplayMode)` |
| `txtTCQ6.AccessibleLabel` | `LookUp(colAnswers,Slot=6,Prompt) & If(LookUp(colAnswers,Slot=6,Required),". Required", ". Optional")` |
| `lblTCQ6Counter` | X `22`; Y `txtTCQ6.Y+txtTCQ6.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblTCQ6Counter.Text` | `Text(Len(txtTCQ6.Text)) & " / " & Text(varMaxResponseLength)` |

`txtTCQ6.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=6), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

#### BestInnovatorTeam: form dimensions and missing-property completion

Set `frmBestInnovatorTeam.Width` from its actual parent as described above. Set `frmBestInnovatorTeam.Height` to:

```powerfx
dcTCQ1Response.Height +
dcTCQ2Response.Height +
dcTCQ3Response.Height +
dcTCQ4Response.Height +
dcTCQ5Response.Height +
dcTCQ6Response.Height +
dcTCAttachments.Height +
24
```


Rename each generated response error label as listed. Keep it directly inside the response card, not inside the question container. Set AutoHeight=true, Height=10, X=22, Width=Parent.Width-44, Text=Parent.Error, Visible=!IsBlank(Parent.Error), Color=Theme.Error, Size=9, Live=Live.Assertive. Hide only the redundant generated response field-heading labels.

| Error label | Parent card | Y |
|---|---|---|
| `errTCQ1` | `dcTCQ1Response` | `cntTCQ1.Y + cntTCQ1.Height + 4` |
| `errTCQ2` | `dcTCQ2Response` | `cntTCQ2.Y + cntTCQ2.Height + 4` |
| `errTCQ3` | `dcTCQ3Response` | `cntTCQ3.Y + cntTCQ3.Height + 4` |
| `errTCQ4` | `dcTCQ4Response` | `cntTCQ4.Y + cntTCQ4.Height + 4` |
| `errTCQ5` | `dcTCQ5Response` | `cntTCQ5.Y + cntTCQ5.Height + 4` |
| `errTCQ6` | `dcTCQ6Response` | `cntTCQ6.Y + cntTCQ6.Height + 4` |

Set these input properties in addition to the question tables:

| Input | BorderColor | Tooltip |
|---|---|---|
| `txtTCQ1` | `If(IsBlank(dcTCQ1Response.Error), dcTCQ1Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 1, Prompt)` |
| `txtTCQ2` | `If(IsBlank(dcTCQ2Response.Error), dcTCQ2Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 2, Prompt)` |
| `txtTCQ3` | `If(IsBlank(dcTCQ3Response.Error), dcTCQ3Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 3, Prompt)` |
| `txtTCQ4` | `If(IsBlank(dcTCQ4Response.Error), dcTCQ4Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 4, Prompt)` |
| `txtTCQ5` | `If(IsBlank(dcTCQ5Response.Error), dcTCQ5Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 5, Prompt)` |
| `txtTCQ6` | `If(IsBlank(dcTCQ6Response.Error), dcTCQ6Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 6, Prompt)` |

For all six inputs use Font=`Font.'Segoe UI'`, Size=`9.75`, Color=`Theme.Body`, Fill=`Theme.Surface`, BorderThickness=`1`, FocusedBorderColor=`Theme.Primary`, FocusedBorderThickness=`2`, PaddingLeft/Right=`11`, PaddingTop/Bottom=`9`, all corner radii=`4`, and TabIndex=`0`. Set heading Font=`Font.'Segoe UI'` and Color=`Theme.Heading`; prompt/counter Font=`Font.'Segoe UI'` and Color=`Theme.Muted`. Prompt AutoHeight=`true`, base Height=`34`, Size=`9.75`; counter AutoHeight=`false`, Height=`18`. All labels Wrap=`true`.


#### BestInnovatorTeam: native attachments and form-level errors

Keep `attTC` directly inside `dcTCAttachments`. Retain the generated DataField, Items, limits, and native binding settings. Do not replace an attachment control with a collection-backed file picker.

| Property | Value |
|---|---|
| `dcTCAttachments.Visible` | `true` |
| `dcTCAttachments.Width` | `Parent.Width` |
| `dcTCAttachments.Height` | `270` |
| `dcTCAttachments.Required` | `false` |
| `dcTCAttachments.Update` | `attTC.Attachments` |
| `attTC.Items` | `Parent.Default` |
| `attTC.DisplayMode` | `If(varIsBusy, DisplayMode.Disabled, Parent.DisplayMode)` |

For `attTC.OnAddFile`, `attTC.OnRemoveFile`, and `attTC.OnUndoRemoveFile`, use the same action:

```powerfx
Set(varHasChanges, true);
Set(varDeclarationAccepted, false);
Set(varResponsesComplete, false)
```

The attachment layout can retain the generated label/editor coordinates. If restyling it, keep the generated error label visible and reserve space for its complete text. Do not suppress native validation messages.

Add a classic label `lblSaveErrorTC` immediately after the form in the scrolling content container. Use the same X and Width as the form, Y=`frmBestInnovatorTeam.Y + frmBestInnovatorTeam.Height + 8`, AutoHeight=`true`, Text=`frmBestInnovatorTeam.Error`, Visible=`!IsBlank(frmBestInnovatorTeam.Error)`, Color=`Theme.Error`, and Live=`Live.Assertive`. Place the action row after this label when visible so errors from hidden metadata cards are not lost. Do not reset inputs on failure.


#### BestInnovatorTeam: action controls

| Control | Text | Visible | DisplayMode |
|---|---|---|---|
| `btnTCSaveDraft` | `"Save draft"` | `!varReadOnly` | `If(varIsBusy \|\| varReadOnly \|\| !varCategoryComplete, DisplayMode.Disabled, DisplayMode.Edit)` |
| `btnTCReview` | `"Review"` | `!varReadOnly` | `If(varIsBusy \|\| varReadOnly, DisplayMode.Disabled, DisplayMode.Edit)` |
| `btnTCBack` | `"Back to details"` | `!varReadOnly` | `If(varIsBusy, DisplayMode.Disabled, DisplayMode.Edit)` |

Use the complete OnSelect blocks above for these controls. Do not append a status Patch directly after SubmitForm. A read-only Back to My nominations button can use `Navigate(scrMyNominations, ScreenTransition.None)` with Visible=`varReadOnly`.


<a id="form-ti"></a>

### MDAwardTeam: TEAM_IMPACT / TI

Use the common form-building and scrolling rules above. These formulas target classic controls and English Power Fx separators. They are not yet Studio-compiled or runtime-tested.

#### Controls to create

Screen `scrMDAwardTeam`; Edit form `frmMDAwardTeam`; saved-record variable `varRecordTI`; latest-record variable `varLatestTI`. Create six response text inputs `txtTIQ1` … `txtTIQ6` in the corresponding response cards, and keep native attachment input `attTI` inside `dcTIAttachments`.

Form DataSource = `MDAwardTeam`; Item = `varRecordTI`; DefaultMode = `FormMode.New`; NumberOfColumns = `1`; SnapToColumns = `false`. See layout guide for X/Y/Width/Height. Use the form's generated cards and unlock them. Preserve generated DataField strings exactly; if the connector shows a display name with spaces, use Studio's actual generated identifier. Required = `false` on entry cards to allow incomplete drafts; submission requirements are enforced separately. Do not remove metadata cards just because they are hidden.

Response cards are `dcTIQ1Response` … `dcTIQ6Response`. The other Q cards hold snapshots/flags and are hidden. Do not rename a response card to its text input name.

#### scrMDAwardTeam.OnVisible

```powerfx
Set(varCurrentStep, 3)
```

Do not call NewForm/ResetForm here: returning from review must preserve inputs and queued files.

#### All card Update properties

| SharePoint DataField / card | Update formula |
|---|---|
| `Title` / `dcTITitle` | `Left(varCategory.CategoryCode & " - " & If(varAwardType = "Individual", Coalesce(varEmployee.DisplayName, "Draft"), If(IsBlank(Trim(varTeamName)), "Draft", varTeamName)),255)` |
| `Category` / `dcTICategory` | `{Id: varCategory.ID, Value: varCategory.Title}` |
| `QuestionSetVersion` / `dcTIQuestionSetVersion` | `varQuestionVersion` |
| `QuestionCount` / `dcTIQuestionCount` | `varQuestionCount` |
| `NominatedBy` / `dcTINominatedBy` | `varNominator` |
| `NominatorEmail` / `dcTINominatorEmail` | `varUserEmail` |
| `EmployeeRole` / `dcTIEmployeeRole` | `Trim(varRole)` |
| `EmployeeLevel` / `dcTIEmployeeLevel` | `If(IsBlank(varLevel), Blank(), LookUp(Choices(MDAwardTeam.EmployeeLevel), Value = varLevel))` |
| `NominationStatus` / `dcTINominationStatus` | `{Value: "Draft"}` |
| `DeclarationAccepted` / `dcTIDeclarationAccepted` | `false` |
| `SubmittedOn` / `dcTISubmittedOn` | `Blank()` |
| `TeamName` / `dcTITeamName` | `Trim(varTeamName)` |
| `TeamPrimaryContact` / `dcTITeamPrimaryContact` | `If(IsBlank(varPrimaryContact.Claims), Blank(), varPrimaryContact)` |
| `TeamMembers` / `dcTITeamMembers` | `colTeamMembers` |
| `Q1PromptSnapshot` / `dcTIQ1PromptSnapshot` | `LookUp(colAnswers, Slot = 1, Prompt)` |
| `Q1RequiredSnapshot` / `dcTIQ1RequiredSnapshot` | `LookUp(colAnswers, Slot = 1, Required)` |
| `Q1Response` / `dcTIQ1Response` | `If(1 <= varQuestionCount, txtTIQ1.Text, "")` |
| `Q2PromptSnapshot` / `dcTIQ2PromptSnapshot` | `LookUp(colAnswers, Slot = 2, Prompt)` |
| `Q2RequiredSnapshot` / `dcTIQ2RequiredSnapshot` | `LookUp(colAnswers, Slot = 2, Required)` |
| `Q2Response` / `dcTIQ2Response` | `If(2 <= varQuestionCount, txtTIQ2.Text, "")` |
| `Q3PromptSnapshot` / `dcTIQ3PromptSnapshot` | `LookUp(colAnswers, Slot = 3, Prompt)` |
| `Q3RequiredSnapshot` / `dcTIQ3RequiredSnapshot` | `LookUp(colAnswers, Slot = 3, Required)` |
| `Q3Response` / `dcTIQ3Response` | `If(3 <= varQuestionCount, txtTIQ3.Text, "")` |
| `Q4PromptSnapshot` / `dcTIQ4PromptSnapshot` | `LookUp(colAnswers, Slot = 4, Prompt)` |
| `Q4RequiredSnapshot` / `dcTIQ4RequiredSnapshot` | `LookUp(colAnswers, Slot = 4, Required)` |
| `Q4Response` / `dcTIQ4Response` | `If(4 <= varQuestionCount, txtTIQ4.Text, "")` |
| `Q5PromptSnapshot` / `dcTIQ5PromptSnapshot` | `LookUp(colAnswers, Slot = 5, Prompt)` |
| `Q5RequiredSnapshot` / `dcTIQ5RequiredSnapshot` | `LookUp(colAnswers, Slot = 5, Required)` |
| `Q5Response` / `dcTIQ5Response` | `If(5 <= varQuestionCount, txtTIQ5.Text, "")` |
| `Q6PromptSnapshot` / `dcTIQ6PromptSnapshot` | `LookUp(colAnswers, Slot = 6, Prompt)` |
| `Q6RequiredSnapshot` / `dcTIQ6RequiredSnapshot` | `LookUp(colAnswers, Slot = 6, Required)` |
| `Q6Response` / `dcTIQ6Response` | `If(6 <= varQuestionCount, txtTIQ6.Text, "")` |
| Native Attachments / `dcTIAttachments` | `attTI.Attachments` |

All cards except Q1–Q6 Response and Attachments: Visible = `false`, Height = `0`, Required = `false`. Set form-card DisplayMode to `Parent.DisplayMode`. Set each child editor DisplayMode to its card's DisplayMode, and disable it while varIsBusy. Hidden metadata's Update properties still participate in SubmitForm.

Keep native attachment Items = `Parent.Default` when directly inside its data card, and retain the generated attachment DataField (often `"{Attachments}"`). Do not type a guessed DataField. Preserve the other generated attachment properties, including MaxAttachments/MaxAttachmentSize, until an approved policy is chosen. Appending files does not save them until SubmitForm completes.

#### btnTISaveDraft.OnSelect

```powerfx
If(!varIsBusy && !varReadOnly && varCategoryComplete,
    ClearCollect(colCapturedAnswers, Table(
    {Slot: 1, Prompt: LookUp(colAnswers, Slot = 1, Prompt), Required: LookUp(colAnswers, Slot = 1, Required), Response: txtTIQ1.Text},
    {Slot: 2, Prompt: LookUp(colAnswers, Slot = 2, Prompt), Required: LookUp(colAnswers, Slot = 2, Required), Response: txtTIQ2.Text},
    {Slot: 3, Prompt: LookUp(colAnswers, Slot = 3, Prompt), Required: LookUp(colAnswers, Slot = 3, Required), Response: txtTIQ3.Text},
    {Slot: 4, Prompt: LookUp(colAnswers, Slot = 4, Prompt), Required: LookUp(colAnswers, Slot = 4, Required), Response: txtTIQ4.Text},
    {Slot: 5, Prompt: LookUp(colAnswers, Slot = 5, Prompt), Required: LookUp(colAnswers, Slot = 5, Required), Response: txtTIQ5.Text},
    {Slot: 6, Prompt: LookUp(colAnswers, Slot = 6, Prompt), Required: LookUp(colAnswers, Slot = 6, Required), Response: txtTIQ6.Text}
));
ClearCollect(colAnswers, colCapturedAnswers);
    If(CountIf(colAnswers, Len(Response) > varMaxResponseLength) > 0,
        Notify("A response exceeds the configured limit.", NotificationType.Warning),
        Set(varIsBusy, true);
Set(varPreflightOK, true);
If(!IsBlank(varNominationId),
    IfError(
        Refresh(MDAwardTeam);
        Set(varLatestTI, LookUp(MDAwardTeam, ID = varNominationId));
        If(IsBlank(varLatestTI.ID) ||
           varLatestTI.NominationStatus.Value <> "Draft" ||
           varLatestTI.Modified <> varLoadedModified,
            Set(varPreflightOK, false);
            Notify("This item changed or is no longer an editable draft. Keep a copy of your changes, then reopen it from My nominations.", NotificationType.Error)
        );
        true,
        Set(varPreflightOK, false);
        Notify("Could not check the saved draft. Your changes have been retained; try again when connected.", NotificationType.Error);
        false
    )
);
If(varPreflightOK,
    Set(varSaveIntent, "Draft");
    SubmitForm(frmMDAwardTeam),
    Set(varIsBusy, false)
)
    )
)
```

#### btnTIReview.OnSelect

Set DisplayMode to `If(varIsBusy || varReadOnly, DisplayMode.Disabled, DisplayMode.Edit)`.

```powerfx
ClearCollect(colCapturedAnswers, Table(
    {Slot: 1, Prompt: LookUp(colAnswers, Slot = 1, Prompt), Required: LookUp(colAnswers, Slot = 1, Required), Response: txtTIQ1.Text},
    {Slot: 2, Prompt: LookUp(colAnswers, Slot = 2, Prompt), Required: LookUp(colAnswers, Slot = 2, Required), Response: txtTIQ2.Text},
    {Slot: 3, Prompt: LookUp(colAnswers, Slot = 3, Prompt), Required: LookUp(colAnswers, Slot = 3, Required), Response: txtTIQ3.Text},
    {Slot: 4, Prompt: LookUp(colAnswers, Slot = 4, Prompt), Required: LookUp(colAnswers, Slot = 4, Required), Response: txtTIQ4.Text},
    {Slot: 5, Prompt: LookUp(colAnswers, Slot = 5, Prompt), Required: LookUp(colAnswers, Slot = 5, Required), Response: txtTIQ5.Text},
    {Slot: 6, Prompt: LookUp(colAnswers, Slot = 6, Prompt), Required: LookUp(colAnswers, Slot = 6, Required), Response: txtTIQ6.Text}
));
ClearCollect(colAnswers, colCapturedAnswers);
Set(varDetailsComplete, DetailsValid);
Set(varResponsesComplete, ResponsesValid);
If(!DetailsValid,
    Notify("Complete nominee details, role and level before review.", NotificationType.Warning);
    Navigate(scrNomineeDetails, ScreenTransition.None),
    !ResponsesValid,
    Notify("Complete every required response before review.", NotificationType.Warning),
    Set(varDeclarationAccepted, false);
    ClearCollect(colReviewFiles, ForAll(attTI.Attachments As file, {FileName: file.Name}));
    Set(varCurrentStep, 4);
    Navigate(scrReview, ScreenTransition.None)
)
```

`colCapturedAnswers` prevents clearing the source table while reading its snapshots. Review reads current text controls directly, so it does not depend on OnChange timing. If Studio exposes the native file-name column as DisplayName instead of Name, use that actual column in the one FileName projection above; do not change attachment Items/Update or collect file bodies.

#### frmMDAwardTeam.OnSuccess

```powerfx
Set(varRecordTI, frmMDAwardTeam.LastSubmit);
Set(varNominationId, varRecordTI.ID);
Set(varLoadedModified, varRecordTI.Modified);
EditForm(frmMDAwardTeam);
Set(varHasChanges, false);
If(varSaveIntent = "Submit",
    IfError(
        Set(varRecordTI,
            Patch(MDAwardTeam, varRecordTI,
                {NominationStatus: {Value: "Submitted"},
                 DeclarationAccepted: true, SubmittedOn: Now()}
            )
        );
        Set(varLoadedModified, varRecordTI.Modified);
        Set(varSubmittedOn, varRecordTI.SubmittedOn);
        Set(varSubmissionComplete, true);
        Set(varReadOnly, true);
        Set(varIsBusy, false);
        ViewForm(frmMDAwardTeam);
        Navigate(scrConfirmation, ScreenTransition.None);
        true,
        Set(varIsBusy, false);
        Set(varSubmissionComplete, false);
        Set(varSaveIntent, "Draft");
        Notify("Your draft save succeeded, but submission was not confirmed. Check My nominations before retrying. Your existing item ID is retained.", NotificationType.Error);
        false
    ),
    Set(varIsBusy, false);
    Notify("Draft saved. Reference: " & varCategory.CategoryCode & "-" & Text(varNominationId, "000000"), NotificationType.Success)
)
```

#### frmMDAwardTeam.OnFailure

```powerfx
Set(varIsBusy, false);
Set(varSubmissionComplete, false);
Set(varHasChanges, true);
Notify("Save was not confirmed. Your inputs are retained. If the connection timed out, check My nominations before retrying because the server may have saved the item.", NotificationType.Error)
```

#### Back to details

Use a native button; Visible = `!varReadOnly`; DisplayMode disabled while varIsBusy. Its OnSelect:

```powerfx
ClearCollect(colCapturedAnswers, Table(
    {Slot: 1, Prompt: LookUp(colAnswers, Slot = 1, Prompt), Required: LookUp(colAnswers, Slot = 1, Required), Response: txtTIQ1.Text},
    {Slot: 2, Prompt: LookUp(colAnswers, Slot = 2, Prompt), Required: LookUp(colAnswers, Slot = 2, Required), Response: txtTIQ2.Text},
    {Slot: 3, Prompt: LookUp(colAnswers, Slot = 3, Prompt), Required: LookUp(colAnswers, Slot = 3, Required), Response: txtTIQ3.Text},
    {Slot: 4, Prompt: LookUp(colAnswers, Slot = 4, Prompt), Required: LookUp(colAnswers, Slot = 4, Required), Response: txtTIQ4.Text},
    {Slot: 5, Prompt: LookUp(colAnswers, Slot = 5, Prompt), Required: LookUp(colAnswers, Slot = 5, Required), Response: txtTIQ5.Text},
    {Slot: 6, Prompt: LookUp(colAnswers, Slot = 6, Prompt), Required: LookUp(colAnswers, Slot = 6, Required), Response: txtTIQ6.Text}
));
ClearCollect(colAnswers, colCapturedAnswers);
Set(varDeclarationAccepted, false);
Set(varCurrentStep, 1);
Navigate(scrNomineeDetails, ScreenTransition.None)
```

#### My nominations gallery galMineTI

Visible = `varBrowseCode = "TEAM_IMPACT"`. Items:

```powerfx
SortByColumns(
    Filter(MDAwardTeam,
        NominatorEmail = varUserEmail,
        (varBrowseStatus = "All" || NominationStatus.Value = varBrowseStatus),
        (varBrowseId = 0 || ID = varBrowseId)
    ),
    "Modified", SortOrder.Descending
)
```

Use `ThisItem.ID`, `ThisItem.Modified`, `ThisItem.NominationStatus.Value`, and `ThisItem.TeamName` in native labels. Reference Text = `"TEAM_IMPACT-" & Text(ThisItem.ID, "000000")`. An Open button inside this gallery uses the following OnSelect; it queries the clicked ID again before opening. Inactive/retired categories can still open historical records.

```powerfx
If(!varIsBusy,
    Set(varIsBusy, true);
    Set(varOpenOK, true);
    IfError(
        Refresh(MDAwardTeam);
        Set(varRecordTI, LookUp(MDAwardTeam, ID = ThisItem.ID && NominatorEmail = varUserEmail));
        Refresh(AwardCategories);
        Set(varCategory, LookUp(AwardCategories, ID = varRecordTI.Category.Id));
        true,
        Set(varOpenOK, false);
        false
    );
    If(!varOpenOK || IsBlank(varRecordTI.ID) || varCategory.CategoryCode <> "TEAM_IMPACT" ||
       IsBlank(varRecordTI.QuestionSetVersion) || varRecordTI.QuestionSetVersion < 1 ||
       IsBlank(varRecordTI.QuestionCount) || varRecordTI.QuestionCount < 3 || varRecordTI.QuestionCount > 6 ||
       varRecordTI.QuestionCount <> RoundDown(varRecordTI.QuestionCount,0) ||
       IsBlank(varRecordTI.Q1PromptSnapshot) || IsBlank(varRecordTI.Q2PromptSnapshot) || IsBlank(varRecordTI.Q3PromptSnapshot) ||
       (varRecordTI.QuestionCount>=4 && IsBlank(varRecordTI.Q4PromptSnapshot)) ||
       (varRecordTI.QuestionCount>=5 && IsBlank(varRecordTI.Q5PromptSnapshot)) ||
       (varRecordTI.QuestionCount>=6 && IsBlank(varRecordTI.Q6PromptSnapshot)) ||
       !(varRecordTI.NominationStatus.Value in ["Draft", "Submitted"]),
        Set(varIsBusy, false);
        Notify("Unable to open this nomination. Check access and the saved category/question metadata.", NotificationType.Error),
        Set(varAwardType, "Team");
        Set(varNominationId, varRecordTI.ID);
        Set(varLoadedModified, varRecordTI.Modified);
        Set(varQuestionVersion, varRecordTI.QuestionSetVersion);
        Set(varQuestionCount, varRecordTI.QuestionCount);
        Set(varRole, Coalesce(varRecordTI.EmployeeRole, ""));
        Set(varLevel, Coalesce(varRecordTI.EmployeeLevel.Value, ""));
        Set(varNominator, varRecordTI.NominatedBy);
        Set(varTeamName, Coalesce(varRecordTI.TeamName, ""));
        Set(varPrimaryContact, Coalesce(varRecordTI.TeamPrimaryContact, varEmptyPerson));
        Set(varEmployee, varEmptyPerson);
        ClearCollect(colTeamMembers, varRecordTI.TeamMembers);
        ClearCollect(colAnswers, Table(
    {Slot: 1, Prompt: Coalesce(varRecordTI.Q1PromptSnapshot, ""), Required: Coalesce(varRecordTI.Q1RequiredSnapshot, false), Response: Coalesce(varRecordTI.Q1Response, "")},
    {Slot: 2, Prompt: Coalesce(varRecordTI.Q2PromptSnapshot, ""), Required: Coalesce(varRecordTI.Q2RequiredSnapshot, false), Response: Coalesce(varRecordTI.Q2Response, "")},
    {Slot: 3, Prompt: Coalesce(varRecordTI.Q3PromptSnapshot, ""), Required: Coalesce(varRecordTI.Q3RequiredSnapshot, false), Response: Coalesce(varRecordTI.Q3Response, "")},
    {Slot: 4, Prompt: Coalesce(varRecordTI.Q4PromptSnapshot, ""), Required: Coalesce(varRecordTI.Q4RequiredSnapshot, false), Response: Coalesce(varRecordTI.Q4Response, "")},
    {Slot: 5, Prompt: Coalesce(varRecordTI.Q5PromptSnapshot, ""), Required: Coalesce(varRecordTI.Q5RequiredSnapshot, false), Response: Coalesce(varRecordTI.Q5Response, "")},
    {Slot: 6, Prompt: Coalesce(varRecordTI.Q6PromptSnapshot, ""), Required: Coalesce(varRecordTI.Q6RequiredSnapshot, false), Response: Coalesce(varRecordTI.Q6Response, "")}
));
        Set(varReadOnly, varRecordTI.NominationStatus.Value = "Submitted");
        Set(varSubmissionComplete, varReadOnly);
        Set(varSubmittedOn, varRecordTI.SubmittedOn);
        Set(varCategoryComplete, true);
        Set(varDetailsComplete, DetailsValid);
        Set(varResponsesComplete, ResponsesValid);
        Set(varDeclarationAccepted, false);
        Set(varHasChanges, false);
        Set(varSaveIntent, "Draft");
        ResetForm(frmMDAwardTeam);
        If(varReadOnly, ViewForm(frmMDAwardTeam), EditForm(frmMDAwardTeam));
        Set(varIsBusy, false);
        Navigate(scrMDAwardTeam, ScreenTransition.None)
    )
)
```

Submitted items reuse this same typed form in View mode, including native file download. Form entry actions are hidden. This is the read-only screen implementation; a separate duplicate scrViewNomination is unnecessary.

#### Check this category before continuing

Save an incomplete draft, retain its ID, attach a small synthetic file, save again, reopen it, complete required answers, review unsaved changes, and submit. Confirm one item, correct snapshots, declaration and SubmittedOn. Reopen read-only. Test failed save/retry and concurrent modification. Use the full acceptance checklist; no runtime results are claimed here.

#### Question control properties

Insert a manual container inside each response card. Keep these exact unique names. Set label Font to Segoe UI, heading Color to Theme.Heading, body/counter Color to Theme.Muted. All labels wrap. Use the common input styling from the layout guide.

##### Slot 1

| Control / property | Formula or value |
|---|---|
| `dcTIQ1Response.Visible` | `1 <= varQuestionCount` |
| `dcTIQ1Response.X` / Y | `0` / `0` |
| `dcTIQ1Response.Width` | `Parent.Width` |
| `dcTIQ1Response.Height` | `If(Self.Visible, cntTIQ1.Y + cntTIQ1.Height + If(IsBlank(Self.Error), 0, errTIQ1.Height + 8) + 18, 0)` |
| `cntTIQ1` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntTIQ1.Height` | `lblTIQ1Counter.Y + lblTIQ1Counter.Height + 14` |
| `lblTIQ1Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblTIQ1Heading.Text` | `With({p:LookUp(colAnswers,Slot=1,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 1")) & If(LookUp(colAnswers,Slot=1,Required)," *","")` |
| `lblTIQ1Prompt` | X `22`; Y `lblTIQ1Heading.Y+lblTIQ1Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblTIQ1Prompt.Text` | `With({p:LookUp(colAnswers,Slot=1,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtTIQ1` | X `22`; Y `lblTIQ1Prompt.Y+lblTIQ1Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtTIQ1.Default` | `LookUp(colAnswers,Slot=1,Response)` |
| `txtTIQ1.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtTIQ1.DelayOutput` | `false` |
| `txtTIQ1.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcTIQ1Response.DisplayMode)` |
| `txtTIQ1.AccessibleLabel` | `LookUp(colAnswers,Slot=1,Prompt) & If(LookUp(colAnswers,Slot=1,Required),". Required", ". Optional")` |
| `lblTIQ1Counter` | X `22`; Y `txtTIQ1.Y+txtTIQ1.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblTIQ1Counter.Text` | `Text(Len(txtTIQ1.Text)) & " / " & Text(varMaxResponseLength)` |

`txtTIQ1.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=1), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 2

| Control / property | Formula or value |
|---|---|
| `dcTIQ2Response.Visible` | `2 <= varQuestionCount` |
| `dcTIQ2Response.X` / Y | `0` / `1` |
| `dcTIQ2Response.Width` | `Parent.Width` |
| `dcTIQ2Response.Height` | `If(Self.Visible, cntTIQ2.Y + cntTIQ2.Height + If(IsBlank(Self.Error), 0, errTIQ2.Height + 8) + 18, 0)` |
| `cntTIQ2` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntTIQ2.Height` | `lblTIQ2Counter.Y + lblTIQ2Counter.Height + 14` |
| `lblTIQ2Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblTIQ2Heading.Text` | `With({p:LookUp(colAnswers,Slot=2,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 2")) & If(LookUp(colAnswers,Slot=2,Required)," *","")` |
| `lblTIQ2Prompt` | X `22`; Y `lblTIQ2Heading.Y+lblTIQ2Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblTIQ2Prompt.Text` | `With({p:LookUp(colAnswers,Slot=2,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtTIQ2` | X `22`; Y `lblTIQ2Prompt.Y+lblTIQ2Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtTIQ2.Default` | `LookUp(colAnswers,Slot=2,Response)` |
| `txtTIQ2.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtTIQ2.DelayOutput` | `false` |
| `txtTIQ2.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcTIQ2Response.DisplayMode)` |
| `txtTIQ2.AccessibleLabel` | `LookUp(colAnswers,Slot=2,Prompt) & If(LookUp(colAnswers,Slot=2,Required),". Required", ". Optional")` |
| `lblTIQ2Counter` | X `22`; Y `txtTIQ2.Y+txtTIQ2.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblTIQ2Counter.Text` | `Text(Len(txtTIQ2.Text)) & " / " & Text(varMaxResponseLength)` |

`txtTIQ2.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=2), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 3

| Control / property | Formula or value |
|---|---|
| `dcTIQ3Response.Visible` | `3 <= varQuestionCount` |
| `dcTIQ3Response.X` / Y | `0` / `2` |
| `dcTIQ3Response.Width` | `Parent.Width` |
| `dcTIQ3Response.Height` | `If(Self.Visible, cntTIQ3.Y + cntTIQ3.Height + If(IsBlank(Self.Error), 0, errTIQ3.Height + 8) + 18, 0)` |
| `cntTIQ3` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntTIQ3.Height` | `lblTIQ3Counter.Y + lblTIQ3Counter.Height + 14` |
| `lblTIQ3Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblTIQ3Heading.Text` | `With({p:LookUp(colAnswers,Slot=3,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 3")) & If(LookUp(colAnswers,Slot=3,Required)," *","")` |
| `lblTIQ3Prompt` | X `22`; Y `lblTIQ3Heading.Y+lblTIQ3Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblTIQ3Prompt.Text` | `With({p:LookUp(colAnswers,Slot=3,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtTIQ3` | X `22`; Y `lblTIQ3Prompt.Y+lblTIQ3Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtTIQ3.Default` | `LookUp(colAnswers,Slot=3,Response)` |
| `txtTIQ3.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtTIQ3.DelayOutput` | `false` |
| `txtTIQ3.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcTIQ3Response.DisplayMode)` |
| `txtTIQ3.AccessibleLabel` | `LookUp(colAnswers,Slot=3,Prompt) & If(LookUp(colAnswers,Slot=3,Required),". Required", ". Optional")` |
| `lblTIQ3Counter` | X `22`; Y `txtTIQ3.Y+txtTIQ3.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblTIQ3Counter.Text` | `Text(Len(txtTIQ3.Text)) & " / " & Text(varMaxResponseLength)` |

`txtTIQ3.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=3), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 4

| Control / property | Formula or value |
|---|---|
| `dcTIQ4Response.Visible` | `4 <= varQuestionCount` |
| `dcTIQ4Response.X` / Y | `0` / `3` |
| `dcTIQ4Response.Width` | `Parent.Width` |
| `dcTIQ4Response.Height` | `If(Self.Visible, cntTIQ4.Y + cntTIQ4.Height + If(IsBlank(Self.Error), 0, errTIQ4.Height + 8) + 18, 0)` |
| `cntTIQ4` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntTIQ4.Height` | `lblTIQ4Counter.Y + lblTIQ4Counter.Height + 14` |
| `lblTIQ4Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblTIQ4Heading.Text` | `With({p:LookUp(colAnswers,Slot=4,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 4")) & If(LookUp(colAnswers,Slot=4,Required)," *","")` |
| `lblTIQ4Prompt` | X `22`; Y `lblTIQ4Heading.Y+lblTIQ4Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblTIQ4Prompt.Text` | `With({p:LookUp(colAnswers,Slot=4,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtTIQ4` | X `22`; Y `lblTIQ4Prompt.Y+lblTIQ4Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtTIQ4.Default` | `LookUp(colAnswers,Slot=4,Response)` |
| `txtTIQ4.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtTIQ4.DelayOutput` | `false` |
| `txtTIQ4.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcTIQ4Response.DisplayMode)` |
| `txtTIQ4.AccessibleLabel` | `LookUp(colAnswers,Slot=4,Prompt) & If(LookUp(colAnswers,Slot=4,Required),". Required", ". Optional")` |
| `lblTIQ4Counter` | X `22`; Y `txtTIQ4.Y+txtTIQ4.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblTIQ4Counter.Text` | `Text(Len(txtTIQ4.Text)) & " / " & Text(varMaxResponseLength)` |

`txtTIQ4.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=4), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 5

| Control / property | Formula or value |
|---|---|
| `dcTIQ5Response.Visible` | `5 <= varQuestionCount` |
| `dcTIQ5Response.X` / Y | `0` / `4` |
| `dcTIQ5Response.Width` | `Parent.Width` |
| `dcTIQ5Response.Height` | `If(Self.Visible, cntTIQ5.Y + cntTIQ5.Height + If(IsBlank(Self.Error), 0, errTIQ5.Height + 8) + 18, 0)` |
| `cntTIQ5` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntTIQ5.Height` | `lblTIQ5Counter.Y + lblTIQ5Counter.Height + 14` |
| `lblTIQ5Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblTIQ5Heading.Text` | `With({p:LookUp(colAnswers,Slot=5,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 5")) & If(LookUp(colAnswers,Slot=5,Required)," *","")` |
| `lblTIQ5Prompt` | X `22`; Y `lblTIQ5Heading.Y+lblTIQ5Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblTIQ5Prompt.Text` | `With({p:LookUp(colAnswers,Slot=5,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtTIQ5` | X `22`; Y `lblTIQ5Prompt.Y+lblTIQ5Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtTIQ5.Default` | `LookUp(colAnswers,Slot=5,Response)` |
| `txtTIQ5.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtTIQ5.DelayOutput` | `false` |
| `txtTIQ5.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcTIQ5Response.DisplayMode)` |
| `txtTIQ5.AccessibleLabel` | `LookUp(colAnswers,Slot=5,Prompt) & If(LookUp(colAnswers,Slot=5,Required),". Required", ". Optional")` |
| `lblTIQ5Counter` | X `22`; Y `txtTIQ5.Y+txtTIQ5.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblTIQ5Counter.Text` | `Text(Len(txtTIQ5.Text)) & " / " & Text(varMaxResponseLength)` |

`txtTIQ5.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=5), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 6

| Control / property | Formula or value |
|---|---|
| `dcTIQ6Response.Visible` | `6 <= varQuestionCount` |
| `dcTIQ6Response.X` / Y | `0` / `5` |
| `dcTIQ6Response.Width` | `Parent.Width` |
| `dcTIQ6Response.Height` | `If(Self.Visible, cntTIQ6.Y + cntTIQ6.Height + If(IsBlank(Self.Error), 0, errTIQ6.Height + 8) + 18, 0)` |
| `cntTIQ6` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntTIQ6.Height` | `lblTIQ6Counter.Y + lblTIQ6Counter.Height + 14` |
| `lblTIQ6Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblTIQ6Heading.Text` | `With({p:LookUp(colAnswers,Slot=6,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 6")) & If(LookUp(colAnswers,Slot=6,Required)," *","")` |
| `lblTIQ6Prompt` | X `22`; Y `lblTIQ6Heading.Y+lblTIQ6Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblTIQ6Prompt.Text` | `With({p:LookUp(colAnswers,Slot=6,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtTIQ6` | X `22`; Y `lblTIQ6Prompt.Y+lblTIQ6Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtTIQ6.Default` | `LookUp(colAnswers,Slot=6,Response)` |
| `txtTIQ6.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtTIQ6.DelayOutput` | `false` |
| `txtTIQ6.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcTIQ6Response.DisplayMode)` |
| `txtTIQ6.AccessibleLabel` | `LookUp(colAnswers,Slot=6,Prompt) & If(LookUp(colAnswers,Slot=6,Required),". Required", ". Optional")` |
| `lblTIQ6Counter` | X `22`; Y `txtTIQ6.Y+txtTIQ6.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblTIQ6Counter.Text` | `Text(Len(txtTIQ6.Text)) & " / " & Text(varMaxResponseLength)` |

`txtTIQ6.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=6), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

#### MDAwardTeam: form dimensions and missing-property completion

Set `frmMDAwardTeam.Width` from its actual parent as described above. Set `frmMDAwardTeam.Height` to:

```powerfx
dcTIQ1Response.Height +
dcTIQ2Response.Height +
dcTIQ3Response.Height +
dcTIQ4Response.Height +
dcTIQ5Response.Height +
dcTIQ6Response.Height +
dcTIAttachments.Height +
24
```


Rename each generated response error label as listed. Keep it directly inside the response card, not inside the question container. Set AutoHeight=true, Height=10, X=22, Width=Parent.Width-44, Text=Parent.Error, Visible=!IsBlank(Parent.Error), Color=Theme.Error, Size=9, Live=Live.Assertive. Hide only the redundant generated response field-heading labels.

| Error label | Parent card | Y |
|---|---|---|
| `errTIQ1` | `dcTIQ1Response` | `cntTIQ1.Y + cntTIQ1.Height + 4` |
| `errTIQ2` | `dcTIQ2Response` | `cntTIQ2.Y + cntTIQ2.Height + 4` |
| `errTIQ3` | `dcTIQ3Response` | `cntTIQ3.Y + cntTIQ3.Height + 4` |
| `errTIQ4` | `dcTIQ4Response` | `cntTIQ4.Y + cntTIQ4.Height + 4` |
| `errTIQ5` | `dcTIQ5Response` | `cntTIQ5.Y + cntTIQ5.Height + 4` |
| `errTIQ6` | `dcTIQ6Response` | `cntTIQ6.Y + cntTIQ6.Height + 4` |

Set these input properties in addition to the question tables:

| Input | BorderColor | Tooltip |
|---|---|---|
| `txtTIQ1` | `If(IsBlank(dcTIQ1Response.Error), dcTIQ1Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 1, Prompt)` |
| `txtTIQ2` | `If(IsBlank(dcTIQ2Response.Error), dcTIQ2Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 2, Prompt)` |
| `txtTIQ3` | `If(IsBlank(dcTIQ3Response.Error), dcTIQ3Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 3, Prompt)` |
| `txtTIQ4` | `If(IsBlank(dcTIQ4Response.Error), dcTIQ4Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 4, Prompt)` |
| `txtTIQ5` | `If(IsBlank(dcTIQ5Response.Error), dcTIQ5Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 5, Prompt)` |
| `txtTIQ6` | `If(IsBlank(dcTIQ6Response.Error), dcTIQ6Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 6, Prompt)` |

For all six inputs use Font=`Font.'Segoe UI'`, Size=`9.75`, Color=`Theme.Body`, Fill=`Theme.Surface`, BorderThickness=`1`, FocusedBorderColor=`Theme.Primary`, FocusedBorderThickness=`2`, PaddingLeft/Right=`11`, PaddingTop/Bottom=`9`, all corner radii=`4`, and TabIndex=`0`. Set heading Font=`Font.'Segoe UI'` and Color=`Theme.Heading`; prompt/counter Font=`Font.'Segoe UI'` and Color=`Theme.Muted`. Prompt AutoHeight=`true`, base Height=`34`, Size=`9.75`; counter AutoHeight=`false`, Height=`18`. All labels Wrap=`true`.


#### MDAwardTeam: native attachments and form-level errors

Keep `attTI` directly inside `dcTIAttachments`. Retain the generated DataField, Items, limits, and native binding settings. Do not replace an attachment control with a collection-backed file picker.

| Property | Value |
|---|---|
| `dcTIAttachments.Visible` | `true` |
| `dcTIAttachments.Width` | `Parent.Width` |
| `dcTIAttachments.Height` | `270` |
| `dcTIAttachments.Required` | `false` |
| `dcTIAttachments.Update` | `attTI.Attachments` |
| `attTI.Items` | `Parent.Default` |
| `attTI.DisplayMode` | `If(varIsBusy, DisplayMode.Disabled, Parent.DisplayMode)` |

For `attTI.OnAddFile`, `attTI.OnRemoveFile`, and `attTI.OnUndoRemoveFile`, use the same action:

```powerfx
Set(varHasChanges, true);
Set(varDeclarationAccepted, false);
Set(varResponsesComplete, false)
```

The attachment layout can retain the generated label/editor coordinates. If restyling it, keep the generated error label visible and reserve space for its complete text. Do not suppress native validation messages.

Add a classic label `lblSaveErrorTI` immediately after the form in the scrolling content container. Use the same X and Width as the form, Y=`frmMDAwardTeam.Y + frmMDAwardTeam.Height + 8`, AutoHeight=`true`, Text=`frmMDAwardTeam.Error`, Visible=`!IsBlank(frmMDAwardTeam.Error)`, Color=`Theme.Error`, and Live=`Live.Assertive`. Place the action row after this label when visible so errors from hidden metadata cards are not lost. Do not reset inputs on failure.


#### MDAwardTeam: action controls

| Control | Text | Visible | DisplayMode |
|---|---|---|---|
| `btnTISaveDraft` | `"Save draft"` | `!varReadOnly` | `If(varIsBusy \|\| varReadOnly \|\| !varCategoryComplete, DisplayMode.Disabled, DisplayMode.Edit)` |
| `btnTIReview` | `"Review"` | `!varReadOnly` | `If(varIsBusy \|\| varReadOnly, DisplayMode.Disabled, DisplayMode.Edit)` |
| `btnTIBack` | `"Back to details"` | `!varReadOnly` | `If(varIsBusy, DisplayMode.Disabled, DisplayMode.Edit)` |

Use the complete OnSelect blocks above for these controls. Do not append a status Patch directly after SubmitForm. A read-only Back to My nominations button can use `Navigate(scrMyNominations, ScreenTransition.None)` with Visible=`varReadOnly`.


<a id="form-tt"></a>

### SpecialTeamAward: TEAM_TRANSFORM / TT

Use the common form-building and scrolling rules above. These formulas target classic controls and English Power Fx separators. They are not yet Studio-compiled or runtime-tested.

#### Controls to create

Screen `scrSpecialTeamAward`; Edit form `frmSpecialTeamAward`; saved-record variable `varRecordTT`; latest-record variable `varLatestTT`. Create six response text inputs `txtTTQ1` … `txtTTQ6` in the corresponding response cards, and keep native attachment input `attTT` inside `dcTTAttachments`.

Form DataSource = `SpecialTeamAward`; Item = `varRecordTT`; DefaultMode = `FormMode.New`; NumberOfColumns = `1`; SnapToColumns = `false`. See layout guide for X/Y/Width/Height. Use the form's generated cards and unlock them. Preserve generated DataField strings exactly; if the connector shows a display name with spaces, use Studio's actual generated identifier. Required = `false` on entry cards to allow incomplete drafts; submission requirements are enforced separately. Do not remove metadata cards just because they are hidden.

Response cards are `dcTTQ1Response` … `dcTTQ6Response`. The other Q cards hold snapshots/flags and are hidden. Do not rename a response card to its text input name.

#### scrSpecialTeamAward.OnVisible

```powerfx
Set(varCurrentStep, 3)
```

Do not call NewForm/ResetForm here: returning from review must preserve inputs and queued files.

#### All card Update properties

| SharePoint DataField / card | Update formula |
|---|---|
| `Title` / `dcTTTitle` | `Left(varCategory.CategoryCode & " - " & If(varAwardType = "Individual", Coalesce(varEmployee.DisplayName, "Draft"), If(IsBlank(Trim(varTeamName)), "Draft", varTeamName)),255)` |
| `Category` / `dcTTCategory` | `{Id: varCategory.ID, Value: varCategory.Title}` |
| `QuestionSetVersion` / `dcTTQuestionSetVersion` | `varQuestionVersion` |
| `QuestionCount` / `dcTTQuestionCount` | `varQuestionCount` |
| `NominatedBy` / `dcTTNominatedBy` | `varNominator` |
| `NominatorEmail` / `dcTTNominatorEmail` | `varUserEmail` |
| `EmployeeRole` / `dcTTEmployeeRole` | `Trim(varRole)` |
| `EmployeeLevel` / `dcTTEmployeeLevel` | `If(IsBlank(varLevel), Blank(), LookUp(Choices(SpecialTeamAward.EmployeeLevel), Value = varLevel))` |
| `NominationStatus` / `dcTTNominationStatus` | `{Value: "Draft"}` |
| `DeclarationAccepted` / `dcTTDeclarationAccepted` | `false` |
| `SubmittedOn` / `dcTTSubmittedOn` | `Blank()` |
| `TeamName` / `dcTTTeamName` | `Trim(varTeamName)` |
| `TeamPrimaryContact` / `dcTTTeamPrimaryContact` | `If(IsBlank(varPrimaryContact.Claims), Blank(), varPrimaryContact)` |
| `TeamMembers` / `dcTTTeamMembers` | `colTeamMembers` |
| `Q1PromptSnapshot` / `dcTTQ1PromptSnapshot` | `LookUp(colAnswers, Slot = 1, Prompt)` |
| `Q1RequiredSnapshot` / `dcTTQ1RequiredSnapshot` | `LookUp(colAnswers, Slot = 1, Required)` |
| `Q1Response` / `dcTTQ1Response` | `If(1 <= varQuestionCount, txtTTQ1.Text, "")` |
| `Q2PromptSnapshot` / `dcTTQ2PromptSnapshot` | `LookUp(colAnswers, Slot = 2, Prompt)` |
| `Q2RequiredSnapshot` / `dcTTQ2RequiredSnapshot` | `LookUp(colAnswers, Slot = 2, Required)` |
| `Q2Response` / `dcTTQ2Response` | `If(2 <= varQuestionCount, txtTTQ2.Text, "")` |
| `Q3PromptSnapshot` / `dcTTQ3PromptSnapshot` | `LookUp(colAnswers, Slot = 3, Prompt)` |
| `Q3RequiredSnapshot` / `dcTTQ3RequiredSnapshot` | `LookUp(colAnswers, Slot = 3, Required)` |
| `Q3Response` / `dcTTQ3Response` | `If(3 <= varQuestionCount, txtTTQ3.Text, "")` |
| `Q4PromptSnapshot` / `dcTTQ4PromptSnapshot` | `LookUp(colAnswers, Slot = 4, Prompt)` |
| `Q4RequiredSnapshot` / `dcTTQ4RequiredSnapshot` | `LookUp(colAnswers, Slot = 4, Required)` |
| `Q4Response` / `dcTTQ4Response` | `If(4 <= varQuestionCount, txtTTQ4.Text, "")` |
| `Q5PromptSnapshot` / `dcTTQ5PromptSnapshot` | `LookUp(colAnswers, Slot = 5, Prompt)` |
| `Q5RequiredSnapshot` / `dcTTQ5RequiredSnapshot` | `LookUp(colAnswers, Slot = 5, Required)` |
| `Q5Response` / `dcTTQ5Response` | `If(5 <= varQuestionCount, txtTTQ5.Text, "")` |
| `Q6PromptSnapshot` / `dcTTQ6PromptSnapshot` | `LookUp(colAnswers, Slot = 6, Prompt)` |
| `Q6RequiredSnapshot` / `dcTTQ6RequiredSnapshot` | `LookUp(colAnswers, Slot = 6, Required)` |
| `Q6Response` / `dcTTQ6Response` | `If(6 <= varQuestionCount, txtTTQ6.Text, "")` |
| Native Attachments / `dcTTAttachments` | `attTT.Attachments` |

All cards except Q1–Q6 Response and Attachments: Visible = `false`, Height = `0`, Required = `false`. Set form-card DisplayMode to `Parent.DisplayMode`. Set each child editor DisplayMode to its card's DisplayMode, and disable it while varIsBusy. Hidden metadata's Update properties still participate in SubmitForm.

Keep native attachment Items = `Parent.Default` when directly inside its data card, and retain the generated attachment DataField (often `"{Attachments}"`). Do not type a guessed DataField. Preserve the other generated attachment properties, including MaxAttachments/MaxAttachmentSize, until an approved policy is chosen. Appending files does not save them until SubmitForm completes.

#### btnTTSaveDraft.OnSelect

```powerfx
If(!varIsBusy && !varReadOnly && varCategoryComplete,
    ClearCollect(colCapturedAnswers, Table(
    {Slot: 1, Prompt: LookUp(colAnswers, Slot = 1, Prompt), Required: LookUp(colAnswers, Slot = 1, Required), Response: txtTTQ1.Text},
    {Slot: 2, Prompt: LookUp(colAnswers, Slot = 2, Prompt), Required: LookUp(colAnswers, Slot = 2, Required), Response: txtTTQ2.Text},
    {Slot: 3, Prompt: LookUp(colAnswers, Slot = 3, Prompt), Required: LookUp(colAnswers, Slot = 3, Required), Response: txtTTQ3.Text},
    {Slot: 4, Prompt: LookUp(colAnswers, Slot = 4, Prompt), Required: LookUp(colAnswers, Slot = 4, Required), Response: txtTTQ4.Text},
    {Slot: 5, Prompt: LookUp(colAnswers, Slot = 5, Prompt), Required: LookUp(colAnswers, Slot = 5, Required), Response: txtTTQ5.Text},
    {Slot: 6, Prompt: LookUp(colAnswers, Slot = 6, Prompt), Required: LookUp(colAnswers, Slot = 6, Required), Response: txtTTQ6.Text}
));
ClearCollect(colAnswers, colCapturedAnswers);
    If(CountIf(colAnswers, Len(Response) > varMaxResponseLength) > 0,
        Notify("A response exceeds the configured limit.", NotificationType.Warning),
        Set(varIsBusy, true);
Set(varPreflightOK, true);
If(!IsBlank(varNominationId),
    IfError(
        Refresh(SpecialTeamAward);
        Set(varLatestTT, LookUp(SpecialTeamAward, ID = varNominationId));
        If(IsBlank(varLatestTT.ID) ||
           varLatestTT.NominationStatus.Value <> "Draft" ||
           varLatestTT.Modified <> varLoadedModified,
            Set(varPreflightOK, false);
            Notify("This item changed or is no longer an editable draft. Keep a copy of your changes, then reopen it from My nominations.", NotificationType.Error)
        );
        true,
        Set(varPreflightOK, false);
        Notify("Could not check the saved draft. Your changes have been retained; try again when connected.", NotificationType.Error);
        false
    )
);
If(varPreflightOK,
    Set(varSaveIntent, "Draft");
    SubmitForm(frmSpecialTeamAward),
    Set(varIsBusy, false)
)
    )
)
```

#### btnTTReview.OnSelect

Set DisplayMode to `If(varIsBusy || varReadOnly, DisplayMode.Disabled, DisplayMode.Edit)`.

```powerfx
ClearCollect(colCapturedAnswers, Table(
    {Slot: 1, Prompt: LookUp(colAnswers, Slot = 1, Prompt), Required: LookUp(colAnswers, Slot = 1, Required), Response: txtTTQ1.Text},
    {Slot: 2, Prompt: LookUp(colAnswers, Slot = 2, Prompt), Required: LookUp(colAnswers, Slot = 2, Required), Response: txtTTQ2.Text},
    {Slot: 3, Prompt: LookUp(colAnswers, Slot = 3, Prompt), Required: LookUp(colAnswers, Slot = 3, Required), Response: txtTTQ3.Text},
    {Slot: 4, Prompt: LookUp(colAnswers, Slot = 4, Prompt), Required: LookUp(colAnswers, Slot = 4, Required), Response: txtTTQ4.Text},
    {Slot: 5, Prompt: LookUp(colAnswers, Slot = 5, Prompt), Required: LookUp(colAnswers, Slot = 5, Required), Response: txtTTQ5.Text},
    {Slot: 6, Prompt: LookUp(colAnswers, Slot = 6, Prompt), Required: LookUp(colAnswers, Slot = 6, Required), Response: txtTTQ6.Text}
));
ClearCollect(colAnswers, colCapturedAnswers);
Set(varDetailsComplete, DetailsValid);
Set(varResponsesComplete, ResponsesValid);
If(!DetailsValid,
    Notify("Complete nominee details, role and level before review.", NotificationType.Warning);
    Navigate(scrNomineeDetails, ScreenTransition.None),
    !ResponsesValid,
    Notify("Complete every required response before review.", NotificationType.Warning),
    Set(varDeclarationAccepted, false);
    ClearCollect(colReviewFiles, ForAll(attTT.Attachments As file, {FileName: file.Name}));
    Set(varCurrentStep, 4);
    Navigate(scrReview, ScreenTransition.None)
)
```

`colCapturedAnswers` prevents clearing the source table while reading its snapshots. Review reads current text controls directly, so it does not depend on OnChange timing. If Studio exposes the native file-name column as DisplayName instead of Name, use that actual column in the one FileName projection above; do not change attachment Items/Update or collect file bodies.

#### frmSpecialTeamAward.OnSuccess

```powerfx
Set(varRecordTT, frmSpecialTeamAward.LastSubmit);
Set(varNominationId, varRecordTT.ID);
Set(varLoadedModified, varRecordTT.Modified);
EditForm(frmSpecialTeamAward);
Set(varHasChanges, false);
If(varSaveIntent = "Submit",
    IfError(
        Set(varRecordTT,
            Patch(SpecialTeamAward, varRecordTT,
                {NominationStatus: {Value: "Submitted"},
                 DeclarationAccepted: true, SubmittedOn: Now()}
            )
        );
        Set(varLoadedModified, varRecordTT.Modified);
        Set(varSubmittedOn, varRecordTT.SubmittedOn);
        Set(varSubmissionComplete, true);
        Set(varReadOnly, true);
        Set(varIsBusy, false);
        ViewForm(frmSpecialTeamAward);
        Navigate(scrConfirmation, ScreenTransition.None);
        true,
        Set(varIsBusy, false);
        Set(varSubmissionComplete, false);
        Set(varSaveIntent, "Draft");
        Notify("Your draft save succeeded, but submission was not confirmed. Check My nominations before retrying. Your existing item ID is retained.", NotificationType.Error);
        false
    ),
    Set(varIsBusy, false);
    Notify("Draft saved. Reference: " & varCategory.CategoryCode & "-" & Text(varNominationId, "000000"), NotificationType.Success)
)
```

#### frmSpecialTeamAward.OnFailure

```powerfx
Set(varIsBusy, false);
Set(varSubmissionComplete, false);
Set(varHasChanges, true);
Notify("Save was not confirmed. Your inputs are retained. If the connection timed out, check My nominations before retrying because the server may have saved the item.", NotificationType.Error)
```

#### Back to details

Use a native button; Visible = `!varReadOnly`; DisplayMode disabled while varIsBusy. Its OnSelect:

```powerfx
ClearCollect(colCapturedAnswers, Table(
    {Slot: 1, Prompt: LookUp(colAnswers, Slot = 1, Prompt), Required: LookUp(colAnswers, Slot = 1, Required), Response: txtTTQ1.Text},
    {Slot: 2, Prompt: LookUp(colAnswers, Slot = 2, Prompt), Required: LookUp(colAnswers, Slot = 2, Required), Response: txtTTQ2.Text},
    {Slot: 3, Prompt: LookUp(colAnswers, Slot = 3, Prompt), Required: LookUp(colAnswers, Slot = 3, Required), Response: txtTTQ3.Text},
    {Slot: 4, Prompt: LookUp(colAnswers, Slot = 4, Prompt), Required: LookUp(colAnswers, Slot = 4, Required), Response: txtTTQ4.Text},
    {Slot: 5, Prompt: LookUp(colAnswers, Slot = 5, Prompt), Required: LookUp(colAnswers, Slot = 5, Required), Response: txtTTQ5.Text},
    {Slot: 6, Prompt: LookUp(colAnswers, Slot = 6, Prompt), Required: LookUp(colAnswers, Slot = 6, Required), Response: txtTTQ6.Text}
));
ClearCollect(colAnswers, colCapturedAnswers);
Set(varDeclarationAccepted, false);
Set(varCurrentStep, 1);
Navigate(scrNomineeDetails, ScreenTransition.None)
```

#### My nominations gallery galMineTT

Visible = `varBrowseCode = "TEAM_TRANSFORM"`. Items:

```powerfx
SortByColumns(
    Filter(SpecialTeamAward,
        NominatorEmail = varUserEmail,
        (varBrowseStatus = "All" || NominationStatus.Value = varBrowseStatus),
        (varBrowseId = 0 || ID = varBrowseId)
    ),
    "Modified", SortOrder.Descending
)
```

Use `ThisItem.ID`, `ThisItem.Modified`, `ThisItem.NominationStatus.Value`, and `ThisItem.TeamName` in native labels. Reference Text = `"TEAM_TRANSFORM-" & Text(ThisItem.ID, "000000")`. An Open button inside this gallery uses the following OnSelect; it queries the clicked ID again before opening. Inactive/retired categories can still open historical records.

```powerfx
If(!varIsBusy,
    Set(varIsBusy, true);
    Set(varOpenOK, true);
    IfError(
        Refresh(SpecialTeamAward);
        Set(varRecordTT, LookUp(SpecialTeamAward, ID = ThisItem.ID && NominatorEmail = varUserEmail));
        Refresh(AwardCategories);
        Set(varCategory, LookUp(AwardCategories, ID = varRecordTT.Category.Id));
        true,
        Set(varOpenOK, false);
        false
    );
    If(!varOpenOK || IsBlank(varRecordTT.ID) || varCategory.CategoryCode <> "TEAM_TRANSFORM" ||
       IsBlank(varRecordTT.QuestionSetVersion) || varRecordTT.QuestionSetVersion < 1 ||
       IsBlank(varRecordTT.QuestionCount) || varRecordTT.QuestionCount < 3 || varRecordTT.QuestionCount > 6 ||
       varRecordTT.QuestionCount <> RoundDown(varRecordTT.QuestionCount,0) ||
       IsBlank(varRecordTT.Q1PromptSnapshot) || IsBlank(varRecordTT.Q2PromptSnapshot) || IsBlank(varRecordTT.Q3PromptSnapshot) ||
       (varRecordTT.QuestionCount>=4 && IsBlank(varRecordTT.Q4PromptSnapshot)) ||
       (varRecordTT.QuestionCount>=5 && IsBlank(varRecordTT.Q5PromptSnapshot)) ||
       (varRecordTT.QuestionCount>=6 && IsBlank(varRecordTT.Q6PromptSnapshot)) ||
       !(varRecordTT.NominationStatus.Value in ["Draft", "Submitted"]),
        Set(varIsBusy, false);
        Notify("Unable to open this nomination. Check access and the saved category/question metadata.", NotificationType.Error),
        Set(varAwardType, "Team");
        Set(varNominationId, varRecordTT.ID);
        Set(varLoadedModified, varRecordTT.Modified);
        Set(varQuestionVersion, varRecordTT.QuestionSetVersion);
        Set(varQuestionCount, varRecordTT.QuestionCount);
        Set(varRole, Coalesce(varRecordTT.EmployeeRole, ""));
        Set(varLevel, Coalesce(varRecordTT.EmployeeLevel.Value, ""));
        Set(varNominator, varRecordTT.NominatedBy);
        Set(varTeamName, Coalesce(varRecordTT.TeamName, ""));
        Set(varPrimaryContact, Coalesce(varRecordTT.TeamPrimaryContact, varEmptyPerson));
        Set(varEmployee, varEmptyPerson);
        ClearCollect(colTeamMembers, varRecordTT.TeamMembers);
        ClearCollect(colAnswers, Table(
    {Slot: 1, Prompt: Coalesce(varRecordTT.Q1PromptSnapshot, ""), Required: Coalesce(varRecordTT.Q1RequiredSnapshot, false), Response: Coalesce(varRecordTT.Q1Response, "")},
    {Slot: 2, Prompt: Coalesce(varRecordTT.Q2PromptSnapshot, ""), Required: Coalesce(varRecordTT.Q2RequiredSnapshot, false), Response: Coalesce(varRecordTT.Q2Response, "")},
    {Slot: 3, Prompt: Coalesce(varRecordTT.Q3PromptSnapshot, ""), Required: Coalesce(varRecordTT.Q3RequiredSnapshot, false), Response: Coalesce(varRecordTT.Q3Response, "")},
    {Slot: 4, Prompt: Coalesce(varRecordTT.Q4PromptSnapshot, ""), Required: Coalesce(varRecordTT.Q4RequiredSnapshot, false), Response: Coalesce(varRecordTT.Q4Response, "")},
    {Slot: 5, Prompt: Coalesce(varRecordTT.Q5PromptSnapshot, ""), Required: Coalesce(varRecordTT.Q5RequiredSnapshot, false), Response: Coalesce(varRecordTT.Q5Response, "")},
    {Slot: 6, Prompt: Coalesce(varRecordTT.Q6PromptSnapshot, ""), Required: Coalesce(varRecordTT.Q6RequiredSnapshot, false), Response: Coalesce(varRecordTT.Q6Response, "")}
));
        Set(varReadOnly, varRecordTT.NominationStatus.Value = "Submitted");
        Set(varSubmissionComplete, varReadOnly);
        Set(varSubmittedOn, varRecordTT.SubmittedOn);
        Set(varCategoryComplete, true);
        Set(varDetailsComplete, DetailsValid);
        Set(varResponsesComplete, ResponsesValid);
        Set(varDeclarationAccepted, false);
        Set(varHasChanges, false);
        Set(varSaveIntent, "Draft");
        ResetForm(frmSpecialTeamAward);
        If(varReadOnly, ViewForm(frmSpecialTeamAward), EditForm(frmSpecialTeamAward));
        Set(varIsBusy, false);
        Navigate(scrSpecialTeamAward, ScreenTransition.None)
    )
)
```

Submitted items reuse this same typed form in View mode, including native file download. Form entry actions are hidden. This is the read-only screen implementation; a separate duplicate scrViewNomination is unnecessary.

#### Check this category before continuing

Save an incomplete draft, retain its ID, attach a small synthetic file, save again, reopen it, complete required answers, review unsaved changes, and submit. Confirm one item, correct snapshots, declaration and SubmittedOn. Reopen read-only. Test failed save/retry and concurrent modification. Use the full acceptance checklist; no runtime results are claimed here.

#### Question control properties

Insert a manual container inside each response card. Keep these exact unique names. Set label Font to Segoe UI, heading Color to Theme.Heading, body/counter Color to Theme.Muted. All labels wrap. Use the common input styling from the layout guide.

##### Slot 1

| Control / property | Formula or value |
|---|---|
| `dcTTQ1Response.Visible` | `1 <= varQuestionCount` |
| `dcTTQ1Response.X` / Y | `0` / `0` |
| `dcTTQ1Response.Width` | `Parent.Width` |
| `dcTTQ1Response.Height` | `If(Self.Visible, cntTTQ1.Y + cntTTQ1.Height + If(IsBlank(Self.Error), 0, errTTQ1.Height + 8) + 18, 0)` |
| `cntTTQ1` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntTTQ1.Height` | `lblTTQ1Counter.Y + lblTTQ1Counter.Height + 14` |
| `lblTTQ1Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblTTQ1Heading.Text` | `With({p:LookUp(colAnswers,Slot=1,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 1")) & If(LookUp(colAnswers,Slot=1,Required)," *","")` |
| `lblTTQ1Prompt` | X `22`; Y `lblTTQ1Heading.Y+lblTTQ1Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblTTQ1Prompt.Text` | `With({p:LookUp(colAnswers,Slot=1,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtTTQ1` | X `22`; Y `lblTTQ1Prompt.Y+lblTTQ1Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtTTQ1.Default` | `LookUp(colAnswers,Slot=1,Response)` |
| `txtTTQ1.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtTTQ1.DelayOutput` | `false` |
| `txtTTQ1.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcTTQ1Response.DisplayMode)` |
| `txtTTQ1.AccessibleLabel` | `LookUp(colAnswers,Slot=1,Prompt) & If(LookUp(colAnswers,Slot=1,Required),". Required", ". Optional")` |
| `lblTTQ1Counter` | X `22`; Y `txtTTQ1.Y+txtTTQ1.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblTTQ1Counter.Text` | `Text(Len(txtTTQ1.Text)) & " / " & Text(varMaxResponseLength)` |

`txtTTQ1.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=1), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 2

| Control / property | Formula or value |
|---|---|
| `dcTTQ2Response.Visible` | `2 <= varQuestionCount` |
| `dcTTQ2Response.X` / Y | `0` / `1` |
| `dcTTQ2Response.Width` | `Parent.Width` |
| `dcTTQ2Response.Height` | `If(Self.Visible, cntTTQ2.Y + cntTTQ2.Height + If(IsBlank(Self.Error), 0, errTTQ2.Height + 8) + 18, 0)` |
| `cntTTQ2` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntTTQ2.Height` | `lblTTQ2Counter.Y + lblTTQ2Counter.Height + 14` |
| `lblTTQ2Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblTTQ2Heading.Text` | `With({p:LookUp(colAnswers,Slot=2,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 2")) & If(LookUp(colAnswers,Slot=2,Required)," *","")` |
| `lblTTQ2Prompt` | X `22`; Y `lblTTQ2Heading.Y+lblTTQ2Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblTTQ2Prompt.Text` | `With({p:LookUp(colAnswers,Slot=2,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtTTQ2` | X `22`; Y `lblTTQ2Prompt.Y+lblTTQ2Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtTTQ2.Default` | `LookUp(colAnswers,Slot=2,Response)` |
| `txtTTQ2.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtTTQ2.DelayOutput` | `false` |
| `txtTTQ2.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcTTQ2Response.DisplayMode)` |
| `txtTTQ2.AccessibleLabel` | `LookUp(colAnswers,Slot=2,Prompt) & If(LookUp(colAnswers,Slot=2,Required),". Required", ". Optional")` |
| `lblTTQ2Counter` | X `22`; Y `txtTTQ2.Y+txtTTQ2.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblTTQ2Counter.Text` | `Text(Len(txtTTQ2.Text)) & " / " & Text(varMaxResponseLength)` |

`txtTTQ2.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=2), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 3

| Control / property | Formula or value |
|---|---|
| `dcTTQ3Response.Visible` | `3 <= varQuestionCount` |
| `dcTTQ3Response.X` / Y | `0` / `2` |
| `dcTTQ3Response.Width` | `Parent.Width` |
| `dcTTQ3Response.Height` | `If(Self.Visible, cntTTQ3.Y + cntTTQ3.Height + If(IsBlank(Self.Error), 0, errTTQ3.Height + 8) + 18, 0)` |
| `cntTTQ3` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntTTQ3.Height` | `lblTTQ3Counter.Y + lblTTQ3Counter.Height + 14` |
| `lblTTQ3Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblTTQ3Heading.Text` | `With({p:LookUp(colAnswers,Slot=3,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 3")) & If(LookUp(colAnswers,Slot=3,Required)," *","")` |
| `lblTTQ3Prompt` | X `22`; Y `lblTTQ3Heading.Y+lblTTQ3Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblTTQ3Prompt.Text` | `With({p:LookUp(colAnswers,Slot=3,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtTTQ3` | X `22`; Y `lblTTQ3Prompt.Y+lblTTQ3Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtTTQ3.Default` | `LookUp(colAnswers,Slot=3,Response)` |
| `txtTTQ3.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtTTQ3.DelayOutput` | `false` |
| `txtTTQ3.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcTTQ3Response.DisplayMode)` |
| `txtTTQ3.AccessibleLabel` | `LookUp(colAnswers,Slot=3,Prompt) & If(LookUp(colAnswers,Slot=3,Required),". Required", ". Optional")` |
| `lblTTQ3Counter` | X `22`; Y `txtTTQ3.Y+txtTTQ3.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblTTQ3Counter.Text` | `Text(Len(txtTTQ3.Text)) & " / " & Text(varMaxResponseLength)` |

`txtTTQ3.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=3), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 4

| Control / property | Formula or value |
|---|---|
| `dcTTQ4Response.Visible` | `4 <= varQuestionCount` |
| `dcTTQ4Response.X` / Y | `0` / `3` |
| `dcTTQ4Response.Width` | `Parent.Width` |
| `dcTTQ4Response.Height` | `If(Self.Visible, cntTTQ4.Y + cntTTQ4.Height + If(IsBlank(Self.Error), 0, errTTQ4.Height + 8) + 18, 0)` |
| `cntTTQ4` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntTTQ4.Height` | `lblTTQ4Counter.Y + lblTTQ4Counter.Height + 14` |
| `lblTTQ4Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblTTQ4Heading.Text` | `With({p:LookUp(colAnswers,Slot=4,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 4")) & If(LookUp(colAnswers,Slot=4,Required)," *","")` |
| `lblTTQ4Prompt` | X `22`; Y `lblTTQ4Heading.Y+lblTTQ4Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblTTQ4Prompt.Text` | `With({p:LookUp(colAnswers,Slot=4,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtTTQ4` | X `22`; Y `lblTTQ4Prompt.Y+lblTTQ4Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtTTQ4.Default` | `LookUp(colAnswers,Slot=4,Response)` |
| `txtTTQ4.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtTTQ4.DelayOutput` | `false` |
| `txtTTQ4.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcTTQ4Response.DisplayMode)` |
| `txtTTQ4.AccessibleLabel` | `LookUp(colAnswers,Slot=4,Prompt) & If(LookUp(colAnswers,Slot=4,Required),". Required", ". Optional")` |
| `lblTTQ4Counter` | X `22`; Y `txtTTQ4.Y+txtTTQ4.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblTTQ4Counter.Text` | `Text(Len(txtTTQ4.Text)) & " / " & Text(varMaxResponseLength)` |

`txtTTQ4.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=4), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 5

| Control / property | Formula or value |
|---|---|
| `dcTTQ5Response.Visible` | `5 <= varQuestionCount` |
| `dcTTQ5Response.X` / Y | `0` / `4` |
| `dcTTQ5Response.Width` | `Parent.Width` |
| `dcTTQ5Response.Height` | `If(Self.Visible, cntTTQ5.Y + cntTTQ5.Height + If(IsBlank(Self.Error), 0, errTTQ5.Height + 8) + 18, 0)` |
| `cntTTQ5` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntTTQ5.Height` | `lblTTQ5Counter.Y + lblTTQ5Counter.Height + 14` |
| `lblTTQ5Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblTTQ5Heading.Text` | `With({p:LookUp(colAnswers,Slot=5,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 5")) & If(LookUp(colAnswers,Slot=5,Required)," *","")` |
| `lblTTQ5Prompt` | X `22`; Y `lblTTQ5Heading.Y+lblTTQ5Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblTTQ5Prompt.Text` | `With({p:LookUp(colAnswers,Slot=5,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtTTQ5` | X `22`; Y `lblTTQ5Prompt.Y+lblTTQ5Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtTTQ5.Default` | `LookUp(colAnswers,Slot=5,Response)` |
| `txtTTQ5.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtTTQ5.DelayOutput` | `false` |
| `txtTTQ5.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcTTQ5Response.DisplayMode)` |
| `txtTTQ5.AccessibleLabel` | `LookUp(colAnswers,Slot=5,Prompt) & If(LookUp(colAnswers,Slot=5,Required),". Required", ". Optional")` |
| `lblTTQ5Counter` | X `22`; Y `txtTTQ5.Y+txtTTQ5.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblTTQ5Counter.Text` | `Text(Len(txtTTQ5.Text)) & " / " & Text(varMaxResponseLength)` |

`txtTTQ5.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=5), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

##### Slot 6

| Control / property | Formula or value |
|---|---|
| `dcTTQ6Response.Visible` | `6 <= varQuestionCount` |
| `dcTTQ6Response.X` / Y | `0` / `5` |
| `dcTTQ6Response.Width` | `Parent.Width` |
| `dcTTQ6Response.Height` | `If(Self.Visible, cntTTQ6.Y + cntTTQ6.Height + If(IsBlank(Self.Error), 0, errTTQ6.Height + 8) + 18, 0)` |
| `cntTTQ6` inside card | X/Y `0`; Width `Parent.Width`; Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; radius `8` |
| `cntTTQ6.Height` | `lblTTQ6Counter.Y + lblTTQ6Counter.Height + 14` |
| `lblTTQ6Heading` inside container | X `22`; Y `20`; Width `Parent.Width-44`; AutoHeight `true`; Size `12.75`; Semibold |
| `lblTTQ6Heading.Text` | `With({p:LookUp(colAnswers,Slot=6,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 6")) & If(LookUp(colAnswers,Slot=6,Required)," *","")` |
| `lblTTQ6Prompt` | X `22`; Y `lblTTQ6Heading.Y+lblTTQ6Heading.Height+8`; Width `Parent.Width-44`; AutoHeight `true`; Size `9.75` |
| `lblTTQ6Prompt.Text` | `With({p:LookUp(colAnswers,Slot=6,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `txtTTQ6` | X `22`; Y `lblTTQ6Prompt.Y+lblTTQ6Prompt.Height+18`; Width `Parent.Width-44`; Height `If(App.Width<=760,180,142)` |
| `txtTTQ6.Default` | `LookUp(colAnswers,Slot=6,Response)` |
| `txtTTQ6.Mode` / MaxLength | `TextMode.MultiLine` / `varMaxResponseLength` |
| `txtTTQ6.DelayOutput` | `false` |
| `txtTTQ6.DisplayMode` | `If(varIsBusy,DisplayMode.Disabled,dcTTQ6Response.DisplayMode)` |
| `txtTTQ6.AccessibleLabel` | `LookUp(colAnswers,Slot=6,Prompt) & If(LookUp(colAnswers,Slot=6,Required),". Required", ". Optional")` |
| `lblTTQ6Counter` | X `22`; Y `txtTTQ6.Y+txtTTQ6.Height+6`; Width `Parent.Width-44`; Height `18`; Size `7.5`; Align `Align.Right` |
| `lblTTQ6Counter.Text` | `Text(Len(txtTTQ6.Text)) & " / " & Text(varMaxResponseLength)` |

`txtTTQ6.OnChange`:

```powerfx
Patch(colAnswers, LookUp(colAnswers,Slot=6), {Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

#### SpecialTeamAward: form dimensions and missing-property completion

Set `frmSpecialTeamAward.Width` from its actual parent as described above. Set `frmSpecialTeamAward.Height` to:

```powerfx
dcTTQ1Response.Height +
dcTTQ2Response.Height +
dcTTQ3Response.Height +
dcTTQ4Response.Height +
dcTTQ5Response.Height +
dcTTQ6Response.Height +
dcTTAttachments.Height +
24
```


Rename each generated response error label as listed. Keep it directly inside the response card, not inside the question container. Set AutoHeight=true, Height=10, X=22, Width=Parent.Width-44, Text=Parent.Error, Visible=!IsBlank(Parent.Error), Color=Theme.Error, Size=9, Live=Live.Assertive. Hide only the redundant generated response field-heading labels.

| Error label | Parent card | Y |
|---|---|---|
| `errTTQ1` | `dcTTQ1Response` | `cntTTQ1.Y + cntTTQ1.Height + 4` |
| `errTTQ2` | `dcTTQ2Response` | `cntTTQ2.Y + cntTTQ2.Height + 4` |
| `errTTQ3` | `dcTTQ3Response` | `cntTTQ3.Y + cntTTQ3.Height + 4` |
| `errTTQ4` | `dcTTQ4Response` | `cntTTQ4.Y + cntTTQ4.Height + 4` |
| `errTTQ5` | `dcTTQ5Response` | `cntTTQ5.Y + cntTTQ5.Height + 4` |
| `errTTQ6` | `dcTTQ6Response` | `cntTTQ6.Y + cntTTQ6.Height + 4` |

Set these input properties in addition to the question tables:

| Input | BorderColor | Tooltip |
|---|---|---|
| `txtTTQ1` | `If(IsBlank(dcTTQ1Response.Error), dcTTQ1Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 1, Prompt)` |
| `txtTTQ2` | `If(IsBlank(dcTTQ2Response.Error), dcTTQ2Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 2, Prompt)` |
| `txtTTQ3` | `If(IsBlank(dcTTQ3Response.Error), dcTTQ3Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 3, Prompt)` |
| `txtTTQ4` | `If(IsBlank(dcTTQ4Response.Error), dcTTQ4Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 4, Prompt)` |
| `txtTTQ5` | `If(IsBlank(dcTTQ5Response.Error), dcTTQ5Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 5, Prompt)` |
| `txtTTQ6` | `If(IsBlank(dcTTQ6Response.Error), dcTTQ6Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 6, Prompt)` |

For all six inputs use Font=`Font.'Segoe UI'`, Size=`9.75`, Color=`Theme.Body`, Fill=`Theme.Surface`, BorderThickness=`1`, FocusedBorderColor=`Theme.Primary`, FocusedBorderThickness=`2`, PaddingLeft/Right=`11`, PaddingTop/Bottom=`9`, all corner radii=`4`, and TabIndex=`0`. Set heading Font=`Font.'Segoe UI'` and Color=`Theme.Heading`; prompt/counter Font=`Font.'Segoe UI'` and Color=`Theme.Muted`. Prompt AutoHeight=`true`, base Height=`34`, Size=`9.75`; counter AutoHeight=`false`, Height=`18`. All labels Wrap=`true`.


#### SpecialTeamAward: native attachments and form-level errors

Keep `attTT` directly inside `dcTTAttachments`. Retain the generated DataField, Items, limits, and native binding settings. Do not replace an attachment control with a collection-backed file picker.

| Property | Value |
|---|---|
| `dcTTAttachments.Visible` | `true` |
| `dcTTAttachments.Width` | `Parent.Width` |
| `dcTTAttachments.Height` | `270` |
| `dcTTAttachments.Required` | `false` |
| `dcTTAttachments.Update` | `attTT.Attachments` |
| `attTT.Items` | `Parent.Default` |
| `attTT.DisplayMode` | `If(varIsBusy, DisplayMode.Disabled, Parent.DisplayMode)` |

For `attTT.OnAddFile`, `attTT.OnRemoveFile`, and `attTT.OnUndoRemoveFile`, use the same action:

```powerfx
Set(varHasChanges, true);
Set(varDeclarationAccepted, false);
Set(varResponsesComplete, false)
```

The attachment layout can retain the generated label/editor coordinates. If restyling it, keep the generated error label visible and reserve space for its complete text. Do not suppress native validation messages.

Add a classic label `lblSaveErrorTT` immediately after the form in the scrolling content container. Use the same X and Width as the form, Y=`frmSpecialTeamAward.Y + frmSpecialTeamAward.Height + 8`, AutoHeight=`true`, Text=`frmSpecialTeamAward.Error`, Visible=`!IsBlank(frmSpecialTeamAward.Error)`, Color=`Theme.Error`, and Live=`Live.Assertive`. Place the action row after this label when visible so errors from hidden metadata cards are not lost. Do not reset inputs on failure.


#### SpecialTeamAward: action controls

| Control | Text | Visible | DisplayMode |
|---|---|---|---|
| `btnTTSaveDraft` | `"Save draft"` | `!varReadOnly` | `If(varIsBusy \|\| varReadOnly \|\| !varCategoryComplete, DisplayMode.Disabled, DisplayMode.Edit)` |
| `btnTTReview` | `"Review"` | `!varReadOnly` | `If(varIsBusy \|\| varReadOnly, DisplayMode.Disabled, DisplayMode.Edit)` |
| `btnTTBack` | `"Back to details"` | `!varReadOnly` | `If(varIsBusy, DisplayMode.Disabled, DisplayMode.Edit)` |

Use the complete OnSelect blocks above for these controls. Do not append a status Patch directly after SubmitForm. A read-only Back to My nominations button can use `Navigate(scrMyNominations, ScreenTransition.None)` with Visible=`varReadOnly`.


## Shared app formulas and routed actions

Create all six forms/data sources and all named shared controls first. Set App.StartScreen to `scrHome`. Paste named formulas into App.Formulas, initialization actions into App.OnStart, and run OnStart once during setup. Do not initialize by merely setting every unresolved name to false; records, person objects, collections, and named formulas have specific types.

The all-zero administrator object ID below is a nonfunctional placeholder, not an authorization policy. Configure actual identities privately and enforce SharePoint permissions. The app-level flag only controls UI visibility.


### App.Formulas

```powerfx
Theme = {
    Brand: "Contoso", AppTitle: "Employee & Team Recognition Awards",
    PrimaryHex: "#0f6cbd", SuccessHex: "#107c10", BorderHex: "#d8dee7",
    MutedHex: "#667085", PaleHex: "#eff6fc",
    Primary: ColorValue("#0f6cbd"), PrimaryHover: ColorValue("#0b5a9e"),
    Heading: ColorValue("#17253f"), Body: ColorValue("#27364f"),
    Muted: ColorValue("#667085"), Border: ColorValue("#d8dee7"),
    SoftBorder: ColorValue("#e8ebf0"), Page: ColorValue("#f4f6f8"),
    Surface: ColorValue("#ffffff"), Pale: ColorValue("#eff6fc"),
    Success: ColorValue("#107c10"), SuccessPale: ColorValue("#f1faf1"),
    Error: ColorValue("#c50f1f")
};
LevelOptions = Switch(varCategory.CategoryCode,
    "IND_CUSTOMER",Choices(MDAward.EmployeeLevel),
    "IND_EXCELLENCE",Choices(TrendMarcherAward.EmployeeLevel),
    "TEAM_COLLAB",Choices(BestInnovatorTeam.EmployeeLevel),
    "TEAM_IMPACT",Choices(MDAwardTeam.EmployeeLevel),
    "TEAM_TRANSFORM",Choices(SpecialTeamAward.EmployeeLevel),
    Choices(BestInnovatorIndividual.EmployeeLevel)
);
DetailsValid =
    If(varAwardType = "Individual",
        !IsBlank(varEmployee.Claims),
        !IsBlank(Trim(varTeamName)) && !IsBlank(varPrimaryContact.Claims)
    ) && !IsBlank(Trim(varRole)) && !IsBlank(varLevel) &&
    CountIf(LevelOptions,Value=varLevel)>0;
ResponsesValid =
    varQuestionCount >= 3 && varQuestionCount <= 6 &&
    CountIf(colAnswers, Slot <= varQuestionCount &&
        ((Required && IsBlank(Trim(Substitute(Substitute(Substitute(Response,Char(10)," "),Char(13)," "),Char(9)," ")))) || Len(Response) > varMaxResponseLength)
    ) = 0;
NomineeDisplay = If(varAwardType = "Individual", varEmployee.DisplayName, varTeamName);
NominationReference = If(IsBlank(varNominationId), "Not saved yet",
    varCategory.CategoryCode & "-" & Text(varNominationId, "000000"));
```


### App.OnStart

```powerfx
Set(varUserEmail, Lower(User().Email));
Set(varMaxResponseLength, 2000);
Set(varEmptyPerson, {
    '@odata.type': "#Microsoft.Azure.Connectors.SharePoint.SPListExpandedUser",
    Claims: "", DisplayName: "", Email: "", Department: "", JobTitle: "", Picture: ""
});
Set(varSignedInPerson, {
    '@odata.type': "#Microsoft.Azure.Connectors.SharePoint.SPListExpandedUser",
    Claims: "i:0#.f|membership|" & varUserEmail,
    DisplayName: User().FullName, Email: varUserEmail,
    Department: "", JobTitle: "", Picture: ""
});
ClearCollect(colQuestionAdminIds, {ObjectId: "00000000-0000-0000-0000-000000000000"});
Set(varCanManageQuestions, Lower(Text(User().EntraObjectId)) in colQuestionAdminIds.ObjectId);
Set(varIsBusy, false);
Set(varReadOnly, false);
Set(varHasChanges, false);
Set(varDeclarationAccepted, false);
Set(varCurrentStep, 1);
Set(varDetailsComplete, false);
Set(varCategoryComplete, false);
Set(varResponsesComplete, false);
Set(varSubmissionComplete, false);
Set(varAwardType, "Individual");
Set(varEmployee, varEmptyPerson);
Set(varPrimaryContact, varEmptyPerson);
Set(varNominator, varSignedInPerson);
Set(varTeamName, "");
Set(varRole, "");
Set(varLevel, "");
Set(varCategory, Defaults(AwardCategories));
Set(varPendingCategory, Defaults(AwardCategories));
Set(varNominationId, Blank());
Set(varLoadedModified, Blank());
Set(varSubmittedOn, Blank());
Set(varQuestionVersion, 0);
Set(varQuestionCount, 0);
Set(varSaveIntent, "Draft");
Set(varShowCategoryChangeDialog, false);
Set(varShowExitDialog, false);
Set(varShowAdminDiscard, false);
Set(varExitAction, "");
Set(varBrowseCode, "IND_INNOVATION");
Set(varBrowseType, "Individual");
Set(varBrowseStatus, "All");
Set(varBrowseId, 0);
ClearCollect(colTeamMembers, varEmptyPerson); Clear(colTeamMembers);
ClearCollect(colAnswers, ForAll(Sequence(6) As n,
    {Slot: n.Value, Prompt: "", Required: false, Response: ""}));
ClearCollect(colCapturedAnswers, colAnswers);
ClearCollect(colReviewFiles, {FileName: ""}); Clear(colReviewFiles);
ClearCollect(colCandidateQuestions, Defaults(AwardQuestions)); Clear(colCandidateQuestions);
ClearCollect(colCategoryOptions, Defaults(AwardCategories)); Clear(colCategoryOptions);
ClearCollect(colAdminCategories, Defaults(AwardCategories)); Clear(colAdminCategories);
ClearCollect(colAdminSource, Defaults(AwardQuestions)); Clear(colAdminSource);
ClearCollect(colAdminQuestions,
    {Slot: 1, Title: "", QuestionText: "", GuidanceText: "", IsRequired: true});
Clear(colAdminQuestions);
ClearCollect(colPublishErrors, {Slot: 0, Message: ""}); Clear(colPublishErrors);
Set(varAdminCategory, Defaults(AwardCategories));
Set(varAdminBaseVersion, 0);
Set(varAdminNewVersion, 0);
Set(varAdminSourceVersion, 0);
Set(varAdminDirty, false);
Set(varAdminLoadOK, false);
Set(varRecordII, Defaults(BestInnovatorIndividual));
Set(varRecordIC, Defaults(MDAward));
Set(varRecordIE, Defaults(TrendMarcherAward));
Set(varRecordTC, Defaults(BestInnovatorTeam));
Set(varRecordTI, Defaults(MDAwardTeam));
Set(varRecordTT, Defaults(SpecialTeamAward));
```


### New nomination action after any required discard confirmation

```powerfx
Set(varAwardType, "Individual");
Set(varEmployee, varEmptyPerson);
Set(varPrimaryContact, varEmptyPerson);
Set(varNominator, varSignedInPerson);
Set(varTeamName, ""); Set(varRole, ""); Set(varLevel, "");
Clear(colTeamMembers);
Set(varCategory, Defaults(AwardCategories));
Set(varPendingCategory, Defaults(AwardCategories));
Set(varNominationId, Blank()); Set(varLoadedModified, Blank()); Set(varSubmittedOn, Blank());
Set(varQuestionVersion, 0); Set(varQuestionCount, 0);
Set(varReadOnly, false); Set(varIsBusy, false); Set(varHasChanges, false);
Set(varSaveIntent, "Draft"); Set(varDeclarationAccepted, false);
Set(varCurrentStep, 1); Set(varDetailsComplete, false); Set(varCategoryComplete, false);
Set(varResponsesComplete, false); Set(varSubmissionComplete, false);
Set(varShowExitDialog, false); Set(varShowCategoryChangeDialog, false);
ClearCollect(colAnswers, ForAll(Sequence(6) As n,
    {Slot: n.Value, Prompt: "", Required: false, Response: ""}));
Clear(colReviewFiles);
Set(varRecordII, Defaults(BestInnovatorIndividual));
ResetForm(frmBestInnovatorIndividual);
NewForm(frmBestInnovatorIndividual);
Set(varRecordIC, Defaults(MDAward));
ResetForm(frmMDAward);
NewForm(frmMDAward);
Set(varRecordIE, Defaults(TrendMarcherAward));
ResetForm(frmTrendMarcherAward);
NewForm(frmTrendMarcherAward);
Set(varRecordTC, Defaults(BestInnovatorTeam));
ResetForm(frmBestInnovatorTeam);
NewForm(frmBestInnovatorTeam);
Set(varRecordTI, Defaults(MDAwardTeam));
ResetForm(frmMDAwardTeam);
NewForm(frmMDAwardTeam);
Set(varRecordTT, Defaults(SpecialTeamAward));
ResetForm(frmSpecialTeamAward);
NewForm(frmSpecialTeamAward);
Navigate(scrNomineeDetails, ScreenTransition.None)
```


### Details Continue button OnSelect

```powerfx
Set(varTeamName, txtTeamName.Text);
Set(varRole, txtRole.Text);
Set(varLevel, Coalesce(cmbLevel.Selected.Value, ""));
Set(varDetailsComplete, DetailsValid);
Set(varDeclarationAccepted, false);
If(varCategoryComplete,
    Switch(varCategory.CategoryCode,
    "IND_INNOVATION", Navigate(scrBestInnovatorIndividual, ScreenTransition.None),
    "IND_CUSTOMER", Navigate(scrMDAward, ScreenTransition.None),
    "IND_EXCELLENCE", Navigate(scrTrendMarcherAward, ScreenTransition.None),
    "TEAM_COLLAB", Navigate(scrBestInnovatorTeam, ScreenTransition.None),
    "TEAM_IMPACT", Navigate(scrMDAwardTeam, ScreenTransition.None),
    "TEAM_TRANSFORM", Navigate(scrSpecialTeamAward, ScreenTransition.None),
    Notify("This category has no configured form.", NotificationType.Error)
),
    Set(varCurrentStep, 2);
    Navigate(scrCategorySelection, ScreenTransition.None)
)
```


### Category load action after selection/discard checks

```powerfx
If(!varIsBusy,
    If(varCategoryComplete && varPendingCategory.ID = varCategory.ID,
        Switch(varCategory.CategoryCode,
    "IND_INNOVATION", Navigate(scrBestInnovatorIndividual, ScreenTransition.None),
    "IND_CUSTOMER", Navigate(scrMDAward, ScreenTransition.None),
    "IND_EXCELLENCE", Navigate(scrTrendMarcherAward, ScreenTransition.None),
    "TEAM_COLLAB", Navigate(scrBestInnovatorTeam, ScreenTransition.None),
    "TEAM_IMPACT", Navigate(scrMDAwardTeam, ScreenTransition.None),
    "TEAM_TRANSFORM", Navigate(scrSpecialTeamAward, ScreenTransition.None),
    Notify("This category has no configured form.", NotificationType.Error)
),
        Set(varIsBusy, true);
        Set(varLoadOK, true);
        IfError(
            Refresh(AwardCategories);
            Set(varCandidateCategory, LookUp(AwardCategories, ID = varPendingCategory.ID));
            Refresh(AwardQuestions);
            ClearCollect(colCandidateQuestions,
                SortByColumns(Filter(AwardQuestions,
                    Category.Id = varCandidateCategory.ID,
                    QuestionSetVersion = varCandidateCategory.PublishedQuestionVersion
                ), "DisplayOrder", SortOrder.Ascending)
            );
            true,
            Set(varLoadOK, false); false
        );
        If(!varLoadOK || IsBlank(varCandidateCategory.ID) || !varCandidateCategory.IsActive ||
           varCandidateCategory.AwardType.Value <> varAwardType ||
           Switch(varCandidateCategory.CategoryCode,
             "IND_INNOVATION", "Individual", "IND_CUSTOMER", "Individual", "IND_EXCELLENCE", "Individual",
             "TEAM_COLLAB", "Team", "TEAM_IMPACT", "Team", "TEAM_TRANSFORM", "Team", "") <> varAwardType ||
           Coalesce(varCandidateCategory.PublishedQuestionVersion, 0) < 1 ||
           CountRows(colCandidateQuestions) < 3 || CountRows(colCandidateQuestions) > 6 ||
           CountRows(Distinct(colCandidateQuestions, DisplayOrder)) <> CountRows(colCandidateQuestions) ||
           CountIf(colCandidateQuestions,
               DisplayOrder < 1 || DisplayOrder > CountRows(colCandidateQuestions) ||
               DisplayOrder <> RoundDown(DisplayOrder, 0) ||
               QuestionKey.Value <> "Q" & Text(DisplayOrder) ||
               ConfigurationKey <> varCandidateCategory.CategoryCode & "-V" & Text(QuestionSetVersion) & "-" & QuestionKey.Value ||
               IsBlank(Trim(Title)) || Char(10) in Title ||
               IsBlank(Trim(Substitute(Substitute(Substitute(QuestionText,Char(10)," "),Char(13)," "),Char(9)," ")))
           ) > 0,
            Set(varIsBusy, false);
            Notify("This category does not have a valid published set of 3–6 questions. Contact the configuration manager.", NotificationType.Error),
            Set(varCategory, varCandidateCategory);
            Set(varQuestionVersion, varCandidateCategory.PublishedQuestionVersion);
            Set(varQuestionCount, CountRows(colCandidateQuestions));
            ClearCollect(colAnswers,
                ForAll(Sequence(6) As n,
                    With({q: LookUp(colCandidateQuestions, DisplayOrder = n.Value)},
                        {Slot: n.Value,
                         Prompt: If(n.Value <= varQuestionCount,
                             q.Title & Char(10) & q.QuestionText &
                             If(IsBlank(q.GuidanceText), "", Char(10) & Char(10) & "Guidance: " & q.GuidanceText), ""),
                         Required: If(n.Value <= varQuestionCount, q.IsRequired, false),
                         Response: ""}
                    )
                )
            );
            Set(varCategoryComplete, true);
            Set(varResponsesComplete, false);
            Set(varDeclarationAccepted, false);
            Set(varHasChanges, true);
            Set(varShowCategoryChangeDialog, false);
            ResetForm(frmBestInnovatorIndividual); NewForm(frmBestInnovatorIndividual);
            ResetForm(frmMDAward); NewForm(frmMDAward);
            ResetForm(frmTrendMarcherAward); NewForm(frmTrendMarcherAward);
            ResetForm(frmBestInnovatorTeam); NewForm(frmBestInnovatorTeam);
            ResetForm(frmMDAwardTeam); NewForm(frmMDAwardTeam);
            ResetForm(frmSpecialTeamAward); NewForm(frmSpecialTeamAward);
            Set(varIsBusy, false);
            Set(varCurrentStep, 3);
            Switch(varCategory.CategoryCode,
    "IND_INNOVATION", Navigate(scrBestInnovatorIndividual, ScreenTransition.None),
    "IND_CUSTOMER", Navigate(scrMDAward, ScreenTransition.None),
    "IND_EXCELLENCE", Navigate(scrTrendMarcherAward, ScreenTransition.None),
    "TEAM_COLLAB", Navigate(scrBestInnovatorTeam, ScreenTransition.None),
    "TEAM_IMPACT", Navigate(scrMDAwardTeam, ScreenTransition.None),
    "TEAM_TRANSFORM", Navigate(scrSpecialTeamAward, ScreenTransition.None),
    Notify("This category has no configured form.", NotificationType.Error)
)
        )
    )
)
```


### Return to the existing active form without resetting it

```powerfx
Switch(varCategory.CategoryCode,
    "IND_INNOVATION", Navigate(scrBestInnovatorIndividual, ScreenTransition.None),
    "IND_CUSTOMER", Navigate(scrMDAward, ScreenTransition.None),
    "IND_EXCELLENCE", Navigate(scrTrendMarcherAward, ScreenTransition.None),
    "TEAM_COLLAB", Navigate(scrBestInnovatorTeam, ScreenTransition.None),
    "TEAM_IMPACT", Navigate(scrMDAwardTeam, ScreenTransition.None),
    "TEAM_TRANSFORM", Navigate(scrSpecialTeamAward, ScreenTransition.None),
    Notify("This category has no configured form.", NotificationType.Error)
)
```


### Review screen Submit button OnSelect

```powerfx
If(!varIsBusy && !varReadOnly,
    If(!DetailsValid || !ResponsesValid || !varCategoryComplete || !varDeclarationAccepted,
        Notify("Review the required information and accept the declaration before submitting.", NotificationType.Warning),
        Switch(varCategory.CategoryCode,
    "IND_INNOVATION",
Set(varIsBusy, true);
Set(varPreflightOK, true);
If(!IsBlank(varNominationId),
    IfError(
        Refresh(BestInnovatorIndividual);
        Set(varLatestII, LookUp(BestInnovatorIndividual, ID = varNominationId));
        If(IsBlank(varLatestII.ID) ||
           varLatestII.NominationStatus.Value <> "Draft" ||
           varLatestII.Modified <> varLoadedModified,
            Set(varPreflightOK, false);
            Notify("This item changed or is no longer an editable draft. Keep a copy of your changes, then reopen it from My nominations.", NotificationType.Error)
        );
        true,
        Set(varPreflightOK, false);
        Notify("Could not check the saved draft. Your changes have been retained; try again when connected.", NotificationType.Error);
        false
    )
);
If(varPreflightOK,
    Set(varSaveIntent, "Submit");
    SubmitForm(frmBestInnovatorIndividual),
    Set(varIsBusy, false)
),
    "IND_CUSTOMER",
Set(varIsBusy, true);
Set(varPreflightOK, true);
If(!IsBlank(varNominationId),
    IfError(
        Refresh(MDAward);
        Set(varLatestIC, LookUp(MDAward, ID = varNominationId));
        If(IsBlank(varLatestIC.ID) ||
           varLatestIC.NominationStatus.Value <> "Draft" ||
           varLatestIC.Modified <> varLoadedModified,
            Set(varPreflightOK, false);
            Notify("This item changed or is no longer an editable draft. Keep a copy of your changes, then reopen it from My nominations.", NotificationType.Error)
        );
        true,
        Set(varPreflightOK, false);
        Notify("Could not check the saved draft. Your changes have been retained; try again when connected.", NotificationType.Error);
        false
    )
);
If(varPreflightOK,
    Set(varSaveIntent, "Submit");
    SubmitForm(frmMDAward),
    Set(varIsBusy, false)
),
    "IND_EXCELLENCE",
Set(varIsBusy, true);
Set(varPreflightOK, true);
If(!IsBlank(varNominationId),
    IfError(
        Refresh(TrendMarcherAward);
        Set(varLatestIE, LookUp(TrendMarcherAward, ID = varNominationId));
        If(IsBlank(varLatestIE.ID) ||
           varLatestIE.NominationStatus.Value <> "Draft" ||
           varLatestIE.Modified <> varLoadedModified,
            Set(varPreflightOK, false);
            Notify("This item changed or is no longer an editable draft. Keep a copy of your changes, then reopen it from My nominations.", NotificationType.Error)
        );
        true,
        Set(varPreflightOK, false);
        Notify("Could not check the saved draft. Your changes have been retained; try again when connected.", NotificationType.Error);
        false
    )
);
If(varPreflightOK,
    Set(varSaveIntent, "Submit");
    SubmitForm(frmTrendMarcherAward),
    Set(varIsBusy, false)
),
    "TEAM_COLLAB",
Set(varIsBusy, true);
Set(varPreflightOK, true);
If(!IsBlank(varNominationId),
    IfError(
        Refresh(BestInnovatorTeam);
        Set(varLatestTC, LookUp(BestInnovatorTeam, ID = varNominationId));
        If(IsBlank(varLatestTC.ID) ||
           varLatestTC.NominationStatus.Value <> "Draft" ||
           varLatestTC.Modified <> varLoadedModified,
            Set(varPreflightOK, false);
            Notify("This item changed or is no longer an editable draft. Keep a copy of your changes, then reopen it from My nominations.", NotificationType.Error)
        );
        true,
        Set(varPreflightOK, false);
        Notify("Could not check the saved draft. Your changes have been retained; try again when connected.", NotificationType.Error);
        false
    )
);
If(varPreflightOK,
    Set(varSaveIntent, "Submit");
    SubmitForm(frmBestInnovatorTeam),
    Set(varIsBusy, false)
),
    "TEAM_IMPACT",
Set(varIsBusy, true);
Set(varPreflightOK, true);
If(!IsBlank(varNominationId),
    IfError(
        Refresh(MDAwardTeam);
        Set(varLatestTI, LookUp(MDAwardTeam, ID = varNominationId));
        If(IsBlank(varLatestTI.ID) ||
           varLatestTI.NominationStatus.Value <> "Draft" ||
           varLatestTI.Modified <> varLoadedModified,
            Set(varPreflightOK, false);
            Notify("This item changed or is no longer an editable draft. Keep a copy of your changes, then reopen it from My nominations.", NotificationType.Error)
        );
        true,
        Set(varPreflightOK, false);
        Notify("Could not check the saved draft. Your changes have been retained; try again when connected.", NotificationType.Error);
        false
    )
);
If(varPreflightOK,
    Set(varSaveIntent, "Submit");
    SubmitForm(frmMDAwardTeam),
    Set(varIsBusy, false)
),
    "TEAM_TRANSFORM",
Set(varIsBusy, true);
Set(varPreflightOK, true);
If(!IsBlank(varNominationId),
    IfError(
        Refresh(SpecialTeamAward);
        Set(varLatestTT, LookUp(SpecialTeamAward, ID = varNominationId));
        If(IsBlank(varLatestTT.ID) ||
           varLatestTT.NominationStatus.Value <> "Draft" ||
           varLatestTT.Modified <> varLoadedModified,
            Set(varPreflightOK, false);
            Notify("This item changed or is no longer an editable draft. Keep a copy of your changes, then reopen it from My nominations.", NotificationType.Error)
        );
        true,
        Set(varPreflightOK, false);
        Notify("Could not check the saved draft. Your changes have been retained; try again when connected.", NotificationType.Error);
        false
    )
);
If(varPreflightOK,
    Set(varSaveIntent, "Submit");
    SubmitForm(frmSpecialTeamAward),
    Set(varIsBusy, false)
),
            Notify("The selected category has no configured form.", NotificationType.Error)
        )
    )
)
```


### Question administration copy/load button OnSelect

```powerfx
If(varCanManageQuestions && !varIsBusy,
    Set(varIsBusy, true);
    Set(varAdminLoadOK, true);
    IfError(
        Refresh(AwardCategories); Refresh(AwardQuestions);
        Set(varAdminCategory, LookUp(AwardCategories, ID = cmbAdminCategory.Selected.ID));
        Set(varAdminBaseVersion, Coalesce(varAdminCategory.PublishedQuestionVersion, 0));
        Set(varAdminHighestVersion,
            Coalesce(First(SortByColumns(
                Filter(AwardQuestions, Category.Id = varAdminCategory.ID),
                "QuestionSetVersion", SortOrder.Descending
            )).QuestionSetVersion, 0)
        );
        Set(varAdminNewVersion, varAdminHighestVersion + 1);
        Set(varAdminSourceVersion, If(varAdminBaseVersion > 0, varAdminBaseVersion, varAdminHighestVersion));
        ClearCollect(colAdminSource, SortByColumns(Filter(AwardQuestions,
            Category.Id = varAdminCategory.ID, QuestionSetVersion = varAdminSourceVersion
        ), "DisplayOrder", SortOrder.Ascending));
        If(CountRows(colAdminSource) = 0,
            ClearCollect(colAdminQuestions, ForAll(Sequence(3) As n,
                {Slot: n.Value, Title: "", QuestionText: "", GuidanceText: "", IsRequired: true})),
            ClearCollect(colAdminQuestions, ForAll(colAdminSource As q,
                {Slot: q.DisplayOrder, Title: q.Title, QuestionText: q.QuestionText,
                 GuidanceText: Coalesce(q.GuidanceText, ""), IsRequired: q.IsRequired}))
        );
        Set(varAdminDirty, false);
        true,
        Set(varAdminLoadOK, false);
        Notify("Unable to load the configuration. Nothing has been published.", NotificationType.Error);
        false
    );
    Set(varIsBusy, false)
)
```


### Question administration Publish button OnSelect

```powerfx
If(varCanManageQuestions && varAdminLoadOK && !varIsBusy,
    ClearCollect(colAdminEdits, ForAll(galAdminQuestions.AllItems As row,
        {Slot: row.Slot, Title: row.txtAdminTitle.Text,
         QuestionText: row.txtAdminQuestion.Text, GuidanceText: row.txtAdminGuidance.Text,
         IsRequired: row.chkAdminRequired.Value}));
    ForAll(colAdminEdits As edit,
        Patch(colAdminQuestions, LookUp(colAdminQuestions, Slot = edit.Slot),
            {Title: edit.Title, QuestionText: edit.QuestionText,
             GuidanceText: edit.GuidanceText, IsRequired: edit.IsRequired}));
    If(IsBlank(varAdminCategory.ID) || varAdminNewVersion <= varAdminBaseVersion ||
       CountRows(colAdminQuestions) < 3 || CountRows(colAdminQuestions) > 6 ||
       CountRows(Distinct(colAdminQuestions, Slot)) <> CountRows(colAdminQuestions) ||
       CountIf(colAdminQuestions,
           Slot < 1 || Slot > CountRows(colAdminQuestions) || Slot <> RoundDown(Slot, 0) ||
           IsBlank(Trim(Title)) || Len(Title) > 255 || Char(10) in Title ||
           IsBlank(Trim(Substitute(Substitute(Substitute(QuestionText,Char(10)," "),Char(13)," "),Char(9)," ")))
       ) > 0,
        Notify("Supply 3–6 ordered questions, each with a one-line title and question text.", NotificationType.Warning),
        Set(varIsBusy, true);
        Clear(colPublishErrors);
        Set(varPublishOK, true);
        IfError(
            Refresh(AwardCategories);
            Set(varAdminLatestCategory, LookUp(AwardCategories, ID = varAdminCategory.ID));
            If(Coalesce(varAdminLatestCategory.PublishedQuestionVersion, 0) <> varAdminBaseVersion,
                Set(varPublishOK, false);
                Notify("Another version has been published. Reload before making further changes.", NotificationType.Error)
            );
            true,
            Set(varPublishOK, false); false
        );
        If(varPublishOK,
            IfError(
                ForAll(colAdminQuestions As q,
                    With({keyText: varAdminCategory.CategoryCode & "-V" & Text(varAdminNewVersion) & "-Q" & Text(q.Slot)},
                        IfError(
                            With({existing: LookUp(AwardQuestions, ConfigurationKey = keyText)},
                                If(IsBlank(existing.ID),
                                    Patch(AwardQuestions, Defaults(AwardQuestions),
                                        {Title: q.Title,
                                         Category: {Id: varAdminCategory.ID, Value: varAdminCategory.Title},
                                         QuestionSetVersion: varAdminNewVersion,
                                         QuestionKey: {Value: "Q" & Text(q.Slot)},
                                         QuestionText: q.QuestionText, GuidanceText: q.GuidanceText,
                                         DisplayOrder: q.Slot, IsRequired: q.IsRequired,
                                         ConfigurationKey: keyText}
                                    ); true,
                                    existing.Category.Id = varAdminCategory.ID &&
                                    existing.QuestionSetVersion = varAdminNewVersion &&
                                    existing.QuestionKey.Value = "Q" & Text(q.Slot) &&
                                    existing.Title = q.Title && existing.QuestionText = q.QuestionText &&
                                    Coalesce(existing.GuidanceText, "") = q.GuidanceText &&
                                    existing.IsRequired = q.IsRequired && existing.DisplayOrder = q.Slot,
                                    true,
                                    Collect(colPublishErrors, {Slot: q.Slot, Message: "This version/key already contains different content. Allocate a new version."}); false
                                )
                            ),
                            Collect(colPublishErrors, {Slot: q.Slot, Message: "Question save failed. Publication was not completed."}); false
                        )
                    )
                ); true,
                Set(varPublishOK, false); false
            );
            If(CountRows(colPublishErrors) > 0, Set(varPublishOK, false));
            If(varPublishOK,
                IfError(
                    Refresh(AwardQuestions);
                    ClearCollect(colAdminSaved,
                        Filter(AwardQuestions, Category.Id = varAdminCategory.ID,
                            QuestionSetVersion = varAdminNewVersion));
                    If(CountRows(colAdminSaved) <> CountRows(colAdminQuestions) ||
                       CountIf(colAdminQuestions As q,
                           With({saved: LookUp(colAdminSaved, QuestionKey.Value = "Q" & Text(q.Slot))},
                               IsBlank(saved.ID) || saved.DisplayOrder <> q.Slot ||
                               saved.Title <> q.Title || saved.QuestionText <> q.QuestionText ||
                               Coalesce(saved.GuidanceText, "") <> q.GuidanceText || saved.IsRequired <> q.IsRequired ||
                               saved.ConfigurationKey <> varAdminCategory.CategoryCode & "-V" & Text(varAdminNewVersion) & "-Q" & Text(q.Slot)
                           )
                       ) > 0,
                        Set(varPublishOK, false)
                    ); true,
                    Set(varPublishOK, false); false
                )
            );
            If(varPublishOK,
                IfError(
                    Refresh(AwardCategories);
                    Set(varAdminLatestCategory, LookUp(AwardCategories, ID = varAdminCategory.ID));
                    If(Coalesce(varAdminLatestCategory.PublishedQuestionVersion, 0) <> varAdminBaseVersion,
                        Set(varPublishOK, false),
                        Set(varAdminCategory, Patch(AwardCategories, varAdminLatestCategory,
                            {PublishedQuestionVersion: varAdminNewVersion, IsActive: true}));
                        Set(varAdminBaseVersion, varAdminNewVersion);
                        Set(varAdminDirty, false)
                    ); true,
                    Set(varPublishOK, false); false
                )
            )
        );
        Set(varIsBusy, false);
        If(varPublishOK,
            Notify("Question version " & Text(varAdminNewVersion) & " published and category activated.", NotificationType.Success),
            Notify("Publication was not confirmed. Refresh the category pointer before retrying; retained question rows must not be deleted or overwritten.", NotificationType.Error)
        )
    )
)
```


## Other shared screens

The following sections provide the shared controls and property wiring. They are implementation recipes, not reviewed exports of those screens. Use the exact typed routes above and the six per-form browse/open actions; never replace them with a runtime string data-source variable.


### Step 1 — details; step 2 — category selection

Build the page shell first. These screen controls are shared by all six category forms. A nominee can be entered before selecting a category, but nothing is saved until a category identifies the destination list.

#### 1. Home

Heading: **Employee & Team Recognition Awards** from `Theme.AppTitle`. Add brief instruction text describing the four stages. Add New nomination and My nominations native buttons. New uses `NewNomination.OnSelect.fx`; My uses `Navigate(scrMyNominations,ScreenTransition.None)`. Add Manage questions with Visible `varCanManageQuestions` and OnSelect `Navigate(scrQuestionAdministration,ScreenTransition.None)`. Keep the Home page simple; the supplied nomination design starts with the actual step-1 screen.

#### 2. scrNomineeDetails

OnVisible:

```powerfx
Set(varCurrentStep, 1)
```

Heading “Nominee details”; subtitle “Choose the nomination type and tell us who you are recognizing.” These are UI instructions, not question content. Add white `cntDetailsCard` with the card styling in the layout guide. X/Width match the page heading; Y after subtitle +26. Internal horizontal padding `If(App.Width<=760,17,34)` and top padding `If(App.Width<=760,21,30)`. In the measurements below, `padding` means the expression `If(App.Width<=760,17,34)`, not an undeclared Power Fx variable. Use native controls in the following order. For each successive field label set Y to the previous visible control's Y+Height+18; its input starts at label.Y+label.Height+7. Use zero Height for hidden nominee/team sections so following fields move upward.

##### A. Type cards

Add label “Nomination type”, then `btnIndividualType` and `btnTeamType`, approximately 103px high. Desktop widths `(Min(590,Parent.Width-2*padding)-16)/2`, horizontal gap16; mobile stack, full available width. Use Fill `If(varAwardType="Individual",Theme.Pale,Theme.Surface)` for Individual, analogous Team; BorderColor primary when selected else border; BorderThickness 2 when selected else1; corner radii7. Text “Individual award” / “Team award”, Size12.75, Semibold, Align.Left, PaddingLeft18. A check icon or label with “Selected” is visible only on the selected card.

Individual OnSelect:

```powerfx
If(!varCategoryComplete,
    Set(varAwardType,"Individual");
    Set(varHasChanges,true); Set(varDetailsComplete,false);
    Set(varDeclarationAccepted,false)
)
```

Team OnSelect changes the literal to `"Team"`. DisplayMode for both:

```powerfx
If(varIsBusy || varReadOnly || varCategoryComplete,DisplayMode.Disabled,DisplayMode.Edit)
```

Award type locks once questions have been loaded, even before the first save, to avoid applying team inputs to an individual form. To start a different type after that point, use New nomination and confirm discarding unsaved changes. Before category selection, changing the type may retain hidden in-memory detail values for convenience; only the chosen type is stored by its typed form. There is no silent default category.

##### B. Nominator

Label “Nominated by”; read-only person row Text `User().FullName & Char(10) & varUserEmail`. Width `Min(590,Parent.Width-2*padding)`, Height56, Size9.75, white/pale fill. This is the signed-in nominator, never an editable field. On resumed records the form saves its loaded `varNominator`; My nominations only opens the current user's records.

##### C. Individual nominee — cmbNominee

Visible `varAwardType="Individual"`. Label “Nominee *”. Use a classic single-select Combo box `cmbNominee`, 56px high, width up to590. Apply directory style from the layout guide. Items:

```powerfx
If(Len(Self.SearchText)<2,
    Blank(),
    IfError(Office365Users.SearchUserV2(
        {searchTerm:Self.SearchText,top:25,isSearchTermRequired:true}
    ).value,
        Notify("Directory search failed. Check the directory connection and try again.", NotificationType.Error);
        Blank())
)
```

This is a bounded directory search, not a locally copied directory. Search term and returned field names come from [Office 365 Users SearchUserV2](https://learn.microsoft.com/en-us/connectors/office365users/). Show helper text “Enter at least two characters. If no results appear, refine the search or check the directory connection.” Tenant policies can affect results; test with real authorized accounts.

DefaultSelectedItems:

```powerfx
If(IsBlank(varEmployee.Claims),Blank(),
    Table({DisplayName:varEmployee.DisplayName,Mail:varEmployee.Email,
           UserPrincipalName:Last(Split(varEmployee.Claims,"|")).Value})
)
```

OnChange:

```powerfx
With({u:Self.Selected},
    If(IsBlank(Coalesce(u.UserPrincipalName,u.Mail)),
        Set(varEmployee,varEmptyPerson),
        Set(varEmployee,{
            '@odata.type':"#Microsoft.Azure.Connectors.SharePoint.SPListExpandedUser",
            Claims:"i:0#.f|membership|" & Lower(Coalesce(u.UserPrincipalName,u.Mail)),
            DisplayName:u.DisplayName,Email:Coalesce(u.Mail,u.UserPrincipalName),
            Department:"",JobTitle:"",Picture:""
        })
    )
);
Set(varHasChanges,true); Set(varDetailsComplete,false);
Set(varDeclarationAccepted,false)
```

Use UPN for the membership claim and Mail for display where available; do not assume they are always identical. Test guest identities separately if they will be allowed. The fixed schema does not include a guest/employee eligibility policy.

##### D. Team controls

Put these in manual container `cntTeamDetails` with Visible `varAwardType="Team"`, Height based on its last child. When hidden set its Height to0 so following fields move up. Add:

1. `txtTeamName`, label “Team name *”, Default `varTeamName`, MaxLength255, single-line. OnChange: `Set(varTeamName,Self.Text); Set(varHasChanges,true); Set(varDetailsComplete,false); Set(varDeclarationAccepted,false)`.
2. `cmbPrimaryContact`, label “Primary contact *”. Same directory Items formula and Combo styling as cmbNominee. DefaultSelectedItems uses `varPrimaryContact` instead of `varEmployee`. Its full OnChange is the cmbNominee formula with only `varEmployee` changed to `varPrimaryContact`.
3. `cmbTeamMemberToAdd`, label “Team members (optional)”, same directory Items, DefaultSelectedItems `Blank()`, SelectMultiple false. An Add member button appears alongside it. We use explicit Add/Remove so selected members remain visible even when a new directory search changes the result set.
4. Gallery `galTeamMembers`, Items `colTeamMembers`, TemplateSize40, Height `Min(200,CountRows(colTeamMembers)*40)`, ShowScrollbar true. Labels show ThisItem.DisplayName; remove icon/button OnSelect `Remove(colTeamMembers,ThisItem); Set(varHasChanges,true); Set(varDeclarationAccepted,false)`. Disable removal while busy/read-only.

Add member button OnSelect:

```powerfx
With({u:cmbTeamMemberToAdd.Selected},
    With({claim:"i:0#.f|membership|" & Lower(Coalesce(u.UserPrincipalName,u.Mail))},
        If(!IsBlank(Coalesce(u.UserPrincipalName,u.Mail)) &&
           IsBlank(LookUp(colTeamMembers,Claims=claim)),
            Collect(colTeamMembers,{
                '@odata.type':"#Microsoft.Azure.Connectors.SharePoint.SPListExpandedUser",
                Claims:claim,DisplayName:u.DisplayName,Email:Coalesce(u.Mail,u.UserPrincipalName),
                Department:"",JobTitle:"",Picture:""
            });
            Set(varHasChanges,true); Set(varDeclarationAccepted,false);
            Reset(cmbTeamMemberToAdd)
        )
    )
)
```

Team members are optional and may include the primary contact unless business rules later say otherwise. Do not invent a mandatory team-member count.

##### E. Role and level

Below the visible nominee/team section add `cntRoleLevel`. Width `Min(590,card.Width-2*padding)`. Desktop Height80, mobile Height170. Role label “Nominee role *” for Individual, “Primary contact role *” for Team. Level label likewise. Desktop two columns `(Parent.Width-18)/2`; mobile full width, level starts90px below role.

`txtRole`: Default `varRole`; MaxLength255; Height40. OnChange:

```powerfx
Set(varRole,Self.Text);
Set(varHasChanges,true); Set(varDetailsComplete,false);
Set(varDeclarationAccepted,false)
```

`cmbLevel`: classic Combo, SelectMultiple false; IsSearchable false; DisplayFields `["Value"]`; SearchFields `["Value"]`; Height40; InputTextPlaceholder “Select level”. Items read actual choice metadata:

```powerfx
Switch(varCategory.CategoryCode,
    "IND_CUSTOMER",Choices(MDAward.EmployeeLevel),
    "IND_EXCELLENCE",Choices(TrendMarcherAward.EmployeeLevel),
    "TEAM_COLLAB",Choices(BestInnovatorTeam.EmployeeLevel),
    "TEAM_IMPACT",Choices(MDAwardTeam.EmployeeLevel),
    "TEAM_TRANSFORM",Choices(SpecialTeamAward.EmployeeLevel),
    Choices(BestInnovatorIndividual.EmployeeLevel)
)
```

The same expression is defined centrally as `LevelOptions` in App.Formulas, so you can set Items to `LevelOptions`. Before category selection the IndividualInnovation list supplies the common level choices; maintain identical choice values across all six lists. DefaultSelectedItems `Filter(LevelOptions,Value=varLevel)`. DetailsValid also checks the level is still an allowed choice. OnChange:

```powerfx
Set(varLevel,Coalesce(Self.Selected.Value,""));
Set(varHasChanges,true); Set(varDetailsComplete,false);
Set(varDeclarationAccepted,false)
```

Below controls show a muted helper: “Required details are needed before review. You can select a category and save an incomplete draft.” `cntDetailsCard.Height` = last helper Y + Height +30; action row below card+24. Continue OnSelect is [Details.Continue.OnSelect.fx](documentation/manual-build/Details.Continue.OnSelect.fx). It captures text values directly, then goes to category selection, or back to the existing form when a category is already loaded. Continue is allowed with incomplete details **to permit incomplete drafts**; review is not. Save draft is not present on this screen because a new record may not yet have a destination.

#### 3. scrCategorySelection

OnVisible:

```powerfx
Set(varCurrentStep,2);
Set(varCategoryLoadError,false);
IfError(
    Refresh(AwardCategories);
    ClearCollect(colCategoryOptions,SortByColumns(
        Filter(AwardCategories,IsActive=true,AwardType.Value=varAwardType),
        "DisplayOrder",SortOrder.Ascending));
    true,
    Set(varCategoryLoadError,true);
    Clear(colCategoryOptions);
    false
)
```

This collection is the bounded category configuration (three categories per type), not nomination data. Add heading “Award category” and subtitle “Choose the category that best matches the nomination.” Add a summary strip with current nominee/type. Back OnSelect `Navigate(scrNomineeDetails,ScreenTransition.None)`.

##### A. Category cards

Insert vertical gallery `galCategories` with Items `colCategoryOptions`. Set WrapCount `If(App.Width<=760,1,3)`, TemplatePadding8, TemplateSize261, Width equal to page inner width. Height `If(App.Width<=760,CountRows(colCategoryOptions)*261,261)`. Remove generated image/body controls. Inside each item add a manual container Width `Parent.TemplateWidth-16`, Height245, X8, Y8, Fill `If(ThisItem.ID=varPendingCategory.ID,Theme.Pale,Theme.Surface)`, BorderColor primary if selected else border, BorderThickness2 if selected else1, corner radii8.

Add a small native icon in a 43px pale square, heading Title label X20 Y78 WidthParent.Width-40 AutoHeight Size12.75 Semibold, description X20 Yheadingbottom+10 WidthParent.Width-40 AutoHeight Size9.75, and Selected indicator in top right. Icons can be stable per category code, but text/order/availability come from SharePoint. As a baseline use the same award SVG for all categories; icon differences are cosmetic and do not require new columns. Verify long descriptions fit; increase card/gallery row height together if business copy is longer.

Add a native transparent selection button within the gallery template, outside the decorative container so `ThisItem` is the gallery item. X/Y8, WidthParent.TemplateWidth-16, Height245, Text `""`, AccessibleLabel `"Select " & ThisItem.Title`. OnSelect:

```powerfx
Set(varPendingCategory,ThisItem)
```

Use a clearly visible focus border. DisplayMode disabled when busy or when a nomination has already been saved. A saved record never changes category/version through this screen.

Empty-state label Visible `!varCategoryLoadError && IsEmpty(colCategoryOptions)`, Text “No categories are currently published for this nomination type.” Error label Visible varCategoryLoadError, Text “Categories could not be loaded. Check the connection and try again.” Add Retry `Select(btnRefreshCategories)` only if a same-screen hidden button holds the OnVisible refresh code; alternatively paste that refresh block directly into Retry. Do not make an empty state look like a loading spinner indefinitely.

##### B. Load the selected question version

Add same-screen hidden `btnLoadCategory`, DisplayMode.Edit, OnSelect the full [Category.Load.OnSelect.fx](documentation/manual-build/Category.Load.OnSelect.fx). It re-reads the selected category/published pointer and validates 3–6 ordered Q1..QN rows before initializing snapshots. Changing an unsaved selection resets all form controls and queued evidence **only after confirmation and successful configuration validation**. Returning to the same selected category preserves current answers and attachments.

Continue DisplayMode:

```powerfx
If(varIsBusy || IsBlank(varPendingCategory.ID) || !IsBlank(varNominationId),
    DisplayMode.Disabled,DisplayMode.Edit)
```

Continue OnSelect:

```powerfx
If(varCategoryComplete && varPendingCategory.ID<>varCategory.ID,
    Set(varShowCategoryChangeDialog,true),
    Select(btnLoadCategory)
)
```

Add a modal dialog Visible `varShowCategoryChangeDialog`: “Changing category clears the current responses and selected evidence. Nominee details will be retained.” Cancel `Set(varShowCategoryChangeDialog,false)`. Confirm `Select(btnLoadCategory)`. Disable both while busy. Configuration errors retain the old answers and let the user cancel the dialog.

On each step-3 form, add Change category button Visible `!varReadOnly && IsBlank(varNominationId)`, OnSelect:

```powerfx
Set(varPendingCategory,varCategory);
Set(varDeclarationAccepted,false);
Navigate(scrCategorySelection,ScreenTransition.None)
```

No new snapshot is fetched when resuming a saved draft; use the per-category gallery Open formula instead. Seed rows remain inactive until an approved administrator publishes them. The UI must not automatically substitute prototype questions when no published configuration exists.

Continue with the six [typed form recipes](documentation/manual-build/Form-Mapping.md), then [review, browse and administration](documentation/manual-build/03-Review-Browse-and-Administration.md).

### Review, submission, My nominations and administration

Finish all six typed forms first. This chapter references their exact names. Submission is asynchronous: the active form saves the Draft and files; its OnSuccess then updates that same saved item to Submitted. Do not put a status Patch immediately after SubmitForm in the button formula. [Microsoft form functions](https://learn.microsoft.com/en-us/power-platform/power-fx/reference/function-form).

#### 1. scrReview

Use the 960px centered page shell. OnVisible:

```powerfx
Set(varCurrentStep,4)
```

Heading “Review & submit”; subtitle “Check the nomination and supporting evidence before submitting.” Step-3 Review buttons already validate required details/responses and capture text controls directly into colAnswers, plus filenames into colReviewFiles. They reset declaration each time. Never re-query nomination answers from SharePoint for this review; that would omit current unsaved changes.

##### A. Details summary

Add white `cntReviewDetails`, X/Width same as page heading, Y after subtitle+26, padding28. Add `lblReviewDetails` X28 Y24 WidthParent.Width-56, AutoHeight true, Size9.75, Text:

```powerfx
"Nomination type: " & varAwardType & Char(10) &
"Category: " & varCategory.Title & Char(10) &
"Nominated by: " & varNominator.DisplayName & Char(10) &
If(varAwardType="Individual",
    "Nominee: " & varEmployee.DisplayName,
    "Team: " & varTeamName & Char(10) &
    "Primary contact: " & varPrimaryContact.DisplayName & Char(10) &
    "Team members: " & If(IsEmpty(colTeamMembers),"None added",Concat(colTeamMembers,DisplayName,", "))
) & Char(10) &
"Role: " & varRole & Char(10) & "Level: " & varLevel & Char(10) &
"Question version: " & Text(varQuestionVersion)
```

For closer desktop fidelity, split this label into two columns of the same fields: left nominee/type/nominator, right category/role/level. Use 18px vertical and50px horizontal gaps; stack at760px. The one-label formula above is the simplest complete accessible fallback and preserves all information without clipping.

Add Edit details native button X28, Y `lblReviewDetails.Y+lblReviewDetails.Height+16`, Width120, Height38. OnSelect:

```powerfx
Set(varDeclarationAccepted,false);
Navigate(scrNomineeDetails,ScreenTransition.None)
```

cntReviewDetails.Height = edit button Y+Height+24. Do not auto-reset form controls when entering details; the following Continue goes back to the existing typed form, preserving queued files.

##### B. All questions and answers

Build the six expanding read-only blocks exactly as [Review-Question-Controls.md](documentation/manual-build/Review-Question-Controls.md). Prompts/answers are dynamic snapshots, not hardcoded category text. All answer labels have AutoHeight true. The source prototype's five-line clipping is deliberately not carried over: the user must see the entire answer before accepting the declaration.

##### C. Evidence review

Add `cntReviewEvidence` after the final question block, same X/Width, white card, padding28. Heading “Supporting evidence”. Add Label `lblReviewFiles`, X28 Y58 WidthParent.Width-56, AutoHeight true, Text:

```powerfx
If(IsEmpty(colReviewFiles),"No files attached.",Concat(colReviewFiles,FileName,Char(10)))
```

This is the pending attachment filename list captured from the current native form. Files are not uploaded until SubmitForm. To inspect/add/remove evidence, return to the original form. Add Edit responses and evidence button below this label; OnSelect:

```powerfx
Set(varDeclarationAccepted,false);
```

Immediately after that statement paste the full action block from [Navigate-Active-Form.fx](documentation/manual-build/Navigate-Active-Form.fx). Do not call NewForm/ResetForm. Set cntReviewEvidence.Height to edit button Y+Height+24.

##### D. Declaration and Submit

Add a white declaration card below evidence+18, same X/Width. Classic Checkbox `chkDeclaration`, X20 Y16 WidthParent.Width-40 Height80 (increase if text wraps on mobile), Text “I confirm that the information in this nomination is accurate and appropriate to submit.” This is proposed UI wording; replace with the approved declaration before release. Default `varDeclarationAccepted`; OnCheck `Set(varDeclarationAccepted,true)`; OnUncheck `Set(varDeclarationAccepted,false)`; DisplayMode disabled while varIsBusy.

Add helper label: “Submitting saves this nomination. Submitted nominations are read-only in this app.” Do not claim a notification email was sent; no notification flow is included. Card Height = checkbox Y+Height+helper Height+28.

Below add Back and Submit nomination buttons. Back resets declaration then uses Navigate-Active-Form.fx. Submit.OnSelect is the complete [Review.Submit.OnSelect.fx](documentation/manual-build/Review.Submit.OnSelect.fx). Submit.DisplayMode:

```powerfx
If(varIsBusy || varReadOnly || !varDeclarationAccepted ||
   !DetailsValid || !ResponsesValid || !varCategoryComplete,
   DisplayMode.Disabled,DisplayMode.Edit)
```

The file contains all six routing branches, fresh saved-item status/Modified checks, SaveIntent and SubmitForm calls. Each form's OnSuccess captures LastSubmit/ID, sets EditForm for subsequent saves, and performs the final status update only when SaveIntent is Submit. The busy state remains true through both phases. Navigation to confirmation occurs only in the successful status-update branch.

If the final status update fails, the first save has already returned an ID. Retain that ID, show the failure and check the current server status before retrying. A network timeout can make the outcome uncertain even if the server committed; do not promise that such an item definitely remains a Draft. Likewise, if the initial new-item SubmitForm times out before LastSubmit is returned, check My nominations before retrying creation. The fixed schema has no client-generated idempotency key, so exactly-once creation under an ambiguous network failure cannot be guaranteed by these client formulas.

#### 2. scrConfirmation

Use the page shell without stepper. Center a white card Width `Min(640,parent.Width-32)`, X centered, Y48, padding32. Add native success icon/circle, heading “Nomination submitted”, and labels:

| Label | Text |
|---|---|
| Reference | `NominationReference` |
| Category | `varCategory.Title` |
| Nominee/team | `NomineeDisplay` |
| Time | `Text(varSubmittedOn,"dd mmm yyyy, hh:mm")` |

Time is displayed in the app user's local context; SharePoint stores the underlying date/time. Add View nomination with OnSelect the full Navigate-Active-Form block. Forms have already been placed in View mode by successful submission. Add My nominations → Navigate(scrMyNominations); New nomination → full NewNomination block. No fabricated nominee/reference/date should appear here.

#### 3. scrMyNominations

Heading “My nominations”, subtitle “View your submitted nominations or continue a draft.” No stepper. The original all-category prototype list is implemented as a category-selected view to preserve delegation across six physical lists. Do not merge all nominations using ClearCollect/ForAll and assume it is complete.

##### A. Screen refresh and filters

OnVisible:

```powerfx
Set(varBrowseError,false);
IfError(
    Refresh(AwardCategories);
    ClearCollect(colBrowseCategories,SortByColumns(AwardCategories,"DisplayOrder",SortOrder.Ascending));
    Switch(varBrowseCode,
        "IND_INNOVATION",Refresh(BestInnovatorIndividual),
        "IND_CUSTOMER",Refresh(MDAward),
        "IND_EXCELLENCE",Refresh(TrendMarcherAward),
        "TEAM_COLLAB",Refresh(BestInnovatorTeam),
        "TEAM_IMPACT",Refresh(MDAwardTeam),
        "TEAM_TRANSFORM",Refresh(SpecialTeamAward)
    ); true,
    Set(varBrowseError,true); false
)
```

Add Individual and Team type buttons. Individual.OnSelect:

```powerfx
Set(varBrowseType,"Individual");
Set(varBrowseCode,First(Filter(colBrowseCategories,AwardType.Value="Individual")).CategoryCode);
Set(varBrowseId,0); Reset(txtBrowseId)
```

Team uses `"Team"` in both places. Add classic Combo `cmbBrowseCategory`, Items `Filter(colBrowseCategories,AwardType.Value=varBrowseType)`, DisplayFields `["Title"]`, SelectMultiple false, IsSearchable false, DefaultSelectedItems `Filter(colBrowseCategories,CategoryCode=varBrowseCode)`. OnChange `Set(varBrowseCode,Self.Selected.CategoryCode); Set(varBrowseId,0); Reset(txtBrowseId)`. Include inactive categories so old nominations remain discoverable.

Status Dropdown `ddBrowseStatus`, Items `["All","Draft","Submitted"]`, Default `"All"`, OnChange `Set(varBrowseStatus,Self.Selected.Value)`.

Optional exact item-ID input `txtBrowseId`: label “Find item ID in this category”, Default `""`, Format `TextFormat.Number`, HintText “For example, 42”. OnChange:

```powerfx
If(IsBlank(Trim(Self.Text)),
    Set(varBrowseId,0),
    If(IsNumeric(Self.Text) && Value(Self.Text)>0 && Value(Self.Text)=RoundDown(Value(Self.Text),0),
        Set(varBrowseId,Value(Self.Text)),
        Notify("Enter a positive whole item ID.",NotificationType.Warning);
        Set(varBrowseId,0); Reset(txtBrowseId)
    )
)
```

The derived reference includes the category code plus this numeric ID. This is an exact lookup, not a promised full-text search over six lists. Add explicit Refresh button with the same selected-source Switch inside IfError as OnVisible; it does not reset the current filters.

##### B. Six galleries, one visible

Create `galMineII`, `galMineIC`, `galMineIE`, `galMineTC`, `galMineTI`, `galMineTT` at identical X/Y/Width/Height below the filters. Set their Items/Visible/Open buttons from the corresponding Form-CODE.md file. They query their actual typed source directly. Do not collect their results into a common unbounded table. Use a vertical gallery, TemplatePadding0, TemplateSize `If(App.Width<=760,150,76)`, Height `Max(280,App.Height-cntScrollMine.Y-Self.Y-56)`, ShowScrollbar true. The enclosing page height should end just below the gallery.

Desktop columns: Reference x16 width190; Nominee/team x216 width `Max(120,Parent.TemplateWidth-570)`; Modified x `Parent.TemplateWidth-330` width150; status x `Parent.TemplateWidth-170` width90; Open x `Parent.TemplateWidth-78` width62. On mobile stack reference y12, nominee y38, date/status y66, Open y102. Use native labels with Size9.75, truncate only the list summary if needed; full values display on opening. Status pill Fill pale green for Submitted, pale blue for Draft; show the status word as well as color. Draw a 1px bottom rule.

Each form recipe supplies the complete gallery Open.OnSelect: it refreshes and re-reads the clicked ID owned by the current user, loads saved snapshots and people, and opens Draft in EditForm or Submitted in ViewForm. It does not reinitialize questions from today's published configuration.

Empty label per gallery Visible `thatGallery.Visible && !varBrowseError && IsEmpty(thatGallery.AllItems)`, Text “No nominations match this selection.” Hide or replace this label while that gallery is loading. Error banner Visible varBrowseError. A missing result after a connection error must not be presented as a confirmed empty list.

Filtering by indexed NominatorEmail, Choice.Value and equality ID is designed to delegate; verify blue delegation warnings and test with more records than the configured data row limit. SharePoint permits only certain operators for complex fields and ID. [Microsoft SharePoint delegation table](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/connections/connection-sharepoint-online). If Studio flags the constant OR filters, rewrite as explicit If branches for All/exact status and zero/exact ID, each branch returning a direct Filter/SortByColumns on the same source; do not increase the row limit as a substitute.

#### 4. scrQuestionAdministration

This stage is included so question wording, guidance, required flags and count stay dynamic. Publication is a deliberate administrator action and activates the category. Do not publish the current seed wording/levels until approved for the intended development or production use. The guide itself does not change the live publication state.

Use the page shell without stepper; heading “Manage award questions”. The main editing container Visible `varCanManageQuestions`. If false, show “You do not have access to question administration” plus a Home button. All load/publish handlers also check the flag, but **the real write restriction is SharePoint permissions**, not this variable.

OnVisible:

```powerfx
If(varCanManageQuestions,
    IfError(
        Refresh(AwardCategories);
        ClearCollect(colAdminCategories,SortByColumns(AwardCategories,"DisplayOrder",SortOrder.Ascending));
        true,
        Notify("Could not load categories.",NotificationType.Error); false
    )
)
```

##### A. Category and new version

Add `cmbAdminCategory`: Items colAdminCategories; DisplayFields `["Title"]`; SelectMultiple false; IsSearchable false. Add label displaying loaded category, published version and editing version:

```powerfx
Coalesce(varAdminCategory.Title,"No category loaded") &
"  • Published: " & Text(varAdminBaseVersion) &
"  • Editing new version: " & Text(varAdminNewVersion)
```

Add hidden local button `btnAdminLoadCopy`, OnSelect full [Admin.LoadCopy.OnSelect.fx](documentation/manual-build/Admin.LoadCopy.OnSelect.fx). Visible button “Copy to new version” has DisplayMode disabled when no selected ID or busy. OnSelect:

```powerfx
If(varAdminDirty,
    Set(varShowAdminDiscard,true),
    Select(btnAdminLoadCopy)
)
```

Add dialog Visible varShowAdminDiscard, text “Discard local question edits and load the selected category?”. Cancel sets false; Confirm sets false then Select(btnAdminLoadCopy). Initialize varShowAdminDiscard false in App.OnStart. The load code selects the current published version, or highest staged version when none is published; it allocates highest existing version+1. It never edits a previously saved question row. Test delegation for the filtered/sorted highest-version query before relying on a long version history. It assumes a coordinated single publisher per category; it is not a distributed version allocator.

##### B. Editor gallery

Use a vertical gallery `galAdminQuestions`, Items `Sort(colAdminQuestions,Slot,SortOrder.Ascending)`, TemplateSize440, TemplatePadding12, Height `Min(1000,CountRows(colAdminQuestions)*440)`. At 390px use TemplateSize520. Keep the gallery scrollable and the Publish/Preview buttons visible below or in a sticky action area.

Inside each template create the following controls with **these exact names** (gallery controls have one name reused across rows):

| Control | Core properties |
|---|---|
| Slot label | Text `"Q" & Text(ThisItem.Slot)`; X16 Y12; Height24; Semibold |
| `txtAdminTitle` | Default `ThisItem.Title`; X16 Y48; WidthParent.TemplateWidth-32; Height40; MaxLength255; single-line; accessible label “Criterion title” |
| `txtAdminQuestion` | Default `ThisItem.QuestionText`; X16 Y110; Width same; Height120; Mode TextMode.MultiLine; accessible label “Question text” |
| `txtAdminGuidance` | Default `ThisItem.GuidanceText`; X16 Y254; Width same; Height100; Mode TextMode.MultiLine; accessible label “Optional guidance” |
| `chkAdminRequired` | Default `ThisItem.IsRequired`; X16 Y374; Height40; Text “Required response” |

Add native field labels in the gaps above the text inputs; on mobile expand TemplateSize/positions as needed to avoid overlaps. Text controls DelayOutput false, DisplayMode disabled while busy. Each OnChange patches only the local collection:

```powerfx
// txtAdminTitle.OnChange
Patch(colAdminQuestions,LookUp(colAdminQuestions,Slot=ThisItem.Slot),{Title:Self.Text});
Set(varAdminDirty,true)
```

txtAdminQuestion uses `{QuestionText:Self.Text}`; txtAdminGuidance uses `{GuidanceText:Self.Text}`. Checkbox OnCheck uses `{IsRequired:true}`, OnUncheck `{IsRequired:false}`, followed by Set(varAdminDirty,true). No SharePoint writes occur while typing. Unlike employee responses, this is a bounded administrator editor with at most six rows. The Publish action also captures currently realized editor values before validating to avoid losing a last focused edit.

Add question button DisplayMode disabled if CountRows(colAdminQuestions)>=6 or busy; OnSelect:

```powerfx
If(CountRows(colAdminQuestions)<6,
    Collect(colAdminQuestions,{Slot:CountRows(colAdminQuestions)+1,Title:"",QuestionText:"",GuidanceText:"",IsRequired:true});
    Set(varAdminDirty,true)
)
```

Remove last question button disabled at<=3; OnSelect:

```powerfx
If(CountRows(colAdminQuestions)>3,
    With({lastSlot:Max(colAdminQuestions,Slot)},RemoveIf(colAdminQuestions,Slot=lastSlot));
    Set(varAdminDirty,true)
)
```

Removing only the last local slot keeps Q1..QN contiguous. To reorder content, edit the local slots' contents; do not renumber published rows or change ConfigurationKey. No saved SharePoint rows are deleted by this editor.

##### C. Preview and publish

Add a preview panel or read-only gallery Items `Sort(colAdminQuestions,Slot,SortOrder.Ascending)`. Show Title, QuestionText, GuidanceText and required marker with the same fonts/card styling as employee cards. The preview does not set varCategory/colAnswers or overwrite an employee nomination in progress. If there are unsaved employee changes, navigate to Admin only through a discard/save confirmation.

Add “Publish new version and activate category” button. DisplayMode:

```powerfx
If(!varCanManageQuestions || !varAdminLoadOK || varIsBusy || IsBlank(varAdminCategory.ID) ||
   varAdminNewVersion<=varAdminBaseVersion,
   DisplayMode.Disabled,DisplayMode.Edit)
```

OnSelect is the complete [Admin.Publish.OnSelect.fx](documentation/manual-build/Admin.Publish.OnSelect.fx). It requires a successful configuration load, captures local editor values, validates 3–6 contiguous slots, checks the old category pointer, creates missing question rows, checks any existing keys match exactly, re-reads the saved set, checks the pointer again, then updates PublishedQuestionVersion and IsActive **last**. A failed load cannot publish stale editor content under a newly selected category. It never overwrites existing published rows. Add errors gallery Items colPublishErrors, labels ThisItem.Slot/Message.

If a row save fails, the category pointer is unchanged by that attempt and partial new-version rows may remain. Retry with identical content can reuse matching keys. If content has changed since a partial save, do not overwrite those keys: allocate a fresh version while retaining local edits. Add “Use a fresh version number” button, DisplayMode disabled while busy/no category; OnSelect:

```powerfx
IfError(
    Refresh(AwardCategories); Refresh(AwardQuestions);
    If(Coalesce(LookUp(AwardCategories,ID=varAdminCategory.ID,PublishedQuestionVersion),0)<>varAdminBaseVersion,
        Notify("A new version was published. Reload the category before continuing.",NotificationType.Warning),
        Set(varAdminNewVersion,Coalesce(First(SortByColumns(
            Filter(AwardQuestions,Category.Id=varAdminCategory.ID),
            "QuestionSetVersion",SortOrder.Descending)).QuestionSetVersion,0)+1);
        Set(varAdminDirty,true)
    ); true,
    Notify("Could not allocate the next version. Check your connection.",NotificationType.Error); false
)
```

A pointer-update timeout has an uncertain outcome; refresh before retrying. Coordinate one publisher per category. Strong concurrent publication requires a serialized backend mechanism, which is outside this fixed-schema manual Canvas implementation. Keep old versions and snapshots intact.

##### D. Category descriptions and inactive state

The six category codes/destinations are fixed. Authorized managers can change Title, Description and DisplayOrder in the AwardCategories SharePoint list; the app reads them dynamically. IsActive=false removes a category from new nominations but does not hide history in My nominations. Do not change CategoryCode, delete categories used by nominations, or set PublishedQuestionVersion to an unvalidated set. Adding a seventh category requires a new agreed source/form mapping, not only a config row.

No tag editors/columns are included. The proposed three question tags need a later storage and UX decision.

### Six expanding review question blocks

Create these six manual containers directly in the review page content container, after `cntReviewDetails`. They display the complete current prompts and responses. Use no input controls and no fixed-line clipping. All labels use Segoe UI and wrap. Each container Fill = Theme.Surface, BorderColor = Theme.Border, BorderThickness = 1, corner radii = 8. The formula for its Height refers only to its children, not its parent Height, avoiding a layout cycle.

For the first container use X = `cntReviewDetails.X`, Width = `cntReviewDetails.Width`. Use that same X/Width for the remaining five. `cntReviewDetails` must have its explicit Height from the main review guide.

#### Review slot 1

| Control / property | Value |
|---|---|
| `cntReviewQ1.Y` | `cntReviewDetails.Y+cntReviewDetails.Height+If(1<=varQuestionCount,18,0)` |
| `cntReviewQ1.Visible` | `1<=varQuestionCount` |
| `cntReviewQ1.Height` | `If(Self.Visible,lblReviewAnswer1.Y+lblReviewAnswer1.Height+24,0)` |
| `lblReviewHeading1` | X `28`; Y `24`; Width `Parent.Width-56`; AutoHeight `true`; Size `12.75`; Semibold; Color `Theme.Heading` |
| Heading Text | `With({p:LookUp(colAnswers,Slot=1,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 1"))` |
| `lblReviewPrompt1` | X `28`; Y `lblReviewHeading1.Y+lblReviewHeading1.Height+10`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `Theme.Muted` |
| Prompt Text | `With({p:LookUp(colAnswers,Slot=1,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `lblReviewAnswer1` | X `28`; Y `lblReviewPrompt1.Y+lblReviewPrompt1.Height+16`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `Theme.Body` |
| Answer Text | `With({a:LookUp(colAnswers,Slot=1,Response)},If(IsBlank(Trim(a)),"No response supplied (optional).",a))` |

#### Review slot 2

| Control / property | Value |
|---|---|
| `cntReviewQ2.Y` | `cntReviewQ1.Y+cntReviewQ1.Height+If(2<=varQuestionCount,18,0)` |
| `cntReviewQ2.Visible` | `2<=varQuestionCount` |
| `cntReviewQ2.Height` | `If(Self.Visible,lblReviewAnswer2.Y+lblReviewAnswer2.Height+24,0)` |
| `lblReviewHeading2` | X `28`; Y `24`; Width `Parent.Width-56`; AutoHeight `true`; Size `12.75`; Semibold; Color `Theme.Heading` |
| Heading Text | `With({p:LookUp(colAnswers,Slot=2,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 2"))` |
| `lblReviewPrompt2` | X `28`; Y `lblReviewHeading2.Y+lblReviewHeading2.Height+10`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `Theme.Muted` |
| Prompt Text | `With({p:LookUp(colAnswers,Slot=2,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `lblReviewAnswer2` | X `28`; Y `lblReviewPrompt2.Y+lblReviewPrompt2.Height+16`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `Theme.Body` |
| Answer Text | `With({a:LookUp(colAnswers,Slot=2,Response)},If(IsBlank(Trim(a)),"No response supplied (optional).",a))` |

#### Review slot 3

| Control / property | Value |
|---|---|
| `cntReviewQ3.Y` | `cntReviewQ2.Y+cntReviewQ2.Height+If(3<=varQuestionCount,18,0)` |
| `cntReviewQ3.Visible` | `3<=varQuestionCount` |
| `cntReviewQ3.Height` | `If(Self.Visible,lblReviewAnswer3.Y+lblReviewAnswer3.Height+24,0)` |
| `lblReviewHeading3` | X `28`; Y `24`; Width `Parent.Width-56`; AutoHeight `true`; Size `12.75`; Semibold; Color `Theme.Heading` |
| Heading Text | `With({p:LookUp(colAnswers,Slot=3,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 3"))` |
| `lblReviewPrompt3` | X `28`; Y `lblReviewHeading3.Y+lblReviewHeading3.Height+10`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `Theme.Muted` |
| Prompt Text | `With({p:LookUp(colAnswers,Slot=3,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `lblReviewAnswer3` | X `28`; Y `lblReviewPrompt3.Y+lblReviewPrompt3.Height+16`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `Theme.Body` |
| Answer Text | `With({a:LookUp(colAnswers,Slot=3,Response)},If(IsBlank(Trim(a)),"No response supplied (optional).",a))` |

#### Review slot 4

| Control / property | Value |
|---|---|
| `cntReviewQ4.Y` | `cntReviewQ3.Y+cntReviewQ3.Height+If(4<=varQuestionCount,18,0)` |
| `cntReviewQ4.Visible` | `4<=varQuestionCount` |
| `cntReviewQ4.Height` | `If(Self.Visible,lblReviewAnswer4.Y+lblReviewAnswer4.Height+24,0)` |
| `lblReviewHeading4` | X `28`; Y `24`; Width `Parent.Width-56`; AutoHeight `true`; Size `12.75`; Semibold; Color `Theme.Heading` |
| Heading Text | `With({p:LookUp(colAnswers,Slot=4,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 4"))` |
| `lblReviewPrompt4` | X `28`; Y `lblReviewHeading4.Y+lblReviewHeading4.Height+10`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `Theme.Muted` |
| Prompt Text | `With({p:LookUp(colAnswers,Slot=4,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `lblReviewAnswer4` | X `28`; Y `lblReviewPrompt4.Y+lblReviewPrompt4.Height+16`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `Theme.Body` |
| Answer Text | `With({a:LookUp(colAnswers,Slot=4,Response)},If(IsBlank(Trim(a)),"No response supplied (optional).",a))` |

#### Review slot 5

| Control / property | Value |
|---|---|
| `cntReviewQ5.Y` | `cntReviewQ4.Y+cntReviewQ4.Height+If(5<=varQuestionCount,18,0)` |
| `cntReviewQ5.Visible` | `5<=varQuestionCount` |
| `cntReviewQ5.Height` | `If(Self.Visible,lblReviewAnswer5.Y+lblReviewAnswer5.Height+24,0)` |
| `lblReviewHeading5` | X `28`; Y `24`; Width `Parent.Width-56`; AutoHeight `true`; Size `12.75`; Semibold; Color `Theme.Heading` |
| Heading Text | `With({p:LookUp(colAnswers,Slot=5,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 5"))` |
| `lblReviewPrompt5` | X `28`; Y `lblReviewHeading5.Y+lblReviewHeading5.Height+10`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `Theme.Muted` |
| Prompt Text | `With({p:LookUp(colAnswers,Slot=5,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `lblReviewAnswer5` | X `28`; Y `lblReviewPrompt5.Y+lblReviewPrompt5.Height+16`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `Theme.Body` |
| Answer Text | `With({a:LookUp(colAnswers,Slot=5,Response)},If(IsBlank(Trim(a)),"No response supplied (optional).",a))` |

#### Review slot 6

| Control / property | Value |
|---|---|
| `cntReviewQ6.Y` | `cntReviewQ5.Y+cntReviewQ5.Height+If(6<=varQuestionCount,18,0)` |
| `cntReviewQ6.Visible` | `6<=varQuestionCount` |
| `cntReviewQ6.Height` | `If(Self.Visible,lblReviewAnswer6.Y+lblReviewAnswer6.Height+24,0)` |
| `lblReviewHeading6` | X `28`; Y `24`; Width `Parent.Width-56`; AutoHeight `true`; Size `12.75`; Semibold; Color `Theme.Heading` |
| Heading Text | `With({p:LookUp(colAnswers,Slot=6,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 6"))` |
| `lblReviewPrompt6` | X `28`; Y `lblReviewHeading6.Y+lblReviewHeading6.Height+10`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `Theme.Muted` |
| Prompt Text | `With({p:LookUp(colAnswers,Slot=6,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `lblReviewAnswer6` | X `28`; Y `lblReviewPrompt6.Y+lblReviewPrompt6.Height+16`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `Theme.Body` |
| Answer Text | `With({a:LookUp(colAnswers,Slot=6,Response)},If(IsBlank(Trim(a)),"No response supplied (optional).",a))` |

Place `cntReviewEvidence.Y` at `cntReviewQ6.Y+cntReviewQ6.Height+18`. Hidden trailing question containers have zero Height and add no gap.

## Release verification checklist

- [ ] Apply the remaining II and IC corrections; compare fresh exports.
- [ ] Add all four remaining typed forms from their exact source lists.
- [ ] Confirm 30 non-attachment fields per individual form and 32 per team form.
- [ ] Preserve every generated DataField, person/lookup/choice type, and native attachment binding.
- [ ] Configure shared formulas and state, then resolve all actual App Checker errors.
- [ ] Exercise 3, 4, 5, and 6 active questions with varied prompt lengths and required flags.
- [ ] Verify Q2-Q6 counters use their own inputs, not Q1.
- [ ] Verify 2000-character response enforcement against the configured variable; do not confuse this response limit with an attachment-size policy.
- [ ] Scroll to every question, evidence control, error message, and action on mobile and desktop.
- [ ] Save an incomplete draft, keep its ID, edit it, save again, and verify one saved item.
- [ ] Add/remove/undo a synthetic attachment; save and reopen to verify persistence.
- [ ] Review unsaved responses and pending filenames without reloading server values.
- [ ] Confirm declaration resets when answers, details, or evidence change.
- [ ] Submit only after validation; confirm the final status, declaration, and timestamp after form success.
- [ ] Reopen Submitted in View mode, including attachment download.
- [ ] Test connector failure, server validation, uncertain timeout, retry, and concurrent modification.
- [ ] Confirm failed saves preserve answers/files and clear busy state; inspect My nominations before retrying an ambiguous new-item save.
- [ ] Test ordinary-user access directly in SharePoint, not only through hidden app controls.
- [ ] Approve real administrator access, category/question wording, levels, declaration, and attachment policy privately.
- [ ] Verify environment-variable connection rebinding before export/import or sharing.
- [ ] Keep live URLs, real IDs, user accounts, local paths, and deployment reports out of this change record.

Local checks of this document cover mappings, field coverage, slot/control references,
formula delimiters/quotes, local links, and sanitization. These checks are not a
Power Fx compiler or proof of connector behavior, permissions, rendering, or runtime.
