# scrBestInnovatorTeam — build sheet

[Back to screen index](../Prod.md) · [Build components once](00-Reusable-Components.md)

Build controls in Tree view order. Insert children under the parent shown.

## 1. Complete Tree view

```text
scrBestInnovatorTeam
  cmpHeaderTC [instance of cmpAppHeader]
  cmpNavTC [instance of cmpAppNav]
  cmpStepperTC [instance of cmpStepper]
  cntScrollTC [Vertical container]
    cntPageTC [plain Container]
      lblHeadingTC [Label]
      lblSubtitleTC [Label]
      cntSummaryTC [Container]
        lblSummaryTC [Label]
        btnEditDetailsTC [Button]
      cntProgressTC [Container]
        lblProgressTC [Label]
        lblProgressHelpTC [Label]
      frmBestInnovatorTeam [Edit form]
        dcTCQ1Response [Data card]
          cntTCQ1 [Container]
            lblTCQ1Heading [Label]
            lblTCQ1Prompt [Label]
            txtTCQ1 [Text input]
            lblTCQ1Counter [Label]
          errTCQ1 [Label]
        dcTCQ2Response [Data card]
          cntTCQ2 [Container]
            lblTCQ2Heading [Label]
            lblTCQ2Prompt [Label]
            txtTCQ2 [Text input]
            lblTCQ2Counter [Label]
          errTCQ2 [Label]
        dcTCQ3Response [Data card]
          cntTCQ3 [Container]
            lblTCQ3Heading [Label]
            lblTCQ3Prompt [Label]
            txtTCQ3 [Text input]
            lblTCQ3Counter [Label]
          errTCQ3 [Label]
        dcTCQ4Response [Data card]
          cntTCQ4 [Container]
            lblTCQ4Heading [Label]
            lblTCQ4Prompt [Label]
            txtTCQ4 [Text input]
            lblTCQ4Counter [Label]
          errTCQ4 [Label]
        dcTCQ5Response [Data card]
          cntTCQ5 [Container]
            lblTCQ5Heading [Label]
            lblTCQ5Prompt [Label]
            txtTCQ5 [Text input]
            lblTCQ5Counter [Label]
          errTCQ5 [Label]
        dcTCQ6Response [Data card]
          cntTCQ6 [Container]
            lblTCQ6Heading [Label]
            lblTCQ6Prompt [Label]
            txtTCQ6 [Text input]
            lblTCQ6Counter [Label]
          errTCQ6 [Label]
        dcTCAttachments [Native attachment card]
          attTC [Native Attachments]
        dcTCTitle [Hidden native card; retain generated child editors]
        dcTCCategory [Hidden native card; retain generated child editors]
        dcTCQuestionSetVersion [Hidden native card; retain generated child editors]
        dcTCQuestionCount [Hidden native card; retain generated child editors]
        dcTCNominatedBy [Hidden native card; retain generated child editors]
        dcTCNominatorEmail [Hidden native card; retain generated child editors]
        dcTCEmployeeRole [Hidden native card; retain generated child editors]
        dcTCEmployeeLevel [Hidden native card; retain generated child editors]
        dcTCNominationStatus [Hidden native card; retain generated child editors]
        dcTCDeclarationAccepted [Hidden native card; retain generated child editors]
        dcTCSubmittedOn [Hidden native card; retain generated child editors]
        dcTCTeamName [Hidden native card; retain generated child editors]
        dcTCTeamPrimaryContact [Hidden native card; retain generated child editors]
        dcTCTeamMembers [Hidden native card; retain generated child editors]
        dcTCQ1PromptSnapshot [Hidden native card; retain generated child editors]
        dcTCQ1RequiredSnapshot [Hidden native card; retain generated child editors]
        dcTCQ2PromptSnapshot [Hidden native card; retain generated child editors]
        dcTCQ2RequiredSnapshot [Hidden native card; retain generated child editors]
        dcTCQ3PromptSnapshot [Hidden native card; retain generated child editors]
        dcTCQ3RequiredSnapshot [Hidden native card; retain generated child editors]
        dcTCQ4PromptSnapshot [Hidden native card; retain generated child editors]
        dcTCQ4RequiredSnapshot [Hidden native card; retain generated child editors]
        dcTCQ5PromptSnapshot [Hidden native card; retain generated child editors]
        dcTCQ5RequiredSnapshot [Hidden native card; retain generated child editors]
        dcTCQ6PromptSnapshot [Hidden native card; retain generated child editors]
        dcTCQ6RequiredSnapshot [Hidden native card; retain generated child editors]
      lblSaveErrorTC [Label]
      cntActionsTC [Container]
        btnTCBack [Button]
        btnTCSaveDraft [Button]
        btnTCReview [Button]
        btnTCBackToMine [Button]
  btnStartNewTC [hidden Button]
  btnGoMineTC [hidden Button]
  cntExitOverlayTC [plain Container]
    cntExitDialogTC [plain Container]
      lblExitMessageTC [Label]
      btnExitCancelTC [Button]
      btnExitDiscardTC [Button]
  cntBusyTC [plain Container]
    lblBusyTC [Label]
```

