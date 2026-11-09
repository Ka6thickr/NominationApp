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
