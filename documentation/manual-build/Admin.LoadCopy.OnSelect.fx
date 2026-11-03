If(varCanManageQuestions && !varIsBusy,
    Set(varIsBusy, true);
    Set(varAdminLoadOK, true);
    IfError(
        Refresh(AwardCategories); Refresh(AwardQuestions);
        Set(varAdminCategory, LookUp(AwardCategories, ID = cmbAdminCategory.Selected.ID));
        Set(varAdminBaseVersion, Coalesce(varAdminCategory.PublishedQuestionVersion, 0));
        Set(varAdminHighestVersion,
            Coalesce(First(SortByColumns(
                Filter(AwardQuestions, Category.Id = varAdminCategory.ID),
                "QuestionSetVersion", SortOrder.Descending
            )).QuestionSetVersion, 0)
        );
        Set(varAdminNewVersion, varAdminHighestVersion + 1);
        Set(varAdminSourceVersion, If(varAdminBaseVersion > 0, varAdminBaseVersion, varAdminHighestVersion));
        ClearCollect(colAdminSource, SortByColumns(Filter(AwardQuestions,
            Category.Id = varAdminCategory.ID, QuestionSetVersion = varAdminSourceVersion
        ), "DisplayOrder", SortOrder.Ascending));
        If(CountRows(colAdminSource) = 0,
            ClearCollect(colAdminQuestions, ForAll(Sequence(3) As n,
                {Slot: n.Value, Title: "", QuestionText: "", GuidanceText: "", IsRequired: true})),
            ClearCollect(colAdminQuestions, ForAll(colAdminSource As q,
                {Slot: q.DisplayOrder, Title: q.Title, QuestionText: q.QuestionText,
                 GuidanceText: Coalesce(q.GuidanceText, ""), IsRequired: q.IsRequired}))
        );
        Set(varAdminDirty, false);
        true,
        Set(varAdminLoadOK, false);
        Notify("Unable to load the configuration. Nothing has been published.", NotificationType.Error);
        false
    );
    Set(varIsBusy, false)
)
