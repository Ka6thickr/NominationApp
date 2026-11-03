# TEAM_COLLAB — complete typed form recipe

Read `README.md` and `01-Screens-and-Layout.md` first. These formulas target classic controls and English Power Fx separators. They are not yet Studio-compiled or runtime-tested.

## Controls to create

Screen `scrTeamCollaboration`; Edit form `frmTeamCollaboration`; saved-record variable `varRecordTC`; latest-record variable `varLatestTC`. Create six response text inputs `txtTCQ1` … `txtTCQ6` in the corresponding response cards, and keep native attachment input `attTC` inside `dcTCAttachments`.

Form DataSource = `Nom_TeamCollaboration`; Item = `varRecordTC`; DefaultMode = `FormMode.New`; NumberOfColumns = `1`; SnapToColumns = `false`. See layout guide for X/Y/Width/Height. Use the form's generated cards and unlock them. Preserve generated DataField strings exactly; if the connector shows a display name with spaces, use Studio's actual generated identifier. Required = `false` on entry cards to allow incomplete drafts; submission requirements are enforced separately. Do not remove metadata cards just because they are hidden.

Response cards are `dcTCQ1Response` … `dcTCQ6Response`. The other Q cards hold snapshots/flags and are hidden. Do not rename a response card to its text input name.

## scrTeamCollaboration.OnVisible

```powerfx
Set(varCurrentStep, 3)
```

Do not call NewForm/ResetForm here: returning from review must preserve inputs and queued files.

## All card Update properties

| SharePoint DataField / card | Update formula |
|---|---|
| `Title` / `dcTCTitle` | `Left(varCategory.CategoryCode & " - " & If(varAwardType = "Individual", Coalesce(varEmployee.DisplayName, "Draft"), If(IsBlank(Trim(varTeamName)), "Draft", varTeamName)),255)` |
| `Category` / `dcTCCategory` | `{Id: varCategory.ID, Value: varCategory.Title}` |
| `QuestionSetVersion` / `dcTCQuestionSetVersion` | `varQuestionVersion` |
| `QuestionCount` / `dcTCQuestionCount` | `varQuestionCount` |
| `NominatedBy` / `dcTCNominatedBy` | `varNominator` |
| `NominatorEmail` / `dcTCNominatorEmail` | `varUserEmail` |
| `EmployeeRole` / `dcTCEmployeeRole` | `Trim(varRole)` |
| `EmployeeLevel` / `dcTCEmployeeLevel` | `If(IsBlank(varLevel), Blank(), LookUp(Choices(Nom_TeamCollaboration.EmployeeLevel), Value = varLevel))` |
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