Component children are created once in the component definitions; they do not need separate per-screen labels/buttons. Native cards keep their generated metadata controls.

## 2. Components and scrolling — property table

Use temporary cntPage height=800 only until the action row exists. Turn Flexible height off. Slash-separated properties map to the slash-separated values in order.

| Control / property | Value or formula |
|---|---|
| scrBestInnovatorTeam.Fill | `varAppTheme.Page` |
| cmpHeaderTC.X / Y | `0 / 0` |
| cmpHeaderTC.Width / Height | `Parent.Width / If(App.Width<=760,58,64)` |
| cmpHeaderTC.BrandText / TitleText | `varAppTheme.Brand / varAppTheme.AppTitle` |
| cmpHeaderTC.UserText | `User().FullName` |
| cmpHeaderTC.HeadingColor / SmallLayout | `varAppTheme.Heading / App.Width<=760` |
| cmpNavTC.X / Y | `0 / cmpHeaderTC.Y+cmpHeaderTC.Height` |
| cmpNavTC.Width / Height | `Parent.Width / 48` |
| cmpNavTC.Busy / AccentColor | `varIsBusy / varAppTheme.Primary` |
| cmpNavTC.ActiveTab | `"New"` |
| cntScrollTC.X | `0` |
| cntScrollTC.Y | `cmpStepperTC.Y+cmpStepperTC.Height` |
| cntScrollTC.Width / Height | `Parent.Width / Max(0,Parent.Height-Self.Y)` |
| cntScrollTC.LayoutDirection | `LayoutDirection.Vertical` |
| cntScrollTC.LayoutOverflowY / LayoutOverflowX | `LayoutOverflow.Scroll / LayoutOverflow.Hide` |
| cntScrollTC.LayoutGap / all paddings | `0` |
| cntPageTC.Width | `Min(1180,Parent.Width)` |
| cntPageTC.AlignInContainer | `AlignInContainer.Center` |
| cntPageTC.FillPortions / LayoutMinWidth / LayoutMinHeight | `0 / 0 / 0` |
| cntPageTC.Height | `cntActionsTC.Y+cntActionsTC.Height+If(App.Width<=760,40,56)` |
| lblHeadingTC.X / Y | `If(App.Width<=760,16,24) / If(App.Width<=760,27,39)` |
| lblHeadingTC.Width / AutoHeight | `Parent.Width-2*Self.X / true` |
| lblHeadingTC.Font / Size | `Font.'Segoe UI' / If(App.Width<=760,18.75,22.5)` |
| lblHeadingTC.Color / FontWeight | `varAppTheme.Heading / FontWeight.Semibold` |
| lblSubtitleTC.X / Y | `lblHeadingTC.X / lblHeadingTC.Y+lblHeadingTC.Height+8` |
| lblSubtitleTC.Width / AutoHeight | `lblHeadingTC.Width / true` |
| lblSubtitleTC.Font / Size / Color | `Font.'Segoe UI' / 11.25 / varAppTheme.Muted` |
| cmpStepperTC.X / Y | `(Parent.Width-Self.Width)/2 / cmpNavTC.Y+cmpNavTC.Height` |
| cmpStepperTC.Width / Height | `Min(1060,Parent.Width) / 94` |
| cmpStepperTC.CurrentStep | `varCurrentStep` |
| cmpStepperTC.CurrentHex | `varAppTheme.PrimaryHex` |
| cmpStepperTC.CompleteHex | `varAppTheme.SuccessHex` |
| cmpStepperTC.PendingHex | `varAppTheme.BorderHex` |
| cmpStepperTC.MutedHex | `varAppTheme.MutedHex` |
| cmpStepperTC.HaloHex | `varAppTheme.PaleHex` |
| Control / property | Value or formula |
|---|---|
| cmpStepperTC.Steps | [Copy full formula](fx/cmpStepperTC.Steps.fx) |

