Theme = {
    Brand: "Contoso", AppTitle: "Employee & Team Recognition Awards",
    PrimaryHex: "#0f6cbd", SuccessHex: "#107c10", BorderHex: "#d8dee7",
    MutedHex: "#667085", PaleHex: "#eff6fc",
    Primary: ColorValue("#0f6cbd"), PrimaryHover: ColorValue("#0b5a9e"),
    Heading: ColorValue("#17253f"), Body: ColorValue("#27364f"),
    Muted: ColorValue("#667085"), Border: ColorValue("#d8dee7"),
    SoftBorder: ColorValue("#e8ebf0"), Page: ColorValue("#f4f6f8"),
    Surface: ColorValue("#ffffff"), Pale: ColorValue("#eff6fc"),
    Success: ColorValue("#107c10"), SuccessPale: ColorValue("#f1faf1"),
    Error: ColorValue("#c50f1f")
};
LevelOptions = Switch(varCategory.CategoryCode,
    "IND_CUSTOMER",Choices(Nom_IndividualCustomer.EmployeeLevel),
    "IND_EXCELLENCE",Choices(Nom_IndividualExcellence.EmployeeLevel),
    "TEAM_COLLAB",Choices(Nom_TeamCollaboration.EmployeeLevel),
    "TEAM_IMPACT",Choices(Nom_TeamImpact.EmployeeLevel),
    "TEAM_TRANSFORM",Choices(Nom_TeamTransformation.EmployeeLevel),
    Choices(Nom_IndividualInnovation.EmployeeLevel)
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
