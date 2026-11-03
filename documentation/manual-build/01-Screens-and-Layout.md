# Screens, reusable stepper and visual properties

Use this alongside the screen-specific formulas. All coordinates below are Canvas logical units. Classic text sizes are specified in points as an initial conversion from the source's CSS pixels: 30px → 22.5pt, 18px → 13.5pt, 17px → 12.75pt, 15px → 11.25pt, 13px → 9.75pt. Check actual rendering at browser zoom 100%. Native Semibold approximates CSS weight 600/650; native controls do not expose identical CSS line-height/shadows.

## A. Create one page shell, then duplicate it

Start on scrNomineeDetails. Insert manual-layout containers for header/navigation and an auto-layout vertical container for scrolling. Rename controls before entering their formulas. Power Apps requires app-wide unique control names: append `Details`, `Category`, `II`, `IC`, `IE`, `TC`, `TI`, `TT`, `Review`, `Mine`, `Admin`, etc. when copying. Form recipes already use unique form/input names. In the tables, `cntPage`/`cntScroll` refer to that screen's actual controls.

| Control/property | Value |
|---|---|
| Screen.Fill | `Theme.Page` |
| Header manual container | X `0`; Y `0`; Width `Parent.Width`; Height `If(App.Width <= 760,58,64)`; Fill `Theme.Surface` |
| Navigation manual container | X `0`; Y `header.Y+header.Height`; Width `Parent.Width`; Height `48`; Fill `Theme.Surface` |
| Stepper strip manual container | X `0`; Y `nav.Y+nav.Height`; Width `Parent.Width`; Height `94`; Fill `Theme.Surface` |
| Scrolling vertical container `cntScroll` | X `0`; Y `stepperStrip.Y+stepperStrip.Height`; Width `Parent.Width`; Height `Max(0,Parent.Height-Self.Y)` |
| cntScroll layout | LayoutDirection `LayoutDirection.Vertical`; LayoutOverflowY `LayoutOverflow.Scroll`; LayoutOverflowX `LayoutOverflow.Hide`; LayoutGap `0`; PaddingLeft/Right/Top/Bottom `0` |
| Manual content container `cntPage` inside cntScroll | Width `Min(1030,Parent.Width)`; AlignInContainer `AlignInContainer.Center`; FillPortions `0`; LayoutMinHeight `0`; Height set from last content control as below |
| Inner page content | X `If(App.Width<=760,16,24)`; Width `Parent.Width-2*Self.X` |
| Page heading | Y `If(App.Width<=760,27,39)`; Size `If(App.Width<=760,18.75,22.5)`; Font `Font.'Segoe UI'`; FontWeight `FontWeight.Semibold`; Color `Theme.Heading`; AutoHeight `true` |
| Subtitle | Y `heading.Y+heading.Height+8`; Size `11.25`; Color `Theme.Muted`; AutoHeight `true`; Width same as heading |
| Main section/container | Y `subtitle.Y+subtitle.Height+26`; Width same as heading; X same as heading |
| cntPage.Height | `lastControl.Y + lastControl.Height + If(App.Width<=760,40,56)` |

In auto-layout parents, turn off flexible height for content that must grow to its explicit Height (`FillPortions=0`). Keep the viewport's height fixed to the available screen, and let the content container be taller. This creates one vertical page scrollbar. Do not set every child to `Parent.Height`, which would prevent long forms from growing. If the property pane exposes overflow as a dropdown rather than a formula, select Scroll/Hide there.

Home, My nominations, Admin and Confirmation do not require a stepper; make the strip Height `0`, Visible `false`, so the scrolling container begins immediately after navigation. The six form screens use a page maximum of **1180** instead of 1030. Review uses **960**. Center all three variants using the same AlignInContainer setting.

## B. Header and navigation

Within header use these controls. Replace `hdr` with the actual parent container name when needed.

