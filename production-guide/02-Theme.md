# Theme setup — #E20074

The new guides use **varAppTheme**, a global record initialized with Set in App.OnStart. This does not automatically restyle controls: each Fill/Color/BorderColor must use the values below. The failure of the previous Theme reference has not been diagnosed in your Studio session; this is an explicit replacement strategy, not a claim that named formulas are unsupported.

## Apply once

| Step | Action |
|---|---|
| 1 | Remove the old `Theme = {...};` definition from App.Formulas. Use the updated [App.Formulas.fx](fx/App.Formulas.fx), retaining LevelOptions and validation formulas. |
| 2 | Use the updated [App.OnStart.fx](fx/App.OnStart.fx); its first block initializes varAppTheme. If you already customized OnStart, merge only [Theme.Initialize.fx](fx/Theme.Initialize.fx) at its beginning. |
| 3 | Save unsaved nomination work before running full OnStart, because it resets working state. To refresh colours alone, temporarily paste Theme.Initialize.fx into a temporary button OnSelect and click it; that block changes only the palette. |
| 4 | Replace old control references such as Theme.Primary with varAppTheme.Primary. Check all screens and component instance input properties. |
| 5 | Component definitions use their own input properties; leave Access app scope off. Preview defaults may use literal colours. |

## Control styling and manual fallback

| Control/property | Preferred formula | Manual formula |
|---|---|---|
| Primary button Fill / active accent | varAppTheme.Primary | ColorValue("#E20074") |
| Primary button HoverFill | varAppTheme.PrimaryHover | ColorValue("#B5005D") |
| Primary button Color | Color.White | ColorValue("#FFFFFF") |
| Selected card / halo Fill | varAppTheme.Pale | ColorValue("#FDE6F1") |
| Screen Fill | varAppTheme.Page | ColorValue("#F4F6F8") |
| Card Fill | varAppTheme.Surface | ColorValue("#FFFFFF") |
| Heading Color | varAppTheme.Heading | ColorValue("#17253F") |
| Body Color | varAppTheme.Body | ColorValue("#27364F") |
| Muted label Color | varAppTheme.Muted | ColorValue("#667085") |
| BorderColor | varAppTheme.Border | ColorValue("#D8DEE7") |
| Error label Color | varAppTheme.Error | ColorValue("#C50F1F") |
| Completed step colour | varAppTheme.Success | ColorValue("#107C10") |
| SVG primary hex text | varAppTheme.PrimaryHex | "#E20074" |

Classic controls do not use BasePaletteColor: set their Fill, Color, HoverFill and border properties. If a modern control exposes BasePaletteColor, use ColorValue("#E20074") there, but keep the classic form/control types used by these recipes. A manual colour is a fallback and will not update when the global record changes.

## Verify

Check a primary button is magenta, a selected card is pale pink, completed steps remain green, error text remains red, and header/nav instances receive the palette. Run App Checker for unresolved Theme references. The global variable must be initialized before expecting colours in preview.

The global-variable approach follows the [requested theming article](https://www.matthewdevaney.com/power-apps-coding-standards-for-canvas-apps/power-apps-app-theming-guidelines/). Its later comments also discuss named formulas; global variables are chosen here for explicit manual initialization.
