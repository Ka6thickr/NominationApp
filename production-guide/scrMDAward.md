# scrMDAward — build sheet

[Back to screen index](../Prod.md) · [Build components once](00-Reusable-Components.md)

**Keep the existing form and corrected cards. Build only the surrounding page controls.**

## 1. Complete Tree view

```text
scrMDAward
  cmpHeaderIC [instance of cmpAppHeader]
  cmpNavIC [instance of cmpAppNav]
  cmpStepperIC [instance of cmpStepper]
  cntScrollIC [Vertical container]
    cntPageIC [plain Container]
      lblHeadingIC [Label]
      lblSubtitleIC [Label]
      cntSummaryIC [Container]
        lblSummaryIC [Label]
        btnEditDetailsIC [Button]
      cntProgressIC [Container]
        lblProgressIC [Label]
        lblProgressHelpIC [Label]
      frmMDAward [Existing Edit form]
      lblSaveErrorIC [Label]
      cntActionsIC [Container]
        btnICBack [Button]
        btnICSaveDraft [Button]
        btnICReview [Button]
        btnICBackToMine [Button]
  btnStartNewIC [hidden Button]
  btnGoMineIC [hidden Button]
  cntExitOverlayIC [plain Container]
    cntExitDialogIC [plain Container]
      lblExitMessageIC [Label]
      btnExitCancelIC [Button]
      btnExitDiscardIC [Button]
  cntBusyIC [plain Container]
    lblBusyIC [Label]
```

Component children are created once in the component definitions; they do not need separate per-screen labels/buttons. Native cards keep their generated metadata controls.

## 2. Components and scrolling — property table

Use temporary cntPage height=800 only until the action row exists. Turn Flexible height off. Slash-separated properties map to the slash-separated values in order.

| Control / property | Value or formula |
|---|---|
| scrMDAward.Fill | `varAppTheme.Page` |
| cmpHeaderIC.X / Y | `0 / 0` |
| cmpHeaderIC.Width / Height | `Parent.Width / If(App.Width<=760,58,64)` |
| cmpHeaderIC.BrandText / TitleText | `varAppTheme.Brand / varAppTheme.AppTitle` |
| cmpHeaderIC.UserText | `User().FullName` |
| cmpHeaderIC.HeadingColor / SmallLayout | `varAppTheme.Heading / App.Width<=760` |
| cmpNavIC.X / Y | `0 / cmpHeaderIC.Y+cmpHeaderIC.Height` |
| cmpNavIC.Width / Height | `Parent.Width / 48` |
| cmpNavIC.Busy / AccentColor | `varIsBusy / varAppTheme.Primary` |
| cmpNavIC.ActiveTab | `"New"` |
| cntScrollIC.X | `0` |
| cntScrollIC.Y | `cmpStepperIC.Y+cmpStepperIC.Height` |
| cntScrollIC.Width / Height | `Parent.Width / Max(0,Parent.Height-Self.Y)` |
| cntScrollIC.LayoutDirection | `LayoutDirection.Vertical` |
| cntScrollIC.LayoutOverflowY / LayoutOverflowX | `LayoutOverflow.Scroll / LayoutOverflow.Hide` |
| cntScrollIC.LayoutGap / all paddings | `0` |
| cntPageIC.Width | `Min(1180,Parent.Width)` |
| cntPageIC.AlignInContainer | `AlignInContainer.Center` |
| cntPageIC.FillPortions / LayoutMinWidth / LayoutMinHeight | `0 / 0 / 0` |
| cntPageIC.Height | `cntActionsIC.Y+cntActionsIC.Height+If(App.Width<=760,40,56)` |
| lblHeadingIC.X / Y | `If(App.Width<=760,16,24) / If(App.Width<=760,27,39)` |
| lblHeadingIC.Width / AutoHeight | `Parent.Width-2*Self.X / true` |
| lblHeadingIC.Font / Size | `Font.'Segoe UI' / If(App.Width<=760,18.75,22.5)` |
| lblHeadingIC.Color / FontWeight | `varAppTheme.Heading / FontWeight.Semibold` |
| lblSubtitleIC.X / Y | `lblHeadingIC.X / lblHeadingIC.Y+lblHeadingIC.Height+8` |
| lblSubtitleIC.Width / AutoHeight | `lblHeadingIC.Width / true` |
| lblSubtitleIC.Font / Size / Color | `Font.'Segoe UI' / 11.25 / varAppTheme.Muted` |
| cmpStepperIC.X / Y | `(Parent.Width-Self.Width)/2 / cmpNavIC.Y+cmpNavIC.Height` |
| cmpStepperIC.Width / Height | `Min(1060,Parent.Width) / 94` |
| cmpStepperIC.CurrentStep | `varCurrentStep` |
| cmpStepperIC.CurrentHex | `varAppTheme.PrimaryHex` |
| cmpStepperIC.CompleteHex | `varAppTheme.SuccessHex` |
| cmpStepperIC.PendingHex | `varAppTheme.BorderHex` |
| cmpStepperIC.MutedHex | `varAppTheme.MutedHex` |
| cmpStepperIC.HaloHex | `varAppTheme.PaleHex` |
| Control / property | Value or formula |
|---|---|
| cmpStepperIC.Steps | [Copy full formula](fx/cmpStepperIC.Steps.fx) |

