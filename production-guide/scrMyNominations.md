# scrMyNominations — build sheet

[Back to screen index](../Prod.md) · [Build components once](00-Reusable-Components.md)

Build controls in Tree view order. Insert children under the parent shown.

## 1. Complete Tree view

```text
scrMyNominations
  cmpHeaderMine [instance of cmpAppHeader]
  cmpNavMine [instance of cmpAppNav]
  cntScrollMine [Vertical container]
    cntPageMine [plain Container]
      lblHeadingMine [Label]
      lblSubtitleMine [Label]
      cntMineFilters [Container]
        btnBrowseIndividual [Button]
        btnBrowseTeam [Button]
        cmbBrowseCategory [Classic Combo box]
        ddBrowseStatus [Classic Dropdown]
        txtBrowseId [Classic Text input]
        btnBrowseRefresh [Button]
      lblBrowseError [Label]
      cntMineResults [Container]
        galMineII [Gallery]
          lblMineReferenceII [Label]
          lblMineNomineeII [Label]
          lblMineModifiedII [Label]
          lblMineStatusII [Label]
          btnMineOpenII [Button]
        galMineIC [Gallery]
          lblMineReferenceIC [Label]
          lblMineNomineeIC [Label]
          lblMineModifiedIC [Label]
          lblMineStatusIC [Label]
          btnMineOpenIC [Button]
        galMineIE [Gallery]
          lblMineReferenceIE [Label]
          lblMineNomineeIE [Label]
          lblMineModifiedIE [Label]
          lblMineStatusIE [Label]
          btnMineOpenIE [Button]
        galMineTC [Gallery]
          lblMineReferenceTC [Label]
          lblMineNomineeTC [Label]
          lblMineModifiedTC [Label]
          lblMineStatusTC [Label]
          btnMineOpenTC [Button]
        galMineTI [Gallery]
          lblMineReferenceTI [Label]
          lblMineNomineeTI [Label]
          lblMineModifiedTI [Label]
          lblMineStatusTI [Label]
          btnMineOpenTI [Button]
        galMineTT [Gallery]
          lblMineReferenceTT [Label]
          lblMineNomineeTT [Label]
          lblMineModifiedTT [Label]
          lblMineStatusTT [Label]
          btnMineOpenTT [Button]
      cntActionsMine [Container]
        btnMineNew [Button]
  btnStartNewMine [hidden Button]
  btnGoMineMine [hidden Button]
  cntExitOverlayMine [plain Container]
    cntExitDialogMine [plain Container]
      lblExitMessageMine [Label]
      btnExitCancelMine [Button]
      btnExitDiscardMine [Button]
  cntBusyMine [plain Container]
    lblBusyMine [Label]
```

Component children are created once in the component definitions; they do not need separate per-screen labels/buttons. Native cards keep their generated metadata controls.

## 2. Components and scrolling — property table

Use temporary cntPage height=800 only until the action row exists. Turn Flexible height off. Slash-separated properties map to the slash-separated values in order.

| Control / property | Value or formula |
|---|---|
| scrMyNominations.Fill | `varAppTheme.Page` |
| cmpHeaderMine.X / Y | `0 / 0` |
| cmpHeaderMine.Width / Height | `Parent.Width / If(App.Width<=760,58,64)` |
| cmpHeaderMine.BrandText / TitleText | `varAppTheme.Brand / varAppTheme.AppTitle` |
| cmpHeaderMine.UserText | `User().FullName` |
| cmpHeaderMine.HeadingColor / SmallLayout | `varAppTheme.Heading / App.Width<=760` |
| cmpNavMine.X / Y | `0 / cmpHeaderMine.Y+cmpHeaderMine.Height` |
| cmpNavMine.Width / Height | `Parent.Width / 48` |
| cmpNavMine.Busy / AccentColor | `varIsBusy / varAppTheme.Primary` |
| cmpNavMine.ActiveTab | `"Mine"` |
| cntScrollMine.X | `0` |
| cntScrollMine.Y | `cmpNavMine.Y+cmpNavMine.Height` |
| cntScrollMine.Width / Height | `Parent.Width / Max(0,Parent.Height-Self.Y)` |
| cntScrollMine.LayoutDirection | `LayoutDirection.Vertical` |
| cntScrollMine.LayoutOverflowY / LayoutOverflowX | `LayoutOverflow.Scroll / LayoutOverflow.Hide` |
| cntScrollMine.LayoutGap / all paddings | `0` |
| cntPageMine.Width | `Min(1030,Parent.Width)` |
| cntPageMine.AlignInContainer | `AlignInContainer.Center` |
| cntPageMine.FillPortions / LayoutMinWidth / LayoutMinHeight | `0 / 0 / 0` |
| cntPageMine.Height | `cntActionsMine.Y+cntActionsMine.Height+If(App.Width<=760,40,56)` |
| lblHeadingMine.X / Y | `If(App.Width<=760,16,24) / If(App.Width<=760,27,39)` |
| lblHeadingMine.Width / AutoHeight | `Parent.Width-2*Self.X / true` |
| lblHeadingMine.Font / Size | `Font.'Segoe UI' / If(App.Width<=760,18.75,22.5)` |
| lblHeadingMine.Color / FontWeight | `varAppTheme.Heading / FontWeight.Semibold` |
| lblSubtitleMine.X / Y | `lblHeadingMine.X / lblHeadingMine.Y+lblHeadingMine.Height+8` |
| lblSubtitleMine.Width / AutoHeight | `lblHeadingMine.Width / true` |
| lblSubtitleMine.Font / Size / Color | `Font.'Segoe UI' / 11.25 / varAppTheme.Muted` |

