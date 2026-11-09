With({u:cmbTeamMemberToAdd.Selected},
    With({claim:"i:0#.f|membership|" & Lower(Coalesce(u.UserPrincipalName,u.Mail))},
        If(!IsBlank(Coalesce(u.UserPrincipalName,u.Mail)) &&
           IsBlank(LookUp(colTeamMembers,Claims=claim)),
            Collect(colTeamMembers,{
                '@odata.type':"#Microsoft.Azure.Connectors.SharePoint.SPListExpandedUser",
                Claims:claim,DisplayName:u.DisplayName,Email:Coalesce(u.Mail,u.UserPrincipalName),
                Department:"",JobTitle:"",Picture:""
            });
            Set(varHasChanges,true); Set(varDeclarationAccepted,false);
            Reset(cmbTeamMemberToAdd)
        )
    )
)