## 3. Navigation events and hidden helpers

| Control / property | Value or formula |
|---|---|
| cmpNavTC.OnNew | [Copy full formula](fx/cmpNavTC.OnNew.fx) |
| cmpNavTC.OnMine | [Copy full formula](fx/cmpNavTC.OnMine.fx) |
| btnStartNewTC.OnSelect | [Copy full New nomination formula](fx/NewNomination.OnSelect.fx) |
| btnGoMineTC.OnSelect | `Navigate(scrMyNominations,ScreenTransition.None)` |
| btnStartNewTC and btnGoMineTC: Visible / DisplayMode | `false / DisplayMode.Edit` |

Paste event formulas on the **component instance**, not its definition. Hidden helpers remain on this same screen.

## 4. Dialog and busy controls — property table

| Control / property | Value or formula |
|---|---|
| cntExitOverlayTC.X / Y / Width / Height | `0 / 0 / Parent.Width / Parent.Height` |
| cntExitOverlayTC.Visible / Fill | `varShowExitDialog / RGBA(0,0,0,0.35)` |
| cntExitDialogTC.Width / Height | `Min(440,Parent.Width-32) / 220` |
| cntExitDialogTC.X / Y | `(Parent.Width-Self.Width)/2 / Max(16,(Parent.Height-Self.Height)/2)` |
| cntExitDialogTC.Fill | `varAppTheme.Surface` |
| lblExitMessageTC.X / Y / Width / Height | `20 / 20 / Parent.Width-40 / 112` |
| lblExitMessageTC.Text | `"Leave this page? Unsaved changes and selected files will be discarded."` |
| btnExitCancelTC.X / Y / Width / Height | `20 / 160 / 110 / 38` |
| btnExitCancelTC.Text / OnSelect | `"Cancel" / Set(varShowExitDialog,false)` |
| btnExitDiscardTC.X / Y / Width / Height | `Parent.Width-140 / 160 / 120 / 38` |
| btnExitDiscardTC.Text | `"Discard"` |
| cntBusyTC.X / Y / Width / Height | `0 / 0 / Parent.Width / Parent.Height` |
| cntBusyTC.Visible / Fill | `varIsBusy / RGBA(255,255,255,0.65)` |
| lblBusyTC.Text / Align | `"Saving or loading…" / Align.Center` |
| lblBusyTC.X / Y / Width / Height | `0 / (Parent.Height-40)/2 / Parent.Width / 40` |
| Control / property | Value or formula |
|---|---|
| btnExitDiscardTC.OnSelect | [Copy full formula](fx/btnExitDiscardTC.OnSelect.fx) |

## 5. Screen content, buttons and formulas



Keep frmBestInnovatorTeam inside cntPageTC. Also create lblSaveErrorTC, cntSummaryTC, cntProgressTC and cntActionsTC inside that page. Use [the exact placement table](Reference.md) below for each coordinate; it expands every reference for this screen.

cntActionsTC.Y=`Max(frmBestInnovatorTeam.Y+frmBestInnovatorTeam.Height,If(lblSaveErrorTC.Visible,lblSaveErrorTC.Y+lblSaveErrorTC.Height,0),cntProgressTC.Y+cntProgressTC.Height)+20`.

