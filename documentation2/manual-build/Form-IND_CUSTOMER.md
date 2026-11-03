# IND_CUSTOMER — complete typed form recipe

Read `README.md` and `01-Screens-and-Layout.md` first. These formulas target classic controls and English Power Fx separators. They are not yet Studio-compiled or runtime-tested.

## Controls to create

Screen `scrIndividualCustomer`; Edit form `frmIndividualCustomer`; saved-record variable `varRecordIC`; latest-record variable `varLatestIC`. Create six response text inputs `txtICQ1` … `txtICQ6` in the corresponding response cards, and keep native attachment input `attIC` inside `dcICAttachments`.

Form DataSource = `TrendMarcherAward`; Item = `varRecordIC`; DefaultMode = `FormMode.New`; NumberOfColumns = `1`; SnapToColumns = `false`. See layout guide for X/Y/Width/Height. Use the form's generated cards and unlock them. Preserve generated DataField strings exactly; if the connector shows a display name with spaces, use Studio's actual generated identifier. Required = `false` on entry cards to allow incomplete drafts; submission requirements are enforced separately. Do not remove metadata cards just because they are hidden.

Response cards are `dcICQ1Response` … `dcICQ6Response`. The other Q cards hold snapshots/flags and are hidden. Do not rename a response card to its text input name.

## scrIndividualCustomer.OnVisible

```powerfx
Set(varCurrentStep, 3)
```

Do not call NewForm/ResetForm here: returning from review must preserve inputs and queued files.

## All card Update properties

| SharePoint DataField / card | Update formula |
|---|---|
| `Title` / `dcICTitle` | `Left(varCategory.CategoryCode & " - " & If(varAwardType = "Individual", Coalesce(varEmployee.DisplayName, "Draft"), If(IsBlank(Trim(varTeamName)), "Draft", varTeamName)),255)` |
| `Category` / `dcICCategory` | `{Id: varCategory.ID, Value: varCategory.Title}` |
| `QuestionSetVersion` / `dcICQuestionSetVersion` | `varQuestionVersion` |
| `QuestionCount` / `dcICQuestionCount` | `varQuestionCount` |
| `NominatedBy` / `dcICNominatedBy` | `varNominator` |
| `NominatorEmail` / `dcICNominatorEmail` | `varUserEmail` |
| `EmployeeRole` / `dcICEmployeeRole` | `Trim(varRole)` |
| `EmployeeLevel` / `dcICEmployeeLevel` | `If(IsBlank(varLevel), Blank(), LookUp(Choices(TrendMarcherAward.EmployeeLevel), Value = varLevel))` |
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

## btnICSaveDraft.OnSelect

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
        Refresh(TrendMarcherAward);
        Set(varLatestIC, LookUp(TrendMarcherAward, ID = varNominationId));
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
    SubmitForm(frmIndividualCustomer),
    Set(varIsBusy, false)
)
    )
)
```

## btnICReview.OnSelect

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

## frmIndividualCustomer.OnSuccess

```powerfx
Set(varRecordIC, frmIndividualCustomer.LastSubmit);
Set(varNominationId, varRecordIC.ID);
Set(varLoadedModified, varRecordIC.Modified);
EditForm(frmIndividualCustomer);
Set(varHasChanges, false);
If(varSaveIntent = "Submit",
    IfError(
        Set(varRecordIC,
            Patch(TrendMarcherAward, varRecordIC,
                {NominationStatus: {Value: "Submitted"},
                 DeclarationAccepted: true, SubmittedOn: Now()}
            )
        );
        Set(varLoadedModified, varRecordIC.Modified);
        Set(varSubmittedOn, varRecordIC.SubmittedOn);
        Set(varSubmissionComplete, true);
        Set(varReadOnly, true);
        Set(varIsBusy, false);
        ViewForm(frmIndividualCustomer);
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

## frmIndividualCustomer.OnFailure

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

## My nominations gallery galMineIC

Visible = `varBrowseCode = "IND_CUSTOMER"`. Items:

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

Use `ThisItem.ID`, `ThisItem.Modified`, `ThisItem.NominationStatus.Value`, and `ThisItem.NominatedEmployee.DisplayName` in native labels. Reference Text = `"IND_CUSTOMER-" & Text(ThisItem.ID, "000000")`. An Open button inside this gallery uses the following OnSelect; it queries the clicked ID again before opening. Inactive/retired categories can still open historical records.

```powerfx
If(!varIsBusy,
    Set(varIsBusy, true);
    Set(varOpenOK, true);
    IfError(
        Refresh(TrendMarcherAward);
        Set(varRecordIC, LookUp(TrendMarcherAward, ID = ThisItem.ID && NominatorEmail = varUserEmail));
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
        ResetForm(frmIndividualCustomer);
        If(varReadOnly, ViewForm(frmIndividualCustomer), EditForm(frmIndividualCustomer));
        Set(varIsBusy, false);
        Navigate(scrIndividualCustomer, ScreenTransition.None)
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
| `dcICQ1Response.Visible` | `1 <= varQuestionCount` |
| `dcICQ1Response.X` / Y | `0` / `0` |
| `dcICQ1Response.Width` | `Parent.Width` |
| `dcICQ1Response.Height` | `If(Self.Visible, cntICQ1.Height + 18, 0)` |
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

### Slot 2

| Control / property | Formula or value |
|---|---|
| `dcICQ2Response.Visible` | `2 <= varQuestionCount` |
| `dcICQ2Response.X` / Y | `0` / `1` |
| `dcICQ2Response.Width` | `Parent.Width` |
| `dcICQ2Response.Height` | `If(Self.Visible, cntICQ2.Height + 18, 0)` |
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

### Slot 3

| Control / property | Formula or value |
|---|---|
| `dcICQ3Response.Visible` | `3 <= varQuestionCount` |
| `dcICQ3Response.X` / Y | `0` / `2` |
| `dcICQ3Response.Width` | `Parent.Width` |
| `dcICQ3Response.Height` | `If(Self.Visible, cntICQ3.Height + 18, 0)` |
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

### Slot 4

| Control / property | Formula or value |
|---|---|
| `dcICQ4Response.Visible` | `4 <= varQuestionCount` |
| `dcICQ4Response.X` / Y | `0` / `3` |
| `dcICQ4Response.Width` | `Parent.Width` |
| `dcICQ4Response.Height` | `If(Self.Visible, cntICQ4.Height + 18, 0)` |
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

### Slot 5

| Control / property | Formula or value |
|---|---|
| `dcICQ5Response.Visible` | `5 <= varQuestionCount` |
| `dcICQ5Response.X` / Y | `0` / `4` |
| `dcICQ5Response.Width` | `Parent.Width` |
| `dcICQ5Response.Height` | `If(Self.Visible, cntICQ5.Height + 18, 0)` |
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

### Slot 6

| Control / property | Formula or value |
|---|---|
| `dcICQ6Response.Visible` | `6 <= varQuestionCount` |
| `dcICQ6Response.X` / Y | `0` / `5` |
| `dcICQ6Response.Width` | `Parent.Width` |
| `dcICQ6Response.Height` | `If(Self.Visible, cntICQ6.Height + 18, 0)` |
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
