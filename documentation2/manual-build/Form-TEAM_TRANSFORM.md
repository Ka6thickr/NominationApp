# TEAM_TRANSFORM — complete typed form recipe

Read `README.md` and `01-Screens-and-Layout.md` first. These formulas target classic controls and English Power Fx separators. They are not yet Studio-compiled or runtime-tested.

## Controls to create

Screen `scrTeamTransformation`; Edit form `frmTeamTransformation`; saved-record variable `varRecordTT`; latest-record variable `varLatestTT`. Create six response text inputs `txtTTQ1` … `txtTTQ6` in the corresponding response cards, and keep native attachment input `attTT` inside `dcTTAttachments`.

Form DataSource = `SpecialTeamAward`; Item = `varRecordTT`; DefaultMode = `FormMode.New`; NumberOfColumns = `1`; SnapToColumns = `false`. See layout guide for X/Y/Width/Height. Use the form's generated cards and unlock them. Preserve generated DataField strings exactly; if the connector shows a display name with spaces, use Studio's actual generated identifier. Required = `false` on entry cards to allow incomplete drafts; submission requirements are enforced separately. Do not remove metadata cards just because they are hidden.

Response cards are `dcTTQ1Response` … `dcTTQ6Response`. The other Q cards hold snapshots/flags and are hidden. Do not rename a response card to its text input name.

## scrTeamTransformation.OnVisible

```powerfx
Set(varCurrentStep, 3)
```

Do not call NewForm/ResetForm here: returning from review must preserve inputs and queued files.

## All card Update properties

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

## btnTTSaveDraft.OnSelect

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
    SubmitForm(frmTeamTransformation),
    Set(varIsBusy, false)
)
    )
)
```

## btnTTReview.OnSelect

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

## frmTeamTransformation.OnSuccess

```powerfx
Set(varRecordTT, frmTeamTransformation.LastSubmit);
Set(varNominationId, varRecordTT.ID);
Set(varLoadedModified, varRecordTT.Modified);
EditForm(frmTeamTransformation);
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
        ViewForm(frmTeamTransformation);
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

## frmTeamTransformation.OnFailure

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

## My nominations gallery galMineTT

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
        ResetForm(frmTeamTransformation);
        If(varReadOnly, ViewForm(frmTeamTransformation), EditForm(frmTeamTransformation));
        Set(varIsBusy, false);
        Navigate(scrTeamTransformation, ScreenTransition.None)
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
| `dcTTQ1Response.Visible` | `1 <= varQuestionCount` |
| `dcTTQ1Response.X` / Y | `0` / `0` |
| `dcTTQ1Response.Width` | `Parent.Width` |
| `dcTTQ1Response.Height` | `If(Self.Visible, cntTTQ1.Height + 18, 0)` |
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

### Slot 2

| Control / property | Formula or value |
|---|---|
| `dcTTQ2Response.Visible` | `2 <= varQuestionCount` |
| `dcTTQ2Response.X` / Y | `0` / `1` |
| `dcTTQ2Response.Width` | `Parent.Width` |
| `dcTTQ2Response.Height` | `If(Self.Visible, cntTTQ2.Height + 18, 0)` |
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

### Slot 3

| Control / property | Formula or value |
|---|---|
| `dcTTQ3Response.Visible` | `3 <= varQuestionCount` |
| `dcTTQ3Response.X` / Y | `0` / `2` |
| `dcTTQ3Response.Width` | `Parent.Width` |
| `dcTTQ3Response.Height` | `If(Self.Visible, cntTTQ3.Height + 18, 0)` |
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

### Slot 4

| Control / property | Formula or value |
|---|---|
| `dcTTQ4Response.Visible` | `4 <= varQuestionCount` |
| `dcTTQ4Response.X` / Y | `0` / `3` |
| `dcTTQ4Response.Width` | `Parent.Width` |
| `dcTTQ4Response.Height` | `If(Self.Visible, cntTTQ4.Height + 18, 0)` |
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

### Slot 5

| Control / property | Formula or value |
|---|---|
| `dcTTQ5Response.Visible` | `5 <= varQuestionCount` |
| `dcTTQ5Response.X` / Y | `0` / `4` |
| `dcTTQ5Response.Width` | `Parent.Width` |
| `dcTTQ5Response.Height` | `If(Self.Visible, cntTTQ5.Height + 18, 0)` |
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

### Slot 6

| Control / property | Formula or value |
|---|---|
| `dcTTQ6Response.Visible` | `6 <= varQuestionCount` |
| `dcTTQ6Response.X` / Y | `0` / `5` |
| `dcTTQ6Response.Width` | `Parent.Width` |
| `dcTTQ6Response.Height` | `If(Self.Visible, cntTTQ6.Height + 18, 0)` |
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