## 3. Navigation events and hidden helpers

| Control / property | Value or formula |
|---|---|
| cmpNavMine.OnNew | [Copy full formula](fx/cmpNavMine.OnNew.fx) |
| cmpNavMine.OnMine | [Copy full formula](fx/cmpNavMine.OnMine.fx) |
| btnStartNewMine.OnSelect | [Copy full New nomination formula](fx/NewNomination.OnSelect.fx) |
| btnGoMineMine.OnSelect | `Navigate(scrMyNominations,ScreenTransition.None)` |
| btnStartNewMine and btnGoMineMine: Visible / DisplayMode | `false / DisplayMode.Edit` |

Paste event formulas on the **component instance**, not its definition. Hidden helpers remain on this same screen.

## 4. Dialog and busy controls — property table

| Control / property | Value or formula |
|---|---|
| cntExitOverlayMine.X / Y / Width / Height | `0 / 0 / Parent.Width / Parent.Height` |
| cntExitOverlayMine.Visible / Fill | `varShowExitDialog / RGBA(0,0,0,0.35)` |
| cntExitDialogMine.Width / Height | `Min(440,Parent.Width-32) / 220` |
| cntExitDialogMine.X / Y | `(Parent.Width-Self.Width)/2 / Max(16,(Parent.Height-Self.Height)/2)` |
| cntExitDialogMine.Fill | `varAppTheme.Surface` |
| lblExitMessageMine.X / Y / Width / Height | `20 / 20 / Parent.Width-40 / 112` |
| lblExitMessageMine.Text | `"Leave this page? Unsaved changes and selected files will be discarded."` |
| btnExitCancelMine.X / Y / Width / Height | `20 / 160 / 110 / 38` |
| btnExitCancelMine.Text / OnSelect | `"Cancel" / Set(varShowExitDialog,false)` |
| btnExitDiscardMine.X / Y / Width / Height | `Parent.Width-140 / 160 / 120 / 38` |
| btnExitDiscardMine.Text | `"Discard"` |
| cntBusyMine.X / Y / Width / Height | `0 / 0 / Parent.Width / Parent.Height` |
| cntBusyMine.Visible / Fill | `varIsBusy / RGBA(255,255,255,0.65)` |
| lblBusyMine.Text / Align | `"Saving or loading…" / Align.Center` |
| lblBusyMine.X / Y / Width / Height | `0 / (Parent.Height-40)/2 / Parent.Width / 40` |
| Control / property | Value or formula |
|---|---|
| btnExitDiscardMine.OnSelect | [Copy full formula](fx/btnExitDiscardMine.OnSelect.fx) |

## 5. Screen content, buttons and formulas



lblHeadingMine.Text=`"My nominations"`; lblSubtitleMine.Text=`"View submitted nominations or continue a draft."`. cntActionsMine.Y=`cntMineResults.Y+cntMineResults.Height+24`.


Inside cntActionsMine, place these classic buttons. For this screen set cntActionsMine.Height=`If(App.Width<=760,50,48)`. Each button Width=`If(App.Width<=760,Parent.Width,Min(240,(Parent.Width-0)/1))`, Height=38; X=`If(App.Width<=760,0,index*(Self.Width+12))`, Y=`If(App.Width<=760,index*50,0)`. Replace index with the literal number in the table; do not create an index variable.

| Index | Exact name | Text | OnSelect / exact block to copy |
|---|---|---|---|

| 0 | btnMineNew | New nomination | `Select(btnStartNewMine)` |

Create cntMineFilters inside cntPageMine: X/Width match heading,Y=lblSubtitleMine.Y+lblSubtitleMine.Height+26,Height=If(App.Width<=760,240,100). Place the filter controls named in **3. scrMyNominations** inside, stacked on mobile. Create cntMineResults below filters+20, X/Width match heading,Height=600. Place galMineII,galMineIC,galMineIE,galMineTC,galMineTI,galMineTT inside it with X/Y=0,Width/Height=Parent.Width/Parent.Height. Only the selected category gallery is Visible. This is a deliberately bounded scrolling results gallery so delegated records can load; it is not an unbounded collection. Apply the six typed Items/OnSelect recipes from their form sections. Apply the complete My nominations OnVisible refresh block. Keep content height fixed to allow gallery virtualization; page scroll still reaches the action row.

