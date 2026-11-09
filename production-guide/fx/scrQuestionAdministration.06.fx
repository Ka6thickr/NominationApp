If(CountRows(colAdminQuestions)>3,
    With({lastSlot:Max(colAdminQuestions,Slot)},RemoveIf(colAdminQuestions,Slot=lastSlot));
    Set(varAdminDirty,true)
)
