With({u:Self.Selected},
    If(IsBlank(Coalesce(u.UserPrincipalName,u.Mail)),
        Set(varEmployee,varEmptyPerson),
        Set(varEmployee,{
            '@odata.type':"#Microsoft.Azure.Connectors.SharePoint.SPListExpandedUser",
            Claims:"i:0#.f|membership|" & Lower(Coalesce(u.UserPrincipalName,u.Mail)),
            DisplayName:u.DisplayName,Email:Coalesce(u.Mail,u.UserPrincipalName),
            Department:"",JobTitle:"",Picture:""
        })
    )
);
Set(varHasChanges,true); Set(varDetailsComplete,false);
Set(varDeclarationAccepted,false)
