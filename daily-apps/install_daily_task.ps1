$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$generator = Join-Path $PSScriptRoot "generate_daily_app.py"
$pythonCommand = Get-Command python.exe -ErrorAction Stop
$python = $pythonCommand.Source
$taskName = "Boredom-Busters Daily Website"

if (-not (Test-Path -LiteralPath $generator -PathType Leaf)) {
    throw "Daily website generator was not found: $generator"
}

$service = New-Object -ComObject "Schedule.Service"
$service.Connect()
$folder = $service.GetFolder("\")
$definition = $service.NewTask(0)
$definition.RegistrationInfo.Description = "Adds one new Boredom-Busters mini website each day at midnight."
$definition.Settings.Enabled = $true
$definition.Settings.StartWhenAvailable = $true
$definition.Settings.MultipleInstances = 2
$definition.Settings.ExecutionTimeLimit = "PT15M"
$definition.Settings.DisallowStartIfOnBatteries = $false
$definition.Settings.StopIfGoingOnBatteries = $false
$definition.Principal.UserId = "$env:USERDOMAIN\$env:USERNAME"
$definition.Principal.LogonType = 3
$definition.Principal.RunLevel = 0

$trigger = $definition.Triggers.Create(2)
$trigger.StartBoundary = (Get-Date).Date.AddDays(1).ToString("s")
$trigger.DaysInterval = 1
$trigger.Enabled = $true

$action = $definition.Actions.Create(0)
$action.Path = $python
$action.Arguments = "`"$generator`""
$action.WorkingDirectory = $root

$null = $folder.RegisterTaskDefinition($taskName, $definition, 6, $null, $null, 3)
Write-Output "Scheduled '$taskName' to run daily at midnight, starting $($trigger.StartBoundary)."
Write-Output "The computer must be on and your Windows account signed in. Missed runs start when available."
