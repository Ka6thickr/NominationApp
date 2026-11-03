# IND_INNOVATION — complete typed form recipe

Read `README.md` and `01-Screens-and-Layout.md` first. These formulas target classic controls and English Power Fx separators. They are not yet Studio-compiled or runtime-tested.

## Controls to create

Screen `scrIndividualInnovation`; Edit form `frmIndividualInnovation`; saved-record variable `varRecordII`; latest-record variable `varLatestII`. Create six response text inputs `txtIIQ1` … `txtIIQ6` in the corresponding response cards, and keep native attachment input `attII` inside `dcIIAttachments`.

Form DataSource = `MDAward`; Item = `varRecordII`; DefaultMode = `FormMode.New`; NumberOfColumns = `1`; SnapToColumns = `false`. See layout guide for X/Y/Width/Height. Use the form's generated cards and unlock them. Preserve generated DataField strings exactly; if the connector shows a display name with spaces, use Studio's actual generated identifier. Required = `false` on entry cards to allow incomplete drafts; submission requirements are enforced separately. Do not remove metadata cards just because they are hidden.

Response cards are `dcIIQ1Response` … `dcIIQ6Response`. The other Q cards hold snapshots/flags and are hidden. Do not rename a response card to its text input name.

## scrIndividualInnovation.OnVisible

```powerfx
Set(varCurrentStep, 3)
```

Do not call NewForm/ResetForm here: returning from review must preserve inputs and queued files.

## All card Update properties

| SharePoint DataField / card | Update formula |
|---|---|
| `Title` / `dcIITitle` | `Left(varCategory.CategoryCode & " - " & If(varAwardType = "Individual", Coalesce(varEmployee.DisplayName, "Draft"), If(IsBlank(Trim(varTeamName)), "Draft", varTeamName)),255)` |
| `Category` / `dcIICategory` | `{Id: varCategory.ID, Value: varCategory.Title}` |
| `QuestionSetVersion` / `dcIIQuestionSetVersion` | `varQuestionVersion` |
| `QuestionCount` / `dcIIQuestionCount` | `varQuestionCount` |
| `NominatedBy` / `dcIINominatedBy` | `varNominator` |
| `NominatorEmail` / `dcIINominatorEmail` | `varUserEmail` |
| `EmployeeRole` / `dcIIEmployeeRole` | `Trim(varRole)` |
| `EmployeeLevel` / `dcIIEmployeeLevel` | `If(IsBlank(varLevel), Blank(), LookUp(Choices(MDAward.EmployeeLevel), Value = varLevel))` |
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

## btnIISaveDraft.OnSelect

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
        Refresh(MDAward);
        Set(varLatestII, LookUp(MDAward, ID = varNominationId));
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
    SubmitForm(frmIndividualInnovation),
    Set(varIsBusy, false)
)
    )
)
```

## btnIIReview.OnSelect

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

## frmIndividualInnovation.OnSuccess

```powerfx
Set(varRecordII, frmIndividualInnovation.LastSubmit);
Set(varNominationId, varRecordII.ID);
Set(varLoadedModified, varRecordII.Modified);
EditForm(frmIndividualInnovation);
Set(varHasChanges, false);
If(varSaveIntent = "Submit",
    IfError(
        Set(varRecordII,
            Patch(MDAward, varRecordII,
                {NominationStatus: {Value: "Submitted"},
                 DeclarationAccepted: true, SubmittedOn: Now()}
            )
        );
        Set(varLoadedModified, varRecordII.Modified);
        Set(varSubmittedOn, varRecordII.SubmittedOn);
        Set(varSubmissionComplete, true);
        Set(varReadOnly, true);
        Set(varIsBusy, false);
        ViewForm(frmIndividualInnovation);
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

## frmIndividualInnovation.OnFailure

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

## My nominations gallery galMineII

Visible = `varBrowseCode = "IND_INNOVATION"`. Items:

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

Use `ThisItem.ID`, `ThisItem.Modified`, `ThisItem.NominationStatus.Value`, and `ThisItem.NominatedEmployee.DisplayName` in native labels. Reference Text = `"IND_INNOVATION-" & Text(ThisItem.ID, "000000")`. An Open button inside this gallery uses the following OnSelect; it queries the clicked ID again before opening. Inactive/retired categories can still open historical records.

```powerfx
If(!varIsBusy,
    Set(varIsBusy, true);
    Set(varOpenOK, true);
    IfError(
        Refresh(MDAward);
        Set(varRecordII, LookUp(MDAward, ID = ThisItem.ID && NominatorEmail = varUserEmail));
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
        ResetForm(frmIndividualInnovation);
        If(varReadOnly, ViewForm(frmIndividualInnovation), EditForm(frmIndividualInnovation));
        Set(varIsBusy, false);
        Navigate(scrIndividualInnovation, ScreenTransition.None)
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
| `dcIIQ1Response.Visible` | `1 <= varQuestionCount` |
| `dcIIQ1Response.X` / Y | `0` / `0` |
| `dcIIQ1Response.Width` | `Parent.Width` |
| `dcIIQ1Response.Height` | `If(Self.Visible, cntIIQ1.Height + 18, 0)` |
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

### Slot 2

| Control / property | Formula or value |
|---|---|
| `dcIIQ2Response.Visible` | `2 <= varQuestionCount` |
| `dcIIQ2Response.X` / Y | `0` / `1` |
| `dcIIQ2Response.Width` | `Parent.Width` |
| `dcIIQ2Response.Height` | `If(Self.Visible, cntIIQ2.Height + 18, 0)` |
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

### Slot 3

| Control / property | Formula or value |
|---|---|
| `dcIIQ3Response.Visible` | `3 <= varQuestionCount` |
| `dcIIQ3Response.X` / Y | `0` / `2` |
| `dcIIQ3Response.Width` | `Parent.Width` |
| `dcIIQ3Response.Height` | `If(Self.Visible, cntIIQ3.Height + 18, 0)` |
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

### Slot 4

| Control / property | Formula or value |
|---|---|
| `dcIIQ4Response.Visible` | `4 <= varQuestionCount` |
| `dcIIQ4Response.X` / Y | `0` / `3` |
| `dcIIQ4Response.Width` | `Parent.Width` |
| `dcIIQ4Response.Height` | `If(Self.Visible, cntIIQ4.Height + 18, 0)` |
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

### Slot 5

| Control / property | Formula or value |
|---|---|
| `dcIIQ5Response.Visible` | `5 <= varQuestionCount` |
| `dcIIQ5Response.X` / Y | `0` / `4` |
| `dcIIQ5Response.Width` | `Parent.Width` |
| `dcIIQ5Response.Height` | `If(Self.Visible, cntIIQ5.Height + 18, 0)` |
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

### Slot 6

| Control / property | Formula or value |
|---|---|
| `dcIIQ6Response.Visible` | `6 <= varQuestionCount` |
| `dcIIQ6Response.X` / Y | `0` / `5` |
| `dcIIQ6Response.Width` | `Parent.Width` |
| `dcIIQ6Response.Height` | `If(Self.Visible, cntIIQ6.Height + 18, 0)` |
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