## 3. Navigation events and hidden helpers

| Control / property | Value or formula |
|---|---|
| cmpNavIC.OnNew | [Copy full formula](fx/cmpNavIC.OnNew.fx) |
| cmpNavIC.OnMine | [Copy full formula](fx/cmpNavIC.OnMine.fx) |
| btnStartNewIC.OnSelect | [Copy full New nomination formula](fx/NewNomination.OnSelect.fx) |
| btnGoMineIC.OnSelect | `Navigate(scrMyNominations,ScreenTransition.None)` |
| btnStartNewIC and btnGoMineIC: Visible / DisplayMode | `false / DisplayMode.Edit` |

Paste event formulas on the **component instance**, not its definition. Hidden helpers remain on this same screen.

## 4. Dialog and busy controls — property table

| Control / property | Value or formula |
|---|---|
| cntExitOverlayIC.X / Y / Width / Height | `0 / 0 / Parent.Width / Parent.Height` |
| cntExitOverlayIC.Visible / Fill | `varShowExitDialog / RGBA(0,0,0,0.35)` |
| cntExitDialogIC.Width / Height | `Min(440,Parent.Width-32) / 220` |
| cntExitDialogIC.X / Y | `(Parent.Width-Self.Width)/2 / Max(16,(Parent.Height-Self.Height)/2)` |
| cntExitDialogIC.Fill | `varAppTheme.Surface` |
| lblExitMessageIC.X / Y / Width / Height | `20 / 20 / Parent.Width-40 / 112` |
| lblExitMessageIC.Text | `"Leave this page? Unsaved changes and selected files will be discarded."` |
| btnExitCancelIC.X / Y / Width / Height | `20 / 160 / 110 / 38` |
| btnExitCancelIC.Text / OnSelect | `"Cancel" / Set(varShowExitDialog,false)` |
| btnExitDiscardIC.X / Y / Width / Height | `Parent.Width-140 / 160 / 120 / 38` |
| btnExitDiscardIC.Text | `"Discard"` |
| cntBusyIC.X / Y / Width / Height | `0 / 0 / Parent.Width / Parent.Height` |
| cntBusyIC.Visible / Fill | `varIsBusy / RGBA(255,255,255,0.65)` |
| lblBusyIC.Text / Align | `"Saving or loading…" / Align.Center` |
| lblBusyIC.X / Y / Width / Height | `0 / (Parent.Height-40)/2 / Parent.Width / 40` |
| Control / property | Value or formula |
|---|---|
| btnExitDiscardIC.OnSelect | [Copy full formula](fx/btnExitDiscardIC.OnSelect.fx) |

## 5. Screen content, buttons and formulas