| Control | Properties |
|---|---|
| Logo background container | X `If(App.Width<=760,16,40)`; Y `(Parent.Height-28)/2`; Width/Height `28`; Fill `Theme.Primary`; all corner radii `6` |
| Award logo Image inside background | X/Y `4`; Width/Height `20`; ImagePosition `ImagePosition.Fit`; AccessibleLabel `Theme.Brand & " awards"`; Image formula below |
| Brand label | X `logo.X+logo.Width+10`; Y `(Parent.Height-28)/2`; Height `28`; Width `62`; Text `Theme.Brand`; Size `11.25`; Semibold; Color `Theme.Heading` |
| Divider rectangle | X `brand.X+brand.Width+12`; Y `20`; Width `1`; Height `24`; Fill `Theme.Border`; Visible `App.Width>760` |
| App title label | X `divider.X+14`; Y `18`; Height `28`; Width `Max(0,Parent.Width-Self.X-230)`; Text `Theme.AppTitle`; Size `9.75`; Visible `App.Width>760` |
| Avatar circle | X `Parent.Width-If(App.Width<=760,50,180)`; Y `(Parent.Height-32)/2`; Width/Height `32`; Fill `Theme.Pale`; radius `16` |
| Avatar initials label | Same bounds as circle; Align `Align.Center`; Text `Upper(Left(User().FullName,1) & Left(Last(Split(User().FullName," ")).Value,1))`; Color `Theme.Primary`; Size `9` |
| User label | X `avatar.X+40`; Y `13`; Width `125`; Height `22`; Text `User().FullName`; Size `9`; Visible `App.Width>760` |
| Signed-in label | X same as user; Y `34`; Height `16`; Text `"Signed in"`; Color `Theme.Muted`; Size `7.5`; Visible `App.Width>760` |
| Bottom rule | X `0`; Y `Parent.Height-1`; Width `Parent.Width`; Height `1`; Fill `Theme.SoftBorder` |

Award logo Image (paths from supplied HTML, retained as Contoso placeholder branding):

```powerfx
"data:image/svg+xml;utf8," & EncodeUrl(
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'><path d='M12 15a6 6 0 1 0 0-12 6 6 0 0 0 0 12Z'/><path d='m8.5 14.5-1 6 4.5-2.5 4.5 2.5-1-6'/></svg>"
)
```

Place a centered navigation content container of Width `Min(1180,Parent.Width)` and X `(Parent.Width-Self.Width)/2`. Add native transparent buttons New nomination and My nominations: X `16` / `170`, Width `150`, Height `47`, Y `0`, Size `9.75`, BorderThickness `0`, Color `Theme.Primary` for current section else `Theme.Body`, HoverFill `Theme.Pale`. Draw a 2px primary rectangle along the active button's bottom. Wire actions using the discard recipe in README. Administration button may be aligned right with Visible `varCanManageQuestions`; hide text at very narrow widths or put it on Home. Do not hardcode Jordan Lee or other prototype people.

Optional Help opens a local information dialog explaining the four stages and draft saving; no invented support URL or email is required. Its Close button clears `varShowHelp`. Initialize that variable to false in App.OnStart if adding this optional dialog.

## C. Stepper component — dynamic SVG colors

Follow [Process-Stepper-Component.md](../Process-Stepper-Component.md) to create `cmpStepper` and paste its complete SVG Image formula. This is the reusable visual component requested. HTML is a display-only alternative; dynamic SVG is rendered by a native Image control, not embedded JavaScript.

On each screen's component instance:

| Input/property | Formula |
|---|---|
| Width | `Min(1060,Parent.Width)` |
| X | `(Parent.Width-Self.Width)/2` |
| Height / Y | `94` / `0` |
| CurrentStep | `varCurrentStep` |
| CurrentHex / CompleteHex | `Theme.PrimaryHex` / `Theme.SuccessHex` |
| PendingHex / MutedHex / HaloHex | `Theme.BorderHex` / `Theme.MutedHex` / `Theme.PaleHex` |

Steps:

```powerfx
Table(
    {StepNo:1, Label:"Nominee details", IsComplete:varDetailsComplete},
    {StepNo:2, Label:"Award category", IsComplete:varCategoryComplete},
    {StepNo:3, Label:"Criteria & evidence", IsComplete:varResponsesComplete},
    {StepNo:4, Label:"Review & submit", IsComplete:varSubmissionComplete}
)
```

