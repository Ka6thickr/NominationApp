# scrMDAwardTeam — build sheet

[Back to screen index](../Prod.md) · [Build components once](00-Reusable-Components.md)

Build controls in Tree view order. Insert children under the parent shown.

## 1. Complete Tree view

```text
scrMDAwardTeam
  cmpHeaderTI [instance of cmpAppHeader]
  cmpNavTI [instance of cmpAppNav]
  cmpStepperTI [instance of cmpStepper]
  cntScrollTI [Vertical container]
    cntPageTI [plain Container]
      lblHeadingTI [Label]
      lblSubtitleTI [Label]
      cntSummaryTI [Container]
        lblSummaryTI [Label]
        btnEditDetailsTI [Button]
      cntProgressTI [Container]
        lblProgressTI [Label]
        lblProgressHelpTI [Label]
      frmMDAwardTeam [Edit form]
        dcTIQ1Response [Data card]
          cntTIQ1 [Container]
            lblTIQ1Heading [Label]
            lblTIQ1Prompt [Label]
            txtTIQ1 [Text input]
            lblTIQ1Counter [Label]
          errTIQ1 [Label]
        dcTIQ2Response [Data card]
          cntTIQ2 [Container]
            lblTIQ2Heading [Label]
            lblTIQ2Prompt [Label]
            txtTIQ2 [Text input]
            lblTIQ2Counter [Label]
          errTIQ2 [Label]
        dcTIQ3Response [Data card]
          cntTIQ3 [Container]
            lblTIQ3Heading [Label]
            lblTIQ3Prompt [Label]
            txtTIQ3 [Text input]
            lblTIQ3Counter [Label]
          errTIQ3 [Label]
        dcTIQ4Response [Data card]
          cntTIQ4 [Container]
            lblTIQ4Heading [Label]
            lblTIQ4Prompt [Label]
            txtTIQ4 [Text input]
            lblTIQ4Counter [Label]
          errTIQ4 [Label]
        dcTIQ5Response [Data card]
          cntTIQ5 [Container]
            lblTIQ5Heading [Label]
            lblTIQ5Prompt [Label]
            txtTIQ5 [Text input]
            lblTIQ5Counter [Label]
          errTIQ5 [Label]
        dcTIQ6Response [Data card]
          cntTIQ6 [Container]
            lblTIQ6Heading [Label]
            lblTIQ6Prompt [Label]
            txtTIQ6 [Text input]
            lblTIQ6Counter [Label]
          errTIQ6 [Label]
        dcTIAttachments [Native attachment card]
          attTI [Native Attachments]
        dcTITitle [Hidden native card; retain generated child editors]
        dcTICategory [Hidden native card; retain generated child editors]
        dcTIQuestionSetVersion [Hidden native card; retain generated child editors]
        dcTIQuestionCount [Hidden native card; retain generated child editors]
        dcTINominatedBy [Hidden native card; retain generated child editors]
        dcTINominatorEmail [Hidden native card; retain generated child editors]
        dcTIEmployeeRole [Hidden native card; retain generated child editors]
        dcTIEmployeeLevel [Hidden native card; retain generated child editors]
        dcTINominationStatus [Hidden native card; retain generated child editors]
        dcTIDeclarationAccepted [Hidden native card; retain generated child editors]
        dcTISubmittedOn [Hidden native card; retain generated child editors]
        dcTITeamName [Hidden native card; retain generated child editors]
        dcTITeamPrimaryContact [Hidden native card; retain generated child editors]
        dcTITeamMembers [Hidden native card; retain generated child editors]
        dcTIQ1PromptSnapshot [Hidden native card; retain generated child editors]
        dcTIQ1RequiredSnapshot [Hidden native card; retain generated child editors]
        dcTIQ2PromptSnapshot [Hidden native card; retain generated child editors]
        dcTIQ2RequiredSnapshot [Hidden native card; retain generated child editors]
        dcTIQ3PromptSnapshot [Hidden native card; retain generated child editors]
        dcTIQ3RequiredSnapshot [Hidden native card; retain generated child editors]
        dcTIQ4PromptSnapshot [Hidden native card; retain generated child editors]
        dcTIQ4RequiredSnapshot [Hidden native card; retain generated child editors]
        dcTIQ5PromptSnapshot [Hidden native card; retain generated child editors]
        dcTIQ5RequiredSnapshot [Hidden native card; retain generated child editors]
        dcTIQ6PromptSnapshot [Hidden native card; retain generated child editors]
        dcTIQ6RequiredSnapshot [Hidden native card; retain generated child editors]
      lblSaveErrorTI [Label]
      cntActionsTI [Container]
        btnTIBack [Button]
        btnTISaveDraft [Button]
        btnTIReview [Button]
        btnTIBackToMine [Button]
  btnStartNewTI [hidden Button]
  btnGoMineTI [hidden Button]
  cntExitOverlayTI [plain Container]
    cntExitDialogTI [plain Container]
      lblExitMessageTI [Label]
      btnExitCancelTI [Button]
      btnExitDiscardTI [Button]
  cntBusyTI [plain Container]
    lblBusyTI [Label]
```