Keep frmMDAward inside cntPageIC. Also create lblSaveErrorIC, cntSummaryIC, cntProgressIC and cntActionsIC inside that page. Use [the exact placement table](Reference.md) below for each coordinate; it expands every reference for this screen.

cntActionsIC.Y=`Max(frmMDAward.Y+frmMDAward.Height,If(lblSaveErrorIC.Visible,lblSaveErrorIC.Y+lblSaveErrorIC.Height,0),cntProgressIC.Y+cntProgressIC.Height)+20`.

Inside cntSummaryIC, create lblSummaryIC: X=20,Y=16,Width=`Max(0,Parent.Width-160)`,AutoHeight=true,Text=`Coalesce(NomineeDisplay,"Details incomplete") & "  •  " & varAwardType & " award" & Char(10) & NominationReference`. Create btnEditDetailsIC: Text="Edit details", X=`Parent.Width-130`,Y=16,Width=110,Height=38,Visible=`!varReadOnly`,OnSelect=`Select(btnICBack)`.

Inside cntProgressIC, create lblProgressIC: X/Y=16,Width=Parent.Width-32,AutoHeight=true,Text=`Text(CountIf(colAnswers,Slot<=varQuestionCount && !IsBlank(Trim(Response)))) & " of " & Text(varQuestionCount) & " responses entered"`. Add lblProgressHelpIC: X=16,Y=`lblProgressIC.Y+lblProgressIC.Height+10`,Width=Parent.Width-32,AutoHeight=true,Text="Required responses must be completed before review. You can save an incomplete draft.",Visible=`!varReadOnly`. Grow the progress container if long text exceeds its planned height; the action-row Max formula prevents overlap.

| Button in cntActionsIC | X | Y | Width | Text / action |
|---|---|---|---|---|
| btnICBack | `0` | `0` | `80` | Back / full Back to details block in this form's recipe |
| btnICSaveDraft | `If(App.Width<=760,92,Parent.Width-278)` | `0` | `120` | Save draft / full btnICSaveDraft.OnSelect |
| btnICReview | `If(App.Width<=760,0,Parent.Width-146)` | `If(App.Width<=760,50,0)` | `If(App.Width<=760,Parent.Width,146)` | Review / full btnICReview.OnSelect |
| btnICBackToMine | `0` | `0` | `180` | My nominations / `Select(btnGoMineIC)` |

