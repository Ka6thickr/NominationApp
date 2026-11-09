# scrSpecialTeamAward — build sheet

[Back to screen index](../Prod.md) · [Build components once](00-Reusable-Components.md)

Build controls in Tree view order. Insert children under the parent shown.

## 1. Complete Tree view

```text
scrSpecialTeamAward
  cmpHeaderTT [instance of cmpAppHeader]
  cmpNavTT [instance of cmpAppNav]
  cmpStepperTT [instance of cmpStepper]
  cntScrollTT [Vertical container]
    cntPageTT [plain Container]
      lblHeadingTT [Label]
      lblSubtitleTT [Label]
      cntSummaryTT [Container]
        lblSummaryTT [Label]
        btnEditDetailsTT [Button]
      cntProgressTT [Container]
        lblProgressTT [Label]
        lblProgressHelpTT [Label]
      frmSpecialTeamAward [Edit form]
        dcTTQ1Response [Data card]
          cntTTQ1 [Container]
            lblTTQ1Heading [Label]
            lblTTQ1Prompt [Label]
            txtTTQ1 [Text input]
            lblTTQ1Counter [Label]
          errTTQ1 [Label]
        dcTTQ2Response [Data card]
          cntTTQ2 [Container]
            lblTTQ2Heading [Label]
            lblTTQ2Prompt [Label]
            txtTTQ2 [Text input]
            lblTTQ2Counter [Label]
          errTTQ2 [Label]
        dcTTQ3Response [Data card]
          cntTTQ3 [Container]
            lblTTQ3Heading [Label]
            lblTTQ3Prompt [Label]
            txtTTQ3 [Text input]
            lblTTQ3Counter [Label]
          errTTQ3 [Label]
        dcTTQ4Response [Data card]
          cntTTQ4 [Container]
            lblTTQ4Heading [Label]
            lblTTQ4Prompt [Label]
            txtTTQ4 [Text input]
            lblTTQ4Counter [Label]
          errTTQ4 [Label]
        dcTTQ5Response [Data card]
          cntTTQ5 [Container]
            lblTTQ5Heading [Label]
            lblTTQ5Prompt [Label]
            txtTTQ5 [Text input]
            lblTTQ5Counter [Label]
          errTTQ5 [Label]
        dcTTQ6Response [Data card]
          cntTTQ6 [Container]
            lblTTQ6Heading [Label]
            lblTTQ6Prompt [Label]
            txtTTQ6 [Text input]
            lblTTQ6Counter [Label]
          errTTQ6 [Label]
        dcTTAttachments [Native attachment card]
          attTT [Native Attachments]
        dcTTTitle [Hidden native card; retain generated child editors]
        dcTTCategory [Hidden native card; retain generated child editors]
        dcTTQuestionSetVersion [Hidden native card; retain generated child editors]
        dcTTQuestionCount [Hidden native card; retain generated child editors]
        dcTTNominatedBy [Hidden native card; retain generated child editors]
        dcTTNominatorEmail [Hidden native card; retain generated child editors]
        dcTTEmployeeRole [Hidden native card; retain generated child editors]
        dcTTEmployeeLevel [Hidden native card; retain generated child editors]
        dcTTNominationStatus [Hidden native card; retain generated child editors]
        dcTTDeclarationAccepted [Hidden native card; retain generated child editors]
        dcTTSubmittedOn [Hidden native card; retain generated child editors]
        dcTTTeamName [Hidden native card; retain generated child editors]
        dcTTTeamPrimaryContact [Hidden native card; retain generated child editors]
        dcTTTeamMembers [Hidden native card; retain generated child editors]
        dcTTQ1PromptSnapshot [Hidden native card; retain generated child editors]
        dcTTQ1RequiredSnapshot [Hidden native card; retain generated child editors]
        dcTTQ2PromptSnapshot [Hidden native card; retain generated child editors]
        dcTTQ2RequiredSnapshot [Hidden native card; retain generated child editors]
        dcTTQ3PromptSnapshot [Hidden native card; retain generated child editors]
        dcTTQ3RequiredSnapshot [Hidden native card; retain generated child editors]
        dcTTQ4PromptSnapshot [Hidden native card; retain generated child editors]
        dcTTQ4RequiredSnapshot [Hidden native card; retain generated child editors]
        dcTTQ5PromptSnapshot [Hidden native card; retain generated child editors]
        dcTTQ5RequiredSnapshot [Hidden native card; retain generated child editors]
        dcTTQ6PromptSnapshot [Hidden native card; retain generated child editors]
        dcTTQ6RequiredSnapshot [Hidden native card; retain generated child editors]
      lblSaveErrorTT [Label]
      cntActionsTT [Container]
        btnTTBack [Button]
        btnTTSaveDraft [Button]
        btnTTReview [Button]
        btnTTBackToMine [Button]
  btnStartNewTT [hidden Button]
  btnGoMineTT [hidden Button]
  cntExitOverlayTT [plain Container]
    cntExitDialogTT [plain Container]
      lblExitMessageTT [Label]
      btnExitCancelTT [Button]
      btnExitDiscardTT [Button]
  cntBusyTT [plain Container]
    lblBusyTT [Label]
```