Inside cntSummaryTC, create lblSummaryTC: X=20,Y=16,Width=`Max(0,Parent.Width-160)`,AutoHeight=true,Text=`Coalesce(NomineeDisplay,"Details incomplete") & "  •  " & varAwardType & " award" & Char(10) & NominationReference`. Create btnEditDetailsTC: Text="Edit details", X=`Parent.Width-130`,Y=16,Width=110,Height=38,Visible=`!varReadOnly`,OnSelect=`Select(btnTCBack)`.

Inside cntProgressTC, create lblProgressTC: X/Y=16,Width=Parent.Width-32,AutoHeight=true,Text=`Text(CountIf(colAnswers,Slot<=varQuestionCount && !IsBlank(Trim(Response)))) & " of " & Text(varQuestionCount) & " responses entered"`. Add lblProgressHelpTC: X=16,Y=`lblProgressTC.Y+lblProgressTC.Height+10`,Width=Parent.Width-32,AutoHeight=true,Text="Required responses must be completed before review. You can save an incomplete draft.",Visible=`!varReadOnly`. Grow the progress container if long text exceeds its planned height; the action-row Max formula prevents overlap.

| Button in cntActionsTC | X | Y | Width | Text / action |
|---|---|---|---|---|
| btnTCBack | `0` | `0` | `80` | Back / full Back to details block in this form's recipe |
| btnTCSaveDraft | `If(App.Width<=760,92,Parent.Width-278)` | `0` | `120` | Save draft / full btnTCSaveDraft.OnSelect |
| btnTCReview | `If(App.Width<=760,0,Parent.Width-146)` | `If(App.Width<=760,50,0)` | `If(App.Width<=760,Parent.Width,146)` | Review / full btnTCReview.OnSelect |
| btnTCBackToMine | `0` | `0` | `180` | My nominations / `Select(btnGoMineTC)` |