First three buttons Visible=`!varReadOnly`; btnICBackToMine.Visible=varReadOnly. Back DisplayMode disables while busy; Save disables while busy/read-only/no category; Review disables while busy/read-only. Copy the complete actions from [this form's recipe](Reference.md); do not replace capture/preflight/save handlers with a simple Navigate. Set screen OnVisible=`Set(varCurrentStep,3)`.


### Exact content placement

## scrMDAward — placement

| Control / property | Formula / value |
|---|---|
| `cntPageIC.Width` | `Min(1180, Parent.Width)` |
| `lblHeadingIC.X` | `If(App.Width<=760,16,24)` |
| `lblHeadingIC.Width` | `cntPageIC.Width-2*Self.X` |
| `lblHeadingIC.Y` | `If(App.Width<=760,27,39)` |
| `lblHeadingIC.Text` | `If(varReadOnly,"View nomination","Criteria & evidence")` |
| `lblSubtitleIC.Y` | `lblHeadingIC.Y+lblHeadingIC.Height+8` |
| `lblSubtitleIC.Text` | `varCategory.Title` |
| `cntSummaryIC.X / Width` | `lblHeadingIC.X` / `lblHeadingIC.Width` |
| `cntSummaryIC.Y` | `lblSubtitleIC.Y+lblSubtitleIC.Height+18` |
| `cntSummaryIC.Height` | `If(App.Width<=760,112,72)` |
| `cntProgressIC.X` | `If(App.Width<=760,lblHeadingIC.X,lblHeadingIC.X+lblHeadingIC.Width-260)` |
| `cntProgressIC.Y` | `cntSummaryIC.Y+cntSummaryIC.Height+22` |
| `cntProgressIC.Width / Height` | `If(App.Width<=760,lblHeadingIC.Width,260)` / `If(App.Width<=760,100,260)` |
| `frmMDAward.X` | `lblHeadingIC.X` |
| `frmMDAward.Y` | `If(App.Width<=760,cntProgressIC.Y+cntProgressIC.Height+22,cntProgressIC.Y)` |
| `frmMDAward.Width` | `If(App.Width<=760,lblHeadingIC.Width,lblHeadingIC.Width-282)` |
| `lblSaveErrorIC.Y` | `frmMDAward.Y+frmMDAward.Height+8` |
| `lblSaveErrorIC.X / Width` | `frmMDAward.X` / `frmMDAward.Width` |
| `lblSaveErrorIC.AutoHeight / Visible / Text` | `true` / `!IsBlank(frmMDAward.Error)` / `frmMDAward.Error` |
| `cntActionsIC.X / Width` | `lblHeadingIC.X` / `lblHeadingIC.Width` |
| `cntActionsIC.Y` | `Max(frmMDAward.Y+frmMDAward.Height,If(lblSaveErrorIC.Visible,lblSaveErrorIC.Y+lblSaveErrorIC.Height,0),cntProgressIC.Y+cntProgressIC.Height)+20` |
| `cntActionsIC.Height` | `If(App.Width<=760,96,48)` |
| `cntPageIC.Height` | `cntActionsIC.Y+cntActionsIC.Height+If(App.Width<=760,40,56)` |

Use the explicit sum of error-aware response card heights plus attachment card height +24 from the MDAward recipe below. Set subtitle X/Width to the heading X/Width, heading/subtitle AutoHeight=true, and use the common theme typography. Place Save/Review/Back buttons inside cntActionsIC using the shared action-row coordinates. The Details edit button uses the same capture-before-navigation action as btnICBack. Do not set cntPageIC.Height to the viewport height.


### Existing form reference — verify only when needed

### MDAward: IND_CUSTOMER / IC

Use the common form-building and scrolling rules above. These formulas target classic controls and English Power Fx separators. They are not yet Studio-compiled or runtime-tested.

#### Controls to create

Screen `scrMDAward`; Edit form `frmMDAward`; saved-record variable `varRecordIC`; latest-record variable `varLatestIC`. Create six response text inputs `txtICQ1` … `txtICQ6` in the corresponding response cards, and keep native attachment input `attIC` inside `dcICAttachments`.

Form DataSource = `MDAward`; Item = `varRecordIC`; DefaultMode = `FormMode.New`; NumberOfColumns = `1`; SnapToColumns = `false`. See layout guide for X/Y/Width/Height. Use the form's generated cards and unlock them. Preserve generated DataField strings exactly; if the connector shows a display name with spaces, use Studio's actual generated identifier. Required = `false` on entry cards to allow incomplete drafts; submission requirements are enforced separately. Do not remove metadata cards just because they are hidden.

Response cards are `dcICQ1Response` … `dcICQ6Response`. The other Q cards hold snapshots/flags and are hidden. Do not rename a response card to its text input name.

#### scrMDAward.OnVisible

[Copy full formula](fx/scrMDAward.01.fx) — paste into the property identified immediately above.


Do not call NewForm/ResetForm here: returning from review must preserve inputs and queued files.

#### All card Update properties

| SharePoint DataField / card | Update formula |
|---|---|
| `Title` / `dcICTitle` | `Left(varCategory.CategoryCode & " - " & If(varAwardType = "Individual", Coalesce(varEmployee.DisplayName, "Draft"), If(IsBlank(Trim(varTeamName)), "Draft", varTeamName)),255)` |
| `Category` / `dcICCategory` | `{Id: varCategory.ID, Value: varCategory.Title}` |
| `QuestionSetVersion` / `dcICQuestionSetVersion` | `varQuestionVersion` |
| `QuestionCount` / `dcICQuestionCount` | `varQuestionCount` |
| `NominatedBy` / `dcICNominatedBy` | `varNominator` |
| `NominatorEmail` / `dcICNominatorEmail` | `varUserEmail` |
| `EmployeeRole` / `dcICEmployeeRole` | `Trim(varRole)` |
| `EmployeeLevel` / `dcICEmployeeLevel` | `If(IsBlank(varLevel), Blank(), LookUp(Choices(MDAward.EmployeeLevel), Value = varLevel))` |
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

#### btnICSaveDraft.OnSelect

[Copy full formula](fx/scrMDAward.02.fx) — paste into the property identified immediately above.


#### btnICReview.OnSelect

Set DisplayMode to `If(varIsBusy || varReadOnly, DisplayMode.Disabled, DisplayMode.Edit)`.

[Copy full formula](fx/scrMDAward.03.fx) — paste into the property identified immediately above.


`colCapturedAnswers` prevents clearing the source table while reading its snapshots. Review reads current text controls directly, so it does not depend on OnChange timing. If Studio exposes the native file-name column as DisplayName instead of Name, use that actual column in the one FileName projection above; do not change attachment Items/Update or collect file bodies.

#### frmMDAward.OnSuccess

[Copy full formula](fx/scrMDAward.04.fx) — paste into the property identified immediately above.


#### frmMDAward.OnFailure

[Copy full formula](fx/scrMDAward.05.fx) — paste into the property identified immediately above.


#### Back to details

Use a native button; Visible = `!varReadOnly`; DisplayMode disabled while varIsBusy. Its OnSelect:

[Copy full formula](fx/scrMDAward.06.fx) — paste into the property identified immediately above.


#### My nominations gallery galMineIC

Visible = `varBrowseCode = "IND_CUSTOMER"`. Items:

[Copy full formula](fx/scrMDAward.07.fx) — paste into the property identified immediately above.


Use `ThisItem.ID`, `ThisItem.Modified`, `ThisItem.NominationStatus.Value`, and `ThisItem.NominatedEmployee.DisplayName` in native labels. Reference Text = `"IND_CUSTOMER-" & Text(ThisItem.ID, "000000")`. An Open button inside this gallery uses the following OnSelect; it queries the clicked ID again before opening. Inactive/retired categories can still open historical records.

[Copy full formula](fx/scrMDAward.08.fx) — paste into the property identified immediately above.


Submitted items reuse this same typed form in View mode, including native file download. Form entry actions are hidden. This is the read-only screen implementation; a separate duplicate scrViewNomination is unnecessary.

#### Check this category before continuing

Save an incomplete draft, retain its ID, attach a small synthetic file, save again, reopen it, complete required answers, review unsaved changes, and submit. Confirm one item, correct snapshots, declaration and SubmittedOn. Reopen read-only. Test failed save/retry and concurrent modification. Use the full acceptance checklist; no runtime results are claimed here.

#### Question control properties

Insert a manual container inside each response card. Keep these exact unique names. Set label Font to Segoe UI, heading Color to varAppTheme.Heading, body/counter Color to varAppTheme.Muted. All labels wrap. Use the common input styling from the layout guide.

##### Slot 1

| Control / property | Formula or value |
|---|---|
| `dcICQ1Response.Visible` | `1 <= varQuestionCount` |
| `dcICQ1Response.X` / Y | `0` / `0` |
| `dcICQ1Response.Width` | `Parent.Width` |
| `dcICQ1Response.Height` | `If(Self.Visible, cntICQ1.Y + cntICQ1.Height + If(IsBlank(Self.Error), 0, errICQ1.Height + 8) + 18, 0)` |
| `cntICQ1` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrMDAward.09.fx) — paste into the property identified immediately above.


