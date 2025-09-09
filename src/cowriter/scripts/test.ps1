Add-Type -AssemblyName System.Net.Http

$client = [System.Net.Http.HttpClient]::new()
$request = [System.Net.Http.HttpRequestMessage]::new([System.Net.Http.HttpMethod]::Post, 'http://localhost:11434/api/pull')
$request.Content = [System.Net.Http.StringContent]::new('{"model":"llama2"}', [System.Text.Encoding]::UTF8, 'application/json')

$response = $client.SendAsync($request, [System.Net.Http.HttpCompletionOption]::ResponseHeadersRead).Result
$stream = $response.Content.ReadAsStreamAsync().Result
$reader = New-Object System.IO.StreamReader($stream)

while (-not $reader.EndOfStream) {
    $line = $reader.ReadLine()
    # Process each line (should be a JSON object with progress)
    Write-Host $line
    # Optionally, parse JSON and update your progress bar
}