Component children are created once in the component definitions; they do not need separate per-screen labels/buttons. Native cards keep their generated metadata controls.

## 2. Components and scrolling — property table

Use temporary cntPage height=800 only until the action row exists. Turn Flexible height off. Slash-separated properties map to the slash-separated values in order.

| Control / property | Value or formula |
|---|---|
| scrSpecialTeamAward.Fill | `varAppTheme.Page` |
| cmpHeaderTT.X / Y | `0 / 0` |
| cmpHeaderTT.Width / Height | `Parent.Width / If(App.Width<=760,58,64)` |
| cmpHeaderTT.BrandText / TitleText | `varAppTheme.Brand / varAppTheme.AppTitle` |
| cmpHeaderTT.UserText | `User().FullName` |
| cmpHeaderTT.HeadingColor / SmallLayout | `varAppTheme.Heading / App.Width<=760` |
| cmpNavTT.X / Y | `0 / cmpHeaderTT.Y+cmpHeaderTT.Height` |
| cmpNavTT.Width / Height | `Parent.Width / 48` |
| cmpNavTT.Busy / AccentColor | `varIsBusy / varAppTheme.Primary` |
| cmpNavTT.ActiveTab | `"New"` |
| cntScrollTT.X | `0` |
| cntScrollTT.Y | `cmpStepperTT.Y+cmpStepperTT.Height` |
| cntScrollTT.Width / Height | `Parent.Width / Max(0,Parent.Height-Self.Y)` |
| cntScrollTT.LayoutDirection | `LayoutDirection.Vertical` |
| cntScrollTT.LayoutOverflowY / LayoutOverflowX | `LayoutOverflow.Scroll / LayoutOverflow.Hide` |
| cntScrollTT.LayoutGap / all paddings | `0` |
| cntPageTT.Width | `Min(1180,Parent.Width)` |
| cntPageTT.AlignInContainer | `AlignInContainer.Center` |
| cntPageTT.FillPortions / LayoutMinWidth / LayoutMinHeight | `0 / 0 / 0` |
| cntPageTT.Height | `cntActionsTT.Y+cntActionsTT.Height+If(App.Width<=760,40,56)` |
| lblHeadingTT.X / Y | `If(App.Width<=760,16,24) / If(App.Width<=760,27,39)` |
| lblHeadingTT.Width / AutoHeight | `Parent.Width-2*Self.X / true` |
| lblHeadingTT.Font / Size | `Font.'Segoe UI' / If(App.Width<=760,18.75,22.5)` |
| lblHeadingTT.Color / FontWeight | `varAppTheme.Heading / FontWeight.Semibold` |
| lblSubtitleTT.X / Y | `lblHeadingTT.X / lblHeadingTT.Y+lblHeadingTT.Height+8` |
| lblSubtitleTT.Width / AutoHeight | `lblHeadingTT.Width / true` |
| lblSubtitleTT.Font / Size / Color | `Font.'Segoe UI' / 11.25 / varAppTheme.Muted` |
| cmpStepperTT.X / Y | `(Parent.Width-Self.Width)/2 / cmpNavTT.Y+cmpNavTT.Height` |
| cmpStepperTT.Width / Height | `Min(1060,Parent.Width) / 94` |
| cmpStepperTT.CurrentStep | `varCurrentStep` |
| cmpStepperTT.CurrentHex | `varAppTheme.PrimaryHex` |
| cmpStepperTT.CompleteHex | `varAppTheme.SuccessHex` |
| cmpStepperTT.PendingHex | `varAppTheme.BorderHex` |
| cmpStepperTT.MutedHex | `varAppTheme.MutedHex` |
| cmpStepperTT.HaloHex | `varAppTheme.PaleHex` |
| Control / property | Value or formula |
|---|---|
| cmpStepperTT.Steps | [Copy full formula](fx/cmpStepperTT.Steps.fx) |

