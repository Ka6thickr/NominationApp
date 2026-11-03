If(varCanManageQuestions && varAdminLoadOK && !varIsBusy,
    ClearCollect(colAdminEdits, ForAll(galAdminQuestions.AllItems As row,
        {Slot: row.Slot, Title: row.txtAdminTitle.Text,
         QuestionText: row.txtAdminQuestion.Text, GuidanceText: row.txtAdminGuidance.Text,
         IsRequired: row.chkAdminRequired.Value}));
    ForAll(colAdminEdits As edit,
        Patch(colAdminQuestions, LookUp(colAdminQuestions, Slot = edit.Slot),
            {Title: edit.Title, QuestionText: edit.QuestionText,
             GuidanceText: edit.GuidanceText, IsRequired: edit.IsRequired}));
    If(IsBlank(varAdminCategory.ID) || varAdminNewVersion <= varAdminBaseVersion ||
       CountRows(colAdminQuestions) < 3 || CountRows(colAdminQuestions) > 6 ||
       CountRows(Distinct(colAdminQuestions, Slot)) <> CountRows(colAdminQuestions) ||
       CountIf(colAdminQuestions,
           Slot < 1 || Slot > CountRows(colAdminQuestions) || Slot <> RoundDown(Slot, 0) ||
           IsBlank(Trim(Title)) || Len(Title) > 255 || Char(10) in Title ||
           IsBlank(Trim(Substitute(Substitute(Substitute(QuestionText,Char(10)," "),Char(13)," "),Char(9)," ")))
       ) > 0,
        Notify("Supply 3–6 ordered questions, each with a one-line title and question text.", NotificationType.Warning),
        Set(varIsBusy, true);
        Clear(colPublishErrors);
        Set(varPublishOK, true);
        IfError(
            Refresh(AwardCategories);
            Set(varAdminLatestCategory, LookUp(AwardCategories, ID = varAdminCategory.ID));
            If(Coalesce(varAdminLatestCategory.PublishedQuestionVersion, 0) <> varAdminBaseVersion,
                Set(varPublishOK, false);
                Notify("Another version has been published. Reload before making further changes.", NotificationType.Error)
            );
            true,
            Set(varPublishOK, false); false
        );
        If(varPublishOK,
            IfError(
                ForAll(colAdminQuestions As q,
                    With({keyText: varAdminCategory.CategoryCode & "-V" & Text(varAdminNewVersion) & "-Q" & Text(q.Slot)},
                        IfError(
                            With({existing: LookUp(AwardQuestions, ConfigurationKey = keyText)},
                                If(IsBlank(existing.ID),
                                    Patch(AwardQuestions, Defaults(AwardQuestions),
                                        {Title: q.Title,
                                         Category: {Id: varAdminCategory.ID, Value: varAdminCategory.Title},
                                         QuestionSetVersion: varAdminNewVersion,
                                         QuestionKey: {Value: "Q" & Text(q.Slot)},
                                         QuestionText: q.QuestionText, GuidanceText: q.GuidanceText,
                                         DisplayOrder: q.Slot, IsRequired: q.IsRequired,
                                         ConfigurationKey: keyText}
                                    ); true,
                                    existing.Category.Id = varAdminCategory.ID &&
                                    existing.QuestionSetVersion = varAdminNewVersion &&
                                    existing.QuestionKey.Value = "Q" & Text(q.Slot) &&
                                    existing.Title = q.Title && existing.QuestionText = q.QuestionText &&
                                    Coalesce(existing.GuidanceText, "") = q.GuidanceText &&
                                    existing.IsRequired = q.IsRequired && existing.DisplayOrder = q.Slot,
                                    true,
                                    Collect(colPublishErrors, {Slot: q.Slot, Message: "This version/key already contains different content. Allocate a new version."}); false
                                )
                            ),
                            Collect(colPublishErrors, {Slot: q.Slot, Message: "Question save failed. Publication was not completed."}); false
                        )
                    )
                ); true,
                Set(varPublishOK, false); false
            );
            If(CountRows(colPublishErrors) > 0, Set(varPublishOK, false));
            If(varPublishOK,
                IfError(
                    Refresh(AwardQuestions);
                    ClearCollect(colAdminSaved,
                        Filter(AwardQuestions, Category.Id = varAdminCategory.ID,
                            QuestionSetVersion = varAdminNewVersion));
                    If(CountRows(colAdminSaved) <> CountRows(colAdminQuestions) ||
                       CountIf(colAdminQuestions As q,
                           With({saved: LookUp(colAdminSaved, QuestionKey.Value = "Q" & Text(q.Slot))},
                               IsBlank(saved.ID) || saved.DisplayOrder <> q.Slot ||
                               saved.Title <> q.Title || saved.QuestionText <> q.QuestionText ||
                               Coalesce(saved.GuidanceText, "") <> q.GuidanceText || saved.IsRequired <> q.IsRequired ||
                               saved.ConfigurationKey <> varAdminCategory.CategoryCode & "-V" & Text(varAdminNewVersion) & "-Q" & Text(q.Slot)
                           )
                       ) > 0,
                        Set(varPublishOK, false)
                    ); true,
                    Set(varPublishOK, false); false
                )
            );
            If(varPublishOK,
                IfError(
                    Refresh(AwardCategories);
                    Set(varAdminLatestCategory, LookUp(AwardCategories, ID = varAdminCategory.ID));
                    If(Coalesce(varAdminLatestCategory.PublishedQuestionVersion, 0) <> varAdminBaseVersion,
                        Set(varPublishOK, false),
                        Set(varAdminCategory, Patch(AwardCategories, varAdminLatestCategory,
                            {PublishedQuestionVersion: varAdminNewVersion, IsActive: true}));
                        Set(varAdminBaseVersion, varAdminNewVersion);
                        Set(varAdminDirty, false)
                    ); true,
                    Set(varPublishOK, false); false
                )
            )
        );
        Set(varIsBusy, false);
        If(varPublishOK,
            Notify("Question version " & Text(varAdminNewVersion) & " published and category activated.", NotificationType.Success),
            Notify("Publication was not confirmed. Refresh the category pointer before retrying; retained question rows must not be deleted or overwritten.", NotificationType.Error)
        )
    )
)