Component children are created once in the component definitions; they do not need separate per-screen labels/buttons. Native cards keep their generated metadata controls.

## 2. Components and scrolling — property table

Use temporary cntPage height=800 only until the action row exists. Turn Flexible height off. Slash-separated properties map to the slash-separated values in order.

| Control / property | Value or formula |
|---|---|
| scrMDAwardTeam.Fill | `varAppTheme.Page` |
| cmpHeaderTI.X / Y | `0 / 0` |
| cmpHeaderTI.Width / Height | `Parent.Width / If(App.Width<=760,58,64)` |
| cmpHeaderTI.BrandText / TitleText | `varAppTheme.Brand / varAppTheme.AppTitle` |
| cmpHeaderTI.UserText | `User().FullName` |
| cmpHeaderTI.HeadingColor / SmallLayout | `varAppTheme.Heading / App.Width<=760` |
| cmpNavTI.X / Y | `0 / cmpHeaderTI.Y+cmpHeaderTI.Height` |
| cmpNavTI.Width / Height | `Parent.Width / 48` |
| cmpNavTI.Busy / AccentColor | `varIsBusy / varAppTheme.Primary` |
| cmpNavTI.ActiveTab | `"New"` |
| cntScrollTI.X | `0` |
| cntScrollTI.Y | `cmpStepperTI.Y+cmpStepperTI.Height` |
| cntScrollTI.Width / Height | `Parent.Width / Max(0,Parent.Height-Self.Y)` |
| cntScrollTI.LayoutDirection | `LayoutDirection.Vertical` |
| cntScrollTI.LayoutOverflowY / LayoutOverflowX | `LayoutOverflow.Scroll / LayoutOverflow.Hide` |
| cntScrollTI.LayoutGap / all paddings | `0` |
| cntPageTI.Width | `Min(1180,Parent.Width)` |
| cntPageTI.AlignInContainer | `AlignInContainer.Center` |
| cntPageTI.FillPortions / LayoutMinWidth / LayoutMinHeight | `0 / 0 / 0` |
| cntPageTI.Height | `cntActionsTI.Y+cntActionsTI.Height+If(App.Width<=760,40,56)` |
| lblHeadingTI.X / Y | `If(App.Width<=760,16,24) / If(App.Width<=760,27,39)` |
| lblHeadingTI.Width / AutoHeight | `Parent.Width-2*Self.X / true` |
| lblHeadingTI.Font / Size | `Font.'Segoe UI' / If(App.Width<=760,18.75,22.5)` |
| lblHeadingTI.Color / FontWeight | `varAppTheme.Heading / FontWeight.Semibold` |
| lblSubtitleTI.X / Y | `lblHeadingTI.X / lblHeadingTI.Y+lblHeadingTI.Height+8` |
| lblSubtitleTI.Width / AutoHeight | `lblHeadingTI.Width / true` |
| lblSubtitleTI.Font / Size / Color | `Font.'Segoe UI' / 11.25 / varAppTheme.Muted` |
| cmpStepperTI.X / Y | `(Parent.Width-Self.Width)/2 / cmpNavTI.Y+cmpNavTI.Height` |
| cmpStepperTI.Width / Height | `Min(1060,Parent.Width) / 94` |
| cmpStepperTI.CurrentStep | `varCurrentStep` |
| cmpStepperTI.CurrentHex | `varAppTheme.PrimaryHex` |
| cmpStepperTI.CompleteHex | `varAppTheme.SuccessHex` |
| cmpStepperTI.PendingHex | `varAppTheme.BorderHex` |
| cmpStepperTI.MutedHex | `varAppTheme.MutedHex` |
| cmpStepperTI.HaloHex | `varAppTheme.PaleHex` |
| Control / property | Value or formula |
|---|---|
| cmpStepperTI.Steps | [Copy full formula](fx/cmpStepperTI.Steps.fx) |