First three buttons Visible=`!varReadOnly`; btnTCBackToMine.Visible=varReadOnly. Back DisplayMode disables while busy; Save disables while busy/read-only/no category; Review disables while busy/read-only. Copy the complete actions from [this form's recipe](Reference.md); do not replace capture/preflight/save handlers with a simple Navigate. Set screen OnVisible=`Set(varCurrentStep,3)`.


### Exact content placement

## scrBestInnovatorTeam — placement

| Control / property | Formula / value |
|---|---|
| `cntPageTC.Width` | `Min(1180, Parent.Width)` |
| `lblHeadingTC.X` | `If(App.Width<=760,16,24)` |
| `lblHeadingTC.Width` | `cntPageTC.Width-2*Self.X` |
| `lblHeadingTC.Y` | `If(App.Width<=760,27,39)` |
| `lblHeadingTC.Text` | `If(varReadOnly,"View nomination","Criteria & evidence")` |
| `lblSubtitleTC.Y` | `lblHeadingTC.Y+lblHeadingTC.Height+8` |
| `lblSubtitleTC.Text` | `varCategory.Title` |
| `cntSummaryTC.X / Width` | `lblHeadingTC.X` / `lblHeadingTC.Width` |
| `cntSummaryTC.Y` | `lblSubtitleTC.Y+lblSubtitleTC.Height+18` |
| `cntSummaryTC.Height` | `If(App.Width<=760,112,72)` |
| `cntProgressTC.X` | `If(App.Width<=760,lblHeadingTC.X,lblHeadingTC.X+lblHeadingTC.Width-260)` |
| `cntProgressTC.Y` | `cntSummaryTC.Y+cntSummaryTC.Height+22` |
| `cntProgressTC.Width / Height` | `If(App.Width<=760,lblHeadingTC.Width,260)` / `If(App.Width<=760,100,260)` |
| `frmBestInnovatorTeam.X` | `lblHeadingTC.X` |
| `frmBestInnovatorTeam.Y` | `If(App.Width<=760,cntProgressTC.Y+cntProgressTC.Height+22,cntProgressTC.Y)` |
| `frmBestInnovatorTeam.Width` | `If(App.Width<=760,lblHeadingTC.Width,lblHeadingTC.Width-282)` |
| `lblSaveErrorTC.Y` | `frmBestInnovatorTeam.Y+frmBestInnovatorTeam.Height+8` |
| `lblSaveErrorTC.X / Width` | `frmBestInnovatorTeam.X` / `frmBestInnovatorTeam.Width` |
| `lblSaveErrorTC.AutoHeight / Visible / Text` | `true` / `!IsBlank(frmBestInnovatorTeam.Error)` / `frmBestInnovatorTeam.Error` |
| `cntActionsTC.X / Width` | `lblHeadingTC.X` / `lblHeadingTC.Width` |
| `cntActionsTC.Y` | `Max(frmBestInnovatorTeam.Y+frmBestInnovatorTeam.Height,If(lblSaveErrorTC.Visible,lblSaveErrorTC.Y+lblSaveErrorTC.Height,0),cntProgressTC.Y+cntProgressTC.Height)+20` |
| `cntActionsTC.Height` | `If(App.Width<=760,96,48)` |
| `cntPageTC.Height` | `cntActionsTC.Y+cntActionsTC.Height+If(App.Width<=760,40,56)` |

Use the explicit sum of error-aware response card heights plus attachment card height +24 from the BestInnovatorTeam recipe below. Set subtitle X/Width to the heading X/Width, heading/subtitle AutoHeight=true, and use the common theme typography. Place Save/Review/Back buttons inside cntActionsTC using the shared action-row coordinates. The Details edit button uses the same capture-before-navigation action as btnTCBack. Do not set cntPageTC.Height to the viewport height.


### Build this form and every card

### BestInnovatorTeam: TEAM_COLLAB / TC

Use the common form-building and scrolling rules above. These formulas target classic controls and English Power Fx separators. They are not yet Studio-compiled or runtime-tested.

#### Controls to create

Screen `scrBestInnovatorTeam`; Edit form `frmBestInnovatorTeam`; saved-record variable `varRecordTC`; latest-record variable `varLatestTC`. Create six response text inputs `txtTCQ1` … `txtTCQ6` in the corresponding response cards, and keep native attachment input `attTC` inside `dcTCAttachments`.

Form DataSource = `BestInnovatorTeam`; Item = `varRecordTC`; DefaultMode = `FormMode.New`; NumberOfColumns = `1`; SnapToColumns = `false`. See layout guide for X/Y/Width/Height. Use the form's generated cards and unlock them. Preserve generated DataField strings exactly; if the connector shows a display name with spaces, use Studio's actual generated identifier. Required = `false` on entry cards to allow incomplete drafts; submission requirements are enforced separately. Do not remove metadata cards just because they are hidden.

Response cards are `dcTCQ1Response` … `dcTCQ6Response`. The other Q cards hold snapshots/flags and are hidden. Do not rename a response card to its text input name.

#### scrBestInnovatorTeam.OnVisible

[Copy full formula](fx/scrBestInnovatorTeam.01.fx) — paste into the property identified immediately above.


Do not call NewForm/ResetForm here: returning from review must preserve inputs and queued files.

#### All card Update properties

| SharePoint DataField / card | Update formula |
|---|---|
| `Title` / `dcTCTitle` | `Left(varCategory.CategoryCode & " - " & If(varAwardType = "Individual", Coalesce(varEmployee.DisplayName, "Draft"), If(IsBlank(Trim(varTeamName)), "Draft", varTeamName)),255)` |
| `Category` / `dcTCCategory` | `{Id: varCategory.ID, Value: varCategory.Title}` |
| `QuestionSetVersion` / `dcTCQuestionSetVersion` | `varQuestionVersion` |
| `QuestionCount` / `dcTCQuestionCount` | `varQuestionCount` |
| `NominatedBy` / `dcTCNominatedBy` | `varNominator` |
| `NominatorEmail` / `dcTCNominatorEmail` | `varUserEmail` |
| `EmployeeRole` / `dcTCEmployeeRole` | `Trim(varRole)` |
| `EmployeeLevel` / `dcTCEmployeeLevel` | `If(IsBlank(varLevel), Blank(), LookUp(Choices(BestInnovatorTeam.EmployeeLevel), Value = varLevel))` |
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

#### btnTCSaveDraft.OnSelect

[Copy full formula](fx/scrBestInnovatorTeam.02.fx) — paste into the property identified immediately above.


#### btnTCReview.OnSelect

Set DisplayMode to `If(varIsBusy || varReadOnly, DisplayMode.Disabled, DisplayMode.Edit)`.

[Copy full formula](fx/scrBestInnovatorTeam.03.fx) — paste into the property identified immediately above.


`colCapturedAnswers` prevents clearing the source table while reading its snapshots. Review reads current text controls directly, so it does not depend on OnChange timing. If Studio exposes the native file-name column as DisplayName instead of Name, use that actual column in the one FileName projection above; do not change attachment Items/Update or collect file bodies.

#### frmBestInnovatorTeam.OnSuccess

[Copy full formula](fx/scrBestInnovatorTeam.04.fx) — paste into the property identified immediately above.


#### frmBestInnovatorTeam.OnFailure

[Copy full formula](fx/scrBestInnovatorTeam.05.fx) — paste into the property identified immediately above.


#### Back to details

Use a native button; Visible = `!varReadOnly`; DisplayMode disabled while varIsBusy. Its OnSelect:

[Copy full formula](fx/scrBestInnovatorTeam.06.fx) — paste into the property identified immediately above.


#### My nominations gallery galMineTC

Visible = `varBrowseCode = "TEAM_COLLAB"`. Items:

[Copy full formula](fx/scrBestInnovatorTeam.07.fx) — paste into the property identified immediately above.


Use `ThisItem.ID`, `ThisItem.Modified`, `ThisItem.NominationStatus.Value`, and `ThisItem.TeamName` in native labels. Reference Text = `"TEAM_COLLAB-" & Text(ThisItem.ID, "000000")`. An Open button inside this gallery uses the following OnSelect; it queries the clicked ID again before opening. Inactive/retired categories can still open historical records.

[Copy full formula](fx/scrBestInnovatorTeam.08.fx) — paste into the property identified immediately above.


Submitted items reuse this same typed form in View mode, including native file download. Form entry actions are hidden. This is the read-only screen implementation; a separate duplicate scrViewNomination is unnecessary.

#### Check this category before continuing

Save an incomplete draft, retain its ID, attach a small synthetic file, save again, reopen it, complete required answers, review unsaved changes, and submit. Confirm one item, correct snapshots, declaration and SubmittedOn. Reopen read-only. Test failed save/retry and concurrent modification. Use the full acceptance checklist; no runtime results are claimed here.

#### Question control properties

Insert a manual container inside each response card. Keep these exact unique names. Set label Font to Segoe UI, heading Color to varAppTheme.Heading, body/counter Color to varAppTheme.Muted. All labels wrap. Use the common input styling from the layout guide.

##### Slot 1

| Control / property | Formula or value |
|---|---|
| `dcTCQ1Response.Visible` | `1 <= varQuestionCount` |
| `dcTCQ1Response.X` / Y | `0` / `0` |
| `dcTCQ1Response.Width` | `Parent.Width` |
| `dcTCQ1Response.Height` | `If(Self.Visible, cntTCQ1.Y + cntTCQ1.Height + If(IsBlank(Self.Error), 0, errTCQ1.Height + 8) + 18, 0)` |
| `cntTCQ1` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrBestInnovatorTeam.09.fx) — paste into the property identified immediately above.


