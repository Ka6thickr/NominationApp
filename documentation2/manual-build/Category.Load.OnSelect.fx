If(!varIsBusy,
    If(varCategoryComplete && varPendingCategory.ID = varCategory.ID,
        Switch(varCategory.CategoryCode,
    "IND_INNOVATION", Navigate(scrIndividualInnovation, ScreenTransition.None),
    "IND_CUSTOMER", Navigate(scrIndividualCustomer, ScreenTransition.None),
    "IND_EXCELLENCE", Navigate(scrIndividualExcellence, ScreenTransition.None),
    "TEAM_COLLAB", Navigate(scrTeamCollaboration, ScreenTransition.None),
    "TEAM_IMPACT", Navigate(scrTeamImpact, ScreenTransition.None),
    "TEAM_TRANSFORM", Navigate(scrTeamTransformation, ScreenTransition.None),
    Notify("This category has no configured form.", NotificationType.Error)
),
        Set(varIsBusy, true);
        Set(varLoadOK, true);
        IfError(
            Refresh(AwardCategories);
            Set(varCandidateCategory, LookUp(AwardCategories, ID = varPendingCategory.ID));
            Refresh(AwardQuestions);
            ClearCollect(colCandidateQuestions,
                SortByColumns(Filter(AwardQuestions,
                    Category.Id = varCandidateCategory.ID,
                    QuestionSetVersion = varCandidateCategory.PublishedQuestionVersion
                ), "DisplayOrder", SortOrder.Ascending)
            );
            true,
            Set(varLoadOK, false); false
        );
        If(!varLoadOK || IsBlank(varCandidateCategory.ID) || !varCandidateCategory.IsActive ||
           varCandidateCategory.AwardType.Value <> varAwardType ||
           Switch(varCandidateCategory.CategoryCode,
             "IND_INNOVATION", "Individual", "IND_CUSTOMER", "Individual", "IND_EXCELLENCE", "Individual",
             "TEAM_COLLAB", "Team", "TEAM_IMPACT", "Team", "TEAM_TRANSFORM", "Team", "") <> varAwardType ||
           Coalesce(varCandidateCategory.PublishedQuestionVersion, 0) < 1 ||
           CountRows(colCandidateQuestions) < 3 || CountRows(colCandidateQuestions) > 6 ||
           CountRows(Distinct(colCandidateQuestions, DisplayOrder)) <> CountRows(colCandidateQuestions) ||
           CountIf(colCandidateQuestions,
               DisplayOrder < 1 || DisplayOrder > CountRows(colCandidateQuestions) ||
               DisplayOrder <> RoundDown(DisplayOrder, 0) ||
               QuestionKey.Value <> "Q" & Text(DisplayOrder) ||
               ConfigurationKey <> varCandidateCategory.CategoryCode & "-V" & Text(QuestionSetVersion) & "-" & QuestionKey.Value ||
               IsBlank(Trim(Title)) || Char(10) in Title ||
               IsBlank(Trim(Substitute(Substitute(Substitute(QuestionText,Char(10)," "),Char(13)," "),Char(9)," ")))
           ) > 0,
            Set(varIsBusy, false);
            Notify("This category does not have a valid published set of 3–6 questions. Contact the configuration manager.", NotificationType.Error),
            Set(varCategory, varCandidateCategory);
            Set(varQuestionVersion, varCandidateCategory.PublishedQuestionVersion);
            Set(varQuestionCount, CountRows(colCandidateQuestions));
            ClearCollect(colAnswers,
                ForAll(Sequence(6) As n,
                    With({q: LookUp(colCandidateQuestions, DisplayOrder = n.Value)},
                        {Slot: n.Value,
                         Prompt: If(n.Value <= varQuestionCount,
                             q.Title & Char(10) & q.QuestionText &
                             If(IsBlank(q.GuidanceText), "", Char(10) & Char(10) & "Guidance: " & q.GuidanceText), ""),
                         Required: If(n.Value <= varQuestionCount, q.IsRequired, false),
                         Response: ""}
                    )
                )
            );
            Set(varCategoryComplete, true);
            Set(varResponsesComplete, false);
            Set(varDeclarationAccepted, false);
            Set(varHasChanges, true);
            Set(varShowCategoryChangeDialog, false);
            ResetForm(frmIndividualInnovation); NewForm(frmIndividualInnovation);
            ResetForm(frmIndividualCustomer); NewForm(frmIndividualCustomer);
            ResetForm(frmIndividualExcellence); NewForm(frmIndividualExcellence);
            ResetForm(frmTeamCollaboration); NewForm(frmTeamCollaboration);
            ResetForm(frmTeamImpact); NewForm(frmTeamImpact);
            ResetForm(frmTeamTransformation); NewForm(frmTeamTransformation);
            Set(varIsBusy, false);
            Set(varCurrentStep, 3);
            Switch(varCategory.CategoryCode,
    "IND_INNOVATION", Navigate(scrIndividualInnovation, ScreenTransition.None),
    "IND_CUSTOMER", Navigate(scrIndividualCustomer, ScreenTransition.None),
    "IND_EXCELLENCE", Navigate(scrIndividualExcellence, ScreenTransition.None),
    "TEAM_COLLAB", Navigate(scrTeamCollaboration, ScreenTransition.None),
    "TEAM_IMPACT", Navigate(scrTeamImpact, ScreenTransition.None),
    "TEAM_TRANSFORM", Navigate(scrTeamTransformation, ScreenTransition.None),
    Notify("This category has no configured form.", NotificationType.Error)
)
        )
    )
)
