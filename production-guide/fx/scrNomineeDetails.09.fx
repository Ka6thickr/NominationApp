Switch(varCategory.CategoryCode,
    "IND_CUSTOMER",Choices(MDAward.EmployeeLevel),
    "IND_EXCELLENCE",Choices(TrendMarcherAward.EmployeeLevel),
    "TEAM_COLLAB",Choices(BestInnovatorTeam.EmployeeLevel),
    "TEAM_IMPACT",Choices(MDAwardTeam.EmployeeLevel),
    "TEAM_TRANSFORM",Choices(SpecialTeamAward.EmployeeLevel),
    Choices(BestInnovatorIndividual.EmployeeLevel)
)
