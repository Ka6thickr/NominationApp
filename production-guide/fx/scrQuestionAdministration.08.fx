IfError(
    Refresh(AwardCategories); Refresh(AwardQuestions);
    If(Coalesce(LookUp(AwardCategories,ID=varAdminCategory.ID,PublishedQuestionVersion),0)<>varAdminBaseVersion,
        Notify("A new version was published. Reload the category before continuing.",NotificationType.Warning),
        Set(varAdminNewVersion,Coalesce(First(SortByColumns(
            Filter(AwardQuestions,Category.Id=varAdminCategory.ID),
            "QuestionSetVersion",SortOrder.Descending)).QuestionSetVersion,0)+1);
        Set(varAdminDirty,true)
    ); true,
    Notify("Could not allocate the next version. Check your connection.",NotificationType.Error); false
)