Current stage overrides completed appearance when revisiting. The checkmark means validated progress, not necessarily saved data. Only successful final status Patch completes submission. Keep stepper read-only and use native Back/Edit buttons. With the full app guide, the named `DetailsValid`/`ResponsesValid` checks determine completion; merely advancing screens must not mark missing details valid.

## D. Reusable native control styling

| Control | Properties |
|---|---|
| Section card container | Fill `Theme.Surface`; BorderColor `Theme.Border`; BorderThickness `1`; all corner radii `10`; DropShadow `DropShadow.None` initially |
| Field label | Size `9.75`; Semibold; Color `Theme.Body`; Height `22`; AutoHeight true for longer labels |
| Standard classic Text input | Height `40`; Size `9.75`; Font Segoe UI; Color `Theme.Body`; Fill white; BorderColor `ColorValue("#aeb8c5")`; BorderThickness `1`; FocusedBorderColor `Theme.Primary`; FocusedBorderThickness `2`; RadiusTopLeft/Right/BottomLeft/BottomRight `4`; PaddingLeft/Right `11`; PaddingTop/Bottom `9`; DelayOutput `false` |
| People Combo box | Height `56`; Size `9.75`; border/input colors as above; SelectMultiple `false`; IsSearchable `true`; DisplayFields `["DisplayName","Mail"]`; SearchFields `["DisplayName","Mail"]`; InputTextPlaceholder `"Search for a person"` |
| Primary Button | Height `38`; Size `9.75`; Semibold; Fill `Theme.Primary`; HoverFill `Theme.PrimaryHover`; Color white; BorderThickness `0`; radius `4`; FocusedBorderThickness `2` |
| Secondary Button | Same size/radius; Fill white; Color `Theme.Body`; BorderColor `Theme.Border`; BorderThickness `1`; HoverFill `Theme.Pale` |
| Link Button | Fill transparent; BorderThickness `0`; Color `Theme.Primary`; Size `9.75`; underline optional; keep native keyboard focus |
| Required/error helper | Color `Theme.Error`; Size `9`; AutoHeight true; explain the issue in text, not color alone |

Set AccessibleLabel to the field/question meaning, not the control name. Input DisplayMode = `If(varIsBusy || varReadOnly,DisplayMode.Disabled,DisplayMode.Edit)` on step 1. In form cards retain `DisplayMode.View` for read-only text instead of disabling all text: `If(varIsBusy,DisplayMode.Disabled,dcActual.DisplayMode)`. TabIndex `0` for interactive controls and `-1` for decoration; keep Tree view order aligned with reading order. Use a visible Label with Live `Live.Polite` for progress/save state when supported.

## E. Step-3 layout and the six form cards

Build the visual structure once on scrIndividualInnovation, then create the other five forms with their actual data sources and recipes. **Do not just change a form DataSource and assume its generated cards changed correctly.** Add fields from each actual source and map their Update properties.

Inside the 1180px `cntPage`, add heading, subtitle, a summary strip, `cntProgressII`, form `frmIndividualInnovation`, and action buttons. The main section is the available inner width after the standard page padding.

| Element | Formula/measurement |
|---|---|
| Heading.Text | `If(varReadOnly,"View nomination","Criteria & evidence")` |
| Subtitle.Text | `varCategory.Title` |
| Summary strip | X same as heading; Y after subtitle +18; Width same as heading; Height `If(App.Width<=760,112,72)`; white fill, border1, radius8 |
| Summary text | `Coalesce(NomineeDisplay,"Details incomplete") & "  •  " & varAwardType & " award" & Char(10) & NominationReference`; label AutoHeight; padding20 |
| Details edit button | In summary; Text `"Edit details"`; Visible `!varReadOnly`; OnSelect use the per-form Back-to-details block |
| Progress/sidebar | Width `If(App.Width<=760,innerWidth,260)`; X `If(App.Width<=760,innerX,innerX+innerWidth-260)`; Y `summary.Y+summary.Height+22`; Height `If(App.Width<=760,100,260)` |
| Form.X | `innerX` |
| Form.Y | `If(App.Width<=760,progress.Y+progress.Height+22,progress.Y)` |
| Form.Width | `If(App.Width<=760,innerWidth,innerWidth-282)` |
| Form.Height | Sum the six **response** card Heights plus attachment card Height + `24` |
| Save/Review action row | Y `form.Y+form.Height+20`; X `innerX`; Width `innerWidth`; Height `If(App.Width<=760,96,48)` |

