# NominationApp - cross-agent checkpoint

Updated: 13 November 2026, approximately 19:20 IST.

## 1. Read this first

This is a handoff for Codex, Copilot, and other coding agents continuing the
Power Apps Canvas nomination application associated with:

https://github.com/Ka6thickr/NominationApp

The user builds the app manually in Power Apps Studio using copy/paste property
formulas. Most recent work was supplied as instructions, not applied to repository
source or directly deployed to Power Apps. Do not equate a supplied formula with
a verified live change.

Evidence and precedence:

1. The user's latest decisions below override older proposals.
2. Latest screen exports establish what was present at export time.
3. This checkpoint records conversation decisions and supplied changes.
4. Repository guides provide baseline structure but still contain legacy formulas.

No live Power Apps Studio, SharePoint tenant, connector, or deployment access was
available. Static delimiter checks are NOT Power Fx compilation or runtime tests.
User attachments are read-only snapshots and must not be edited.

## 2. Locations and repository state

- Original working clone:
  `C:\Users\A200167682\Downloads\Files\NominationApp`
- This requested handoff:
  `C:\Users\A200167682\Downloads\NominationAppNew\changes.md`
- The destination contains a `NominationApp` subdirectory. Its Git status,
  relationship to the original clone, and contents have NOT been investigated.
  Do not assume it is the active clone or has the same commits.
- Original clone origin: `https://github.com/Ka6thickr/NominationApp.git`.
- Original clone HEAD at checkpoint: `6cf322d`.
- Original clone status checked at this checkpoint: modified `Prod.md`.
- Do not overwrite that uncommitted documentation.

Earlier local Git operations:

- Fetched upstream additions through `6adfd71`.
- `67f1e93`: Document category code migration and validation checkpoint.
- `6cf322d`: Merge remote-tracking branch 'origin/main'.
- No push was performed in this work.
- Earlier branch status was two ahead / zero behind origin/main; fetch and inspect
  before relying on that historical count.

This checkpoint is a local Markdown handoff, not a commit, tag, or pushed GitHub
checkpoint. Add it to the intended repository and commit/push only when requested.

## 3. Application structure and identifiers

There are six physical SharePoint nomination lists, each with its own native form.
Do not merge all nominations into an unbounded collection and claim completeness.

| CategoryCode / reference prefix | List | Screen | Form | Control prefix |
|---|---|---|---|---|
| IND_BII | BestInnovatorIndividual | scrBestInnovatorIndividual | frmBestInnovatorIndividual | II |
| IND_MDA | MDAward | scrMDAward | frmMDAward | IC |
| IND_TMA | TrendMarcherAward | scrTrendMarcherAward | frmTrendMarcherAward | IE |
| TEAM_BIT | BestInnovatorTeam | scrBestInnovatorTeam | frmBestInnovatorTeam | TC |
| TEAM_MDAT | MDAwardTeam | scrMDAwardTeam | frmMDAwardTeam | TI |
| TEAM_STA | SpecialTeamAward | scrSpecialTeamAward | frmSpecialTeamAward | TT |

Legacy app replacements:

| Old code | New code |
|---|---|
| IND_INNOVATION | IND_BII |
| IND_CUSTOMER | IND_MDA |
| IND_EXCELLENCE | IND_TMA |
| TEAM_COLLAB | TEAM_BIT |
| TEAM_IMPACT | TEAM_MDAT |
| TEAM_TRANSFORM | TEAM_STA |

A SharePoint screenshot also showed a different old set:
`IND_INNOVATOR`, `IND_TSTAR_MD`, `IND_TRENDMACHER`, `TEAM_INNOV`, `TEAM_MD`,
`TEAM_SPECIAL_AWARD_OB`. Inspect actual configuration; do not assume replacement
of only repository literals completes the migration.

Keep category row IDs and nomination lookup relationships intact. Do not create
duplicate categories or silently alter historical saved snapshots.

Saved nomination reference:

```powerfx
If(
    IsBlank(varNominationId),
    "Not saved yet",
    varCategory.CategoryCode & "-" & Text(varNominationId,"000000")
)
```

Update all routing, LevelOptions, loading, review actions, confirmation navigation,
browse refresh/visibility, and Open actions consistently to the new codes.

## 4. Final tag design - overrides upstream selectable-tag proposal

FINAL USER REQUIREMENTS:

- Tags are read-only; users do not select, edit, or toggle them.
- `AwardQuestions.Title` contains 1-3 pipe-separated labels.
- Actual question text comes from `QuestionText`; guidance from `GuidanceText`.
- Display every configured tag, with `#` prefixed for display only.
- Validate trimmed nonempty labels, 1-40 characters, unique ignoring case.
- Forbid `#`, carriage returns, and line feeds inside labels.
- Use three native Classic buttons per question, `DisplayMode.View`,
  empty OnSelect, and TabIndex -1.
- Do not use a custom component inside native form data-card containers: Studio
  rejected that nesting. Do not repeat that insertion approach.
- No SelectedTags state or selected-tag columns are needed.
- If optional selected-tag columns already exist, do not delete stored data.

Storage on EACH of the six nomination lists:

`Q1TagsSnapshot`, `Q2TagsSnapshot`, `Q3TagsSnapshot`, `Q4TagsSnapshot`,
`Q5TagsSnapshot`, `Q6TagsSnapshot`.

Plain multiline text, not required, append off. Refresh source metadata and add
these fields through the native form's Edit fields, then hide the cards.

Canonical answer shape:

```powerfx
{
    Slot: n.Value,
    Prompt: "",
    Required: false,
    Response: "",
    TagOptions: ""
}
```

Preserve this shape in App.OnStart, every New helper, category load, Save/Review/
Back capture, and all six My nominations Open actions.

Initialize `colCapturedAnswers` from `colAnswers` after new answer initialization.
Do not clear tags in normal screen OnVisible.

Hidden tags card for slot 1 (adapt slot/control prefix):

```powerfx
Visible = false
Height = 0
Required = false
Update = If(1<=varQuestionCount,LookUp(colAnswers,Slot=1,TagOptions),"")
```

Preserve generated native DataField/Default metadata.

Capture records must retain TagOptions:

```powerfx
{
    Slot: 1,
    Prompt: LookUp(colAnswers,Slot=1,Prompt),
    Required: LookUp(colAnswers,Slot=1,Required),
    Response: txtICQ1.Text,
    TagOptions: LookUp(colAnswers,Slot=1,TagOptions)
}
```

Capture all six slots, then `ClearCollect(colAnswers,colCapturedAnswers)`.
Do not replace existing guards, validation, preflight, or navigation.

Reopen records restore `TagOptions: Coalesce(varRecordIC.Q1TagsSnapshot,"")`,
and matching fields for Q2-Q6/prefixes. Never backfill old blank snapshots from
today's AwardQuestions.

## 5. Category loader and question text

The original loader used Title as the question-heading line, causing tag labels
to appear as headings. A full corrected btnLoadCategory.OnSelect was supplied.
Its presence in the live app has not been independently confirmed.

For each active slot, construct:

```powerfx
Prompt:
    "Question " & Text(n.Value) & Char(10) & q.QuestionText &
    If(IsBlank(q.GuidanceText),"",
       Char(10)&Char(10)&"Guidance: "&q.GuidanceText),
TagOptions:
    Concat(Split(q.Title,"|"),Trim(Value),"|")
```

Unused slots get blank Prompt/Response/TagOptions and Required=false.

The loader validates connection/configuration, category/type/code, published
version, 3-6 contiguous integer DisplayOrder values, Qn keys, ConfigurationKey,
nonblank questions, and valid tags. Failure leaves existing answers intact and
notifies. Success resets/new-modes the six forms and routes by the new codes.

Important caveats in the last supplied complete loader:

- Outer guard was `!varIsBusy`; stronger read-only/unsaved guards were discussed
  but must not be assumed present.