##### Slot 2

| Control / property | Formula or value |
|---|---|
| `dcICQ2Response.Visible` | `2 <= varQuestionCount` |
| `dcICQ2Response.X` / Y | `0` / `1` |
| `dcICQ2Response.Width` | `Parent.Width` |
| `dcICQ2Response.Height` | `If(Self.Visible, cntICQ2.Y + cntICQ2.Height + If(IsBlank(Self.Error), 0, errICQ2.Height + 8) + 18, 0)` |
| `cntICQ2` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrMDAward.10.fx) — paste into the property identified immediately above.


##### Slot 3

| Control / property | Formula or value |
|---|---|
| `dcICQ3Response.Visible` | `3 <= varQuestionCount` |
| `dcICQ3Response.X` / Y | `0` / `2` |
| `dcICQ3Response.Width` | `Parent.Width` |
| `dcICQ3Response.Height` | `If(Self.Visible, cntICQ3.Y + cntICQ3.Height + If(IsBlank(Self.Error), 0, errICQ3.Height + 8) + 18, 0)` |
| `cntICQ3` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrMDAward.11.fx) — paste into the property identified immediately above.


##### Slot 4

| Control / property | Formula or value |
|---|---|
| `dcICQ4Response.Visible` | `4 <= varQuestionCount` |
| `dcICQ4Response.X` / Y | `0` / `3` |
| `dcICQ4Response.Width` | `Parent.Width` |
| `dcICQ4Response.Height` | `If(Self.Visible, cntICQ4.Y + cntICQ4.Height + If(IsBlank(Self.Error), 0, errICQ4.Height + 8) + 18, 0)` |
| `cntICQ4` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrMDAward.12.fx) — paste into the property identified immediately above.