## 3. Navigation events and hidden helpers

| Control / property | Value or formula |
|---|---|
| cmpNavTT.OnNew | [Copy full formula](fx/cmpNavTT.OnNew.fx) |
| cmpNavTT.OnMine | [Copy full formula](fx/cmpNavTT.OnMine.fx) |
| btnStartNewTT.OnSelect | [Copy full New nomination formula](fx/NewNomination.OnSelect.fx) |
| btnGoMineTT.OnSelect | `Navigate(scrMyNominations,ScreenTransition.None)` |
| btnStartNewTT and btnGoMineTT: Visible / DisplayMode | `false / DisplayMode.Edit` |

Paste event formulas on the **component instance**, not its definition. Hidden helpers remain on this same screen.

## 4. Dialog and busy controls — property table

| Control / property | Value or formula |
|---|---|
| cntExitOverlayTT.X / Y / Width / Height | `0 / 0 / Parent.Width / Parent.Height` |
| cntExitOverlayTT.Visible / Fill | `varShowExitDialog / RGBA(0,0,0,0.35)` |
| cntExitDialogTT.Width / Height | `Min(440,Parent.Width-32) / 220` |
| cntExitDialogTT.X / Y | `(Parent.Width-Self.Width)/2 / Max(16,(Parent.Height-Self.Height)/2)` |
| cntExitDialogTT.Fill | `varAppTheme.Surface` |
| lblExitMessageTT.X / Y / Width / Height | `20 / 20 / Parent.Width-40 / 112` |
| lblExitMessageTT.Text | `"Leave this page? Unsaved changes and selected files will be discarded."` |
| btnExitCancelTT.X / Y / Width / Height | `20 / 160 / 110 / 38` |
| btnExitCancelTT.Text / OnSelect | `"Cancel" / Set(varShowExitDialog,false)` |
| btnExitDiscardTT.X / Y / Width / Height | `Parent.Width-140 / 160 / 120 / 38` |
| btnExitDiscardTT.Text | `"Discard"` |
| cntBusyTT.X / Y / Width / Height | `0 / 0 / Parent.Width / Parent.Height` |
| cntBusyTT.Visible / Fill | `varIsBusy / RGBA(255,255,255,0.65)` |
| lblBusyTT.Text / Align | `"Saving or loading…" / Align.Center` |
| lblBusyTT.X / Y / Width / Height | `0 / (Parent.Height-40)/2 / Parent.Width / 40` |
| Control / property | Value or formula |
|---|---|
| btnExitDiscardTT.OnSelect | [Copy full formula](fx/btnExitDiscardTT.OnSelect.fx) |

## 5. Screen content, buttons and formulas



Keep frmSpecialTeamAward inside cntPageTT. Also create lblSaveErrorTT, cntSummaryTT, cntProgressTT and cntActionsTT inside that page. Use [the exact placement table](Reference.md) below for each coordinate; it expands every reference for this screen.

cntActionsTT.Y=`Max(frmSpecialTeamAward.Y+frmSpecialTeamAward.Height,If(lblSaveErrorTT.Visible,lblSaveErrorTT.Y+lblSaveErrorTT.Height,0),cntProgressTT.Y+cntProgressTT.Height)+20`.