- Same-category shortcut retains loaded answers.
- Category-success clearing of review files and initialization of
  colCapturedAnswers were not confirmed in that supplied version.
- Test a NEW nomination to see new heading/tag construction. Old drafts retain
  their saved prompt/tag snapshots intentionally.

ConfigurationKey format: `IND_MDA-V1-Q1`, using actual code/version/order.
Publish complete immutable question versions, update PublishedQuestionVersion
last, and retain prior versions. MDAward/TrendMarcher were configured with six
questions; other categories with three in earlier screenshots. All forms support
six slots but must respect actual varQuestionCount.

## 6. Final native question layout

Control naming for each prefix P and slot n:

```text
frm...
  dcPQnResponse
    cntPQn
      lblPQnHeading
      btnPQnTagOne
      btnPQnTagTwo
      btnPQnTagThree
      lblPQnPrompt
      txtPQn
      lblPQnCounter
    errPQn
  dcPQnTagsSnapshot
```

P is II, IC, IE, TC, TI, or TT; n is 1-6. These are naming descriptions,
not literal Power Fx identifiers.

Final placement: horizontal right-aligned pills beside heading on wide screens;
below heading when App.Width<=760. Earlier vertically stacked layout is superseded.
Green/orange screenshot rectangles were placement markers only, NOT requested
button colors.

Pill styling:

| Position | Fill | Text/border |
|---|---|---|
| One | #FDE6F1 | #E20074 |
| Two | #E8F2FC | #0F6CBD |
| Three | #EAF5EA | #107C10 |

Height32, width `Max(72,Len(Self.Text)*6+24)`, radius16, border1,
Segoe UI size9.75. Hover/pressed retain normal fill/color.

Example IC Q1 layout:

```powerfx
// All three Y
If(App.Width<=760,lblICQ1Heading.Y+lblICQ1Heading.Height+8,16)

// TagThree.X
Parent.Width-22-Self.Width
// TagTwo.X
If(btnICQ1TagThree.Visible,btnICQ1TagThree.X-8-Self.Width,Parent.Width-22-Self.Width)
// TagOne.X
If(btnICQ1TagTwo.Visible,btnICQ1TagTwo.X-8-Self.Width,Parent.Width-22-Self.Width)

// Heading.Width
If(App.Width<=760,Parent.Width-44,
   If(btnICQ1TagOne.Visible,Max(0,btnICQ1TagOne.X-30),Parent.Width-44))

// Prompt.Y
Max(
    lblICQ1Heading.Y+lblICQ1Heading.Height,
    If(btnICQ1TagOne.Visible,btnICQ1TagOne.Y+btnICQ1TagOne.Height,0),
    If(btnICQ1TagTwo.Visible,btnICQ1TagTwo.Y+btnICQ1TagTwo.Height,0),
    If(btnICQ1TagThree.Visible,btnICQ1TagThree.Y+btnICQ1TagThree.Height,0)
)+8
```

TagOne visible if slot active and TagOptions not blank. TagTwo/Three additionally
require >=2/>=3 entries from Split(TagOptions,Char(124)). Text uses trimmed
first/second/third entry prefixed with "#". Char(124) avoids broken Markdown tables.

Heading reads saved Prompt before first Char(10), with required asterisk.
Prompt label reads everything after first Char(10).
Keep AutoHeight=true on both.

Input Y = prompt bottom +18; counter Y = input bottom +6;
container Height = counter bottom +14. Error-aware native card Height includes
container bottom + error label allocation +18.

Response input OnChange (adapt slot):

```powerfx
Patch(colAnswers,LookUp(colAnswers,Slot=1),{Response:Self.Text});
Set(varHasChanges,true);
Set(varResponsesComplete,false);
Set(varDeclarationAccepted,false)
```

Input DisplayMode follows native card, disabled while busy. Keep multiline,
MaxLength=varMaxResponseLength (2000), DelayOutput=false, existing accessibility.

