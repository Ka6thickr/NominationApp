# Review, submission, My nominations and administration

Finish all six typed forms first. This chapter references their exact names. Submission is asynchronous: the active form saves the Draft and files; its OnSuccess then updates that same saved item to Submitted. Do not put a status Patch immediately after SubmitForm in the button formula. [Microsoft form functions](https://learn.microsoft.com/en-us/power-platform/power-fx/reference/function-form).

## 1. scrReview

Use the 960px centered page shell. OnVisible:

```powerfx
Set(varCurrentStep,4)
```

Heading “Review & submit”; subtitle “Check the nomination and supporting evidence before submitting.” Step-3 Review buttons already validate required details/responses and capture text controls directly into colAnswers, plus filenames into colReviewFiles. They reset declaration each time. Never re-query nomination answers from SharePoint for this review; that would omit current unsaved changes.

### A. Details summary

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

### B. All questions and answers

Build the six expanding read-only blocks exactly as [Review-Question-Controls.md](Review-Question-Controls.md). Prompts/answers are dynamic snapshots, not hardcoded category text. All answer labels have AutoHeight true. The source prototype's five-line clipping is deliberately not carried over: the user must see the entire answer before accepting the declaration.

### C. Evidence review

Add `cntReviewEvidence` after the final question block, same X/Width, white card, padding28. Heading “Supporting evidence”. Add Label `lblReviewFiles`, X28 Y58 WidthParent.Width-56, AutoHeight true, Text:

```powerfx
If(IsEmpty(colReviewFiles),"No files attached.",Concat(colReviewFiles,FileName,Char(10)))
```

This is the pending attachment filename list captured from the current native form. Files are not uploaded until SubmitForm. To inspect/add/remove evidence, return to the original form. Add Edit responses and evidence button below this label; OnSelect:

```powerfx
Set(varDeclarationAccepted,false);
```

Immediately after that statement paste the full action block from [Navigate-Active-Form.fx](Navigate-Active-Form.fx). Do not call NewForm/ResetForm. Set cntReviewEvidence.Height to edit button Y+Height+24.

### D. Declaration and Submit

Add a white declaration card below evidence+18, same X/Width. Classic Checkbox `chkDeclaration`, X20 Y16 WidthParent.Width-40 Height80 (increase if text wraps on mobile), Text “I confirm that the information in this nomination is accurate and appropriate to submit.” This is proposed UI wording; replace with the approved declaration before release. Default `varDeclarationAccepted`; OnCheck `Set(varDeclarationAccepted,true)`; OnUncheck `Set(varDeclarationAccepted,false)`; DisplayMode disabled while varIsBusy.

Add helper label: “Submitting saves this nomination. Submitted nominations are read-only in this app.” Do not claim a notification email was sent; no notification flow is included. Card Height = checkbox Y+Height+helper Height+28.

Below add Back and Submit nomination buttons. Back resets declaration then uses Navigate-Active-Form.fx. Submit.OnSelect is the complete [Review.Submit.OnSelect.fx](Review.Submit.OnSelect.fx). Submit.DisplayMode:

```powerfx
If(varIsBusy || varReadOnly || !varDeclarationAccepted ||
   !DetailsValid || !ResponsesValid || !varCategoryComplete,
   DisplayMode.Disabled,DisplayMode.Edit)
```

The file contains all six routing branches, fresh saved-item status/Modified checks, SaveIntent and SubmitForm calls. Each form's OnSuccess captures LastSubmit/ID, sets EditForm for subsequent saves, and performs the final status update only when SaveIntent is Submit. The busy state remains true through both phases. Navigation to confirmation occurs only in the successful status-update branch.

If the final status update fails, the first save has already returned an ID. Retain that ID, show the failure and check the current server status before retrying. A network timeout can make the outcome uncertain even if the server committed; do not promise that such an item definitely remains a Draft. Likewise, if the initial new-item SubmitForm times out before LastSubmit is returned, check My nominations before retrying creation. The fixed schema has no client-generated idempotency key, so exactly-once creation under an ambiguous network failure cannot be guaranteed by these client formulas.

## 2. scrConfirmation

Use the page shell without stepper. Center a white card Width `Min(640,parent.Width-32)`, X centered, Y48, padding32. Add native success icon/circle, heading “Nomination submitted”, and labels:

| Label | Text |
|---|---|
| Reference | `NominationReference` |
| Category | `varCategory.Title` |
| Nominee/team | `NomineeDisplay` |
| Time | `Text(varSubmittedOn,"dd mmm yyyy, hh:mm")` |

Time is displayed in the app user's local context; SharePoint stores the underlying date/time. Add View nomination with OnSelect the full Navigate-Active-Form block. Forms have already been placed in View mode by successful submission. Add My nominations → Navigate(scrMyNominations); New nomination → full NewNomination block. No fabricated nominee/reference/date should appear here.

## 3. scrMyNominations

Heading “My nominations”, subtitle “View your submitted nominations or continue a draft.” No stepper. The original all-category prototype list is implemented as a category-selected view to preserve delegation across six physical lists. Do not merge all nominations using ClearCollect/ForAll and assume it is complete.

### A. Screen refresh and filters

OnVisible:

```powerfx
Set(varBrowseError,false);
IfError(
    Refresh(AwardCategories);
    ClearCollect(colBrowseCategories,SortByColumns(AwardCategories,"DisplayOrder",SortOrder.Ascending));
    Switch(varBrowseCode,
        "IND_INNOVATION",Refresh(Nom_IndividualInnovation),
        "IND_CUSTOMER",Refresh(Nom_IndividualCustomer),
        "IND_EXCELLENCE",Refresh(Nom_IndividualExcellence),
        "TEAM_COLLAB",Refresh(Nom_TeamCollaboration),
        "TEAM_IMPACT",Refresh(Nom_TeamImpact),
        "TEAM_TRANSFORM",Refresh(Nom_TeamTransformation)
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

### B. Six galleries, one visible

Create `galMineII`, `galMineIC`, `galMineIE`, `galMineTC`, `galMineTI`, `galMineTT` at identical X/Y/Width/Height below the filters. Set their Items/Visible/Open buttons from the corresponding Form-CODE.md file. They query their actual typed source directly. Do not collect their results into a common unbounded table. Use a vertical gallery, TemplatePadding0, TemplateSize `If(App.Width<=760,150,76)`, Height `Max(280,App.Height-cntScrollMine.Y-Self.Y-56)`, ShowScrollbar true. The enclosing page height should end just below the gallery.

Desktop columns: Reference x16 width190; Nominee/team x216 width `Max(120,Parent.TemplateWidth-570)`; Modified x `Parent.TemplateWidth-330` width150; status x `Parent.TemplateWidth-170` width90; Open x `Parent.TemplateWidth-78` width62. On mobile stack reference y12, nominee y38, date/status y66, Open y102. Use native labels with Size9.75, truncate only the list summary if needed; full values display on opening. Status pill Fill pale green for Submitted, pale blue for Draft; show the status word as well as color. Draw a 1px bottom rule.

Each form recipe supplies the complete gallery Open.OnSelect: it refreshes and re-reads the clicked ID owned by the current user, loads saved snapshots and people, and opens Draft in EditForm or Submitted in ViewForm. It does not reinitialize questions from today's published configuration.

Empty label per gallery Visible `thatGallery.Visible && !varBrowseError && IsEmpty(thatGallery.AllItems)`, Text “No nominations match this selection.” Hide or replace this label while that gallery is loading. Error banner Visible varBrowseError. A missing result after a connection error must not be presented as a confirmed empty list.

Filtering by indexed NominatorEmail, Choice.Value and equality ID is designed to delegate; verify blue delegation warnings and test with more records than the configured data row limit. SharePoint permits only certain operators for complex fields and ID. [Microsoft SharePoint delegation table](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/connections/connection-sharepoint-online). If Studio flags the constant OR filters, rewrite as explicit If branches for All/exact status and zero/exact ID, each branch returning a direct Filter/SortByColumns on the same source; do not increase the row limit as a substitute.

## 4. scrQuestionAdministration

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

### A. Category and new version

Add `cmbAdminCategory`: Items colAdminCategories; DisplayFields `["Title"]`; SelectMultiple false; IsSearchable false. Add label displaying loaded category, published version and editing version:

```powerfx
Coalesce(varAdminCategory.Title,"No category loaded") &
"  • Published: " & Text(varAdminBaseVersion) &
"  • Editing new version: " & Text(varAdminNewVersion)
```

Add hidden local button `btnAdminLoadCopy`, OnSelect full [Admin.LoadCopy.OnSelect.fx](Admin.LoadCopy.OnSelect.fx). Visible button “Copy to new version” has DisplayMode disabled when no selected ID or busy. OnSelect:

```powerfx
If(varAdminDirty,
    Set(varShowAdminDiscard,true),
    Select(btnAdminLoadCopy)
)
```

Add dialog Visible varShowAdminDiscard, text “Discard local question edits and load the selected category?”. Cancel sets false; Confirm sets false then Select(btnAdminLoadCopy). Initialize varShowAdminDiscard false in App.OnStart. The load code selects the current published version, or highest staged version when none is published; it allocates highest existing version+1. It never edits a previously saved question row. Test delegation for the filtered/sorted highest-version query before relying on a long version history. It assumes a coordinated single publisher per category; it is not a distributed version allocator.

### B. Editor gallery

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

### C. Preview and publish

Add a preview panel or read-only gallery Items `Sort(colAdminQuestions,Slot,SortOrder.Ascending)`. Show Title, QuestionText, GuidanceText and required marker with the same fonts/card styling as employee cards. The preview does not set varCategory/colAnswers or overwrite an employee nomination in progress. If there are unsaved employee changes, navigate to Admin only through a discard/save confirmation.

Add “Publish new version and activate category” button. DisplayMode:

```powerfx
If(!varCanManageQuestions || !varAdminLoadOK || varIsBusy || IsBlank(varAdminCategory.ID) ||
   varAdminNewVersion<=varAdminBaseVersion,
   DisplayMode.Disabled,DisplayMode.Edit)
```

OnSelect is the complete [Admin.Publish.OnSelect.fx](Admin.Publish.OnSelect.fx). It requires a successful configuration load, captures local editor values, validates 3–6 contiguous slots, checks the old category pointer, creates missing question rows, checks any existing keys match exactly, re-reads the saved set, checks the pointer again, then updates PublishedQuestionVersion and IsActive **last**. A failed load cannot publish stale editor content under a newly selected category. It never overwrites existing published rows. Add errors gallery Items colPublishErrors, labels ThisItem.Slot/Message.

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

### D. Category descriptions and inactive state

The six category codes/destinations are fixed. Authorized managers can change Title, Description and DisplayOrder in the AwardCategories SharePoint list; the app reads them dynamically. IsActive=false removes a category from new nominations but does not hide history in My nominations. Do not change CategoryCode, delete categories used by nominations, or set PublishedQuestionVersion to an unvalidated set. Adding a seventh category requires a new agreed source/form mapping, not only a config row.

No tag editors/columns are included. The proposed three question tags need a later storage and UX decision.
