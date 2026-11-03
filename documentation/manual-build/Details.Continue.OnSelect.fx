Set(varTeamName, txtTeamName.Text);
Set(varRole, txtRole.Text);
Set(varLevel, Coalesce(cmbLevel.Selected.Value, ""));
Set(varDetailsComplete, DetailsValid);
Set(varDeclarationAccepted, false);
If(varCategoryComplete,
    Switch(varCategory.CategoryCode,
    "IND_INNOVATION", Navigate(scrIndividualInnovation, ScreenTransition.None),
    "IND_CUSTOMER", Navigate(scrIndividualCustomer, ScreenTransition.None),
    "IND_EXCELLENCE", Navigate(scrIndividualExcellence, ScreenTransition.None),
    "TEAM_COLLAB", Navigate(scrTeamCollaboration, ScreenTransition.None),
    "TEAM_IMPACT", Navigate(scrTeamImpact, ScreenTransition.None),
    "TEAM_TRANSFORM", Navigate(scrTeamTransformation, ScreenTransition.None),
    Notify("This category has no configured form.", NotificationType.Error)
),
    Set(varCurrentStep, 2);
    Navigate(scrCategorySelection, ScreenTransition.None)
)
