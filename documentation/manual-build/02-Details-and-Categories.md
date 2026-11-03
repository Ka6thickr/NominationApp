# Step 1 — details; step 2 — category selection

Build the page shell first. These screen controls are shared by all six category forms. A nominee can be entered before selecting a category, but nothing is saved until a category identifies the destination list.

## 1. Home

Heading: **Employee & Team Recognition Awards** from `Theme.AppTitle`. Add brief instruction text describing the four stages. Add New nomination and My nominations native buttons. New uses `NewNomination.OnSelect.fx`; My uses `Navigate(scrMyNominations,ScreenTransition.None)`. Add Manage questions with Visible `varCanManageQuestions` and OnSelect `Navigate(scrQuestionAdministration,ScreenTransition.None)`. Keep the Home page simple; the supplied nomination design starts with the actual step-1 screen.

## 2. scrNomineeDetails

OnVisible:

```powerfx
Set(varCurrentStep, 1)
```

Heading “Nominee details”; subtitle “Choose the nomination type and tell us who you are recognizing.” These are UI instructions, not question content. Add white `cntDetailsCard` with the card styling in the layout guide. X/Width match the page heading; Y after subtitle +26. Internal horizontal padding `If(App.Width<=760,17,34)` and top padding `If(App.Width<=760,21,30)`. In the measurements below, `padding` means the expression `If(App.Width<=760,17,34)`, not an undeclared Power Fx variable. Use native controls in the following order. For each successive field label set Y to the previous visible control's Y+Height+18; its input starts at label.Y+label.Height+7. Use zero Height for hidden nominee/team sections so following fields move upward.

### A. Type cards

Add label “Nomination type”, then `btnIndividualType` and `btnTeamType`, approximately 103px high. Desktop widths `(Min(590,Parent.Width-2*padding)-16)/2`, horizontal gap16; mobile stack, full available width. Use Fill `If(varAwardType="Individual",Theme.Pale,Theme.Surface)` for Individual, analogous Team; BorderColor primary when selected else border; BorderThickness 2 when selected else1; corner radii7. Text “Individual award” / “Team award”, Size12.75, Semibold, Align.Left, PaddingLeft18. A check icon or label with “Selected” is visible only on the selected card.

Individual OnSelect:

```powerfx
If(!varCategoryComplete,
    Set(varAwardType,"Individual");
    Set(varHasChanges,true); Set(varDetailsComplete,false);
    Set(varDeclarationAccepted,false)
)
```

Team OnSelect changes the literal to `"Team"`. DisplayMode for both:

```powerfx
If(varIsBusy || varReadOnly || varCategoryComplete,DisplayMode.Disabled,DisplayMode.Edit)
```

Award type locks once questions have been loaded, even before the first save, to avoid applying team inputs to an individual form. To start a different type after that point, use New nomination and confirm discarding unsaved changes. Before category selection, changing the type may retain hidden in-memory detail values for convenience; only the chosen type is stored by its typed form. There is no silent default category.

### B. Nominator

Label “Nominated by”; read-only person row Text `User().FullName & Char(10) & varUserEmail`. Width `Min(590,Parent.Width-2*padding)`, Height56, Size9.75, white/pale fill. This is the signed-in nominator, never an editable field. On resumed records the form saves its loaded `varNominator`; My nominations only opens the current user's records.

### C. Individual nominee — cmbNominee

Visible `varAwardType="Individual"`. Label “Nominee *”. Use a classic single-select Combo box `cmbNominee`, 56px high, width up to590. Apply directory style from the layout guide. Items:

```powerfx
If(Len(Self.SearchText)<2,
    Blank(),
    IfError(Office365Users.SearchUserV2(
        {searchTerm:Self.SearchText,top:25,isSearchTermRequired:true}
    ).value, Blank())
)
```

