# scrHome — build sheet

[Back to screen index](../Prod.md) · [Build components once](00-Reusable-Components.md)

Build controls in Tree view order. Insert children under the parent shown.

## 1. Complete Tree view

```text
scrHome
  cmpHeaderHome [instance of cmpAppHeader]
  cmpNavHome [instance of cmpAppNav]
  cntScrollHome [Vertical container]
    cntPageHome [plain Container]
      lblHeadingHome [Label]
      lblSubtitleHome [Label]
      cntActionsHome [Container]
        btnHomeNew [Button]
        btnHomeMine [Button]
        btnHomeAdmin [Button]
  btnStartNewHome [hidden Button]
  btnGoMineHome [hidden Button]
  cntExitOverlayHome [plain Container]
    cntExitDialogHome [plain Container]
      lblExitMessageHome [Label]
      btnExitCancelHome [Button]
      btnExitDiscardHome [Button]
  cntBusyHome [plain Container]
    lblBusyHome [Label]
```

Component children are created once in the component definitions; they do not need separate per-screen labels/buttons. Native cards keep their generated metadata controls.

## 2. Components and scrolling — property table

Use temporary cntPage height=800 only until the action row exists. Turn Flexible height off. Slash-separated properties map to the slash-separated values in order.

| Control / property | Value or formula |
|---|---|
| scrHome.Fill | `varAppTheme.Page` |
| cmpHeaderHome.X / Y | `0 / 0` |
| cmpHeaderHome.Width / Height | `Parent.Width / If(App.Width<=760,58,64)` |
| cmpHeaderHome.BrandText / TitleText | `varAppTheme.Brand / varAppTheme.AppTitle` |
| cmpHeaderHome.UserText | `User().FullName` |
| cmpHeaderHome.HeadingColor / SmallLayout | `varAppTheme.Heading / App.Width<=760` |
| cmpNavHome.X / Y | `0 / cmpHeaderHome.Y+cmpHeaderHome.Height` |
| cmpNavHome.Width / Height | `Parent.Width / 48` |
| cmpNavHome.Busy / AccentColor | `varIsBusy / varAppTheme.Primary` |
| cmpNavHome.ActiveTab | `""` |
| cntScrollHome.X | `0` |
| cntScrollHome.Y | `cmpNavHome.Y+cmpNavHome.Height` |
| cntScrollHome.Width / Height | `Parent.Width / Max(0,Parent.Height-Self.Y)` |
| cntScrollHome.LayoutDirection | `LayoutDirection.Vertical` |
| cntScrollHome.LayoutOverflowY / LayoutOverflowX | `LayoutOverflow.Scroll / LayoutOverflow.Hide` |
| cntScrollHome.LayoutGap / all paddings | `0` |
| cntPageHome.Width | `Min(1030,Parent.Width)` |
| cntPageHome.AlignInContainer | `AlignInContainer.Center` |
| cntPageHome.FillPortions / LayoutMinWidth / LayoutMinHeight | `0 / 0 / 0` |
| cntPageHome.Height | `cntActionsHome.Y+cntActionsHome.Height+If(App.Width<=760,40,56)` |
| lblHeadingHome.X / Y | `If(App.Width<=760,16,24) / If(App.Width<=760,27,39)` |
| lblHeadingHome.Width / AutoHeight | `Parent.Width-2*Self.X / true` |
| lblHeadingHome.Font / Size | `Font.'Segoe UI' / If(App.Width<=760,18.75,22.5)` |
| lblHeadingHome.Color / FontWeight | `varAppTheme.Heading / FontWeight.Semibold` |
| lblSubtitleHome.X / Y | `lblHeadingHome.X / lblHeadingHome.Y+lblHeadingHome.Height+8` |
| lblSubtitleHome.Width / AutoHeight | `lblHeadingHome.Width / true` |
| lblSubtitleHome.Font / Size / Color | `Font.'Segoe UI' / 11.25 / varAppTheme.Muted` |

## 3. Navigation events and hidden helpers

