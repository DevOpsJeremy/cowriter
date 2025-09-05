[CmdletBinding()]
param (
    [uri] $ollama_download_link = 'https://ollama.com/download/OllamaSetup.exe'
)
function Get-RemoteFileSize {
    [CmdletBinding()]
    param (
        [uri] $Uri
    )
    $response = Invoke-WebRequest -Uri $Uri -Method Head
    return [int] ($response.Headers["Content-Length"] | Select-Object -First 1)
}