Inside cntSummaryTT, create lblSummaryTT: X=20,Y=16,Width=`Max(0,Parent.Width-160)`,AutoHeight=true,Text=`Coalesce(NomineeDisplay,"Details incomplete") & "  •  " & varAwardType & " award" & Char(10) & NominationReference`. Create btnEditDetailsTT: Text="Edit details", X=`Parent.Width-130`,Y=16,Width=110,Height=38,Visible=`!varReadOnly`,OnSelect=`Select(btnTTBack)`.

Inside cntProgressTT, create lblProgressTT: X/Y=16,Width=Parent.Width-32,AutoHeight=true,Text=`Text(CountIf(colAnswers,Slot<=varQuestionCount && !IsBlank(Trim(Response)))) & " of " & Text(varQuestionCount) & " responses entered"`. Add lblProgressHelpTT: X=16,Y=`lblProgressTT.Y+lblProgressTT.Height+10`,Width=Parent.Width-32,AutoHeight=true,Text="Required responses must be completed before review. You can save an incomplete draft.",Visible=`!varReadOnly`. Grow the progress container if long text exceeds its planned height; the action-row Max formula prevents overlap.

| Button in cntActionsTT | X | Y | Width | Text / action |
|---|---|---|---|---|
| btnTTBack | `0` | `0` | `80` | Back / full Back to details block in this form's recipe |
| btnTTSaveDraft | `If(App.Width<=760,92,Parent.Width-278)` | `0` | `120` | Save draft / full btnTTSaveDraft.OnSelect |
| btnTTReview | `If(App.Width<=760,0,Parent.Width-146)` | `If(App.Width<=760,50,0)` | `If(App.Width<=760,Parent.Width,146)` | Review / full btnTTReview.OnSelect |
| btnTTBackToMine | `0` | `0` | `180` | My nominations / `Select(btnGoMineTT)` |

