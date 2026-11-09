Set(varTeamName, txtTeamName.Text);
Set(varRole, txtRole.Text);
Set(varLevel, Coalesce(cmbLevel.Selected.Value, ""));
Set(varDetailsComplete, DetailsValid);
Set(varDeclarationAccepted, false);
If(varCategoryComplete,
    Switch(varCategory.CategoryCode,
    "IND_INNOVATION", Navigate(scrBestInnovatorIndividual, ScreenTransition.None),
    "IND_CUSTOMER", Navigate(scrMDAward, ScreenTransition.None),
    "IND_EXCELLENCE", Navigate(scrTrendMarcherAward, ScreenTransition.None),
    "TEAM_COLLAB", Navigate(scrBestInnovatorTeam, ScreenTransition.None),
    "TEAM_IMPACT", Navigate(scrMDAwardTeam, ScreenTransition.None),
    "TEAM_TRANSFORM", Navigate(scrSpecialTeamAward, ScreenTransition.None),
    Notify("This category has no configured form.", NotificationType.Error)
),
    Set(varCurrentStep, 2);
    Navigate(scrCategorySelection, ScreenTransition.None)
)
