If(varCanManageQuestions,
    IfError(
        Refresh(AwardCategories);
        ClearCollect(colAdminCategories,SortByColumns(AwardCategories,"DisplayOrder",SortOrder.Ascending));
        true,
        Notify("Could not load categories.",NotificationType.Error); false
    )
)