First three buttons Visible=`!varReadOnly`; btnTTBackToMine.Visible=varReadOnly. Back DisplayMode disables while busy; Save disables while busy/read-only/no category; Review disables while busy/read-only. Copy the complete actions from [this form's recipe](Reference.md); do not replace capture/preflight/save handlers with a simple Navigate. Set screen OnVisible=`Set(varCurrentStep,3)`.


### Exact content placement

## scrSpecialTeamAward — placement

| Control / property | Formula / value |
|---|---|
| `cntPageTT.Width` | `Min(1180, Parent.Width)` |
| `lblHeadingTT.X` | `If(App.Width<=760,16,24)` |
| `lblHeadingTT.Width` | `cntPageTT.Width-2*Self.X` |
| `lblHeadingTT.Y` | `If(App.Width<=760,27,39)` |
| `lblHeadingTT.Text` | `If(varReadOnly,"View nomination","Criteria & evidence")` |
| `lblSubtitleTT.Y` | `lblHeadingTT.Y+lblHeadingTT.Height+8` |
| `lblSubtitleTT.Text` | `varCategory.Title` |
| `cntSummaryTT.X / Width` | `lblHeadingTT.X` / `lblHeadingTT.Width` |
| `cntSummaryTT.Y` | `lblSubtitleTT.Y+lblSubtitleTT.Height+18` |
| `cntSummaryTT.Height` | `If(App.Width<=760,112,72)` |
| `cntProgressTT.X` | `If(App.Width<=760,lblHeadingTT.X,lblHeadingTT.X+lblHeadingTT.Width-260)` |
| `cntProgressTT.Y` | `cntSummaryTT.Y+cntSummaryTT.Height+22` |
| `cntProgressTT.Width / Height` | `If(App.Width<=760,lblHeadingTT.Width,260)` / `If(App.Width<=760,100,260)` |
| `frmSpecialTeamAward.X` | `lblHeadingTT.X` |
| `frmSpecialTeamAward.Y` | `If(App.Width<=760,cntProgressTT.Y+cntProgressTT.Height+22,cntProgressTT.Y)` |
| `frmSpecialTeamAward.Width` | `If(App.Width<=760,lblHeadingTT.Width,lblHeadingTT.Width-282)` |
| `lblSaveErrorTT.Y` | `frmSpecialTeamAward.Y+frmSpecialTeamAward.Height+8` |
| `lblSaveErrorTT.X / Width` | `frmSpecialTeamAward.X` / `frmSpecialTeamAward.Width` |
| `lblSaveErrorTT.AutoHeight / Visible / Text` | `true` / `!IsBlank(frmSpecialTeamAward.Error)` / `frmSpecialTeamAward.Error` |
| `cntActionsTT.X / Width` | `lblHeadingTT.X` / `lblHeadingTT.Width` |
| `cntActionsTT.Y` | `Max(frmSpecialTeamAward.Y+frmSpecialTeamAward.Height,If(lblSaveErrorTT.Visible,lblSaveErrorTT.Y+lblSaveErrorTT.Height,0),cntProgressTT.Y+cntProgressTT.Height)+20` |
| `cntActionsTT.Height` | `If(App.Width<=760,96,48)` |
| `cntPageTT.Height` | `cntActionsTT.Y+cntActionsTT.Height+If(App.Width<=760,40,56)` |

Use the explicit sum of error-aware response card heights plus attachment card height +24 from the SpecialTeamAward recipe below. Set subtitle X/Width to the heading X/Width, heading/subtitle AutoHeight=true, and use the common theme typography. Place Save/Review/Back buttons inside cntActionsTT using the shared action-row coordinates. The Details edit button uses the same capture-before-navigation action as btnTTBack. Do not set cntPageTT.Height to the viewport height.



### Build this form and every card

### SpecialTeamAward: TEAM_TRANSFORM / TT

Use the common form-building and scrolling rules above. These formulas target classic controls and English Power Fx separators. They are not yet Studio-compiled or runtime-tested.

#### Controls to create

Screen `scrSpecialTeamAward`; Edit form `frmSpecialTeamAward`; saved-record variable `varRecordTT`; latest-record variable `varLatestTT`. Create six response text inputs `txtTTQ1` … `txtTTQ6` in the corresponding response cards, and keep native attachment input `attTT` inside `dcTTAttachments`.

Form DataSource = `SpecialTeamAward`; Item = `varRecordTT`; DefaultMode = `FormMode.New`; NumberOfColumns = `1`; SnapToColumns = `false`. See layout guide for X/Y/Width/Height. Use the form's generated cards and unlock them. Preserve generated DataField strings exactly; if the connector shows a display name with spaces, use Studio's actual generated identifier. Required = `false` on entry cards to allow incomplete drafts; submission requirements are enforced separately. Do not remove metadata cards just because they are hidden.

Response cards are `dcTTQ1Response` … `dcTTQ6Response`. The other Q cards hold snapshots/flags and are hidden. Do not rename a response card to its text input name.

#### scrSpecialTeamAward.OnVisible

[Copy full formula](fx/scrSpecialTeamAward.01.fx) — paste into the property identified immediately above.


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

[Copy full formula](fx/scrSpecialTeamAward.02.fx) — paste into the property identified immediately above.


#### btnTTReview.OnSelect

Set DisplayMode to `If(varIsBusy || varReadOnly, DisplayMode.Disabled, DisplayMode.Edit)`.

[Copy full formula](fx/scrSpecialTeamAward.03.fx) — paste into the property identified immediately above.


`colCapturedAnswers` prevents clearing the source table while reading its snapshots. Review reads current text controls directly, so it does not depend on OnChange timing. If Studio exposes the native file-name column as DisplayName instead of Name, use that actual column in the one FileName projection above; do not change attachment Items/Update or collect file bodies.

#### frmSpecialTeamAward.OnSuccess

[Copy full formula](fx/scrSpecialTeamAward.04.fx) — paste into the property identified immediately above.


#### frmSpecialTeamAward.OnFailure

[Copy full formula](fx/scrSpecialTeamAward.05.fx) — paste into the property identified immediately above.


#### Back to details

Use a native button; Visible = `!varReadOnly`; DisplayMode disabled while varIsBusy. Its OnSelect:

[Copy full formula](fx/scrSpecialTeamAward.06.fx) — paste into the property identified immediately above.


#### My nominations gallery galMineTT

Visible = `varBrowseCode = "TEAM_TRANSFORM"`. Items:

[Copy full formula](fx/scrSpecialTeamAward.07.fx) — paste into the property identified immediately above.


Use `ThisItem.ID`, `ThisItem.Modified`, `ThisItem.NominationStatus.Value`, and `ThisItem.TeamName` in native labels. Reference Text = `"TEAM_TRANSFORM-" & Text(ThisItem.ID, "000000")`. An Open button inside this gallery uses the following OnSelect; it queries the clicked ID again before opening. Inactive/retired categories can still open historical records.

[Copy full formula](fx/scrSpecialTeamAward.08.fx) — paste into the property identified immediately above.


Submitted items reuse this same typed form in View mode, including native file download. Form entry actions are hidden. This is the read-only screen implementation; a separate duplicate scrViewNomination is unnecessary.

#### Check this category before continuing

Save an incomplete draft, retain its ID, attach a small synthetic file, save again, reopen it, complete required answers, review unsaved changes, and submit. Confirm one item, correct snapshots, declaration and SubmittedOn. Reopen read-only. Test failed save/retry and concurrent modification. Use the full acceptance checklist; no runtime results are claimed here.

#### Question control properties

Insert a manual container inside each response card. Keep these exact unique names. Set label Font to Segoe UI, heading Color to varAppTheme.Heading, body/counter Color to varAppTheme.Muted. All labels wrap. Use the common input styling from the layout guide.

##### Slot 1

| Control / property | Formula or value |
|---|---|
| `dcTTQ1Response.Visible` | `1 <= varQuestionCount` |
| `dcTTQ1Response.X` / Y | `0` / `0` |
| `dcTTQ1Response.Width` | `Parent.Width` |
| `dcTTQ1Response.Height` | `If(Self.Visible, cntTTQ1.Y + cntTTQ1.Height + If(IsBlank(Self.Error), 0, errTTQ1.Height + 8) + 18, 0)` |
| `cntTTQ1` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrSpecialTeamAward.09.fx) — paste into the property identified immediately above.


