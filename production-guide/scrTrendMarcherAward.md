# scrTrendMarcherAward — build sheet

[Back to screen index](../Prod.md) · [Build components once](00-Reusable-Components.md)

Build controls in Tree view order. Insert children under the parent shown.

## 1. Complete Tree view

```text
scrTrendMarcherAward
  cmpHeaderIE [instance of cmpAppHeader]
  cmpNavIE [instance of cmpAppNav]
  cmpStepperIE [instance of cmpStepper]
  cntScrollIE [Vertical container]
    cntPageIE [plain Container]
      lblHeadingIE [Label]
      lblSubtitleIE [Label]
      cntSummaryIE [Container]
        lblSummaryIE [Label]
        btnEditDetailsIE [Button]
      cntProgressIE [Container]
        lblProgressIE [Label]
        lblProgressHelpIE [Label]
      frmTrendMarcherAward [Edit form]
        dcIEQ1Response [Data card]
          cntIEQ1 [Container]
            lblIEQ1Heading [Label]
            lblIEQ1Prompt [Label]
            txtIEQ1 [Text input]
            lblIEQ1Counter [Label]
          errIEQ1 [Label]
        dcIEQ2Response [Data card]
          cntIEQ2 [Container]
            lblIEQ2Heading [Label]
            lblIEQ2Prompt [Label]
            txtIEQ2 [Text input]
            lblIEQ2Counter [Label]
          errIEQ2 [Label]
        dcIEQ3Response [Data card]
          cntIEQ3 [Container]
            lblIEQ3Heading [Label]
            lblIEQ3Prompt [Label]
            txtIEQ3 [Text input]
            lblIEQ3Counter [Label]
          errIEQ3 [Label]
        dcIEQ4Response [Data card]
          cntIEQ4 [Container]
            lblIEQ4Heading [Label]
            lblIEQ4Prompt [Label]
            txtIEQ4 [Text input]
            lblIEQ4Counter [Label]
          errIEQ4 [Label]
        dcIEQ5Response [Data card]
          cntIEQ5 [Container]
            lblIEQ5Heading [Label]
            lblIEQ5Prompt [Label]
            txtIEQ5 [Text input]
            lblIEQ5Counter [Label]
          errIEQ5 [Label]
        dcIEQ6Response [Data card]
          cntIEQ6 [Container]
            lblIEQ6Heading [Label]
            lblIEQ6Prompt [Label]
            txtIEQ6 [Text input]
            lblIEQ6Counter [Label]
          errIEQ6 [Label]
        dcIEAttachments [Native attachment card]
          attIE [Native Attachments]
        dcIETitle [Hidden native card; retain generated child editors]
        dcIECategory [Hidden native card; retain generated child editors]
        dcIEQuestionSetVersion [Hidden native card; retain generated child editors]
        dcIEQuestionCount [Hidden native card; retain generated child editors]
        dcIENominatedBy [Hidden native card; retain generated child editors]
        dcIENominatorEmail [Hidden native card; retain generated child editors]
        dcIEEmployeeRole [Hidden native card; retain generated child editors]
        dcIEEmployeeLevel [Hidden native card; retain generated child editors]
        dcIENominationStatus [Hidden native card; retain generated child editors]
        dcIEDeclarationAccepted [Hidden native card; retain generated child editors]
        dcIESubmittedOn [Hidden native card; retain generated child editors]
        dcIENominatedEmployee [Hidden native card; retain generated child editors]
        dcIEQ1PromptSnapshot [Hidden native card; retain generated child editors]
        dcIEQ1RequiredSnapshot [Hidden native card; retain generated child editors]
        dcIEQ2PromptSnapshot [Hidden native card; retain generated child editors]
        dcIEQ2RequiredSnapshot [Hidden native card; retain generated child editors]
        dcIEQ3PromptSnapshot [Hidden native card; retain generated child editors]
        dcIEQ3RequiredSnapshot [Hidden native card; retain generated child editors]
        dcIEQ4PromptSnapshot [Hidden native card; retain generated child editors]
        dcIEQ4RequiredSnapshot [Hidden native card; retain generated child editors]
        dcIEQ5PromptSnapshot [Hidden native card; retain generated child editors]
        dcIEQ5RequiredSnapshot [Hidden native card; retain generated child editors]
        dcIEQ6PromptSnapshot [Hidden native card; retain generated child editors]
        dcIEQ6RequiredSnapshot [Hidden native card; retain generated child editors]
      lblSaveErrorIE [Label]
      cntActionsIE [Container]
        btnIEBack [Button]
        btnIESaveDraft [Button]
        btnIEReview [Button]
        btnIEBackToMine [Button]
  btnStartNewIE [hidden Button]
  btnGoMineIE [hidden Button]
  cntExitOverlayIE [plain Container]
    cntExitDialogIE [plain Container]
      lblExitMessageIE [Label]
      btnExitCancelIE [Button]
      btnExitDiscardIE [Button]
  cntBusyIE [plain Container]
    lblBusyIE [Label]
```

