# IND_EXCELLENCE — complete typed form recipe

Read `README.md` and `01-Screens-and-Layout.md` first. These formulas target classic controls and English Power Fx separators. They are not yet Studio-compiled or runtime-tested.

## Controls to create

Screen `scrIndividualExcellence`; Edit form `frmIndividualExcellence`; saved-record variable `varRecordIE`; latest-record variable `varLatestIE`. Create six response text inputs `txtIEQ1` … `txtIEQ6` in the corresponding response cards, and keep native attachment input `attIE` inside `dcIEAttachments`.

Form DataSource = `BestInnovatorIndividual`; Item = `varRecordIE`; DefaultMode = `FormMode.New`; NumberOfColumns = `1`; SnapToColumns = `false`. See layout guide for X/Y/Width/Height. Use the form's generated cards and unlock them. Preserve generated DataField strings exactly; if the connector shows a display name with spaces, use Studio's actual generated identifier. Required = `false` on entry cards to allow incomplete drafts; submission requirements are enforced separately. Do not remove metadata cards just because they are hidden.

Response cards are `dcIEQ1Response` … `dcIEQ6Response`. The other Q cards hold snapshots/flags and are hidden. Do not rename a response card to its text input name.

## scrIndividualExcellence.OnVisible

```powerfx
Set(varCurrentStep, 3)
```

Do not call NewForm/ResetForm here: returning from review must preserve inputs and queued files.

## All card Update properties

| SharePoint DataField / card | Update formula |
|---|---|
| `Title` / `dcIETitle` | `Left(varCategory.CategoryCode & " - " & If(varAwardType = "Individual", Coalesce(varEmployee.DisplayName, "Draft"), If(IsBlank(Trim(varTeamName)), "Draft", varTeamName)),255)` |
| `Category` / `dcIECategory` | `{Id: varCategory.ID, Value: varCategory.Title}` |
| `QuestionSetVersion` / `dcIEQuestionSetVersion` | `varQuestionVersion` |
| `QuestionCount` / `dcIEQuestionCount` | `varQuestionCount` |
| `NominatedBy` / `dcIENominatedBy` | `varNominator` |
| `NominatorEmail` / `dcIENominatorEmail` | `varUserEmail` |
| `EmployeeRole` / `dcIEEmployeeRole` | `Trim(varRole)` |
| `EmployeeLevel` / `dcIEEmployeeLevel` | `If(IsBlank(varLevel), Blank(), LookUp(Choices(BestInnovatorIndividual.EmployeeLevel), Value = varLevel))` |
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

## btnIESaveDraft.OnSelect

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
        Refresh(BestInnovatorIndividual);
        Set(varLatestIE, LookUp(BestInnovatorIndividual, ID = varNominationId));
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
    SubmitForm(frmIndividualExcellence),
    Set(varIsBusy, false)
)
    )
)
```

## btnIEReview.OnSelect

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

## frmIndividualExcellence.OnSuccess

```powerfx
Set(varRecordIE, frmIndividualExcellence.LastSubmit);
Set(varNominationId, varRecordIE.ID);
Set(varLoadedModified, varRecordIE.Modified);
EditForm(frmIndividualExcellence);
Set(varHasChanges, false);
If(varSaveIntent = "Submit",
    IfError(
        Set(varRecordIE,
            Patch(BestInnovatorIndividual, varRecordIE,
                {NominationStatus: {Value: "Submitted"},
                 DeclarationAccepted: true, SubmittedOn: Now()}
            )
        );
        Set(varLoadedModified, varRecordIE.Modified);
        Set(varSubmittedOn, varRecordIE.SubmittedOn);
        Set(varSubmissionComplete, true);
        Set(varReadOnly, true);
        Set(varIsBusy, false);
        ViewForm(frmIndividualExcellence);
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

## frmIndividualExcellence.OnFailure

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

## My nominations gallery galMineIE

Visible = `varBrowseCode = "IND_EXCELLENCE"`. Items:

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

Use `ThisItem.ID`, `ThisItem.Modified`, `ThisItem.NominationStatus.Value`, and `ThisItem.NominatedEmployee.DisplayName` in native labels. Reference Text = `"IND_EXCELLENCE-" & Text(ThisItem.ID, "000000")`. An Open button inside this gallery uses the following OnSelect; it queries the clicked ID again before opening. Inactive/retired categories can still open historical records.

```powerfx
If(!varIsBusy,
    Set(varIsBusy, true);
    Set(varOpenOK, true);
    IfError(
        Refresh(BestInnovatorIndividual);
        Set(varRecordIE, LookUp(BestInnovatorIndividual, ID = ThisItem.ID && NominatorEmail = varUserEmail));
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
        ResetForm(frmIndividualExcellence);
        If(varReadOnly, ViewForm(frmIndividualExcellence), EditForm(frmIndividualExcellence));
        Set(varIsBusy, false);
        Navigate(scrIndividualExcellence, ScreenTransition.None)
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
| `dcIEQ1Response.Visible` | `1 <= varQuestionCount` |
| `dcIEQ1Response.X` / Y | `0` / `0` |
| `dcIEQ1Response.Width` | `Parent.Width` |
| `dcIEQ1Response.Height` | `If(Self.Visible, cntIEQ1.Height + 18, 0)` |
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

### Slot 2

| Control / property | Formula or value |
|---|---|
| `dcIEQ2Response.Visible` | `2 <= varQuestionCount` |
| `dcIEQ2Response.X` / Y | `0` / `1` |
| `dcIEQ2Response.Width` | `Parent.Width` |
| `dcIEQ2Response.Height` | `If(Self.Visible, cntIEQ2.Height + 18, 0)` |
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

### Slot 3

| Control / property | Formula or value |
|---|---|
| `dcIEQ3Response.Visible` | `3 <= varQuestionCount` |
| `dcIEQ3Response.X` / Y | `0` / `2` |
| `dcIEQ3Response.Width` | `Parent.Width` |
| `dcIEQ3Response.Height` | `If(Self.Visible, cntIEQ3.Height + 18, 0)` |
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

### Slot 4

| Control / property | Formula or value |
|---|---|
| `dcIEQ4Response.Visible` | `4 <= varQuestionCount` |
| `dcIEQ4Response.X` / Y | `0` / `3` |
| `dcIEQ4Response.Width` | `Parent.Width` |
| `dcIEQ4Response.Height` | `If(Self.Visible, cntIEQ4.Height + 18, 0)` |
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

### Slot 5

| Control / property | Formula or value |
|---|---|
| `dcIEQ5Response.Visible` | `5 <= varQuestionCount` |
| `dcIEQ5Response.X` / Y | `0` / `4` |
| `dcIEQ5Response.Width` | `Parent.Width` |
| `dcIEQ5Response.Height` | `If(Self.Visible, cntIEQ5.Height + 18, 0)` |
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

### Slot 6

| Control / property | Formula or value |
|---|---|
| `dcIEQ6Response.Visible` | `6 <= varQuestionCount` |
| `dcIEQ6Response.X` / Y | `0` / `5` |
| `dcIEQ6Response.Width` | `Parent.Width` |
| `dcIEQ6Response.Height` | `If(Self.Visible, cntIEQ6.Height + 18, 0)` |
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
