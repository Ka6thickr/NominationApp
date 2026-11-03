# Dynamic four-step process indicator

Target environment: Ka6thickMSFT. This is a manual component recipe, not a deployed or Studio-tested component. Include it in the full property-by-property Power Fx guide before app authoring.

## Implementation decision

Yes: a Canvas component can render a process indicator whose colors, labels and checkmarks react to Power Fx state. An HTML Text control supports a styled HTML presentation; a native Image control with Power Fx-generated SVG is the preferred option when SVG fill and stroke are required. Do not assume a pasted web page, inline SVG inside HtmlText, JavaScript, or DOM event handlers will behave like the original HTML prototype. Validate the SVG Image rendering on the actual Power Apps clients.

The visual indicator is read-only. Continue/Back and any clickable step targets are native Canvas buttons with ordinary Power Fx navigation and validation. Do not place clickable links inside the SVG or rely on HTML to update app variables. This avoids confusing visual progress with workflow authorization.

Four steps, in the supplied image's order:

1. Nominee details
2. Award category
3. Criteria & evidence
4. Review & submit

| State | Appearance |
|---|---|
| Current | Primary-colored circle with white number and light outer ring; emphasized label |
| Completed | Green circle with white checkmark and green label |
| Upcoming | White circle, muted outline/number/label |
| Connector | Green after a completed step; pale gray otherwise |

Current appearance takes precedence if a user revisits a completed step. Completion is derived from successful validation; moving the current-stage variable alone must not mark future steps complete. The stepper reaching step 4 never means that SharePoint submission succeeded.

## Create the component

1. In Canvas Studio, create component `cmpStepper`; leave app-scope access off.
2. Add input data properties `CurrentStep` (Number), `Steps` (Table), and `CurrentHex`, `CompleteHex`, `PendingHex`, `MutedHex`, `HaloHex` (Text).
3. Use these defaults for the component preview. Colors below reuse the supplied CSS palette; match the screenshot's more violet accent during the first visual review by changing CurrentHex centrally.

| Property | Default |
|---|---|
| CurrentStep | `2` |
| CurrentHex | `"#0f6cbd"` |
| CompleteHex | `"#107c10"` |
| PendingHex | `"#d8dee7"` |
| MutedHex | `"#667085"` |
| HaloHex | `"#eff6fc"` |

`Steps` default (these are UI stage labels, not award question text):

```powerfx
Table(
    {StepNo: 1, Label: "Nominee details", IsComplete: true},
    {StepNo: 2, Label: "Award category", IsComplete: false},
    {StepNo: 3, Label: "Criteria & evidence", IsComplete: false},
    {StepNo: 4, Label: "Review & submit", IsComplete: false}
)
```

4. Set component Width to `1060`, Height to `94` for preview. On each screen, bind the instance Width to the available parent width, capped at 1060. Use centered placement within the page container.
5. Insert Image control `imgStepper`: X `0`, Y `0`, Width `Parent.Width`, Height `60`, ImagePosition `ImagePosition.Fit`, BorderThickness `0`, TabIndex `-1`.
6. Insert native Label `lblCurrentStage` beneath it: X `16`, Y `60`, Width `Parent.Width - 32`, Height `30`, Text as below. Keep it visible for a readable current-state summary on mobile. Set Live to `Live.Polite` if offered by the selected classic Label control.

```powerfx
"Step " & Text(cmpStepper.CurrentStep) & " of 4: " &
LookUp(cmpStepper.Steps, StepNo = cmpStepper.CurrentStep, Label)
```

Use the same expression for `imgStepper.AccessibleLabel`, adding that it is a progress indicator. Do not use the whole image as a single navigation target.

## imgStepper.Image

This formula generates SVG and encodes the full SVG before using it in a data URI. It XML-escapes labels, uses explicit colors, and formats coordinates using a fixed decimal locale. The component expects exactly four ordered, unique StepNo values 1–4 and a CurrentStep in that range. Theme strings must be trusted app-defined hexadecimal colors.