## 3. Navigation events and hidden helpers

| Control / property | Value or formula |
|---|---|
| cmpNavTI.OnNew | [Copy full formula](fx/cmpNavTI.OnNew.fx) |
| cmpNavTI.OnMine | [Copy full formula](fx/cmpNavTI.OnMine.fx) |
| btnStartNewTI.OnSelect | [Copy full New nomination formula](fx/NewNomination.OnSelect.fx) |
| btnGoMineTI.OnSelect | `Navigate(scrMyNominations,ScreenTransition.None)` |
| btnStartNewTI and btnGoMineTI: Visible / DisplayMode | `false / DisplayMode.Edit` |

Paste event formulas on the **component instance**, not its definition. Hidden helpers remain on this same screen.

## 4. Dialog and busy controls — property table

| Control / property | Value or formula |
|---|---|
| cntExitOverlayTI.X / Y / Width / Height | `0 / 0 / Parent.Width / Parent.Height` |
| cntExitOverlayTI.Visible / Fill | `varShowExitDialog / RGBA(0,0,0,0.35)` |
| cntExitDialogTI.Width / Height | `Min(440,Parent.Width-32) / 220` |
| cntExitDialogTI.X / Y | `(Parent.Width-Self.Width)/2 / Max(16,(Parent.Height-Self.Height)/2)` |
| cntExitDialogTI.Fill | `varAppTheme.Surface` |
| lblExitMessageTI.X / Y / Width / Height | `20 / 20 / Parent.Width-40 / 112` |
| lblExitMessageTI.Text | `"Leave this page? Unsaved changes and selected files will be discarded."` |
| btnExitCancelTI.X / Y / Width / Height | `20 / 160 / 110 / 38` |
| btnExitCancelTI.Text / OnSelect | `"Cancel" / Set(varShowExitDialog,false)` |
| btnExitDiscardTI.X / Y / Width / Height | `Parent.Width-140 / 160 / 120 / 38` |
| btnExitDiscardTI.Text | `"Discard"` |
| cntBusyTI.X / Y / Width / Height | `0 / 0 / Parent.Width / Parent.Height` |
| cntBusyTI.Visible / Fill | `varIsBusy / RGBA(255,255,255,0.65)` |
| lblBusyTI.Text / Align | `"Saving or loading…" / Align.Center` |
| lblBusyTI.X / Y / Width / Height | `0 / (Parent.Height-40)/2 / Parent.Width / 40` |
| Control / property | Value or formula |
|---|---|
| btnExitDiscardTI.OnSelect | [Copy full formula](fx/btnExitDiscardTI.OnSelect.fx) |

## 5. Screen content, buttons and formulas



Keep frmMDAwardTeam inside cntPageTI. Also create lblSaveErrorTI, cntSummaryTI, cntProgressTI and cntActionsTI inside that page. Use [the exact placement table](Reference.md) below for each coordinate; it expands every reference for this screen.

cntActionsTI.Y=`Max(frmMDAwardTeam.Y+frmMDAwardTeam.Height,If(lblSaveErrorTI.Visible,lblSaveErrorTI.Y+lblSaveErrorTI.Height,0),cntProgressTI.Y+cntProgressTI.Height)+20`.

