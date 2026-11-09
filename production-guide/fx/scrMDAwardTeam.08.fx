If(!varIsBusy,
    Set(varIsBusy, true);
    Set(varOpenOK, true);
    IfError(
        Refresh(MDAwardTeam);
        Set(varRecordTI, LookUp(MDAwardTeam, ID = ThisItem.ID && NominatorEmail = varUserEmail));
        Refresh(AwardCategories);
        Set(varCategory, LookUp(AwardCategories, ID = varRecordTI.Category.Id));
        true,
        Set(varOpenOK, false);
        false
    );
    If(!varOpenOK || IsBlank(varRecordTI.ID) || varCategory.CategoryCode <> "TEAM_IMPACT" ||
       IsBlank(varRecordTI.QuestionSetVersion) || varRecordTI.QuestionSetVersion < 1 ||
       IsBlank(varRecordTI.QuestionCount) || varRecordTI.QuestionCount < 3 || varRecordTI.QuestionCount > 6 ||
       varRecordTI.QuestionCount <> RoundDown(varRecordTI.QuestionCount,0) ||
       IsBlank(varRecordTI.Q1PromptSnapshot) || IsBlank(varRecordTI.Q2PromptSnapshot) || IsBlank(varRecordTI.Q3PromptSnapshot) ||
       (varRecordTI.QuestionCount>=4 && IsBlank(varRecordTI.Q4PromptSnapshot)) ||
       (varRecordTI.QuestionCount>=5 && IsBlank(varRecordTI.Q5PromptSnapshot)) ||
       (varRecordTI.QuestionCount>=6 && IsBlank(varRecordTI.Q6PromptSnapshot)) ||
       !(varRecordTI.NominationStatus.Value in ["Draft", "Submitted"]),
        Set(varIsBusy, false);
        Notify("Unable to open this nomination. Check access and the saved category/question metadata.", NotificationType.Error),
        Set(varAwardType, "Team");
        Set(varNominationId, varRecordTI.ID);
        Set(varLoadedModified, varRecordTI.Modified);
        Set(varQuestionVersion, varRecordTI.QuestionSetVersion);
        Set(varQuestionCount, varRecordTI.QuestionCount);
        Set(varRole, Coalesce(varRecordTI.EmployeeRole, ""));
        Set(varLevel, Coalesce(varRecordTI.EmployeeLevel.Value, ""));
        Set(varNominator, varRecordTI.NominatedBy);
        Set(varTeamName, Coalesce(varRecordTI.TeamName, ""));
        Set(varPrimaryContact, Coalesce(varRecordTI.TeamPrimaryContact, varEmptyPerson));
        Set(varEmployee, varEmptyPerson);
        ClearCollect(colTeamMembers, varRecordTI.TeamMembers);
        ClearCollect(colAnswers, Table(
    {Slot: 1, Prompt: Coalesce(varRecordTI.Q1PromptSnapshot, ""), Required: Coalesce(varRecordTI.Q1RequiredSnapshot, false), Response: Coalesce(varRecordTI.Q1Response, "")},
    {Slot: 2, Prompt: Coalesce(varRecordTI.Q2PromptSnapshot, ""), Required: Coalesce(varRecordTI.Q2RequiredSnapshot, false), Response: Coalesce(varRecordTI.Q2Response, "")},
    {Slot: 3, Prompt: Coalesce(varRecordTI.Q3PromptSnapshot, ""), Required: Coalesce(varRecordTI.Q3RequiredSnapshot, false), Response: Coalesce(varRecordTI.Q3Response, "")},
    {Slot: 4, Prompt: Coalesce(varRecordTI.Q4PromptSnapshot, ""), Required: Coalesce(varRecordTI.Q4RequiredSnapshot, false), Response: Coalesce(varRecordTI.Q4Response, "")},
    {Slot: 5, Prompt: Coalesce(varRecordTI.Q5PromptSnapshot, ""), Required: Coalesce(varRecordTI.Q5RequiredSnapshot, false), Response: Coalesce(varRecordTI.Q5Response, "")},
    {Slot: 6, Prompt: Coalesce(varRecordTI.Q6PromptSnapshot, ""), Required: Coalesce(varRecordTI.Q6RequiredSnapshot, false), Response: Coalesce(varRecordTI.Q6Response, "")}
));
        Set(varReadOnly, varRecordTI.NominationStatus.Value = "Submitted");
        Set(varSubmissionComplete, varReadOnly);
        Set(varSubmittedOn, varRecordTI.SubmittedOn);
        Set(varCategoryComplete, true);
        Set(varDetailsComplete, DetailsValid);
        Set(varResponsesComplete, ResponsesValid);
        Set(varDeclarationAccepted, false);
        Set(varHasChanges, false);
        Set(varSaveIntent, "Draft");
        ResetForm(frmMDAwardTeam);
        If(varReadOnly, ViewForm(frmMDAwardTeam), EditForm(frmMDAwardTeam));
        Set(varIsBusy, false);
        Navigate(scrMDAwardTeam, ScreenTransition.None)
    )
)
