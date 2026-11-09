Set(varBrowseError,false);
IfError(
    Refresh(AwardCategories);
    ClearCollect(colBrowseCategories,SortByColumns(AwardCategories,"DisplayOrder",SortOrder.Ascending));
    Switch(varBrowseCode,
        "IND_INNOVATION",Refresh(BestInnovatorIndividual),
        "IND_CUSTOMER",Refresh(MDAward),
        "IND_EXCELLENCE",Refresh(TrendMarcherAward),
        "TEAM_COLLAB",Refresh(BestInnovatorTeam),
        "TEAM_IMPACT",Refresh(MDAwardTeam),
        "TEAM_TRANSFORM",Refresh(SpecialTeamAward)
    ); true,
    Set(varBrowseError,true); false
)