Component children are created once in the component definitions; they do not need separate per-screen labels/buttons. Native cards keep their generated metadata controls.

## 2. Components and scrolling — property table

Use temporary cntPage height=800 only until the action row exists. Turn Flexible height off. Slash-separated properties map to the slash-separated values in order.

| Control / property | Value or formula |
|---|---|
| scrTrendMarcherAward.Fill | `varAppTheme.Page` |
| cmpHeaderIE.X / Y | `0 / 0` |
| cmpHeaderIE.Width / Height | `Parent.Width / If(App.Width<=760,58,64)` |
| cmpHeaderIE.BrandText / TitleText | `varAppTheme.Brand / varAppTheme.AppTitle` |
| cmpHeaderIE.UserText | `User().FullName` |
| cmpHeaderIE.HeadingColor / SmallLayout | `varAppTheme.Heading / App.Width<=760` |
| cmpNavIE.X / Y | `0 / cmpHeaderIE.Y+cmpHeaderIE.Height` |
| cmpNavIE.Width / Height | `Parent.Width / 48` |
| cmpNavIE.Busy / AccentColor | `varIsBusy / varAppTheme.Primary` |
| cmpNavIE.ActiveTab | `"New"` |
| cntScrollIE.X | `0` |
| cntScrollIE.Y | `cmpStepperIE.Y+cmpStepperIE.Height` |
| cntScrollIE.Width / Height | `Parent.Width / Max(0,Parent.Height-Self.Y)` |
| cntScrollIE.LayoutDirection | `LayoutDirection.Vertical` |
| cntScrollIE.LayoutOverflowY / LayoutOverflowX | `LayoutOverflow.Scroll / LayoutOverflow.Hide` |
| cntScrollIE.LayoutGap / all paddings | `0` |
| cntPageIE.Width | `Min(1180,Parent.Width)` |
| cntPageIE.AlignInContainer | `AlignInContainer.Center` |
| cntPageIE.FillPortions / LayoutMinWidth / LayoutMinHeight | `0 / 0 / 0` |
| cntPageIE.Height | `cntActionsIE.Y+cntActionsIE.Height+If(App.Width<=760,40,56)` |
| lblHeadingIE.X / Y | `If(App.Width<=760,16,24) / If(App.Width<=760,27,39)` |
| lblHeadingIE.Width / AutoHeight | `Parent.Width-2*Self.X / true` |
| lblHeadingIE.Font / Size | `Font.'Segoe UI' / If(App.Width<=760,18.75,22.5)` |
| lblHeadingIE.Color / FontWeight | `varAppTheme.Heading / FontWeight.Semibold` |
| lblSubtitleIE.X / Y | `lblHeadingIE.X / lblHeadingIE.Y+lblHeadingIE.Height+8` |
| lblSubtitleIE.Width / AutoHeight | `lblHeadingIE.Width / true` |
| lblSubtitleIE.Font / Size / Color | `Font.'Segoe UI' / 11.25 / varAppTheme.Muted` |
| cmpStepperIE.X / Y | `(Parent.Width-Self.Width)/2 / cmpNavIE.Y+cmpNavIE.Height` |
| cmpStepperIE.Width / Height | `Min(1060,Parent.Width) / 94` |
| cmpStepperIE.CurrentStep | `varCurrentStep` |
| cmpStepperIE.CurrentHex | `varAppTheme.PrimaryHex` |
| cmpStepperIE.CompleteHex | `varAppTheme.SuccessHex` |
| cmpStepperIE.PendingHex | `varAppTheme.BorderHex` |
| cmpStepperIE.MutedHex | `varAppTheme.MutedHex` |
| cmpStepperIE.HaloHex | `varAppTheme.PaleHex` |
| Control / property | Value or formula |
|---|---|
| cmpStepperIE.Steps | [Copy full formula](fx/cmpStepperIE.Steps.fx) |