##### Slot 2

| Control / property | Formula or value |
|---|---|
| `dcTTQ2Response.Visible` | `2 <= varQuestionCount` |
| `dcTTQ2Response.X` / Y | `0` / `1` |
| `dcTTQ2Response.Width` | `Parent.Width` |
| `dcTTQ2Response.Height` | `If(Self.Visible, cntTTQ2.Y + cntTTQ2.Height + If(IsBlank(Self.Error), 0, errTTQ2.Height + 8) + 18, 0)` |
| `cntTTQ2` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrSpecialTeamAward.10.fx) — paste into the property identified immediately above.


##### Slot 3

| Control / property | Formula or value |
|---|---|
| `dcTTQ3Response.Visible` | `3 <= varQuestionCount` |
| `dcTTQ3Response.X` / Y | `0` / `2` |
| `dcTTQ3Response.Width` | `Parent.Width` |
| `dcTTQ3Response.Height` | `If(Self.Visible, cntTTQ3.Y + cntTTQ3.Height + If(IsBlank(Self.Error), 0, errTTQ3.Height + 8) + 18, 0)` |
| `cntTTQ3` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrSpecialTeamAward.11.fx) — paste into the property identified immediately above.


##### Slot 4

| Control / property | Formula or value |
|---|---|
| `dcTTQ4Response.Visible` | `4 <= varQuestionCount` |
| `dcTTQ4Response.X` / Y | `0` / `3` |
| `dcTTQ4Response.Width` | `Parent.Width` |
| `dcTTQ4Response.Height` | `If(Self.Visible, cntTTQ4.Y + cntTTQ4.Height + If(IsBlank(Self.Error), 0, errTTQ4.Height + 8) + 18, 0)` |
| `cntTTQ4` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrSpecialTeamAward.12.fx) — paste into the property identified immediately above.


##### Slot 5

| Control / property | Formula or value |
|---|---|
| `dcTTQ5Response.Visible` | `5 <= varQuestionCount` |
| `dcTTQ5Response.X` / Y | `0` / `4` |
| `dcTTQ5Response.Width` | `Parent.Width` |
| `dcTTQ5Response.Height` | `If(Self.Visible, cntTTQ5.Y + cntTTQ5.Height + If(IsBlank(Self.Error), 0, errTTQ5.Height + 8) + 18, 0)` |
| `cntTTQ5` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrSpecialTeamAward.13.fx) — paste into the property identified immediately above.


