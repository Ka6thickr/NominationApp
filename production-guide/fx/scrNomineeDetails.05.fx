If(IsBlank(varEmployee.Claims),Blank(),
    Table({DisplayName:varEmployee.DisplayName,Mail:varEmployee.Email,
           UserPrincipalName:Last(Split(varEmployee.Claims,"|")).Value})
)
