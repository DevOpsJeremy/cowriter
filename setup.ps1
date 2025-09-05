#requires -Version 5.1
#Requires -Assembly PresentationFramework
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
        param (
            [int] $MinFontSize = 8,
            [int] $MaxFontSize = 30
        )

        #region Functions
        function Set-PageContent {
            [CmdletBinding()]
            param (
                [Parameter(Mandatory, Position=0)]
                [int] $Page,
                [Parameter(Mandatory)]
                [array] $Pages,
                [Parameter(Mandatory)]
                [PSObject] $TitleControl,
                [Parameter(Mandatory)]
                [PSObject] $ContentControl
            )
            $pageHash = $Pages[$Page]
            $TitleControl.Text = $pageHash['Title']
            $ContentControl.Content = $pageHash['Content']
        }
        $script:setPageContent = {
            param (
                [int] $Page
            )
            $pageHash = $script:pages[$Page]
            $script:titleBar.Text = $pageHash['Title']
            $script:pageContent.Content = $pageHash['Content']
        }
        function Set-Page {
            [CmdletBinding(DefaultParameterSetName='Next')]
            param (
                [Parameter(Mandatory)]
                $PagesControl,
                [Parameter(Mandatory, ParameterSetName='Next')]
                [switch] $Next,
                [Parameter(Mandatory, ParameterSetName='Previous')]
                [switch] $Previous
            )
            $currentPage = $PagesControl.Tag['Page']
            $minimum = 0
            $maximum = $PagesControl.Tag['Pages'].Count - 1
            if ($Next) {
                $newPage = $currentPage + 1
                if ($newPage -gt $maximum) {
                    return
                }
            }
            if ($Previous) {
                $newPage = $currentPage - 1
                if ($newPage -lt $minimum) {
                    return
                }
            }
            Set-PageContent -Page $newPage
            $PagesControl.Tag['Page'] = $newPage
        }
        $script:setPage = {
            param (
                [switch] $Next,
                [switch] $Previous
            )
            $currentPage = $script:content.Tag['Page']
            $minimum = 0
            $maximum = $script:content.Children.Count - 1
            if ($Next) {
                $newPage = $currentPage + 1
                if ($newPage -gt $maximum) {
                    return
                }
            }
            if ($Previous) {
                $newPage = $currentPage - 1
                if ($newPage -lt $minimum) {
                    return
                }
            }
            . $script:setPageContent -Page $newPage
            $script:content.Tag['Page'] = $newPage
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
            Tag = @{
                MinFontSize = $MinFontSize
                MaxFontSize = $MaxFontSize
            }
        }

        # Grids for the main area + navigation buttons
        $grid = [Grid]::new()
        # Page
        $row1 = [RowDefinition]::new()
        # Navigation buttons
        $row2 = [RowDefinition] @{ Height = 50 }
        [void] $grid.RowDefinitions.Add($row1)
        [void] $grid.RowDefinitions.Add($row2)

        $script:content = [StackPanel] @{
            Margin = "5"
            Orientation = "Vertical"
            Tag = @{
                Page = 0
            }
        }
        [Grid]::SetRow($content, 0)
        [void] $grid.Children.Add($content)

        # Title bar
        # Displays the title for each individual page
        $script:titleBar = [TextBlock] @{
            FontSize = 20
            FontWeight = "Bold"
            Margin = '10,5,0,5'
            Height = 40
        }
        [void] $content.Children.Add($titleBar)

        # Main content area
        # This will update as the user navigates through the wizard
        $script:pageContent = [ContentControl]::new()
        [void] $content.Children.Add($pageContent)

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
        $secondPage = @{
            Title = 'Second page'
            Content = [TextBlock] @{
                Text = "This is the second page."
                TextWrapping = "Wrap"
                Margin = "10"
            }
        }

        $script:pages = @(
            $introduction,
            $secondPage
        )

        # Bottom navigation buttons
        $navGrid = [Grid]::new()
        $navCol1 = [ColumnDefinition]::new()
        $navCol2 = [ColumnDefinition]::new()
        [void] $navGrid.ColumnDefinitions.Add($navCol1)
        [void] $navGrid.ColumnDefinitions.Add($navCol2)
        [void] [Grid]::SetRow($navGrid, 1)
        [void] $grid.Children.Add($navGrid)

        # Zoom panel
        $zoomPanel = [StackPanel] @{
            Orientation = "Horizontal"
            HorizontalAlignment = "Left"
            Margin = "10,10,0,10"
        }
        [void] [Grid]::SetColumn($zoomPanel, 0)
        [void] $navGrid.Children.Add($zoomPanel)
        $zoomOutButton = [Button] @{
            Content = "-"
            Width = 30
            Margin = "10,0,0,0"
        }
        $zoomOutButton.Add_Click({
            if ($window.FontSize -gt $window.Tag['MinFontSize']) {
                $window.FontSize -= 2
            }
        })
        [void] $zoomPanel.Children.Add($zoomOutButton)

        $zoomInButton = [Button] @{
            Content = "+"
            Width = 30
            Margin = "5,0,0,0"
        }
        $zoomInButton.Add_Click({
            if ($window.FontSize -lt $window.Tag['MaxFontSize']) {
                $window.FontSize += 2
            }
        })
        [void] $zoomPanel.Children.Add($zoomInButton)

        # Button panel (back, next, cancel)
        $buttonPanel = [StackPanel] @{
            Orientation = "Horizontal"
            HorizontalAlignment = "Right"
            Margin = "0,10,10,10"
        }
        [void] [Grid]::SetColumn($buttonPanel, 1)
        [void] $navGrid.Children.Add($buttonPanel)

        $backButton = [Button] @{
            Content = "Back"
            Width = 80
            Margin = "0,0,10,0"
        }
        $backButton.Add_Click({ . $script:setPage -Previous })
        [void] $buttonPanel.Children.Add($backButton)

        $nextButton = [Button] @{
            Content = "Next"
            Width = 80
            Margin = "0,0,10,0"
        }
        $nextButton.Add_Click({ . $script:setPage -Next })
        [void] $buttonPanel.Children.Add($nextButton)

        $cancelButton = [Button] @{
            Content = "Cancel"
            Width = 80
            Margin = "0,0,10,0"
        }
        [void] $cancelButton.Add_Click({ $window.Close() })
        [void] $buttonPanel.Children.Add($cancelButton)

        # Set the first page content to start
        . $setPageContent -Page 0
        $window.Content = $grid
        return $window
    }
    #endregion Functions
    
}
Process {
    $window = Build-Window
    $window.ShowDialog()
}
