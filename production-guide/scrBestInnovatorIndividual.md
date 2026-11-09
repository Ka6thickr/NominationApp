# scrBestInnovatorIndividual — build sheet

[Back to screen index](../Prod.md) · [Build components once](00-Reusable-Components.md)

**Keep the existing form and corrected cards. Build only the surrounding page controls.**

## 1. Complete Tree view

```text
scrBestInnovatorIndividual
  cmpHeaderII [instance of cmpAppHeader]
  cmpNavII [instance of cmpAppNav]
  cmpStepperII [instance of cmpStepper]
  cntScrollII [Vertical container]
    cntPageII [plain Container]
      lblHeadingII [Label]
      lblSubtitleII [Label]
      cntSummaryII [Container]
        lblSummaryII [Label]
        btnEditDetailsII [Button]
      cntProgressII [Container]
        lblProgressII [Label]
        lblProgressHelpII [Label]
      frmBestInnovatorIndividual [Existing Edit form]
      lblSaveErrorII [Label]
      cntActionsII [Container]
        btnIIBack [Button]
        btnIISaveDraft [Button]
        btnIIReview [Button]
        btnIIBackToMine [Button]
  btnStartNewII [hidden Button]
  btnGoMineII [hidden Button]
  cntExitOverlayII [plain Container]
    cntExitDialogII [plain Container]
      lblExitMessageII [Label]
      btnExitCancelII [Button]
      btnExitDiscardII [Button]
  cntBusyII [plain Container]
    lblBusyII [Label]
```

Component children are created once in the component definitions; they do not need separate per-screen labels/buttons. Native cards keep their generated metadata controls.

## 2. Components and scrolling — property table

Use temporary cntPage height=800 only until the action row exists. Turn Flexible height off. Slash-separated properties map to the slash-separated values in order.

| Control / property | Value or formula |
|---|---|
| scrBestInnovatorIndividual.Fill | `varAppTheme.Page` |
| cmpHeaderII.X / Y | `0 / 0` |
| cmpHeaderII.Width / Height | `Parent.Width / If(App.Width<=760,58,64)` |
| cmpHeaderII.BrandText / TitleText | `varAppTheme.Brand / varAppTheme.AppTitle` |
| cmpHeaderII.UserText | `User().FullName` |
| cmpHeaderII.HeadingColor / SmallLayout | `varAppTheme.Heading / App.Width<=760` |
| cmpNavII.X / Y | `0 / cmpHeaderII.Y+cmpHeaderII.Height` |
| cmpNavII.Width / Height | `Parent.Width / 48` |
| cmpNavII.Busy / AccentColor | `varIsBusy / varAppTheme.Primary` |
| cmpNavII.ActiveTab | `"New"` |
| cntScrollII.X | `0` |
| cntScrollII.Y | `cmpStepperII.Y+cmpStepperII.Height` |
| cntScrollII.Width / Height | `Parent.Width / Max(0,Parent.Height-Self.Y)` |
| cntScrollII.LayoutDirection | `LayoutDirection.Vertical` |
| cntScrollII.LayoutOverflowY / LayoutOverflowX | `LayoutOverflow.Scroll / LayoutOverflow.Hide` |
| cntScrollII.LayoutGap / all paddings | `0` |
| cntPageII.Width | `Min(1180,Parent.Width)` |
| cntPageII.AlignInContainer | `AlignInContainer.Center` |
| cntPageII.FillPortions / LayoutMinWidth / LayoutMinHeight | `0 / 0 / 0` |
| cntPageII.Height | `cntActionsII.Y+cntActionsII.Height+If(App.Width<=760,40,56)` |
| lblHeadingII.X / Y | `If(App.Width<=760,16,24) / If(App.Width<=760,27,39)` |
| lblHeadingII.Width / AutoHeight | `Parent.Width-2*Self.X / true` |
| lblHeadingII.Font / Size | `Font.'Segoe UI' / If(App.Width<=760,18.75,22.5)` |
| lblHeadingII.Color / FontWeight | `varAppTheme.Heading / FontWeight.Semibold` |
| lblSubtitleII.X / Y | `lblHeadingII.X / lblHeadingII.Y+lblHeadingII.Height+8` |
| lblSubtitleII.Width / AutoHeight | `lblHeadingII.Width / true` |
| lblSubtitleII.Font / Size / Color | `Font.'Segoe UI' / 11.25 / varAppTheme.Muted` |
| cmpStepperII.X / Y | `(Parent.Width-Self.Width)/2 / cmpNavII.Y+cmpNavII.Height` |
| cmpStepperII.Width / Height | `Min(1060,Parent.Width) / 94` |
| cmpStepperII.CurrentStep | `varCurrentStep` |
| cmpStepperII.CurrentHex | `varAppTheme.PrimaryHex` |
| cmpStepperII.CompleteHex | `varAppTheme.SuccessHex` |
| cmpStepperII.PendingHex | `varAppTheme.BorderHex` |
| cmpStepperII.MutedHex | `varAppTheme.MutedHex` |
| cmpStepperII.HaloHex | `varAppTheme.PaleHex` |
| Control / property | Value or formula |
|---|---|
| cmpStepperII.Steps | [Copy full formula](fx/cmpStepperII.Steps.fx) |

