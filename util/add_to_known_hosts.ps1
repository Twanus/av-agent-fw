# Usage: .\Add-ToKnownHosts.ps1 -Hostname <hostname>
param(
    [string]$Hostname
)

if (-not $Hostname) {
    Write-Host "Usage: .\Add-ToKnownHosts.ps1 -Hostname <hostname>"
    exit 1
}

$knownHostsPath = "$HOME\.ssh\known_hosts"

if (-not (Test-Path $knownHostsPath)) {
    # Debug: Creating known_hosts file
    Write-Host "Debug: Creating known_hosts file at $knownHostsPath"
    New-Item -ItemType File -Path $knownHostsPath -Force
}

# Function to append host keys
function Add-HostKey {
    param (
        [string]$KeyType
    )
    $hostKey = & ssh-keyscan -t $KeyType $Hostname 2>$null
    if ($hostKey) {
        Write-Host "Debug: Adding $KeyType key to known_hosts: $hostKey"
        Add-Content -Path $knownHostsPath -Value $hostKey
    }
    else {
        Write-Host "Debug: No $KeyType key found for $Hostname"
    }
}

# Append each key type separately
Add-HostKey -KeyType "rsa"
Add-HostKey -KeyType "ecdsa"
Add-HostKey -KeyType "ed25519"

Write-Host "Host keys for $Hostname added to known_hosts."

# Print out the contents of the known_hosts file
Write-Host "Contents of known_hosts file:"
Get-Content -Path $knownHostsPath