```powerfx
With(
    {w: Max(320, cmpStepper.Width)},
    With(
        {segment: (w - 32) / 4, compact: w <= 760},
        "data:image/svg+xml;utf8," & EncodeUrl(
            "<svg xmlns='http://www.w3.org/2000/svg' width='" &
            Text(w, "0.###", "en-US") & "' height='60' viewBox='0 0 " &
            Text(w, "0.###", "en-US") & " 60'>" &
            Concat(
                Sort(cmpStepper.Steps, StepNo, SortOrder.Ascending) As stage,
                With(
                    {
                        cx: 16 + (stage.StepNo - 1) * segment + If(compact, segment / 2, 14),
                        isCurrent: stage.StepNo = cmpStepper.CurrentStep,
                        isDone: stage.IsComplete,
                        safeLabel: Substitute(
                            Substitute(Substitute(stage.Label, "&", "&amp;"), "<", "&lt;"),
                            ">", "&gt;"
                        )
                    },
                    With(
                        {
                            paint: If(isCurrent, cmpStepper.CurrentHex,
                                isDone, cmpStepper.CompleteHex, cmpStepper.PendingHex),
                            labelPaint: If(isCurrent, cmpStepper.CurrentHex,
                                isDone, cmpStepper.CompleteHex, cmpStepper.MutedHex)
                        },
                        If(
                            stage.StepNo < 4,
                            "<line x1='" & Text(cx + If(compact, 16, 158), "0.###", "en-US") &
                            "' y1='30' x2='" & Text(cx + segment - 17, "0.###", "en-US") &
                            "' y2='30' stroke='" &
                            If(isDone, cmpStepper.CompleteHex, cmpStepper.PendingHex) &
                            "' stroke-width='1.5'/>",
                            ""
                        ) &
                        If(isCurrent,
                            "<circle cx='" & Text(cx, "0.###", "en-US") &
                            "' cy='30' r='17' fill='" & cmpStepper.HaloHex & "'/>", "") &
                        "<circle cx='" & Text(cx, "0.###", "en-US") &
                        "' cy='30' r='12' fill='" &
                        If(isCurrent || isDone, paint, "#ffffff") &
                        "' stroke='" & paint & "' stroke-width='1.5'/>" &
                        If(
                            isDone && !isCurrent,
                            "<path d='M " & Text(cx - 5, "0.###", "en-US") &
                            " 30 l 3 3 l 7 -7' fill='none' stroke='#ffffff' " &
                            "stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'/>",
                            "<text x='" & Text(cx, "0.###", "en-US") &
                            "' y='34' text-anchor='middle' font-family='Segoe UI,Arial,sans-serif' " &
                            "font-size='11' fill='" & If(isCurrent, "#ffffff", cmpStepper.MutedHex) &
                            "'>" & Text(stage.StepNo) & "</text>"
                        ) &
                        If(
                            !compact,
                            "<text x='" & Text(cx + 22, "0.###", "en-US") &
                            "' y='24' font-family='Segoe UI,Arial,sans-serif' font-size='8' fill='" &
                            cmpStepper.MutedHex & "'>STEP " & Text(stage.StepNo) & "</text>" &
                            "<text x='" & Text(cx + 22, "0.###", "en-US") &
                            "' y='39' font-family='Segoe UI,Arial,sans-serif' font-size='11' " &
                            "font-weight='600' fill='" & labelPaint & "'>" & safeLabel & "</text>",
                            ""
                        )
                    )
                )
            ) &
            "</svg>"
        )
    )
)
```

At widths of 760 or below, the numbered/checkmark circles remain visible while the native label gives the full current-stage name. For longer future labels, widen the component, use compact mode, or adjust the geometry after visual testing; SVG text does not automatically wrap.

## Bind app state to component instances