## 3. Navigation events and hidden helpers

| Control / property | Value or formula |
|---|---|
| cmpNavII.OnNew | [Copy full formula](fx/cmpNavII.OnNew.fx) |
| cmpNavII.OnMine | [Copy full formula](fx/cmpNavII.OnMine.fx) |
| btnStartNewII.OnSelect | [Copy full New nomination formula](fx/NewNomination.OnSelect.fx) |
| btnGoMineII.OnSelect | `Navigate(scrMyNominations,ScreenTransition.None)` |
| btnStartNewII and btnGoMineII: Visible / DisplayMode | `false / DisplayMode.Edit` |

Paste event formulas on the **component instance**, not its definition. Hidden helpers remain on this same screen.

## 4. Dialog and busy controls — property table

| Control / property | Value or formula |
|---|---|
| cntExitOverlayII.X / Y / Width / Height | `0 / 0 / Parent.Width / Parent.Height` |
| cntExitOverlayII.Visible / Fill | `varShowExitDialog / RGBA(0,0,0,0.35)` |
| cntExitDialogII.Width / Height | `Min(440,Parent.Width-32) / 220` |
| cntExitDialogII.X / Y | `(Parent.Width-Self.Width)/2 / Max(16,(Parent.Height-Self.Height)/2)` |
| cntExitDialogII.Fill | `varAppTheme.Surface` |
| lblExitMessageII.X / Y / Width / Height | `20 / 20 / Parent.Width-40 / 112` |
| lblExitMessageII.Text | `"Leave this page? Unsaved changes and selected files will be discarded."` |
| btnExitCancelII.X / Y / Width / Height | `20 / 160 / 110 / 38` |
| btnExitCancelII.Text / OnSelect | `"Cancel" / Set(varShowExitDialog,false)` |
| btnExitDiscardII.X / Y / Width / Height | `Parent.Width-140 / 160 / 120 / 38` |
| btnExitDiscardII.Text | `"Discard"` |
| cntBusyII.X / Y / Width / Height | `0 / 0 / Parent.Width / Parent.Height` |
| cntBusyII.Visible / Fill | `varIsBusy / RGBA(255,255,255,0.65)` |
| lblBusyII.Text / Align | `"Saving or loading…" / Align.Center` |
| lblBusyII.X / Y / Width / Height | `0 / (Parent.Height-40)/2 / Parent.Width / 40` |
| Control / property | Value or formula |
|---|---|
| btnExitDiscardII.OnSelect | [Copy full formula](fx/btnExitDiscardII.OnSelect.fx) |

## 5. Screen content, buttons and formulas



Keep frmBestInnovatorIndividual inside cntPageII. Also create lblSaveErrorII, cntSummaryII, cntProgressII and cntActionsII inside that page. Use [the exact placement table](Reference.md) below for each coordinate; it expands every reference for this screen.

cntActionsII.Y=`Max(frmBestInnovatorIndividual.Y+frmBestInnovatorIndividual.Height,If(lblSaveErrorII.Visible,lblSaveErrorII.Y+lblSaveErrorII.Height,0),cntProgressII.Y+cntProgressII.Height)+20`.