## 3. Navigation events and hidden helpers

| Control / property | Value or formula |
|---|---|
| cmpNavIE.OnNew | [Copy full formula](fx/cmpNavIE.OnNew.fx) |
| cmpNavIE.OnMine | [Copy full formula](fx/cmpNavIE.OnMine.fx) |
| btnStartNewIE.OnSelect | [Copy full New nomination formula](fx/NewNomination.OnSelect.fx) |
| btnGoMineIE.OnSelect | `Navigate(scrMyNominations,ScreenTransition.None)` |
| btnStartNewIE and btnGoMineIE: Visible / DisplayMode | `false / DisplayMode.Edit` |

Paste event formulas on the **component instance**, not its definition. Hidden helpers remain on this same screen.

## 4. Dialog and busy controls — property table

| Control / property | Value or formula |
|---|---|
| cntExitOverlayIE.X / Y / Width / Height | `0 / 0 / Parent.Width / Parent.Height` |
| cntExitOverlayIE.Visible / Fill | `varShowExitDialog / RGBA(0,0,0,0.35)` |
| cntExitDialogIE.Width / Height | `Min(440,Parent.Width-32) / 220` |
| cntExitDialogIE.X / Y | `(Parent.Width-Self.Width)/2 / Max(16,(Parent.Height-Self.Height)/2)` |
| cntExitDialogIE.Fill | `varAppTheme.Surface` |
| lblExitMessageIE.X / Y / Width / Height | `20 / 20 / Parent.Width-40 / 112` |
| lblExitMessageIE.Text | `"Leave this page? Unsaved changes and selected files will be discarded."` |
| btnExitCancelIE.X / Y / Width / Height | `20 / 160 / 110 / 38` |
| btnExitCancelIE.Text / OnSelect | `"Cancel" / Set(varShowExitDialog,false)` |
| btnExitDiscardIE.X / Y / Width / Height | `Parent.Width-140 / 160 / 120 / 38` |
| btnExitDiscardIE.Text | `"Discard"` |
| cntBusyIE.X / Y / Width / Height | `0 / 0 / Parent.Width / Parent.Height` |
| cntBusyIE.Visible / Fill | `varIsBusy / RGBA(255,255,255,0.65)` |
| lblBusyIE.Text / Align | `"Saving or loading…" / Align.Center` |
| lblBusyIE.X / Y / Width / Height | `0 / (Parent.Height-40)/2 / Parent.Width / 40` |
| Control / property | Value or formula |
|---|---|
| btnExitDiscardIE.OnSelect | [Copy full formula](fx/btnExitDiscardIE.OnSelect.fx) |

## 5. Screen content, buttons and formulas



Keep frmTrendMarcherAward inside cntPageIE. Also create lblSaveErrorIE, cntSummaryIE, cntProgressIE and cntActionsIE inside that page. Use [the exact placement table](Reference.md) below for each coordinate; it expands every reference for this screen.

cntActionsIE.Y=`Max(frmTrendMarcherAward.Y+frmTrendMarcherAward.Height,If(lblSaveErrorIE.Visible,lblSaveErrorIE.Y+lblSaveErrorIE.Height,0),cntProgressIE.Y+cntProgressIE.Height)+20`.

Inside cntSummaryIE, create lblSummaryIE: X=20,Y=16,Width=`Max(0,Parent.Width-160)`,AutoHeight=true,Text=`Coalesce(NomineeDisplay,"Details incomplete") & "  •  " & varAwardType & " award" & Char(10) & NominationReference`. Create btnEditDetailsIE: Text="Edit details", X=`Parent.Width-130`,Y=16,Width=110,Height=38,Visible=`!varReadOnly`,OnSelect=`Select(btnIEBack)`.