KNOWN LIMITATION: Len*6 is approximate text sizing, not measured width. Three
long labels can overflow narrow containers. No automatic wrap was implemented.
Do not claim universal mobile fit; test longest labels and agree overflow behavior.

## 7. Per-form progress and save/open invariants

Best Innovator Individual:

- Earlier latest exports contained six native tag groups, hidden snapshot cards,
  and capture fixes. Static reviews corrected copied Slot=1 references, a Q6
  heading fallback, and a circular prompt/tag Y reference.
- Final horizontal layout formulas were supplied afterward for all six groups;
  no later export confirms all of those were applied.

MDAward:

- Initial export lacked tags/cards/capture fields; detailed updates supplied.
- Later action-container export had TagOptions in Save/Review/Back captures.
- Full btnMineOpenIC.OnSelect supplied: ownership-filtered ID lookup in MDAward,
  category IND_MDA validation, saved question/status checks, six saved tag fields,
  Draft EditForm / Submitted ViewForm.
- Open restores varNominationId, varLoadedModified, people, role/level, answers,
  flags and native form state; it does not fetch current questions.
- Initialize colCapturedAnswers consistently when integrating; the supplied full
  Open formula did not explicitly initialize that collection.

Other four forms:

- Fully expanded six-slot property workbook and 72 tag-button table rows supplied.
- Actual manual application not yet checked in fresh screen exports.

For ALL forms preserve:

- Correct list, form, attachment control and varRecord prefix.
- Save preflight: refresh correct source; reject missing/non-Draft/changed Modified.
- SubmitForm is asynchronous; final submitted-status Patch remains in OnSuccess.
- Keep saved ID after partial submission failure; show explicit errors.
- Keep native attachments inside their matching form.
- Gallery child Open button has the full Open behavior; gallery OnSelect empty.

Action button styling supplied: magenta primary Review, outlined Save draft/Back/
My nominations, explicit hover/pressed/disabled properties. No unrelated logic
replacement requested.

## 8. My nominations - latest agreed behavior

User explicitly chose ALL their nominations across ALL six categories as separate
category sections on one page, NOT a single merged gallery. Ownership remains
NominatorEmail=varUserEmail; this does not mean everyone's nominations.

Original export had:

- Six galleries at same coordinates, Visible only for matching varBrowseCode.
- Refresh below filters; New nomination below results.
- varBrowseType buttons auto-selected a first category.
- Direct typed gallery Items filtered ownership/status/exact numeric ID.

Supplied updates (application pending fresh export):

### Default loading and Refresh

Final scrMyNominations.OnVisible:

```powerfx
Select(btnBrowseRefresh)
```

Final Refresh deliberately clears filters AND refreshes all six lists:

```powerfx
If(
    !varIsBusy,
    Set(varIsBusy,true);
    Set(varBrowseError,false);
    Set(varBrowseType,"All");
    Set(varBrowseCode,"");
    Set(varBrowseStatus,"All");
    Set(varBrowseId,0);
    Reset(cmbBrowseCategory);
    Reset(ddBrowseStatus);
    Reset(txtBrowseId);
    IfError(
        Refresh(AwardCategories);
        ClearCollect(colBrowseCategories,
            SortByColumns(AwardCategories,"DisplayOrder",SortOrder.Ascending));
        Refresh(BestInnovatorIndividual);
        Refresh(MDAward);
        Refresh(TrendMarcherAward);
        Refresh(BestInnovatorTeam);
        Refresh(MDAwardTeam);
        Refresh(SpecialTeamAward);
        true,
        Set(varBrowseError,true);
        Notify("Nominations could not be refreshed. Check your connection and try again.",
            NotificationType.Error);
        false
    );
    Set(varIsBusy,false)
)
```

This supersedes earlier Refresh-preserves-filters advice. A separate All button
was proposed, then rejected as unnecessary; remove it if created.

### Filters

