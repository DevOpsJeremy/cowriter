param (
    $BuildDir = 'build',
    $ModuleSource = 'src/cowriter',
    $ModuleName = 'cowriter',
    $PesterConfig = 'pester.psd1'
)
task prepare {
    Remove-Item $BuildDir -Recurse -Force -ErrorAction SilentlyContinue
    Install-Module -Name Pester -SkipPublisherCheck -MinimumVersion 5.0.0
    New-Item $BuildDir -ItemType Directory -Force | Out-Null
}
task clean {
    Remove-Item $BuildDir -Recurse -Force -ErrorAction SilentlyContinue
}
task test prepare, {
    $config = Import-PowerShellDataFile $PesterConfig
    Invoke-Pester -Configuration $config
}
task build prepare, {
    Copy-Item $ModuleSource/$ModuleName.psd1 $BuildDir -Force
    $moduleScript = "$BuildDir/$ModuleName.psm1"
    Get-ChildItem "$ModuleSource/public" -Recurse -File -Filter '*.ps1' -Exclude '*.tests.ps1' -OutVariable functions |
        Get-Content |
        Add-Content $moduleScript -Force
    "Export-ModuleMember -Function $($functions.BaseName -join ', ')" | Add-Content $moduleScript
    Copy-Item "$ModuleSource/files" $BuildDir -Recurse -Force
    Copy-Item README.md $BuildDir -Force
}
task publish build, {
    $modulePath = Resolve-Path $BuildDir
    Publish-Module -Path $modulePath -NuGetApiKey $env:NUGET_API_KEY
}
task . build, test
