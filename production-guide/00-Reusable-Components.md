# Build reusable components once

## What changes in your half-built screen

| Keep | Replace after verification | New reusable definition |
|---|---|---|
| frmBestInnovatorIndividual and all corrected cards/events | cntHeaderII and its copied labels/logo | cmpAppHeader |
| cntScrollII and cntPageII | cntNavII and its copied navigation buttons | cmpAppNav |
| Summary, progress, action row and form controls | cntStepperStripII, if only used to host the stepper | cmpStepper directly on the screen |

1. Save a development checkpoint. Create the three components below in the **Components** tab of Tree view.
2. Insert instances on scrBestInnovatorIndividual. Initially hide the old header/nav/strip (Visible=false) rather than deleting them.
3. Update cntScrollII.Y to the formula in its new screen guide. Verify navigation, discard handling and stepper states.
4. Once verified, remove the redundant hidden visual containers if desired. Keep the original form and its controls. Do not copy component children into every screen.

## Property types and terminology

| Term | What to select |
|---|---|
| Manual-layout container | Insert → Layout → plain Container; you set child X/Y |
| Scroll viewport | Insert → Vertical container; set vertical overflow to Scroll |
| Component definition | Create once in Tree view → Components |
| Component instance | Insert a custom component on a screen; set its input/event properties |
| Data input | Custom property: Data, Input, specified data type |
| Event input | Custom property: Event, no parameters; the hosting screen supplies behavior |

For existing apps check Settings → Updates → Enhanced component properties if Event is not offered. Keep **Access app scope off** in all three components. Event properties are required for this recipe; do not substitute a Text/Boolean input for an Event. The host handles state, navigation, forms and SharePoint. See [Microsoft's component property instructions](https://learn.microsoft.com/en-gb/power-apps/maker/canvas-apps/component-properties).

## 1. cmpAppHeader

Create a component named cmpAppHeader. Default Width=1366, Height=64, Fill=Color.White.

```text
cmpAppHeader
  imgHeaderLogo (Image)
  lblHeaderBrand (classic Label)
  lblHeaderTitle (classic Label)
  lblHeaderUser (classic Label)
```

Create these custom properties before setting child formulas:

| Name | Kind / data type | Preview default |
|---|---|---|
| BrandText | Data Input / Text | "Contoso" |
| TitleText | Data Input / Text | "Employee & Team Recognition Awards" |
| UserText | Data Input / Text | "" |
| LogoImage | Data Input / Image | Blank() |
| HeadingColor | Data Input / Color | ColorValue("#17253f") |
| SmallLayout | Data Input / Boolean | false |

| Control | Property | Formula |
|---|---|---|
| imgHeaderLogo | X / Y / Width / Height | 16 / (cmpAppHeader.Height-28)/2 / 28 / 28 |
| imgHeaderLogo | Image / ImagePosition | cmpAppHeader.LogoImage / ImagePosition.Fit |
| imgHeaderLogo | AccessibleLabel | cmpAppHeader.BrandText & " awards" |
| lblHeaderBrand | X / Y / Width / Height | 54 / (cmpAppHeader.Height-28)/2 / 76 / 28 |
| lblHeaderBrand | Text | cmpAppHeader.BrandText |
| lblHeaderTitle | X / Y / Width / Height | 144 / (cmpAppHeader.Height-28)/2 / Max(0,cmpAppHeader.Width-374) / 28 |
| lblHeaderTitle | Text / Visible | cmpAppHeader.TitleText / !cmpAppHeader.SmallLayout |
| lblHeaderUser | X / Y / Width / Height | Max(140,cmpAppHeader.Width-210) / (cmpAppHeader.Height-28)/2 / 190 / 28 |
| lblHeaderUser | Text / Visible | cmpAppHeader.UserText / !cmpAppHeader.SmallLayout |
| All three labels | Font / Color | Font.'Segoe UI' / cmpAppHeader.HeadingColor |
| lblHeaderBrand | Size / FontWeight | 11.25 / FontWeight.Semibold |
| lblHeaderTitle, lblHeaderUser | Size | 9.75 |

## 2. cmpAppNav

Create cmpAppNav, default Width=1366, Height=48, Fill=Color.White.

```text
cmpAppNav
  btnComponentNew (classic Button)
  btnComponentMine (classic Button)
  rectNavSelected (Rectangle)
```

| Custom property | Kind / type | Preview default |
|---|---|---|
| Busy | Data Input / Boolean | false |
| ActiveTab | Data Input / Text | "New" |
| AccentColor | Data Input / Color | ColorValue("#E20074") |
| OnNew | Event, no parameters | Leave behavior empty until instance binding |
| OnMine | Event, no parameters | Leave behavior empty until instance binding |

| Control | Property | Formula |
|---|---|---|
| btnComponentNew | X / Y / Width / Height | 16 / 5 / Min(150,(cmpAppNav.Width-40)/2) / 38 |
| btnComponentMine | X / Y / Width / Height | btnComponentNew.X+btnComponentNew.Width+8 / 5 / btnComponentNew.Width / 38 |
| btnComponentNew | Text / OnSelect | "New nomination" / cmpAppNav.OnNew() |
| btnComponentMine | Text / OnSelect | "My nominations" / cmpAppNav.OnMine() |
| Both buttons | DisplayMode | If(cmpAppNav.Busy,DisplayMode.Disabled,DisplayMode.Edit) |
| Both buttons | Fill / Color / Font / Size | Color.Transparent / cmpAppNav.AccentColor / Font.'Segoe UI' / 9.75 |
| Both buttons | BorderThickness / FocusedBorderThickness | 0 / 2 |
| rectNavSelected | X | If(cmpAppNav.ActiveTab="Mine",btnComponentMine.X,btnComponentNew.X) |
| rectNavSelected | Y / Width / Height / Fill | 46 / btnComponentNew.Width / 2 / cmpAppNav.AccentColor |
| rectNavSelected | Visible | cmpAppNav.ActiveTab="New" Or cmpAppNav.ActiveTab="Mine" |

The component calls its Event properties. Paste the screen-specific event FX files into **the instance's OnNew/OnMine properties**, not into the component's buttons. No hidden helper from another screen is called.

## 3. cmpStepper

Use [the complete stepper component guide](01-Stepper.md). It contains the input-property schema, Image control and SVG formula. Keep the display-only component and existing completion-state logic. Insert its instance directly below cmpAppNav on screens that need the stepper. No cntStepperStrip container is needed in this revised design.

## Verification before duplicating instances

| Check | Expected |
|---|---|
| Change BrandText on one instance | Its header changes without changing the definition |
| Edit a label style in the definition | All instances receive the visual update |
| OnNew while unsaved | Host opens its discard dialog |
| Cancel discard | Existing form data and queued files stay intact |
| Busy=true | Navigation buttons disabled |
| Steps change | Only progress appearance changes; no save/navigation occurs |

Component recipes have not been compiled in your Studio session. Resolve property/schema errors before reusing instances.