##### Slot 2

| Control / property | Formula or value |
|---|---|
| `dcTCQ2Response.Visible` | `2 <= varQuestionCount` |
| `dcTCQ2Response.X` / Y | `0` / `1` |
| `dcTCQ2Response.Width` | `Parent.Width` |
| `dcTCQ2Response.Height` | `If(Self.Visible, cntTCQ2.Y + cntTCQ2.Height + If(IsBlank(Self.Error), 0, errTCQ2.Height + 8) + 18, 0)` |
| `cntTCQ2` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrBestInnovatorTeam.10.fx) — paste into the property identified immediately above.


##### Slot 3

| Control / property | Formula or value |
|---|---|
| `dcTCQ3Response.Visible` | `3 <= varQuestionCount` |
| `dcTCQ3Response.X` / Y | `0` / `2` |
| `dcTCQ3Response.Width` | `Parent.Width` |
| `dcTCQ3Response.Height` | `If(Self.Visible, cntTCQ3.Y + cntTCQ3.Height + If(IsBlank(Self.Error), 0, errTCQ3.Height + 8) + 18, 0)` |
| `cntTCQ3` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrBestInnovatorTeam.11.fx) — paste into the property identified immediately above.


##### Slot 4

| Control / property | Formula or value |
|---|---|
| `dcTCQ4Response.Visible` | `4 <= varQuestionCount` |
| `dcTCQ4Response.X` / Y | `0` / `3` |
| `dcTCQ4Response.Width` | `Parent.Width` |
| `dcTCQ4Response.Height` | `If(Self.Visible, cntTCQ4.Y + cntTCQ4.Height + If(IsBlank(Self.Error), 0, errTCQ4.Height + 8) + 18, 0)` |
| `cntTCQ4` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrBestInnovatorTeam.12.fx) — paste into the property identified immediately above.