##### Slot 6

| Control / property | Formula or value |
|---|---|
| `dcTTQ6Response.Visible` | `6 <= varQuestionCount` |
| `dcTTQ6Response.X` / Y | `0` / `5` |
| `dcTTQ6Response.Width` | `Parent.Width` |
| `dcTTQ6Response.Height` | `If(Self.Visible, cntTTQ6.Y + cntTTQ6.Height + If(IsBlank(Self.Error), 0, errTTQ6.Height + 8) + 18, 0)` |
| `cntTTQ6` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrSpecialTeamAward.14.fx) — paste into the property identified immediately above.


#### SpecialTeamAward: form dimensions and missing-property completion

Set `frmSpecialTeamAward.Width` from its actual parent as described above. Set `frmSpecialTeamAward.Height` to:

[Copy full formula](fx/scrSpecialTeamAward.15.fx) — paste into the property identified immediately above.



Rename each generated response error label as listed. Keep it directly inside the response card, not inside the question container. Set AutoHeight=true, Height=10, X=22, Width=Parent.Width-44, Text=Parent.Error, Visible=!IsBlank(Parent.Error), Color=varAppTheme.Error, Size=9, Live=Live.Assertive. Hide only the redundant generated response field-heading labels.

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

For all six inputs use Font=`Font.'Segoe UI'`, Size=`9.75`, Color=`varAppTheme.Body`, Fill=`varAppTheme.Surface`, BorderThickness=`1`, FocusedBorderColor=`varAppTheme.Primary`, FocusedBorderThickness=`2`, PaddingLeft/Right=`11`, PaddingTop/Bottom=`9`, all corner radii=`4`, and TabIndex=`0`. Set heading Font=`Font.'Segoe UI'` and Color=`varAppTheme.Heading`; prompt/counter Font=`Font.'Segoe UI'` and Color=`varAppTheme.Muted`. Prompt AutoHeight=`true`, base Height=`34`, Size=`9.75`; counter AutoHeight=`false`, Height=`18`. All labels Wrap=`true`.


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

[Copy full formula](fx/scrSpecialTeamAward.16.fx) — paste into the property identified immediately above.


The attachment layout can retain the generated label/editor coordinates. If restyling it, keep the generated error label visible and reserve space for its complete text. Do not suppress native validation messages.

Add a classic label `lblSaveErrorTT` immediately after the form in the scrolling content container. Use the same X and Width as the form, Y=`frmSpecialTeamAward.Y + frmSpecialTeamAward.Height + 8`, AutoHeight=`true`, Text=`frmSpecialTeamAward.Error`, Visible=`!IsBlank(frmSpecialTeamAward.Error)`, Color=`varAppTheme.Error`, and Live=`Live.Assertive`. Place the action row after this label when visible so errors from hidden metadata cards are not lost. Do not reset inputs on failure.


#### SpecialTeamAward: action controls

| Control | Text | Visible | DisplayMode |
|---|---|---|---|
| `btnTTSaveDraft` | `"Save draft"` | `!varReadOnly` | `If(varIsBusy \|\| varReadOnly \|\| !varCategoryComplete, DisplayMode.Disabled, DisplayMode.Edit)` |
| `btnTTReview` | `"Review"` | `!varReadOnly` | `If(varIsBusy \|\| varReadOnly, DisplayMode.Disabled, DisplayMode.Edit)` |
| `btnTTBack` | `"Back to details"` | `!varReadOnly` | `If(varIsBusy, DisplayMode.Disabled, DisplayMode.Edit)` |

Use the complete OnSelect blocks above for these controls. Do not append a status Patch directly after SubmitForm. A read-only Back to My nominations button can use `Navigate(scrMyNominations, ScreenTransition.None)` with Visible=`varReadOnly`.



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
| cmpHeaderTT.LogoImage | [Copy Image formula](fx/Header.LogoImage.fx) |

Before preview, initialize the global palette using [Theme setup](02-Theme.md). Components receive colours through input properties; do not reference app variables inside their definitions.
