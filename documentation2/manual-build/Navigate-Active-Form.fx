Switch(varCategory.CategoryCode,
    "IND_INNOVATION", Navigate(scrIndividualInnovation, ScreenTransition.None),
    "IND_CUSTOMER", Navigate(scrIndividualCustomer, ScreenTransition.None),
    "IND_EXCELLENCE", Navigate(scrIndividualExcellence, ScreenTransition.None),
    "TEAM_COLLAB", Navigate(scrTeamCollaboration, ScreenTransition.None),
    "TEAM_IMPACT", Navigate(scrTeamImpact, ScreenTransition.None),
    "TEAM_TRANSFORM", Navigate(scrTeamTransformation, ScreenTransition.None),
    Notify("This category has no configured form.", NotificationType.Error)
)
