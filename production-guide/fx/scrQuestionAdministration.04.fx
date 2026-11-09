// txtAdminTitle.OnChange
Patch(colAdminQuestions,LookUp(colAdminQuestions,Slot=ThisItem.Slot),{Title:Self.Text});
Set(varAdminDirty,true)