Inside cntSummaryTI, create lblSummaryTI: X=20,Y=16,Width=`Max(0,Parent.Width-160)`,AutoHeight=true,Text=`Coalesce(NomineeDisplay,"Details incomplete") & "  •  " & varAwardType & " award" & Char(10) & NominationReference`. Create btnEditDetailsTI: Text="Edit details", X=`Parent.Width-130`,Y=16,Width=110,Height=38,Visible=`!varReadOnly`,OnSelect=`Select(btnTIBack)`.

Inside cntProgressTI, create lblProgressTI: X/Y=16,Width=Parent.Width-32,AutoHeight=true,Text=`Text(CountIf(colAnswers,Slot<=varQuestionCount && !IsBlank(Trim(Response)))) & " of " & Text(varQuestionCount) & " responses entered"`. Add lblProgressHelpTI: X=16,Y=`lblProgressTI.Y+lblProgressTI.Height+10`,Width=Parent.Width-32,AutoHeight=true,Text="Required responses must be completed before review. You can save an incomplete draft.",Visible=`!varReadOnly`. Grow the progress container if long text exceeds its planned height; the action-row Max formula prevents overlap.

| Button in cntActionsTI | X | Y | Width | Text / action |
|---|---|---|---|---|
| btnTIBack | `0` | `0` | `80` | Back / full Back to details block in this form's recipe |
| btnTISaveDraft | `If(App.Width<=760,92,Parent.Width-278)` | `0` | `120` | Save draft / full btnTISaveDraft.OnSelect |
| btnTIReview | `If(App.Width<=760,0,Parent.Width-146)` | `If(App.Width<=760,50,0)` | `If(App.Width<=760,Parent.Width,146)` | Review / full btnTIReview.OnSelect |
| btnTIBackToMine | `0` | `0` | `180` | My nominations / `Select(btnGoMineTI)` |