Inside cntProgressIE, create lblProgressIE: X/Y=16,Width=Parent.Width-32,AutoHeight=true,Text=`Text(CountIf(colAnswers,Slot<=varQuestionCount && !IsBlank(Trim(Response)))) & " of " & Text(varQuestionCount) & " responses entered"`. Add lblProgressHelpIE: X=16,Y=`lblProgressIE.Y+lblProgressIE.Height+10`,Width=Parent.Width-32,AutoHeight=true,Text="Required responses must be completed before review. You can save an incomplete draft.",Visible=`!varReadOnly`. Grow the progress container if long text exceeds its planned height; the action-row Max formula prevents overlap.

| Button in cntActionsIE | X | Y | Width | Text / action |
|---|---|---|---|---|
| btnIEBack | `0` | `0` | `80` | Back / full Back to details block in this form's recipe |
| btnIESaveDraft | `If(App.Width<=760,92,Parent.Width-278)` | `0` | `120` | Save draft / full btnIESaveDraft.OnSelect |
| btnIEReview | `If(App.Width<=760,0,Parent.Width-146)` | `If(App.Width<=760,50,0)` | `If(App.Width<=760,Parent.Width,146)` | Review / full btnIEReview.OnSelect |
| btnIEBackToMine | `0` | `0` | `180` | My nominations / `Select(btnGoMineIE)` |

