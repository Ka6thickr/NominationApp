LevelOptions = Switch(varCategory.CategoryCode,
    "IND_CUSTOMER",Choices(MDAward.EmployeeLevel),
    "IND_EXCELLENCE",Choices(TrendMarcherAward.EmployeeLevel),
    "TEAM_COLLAB",Choices(BestInnovatorTeam.EmployeeLevel),
    "TEAM_IMPACT",Choices(MDAwardTeam.EmployeeLevel),
    "TEAM_TRANSFORM",Choices(SpecialTeamAward.EmployeeLevel),
    Choices(BestInnovatorIndividual.EmployeeLevel)
);
DetailsValid =
    If(varAwardType = "Individual",
        !IsBlank(varEmployee.Claims),
        !IsBlank(Trim(varTeamName)) && !IsBlank(varPrimaryContact.Claims)
    ) && !IsBlank(Trim(varRole)) && !IsBlank(varLevel) &&
    CountIf(LevelOptions,Value=varLevel)>0;
ResponsesValid =
    varQuestionCount >= 3 && varQuestionCount <= 6 &&
    CountIf(colAnswers, Slot <= varQuestionCount &&
        ((Required && IsBlank(Trim(Substitute(Substitute(Substitute(Response,Char(10)," "),Char(13)," "),Char(9)," ")))) || Len(Response) > varMaxResponseLength)
    ) = 0;
NomineeDisplay = If(varAwardType = "Individual", varEmployee.DisplayName, varTeamName);
NominationReference = If(IsBlank(varNominationId), "Not saved yet",
    varCategory.CategoryCode & "-" & Text(varNominationId, "000000"));