##### Slot 5

| Control / property | Formula or value |
|---|---|
| `dcICQ5Response.Visible` | `5 <= varQuestionCount` |
| `dcICQ5Response.X` / Y | `0` / `4` |
| `dcICQ5Response.Width` | `Parent.Width` |
| `dcICQ5Response.Height` | `If(Self.Visible, cntICQ5.Y + cntICQ5.Height + If(IsBlank(Self.Error), 0, errICQ5.Height + 8) + 18, 0)` |
| `cntICQ5` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrMDAward.13.fx) — paste into the property identified immediately above.


##### Slot 6

| Control / property | Formula or value |
|---|---|
| `dcICQ6Response.Visible` | `6 <= varQuestionCount` |
| `dcICQ6Response.X` / Y | `0` / `5` |
| `dcICQ6Response.Width` | `Parent.Width` |
| `dcICQ6Response.Height` | `If(Self.Visible, cntICQ6.Y + cntICQ6.Height + If(IsBlank(Self.Error), 0, errICQ6.Height + 8) + 18, 0)` |
| `cntICQ6` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrMDAward.14.fx) — paste into the property identified immediately above.


#### MDAward: form dimensions and missing-property completion

Set `frmMDAward.Width` from its actual parent as described above. Set `frmMDAward.Height` to:

[Copy full formula](fx/scrMDAward.15.fx) — paste into the property identified immediately above.



Rename each generated response error label as listed. Keep it directly inside the response card, not inside the question container. Set AutoHeight=true, Height=10, X=22, Width=Parent.Width-44, Text=Parent.Error, Visible=!IsBlank(Parent.Error), Color=varAppTheme.Error, Size=9, Live=Live.Assertive. Hide only the redundant generated response field-heading labels.

| Error label | Parent card | Y |
|---|---|---|
| `errICQ1` | `dcICQ1Response` | `cntICQ1.Y + cntICQ1.Height + 4` |
| `errICQ2` | `dcICQ2Response` | `cntICQ2.Y + cntICQ2.Height + 4` |
| `errICQ3` | `dcICQ3Response` | `cntICQ3.Y + cntICQ3.Height + 4` |
| `errICQ4` | `dcICQ4Response` | `cntICQ4.Y + cntICQ4.Height + 4` |
| `errICQ5` | `dcICQ5Response` | `cntICQ5.Y + cntICQ5.Height + 4` |
| `errICQ6` | `dcICQ6Response` | `cntICQ6.Y + cntICQ6.Height + 4` |

Set these input properties in addition to the question tables:

