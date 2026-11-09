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