##### Slot 5

| Control / property | Formula or value |
|---|---|
| `dcTCQ5Response.Visible` | `5 <= varQuestionCount` |
| `dcTCQ5Response.X` / Y | `0` / `4` |
| `dcTCQ5Response.Width` | `Parent.Width` |
| `dcTCQ5Response.Height` | `If(Self.Visible, cntTCQ5.Y + cntTCQ5.Height + If(IsBlank(Self.Error), 0, errTCQ5.Height + 8) + 18, 0)` |
| `cntTCQ5` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrBestInnovatorTeam.13.fx) — paste into the property identified immediately above.


##### Slot 6

| Control / property | Formula or value |
|---|---|
| `dcTCQ6Response.Visible` | `6 <= varQuestionCount` |
| `dcTCQ6Response.X` / Y | `0` / `5` |
| `dcTCQ6Response.Width` | `Parent.Width` |
| `dcTCQ6Response.Height` | `If(Self.Visible, cntTCQ6.Y + cntTCQ6.Height + If(IsBlank(Self.Error), 0, errTCQ6.Height + 8) + 18, 0)` |
| `cntTCQ6` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrBestInnovatorTeam.14.fx) — paste into the property identified immediately above.


#### BestInnovatorTeam: form dimensions and missing-property completion

Set `frmBestInnovatorTeam.Width` from its actual parent as described above. Set `frmBestInnovatorTeam.Height` to:

[Copy full formula](fx/scrBestInnovatorTeam.15.fx) — paste into the property identified immediately above.



Rename each generated response error label as listed. Keep it directly inside the response card, not inside the question container. Set AutoHeight=true, Height=10, X=22, Width=Parent.Width-44, Text=Parent.Error, Visible=!IsBlank(Parent.Error), Color=varAppTheme.Error, Size=9, Live=Live.Assertive. Hide only the redundant generated response field-heading labels.

| Error label | Parent card | Y |
|---|---|---|
| `errTCQ1` | `dcTCQ1Response` | `cntTCQ1.Y + cntTCQ1.Height + 4` |
| `errTCQ2` | `dcTCQ2Response` | `cntTCQ2.Y + cntTCQ2.Height + 4` |
| `errTCQ3` | `dcTCQ3Response` | `cntTCQ3.Y + cntTCQ3.Height + 4` |
| `errTCQ4` | `dcTCQ4Response` | `cntTCQ4.Y + cntTCQ4.Height + 4` |
| `errTCQ5` | `dcTCQ5Response` | `cntTCQ5.Y + cntTCQ5.Height + 4` |
| `errTCQ6` | `dcTCQ6Response` | `cntTCQ6.Y + cntTCQ6.Height + 4` |

Set these input properties in addition to the question tables:

| Input | BorderColor | Tooltip |
|---|---|---|
| `txtTCQ1` | `If(IsBlank(dcTCQ1Response.Error), dcTCQ1Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 1, Prompt)` |
| `txtTCQ2` | `If(IsBlank(dcTCQ2Response.Error), dcTCQ2Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 2, Prompt)` |
| `txtTCQ3` | `If(IsBlank(dcTCQ3Response.Error), dcTCQ3Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 3, Prompt)` |
| `txtTCQ4` | `If(IsBlank(dcTCQ4Response.Error), dcTCQ4Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 4, Prompt)` |
| `txtTCQ5` | `If(IsBlank(dcTCQ5Response.Error), dcTCQ5Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 5, Prompt)` |
| `txtTCQ6` | `If(IsBlank(dcTCQ6Response.Error), dcTCQ6Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 6, Prompt)` |

For all six inputs use Font=`Font.'Segoe UI'`, Size=`9.75`, Color=`varAppTheme.Body`, Fill=`varAppTheme.Surface`, BorderThickness=`1`, FocusedBorderColor=`varAppTheme.Primary`, FocusedBorderThickness=`2`, PaddingLeft/Right=`11`, PaddingTop/Bottom=`9`, all corner radii=`4`, and TabIndex=`0`. Set heading Font=`Font.'Segoe UI'` and Color=`varAppTheme.Heading`; prompt/counter Font=`Font.'Segoe UI'` and Color=`varAppTheme.Muted`. Prompt AutoHeight=`true`, base Height=`34`, Size=`9.75`; counter AutoHeight=`false`, Height=`18`. All labels Wrap=`true`.


#### BestInnovatorTeam: native attachments and form-level errors

Keep `attTC` directly inside `dcTCAttachments`. Retain the generated DataField, Items, limits, and native binding settings. Do not replace an attachment control with a collection-backed file picker.

| Property | Value |
|---|---|
| `dcTCAttachments.Visible` | `true` |
| `dcTCAttachments.Width` | `Parent.Width` |
| `dcTCAttachments.Height` | `270` |
| `dcTCAttachments.Required` | `false` |
| `dcTCAttachments.Update` | `attTC.Attachments` |
| `attTC.Items` | `Parent.Default` |
| `attTC.DisplayMode` | `If(varIsBusy, DisplayMode.Disabled, Parent.DisplayMode)` |

For `attTC.OnAddFile`, `attTC.OnRemoveFile`, and `attTC.OnUndoRemoveFile`, use the same action:

[Copy full formula](fx/scrBestInnovatorTeam.16.fx) — paste into the property identified immediately above.


The attachment layout can retain the generated label/editor coordinates. If restyling it, keep the generated error label visible and reserve space for its complete text. Do not suppress native validation messages.

Add a classic label `lblSaveErrorTC` immediately after the form in the scrolling content container. Use the same X and Width as the form, Y=`frmBestInnovatorTeam.Y + frmBestInnovatorTeam.Height + 8`, AutoHeight=`true`, Text=`frmBestInnovatorTeam.Error`, Visible=`!IsBlank(frmBestInnovatorTeam.Error)`, Color=`varAppTheme.Error`, and Live=`Live.Assertive`. Place the action row after this label when visible so errors from hidden metadata cards are not lost. Do not reset inputs on failure.


#### BestInnovatorTeam: action controls

| Control | Text | Visible | DisplayMode |
|---|---|---|---|
| `btnTCSaveDraft` | `"Save draft"` | `!varReadOnly` | `If(varIsBusy \|\| varReadOnly \|\| !varCategoryComplete, DisplayMode.Disabled, DisplayMode.Edit)` |
| `btnTCReview` | `"Review"` | `!varReadOnly` | `If(varIsBusy \|\| varReadOnly, DisplayMode.Disabled, DisplayMode.Edit)` |
| `btnTCBack` | `"Back to details"` | `!varReadOnly` | `If(varIsBusy, DisplayMode.Disabled, DisplayMode.Edit)` |

Use the complete OnSelect blocks above for these controls. Do not append a status Patch directly after SubmitForm. A read-only Back to My nominations button can use `Navigate(scrMyNominations, ScreenTransition.None)` with Visible=`varReadOnly`.


<a id="form-ti"></a>


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
| cmpHeaderTC.LogoImage | [Copy Image formula](fx/Header.LogoImage.fx) |

Before preview, initialize the global palette using [Theme setup](02-Theme.md). Components receive colours through input properties; do not reference app variables inside their definitions.