| Input | BorderColor | Tooltip |
|---|---|---|
| `txtICQ1` | `If(IsBlank(dcICQ1Response.Error), dcICQ1Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 1, Prompt)` |
| `txtICQ2` | `If(IsBlank(dcICQ2Response.Error), dcICQ2Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 2, Prompt)` |
| `txtICQ3` | `If(IsBlank(dcICQ3Response.Error), dcICQ3Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 3, Prompt)` |
| `txtICQ4` | `If(IsBlank(dcICQ4Response.Error), dcICQ4Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 4, Prompt)` |
| `txtICQ5` | `If(IsBlank(dcICQ5Response.Error), dcICQ5Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 5, Prompt)` |
| `txtICQ6` | `If(IsBlank(dcICQ6Response.Error), dcICQ6Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 6, Prompt)` |

For all six inputs use Font=`Font.'Segoe UI'`, Size=`9.75`, Color=`varAppTheme.Body`, Fill=`varAppTheme.Surface`, BorderThickness=`1`, FocusedBorderColor=`varAppTheme.Primary`, FocusedBorderThickness=`2`, PaddingLeft/Right=`11`, PaddingTop/Bottom=`9`, all corner radii=`4`, and TabIndex=`0`. Set heading Font=`Font.'Segoe UI'` and Color=`varAppTheme.Heading`; prompt/counter Font=`Font.'Segoe UI'` and Color=`varAppTheme.Muted`. Prompt AutoHeight=`true`, base Height=`34`, Size=`9.75`; counter AutoHeight=`false`, Height=`18`. All labels Wrap=`true`.


#### MDAward: native attachments and form-level errors

Keep `attIC` directly inside `dcICAttachments`. Retain the generated DataField, Items, limits, and native binding settings. Do not replace an attachment control with a collection-backed file picker.

| Property | Value |
|---|---|
| `dcICAttachments.Visible` | `true` |
| `dcICAttachments.Width` | `Parent.Width` |
| `dcICAttachments.Height` | `270` |
| `dcICAttachments.Required` | `false` |
| `dcICAttachments.Update` | `attIC.Attachments` |
| `attIC.Items` | `Parent.Default` |
| `attIC.DisplayMode` | `If(varIsBusy, DisplayMode.Disabled, Parent.DisplayMode)` |

For `attIC.OnAddFile`, `attIC.OnRemoveFile`, and `attIC.OnUndoRemoveFile`, use the same action:

[Copy full formula](fx/scrMDAward.16.fx) — paste into the property identified immediately above.


The attachment layout can retain the generated label/editor coordinates. If restyling it, keep the generated error label visible and reserve space for its complete text. Do not suppress native validation messages.

Add a classic label `lblSaveErrorIC` immediately after the form in the scrolling content container. Use the same X and Width as the form, Y=`frmMDAward.Y + frmMDAward.Height + 8`, AutoHeight=`true`, Text=`frmMDAward.Error`, Visible=`!IsBlank(frmMDAward.Error)`, Color=`varAppTheme.Error`, and Live=`Live.Assertive`. Place the action row after this label when visible so errors from hidden metadata cards are not lost. Do not reset inputs on failure.


#### MDAward: action controls

| Control | Text | Visible | DisplayMode |
|---|---|---|---|
| `btnICSaveDraft` | `"Save draft"` | `!varReadOnly` | `If(varIsBusy \|\| varReadOnly \|\| !varCategoryComplete, DisplayMode.Disabled, DisplayMode.Edit)` |
| `btnICReview` | `"Review"` | `!varReadOnly` | `If(varIsBusy \|\| varReadOnly, DisplayMode.Disabled, DisplayMode.Edit)` |
| `btnICBack` | `"Back to details"` | `!varReadOnly` | `If(varIsBusy, DisplayMode.Disabled, DisplayMode.Edit)` |

Use the complete OnSelect blocks above for these controls. Do not append a status Patch directly after SubmitForm. A read-only Back to My nominations button can use `Navigate(scrMyNominations, ScreenTransition.None)` with Visible=`varReadOnly`.


<a id="form-ie"></a>


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
| cmpHeaderIC.LogoImage | [Copy Image formula](fx/Header.LogoImage.fx) |

Before preview, initialize the global palette using [Theme setup](02-Theme.md). Components receive colours through input properties; do not reference app variables inside their definitions.
