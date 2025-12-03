# test_api.ps1
$baseUrl = "http://localhost:8000"

Write-Host "🚀 PRUEBA DE LA API DE MENSAJES" -ForegroundColor Cyan
Write-Host "="*60

# Función para hacer peticiones
function Invoke-Test {
    param($Method, $Endpoint, $Body, $Description)
    
    Write-Host "`n $Description" -ForegroundColor Yellow
    Write-Host "   $Method $Endpoint"
    
    $headers = @{"Content-Type" = "application/json"}
    
    try {
        if ($Body) {
            $response = Invoke-RestMethod -Uri "$baseUrl$Endpoint" -Method $Method -Headers $headers -Body $Body
        } else {
            $response = Invoke-RestMethod -Uri "$baseUrl$Endpoint" -Method $Method -Headers $headers
        }
        
        Write-Host "    Éxito" -ForegroundColor Green
        $response | ConvertTo-Json -Depth 4 | Out-Host
        return $true
    }
    catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        Write-Host "    Error $statusCode" -ForegroundColor Red
        return $false
    }
}

# Pruebas
Invoke-Test -Method GET -Endpoint "/" -Description "Página principal"

Invoke-Test -Method GET -Endpoint "/health" -Description "Health check"

$timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

$message1 = @{
    message_id = "msg-ps-test-1"
    session_id = "session-ps-001"
    content = "Mensaje de prueba desde PowerShell"
    timestamp = $timestamp
    sender = "user"
} | ConvertTo-Json -Compress

Invoke-Test -Method POST -Endpoint "/api/messages/" -Body $message1 -Description "Crear mensaje normal"

$message2 = @{
    message_id = "msg-ps-test-2"
    session_id = "session-ps-001"
    content = "Este mensaje tiene badword1 y inappropriate palabras"
    timestamp = $timestamp
    sender = "system"
} | ConvertTo-Json -Compress

Invoke-Test -Method POST -Endpoint "/api/messages/" -Body $message2 -Description "Crear mensaje con filtrado"

Invoke-Test -Method GET -Endpoint "/api/messages/session-ps-001" -Description "Obtener todos los mensajes"

Invoke-Test -Method GET -Endpoint "/api/messages/session-ps-001?sender=system&limit=1" -Description "Mensajes filtrados por system"

Write-Host "`n Documentación disponible:" -ForegroundColor Cyan
Write-Host "   Swagger UI: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "   ReDoc: http://localhost:8000/redoc" -ForegroundColor Yellow
Write-Host "`n ¡Prueba completada!" -ForegroundColor Green
