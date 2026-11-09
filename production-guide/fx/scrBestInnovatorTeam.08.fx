If(!varIsBusy,
    Set(varIsBusy, true);
    Set(varOpenOK, true);
    IfError(
        Refresh(BestInnovatorTeam);
        Set(varRecordTC, LookUp(BestInnovatorTeam, ID = ThisItem.ID && NominatorEmail = varUserEmail));
        Refresh(AwardCategories);
        Set(varCategory, LookUp(AwardCategories, ID = varRecordTC.Category.Id));
        true,
        Set(varOpenOK, false);
        false
    );
    If(!varOpenOK || IsBlank(varRecordTC.ID) || varCategory.CategoryCode <> "TEAM_COLLAB" ||
       IsBlank(varRecordTC.QuestionSetVersion) || varRecordTC.QuestionSetVersion < 1 ||
       IsBlank(varRecordTC.QuestionCount) || varRecordTC.QuestionCount < 3 || varRecordTC.QuestionCount > 6 ||
       varRecordTC.QuestionCount <> RoundDown(varRecordTC.QuestionCount,0) ||
       IsBlank(varRecordTC.Q1PromptSnapshot) || IsBlank(varRecordTC.Q2PromptSnapshot) || IsBlank(varRecordTC.Q3PromptSnapshot) ||
       (varRecordTC.QuestionCount>=4 && IsBlank(varRecordTC.Q4PromptSnapshot)) ||
       (varRecordTC.QuestionCount>=5 && IsBlank(varRecordTC.Q5PromptSnapshot)) ||
       (varRecordTC.QuestionCount>=6 && IsBlank(varRecordTC.Q6PromptSnapshot)) ||
       !(varRecordTC.NominationStatus.Value in ["Draft", "Submitted"]),
        Set(varIsBusy, false);
        Notify("Unable to open this nomination. Check access and the saved category/question metadata.", NotificationType.Error),
        Set(varAwardType, "Team");
        Set(varNominationId, varRecordTC.ID);
        Set(varLoadedModified, varRecordTC.Modified);
        Set(varQuestionVersion, varRecordTC.QuestionSetVersion);
        Set(varQuestionCount, varRecordTC.QuestionCount);
        Set(varRole, Coalesce(varRecordTC.EmployeeRole, ""));
        Set(varLevel, Coalesce(varRecordTC.EmployeeLevel.Value, ""));
        Set(varNominator, varRecordTC.NominatedBy);
        Set(varTeamName, Coalesce(varRecordTC.TeamName, ""));
        Set(varPrimaryContact, Coalesce(varRecordTC.TeamPrimaryContact, varEmptyPerson));
        Set(varEmployee, varEmptyPerson);
        ClearCollect(colTeamMembers, varRecordTC.TeamMembers);
        ClearCollect(colAnswers, Table(
    {Slot: 1, Prompt: Coalesce(varRecordTC.Q1PromptSnapshot, ""), Required: Coalesce(varRecordTC.Q1RequiredSnapshot, false), Response: Coalesce(varRecordTC.Q1Response, "")},
    {Slot: 2, Prompt: Coalesce(varRecordTC.Q2PromptSnapshot, ""), Required: Coalesce(varRecordTC.Q2RequiredSnapshot, false), Response: Coalesce(varRecordTC.Q2Response, "")},
    {Slot: 3, Prompt: Coalesce(varRecordTC.Q3PromptSnapshot, ""), Required: Coalesce(varRecordTC.Q3RequiredSnapshot, false), Response: Coalesce(varRecordTC.Q3Response, "")},
    {Slot: 4, Prompt: Coalesce(varRecordTC.Q4PromptSnapshot, ""), Required: Coalesce(varRecordTC.Q4RequiredSnapshot, false), Response: Coalesce(varRecordTC.Q4Response, "")},
    {Slot: 5, Prompt: Coalesce(varRecordTC.Q5PromptSnapshot, ""), Required: Coalesce(varRecordTC.Q5RequiredSnapshot, false), Response: Coalesce(varRecordTC.Q5Response, "")},
    {Slot: 6, Prompt: Coalesce(varRecordTC.Q6PromptSnapshot, ""), Required: Coalesce(varRecordTC.Q6RequiredSnapshot, false), Response: Coalesce(varRecordTC.Q6Response, "")}
));
        Set(varReadOnly, varRecordTC.NominationStatus.Value = "Submitted");
        Set(varSubmissionComplete, varReadOnly);
        Set(varSubmittedOn, varRecordTC.SubmittedOn);
        Set(varCategoryComplete, true);
        Set(varDetailsComplete, DetailsValid);
        Set(varResponsesComplete, ResponsesValid);
        Set(varDeclarationAccepted, false);
        Set(varHasChanges, false);
        Set(varSaveIntent, "Draft");
        ResetForm(frmBestInnovatorTeam);
        If(varReadOnly, ViewForm(frmBestInnovatorTeam), EditForm(frmBestInnovatorTeam));
        Set(varIsBusy, false);
        Navigate(scrBestInnovatorTeam, ScreenTransition.None)
    )
)