First three buttons Visible=`!varReadOnly`; btnIEBackToMine.Visible=varReadOnly. Back DisplayMode disables while busy; Save disables while busy/read-only/no category; Review disables while busy/read-only. Copy the complete actions from [this form's recipe](Reference.md); do not replace capture/preflight/save handlers with a simple Navigate. Set screen OnVisible=`Set(varCurrentStep,3)`.


### Exact content placement

## scrTrendMarcherAward — placement

| Control / property | Formula / value |
|---|---|
| `cntPageIE.Width` | `Min(1180, Parent.Width)` |
| `lblHeadingIE.X` | `If(App.Width<=760,16,24)` |
| `lblHeadingIE.Width` | `cntPageIE.Width-2*Self.X` |
| `lblHeadingIE.Y` | `If(App.Width<=760,27,39)` |
| `lblHeadingIE.Text` | `If(varReadOnly,"View nomination","Criteria & evidence")` |
| `lblSubtitleIE.Y` | `lblHeadingIE.Y+lblHeadingIE.Height+8` |
| `lblSubtitleIE.Text` | `varCategory.Title` |
| `cntSummaryIE.X / Width` | `lblHeadingIE.X` / `lblHeadingIE.Width` |
| `cntSummaryIE.Y` | `lblSubtitleIE.Y+lblSubtitleIE.Height+18` |
| `cntSummaryIE.Height` | `If(App.Width<=760,112,72)` |
| `cntProgressIE.X` | `If(App.Width<=760,lblHeadingIE.X,lblHeadingIE.X+lblHeadingIE.Width-260)` |
| `cntProgressIE.Y` | `cntSummaryIE.Y+cntSummaryIE.Height+22` |
| `cntProgressIE.Width / Height` | `If(App.Width<=760,lblHeadingIE.Width,260)` / `If(App.Width<=760,100,260)` |
| `frmTrendMarcherAward.X` | `lblHeadingIE.X` |
| `frmTrendMarcherAward.Y` | `If(App.Width<=760,cntProgressIE.Y+cntProgressIE.Height+22,cntProgressIE.Y)` |
| `frmTrendMarcherAward.Width` | `If(App.Width<=760,lblHeadingIE.Width,lblHeadingIE.Width-282)` |
| `lblSaveErrorIE.Y` | `frmTrendMarcherAward.Y+frmTrendMarcherAward.Height+8` |
| `lblSaveErrorIE.X / Width` | `frmTrendMarcherAward.X` / `frmTrendMarcherAward.Width` |
| `lblSaveErrorIE.AutoHeight / Visible / Text` | `true` / `!IsBlank(frmTrendMarcherAward.Error)` / `frmTrendMarcherAward.Error` |
| `cntActionsIE.X / Width` | `lblHeadingIE.X` / `lblHeadingIE.Width` |
| `cntActionsIE.Y` | `Max(frmTrendMarcherAward.Y+frmTrendMarcherAward.Height,If(lblSaveErrorIE.Visible,lblSaveErrorIE.Y+lblSaveErrorIE.Height,0),cntProgressIE.Y+cntProgressIE.Height)+20` |
| `cntActionsIE.Height` | `If(App.Width<=760,96,48)` |
| `cntPageIE.Height` | `cntActionsIE.Y+cntActionsIE.Height+If(App.Width<=760,40,56)` |

Use the explicit sum of error-aware response card heights plus attachment card height +24 from the TrendMarcherAward recipe below. Set subtitle X/Width to the heading X/Width, heading/subtitle AutoHeight=true, and use the common theme typography. Place Save/Review/Back buttons inside cntActionsIE using the shared action-row coordinates. The Details edit button uses the same capture-before-navigation action as btnIEBack. Do not set cntPageIE.Height to the viewport height.


### Build this form and every card

### TrendMarcherAward: IND_EXCELLENCE / IE

Use the common form-building and scrolling rules above. These formulas target classic controls and English Power Fx separators. They are not yet Studio-compiled or runtime-tested.

#### Controls to create

Screen `scrTrendMarcherAward`; Edit form `frmTrendMarcherAward`; saved-record variable `varRecordIE`; latest-record variable `varLatestIE`. Create six response text inputs `txtIEQ1` … `txtIEQ6` in the corresponding response cards, and keep native attachment input `attIE` inside `dcIEAttachments`.

Form DataSource = `TrendMarcherAward`; Item = `varRecordIE`; DefaultMode = `FormMode.New`; NumberOfColumns = `1`; SnapToColumns = `false`. See layout guide for X/Y/Width/Height. Use the form's generated cards and unlock them. Preserve generated DataField strings exactly; if the connector shows a display name with spaces, use Studio's actual generated identifier. Required = `false` on entry cards to allow incomplete drafts; submission requirements are enforced separately. Do not remove metadata cards just because they are hidden.

Response cards are `dcIEQ1Response` … `dcIEQ6Response`. The other Q cards hold snapshots/flags and are hidden. Do not rename a response card to its text input name.

#### scrTrendMarcherAward.OnVisible

[Copy full formula](fx/scrTrendMarcherAward.01.fx) — paste into the property identified immediately above.


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

[Copy full formula](fx/scrTrendMarcherAward.02.fx) — paste into the property identified immediately above.


#### btnIEReview.OnSelect

Set DisplayMode to `If(varIsBusy || varReadOnly, DisplayMode.Disabled, DisplayMode.Edit)`.

[Copy full formula](fx/scrTrendMarcherAward.03.fx) — paste into the property identified immediately above.


`colCapturedAnswers` prevents clearing the source table while reading its snapshots. Review reads current text controls directly, so it does not depend on OnChange timing. If Studio exposes the native file-name column as DisplayName instead of Name, use that actual column in the one FileName projection above; do not change attachment Items/Update or collect file bodies.

#### frmTrendMarcherAward.OnSuccess

[Copy full formula](fx/scrTrendMarcherAward.04.fx) — paste into the property identified immediately above.


#### frmTrendMarcherAward.OnFailure

[Copy full formula](fx/scrTrendMarcherAward.05.fx) — paste into the property identified immediately above.


#### Back to details

Use a native button; Visible = `!varReadOnly`; DisplayMode disabled while varIsBusy. Its OnSelect:

[Copy full formula](fx/scrTrendMarcherAward.06.fx) — paste into the property identified immediately above.


#### My nominations gallery galMineIE

Visible = `varBrowseCode = "IND_EXCELLENCE"`. Items:

[Copy full formula](fx/scrTrendMarcherAward.07.fx) — paste into the property identified immediately above.


Use `ThisItem.ID`, `ThisItem.Modified`, `ThisItem.NominationStatus.Value`, and `ThisItem.NominatedEmployee.DisplayName` in native labels. Reference Text = `"IND_EXCELLENCE-" & Text(ThisItem.ID, "000000")`. An Open button inside this gallery uses the following OnSelect; it queries the clicked ID again before opening. Inactive/retired categories can still open historical records.

[Copy full formula](fx/scrTrendMarcherAward.08.fx) — paste into the property identified immediately above.


Submitted items reuse this same typed form in View mode, including native file download. Form entry actions are hidden. This is the read-only screen implementation; a separate duplicate scrViewNomination is unnecessary.

#### Check this category before continuing

Save an incomplete draft, retain its ID, attach a small synthetic file, save again, reopen it, complete required answers, review unsaved changes, and submit. Confirm one item, correct snapshots, declaration and SubmittedOn. Reopen read-only. Test failed save/retry and concurrent modification. Use the full acceptance checklist; no runtime results are claimed here.

#### Question control properties

Insert a manual container inside each response card. Keep these exact unique names. Set label Font to Segoe UI, heading Color to varAppTheme.Heading, body/counter Color to varAppTheme.Muted. All labels wrap. Use the common input styling from the layout guide.

##### Slot 1

| Control / property | Formula or value |
|---|---|
| `dcIEQ1Response.Visible` | `1 <= varQuestionCount` |
| `dcIEQ1Response.X` / Y | `0` / `0` |
| `dcIEQ1Response.Width` | `Parent.Width` |
| `dcIEQ1Response.Height` | `If(Self.Visible, cntIEQ1.Y + cntIEQ1.Height + If(IsBlank(Self.Error), 0, errIEQ1.Height + 8) + 18, 0)` |
| `cntIEQ1` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrTrendMarcherAward.09.fx) — paste into the property identified immediately above.


