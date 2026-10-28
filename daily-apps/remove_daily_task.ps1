$ErrorActionPreference = "Stop"
$taskName = "Boredom-Busters Daily Website"
$service = New-Object -ComObject "Schedule.Service"
$service.Connect()
$folder = $service.GetFolder("\")

try {
    $folder.DeleteTask($taskName, 0)
    Write-Output "Removed scheduled task '$taskName'."
} catch {
    if ($_.Exception.Message -match "cannot find|does not exist|not found") {
        Write-Output "Scheduled task '$taskName' was not installed."
    } else {
        throw
    }
}