```powerfx
// cmbBrowseCategory.Items
Filter(colBrowseCategories,varBrowseType="All"||AwardType.Value=varBrowseType)

// DefaultSelectedItems
Filter(colBrowseCategories,CategoryCode=varBrowseCode)
```

Individual/Team click sets matching type, blank code, zero ID and resets category/
ID inputs; does not force first category. Guard programmatic reset-driven
OnChange with !varIsBusy. Category OnChange sets code from Selected or blank.
Status Default="All"; ID remains numeric exact match. An ID can exist in several
lists, so all-category ID search may match several category sections.

### Sections and scrolling

Keep direct per-source Items; do not use ClearCollect to aggregate nominations.
For each gallery, Visible requires no browse error, matching type or All, and
matching category code or blank.

Add headings lblMineSectionII/IC/IE/TC/TI/TT directly inside cntMineResults.
Stack sections in that order. Each visible heading allocates 36px above its
gallery; each visible gallery Height=300, hidden Height=0; add16 between sections.
Each gallery retains ShowScrollbar=true and existing typed child Open button.
300 is viewport height, not a record cap.

Container Height normally = galMineTT.Y+galMineTT.Height.
Test direct SharePoint delegation and paging beyond row limits.

### Move top actions - no color change

Move btnMineNew from cntActionsMine directly into cntPageMine.
btnBrowseRefresh is already directly in cntPageMine.

```powerfx
// btnMineNew
Width = Min(160,(lblHeadingMine.Width-12)/2)
Height = 38
X = lblHeadingMine.X+lblHeadingMine.Width-Self.Width
Y = If(App.Width<=760,lblSubtitleMine.Y+lblSubtitleMine.Height+16,lblSubtitleMine.Y)

// btnBrowseRefresh
Width = Min(110,(lblHeadingMine.Width-12)/2)
Height = 38
X = btnMineNew.X-Self.Width-12
Y = btnMineNew.Y

// lblSubtitleMine.Width (AutoHeight=true)
If(App.Width<=760,lblHeadingMine.Width,
   Max(0,btnBrowseRefresh.X-Self.X-16))

// cntMineFilters.Y
Max(lblSubtitleMine.Y+lblSubtitleMine.Height,btnMineNew.Y+btnMineNew.Height)+20

// lblBrowseError.Y
cntMineFilters.Y+cntMineFilters.Height+12

// cntMineResults.Y
If(lblBrowseError.Visible,lblBrowseError.Y+lblBrowseError.Height+16,
   cntMineFilters.Y+cntMineFilters.Height+20)

// cntPageMine.Height
cntMineResults.Y+cntMineResults.Height+If(App.Width<=760,40,56)
```

Hide empty cntActionsMine (Visible=false, Height=0).
Preserve colors and OnSelect; orange/green screenshot markers were placement only.

### Empty-state request and unresolved risk

User wants "No nominations yet" when empty. Supplied lblNoNominationsMine directly
in cntMineResults: X0, Y16, Width Parent.Width, Height60, centered muted text.
Text becomes "No nominations match your filters" if filters are active.

Supplied Visible used !varIsBusy, !varBrowseError, at least one visible gallery,
and IsEmpty(AllItems) for all visible galleries. DelayItemLoading=false suggested.

IMPORTANT FOLLOW-UP: this is not yet a robust confirmed-server-empty test.
AllItems represents loaded items, and successful Refresh does not prove gallery
queries have finished. Test loading/failure states before presenting as final.
Also the proposed label at Y16 overlaps the first visible section heading; section
headings/galleries were not yet hidden/repositioned for the global empty state.
The proposed shorter cntMineResults.Height alone does not hide overflowing child
controls reliably. Fix the complete empty-state layout without creating visibility
cycles (do not make label.Visible depend on galleries.Visible while hiding those
galleries based on label.Visible). Do not count limited collections as a proxy
for server completeness.

## 9. Question maintenance and theme

User deferred admin screen / Entra administrator configuration. Authorized
maintainers edit SharePoint configuration manually. Ordinary users require
read-only config access; UI gating is not SharePoint authorization.
All-zero administrator placeholder grants nobody UI admin access.