Inside cntSummaryII, create lblSummaryII: X=20,Y=16,Width=`Max(0,Parent.Width-160)`,AutoHeight=true,Text=`Coalesce(NomineeDisplay,"Details incomplete") & "  •  " & varAwardType & " award" & Char(10) & NominationReference`. Create btnEditDetailsII: Text="Edit details", X=`Parent.Width-130`,Y=16,Width=110,Height=38,Visible=`!varReadOnly`,OnSelect=`Select(btnIIBack)`.

Inside cntProgressII, create lblProgressII: X/Y=16,Width=Parent.Width-32,AutoHeight=true,Text=`Text(CountIf(colAnswers,Slot<=varQuestionCount && !IsBlank(Trim(Response)))) & " of " & Text(varQuestionCount) & " responses entered"`. Add lblProgressHelpII: X=16,Y=`lblProgressII.Y+lblProgressII.Height+10`,Width=Parent.Width-32,AutoHeight=true,Text="Required responses must be completed before review. You can save an incomplete draft.",Visible=`!varReadOnly`. Grow the progress container if long text exceeds its planned height; the action-row Max formula prevents overlap.

| Button in cntActionsII | X | Y | Width | Text / action |
|---|---|---|---|---|
| btnIIBack | `0` | `0` | `80` | Back / full Back to details block in this form's recipe |
| btnIISaveDraft | `If(App.Width<=760,92,Parent.Width-278)` | `0` | `120` | Save draft / full btnIISaveDraft.OnSelect |
| btnIIReview | `If(App.Width<=760,0,Parent.Width-146)` | `If(App.Width<=760,50,0)` | `If(App.Width<=760,Parent.Width,146)` | Review / full btnIIReview.OnSelect |
| btnIIBackToMine | `0` | `0` | `180` | My nominations / `Select(btnGoMineII)` |