##### Slot 2

| Control / property | Formula or value |
|---|---|
| `dcIEQ2Response.Visible` | `2 <= varQuestionCount` |
| `dcIEQ2Response.X` / Y | `0` / `1` |
| `dcIEQ2Response.Width` | `Parent.Width` |
| `dcIEQ2Response.Height` | `If(Self.Visible, cntIEQ2.Y + cntIEQ2.Height + If(IsBlank(Self.Error), 0, errIEQ2.Height + 8) + 18, 0)` |
| `cntIEQ2` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrTrendMarcherAward.10.fx) — paste into the property identified immediately above.


##### Slot 3

| Control / property | Formula or value |
|---|---|
| `dcIEQ3Response.Visible` | `3 <= varQuestionCount` |
| `dcIEQ3Response.X` / Y | `0` / `2` |
| `dcIEQ3Response.Width` | `Parent.Width` |
| `dcIEQ3Response.Height` | `If(Self.Visible, cntIEQ3.Y + cntIEQ3.Height + If(IsBlank(Self.Error), 0, errIEQ3.Height + 8) + 18, 0)` |
| `cntIEQ3` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrTrendMarcherAward.11.fx) — paste into the property identified immediately above.


##### Slot 4

| Control / property | Formula or value |
|---|---|
| `dcIEQ4Response.Visible` | `4 <= varQuestionCount` |
| `dcIEQ4Response.X` / Y | `0` / `3` |
| `dcIEQ4Response.Width` | `Parent.Width` |
| `dcIEQ4Response.Height` | `If(Self.Visible, cntIEQ4.Y + cntIEQ4.Height + If(IsBlank(Self.Error), 0, errIEQ4.Height + 8) + 18, 0)` |
| `cntIEQ4` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrTrendMarcherAward.12.fx) — paste into the property identified immediately above.


##### Slot 5

| Control / property | Formula or value |
|---|---|
| `dcIEQ5Response.Visible` | `5 <= varQuestionCount` |
| `dcIEQ5Response.X` / Y | `0` / `4` |
| `dcIEQ5Response.Width` | `Parent.Width` |
| `dcIEQ5Response.Height` | `If(Self.Visible, cntIEQ5.Y + cntIEQ5.Height + If(IsBlank(Self.Error), 0, errIEQ5.Height + 8) + 18, 0)` |
| `cntIEQ5` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrTrendMarcherAward.13.fx) — paste into the property identified immediately above.


##### Slot 6

| Control / property | Formula or value |
|---|---|
| `dcIEQ6Response.Visible` | `6 <= varQuestionCount` |
| `dcIEQ6Response.X` / Y | `0` / `5` |
| `dcIEQ6Response.Width` | `Parent.Width` |
| `dcIEQ6Response.Height` | `If(Self.Visible, cntIEQ6.Y + cntIEQ6.Height + If(IsBlank(Self.Error), 0, errIEQ6.Height + 8) + 18, 0)` |
| `cntIEQ6` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrTrendMarcherAward.14.fx) — paste into the property identified immediately above.


