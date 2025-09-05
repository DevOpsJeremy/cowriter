function Start-Cowriter {
    [Alias('Cowriter')]
    [CmdletBinding()]
    param (
        [string] $Xaml = "$PSScriptRoot/files/xaml/cowriter.xaml"
    )
    Add-Type -AssemblyName PresentationFramework

    # Load XAML
    [xml]$xaml = Get-Content -Raw -Path $Xaml
    $reader = (New-Object System.Xml.XmlNodeReader $xaml)
    $window = [Windows.Markup.XamlReader]::Load($reader)
    $mainText = $window.FindName("MainText")
    $lineNumbers = $window.FindName("LineNumbers")

    # Logic for the text lines
    $lines_loaded = {
        $visibleLines = [Math]::Ceiling($mainText.ViewportHeight / $mainText.FontSize)
        $totalLines = [Math]::Max($mainText.LineCount, $visibleLines)
        $nums = ""
        for ($i=1; $i -le $totalLines; $i++) { $nums += "$i`n" }
        $lineNumbers.Text = $nums
    }
    $lines_textChanged = {
        $visibleLines = [Math]::Ceiling($mainText.ViewportHeight / $mainText.FontSize)
        $totalLines = [Math]::Max($mainText.LineCount, $visibleLines)
        $textLines = $mainText.Text -split "`n"
        $nums = ""
        for ($i=1; $i -le $totalLines; $i++) { $nums += "$i`n" }
        $lineNumbers.Text = $nums
    }
    $mainText.Add_Loaded($lines_loaded)
    $mainText.Add_TextChanged($lines_textChanged)

    # Logic for the formatting buttons
    $boldButton = $window.FindName("BoldButton")
    $italicButton = $window.FindName("ItalicButton")
    $underlineButton = $window.FindName("UnderlineButton")
    $bulletButton = $window.FindName("BulletButton")
    $numberButton = $window.FindName("NumberButton")

    # Bold
    $boldButton.Add_Click({
        $mainText.Selection.ApplyPropertyValue([System.Windows.Documents.Inline]::FontWeightProperty, [System.Windows.FontWeights]::Bold)
    })
    # Italic
    $italicButton.Add_Click({
        $mainText.Selection.ApplyPropertyValue([System.Windows.Documents.Inline]::FontStyleProperty, [System.Windows.FontStyles]::Italic)
    })

    # Underline
    $underlineButton.Add_Click({
        $mainText.Selection.ApplyPropertyValue([System.Windows.Documents.Inline]::TextDecorationsProperty, [System.Windows.TextDecorations]::Underline)
    })

    <#
    # Bulleted List
    $bulletButton.Add_Click({
        $para = $mainText.Selection.Start.Paragraph
        if ($para -and -not $para.List) {
            $list = New-Object System.Windows.Documents.List
            $list.MarkerStyle = [System.Windows.TextMarkerStyle]::Disc
            $list.ListItems.Add((New-Object System.Windows.Documents.ListItem($para)))
            $mainText.Document.Blocks.InsertBefore($para, $list)
            $mainText.Document.Blocks.Remove($para)
        }
    })

    # Numbered List
    $numberButton.Add_Click({
        $para = $mainText.Selection.Start.Paragraph
        if ($para -and -not $para.List) {
            $list = New-Object System.Windows.Documents.List
            $list.MarkerStyle = [System.Windows.TextMarkerStyle]::Decimal
            $list.ListItems.Add((New-Object System.Windows.Documents.ListItem($para)))
            $mainText.Document.Blocks.InsertBefore($para, $list)
            $mainText.Document.Blocks.Remove($para)
        }
    })
    #>

    $chatHistory = $window.FindName('ChatHistory')
    function Add-ChatBubble {
        [CmdletBinding()]
        param (
            [string] $Message,
            [System.Windows.Media.SolidColorBrush] $Background = [System.Windows.Media.Brushes]::LightBlue,
            [System.Windows.Controls.StackPanel] $ChatPanel,
            [int] $CornerRadius = 10,
            [int] $Padding = 8,
            [int] $Margin = 4,
            [System.Windows.HorizontalAlignment] $HorizontalAlignment = 'Right',
            [int] $MaxWidth = 200,
            [System.Windows.TextWrapping] $TextWrapping = 'Wrap'
        )
        $ChatPanel.AddChild(
            [System.Windows.Controls.Border] @{
                CornerRadius = $CornerRadius
                Padding = $Padding
                Margin = $Margin
                HorizontalAlignment = $HorizontalAlignment
                Background = $Background
                MaxWidth = $MaxWidth
                Child = [System.Windows.Controls.TextBlock] @{
                    Text = $Message
                    TextWrapping = $TextWrapping
                }
            }
        )
    }

    # Show window
    $window.ShowDialog()
}