Theme primary #E20074, hover #B5005D, body #27364F, muted #667085,
surface white; Brand "T-System". Keep shared theme patterns.

Do not introduce TagsValid from the obsolete selectable design. Existing required
response/length validation remains; no tag-selection requirement exists.

## 10. Repository documentation and generated artifacts

Original clone:

- `Prod.md`: mapping/migration checkpoint plus uncommitted Tags follow-up.
  Its exactly-three/selectable description is OUTDATED.
- `NewTags.md`: upstream selectable-pill / exactly-three / 12-column design.
  Superseded by this checkpoint's read-only 1-3 / six-snapshot-field design.
- `tools\Build-ReusableGuides.py`: updated earlier to preserve migration checkpoint
  and emit mapping warnings, not to implement the final app formulas.
- `production-guide\scr*.md` and `production-guide\fx\*.fx`: useful baseline but
  often legacy codes, no tags, and single-category browse behavior.
- `production-guide\fx\scrMDAward.08.fx`: baseline IC Open action, legacy code and
  no tag restoration; do not copy unchanged.
- `tools\Test-ReusableGuides.py` and `tools\Test-ManualGuide.py`: structural tests,
  not Power Apps compiler/runtime tests.

Generated workbook:

`C:\Users\A200167682\.copilot\session-state\0a229f55-e1cd-41fd-a56a-33694285167e\files\Four_Forms_Response_Properties.xlsx`

Generator:

`C:\Users\A200167682\.copilot\session-state\0a229f55-e1cd-41fd-a56a-33694285167e\files\build_response_workbook.py`

Workbook contains Start Here, Control Names, Layout and Events, Capture and Reopen,
and four form-specific sheets. 24 groups, 264 controls, 4,296 property entries,
24 OnChange handlers, 72 tag Text formulas. Formulas stored as text, not Excel
formulas. Checked balanced delimiters, matching slots and no direct selfrefs.
It is a manual reference, not an importable deployed app.

These are local session artifacts, not portable GitHub URLs. Copy the workbook
alongside the intended repository if needed for another machine.

## 11. Evidence, validation and next actions

Static evidence:

- Earlier guide checks: 13 screen trees, component bindings/links, 194 FX delimiter
  checks; generator AST and whitespace checks passed at that time.
- Earlier II export: 266 controls and 2,568 formulas checked structurally.
- Initial MDAward export: 218 controls, 2,202 balanced formulas, no duplicate names
  or direct property selfrefs. It predated tags.
- Later MDAward action export showed correct TagOptions in captures.
- Latest My nominations export reviewed was before all-section/top-button changes.

Do not claim these checks validate the live current app.

Next agent should:

1. Read this handoff, inspect the intended clone and dirty state, obtain latest
   screen exports before overwriting manual changes.
2. Confirm codes/lookup IDs and six snapshot fields across all lists.
3. Verify shared App.OnStart/New/loader answer schema and all six capture/Open paths.
4. Validate final horizontal pills/heading/prompt chain on all forms; handle long
   labels/mobile overflow only after agreeing intended behavior.
5. Complete and test all-category browse default, reset-on-refresh filters, stacked
   sections, top actions, and truthful non-overlapping empty/loading/error states.
6. Update stale repository documentation/formula sources when authorized; use final
   read-only design, not NewTags.md selectable requirements.
7. Test new draft -> save -> reopen same ID -> review/back -> attachments ->
   submit -> confirmation -> Submitted View mode for all six categories.
8. Test older saved blank-tag records, connection failures, concurrent draft edits,
   invalid configuration, ordinary-user permissions, and delegation beyond row limit.
9. Record environment/date/tester/results. Commit/push only on request.

User communication preferences: exact control names, copy/paste-ready formulas,
tables grouped by question and form, no N/prefix placeholders when requesting all
controls. Explain necessary parent moves. Do not reinterpret screenshot marker
colors as styling requests.
