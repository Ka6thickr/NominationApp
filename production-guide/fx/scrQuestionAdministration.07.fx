If(!varCanManageQuestions || !varAdminLoadOK || varIsBusy || IsBlank(varAdminCategory.ID) ||
   varAdminNewVersion<=varAdminBaseVersion,
   DisplayMode.Disabled,DisplayMode.Edit)