First three buttons Visible=`!varReadOnly`; btnTIBackToMine.Visible=varReadOnly. Back DisplayMode disables while busy; Save disables while busy/read-only/no category; Review disables while busy/read-only. Copy the complete actions from [this form's recipe](Reference.md); do not replace capture/preflight/save handlers with a simple Navigate. Set screen OnVisible=`Set(varCurrentStep,3)`.


### Exact content placement

## scrMDAwardTeam — placement

| Control / property | Formula / value |
|---|---|
| `cntPageTI.Width` | `Min(1180, Parent.Width)` |
| `lblHeadingTI.X` | `If(App.Width<=760,16,24)` |
| `lblHeadingTI.Width` | `cntPageTI.Width-2*Self.X` |
| `lblHeadingTI.Y` | `If(App.Width<=760,27,39)` |
| `lblHeadingTI.Text` | `If(varReadOnly,"View nomination","Criteria & evidence")` |
| `lblSubtitleTI.Y` | `lblHeadingTI.Y+lblHeadingTI.Height+8` |
| `lblSubtitleTI.Text` | `varCategory.Title` |
| `cntSummaryTI.X / Width` | `lblHeadingTI.X` / `lblHeadingTI.Width` |
| `cntSummaryTI.Y` | `lblSubtitleTI.Y+lblSubtitleTI.Height+18` |
| `cntSummaryTI.Height` | `If(App.Width<=760,112,72)` |
| `cntProgressTI.X` | `If(App.Width<=760,lblHeadingTI.X,lblHeadingTI.X+lblHeadingTI.Width-260)` |
| `cntProgressTI.Y` | `cntSummaryTI.Y+cntSummaryTI.Height+22` |
| `cntProgressTI.Width / Height` | `If(App.Width<=760,lblHeadingTI.Width,260)` / `If(App.Width<=760,100,260)` |
| `frmMDAwardTeam.X` | `lblHeadingTI.X` |
| `frmMDAwardTeam.Y` | `If(App.Width<=760,cntProgressTI.Y+cntProgressTI.Height+22,cntProgressTI.Y)` |
| `frmMDAwardTeam.Width` | `If(App.Width<=760,lblHeadingTI.Width,lblHeadingTI.Width-282)` |
| `lblSaveErrorTI.Y` | `frmMDAwardTeam.Y+frmMDAwardTeam.Height+8` |
| `lblSaveErrorTI.X / Width` | `frmMDAwardTeam.X` / `frmMDAwardTeam.Width` |
| `lblSaveErrorTI.AutoHeight / Visible / Text` | `true` / `!IsBlank(frmMDAwardTeam.Error)` / `frmMDAwardTeam.Error` |
| `cntActionsTI.X / Width` | `lblHeadingTI.X` / `lblHeadingTI.Width` |
| `cntActionsTI.Y` | `Max(frmMDAwardTeam.Y+frmMDAwardTeam.Height,If(lblSaveErrorTI.Visible,lblSaveErrorTI.Y+lblSaveErrorTI.Height,0),cntProgressTI.Y+cntProgressTI.Height)+20` |
| `cntActionsTI.Height` | `If(App.Width<=760,96,48)` |
| `cntPageTI.Height` | `cntActionsTI.Y+cntActionsTI.Height+If(App.Width<=760,40,56)` |

Use the explicit sum of error-aware response card heights plus attachment card height +24 from the MDAwardTeam recipe below. Set subtitle X/Width to the heading X/Width, heading/subtitle AutoHeight=true, and use the common theme typography. Place Save/Review/Back buttons inside cntActionsTI using the shared action-row coordinates. The Details edit button uses the same capture-before-navigation action as btnTIBack. Do not set cntPageTI.Height to the viewport height.


### Build this form and every card

### MDAwardTeam: TEAM_IMPACT / TI

Use the common form-building and scrolling rules above. These formulas target classic controls and English Power Fx separators. They are not yet Studio-compiled or runtime-tested.

#### Controls to create

Screen `scrMDAwardTeam`; Edit form `frmMDAwardTeam`; saved-record variable `varRecordTI`; latest-record variable `varLatestTI`. Create six response text inputs `txtTIQ1` … `txtTIQ6` in the corresponding response cards, and keep native attachment input `attTI` inside `dcTIAttachments`.

Form DataSource = `MDAwardTeam`; Item = `varRecordTI`; DefaultMode = `FormMode.New`; NumberOfColumns = `1`; SnapToColumns = `false`. See layout guide for X/Y/Width/Height. Use the form's generated cards and unlock them. Preserve generated DataField strings exactly; if the connector shows a display name with spaces, use Studio's actual generated identifier. Required = `false` on entry cards to allow incomplete drafts; submission requirements are enforced separately. Do not remove metadata cards just because they are hidden.

Response cards are `dcTIQ1Response` … `dcTIQ6Response`. The other Q cards hold snapshots/flags and are hidden. Do not rename a response card to its text input name.

#### scrMDAwardTeam.OnVisible

[Copy full formula](fx/scrMDAwardTeam.01.fx) — paste into the property identified immediately above.


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

[Copy full formula](fx/scrMDAwardTeam.02.fx) — paste into the property identified immediately above.


#### btnTIReview.OnSelect

Set DisplayMode to `If(varIsBusy || varReadOnly, DisplayMode.Disabled, DisplayMode.Edit)`.

[Copy full formula](fx/scrMDAwardTeam.03.fx) — paste into the property identified immediately above.


`colCapturedAnswers` prevents clearing the source table while reading its snapshots. Review reads current text controls directly, so it does not depend on OnChange timing. If Studio exposes the native file-name column as DisplayName instead of Name, use that actual column in the one FileName projection above; do not change attachment Items/Update or collect file bodies.

#### frmMDAwardTeam.OnSuccess

[Copy full formula](fx/scrMDAwardTeam.04.fx) — paste into the property identified immediately above.


#### frmMDAwardTeam.OnFailure

[Copy full formula](fx/scrMDAwardTeam.05.fx) — paste into the property identified immediately above.


#### Back to details

Use a native button; Visible = `!varReadOnly`; DisplayMode disabled while varIsBusy. Its OnSelect:

[Copy full formula](fx/scrMDAwardTeam.06.fx) — paste into the property identified immediately above.


#### My nominations gallery galMineTI

Visible = `varBrowseCode = "TEAM_IMPACT"`. Items:

[Copy full formula](fx/scrMDAwardTeam.07.fx) — paste into the property identified immediately above.


Use `ThisItem.ID`, `ThisItem.Modified`, `ThisItem.NominationStatus.Value`, and `ThisItem.TeamName` in native labels. Reference Text = `"TEAM_IMPACT-" & Text(ThisItem.ID, "000000")`. An Open button inside this gallery uses the following OnSelect; it queries the clicked ID again before opening. Inactive/retired categories can still open historical records.

[Copy full formula](fx/scrMDAwardTeam.08.fx) — paste into the property identified immediately above.


Submitted items reuse this same typed form in View mode, including native file download. Form entry actions are hidden. This is the read-only screen implementation; a separate duplicate scrViewNomination is unnecessary.

#### Check this category before continuing

Save an incomplete draft, retain its ID, attach a small synthetic file, save again, reopen it, complete required answers, review unsaved changes, and submit. Confirm one item, correct snapshots, declaration and SubmittedOn. Reopen read-only. Test failed save/retry and concurrent modification. Use the full acceptance checklist; no runtime results are claimed here.

#### Question control properties

Insert a manual container inside each response card. Keep these exact unique names. Set label Font to Segoe UI, heading Color to varAppTheme.Heading, body/counter Color to varAppTheme.Muted. All labels wrap. Use the common input styling from the layout guide.

##### Slot 1

| Control / property | Formula or value |
|---|---|
| `dcTIQ1Response.Visible` | `1 <= varQuestionCount` |
| `dcTIQ1Response.X` / Y | `0` / `0` |
| `dcTIQ1Response.Width` | `Parent.Width` |
| `dcTIQ1Response.Height` | `If(Self.Visible, cntTIQ1.Y + cntTIQ1.Height + If(IsBlank(Self.Error), 0, errTIQ1.Height + 8) + 18, 0)` |
| `cntTIQ1` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrMDAwardTeam.09.fx) — paste into the property identified immediately above.


