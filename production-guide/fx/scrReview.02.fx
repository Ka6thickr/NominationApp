"Nomination type: " & varAwardType & Char(10) &
"Category: " & varCategory.Title & Char(10) &
"Nominated by: " & varNominator.DisplayName & Char(10) &
If(varAwardType="Individual",
    "Nominee: " & varEmployee.DisplayName,
    "Team: " & varTeamName & Char(10) &
    "Primary contact: " & varPrimaryContact.DisplayName & Char(10) &
    "Team members: " & If(IsEmpty(colTeamMembers),"None added",Concat(colTeamMembers,DisplayName,", "))
) & Char(10) &
"Role: " & varRole & Char(10) & "Level: " & varLevel & Char(10) &
"Question version: " & Text(varQuestionVersion)