In the New nomination action (not every screen's OnVisible):

```powerfx
Set(varCurrentStep, 1);
Set(varDetailsComplete, false);
Set(varCategoryComplete, false);
Set(varResponsesComplete, false);
Set(varSubmissionComplete, false)
```

For each stepper instance, set CurrentStep to `varCurrentStep` and Steps to:

```powerfx
Table(
    {StepNo: 1, Label: "Nominee details", IsComplete: varDetailsComplete},
    {StepNo: 2, Label: "Award category", IsComplete: varCategoryComplete},
    {StepNo: 3, Label: "Criteria & evidence", IsComplete: varResponsesComplete},
    {StepNo: 4, Label: "Review & submit", IsComplete: varSubmissionComplete}
)
```

Set CurrentHex/CompleteHex/etc. from one centralized app theme record. The component itself should not reference global variables or data sources.

Place the following in the existing navigation success branches, after their respective validation. They are state updates, not full validation/save formulas:

| Event | State update |
|---|---|
| Validated step-1 details, Continue | `Set(varDetailsComplete, true); Set(varCurrentStep, 2)` |
| Validated category and loaded question version, Continue | `Set(varCategoryComplete, true); Set(varCurrentStep, 3)` |
| Validated required responses, Review | `Set(varResponsesComplete, true); Set(varCurrentStep, 4)` |
| Back to criteria | `Set(varCurrentStep, 3)` |
| Successful final Submitted status update | `Set(varSubmissionComplete, true)` before confirmation navigation |
| Failed draft/form/final-status save | Keep submission complete false; preserve input and show error |

When details become invalid, clear varDetailsComplete. When answers change, clear varResponsesComplete and the declaration; recompute after validation. When an unsaved category/type change is confirmed, clear affected completion flags and snapshots/responses as required. Saved nominations cannot change category. On resume, derive completion from the loaded item's actual values and saved question flags, not the last visited step number. Never store progress-indicator state as new SharePoint columns.

## HTML-only alternative

If HTML Text is preferred for appearance, use the same component inputs and generate four inline-styled cells with Power Fx Concat. A CSS circle with a number/checkmark and CSS connector can reproduce the same state logic without SVG. Use inline styles, a relatively positioned wrapper, and HTML-escaped labels. The HTML-only renderer remains display-only; retain the native current-stage label and navigation buttons. Do not combine two visible renderers in the same instance.

For a complete manual alternative, replace imgStepper with HTML Text control `htmStepper`, X/Y `0`, Width `Parent.Width`, Height `60`, AutoHeight `false`, PaddingLeft/Right/Top/Bottom `0`. Retain lblCurrentStage. Set HtmlText to the following formula. It uses CSS circles/checkmarks, not inline SVG. Select the SVG Image version above when actual SVG fill/stroke is required; both variants use the same input properties and state. HTML Text is not a JavaScript host.

```powerfx
With({compact:cmpStepper.Width<=760},
    "<div style='position:relative;width:100%;height:60px;font-family:Segoe UI,Arial,sans-serif;'>" &
    "<table role='presentation' style='width:100%;table-layout:fixed;border-collapse:collapse;'><tr>" &
    Concat(Sort(cmpStepper.Steps,StepNo,SortOrder.Ascending) As stage,
        With({current:stage.StepNo=cmpStepper.CurrentStep,done:stage.IsComplete,
              safeLabel:Substitute(Substitute(Substitute(stage.Label,"&","&amp;"),"<","&lt;"),">","&gt;")},
            With({paint:If(current,cmpStepper.CurrentHex,done,cmpStepper.CompleteHex,cmpStepper.PendingHex),
                  labelPaint:If(current,cmpStepper.CurrentHex,done,cmpStepper.CompleteHex,cmpStepper.MutedHex)},
                "<td style='width:25%;padding:10px 8px;vertical-align:top;'>" &
                "<div style='position:relative;height:40px;'>" &
                If(stage.StepNo<4,
                    "<div style='position:absolute;top:16px;left:" & If(compact,"40","170") &
                    "px;right:0;height:1px;background:" & If(done,cmpStepper.CompleteHex,cmpStepper.PendingHex) & ";'></div>","") &
                "<div style='position:absolute;left:0;top:3px;width:24px;height:24px;line-height:24px;text-align:center;border-radius:50%;border:1px solid " & paint &
                ";background:" & If(current||done,paint,"#ffffff") &
                ";color:" & If(current||done,"#ffffff",cmpStepper.MutedHex) &
                ";font-size:11px;" & If(current,"box-shadow:0 0 0 4px " & cmpStepper.HaloHex & ";","") & "'>" &
                If(done&&!current,"&#10003;",Text(stage.StepNo)) & "</div>" &
                If(!compact,
                    "<div style='position:absolute;left:36px;top:0;font-size:8px;color:" & cmpStepper.MutedHex & ";'>STEP " & Text(stage.StepNo) & "</div>" &
                    "<div style='position:absolute;left:36px;top:14px;font-size:11px;font-weight:600;color:" & labelPaint & ";'>" & safeLabel & "</div>","") &
                "</div></td>"
            )
        )
    ) & "</tr></table></div>"
)
```

Verify supported CSS in the target Canvas HTML Text control and player. Native buttons still own all actions. Long translated labels may require different geometry; the native current-stage label provides the full current label on narrow screens. The source CSS colors are used initially; component inputs let you change the palette centrally.

## Required acceptance checks

- CurrentStep 1, 2, 3 and 4 show the correct highlighted stage.
- Screenshot state (step 1 completed, step 2 current, 3 and 4 upcoming) renders correctly.
- Revisit a completed step: current ring takes precedence, and answers remain intact.
- Failure/retry does not show successful submission; a Save draft alone never completes step 4.
- A label containing `&` renders literally and does not break the SVG.
- Desktop, 760px, and approximately 390px widths avoid clipping or horizontal scrolling.
- Screen reader announces the current step; keyboard operation uses native buttons.
- Full Canvas Studio and target-client testing is pending. No rendered browser preview substitutes for this verification.

References: [HTML Text control](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/control-html-text), [Image control](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/control-image), [EncodeUrl and HTML encoding](https://learn.microsoft.com/en-us/power-platform/power-fx/reference/function-encode-decode), [Canvas components](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/create-component).