##### Slot 2

| Control / property | Formula or value |
|---|---|
| `dcTIQ2Response.Visible` | `2 <= varQuestionCount` |
| `dcTIQ2Response.X` / Y | `0` / `1` |
| `dcTIQ2Response.Width` | `Parent.Width` |
| `dcTIQ2Response.Height` | `If(Self.Visible, cntTIQ2.Y + cntTIQ2.Height + If(IsBlank(Self.Error), 0, errTIQ2.Height + 8) + 18, 0)` |
| `cntTIQ2` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrMDAwardTeam.10.fx) — paste into the property identified immediately above.


##### Slot 3

| Control / property | Formula or value |
|---|---|
| `dcTIQ3Response.Visible` | `3 <= varQuestionCount` |
| `dcTIQ3Response.X` / Y | `0` / `2` |
| `dcTIQ3Response.Width` | `Parent.Width` |
| `dcTIQ3Response.Height` | `If(Self.Visible, cntTIQ3.Y + cntTIQ3.Height + If(IsBlank(Self.Error), 0, errTIQ3.Height + 8) + 18, 0)` |
| `cntTIQ3` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrMDAwardTeam.11.fx) — paste into the property identified immediately above.


##### Slot 4

| Control / property | Formula or value |
|---|---|
| `dcTIQ4Response.Visible` | `4 <= varQuestionCount` |
| `dcTIQ4Response.X` / Y | `0` / `3` |
| `dcTIQ4Response.Width` | `Parent.Width` |
| `dcTIQ4Response.Height` | `If(Self.Visible, cntTIQ4.Y + cntTIQ4.Height + If(IsBlank(Self.Error), 0, errTIQ4.Height + 8) + 18, 0)` |
| `cntTIQ4` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrMDAwardTeam.12.fx) — paste into the property identified immediately above.


##### Slot 5

| Control / property | Formula or value |
|---|---|
| `dcTIQ5Response.Visible` | `5 <= varQuestionCount` |
| `dcTIQ5Response.X` / Y | `0` / `4` |
| `dcTIQ5Response.Width` | `Parent.Width` |
| `dcTIQ5Response.Height` | `If(Self.Visible, cntTIQ5.Y + cntTIQ5.Height + If(IsBlank(Self.Error), 0, errTIQ5.Height + 8) + 18, 0)` |
| `cntTIQ5` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrMDAwardTeam.13.fx) — paste into the property identified immediately above.