`innerX`/`innerWidth` are explanatory names above, not undeclared Power Fx variables: use `lblHeadingII.X` / `lblHeadingII.Width` (or your actual heading control's properties) in these expressions. Form.Height for II is:

```powerfx
dcIIQ1Response.Height + dcIIQ2Response.Height + dcIIQ3Response.Height +
dcIIQ4Response.Height + dcIIQ5Response.Height + dcIIQ6Response.Height +
dcIIAttachments.Height + 24
```

Progress label Text:

```powerfx
Text(CountIf(colAnswers, Slot<=varQuestionCount && !IsBlank(Trim(Response)))) &
" of " & Text(varQuestionCount) & " responses entered"
```

Add helper label “Required responses must be completed before review. You can save an incomplete draft.” AutoHeight true. The progress total includes optional answers; it does not replace required validation. On submitted records show status/reference and hide editing guidance.

Create response cards with the exact control properties in each **Form-CODE.md → Question control properties** section. Each native input has its own dynamic prompt/required flag; only slots up to QuestionCount are shown. This provides dynamic questions without an editable response gallery. Form card X `0`; Y is the row index 0–5 (form grid ordering, not a pixel offset). Put Attachments at Y `6`. Hidden metadata at Y `7`, Height `0`. If Studio reorders fields, use Edit fields to put Q1Response…Q6Response then Attachments in that order and metadata last.

Attachment card: Height `270`; Width `Parent.Width`; native heading X `22`, Y `18`, Text `"Supporting evidence (optional)"`, Size `12.75`; helper Y `44`, Text `"Add evidence for this nomination."`, Size `9`; native attachment control X `22`, Y `72`, Width `Parent.Width-44`, Height `170`; generated Error label below it. Keep the attachment input directly in the data card so Parent.Default and Parent.DisplayMode refer to that card. AddFile/RemoveFile/UndoRemoveFile all use:

```powerfx
Set(varHasChanges, true);
Set(varDeclarationAccepted, false);
Set(varResponsesComplete, false)
```

Do not add an evidence-link field or per-question file store; the fixed schema supports nomination-level attachments. File upload/delete is supported through a bound form and committed when the form saves. [Microsoft attachment control](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/control-attachments).

Action row: Back X0 Width80; Save draft X `If(App.Width<=760,92,Parent.Width-278)` Width120; Review X `If(App.Width<=760,0,Parent.Width-146)` Y `If(App.Width<=760,50,0)` Width `If(App.Width<=760,Parent.Width,146)`. Buttons Height38. All entry actions Visible `!varReadOnly`; use per-form Save/Review formulas. A read-only Back to My nominations button is visible when `varReadOnly` and simply navigates to scrMyNominations. Do not use Back() for a submitted item because its history might include a previous review page.

## F. Busy and error display

Add a screen-level overlay last in Tree view: X/Y0, Width/Height Parent, Fill `RGBA(255,255,255,0.65)`, Visible `varIsBusy`; centered label “Saving or loading…”. Disable underlying controls while busy. Every formula's terminal error/success path must clear varIsBusy. Form OnFailure must leave inputs and files in place; do not call ResetForm there.

The optional shadow is a visual adjustment after the layout works. Native DropShadow.Light may approximate the HTML's `0 2px 8px rgba(15,23,42,.06)` but is not an exact CSS shadow. Avoid inventing new accent colors or hardcoded category text while matching the reference.
