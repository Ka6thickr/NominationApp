Switch(varCategory.CategoryCode,
    "IND_INNOVATION", Navigate(scrBestInnovatorIndividual, ScreenTransition.None),
    "IND_CUSTOMER", Navigate(scrMDAward, ScreenTransition.None),
    "IND_EXCELLENCE", Navigate(scrTrendMarcherAward, ScreenTransition.None),
    "TEAM_COLLAB", Navigate(scrBestInnovatorTeam, ScreenTransition.None),
    "TEAM_IMPACT", Navigate(scrMDAwardTeam, ScreenTransition.None),
    "TEAM_TRANSFORM", Navigate(scrSpecialTeamAward, ScreenTransition.None),
    Notify("This category has no configured form.", NotificationType.Error)
)