##### Slot 6

| Control / property | Formula or value |
|---|---|
| `dcTIQ6Response.Visible` | `6 <= varQuestionCount` |
| `dcTIQ6Response.X` / Y | `0` / `5` |
| `dcTIQ6Response.Width` | `Parent.Width` |
| `dcTIQ6Response.Height` | `If(Self.Visible, cntTIQ6.Y + cntTIQ6.Height + If(IsBlank(Self.Error), 0, errTIQ6.Height + 8) + 18, 0)` |
| `cntTIQ6` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrMDAwardTeam.14.fx) — paste into the property identified immediately above.


#### MDAwardTeam: form dimensions and missing-property completion

Set `frmMDAwardTeam.Width` from its actual parent as described above. Set `frmMDAwardTeam.Height` to:

[Copy full formula](fx/scrMDAwardTeam.15.fx) — paste into the property identified immediately above.



Rename each generated response error label as listed. Keep it directly inside the response card, not inside the question container. Set AutoHeight=true, Height=10, X=22, Width=Parent.Width-44, Text=Parent.Error, Visible=!IsBlank(Parent.Error), Color=varAppTheme.Error, Size=9, Live=Live.Assertive. Hide only the redundant generated response field-heading labels.

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

For all six inputs use Font=`Font.'Segoe UI'`, Size=`9.75`, Color=`varAppTheme.Body`, Fill=`varAppTheme.Surface`, BorderThickness=`1`, FocusedBorderColor=`varAppTheme.Primary`, FocusedBorderThickness=`2`, PaddingLeft/Right=`11`, PaddingTop/Bottom=`9`, all corner radii=`4`, and TabIndex=`0`. Set heading Font=`Font.'Segoe UI'` and Color=`varAppTheme.Heading`; prompt/counter Font=`Font.'Segoe UI'` and Color=`varAppTheme.Muted`. Prompt AutoHeight=`true`, base Height=`34`, Size=`9.75`; counter AutoHeight=`false`, Height=`18`. All labels Wrap=`true`.


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

[Copy full formula](fx/scrMDAwardTeam.16.fx) — paste into the property identified immediately above.


The attachment layout can retain the generated label/editor coordinates. If restyling it, keep the generated error label visible and reserve space for its complete text. Do not suppress native validation messages.

Add a classic label `lblSaveErrorTI` immediately after the form in the scrolling content container. Use the same X and Width as the form, Y=`frmMDAwardTeam.Y + frmMDAwardTeam.Height + 8`, AutoHeight=`true`, Text=`frmMDAwardTeam.Error`, Visible=`!IsBlank(frmMDAwardTeam.Error)`, Color=`varAppTheme.Error`, and Live=`Live.Assertive`. Place the action row after this label when visible so errors from hidden metadata cards are not lost. Do not reset inputs on failure.


#### MDAwardTeam: action controls

| Control | Text | Visible | DisplayMode |
|---|---|---|---|
| `btnTISaveDraft` | `"Save draft"` | `!varReadOnly` | `If(varIsBusy \|\| varReadOnly \|\| !varCategoryComplete, DisplayMode.Disabled, DisplayMode.Edit)` |
| `btnTIReview` | `"Review"` | `!varReadOnly` | `If(varIsBusy \|\| varReadOnly, DisplayMode.Disabled, DisplayMode.Edit)` |
| `btnTIBack` | `"Back to details"` | `!varReadOnly` | `If(varIsBusy, DisplayMode.Disabled, DisplayMode.Edit)` |

Use the complete OnSelect blocks above for these controls. Do not append a status Patch directly after SubmitForm. A read-only Back to My nominations button can use `Navigate(scrMyNominations, ScreenTransition.None)` with Visible=`varReadOnly`.


<a id="form-tt"></a>


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
| cmpHeaderTI.LogoImage | [Copy Image formula](fx/Header.LogoImage.fx) |

Before preview, initialize the global palette using [Theme setup](02-Theme.md). Components receive colours through input properties; do not reference app variables inside their definitions.
