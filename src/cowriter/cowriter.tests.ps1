Describe module {
    It loads {
        { Import-Module -Name "$PSScriptRoot/cowriter.psd1" -Force -ErrorAction Stop } | Should -Not -Throw
    }
    Context functions {
        $moduleManifest = Import-PowerShellDataFile "$PSScriptRoot/cowriter.psd1"
        $publicFunctions = (Get-ChildItem "$PSScriptRoot/public" -Recurse -File -Filter '*.ps1' -Exclude '*.tests.ps1').BaseName
        $privateFunctions = (Get-ChildItem "$PSScriptRoot/private" -Recurse -File -Filter '*.ps1' -Exclude '*.tests.ps1').BaseName

        BeforeAll {
            $moduleManifest = Import-PowerShellDataFile "$PSScriptRoot/cowriter.psd1"
            $publicFunctions = (Get-ChildItem "$PSScriptRoot/public" -Recurse -File -Filter '*.ps1' -Exclude '*.tests.ps1').BaseName
            $privateFunctions = (Get-ChildItem "$PSScriptRoot/private" -Recurse -File -Filter '*.ps1' -Exclude '*.tests.ps1').BaseName
        }
        Context exported {
            It 'contains <_>' -ForEach $publicFunctions {
                $moduleManifest.FunctionsToExport | Should -Contain $_ -Because "$_ should be exported"
            }
            It '<_> is valid' -ForEach $moduleManifest.FunctionsToExport {
                $publicFunctions | Should -Contain $_ -Because "$_ should be a public function"
            }
            It '<_> is not exported' -ForEach $privateFunctions {
                $moduleManifest.FunctionsToExport | Should -Not -Contain $_ -Because "private function $_ should not be exported"
            }
        }
    }
}
