# Dynamic four-step process indicator

Target environment: your current destination environment. This is a manual component recipe, not a deployed or Studio-tested component. Include it in the full property-by-property Power Fx guide before app authoring.

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
| CurrentHex | `"#E20074"` |
| CompleteHex | `"#107c10"` |
| PendingHex | `"#d8dee7"` |
| MutedHex | `"#667085"` |
| HaloHex | `"#FDE6F1"` |

`Steps` default (these are UI stage labels, not award question text):

[Copy full formula](fx/cmpStepper.01.fx) — paste into the property identified immediately above.


4. Set component Width to `1060`, Height to `94` for preview. On each screen, bind the instance Width to the available parent width, capped at 1060. Use centered placement within the page container.
5. Insert Image control `imgStepper`: X `0`, Y `0`, Width `Parent.Width`, Height `60`, ImagePosition `ImagePosition.Fit`, BorderThickness `0`, TabIndex `-1`.
6. Insert native Label `lblCurrentStage` beneath it: X `16`, Y `60`, Width `Parent.Width - 32`, Height `30`, Text as below. Keep it visible for a readable current-state summary on mobile. Set Live to `Live.Polite` if offered by the selected classic Label control.

[Copy full formula](fx/cmpStepper.02.fx) — paste into the property identified immediately above.


Use the same expression for `imgStepper.AccessibleLabel`, adding that it is a progress indicator. Do not use the whole image as a single navigation target.

## imgStepper.Image

This formula generates SVG and encodes the full SVG before using it in a data URI. It XML-escapes labels, uses explicit colors, and formats coordinates using a fixed decimal locale. The component expects exactly four ordered, unique StepNo values 1–4 and a CurrentStep in that range. Theme strings must be trusted app-defined hexadecimal colors.

[Copy full formula](fx/cmpStepper.03.fx) — paste into the property identified immediately above.


At widths of 760 or below, the numbered/checkmark circles remain visible while the native label gives the full current-stage name. For longer future labels, widen the component, use compact mode, or adjust the geometry after visual testing; SVG text does not automatically wrap.

## Bind app state to component instances

In the New nomination action (not every screen's OnVisible):

[Copy full formula](fx/cmpStepper.04.fx) — paste into the property identified immediately above.


For each stepper instance, set CurrentStep to `varCurrentStep` and Steps to:

[Copy full formula](fx/cmpStepper.05.fx) — paste into the property identified immediately above.


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

[Copy full formula](fx/cmpStepper.06.fx) — paste into the property identified immediately above.


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
