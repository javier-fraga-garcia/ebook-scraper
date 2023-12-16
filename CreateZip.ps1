$compress = @{
    Path = '.\package\*', '.\lambda_function.py'
    CompressionLevel = 'Fastest'
    DestinationPath = '.\lambda_function.zip'
}
Compress-Archive @compress