This is a bounded directory search, not a locally copied directory. Search term and returned field names come from [Office 365 Users SearchUserV2](https://learn.microsoft.com/en-us/connectors/office365users/). Show helper text “Enter at least two characters. If no results appear, refine the search or check the directory connection.” Tenant policies can affect results; test with real authorized accounts.

DefaultSelectedItems:

```powerfx
If(IsBlank(varEmployee.Claims),Blank(),
    Table({DisplayName:varEmployee.DisplayName,Mail:varEmployee.Email,
           UserPrincipalName:Last(Split(varEmployee.Claims,"|")).Value})
)
```

OnChange:

```powerfx
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
```

Use UPN for the membership claim and Mail for display where available; do not assume they are always identical. Test guest identities separately if they will be allowed. The fixed schema does not include a guest/employee eligibility policy.

### D. Team controls

Put these in manual container `cntTeamDetails` with Visible `varAwardType="Team"`, Height based on its last child. When hidden set its Height to0 so following fields move up. Add:

1. `txtTeamName`, label “Team name *”, Default `varTeamName`, MaxLength255, single-line. OnChange: `Set(varTeamName,Self.Text); Set(varHasChanges,true); Set(varDetailsComplete,false); Set(varDeclarationAccepted,false)`.
2. `cmbPrimaryContact`, label “Primary contact *”. Same directory Items formula and Combo styling as cmbNominee. DefaultSelectedItems uses `varPrimaryContact` instead of `varEmployee`. Its full OnChange is the cmbNominee formula with only `varEmployee` changed to `varPrimaryContact`.
3. `cmbTeamMemberToAdd`, label “Team members (optional)”, same directory Items, DefaultSelectedItems `Blank()`, SelectMultiple false. An Add member button appears alongside it. We use explicit Add/Remove so selected members remain visible even when a new directory search changes the result set.
4. Gallery `galTeamMembers`, Items `colTeamMembers`, TemplateSize40, Height `Min(200,CountRows(colTeamMembers)*40)`, ShowScrollbar true. Labels show ThisItem.DisplayName; remove icon/button OnSelect `Remove(colTeamMembers,ThisItem); Set(varHasChanges,true); Set(varDeclarationAccepted,false)`. Disable removal while busy/read-only.

Add member button OnSelect:

```powerfx
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
```

Team members are optional and may include the primary contact unless business rules later say otherwise. Do not invent a mandatory team-member count.

### E. Role and level

Below the visible nominee/team section add `cntRoleLevel`. Width `Min(590,card.Width-2*padding)`. Desktop Height80, mobile Height170. Role label “Nominee role *” for Individual, “Primary contact role *” for Team. Level label likewise. Desktop two columns `(Parent.Width-18)/2`; mobile full width, level starts90px below role.

`txtRole`: Default `varRole`; MaxLength255; Height40. OnChange:

```powerfx
Set(varRole,Self.Text);
Set(varHasChanges,true); Set(varDetailsComplete,false);
Set(varDeclarationAccepted,false)
```

`cmbLevel`: classic Combo, SelectMultiple false; IsSearchable false; DisplayFields `["Value"]`; SearchFields `["Value"]`; Height40; InputTextPlaceholder “Select level”. Items read actual choice metadata:

```powerfx
Switch(varCategory.CategoryCode,
    "IND_CUSTOMER",Choices(Nom_IndividualCustomer.EmployeeLevel),
    "IND_EXCELLENCE",Choices(Nom_IndividualExcellence.EmployeeLevel),
    "TEAM_COLLAB",Choices(Nom_TeamCollaboration.EmployeeLevel),
    "TEAM_IMPACT",Choices(Nom_TeamImpact.EmployeeLevel),
    "TEAM_TRANSFORM",Choices(Nom_TeamTransformation.EmployeeLevel),
    Choices(Nom_IndividualInnovation.EmployeeLevel)
)
```

The same expression is defined centrally as `LevelOptions` in App.Formulas, so you can set Items to `LevelOptions`. Before category selection the IndividualInnovation list supplies the common level choices; maintain identical choice values across all six lists. DefaultSelectedItems `Filter(LevelOptions,Value=varLevel)`. DetailsValid also checks the level is still an allowed choice. OnChange:

```powerfx
Set(varLevel,Coalesce(Self.Selected.Value,""));
Set(varHasChanges,true); Set(varDetailsComplete,false);
Set(varDeclarationAccepted,false)
```

Below controls show a muted helper: “Required details are needed before review. You can select a category and save an incomplete draft.” `cntDetailsCard.Height` = last helper Y + Height +30; action row below card+24. Continue OnSelect is [Details.Continue.OnSelect.fx](Details.Continue.OnSelect.fx). It captures text values directly, then goes to category selection, or back to the existing form when a category is already loaded. Continue is allowed with incomplete details **to permit incomplete drafts**; review is not. Save draft is not present on this screen because a new record may not yet have a destination.

## 3. scrCategorySelection

OnVisible:

```powerfx
Set(varCurrentStep,2);
Set(varCategoryLoadError,false);
IfError(
    Refresh(AwardCategories);
    ClearCollect(colCategoryOptions,SortByColumns(
        Filter(AwardCategories,IsActive=true,AwardType.Value=varAwardType),
        "DisplayOrder",SortOrder.Ascending));
    true,
    Set(varCategoryLoadError,true);
    Clear(colCategoryOptions);
    false
)
```

This collection is the bounded category configuration (three categories per type), not nomination data. Add heading “Award category” and subtitle “Choose the category that best matches the nomination.” Add a summary strip with current nominee/type. Back OnSelect `Navigate(scrNomineeDetails,ScreenTransition.None)`.

### A. Category cards

Insert vertical gallery `galCategories` with Items `colCategoryOptions`. Set WrapCount `If(App.Width<=760,1,3)`, TemplatePadding8, TemplateSize261, Width equal to page inner width. Height `If(App.Width<=760,CountRows(colCategoryOptions)*261,261)`. Remove generated image/body controls. Inside each item add a manual container Width `Parent.TemplateWidth-16`, Height245, X8, Y8, Fill `If(ThisItem.ID=varPendingCategory.ID,Theme.Pale,Theme.Surface)`, BorderColor primary if selected else border, BorderThickness2 if selected else1, corner radii8.

Add a small native icon in a 43px pale square, heading Title label X20 Y78 WidthParent.Width-40 AutoHeight Size12.75 Semibold, description X20 Yheadingbottom+10 WidthParent.Width-40 AutoHeight Size9.75, and Selected indicator in top right. Icons can be stable per category code, but text/order/availability come from SharePoint. As a baseline use the same award SVG for all categories; icon differences are cosmetic and do not require new columns. Verify long descriptions fit; increase card/gallery row height together if business copy is longer.

Add a native transparent selection button within the gallery template, outside the decorative container so `ThisItem` is the gallery item. X/Y8, WidthParent.TemplateWidth-16, Height245, Text `""`, AccessibleLabel `"Select " & ThisItem.Title`. OnSelect:

```powerfx
Set(varPendingCategory,ThisItem)
```

Use a clearly visible focus border. DisplayMode disabled when busy or when a nomination has already been saved. A saved record never changes category/version through this screen.

Empty-state label Visible `!varCategoryLoadError && IsEmpty(colCategoryOptions)`, Text “No categories are currently published for this nomination type.” Error label Visible varCategoryLoadError, Text “Categories could not be loaded. Check the connection and try again.” Add Retry `Select(btnRefreshCategories)` only if a same-screen hidden button holds the OnVisible refresh code; alternatively paste that refresh block directly into Retry. Do not make an empty state look like a loading spinner indefinitely.

### B. Load the selected question version

Add same-screen hidden `btnLoadCategory`, DisplayMode.Edit, OnSelect the full [Category.Load.OnSelect.fx](Category.Load.OnSelect.fx). It re-reads the selected category/published pointer and validates 3–6 ordered Q1..QN rows before initializing snapshots. Changing an unsaved selection resets all form controls and queued evidence **only after confirmation and successful configuration validation**. Returning to the same selected category preserves current answers and attachments.

Continue DisplayMode:

```powerfx
If(varIsBusy || IsBlank(varPendingCategory.ID) || !IsBlank(varNominationId),
    DisplayMode.Disabled,DisplayMode.Edit)
```

Continue OnSelect:

```powerfx
If(varCategoryComplete && varPendingCategory.ID<>varCategory.ID,
    Set(varShowCategoryChangeDialog,true),
    Select(btnLoadCategory)
)
```

Add a modal dialog Visible `varShowCategoryChangeDialog`: “Changing category clears the current responses and selected evidence. Nominee details will be retained.” Cancel `Set(varShowCategoryChangeDialog,false)`. Confirm `Select(btnLoadCategory)`. Disable both while busy. Configuration errors retain the old answers and let the user cancel the dialog.

On each step-3 form, add Change category button Visible `!varReadOnly && IsBlank(varNominationId)`, OnSelect:

```powerfx
Set(varPendingCategory,varCategory);
Set(varDeclarationAccepted,false);
Navigate(scrCategorySelection,ScreenTransition.None)
```

No new snapshot is fetched when resuming a saved draft; use the per-category gallery Open formula instead. Seed rows remain inactive until an approved administrator publishes them. The UI must not automatically substitute prototype questions when no published configuration exists.

Continue with the six [typed form recipes](Form-Mapping.md), then [review, browse and administration](03-Review-Browse-and-Administration.md).