First three buttons Visible=`!varReadOnly`; btnIIBackToMine.Visible=varReadOnly. Back DisplayMode disables while busy; Save disables while busy/read-only/no category; Review disables while busy/read-only. Copy the complete actions from [this form's recipe](Reference.md); do not replace capture/preflight/save handlers with a simple Navigate. Set screen OnVisible=`Set(varCurrentStep,3)`.


### Exact content placement

## scrBestInnovatorIndividual — placement

| Control / property | Formula / value |
|---|---|
| `cntPageII.Width` | `Min(1180, Parent.Width)` |
| `lblHeadingII.X` | `If(App.Width<=760,16,24)` |
| `lblHeadingII.Width` | `cntPageII.Width-2*Self.X` |
| `lblHeadingII.Y` | `If(App.Width<=760,27,39)` |
| `lblHeadingII.Text` | `If(varReadOnly,"View nomination","Criteria & evidence")` |
| `lblSubtitleII.Y` | `lblHeadingII.Y+lblHeadingII.Height+8` |
| `lblSubtitleII.Text` | `varCategory.Title` |
| `cntSummaryII.X / Width` | `lblHeadingII.X` / `lblHeadingII.Width` |
| `cntSummaryII.Y` | `lblSubtitleII.Y+lblSubtitleII.Height+18` |
| `cntSummaryII.Height` | `If(App.Width<=760,112,72)` |
| `cntProgressII.X` | `If(App.Width<=760,lblHeadingII.X,lblHeadingII.X+lblHeadingII.Width-260)` |
| `cntProgressII.Y` | `cntSummaryII.Y+cntSummaryII.Height+22` |
| `cntProgressII.Width / Height` | `If(App.Width<=760,lblHeadingII.Width,260)` / `If(App.Width<=760,100,260)` |
| `frmBestInnovatorIndividual.X` | `lblHeadingII.X` |
| `frmBestInnovatorIndividual.Y` | `If(App.Width<=760,cntProgressII.Y+cntProgressII.Height+22,cntProgressII.Y)` |
| `frmBestInnovatorIndividual.Width` | `If(App.Width<=760,lblHeadingII.Width,lblHeadingII.Width-282)` |
| `lblSaveErrorII.Y` | `frmBestInnovatorIndividual.Y+frmBestInnovatorIndividual.Height+8` |
| `lblSaveErrorII.X / Width` | `frmBestInnovatorIndividual.X` / `frmBestInnovatorIndividual.Width` |
| `lblSaveErrorII.AutoHeight / Visible / Text` | `true` / `!IsBlank(frmBestInnovatorIndividual.Error)` / `frmBestInnovatorIndividual.Error` |
| `cntActionsII.X / Width` | `lblHeadingII.X` / `lblHeadingII.Width` |
| `cntActionsII.Y` | `Max(frmBestInnovatorIndividual.Y+frmBestInnovatorIndividual.Height,If(lblSaveErrorII.Visible,lblSaveErrorII.Y+lblSaveErrorII.Height,0),cntProgressII.Y+cntProgressII.Height)+20` |
| `cntActionsII.Height` | `If(App.Width<=760,96,48)` |
| `cntPageII.Height` | `cntActionsII.Y+cntActionsII.Height+If(App.Width<=760,40,56)` |

Use the explicit sum of error-aware response card heights plus attachment card height +24 from the BestInnovatorIndividual recipe below. Set subtitle X/Width to the heading X/Width, heading/subtitle AutoHeight=true, and use the common theme typography. Place Save/Review/Back buttons inside cntActionsII using the shared action-row coordinates. The Details edit button uses the same capture-before-navigation action as btnIIBack. Do not set cntPageII.Height to the viewport height.


### Existing form reference — verify only when needed

### BestInnovatorIndividual: IND_INNOVATION / II

Use the common form-building and scrolling rules above. These formulas target classic controls and English Power Fx separators. They are not yet Studio-compiled or runtime-tested.

#### Controls to create

Screen `scrBestInnovatorIndividual`; Edit form `frmBestInnovatorIndividual`; saved-record variable `varRecordII`; latest-record variable `varLatestII`. Create six response text inputs `txtIIQ1` … `txtIIQ6` in the corresponding response cards, and keep native attachment input `attII` inside `dcIIAttachments`.

Form DataSource = `BestInnovatorIndividual`; Item = `varRecordII`; DefaultMode = `FormMode.New`; NumberOfColumns = `1`; SnapToColumns = `false`. See layout guide for X/Y/Width/Height. Use the form's generated cards and unlock them. Preserve generated DataField strings exactly; if the connector shows a display name with spaces, use Studio's actual generated identifier. Required = `false` on entry cards to allow incomplete drafts; submission requirements are enforced separately. Do not remove metadata cards just because they are hidden.

Response cards are `dcIIQ1Response` … `dcIIQ6Response`. The other Q cards hold snapshots/flags and are hidden. Do not rename a response card to its text input name.

#### scrBestInnovatorIndividual.OnVisible

[Copy full formula](fx/scrBestInnovatorIndividual.01.fx) — paste into the property identified immediately above.


Do not call NewForm/ResetForm here: returning from review must preserve inputs and queued files.

#### All card Update properties

| SharePoint DataField / card | Update formula |
|---|---|
| `Title` / `dcIITitle` | `Left(varCategory.CategoryCode & " - " & If(varAwardType = "Individual", Coalesce(varEmployee.DisplayName, "Draft"), If(IsBlank(Trim(varTeamName)), "Draft", varTeamName)),255)` |
| `Category` / `dcIICategory` | `{Id: varCategory.ID, Value: varCategory.Title}` |
| `QuestionSetVersion` / `dcIIQuestionSetVersion` | `varQuestionVersion` |
| `QuestionCount` / `dcIIQuestionCount` | `varQuestionCount` |
| `NominatedBy` / `dcIINominatedBy` | `varNominator` |
| `NominatorEmail` / `dcIINominatorEmail` | `varUserEmail` |
| `EmployeeRole` / `dcIIEmployeeRole` | `Trim(varRole)` |
| `EmployeeLevel` / `dcIIEmployeeLevel` | `If(IsBlank(varLevel), Blank(), LookUp(Choices(BestInnovatorIndividual.EmployeeLevel), Value = varLevel))` |
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

#### btnIISaveDraft.OnSelect

[Copy full formula](fx/scrBestInnovatorIndividual.02.fx) — paste into the property identified immediately above.


#### btnIIReview.OnSelect

Set DisplayMode to `If(varIsBusy || varReadOnly, DisplayMode.Disabled, DisplayMode.Edit)`.

[Copy full formula](fx/scrBestInnovatorIndividual.03.fx) — paste into the property identified immediately above.


`colCapturedAnswers` prevents clearing the source table while reading its snapshots. Review reads current text controls directly, so it does not depend on OnChange timing. If Studio exposes the native file-name column as DisplayName instead of Name, use that actual column in the one FileName projection above; do not change attachment Items/Update or collect file bodies.

#### frmBestInnovatorIndividual.OnSuccess

[Copy full formula](fx/scrBestInnovatorIndividual.04.fx) — paste into the property identified immediately above.


#### frmBestInnovatorIndividual.OnFailure

[Copy full formula](fx/scrBestInnovatorIndividual.05.fx) — paste into the property identified immediately above.


#### Back to details

Use a native button; Visible = `!varReadOnly`; DisplayMode disabled while varIsBusy. Its OnSelect:

[Copy full formula](fx/scrBestInnovatorIndividual.06.fx) — paste into the property identified immediately above.


#### My nominations gallery galMineII

Visible = `varBrowseCode = "IND_INNOVATION"`. Items:

[Copy full formula](fx/scrBestInnovatorIndividual.07.fx) — paste into the property identified immediately above.


Use `ThisItem.ID`, `ThisItem.Modified`, `ThisItem.NominationStatus.Value`, and `ThisItem.NominatedEmployee.DisplayName` in native labels. Reference Text = `"IND_INNOVATION-" & Text(ThisItem.ID, "000000")`. An Open button inside this gallery uses the following OnSelect; it queries the clicked ID again before opening. Inactive/retired categories can still open historical records.

[Copy full formula](fx/scrBestInnovatorIndividual.08.fx) — paste into the property identified immediately above.


Submitted items reuse this same typed form in View mode, including native file download. Form entry actions are hidden. This is the read-only screen implementation; a separate duplicate scrViewNomination is unnecessary.

#### Check this category before continuing

Save an incomplete draft, retain its ID, attach a small synthetic file, save again, reopen it, complete required answers, review unsaved changes, and submit. Confirm one item, correct snapshots, declaration and SubmittedOn. Reopen read-only. Test failed save/retry and concurrent modification. Use the full acceptance checklist; no runtime results are claimed here.

#### Question control properties

Insert a manual container inside each response card. Keep these exact unique names. Set label Font to Segoe UI, heading Color to varAppTheme.Heading, body/counter Color to varAppTheme.Muted. All labels wrap. Use the common input styling from the layout guide.

##### Slot 1

| Control / property | Formula or value |
|---|---|
| `dcIIQ1Response.Visible` | `1 <= varQuestionCount` |
| `dcIIQ1Response.X` / Y | `0` / `0` |
| `dcIIQ1Response.Width` | `Parent.Width` |
| `dcIIQ1Response.Height` | `If(Self.Visible, cntIIQ1.Y + cntIIQ1.Height + If(IsBlank(Self.Error), 0, errIIQ1.Height + 8) + 18, 0)` |
| `cntIIQ1` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrBestInnovatorIndividual.09.fx) — paste into the property identified immediately above.