**Filter placement:** preserve the existing filter-control names and OnChange formulas in the browse recipe. Place the Individual/Team selector first, cmbBrowseCategory second, status selector third and txtBrowseId fourth. Give each control a 20-unit label and 40-unit editor. On desktop allocate four equal columns with 12-unit gaps and X=`16+index*((Parent.Width-68)/4+12)`,Width=`(Parent.Width-68)/4`, label Y=8/editor Y=32. On mobile stack four rows with label Y=`12+index*76`, editor Y=label.Y+22, X=16,Width=Parent.Width-32; override cntMineFilters.Height=`If(App.Width<=760,332,100)`. Here index is the literal 0,1,2,3 for the controls in that order. Keep all result galleries at the same origin so only the selected one occupies the viewport.


### Detailed content/control recipe

#### 3. scrMyNominations

Heading “My nominations”, subtitle “View your submitted nominations or continue a draft.” No stepper. The original all-category prototype list is implemented as a category-selected view to preserve delegation across six physical lists. Do not merge all nominations using ClearCollect/ForAll and assume it is complete.

##### A. Screen refresh and filters

OnVisible:

[Copy full formula](fx/scrMyNominations.01.fx) — paste into the property identified immediately above.


Add Individual and Team type buttons. Individual.OnSelect:

[Copy full formula](fx/scrMyNominations.02.fx) — paste into the property identified immediately above.


Team uses `"Team"` in both places. Add classic Combo `cmbBrowseCategory`, Items `Filter(colBrowseCategories,AwardType.Value=varBrowseType)`, DisplayFields `["Title"]`, SelectMultiple false, IsSearchable false, DefaultSelectedItems `Filter(colBrowseCategories,CategoryCode=varBrowseCode)`. OnChange `Set(varBrowseCode,Self.Selected.CategoryCode); Set(varBrowseId,0); Reset(txtBrowseId)`. Include inactive categories so old nominations remain discoverable.

Status Dropdown `ddBrowseStatus`, Items `["All","Draft","Submitted"]`, Default `"All"`, OnChange `Set(varBrowseStatus,Self.Selected.Value)`.

Optional exact item-ID input `txtBrowseId`: label “Find item ID in this category”, Default `""`, Format `TextFormat.Number`, HintText “For example, 42”. OnChange:

[Copy full formula](fx/scrMyNominations.03.fx) — paste into the property identified immediately above.


The derived reference includes the category code plus this numeric ID. This is an exact lookup, not a promised full-text search over six lists. Add explicit Refresh button with the same selected-source Switch inside IfError as OnVisible; it does not reset the current filters.

##### B. Six galleries, one visible

Create `galMineII`, `galMineIC`, `galMineIE`, `galMineTC`, `galMineTI`, `galMineTT` at identical X/Y/Width/Height below the filters. Set their Items/Visible/Open buttons from the corresponding Form-CODE.md file. They query their actual typed source directly. Do not collect their results into a common unbounded table. Use a vertical gallery, TemplatePadding0, TemplateSize `If(App.Width<=760,150,76)`, Height `Max(280,App.Height-cntScrollMine.Y-Self.Y-56)`, ShowScrollbar true. The enclosing page height should end just below the gallery.

Desktop columns: Reference x16 width190; Nominee/team x216 width `Max(120,Parent.TemplateWidth-570)`; Modified x `Parent.TemplateWidth-330` width150; status x `Parent.TemplateWidth-170` width90; Open x `Parent.TemplateWidth-78` width62. On mobile stack reference y12, nominee y38, date/status y66, Open y102. Use native labels with Size9.75, truncate only the list summary if needed; full values display on opening. Status pill Fill pale green for Submitted, pale blue for Draft; show the status word as well as color. Draw a 1px bottom rule.

Each form recipe supplies the complete gallery Open.OnSelect: it refreshes and re-reads the clicked ID owned by the current user, loads saved snapshots and people, and opens Draft in EditForm or Submitted in ViewForm. It does not reinitialize questions from today's published configuration.

Empty label per gallery Visible `thatGallery.Visible && !varBrowseError && IsEmpty(thatGallery.AllItems)`, Text “No nominations match this selection.” Hide or replace this label while that gallery is loading. Error banner Visible varBrowseError. A missing result after a connection error must not be presented as a confirmed empty list.

Filtering by indexed NominatorEmail, Choice.Value and equality ID is designed to delegate; verify blue delegation warnings and test with more records than the configured data row limit. SharePoint permits only certain operators for complex fields and ID. [Microsoft SharePoint delegation table](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/connections/connection-sharepoint-online). If Studio flags the constant OR filters, rewrite as explicit If branches for All/exact status and zero/exact ID, each branch returning a direct Filter/SortByColumns on the same source; do not increase the row limit as a substitute.


### Event file assignments — paste into these exact properties

| Control / property | Value or formula |
|---|---|
| btnMineNew.OnSelect | [Copy full formula](fx/cmpNavMine.OnNew.fx) |

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
| cmpHeaderMine.LogoImage | [Copy Image formula](fx/Header.LogoImage.fx) |

Before preview, initialize the global palette using [Theme setup](02-Theme.md). Components receive colours through input properties; do not reference app variables inside their definitions.