## btnTCSaveDraft.OnSelect

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
        Refresh(Nom_TeamCollaboration);
        Set(varLatestTC, LookUp(Nom_TeamCollaboration, ID = varNominationId));
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
    SubmitForm(frmTeamCollaboration),
    Set(varIsBusy, false)
)
    )
)
```

## btnTCReview.OnSelect

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

## frmTeamCollaboration.OnSuccess

```powerfx
Set(varRecordTC, frmTeamCollaboration.LastSubmit);
Set(varNominationId, varRecordTC.ID);
Set(varLoadedModified, varRecordTC.Modified);
EditForm(frmTeamCollaboration);
Set(varHasChanges, false);
If(varSaveIntent = "Submit",
    IfError(
        Set(varRecordTC,
            Patch(Nom_TeamCollaboration, varRecordTC,
                {NominationStatus: {Value: "Submitted"},
                 DeclarationAccepted: true, SubmittedOn: Now()}
            )
        );
        Set(varLoadedModified, varRecordTC.Modified);
        Set(varSubmittedOn, varRecordTC.SubmittedOn);
        Set(varSubmissionComplete, true);
        Set(varReadOnly, true);
        Set(varIsBusy, false);
        ViewForm(frmTeamCollaboration);
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

## frmTeamCollaboration.OnFailure

```powerfx
Set(varIsBusy, false);
Set(varSubmissionComplete, false);
Set(varHasChanges, true);
Notify("Save was not confirmed. Your inputs are retained. If the connection timed out, check My nominations before retrying because the server may have saved the item.", NotificationType.Error)
```

## Back to details

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

## My nominations gallery galMineTC

Visible = `varBrowseCode = "TEAM_COLLAB"`. Items:

```powerfx
SortByColumns(
    Filter(Nom_TeamCollaboration,
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
        Refresh(Nom_TeamCollaboration);
        Set(varRecordTC, LookUp(Nom_TeamCollaboration, ID = ThisItem.ID && NominatorEmail = varUserEmail));
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
        ResetForm(frmTeamCollaboration);
        If(varReadOnly, ViewForm(frmTeamCollaboration), EditForm(frmTeamCollaboration));
        Set(varIsBusy, false);
        Navigate(scrTeamCollaboration, ScreenTransition.None)
    )
)
```

Submitted items reuse this same typed form in View mode, including native file download. Form entry actions are hidden. This is the read-only screen implementation; a separate duplicate scrViewNomination is unnecessary.

## Check this category before continuing

Save an incomplete draft, retain its ID, attach a small synthetic file, save again, reopen it, complete required answers, review unsaved changes, and submit. Confirm one item, correct snapshots, declaration and SubmittedOn. Reopen read-only. Test failed save/retry and concurrent modification. Use the full acceptance checklist; no runtime results are claimed here.

## Question control properties

Insert a manual container inside each response card. Keep these exact unique names. Set label Font to Segoe UI, heading Color to Theme.Heading, body/counter Color to Theme.Muted. All labels wrap. Use the common input styling from the layout guide.

### Slot 1

| Control / property | Formula or value |
|---|---|
| `dcTCQ1Response.Visible` | `1 <= varQuestionCount` |
| `dcTCQ1Response.X` / Y | `0` / `0` |
| `dcTCQ1Response.Width` | `Parent.Width` |
| `dcTCQ1Response.Height` | `If(Self.Visible, cntTCQ1.Height + 18, 0)` |
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

### Slot 2

| Control / property | Formula or value |
|---|---|
| `dcTCQ2Response.Visible` | `2 <= varQuestionCount` |
| `dcTCQ2Response.X` / Y | `0` / `1` |
| `dcTCQ2Response.Width` | `Parent.Width` |
| `dcTCQ2Response.Height` | `If(Self.Visible, cntTCQ2.Height + 18, 0)` |
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

### Slot 3

| Control / property | Formula or value |
|---|---|
| `dcTCQ3Response.Visible` | `3 <= varQuestionCount` |
| `dcTCQ3Response.X` / Y | `0` / `2` |
| `dcTCQ3Response.Width` | `Parent.Width` |
| `dcTCQ3Response.Height` | `If(Self.Visible, cntTCQ3.Height + 18, 0)` |
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

### Slot 4

| Control / property | Formula or value |
|---|---|
| `dcTCQ4Response.Visible` | `4 <= varQuestionCount` |
| `dcTCQ4Response.X` / Y | `0` / `3` |
| `dcTCQ4Response.Width` | `Parent.Width` |
| `dcTCQ4Response.Height` | `If(Self.Visible, cntTCQ4.Height + 18, 0)` |
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

### Slot 5

| Control / property | Formula or value |
|---|---|
| `dcTCQ5Response.Visible` | `5 <= varQuestionCount` |
| `dcTCQ5Response.X` / Y | `0` / `4` |
| `dcTCQ5Response.Width` | `Parent.Width` |
| `dcTCQ5Response.Height` | `If(Self.Visible, cntTCQ5.Height + 18, 0)` |
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

### Slot 6

| Control / property | Formula or value |
|---|---|
| `dcTCQ6Response.Visible` | `6 <= varQuestionCount` |
| `dcTCQ6Response.X` / Y | `0` / `5` |
| `dcTCQ6Response.Width` | `Parent.Width` |
| `dcTCQ6Response.Height` | `If(Self.Visible, cntTCQ6.Height + 18, 0)` |
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