##### Slot 2

| Control / property | Formula or value |
|---|---|
| `dcIIQ2Response.Visible` | `2 <= varQuestionCount` |
| `dcIIQ2Response.X` / Y | `0` / `1` |
| `dcIIQ2Response.Width` | `Parent.Width` |
| `dcIIQ2Response.Height` | `If(Self.Visible, cntIIQ2.Y + cntIIQ2.Height + If(IsBlank(Self.Error), 0, errIIQ2.Height + 8) + 18, 0)` |
| `cntIIQ2` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrBestInnovatorIndividual.10.fx) — paste into the property identified immediately above.


##### Slot 3

| Control / property | Formula or value |
|---|---|
| `dcIIQ3Response.Visible` | `3 <= varQuestionCount` |
| `dcIIQ3Response.X` / Y | `0` / `2` |
| `dcIIQ3Response.Width` | `Parent.Width` |
| `dcIIQ3Response.Height` | `If(Self.Visible, cntIIQ3.Y + cntIIQ3.Height + If(IsBlank(Self.Error), 0, errIIQ3.Height + 8) + 18, 0)` |
| `cntIIQ3` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrBestInnovatorIndividual.11.fx) — paste into the property identified immediately above.


##### Slot 4

| Control / property | Formula or value |
|---|---|
| `dcIIQ4Response.Visible` | `4 <= varQuestionCount` |
| `dcIIQ4Response.X` / Y | `0` / `3` |
| `dcIIQ4Response.Width` | `Parent.Width` |
| `dcIIQ4Response.Height` | `If(Self.Visible, cntIIQ4.Y + cntIIQ4.Height + If(IsBlank(Self.Error), 0, errIIQ4.Height + 8) + 18, 0)` |
| `cntIIQ4` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrBestInnovatorIndividual.12.fx) — paste into the property identified immediately above.