| Control / property | Value or formula |
|---|---|
| cmpNavHome.OnNew | [Copy full formula](fx/cmpNavHome.OnNew.fx) |
| cmpNavHome.OnMine | [Copy full formula](fx/cmpNavHome.OnMine.fx) |
| btnStartNewHome.OnSelect | [Copy full New nomination formula](fx/NewNomination.OnSelect.fx) |
| btnGoMineHome.OnSelect | `Navigate(scrMyNominations,ScreenTransition.None)` |
| btnStartNewHome and btnGoMineHome: Visible / DisplayMode | `false / DisplayMode.Edit` |

Paste event formulas on the **component instance**, not its definition. Hidden helpers remain on this same screen.

## 4. Dialog and busy controls — property table

| Control / property | Value or formula |
|---|---|
| cntExitOverlayHome.X / Y / Width / Height | `0 / 0 / Parent.Width / Parent.Height` |
| cntExitOverlayHome.Visible / Fill | `varShowExitDialog / RGBA(0,0,0,0.35)` |
| cntExitDialogHome.Width / Height | `Min(440,Parent.Width-32) / 220` |
| cntExitDialogHome.X / Y | `(Parent.Width-Self.Width)/2 / Max(16,(Parent.Height-Self.Height)/2)` |
| cntExitDialogHome.Fill | `varAppTheme.Surface` |
| lblExitMessageHome.X / Y / Width / Height | `20 / 20 / Parent.Width-40 / 112` |
| lblExitMessageHome.Text | `"Leave this page? Unsaved changes and selected files will be discarded."` |
| btnExitCancelHome.X / Y / Width / Height | `20 / 160 / 110 / 38` |
| btnExitCancelHome.Text / OnSelect | `"Cancel" / Set(varShowExitDialog,false)` |
| btnExitDiscardHome.X / Y / Width / Height | `Parent.Width-140 / 160 / 120 / 38` |
| btnExitDiscardHome.Text | `"Discard"` |
| cntBusyHome.X / Y / Width / Height | `0 / 0 / Parent.Width / Parent.Height` |
| cntBusyHome.Visible / Fill | `varIsBusy / RGBA(255,255,255,0.65)` |
| lblBusyHome.Text / Align | `"Saving or loading…" / Align.Center` |
| lblBusyHome.X / Y / Width / Height | `0 / (Parent.Height-40)/2 / Parent.Width / 40` |
| Control / property | Value or formula |
|---|---|
| btnExitDiscardHome.OnSelect | [Copy full formula](fx/btnExitDiscardHome.OnSelect.fx) |

## 5. Screen content, buttons and formulas



lblHeadingHome.Text=`"Employee & Team Recognition Awards"`; lblSubtitleHome.Text=`"Recognize a colleague or team."`. cntActionsHome.Y=`lblSubtitleHome.Y+lblSubtitleHome.Height+26`.


Inside cntActionsHome, place these classic buttons. For this screen set cntActionsHome.Height=`If(App.Width<=760,150,48)`. Each button Width=`If(App.Width<=760,Parent.Width,Min(240,(Parent.Width-24)/3))`, Height=38; X=`If(App.Width<=760,0,index*(Self.Width+12))`, Y=`If(App.Width<=760,index*50,0)`. Replace index with the literal number in the table; do not create an index variable.

| Index | Exact name | Text | OnSelect / exact block to copy |
|---|---|---|---|

| 0 | btnHomeNew | New nomination | `Select(btnStartNewHome)` |
| 1 | btnHomeMine | My nominations | `Select(btnGoMineHome)` |
| 2 | btnHomeAdmin | Manage questions | `Navigate(scrQuestionAdministration,ScreenTransition.None)` |

btnHomeAdmin.Visible=varCanManageQuestions. Keep Home OnVisible free of form resets. The New action resets all six form contexts only after discard handling. No stepper instance is required.

Set btnHomeAdmin.Visible=varCanManageQuestions. Home has no form reset in OnVisible. Apply the full New nomination formula only after unsaved-change checks.

### Event file assignments — paste into these exact properties

| Control / property | Value or formula |
|---|---|
| btnHomeNew.OnSelect | [Copy full formula](fx/cmpNavHome.OnNew.fx) |
| btnHomeMine.OnSelect | [Copy full formula](fx/cmpNavHome.OnMine.fx) |

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
| cmpHeaderHome.LogoImage | [Copy Image formula](fx/Header.LogoImage.fx) |

Before preview, initialize the global palette using [Theme setup](02-Theme.md). Components receive colours through input properties; do not reference app variables inside their definitions.