#### TrendMarcherAward: form dimensions and missing-property completion

Set `frmTrendMarcherAward.Width` from its actual parent as described above. Set `frmTrendMarcherAward.Height` to:

[Copy full formula](fx/scrTrendMarcherAward.15.fx) — paste into the property identified immediately above.



Rename each generated response error label as listed. Keep it directly inside the response card, not inside the question container. Set AutoHeight=true, Height=10, X=22, Width=Parent.Width-44, Text=Parent.Error, Visible=!IsBlank(Parent.Error), Color=varAppTheme.Error, Size=9, Live=Live.Assertive. Hide only the redundant generated response field-heading labels.

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

For all six inputs use Font=`Font.'Segoe UI'`, Size=`9.75`, Color=`varAppTheme.Body`, Fill=`varAppTheme.Surface`, BorderThickness=`1`, FocusedBorderColor=`varAppTheme.Primary`, FocusedBorderThickness=`2`, PaddingLeft/Right=`11`, PaddingTop/Bottom=`9`, all corner radii=`4`, and TabIndex=`0`. Set heading Font=`Font.'Segoe UI'` and Color=`varAppTheme.Heading`; prompt/counter Font=`Font.'Segoe UI'` and Color=`varAppTheme.Muted`. Prompt AutoHeight=`true`, base Height=`34`, Size=`9.75`; counter AutoHeight=`false`, Height=`18`. All labels Wrap=`true`.


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

[Copy full formula](fx/scrTrendMarcherAward.16.fx) — paste into the property identified immediately above.


The attachment layout can retain the generated label/editor coordinates. If restyling it, keep the generated error label visible and reserve space for its complete text. Do not suppress native validation messages.

Add a classic label `lblSaveErrorIE` immediately after the form in the scrolling content container. Use the same X and Width as the form, Y=`frmTrendMarcherAward.Y + frmTrendMarcherAward.Height + 8`, AutoHeight=`true`, Text=`frmTrendMarcherAward.Error`, Visible=`!IsBlank(frmTrendMarcherAward.Error)`, Color=`varAppTheme.Error`, and Live=`Live.Assertive`. Place the action row after this label when visible so errors from hidden metadata cards are not lost. Do not reset inputs on failure.


#### TrendMarcherAward: action controls

| Control | Text | Visible | DisplayMode |
|---|---|---|---|
| `btnIESaveDraft` | `"Save draft"` | `!varReadOnly` | `If(varIsBusy \|\| varReadOnly \|\| !varCategoryComplete, DisplayMode.Disabled, DisplayMode.Edit)` |
| `btnIEReview` | `"Review"` | `!varReadOnly` | `If(varIsBusy \|\| varReadOnly, DisplayMode.Disabled, DisplayMode.Edit)` |
| `btnIEBack` | `"Back to details"` | `!varReadOnly` | `If(varIsBusy, DisplayMode.Disabled, DisplayMode.Edit)` |

Use the complete OnSelect blocks above for these controls. Do not append a status Patch directly after SubmitForm. A read-only Back to My nominations button can use `Navigate(scrMyNominations, ScreenTransition.None)` with Visible=`varReadOnly`.


<a id="form-tc"></a>


### Event file assignments — paste into these exact properties

Form button and event formulas are linked beside their exact headings above.

## 6. Verify before the next screen

| Check | Expected |
|---|---|
| Tree view | Matches the listed parents; no duplicate existing form |
| Components | Header/nav built once; instances have values/events |
| Scroll | Last input, error and action reachable at desktop/mobile widths |
| Cancel | Unsaved answers and queued files retained |
| Formulas | No unresolved names; English separators or locale equivalent |
| Runtime | Test synthetic draft/save/reopen before submission |

## Header image and theme initialization

| Control / property | Value or formula |
|---|---|
| cmpHeaderIE.LogoImage | [Copy Image formula](fx/Header.LogoImage.fx) |

Before preview, initialize the global palette using [Theme setup](02-Theme.md). Components receive colours through input properties; do not reference app variables inside their definitions.
