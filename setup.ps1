#requires -Version 5.1
using namespace System.Windows
using namespace System.Windows.Controls

[CmdletBinding()]
param (
    [uri] $OllamaDownloadUrl = 'https://ollama.com/download/OllamaSetup.exe'
)
Begin {
    #region Functions
    function Get-RemoteFileSize {
        [CmdletBinding()]
        param (
            [uri] $Uri
        )
        $response = Invoke-WebRequest -Uri $Uri -Method Head
        return [int] ($response.Headers["Content-Length"] | Select-Object -First 1)
    }
    function Build-Window {
        [CmdletBinding()]
        param ()

        #region Functions
        function Set-PageContent {
            [CmdletBinding()]
            param (
                
            )
        }
        #endregion Functions

        # Create the window
        $window = [Window] @{
            Title = "Cowriter Setup"
            Width = 600
            Height = 400
            WindowStartupLocation = "CenterScreen"
            Topmost = $true
            FontSize = 16
        }

        # Grids for the main area + navigation buttons
        $grid = [Grid]::new()
        # Individual page titles
        $row1 = [RowDefinition] @{ Height = 40 }
        # Main content
        $row2 = [RowDefinition]::new()
        # Navigation buttons
        $row3 = [RowDefinition] @{ Height = 50 }
        [void] $grid.RowDefinitions.Add($row1)
        [void] $grid.RowDefinitions.Add($row2)
        [void] $grid.RowDefinitions.Add($row3)

        # Title bar
        # Displays the title for each individual page
        $titleBar = [TextBlock] @{
            FontSize = 20
            FontWeight = "Bold"
            Margin = '10,5,0,5'
        }
        [Grid]::SetRow($titleBar, 0)
        [void] $grid.Children.Add($titleBar)

        # Main content area
        # This will update as the user navigates through the wizard
        $pageContent = [ContentControl]::new()
        [Grid]::SetRow($pageContent, 1)
        [void] $grid.Children.Add($pageContent)

        # Pages
        # This is the structure of each page in the wizard
        $introduction = @{
            Title = 'Introduction'
            Content = [TextBlock] @{
                Text = "Welcome to the Cowriter Setup Wizard.`n`nThis wizard will guide you through the installation of Cowriter and its dependencies."
                TextWrapping = "Wrap"
                Margin = "10"
            }
        }

        $pages = @(
            $introduction
        )

        # Bottom navigation buttons
        $buttonPanel = [StackPanel] @{
            Orientation = "Horizontal"
            HorizontalAlignment = "Right"
            Margin = "0,10,10,10"
        }
        [void] [Grid]::SetRow($buttonPanel, 2)
        [void] $grid.Children.Add($buttonPanel)

        $backButton = [Button] @{
            Content = "Back"
            Width = 80
            Margin = "0,0,10,0"
        }
        [void] $buttonPanel.Children.Add($backButton)

        $nextButton = [Button] @{
            Content = "Next"
            Width = 80
            Margin = "0,0,10,0"
        }
        [void] $buttonPanel.Children.Add($nextButton)

        $cancelButton = [Button] @{
            Content = "Cancel"
            Width = 80
            Margin = "0,0,10,0"
        }
        [void] $cancelButton.Add_Click({ $window.Close() })
        [void] $buttonPanel.Children.Add($cancelButton)

        # Set the first page content to start
        $pageContent.Content = $pages[0].Content
        $window.Content = $grid
        return $window
    }
    #endregion Functions
    
    Add-Type -AssemblyName PresentationFramework
}
Process {
    $window = Build-Window
    $window.ShowDialog()
}