##### Slot 5

| Control / property | Formula or value |
|---|---|
| `dcIIQ5Response.Visible` | `5 <= varQuestionCount` |
| `dcIIQ5Response.X` / Y | `0` / `4` |
| `dcIIQ5Response.Width` | `Parent.Width` |
| `dcIIQ5Response.Height` | `If(Self.Visible, cntIIQ5.Y + cntIIQ5.Height + If(IsBlank(Self.Error), 0, errIIQ5.Height + 8) + 18, 0)` |
| `cntIIQ5` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrBestInnovatorIndividual.13.fx) — paste into the property identified immediately above.


##### Slot 6

| Control / property | Formula or value |
|---|---|
| `dcIIQ6Response.Visible` | `6 <= varQuestionCount` |
| `dcIIQ6Response.X` / Y | `0` / `5` |
| `dcIIQ6Response.Width` | `Parent.Width` |
| `dcIIQ6Response.Height` | `If(Self.Visible, cntIIQ6.Y + cntIIQ6.Height + If(IsBlank(Self.Error), 0, errIIQ6.Height + 8) + 18, 0)` |
| `cntIIQ6` inside card | X/Y `0`; Width `Parent.Width`; Fill `varAppTheme.Surface`; BorderColor `varAppTheme.Border`; BorderThickness `1`; radius `8` |
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

[Copy full formula](fx/scrBestInnovatorIndividual.14.fx) — paste into the property identified immediately above.


#### BestInnovatorIndividual: form dimensions and missing-property completion

Set `frmBestInnovatorIndividual.Width` from its actual parent as described above. Set `frmBestInnovatorIndividual.Height` to:

[Copy full formula](fx/scrBestInnovatorIndividual.15.fx) — paste into the property identified immediately above.



Rename each generated response error label as listed. Keep it directly inside the response card, not inside the question container. Set AutoHeight=true, Height=10, X=22, Width=Parent.Width-44, Text=Parent.Error, Visible=!IsBlank(Parent.Error), Color=varAppTheme.Error, Size=9, Live=Live.Assertive. Hide only the redundant generated response field-heading labels.

| Error label | Parent card | Y |
|---|---|---|
| `errIIQ1` | `dcIIQ1Response` | `cntIIQ1.Y + cntIIQ1.Height + 4` |
| `errIIQ2` | `dcIIQ2Response` | `cntIIQ2.Y + cntIIQ2.Height + 4` |
| `errIIQ3` | `dcIIQ3Response` | `cntIIQ3.Y + cntIIQ3.Height + 4` |
| `errIIQ4` | `dcIIQ4Response` | `cntIIQ4.Y + cntIIQ4.Height + 4` |
| `errIIQ5` | `dcIIQ5Response` | `cntIIQ5.Y + cntIIQ5.Height + 4` |
| `errIIQ6` | `dcIIQ6Response` | `cntIIQ6.Y + cntIIQ6.Height + 4` |

Set these input properties in addition to the question tables:

| Input | BorderColor | Tooltip |
|---|---|---|
| `txtIIQ1` | `If(IsBlank(dcIIQ1Response.Error), dcIIQ1Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 1, Prompt)` |
| `txtIIQ2` | `If(IsBlank(dcIIQ2Response.Error), dcIIQ2Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 2, Prompt)` |
| `txtIIQ3` | `If(IsBlank(dcIIQ3Response.Error), dcIIQ3Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 3, Prompt)` |
| `txtIIQ4` | `If(IsBlank(dcIIQ4Response.Error), dcIIQ4Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 4, Prompt)` |
| `txtIIQ5` | `If(IsBlank(dcIIQ5Response.Error), dcIIQ5Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 5, Prompt)` |
| `txtIIQ6` | `If(IsBlank(dcIIQ6Response.Error), dcIIQ6Response.BorderColor, Color.Red)` | `LookUp(colAnswers, Slot = 6, Prompt)` |

For all six inputs use Font=`Font.'Segoe UI'`, Size=`9.75`, Color=`varAppTheme.Body`, Fill=`varAppTheme.Surface`, BorderThickness=`1`, FocusedBorderColor=`varAppTheme.Primary`, FocusedBorderThickness=`2`, PaddingLeft/Right=`11`, PaddingTop/Bottom=`9`, all corner radii=`4`, and TabIndex=`0`. Set heading Font=`Font.'Segoe UI'` and Color=`varAppTheme.Heading`; prompt/counter Font=`Font.'Segoe UI'` and Color=`varAppTheme.Muted`. Prompt AutoHeight=`true`, base Height=`34`, Size=`9.75`; counter AutoHeight=`false`, Height=`18`. All labels Wrap=`true`.


#### BestInnovatorIndividual: native attachments and form-level errors

Keep `attII` directly inside `dcIIAttachments`. Retain the generated DataField, Items, limits, and native binding settings. Do not replace an attachment control with a collection-backed file picker.

| Property | Value |
|---|---|
| `dcIIAttachments.Visible` | `true` |
| `dcIIAttachments.Width` | `Parent.Width` |
| `dcIIAttachments.Height` | `270` |
| `dcIIAttachments.Required` | `false` |
| `dcIIAttachments.Update` | `attII.Attachments` |
| `attII.Items` | `Parent.Default` |
| `attII.DisplayMode` | `If(varIsBusy, DisplayMode.Disabled, Parent.DisplayMode)` |

For `attII.OnAddFile`, `attII.OnRemoveFile`, and `attII.OnUndoRemoveFile`, use the same action:

[Copy full formula](fx/scrBestInnovatorIndividual.16.fx) — paste into the property identified immediately above.


The attachment layout can retain the generated label/editor coordinates. If restyling it, keep the generated error label visible and reserve space for its complete text. Do not suppress native validation messages.

Add a classic label `lblSaveErrorII` immediately after the form in the scrolling content container. Use the same X and Width as the form, Y=`frmBestInnovatorIndividual.Y + frmBestInnovatorIndividual.Height + 8`, AutoHeight=`true`, Text=`frmBestInnovatorIndividual.Error`, Visible=`!IsBlank(frmBestInnovatorIndividual.Error)`, Color=`varAppTheme.Error`, and Live=`Live.Assertive`. Place the action row after this label when visible so errors from hidden metadata cards are not lost. Do not reset inputs on failure.


#### BestInnovatorIndividual: action controls

| Control | Text | Visible | DisplayMode |
|---|---|---|---|
| `btnIISaveDraft` | `"Save draft"` | `!varReadOnly` | `If(varIsBusy \|\| varReadOnly \|\| !varCategoryComplete, DisplayMode.Disabled, DisplayMode.Edit)` |
| `btnIIReview` | `"Review"` | `!varReadOnly` | `If(varIsBusy \|\| varReadOnly, DisplayMode.Disabled, DisplayMode.Edit)` |
| `btnIIBack` | `"Back to details"` | `!varReadOnly` | `If(varIsBusy, DisplayMode.Disabled, DisplayMode.Edit)` |

Use the complete OnSelect blocks above for these controls. Do not append a status Patch directly after SubmitForm. A read-only Back to My nominations button can use `Navigate(scrMyNominations, ScreenTransition.None)` with Visible=`varReadOnly`.


<a id="form-ic"></a>


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
| cmpHeaderII.LogoImage | [Copy Image formula](fx/Header.LogoImage.fx) |

Before preview, initialize the global palette using [Theme setup](02-Theme.md). Components receive colours through input properties; do not reference app variables inside their definitions.
