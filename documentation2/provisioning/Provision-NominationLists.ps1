#requires -Version 7.4
[CmdletBinding()]
param(
    [string]$ConfigPath = (Join-Path $PSScriptRoot 'environment.json'),
    [string]$SeedPath = (Join-Path $PSScriptRoot 'seed-data.json'),
    [string]$ClientId = $env:ENTRAID_APP_ID,
    [switch]$UseExistingConnection,
    [switch]$ValidateOnly,
    [switch]$InspectOnly,
    [switch]$PublishSeed
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$config = Get-Content -LiteralPath $ConfigPath -Raw | ConvertFrom-Json -AsHashtable
$seed = Get-Content -LiteralPath $SeedPath -Raw | ConvertFrom-Json -AsHashtable
$codes = @('IND_INNOVATION','IND_CUSTOMER','IND_EXCELLENCE','TEAM_COLLAB','TEAM_IMPACT','TEAM_TRANSFORM')

function New-FieldDefinition {
    param([string]$Name, [string]$Type, [hashtable]$Options = @{})
    $definition = @{ Name=$Name; Type=$Type; Required=$false; Indexed=$false; Unique=$false }
    foreach ($key in $Options.Keys) { $definition[$key] = $Options[$key] }
    return $definition
}

$categoryFields = @(
    (New-FieldDefinition Title Text @{Required=$true}),
    (New-FieldDefinition CategoryCode Text @{Required=$true; Indexed=$true; Unique=$true}),
    (New-FieldDefinition AwardType Choice @{Required=$true; Choices=@('Individual','Team')}),
    (New-FieldDefinition Description Note),
    (New-FieldDefinition DisplayOrder Number @{Required=$true}),
    (New-FieldDefinition IsActive Boolean @{Default='0'}),
    (New-FieldDefinition PublishedQuestionVersion Number)
)
$questionFields = @(
    (New-FieldDefinition Title Text @{Required=$true}),
    (New-FieldDefinition Category Lookup @{Required=$true; Indexed=$true}),
    (New-FieldDefinition QuestionSetVersion Number @{Required=$true; Indexed=$true}),
    (New-FieldDefinition QuestionKey Choice @{Required=$true; Choices=@('Q1','Q2','Q3','Q4','Q5','Q6')}),
    (New-FieldDefinition QuestionText Note @{Required=$true}),
    (New-FieldDefinition GuidanceText Note),
    (New-FieldDefinition DisplayOrder Number @{Required=$true}),
    (New-FieldDefinition IsRequired Boolean @{Default='1'}),
    (New-FieldDefinition ConfigurationKey Text @{Required=$true; Indexed=$true; Unique=$true})
)
$commonFields = @(
    (New-FieldDefinition Title Text),
    (New-FieldDefinition Category Lookup),
    (New-FieldDefinition QuestionSetVersion Number),
    (New-FieldDefinition QuestionCount Number),
    (New-FieldDefinition NominatedBy User),
    (New-FieldDefinition NominatorEmail Text @{Indexed=$true}),
    (New-FieldDefinition EmployeeRole Text),
    (New-FieldDefinition EmployeeLevel Choice @{Choices=$config.EmployeeLevels}),
    (New-FieldDefinition NominationStatus Choice @{Choices=@('Draft','Submitted'); Default='Draft'; Indexed=$true}),
    (New-FieldDefinition DeclarationAccepted Boolean @{Default='0'}),
    (New-FieldDefinition SubmittedOn DateTime)
)
foreach ($slot in 1..6) {
    $commonFields += New-FieldDefinition "Q${slot}PromptSnapshot" Note
    $commonFields += New-FieldDefinition "Q${slot}RequiredSnapshot" Boolean @{Default='0'}
    $commonFields += New-FieldDefinition "Q${slot}Response" Note
}
$schema = [ordered]@{ Categories=$categoryFields; Questions=$questionFields }
foreach ($code in $codes) {
    $specific = if ($code.StartsWith('IND_')) {
        @(New-FieldDefinition NominatedEmployee User)
    } else {
        @((New-FieldDefinition TeamName Text), (New-FieldDefinition TeamPrimaryContact User), (New-FieldDefinition TeamMembers UserMulti))
    }
    $schema[$code] = @($commonFields) + $specific
}

function ConvertTo-FieldXml {
    param([hashtable]$Definition, [guid]$CategoryListId)
    $document = [System.Xml.XmlDocument]::new()
    $field = $document.CreateElement('Field')
    [void]$document.AppendChild($field)
    $attributes = @{
        ID=([guid]::NewGuid().ToString('B')); Name=$Definition.Name; StaticName=$Definition.Name
        DisplayName=$Definition.Name; Type=$Definition.Type
        Required=$Definition.Required.ToString().ToUpperInvariant()
        Indexed=$Definition.Indexed.ToString().ToUpperInvariant()
        EnforceUniqueValues=$Definition.Unique.ToString().ToUpperInvariant()
    }
    switch ($Definition.Type) {
        'Text' { $attributes.MaxLength = '255' }
        'Note' { $attributes.RichText='FALSE'; $attributes.AppendOnly='FALSE'; $attributes.NumLines='6' }
        'Number' { $attributes.Decimals='0' }
        'Choice' { $attributes.Format='Dropdown'; $attributes.FillInChoice='FALSE' }
        'DateTime' { $attributes.Format='DateTime'; $attributes.StorageTZ='UTC' }
        'Lookup' { $attributes.List=$CategoryListId.ToString('B'); $attributes.ShowField='Title'; $attributes.Mult='FALSE' }
        'User' { $attributes.UserSelectionMode='PeopleOnly'; $attributes.Mult='FALSE' }
        'UserMulti' { $attributes.UserSelectionMode='PeopleOnly'; $attributes.Mult='TRUE' }
    }
    foreach ($key in $attributes.Keys) { $field.SetAttribute($key, [string]$attributes[$key]) }
    if ($Definition.ContainsKey('Choices')) {
        $choicesNode = $document.CreateElement('CHOICES')
        foreach ($value in $Definition.Choices) {
            $choiceNode = $document.CreateElement('CHOICE'); $choiceNode.InnerText = $value
            [void]$choicesNode.AppendChild($choiceNode)
        }
        [void]$field.AppendChild($choicesNode)
    }
    if ($Definition.ContainsKey('Default')) {
        $defaultNode = $document.CreateElement('Default'); $defaultNode.InnerText = $Definition.Default
        [void]$field.AppendChild($defaultNode)
    }
    return $document.OuterXml
}

if ($config.Lists.Count -ne 8 -or @($config.Lists.Values | Select-Object -Unique).Count -ne 8) { throw 'Exactly eight unique list names are required.' }
if ([uri]$config.SiteUrl -isnot [uri] -or -not $config.SiteUrl.StartsWith('https://')) { throw 'An HTTPS site URL is required.' }
if ($config.EmployeeLevels.Count -eq 0) { throw 'EmployeeLevel choices cannot be empty.' }
if ($PublishSeed -and (-not $config.SeedContentApproved -or -not $config.EmployeeLevelsApproved)) { throw 'Approve seed content and employee levels in configuration before publication.' }
if ($seed.Categories.Count -ne 6) { throw 'Expected six seed categories.' }
foreach ($code in $codes) {
    $category = @($seed.Categories | Where-Object CategoryCode -EQ $code)
    if ($category.Count -ne 1) { throw "Missing or duplicate seed category: $code" }
    $category = $category[0]
    $expectedType = if ($code.StartsWith('IND_')) {'Individual'} else {'Team'}
    if ($category.AwardType -ne $expectedType) { throw "Incorrect award type for $code" }
    if ($category.Questions.Count -lt 3 -or $category.Questions.Count -gt 6) { throw "Invalid question count: $code" }
    foreach ($question in $category.Questions) {
        if ([string]::IsNullOrWhiteSpace($question.Title) -or [string]::IsNullOrWhiteSpace($question.QuestionText)) { throw "Empty question in $code" }
    }
}
foreach ($key in $schema.Keys) {
    if (-not $config.Lists.ContainsKey($key)) { throw "Missing list mapping: $key" }
    foreach ($field in $schema[$key]) { [void][xml](ConvertTo-FieldXml $field ([guid]::Empty)) }
    if (@($schema[$key].Name | Select-Object -Unique).Count -ne $schema[$key].Count) { throw "Duplicate column names in $key" }
}
if ($ValidateOnly) {
    [pscustomobject]@{ Result='Local configuration and XML validation passed'; Lists=$schema.Count; CustomColumns=(@($schema.Values | ForEach-Object { $_ } | Where-Object Name -NE 'Title').Count); Categories=6; Questions=(@($seed.Categories | ForEach-Object { $_.Questions }).Count) }
    return
}

Import-Module PnP.PowerShell -MinimumVersion 3.0
if ($UseExistingConnection) { $connection = Get-PnPConnection }
else {
    if (-not $ClientId) { throw 'Supply the approved interactive application ClientId or use an existing connection.' }
    $connection = Connect-PnPOnline -Url $config.SiteUrl -ClientId $ClientId -Interactive -ReturnConnection
}
$web = Get-PnPWeb -Connection $connection
if ($web.Url.TrimEnd('/') -ne $config.SiteUrl.TrimEnd('/')) { throw 'Connection points to a different site. No changes made.' }
$lists = @{}
$allLists = @(Get-PnPList -Connection $connection)
foreach ($key in $schema.Keys) {
    $match = @($allLists | Where-Object Title -EQ $config.Lists[$key])
    if ($match.Count -gt 1) { throw "Ambiguous existing list title: $($config.Lists[$key])" }
    if ($match.Count -eq 1) { $lists[$key]=$match[0] }
}

function Assert-CompatibleField {
    param($Actual, [hashtable]$Expected, [string]$ListKey)
    if ($Actual.TypeAsString -ne $Expected.Type) { throw "Incompatible column type: $ListKey.$($Expected.Name). Expected $($Expected.Type), found $($Actual.TypeAsString)." }
    [xml]$actualXml = $Actual.SchemaXml
    $node = $actualXml.Field
    if ($Expected.Type -eq 'Note' -and ($node.GetAttribute('RichText') -eq 'TRUE' -or $node.GetAttribute('AppendOnly') -eq 'TRUE')) { throw "Incompatible multiline settings: $ListKey.$($Expected.Name)" }
    if ($Expected.Type -eq 'Choice') {
        $existingChoices = @($node.CHOICES.CHOICE | ForEach-Object { [string]$_ })
        if (Compare-Object $existingChoices @($Expected.Choices)) { throw "Choice values differ: $ListKey.$($Expected.Name). Existing data was not changed." }
    }
    if ($Expected.Type -eq 'Lookup') {
        if (-not $lists.ContainsKey('Categories') -or [guid]$node.GetAttribute('List') -ne $lists.Categories.Id) { throw "Lookup points to another list: $ListKey.$($Expected.Name)" }
    }
}

# Inspect every existing target before the first write; authentication/schema errors are not treated as missing lists.
foreach ($key in $schema.Keys) {
    if ($lists.ContainsKey($key)) {
        if ([int]$lists[$key].BaseTemplate -ne 100) { throw "Destination is not a custom list: $key" }
        $actualFields = @(Get-PnPField -List $lists[$key].Id -Connection $connection)
        foreach ($expected in $schema[$key]) {
            $actual = @($actualFields | Where-Object InternalName -CEQ $expected.Name)
            if ($actual.Count -eq 1) { Assert-CompatibleField $actual[0] $expected $key }
        }
    }
}
if ($InspectOnly) {
    foreach ($key in $schema.Keys) { [pscustomobject]@{Key=$key;ListName=$config.Lists[$key];Exists=$lists.ContainsKey($key)} }
    return
}

foreach ($key in $schema.Keys) {
    $name = $config.Lists[$key]
    if (-not $lists.ContainsKey($key)) {
        New-PnPList -Title $name -Template GenericList -EnableVersioning -Connection $connection | Out-Null
        $lists[$key] = Get-PnPList -Identity $name -Connection $connection
        Write-Host "Created $name"
    } else { Write-Host "Reusing $name" }
    $list = $lists[$key]
    Set-PnPList -Identity $list.Id -EnableVersioning $true -Connection $connection | Out-Null
    if ($key -in $codes) {
        Set-PnPList -Identity $list.Id -EnableAttachments $true -ReadSecurity AllUsersReadAccessOnItemsTheyCreate -WriteSecurity WriteOnlyMyItems -Connection $connection | Out-Null
    }
    $actualFields = @(Get-PnPField -List $list.Id -Connection $connection)
    $hasFieldChanges = $false
    foreach ($expected in $schema[$key]) {
        $actual = @($actualFields | Where-Object InternalName -CEQ $expected.Name)
        if ($actual.Count -eq 0) {
            # Queue all missing fields in the PnP connection's supported CSOM context.
            [void]$list.Fields.AddFieldAsXml((ConvertTo-FieldXml $expected $lists.Categories.Id), $false, [Microsoft.SharePoint.Client.AddFieldOptions]::AddFieldInternalNameHint)
            $hasFieldChanges = $true
            continue
        }
        $field = $actual[0]
        $changed = $false
        if ($field.Required -ne $expected.Required) { $field.Required=$expected.Required; $changed=$true }
        if ($expected.Indexed -and -not $field.Indexed) { $field.Indexed=$true; $changed=$true }
        if ($expected.Unique -and -not $field.EnforceUniqueValues) { $field.EnforceUniqueValues=$true; $changed=$true }
        if ($changed) { $field.Update(); $hasFieldChanges=$true }
    }
    if ($hasFieldChanges) { Invoke-PnPQuery -Connection $connection }
    if ($key -in $codes) { Set-PnPField -List $list.Id -Identity Modified -Values @{Indexed=$true} -Connection $connection | Out-Null }
    $defaultView = @(Get-PnPView -List $list.Id -Includes ViewFields,DefaultView -Connection $connection | Where-Object DefaultView)[0]
    # Populate only an untouched starter view; preserve later user view customizations.
    $customViewFields = @($defaultView.ViewFields | Where-Object { $_ -notin @('Attachments','Title','LinkTitle','LinkTitleNoMenu','CategoryCode') })
    if ($customViewFields.Count -eq 0) {
        $viewFields = switch ($key) {
            'Categories' { @('LinkTitle','CategoryCode','AwardType','DisplayOrder','IsActive','PublishedQuestionVersion') }
            'Questions' { @('LinkTitle','Category','QuestionSetVersion','QuestionKey','QuestionText','GuidanceText','IsRequired','DisplayOrder') }
            default {
                $nomineeField = if ($key.StartsWith('IND_')) { 'NominatedEmployee' } else { 'TeamName' }
                @('LinkTitle',$nomineeField,'Category','NominationStatus','Modified','Attachments')
            }
        }
        Set-PnPView -List $list.Id -Identity $defaultView.Id -Fields $viewFields -Connection $connection | Out-Null
    }
    Write-Host "Configured $name ($($schema[$key].Count - 1) custom columns)."
}

$existingCategories = @(Get-PnPListItem -List $lists.Categories.Id -PageSize 100 -Connection $connection)
$existingQuestions = @(Get-PnPListItem -List $lists.Questions.Id -PageSize 100 -Connection $connection)
foreach ($category in $seed.Categories) {
    $code = $category.CategoryCode
    $existing = @($existingCategories | Where-Object { $_['CategoryCode'] -eq $code })
    if ($existing.Count -gt 1) { throw "Duplicate category $code" }
    $isNew = $existing.Count -eq 0
    if ($isNew) {
        $item = Add-PnPListItem -List $lists.Categories.Id -Values @{Title=$category.Title;CategoryCode=$code;AwardType=$category.AwardType;Description=$category.Description;DisplayOrder=$category.DisplayOrder;IsActive=$false} -Connection $connection
    } else { $item = $existing[0] }
    $published = [int]$item['PublishedQuestionVersion']
    # Never modify a published question version or replace business-owned category content.
    if ($published -gt 0) { Write-Host "Preserved published configuration: $code"; continue }
    $slot = 0
    foreach ($question in $category.Questions) {
        $slot++
        $configurationKey = "$code-V1-Q$slot"
        $values = @{Title=$question.Title;Category=$item.Id;QuestionSetVersion=1;QuestionKey="Q$slot";QuestionText=$question.QuestionText;GuidanceText=$question.GuidanceText;DisplayOrder=$slot;IsRequired=$question.IsRequired;ConfigurationKey=$configurationKey}
        $found = @($existingQuestions | Where-Object { $_['ConfigurationKey'] -eq $configurationKey })
        if ($found.Count -eq 0) { Add-PnPListItem -List $lists.Questions.Id -Values $values -Connection $connection | Out-Null }
        elseif ($found.Count -gt 1) { throw "Duplicate configuration key: $configurationKey" }
        else {
            foreach ($column in $values.Keys) {
                $actualValue = if ($column -eq 'Category') { $found[0][$column].LookupId } else { $found[0][$column] }
                if ([string]$actualValue -cne [string]$values[$column]) { throw "Existing draft configuration differs at $configurationKey / $column. It was preserved; review before publishing." }
            }
        }
    }
    $savedQuestions = @(Get-PnPListItem -List $lists.Questions.Id -PageSize 100 -Connection $connection | Where-Object { $_['Category'].LookupId -eq $item.Id -and $_['QuestionSetVersion'] -eq 1 })
    if ($savedQuestions.Count -ne $category.Questions.Count) { throw "Question verification failed for $code; category remains unpublished." }
    $slot = 0
    foreach ($question in $category.Questions) {
        $slot++
        $saved = @($savedQuestions | Where-Object { $_['QuestionKey'] -eq "Q$slot" })
        if ($saved.Count -ne 1 -or $saved[0]['QuestionText'] -cne $question.QuestionText -or [int]$saved[0]['DisplayOrder'] -ne $slot -or $saved[0]['ConfigurationKey'] -cne "$code-V1-Q$slot") { throw "Question content/order verification failed for $code/Q$slot" }
    }
    if ($PublishSeed) {
        $fresh = Get-PnPListItem -List $lists.Categories.Id -Id $item.Id -Connection $connection
        if ([int]$fresh['PublishedQuestionVersion'] -ne $published) { throw "Concurrent publication detected for $code" }
        Set-PnPListItem -List $lists.Categories.Id -Identity $item.Id -Values @{PublishedQuestionVersion=1;IsActive=$true} -Connection $connection | Out-Null
    }
}

$report = foreach ($key in $schema.Keys) {
    $list = Get-PnPList -Identity $lists[$key].Id -Includes EnableVersioning,EnableAttachments,ReadSecurity,WriteSecurity,RootFolder -Connection $connection
    $fields = @(Get-PnPField -List $list.Id -Connection $connection)
    foreach ($expected in $schema[$key]) {
        $field = @($fields | Where-Object InternalName -CEQ $expected.Name)
        if ($field.Count -ne 1) { throw "Missing column after provisioning: $key.$($expected.Name)" }
        Assert-CompatibleField $field[0] $expected $key
        if ($field[0].Required -ne $expected.Required -or ($expected.Indexed -and -not $field[0].Indexed) -or ($expected.Unique -and -not $field[0].EnforceUniqueValues)) { throw "Column constraint verification failed: $key.$($expected.Name)" }
    }
    if (-not $list.EnableVersioning) { throw "Version history disabled: $key" }
    if ($key -in $codes -and (-not $list.EnableAttachments -or $list.ReadSecurity -ne 2 -or $list.WriteSecurity -ne 2)) { throw "Nomination settings verification failed: $key" }
    [ordered]@{Key=$key;ListName=$list.Title;ListId=$list.Id.ToString();Url=([uri]::new([uri]$config.SiteUrl,$list.RootFolder.ServerRelativeUrl).AbsoluteUri);CustomColumns=($schema[$key].Count-1);Verified=$true}
}
$result = [ordered]@{SiteUrl=$web.Url;VerifiedAtUtc=[datetime]::UtcNow.ToString('o');Lists=@($report);SeedPublished=[bool]$PublishSeed;SecurityReviewRequired=$true;Notes=@('Configuration group permissions and removal of ordinary-user delete rights still require approved groups.','Own-item settings do not restrict users with Manage Lists or broader administrator rights.','Submitted-item protection option remains undecided.','Question tags deferred; no tag columns added.')}
$result | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'deployment-result.json') -Encoding utf8
Write-Host 'Verified all eight list schemas. Saved deployment-result.json. No nomination records were seeded.'
