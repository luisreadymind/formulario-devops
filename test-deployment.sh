#!/bin/bash

# Script de prueba para validar el formulario completo
APP_URL="https://formulario-devops-s2uxxgzelbnnk.azurewebsites.net"

echo "🧪 Iniciando prueba completa del formulario..."

# Test 1: Health check
echo "1️⃣  Probando health check..."
health_response=$(curl -s "${APP_URL}/health")
if echo "$health_response" | grep -q "healthy"; then
    echo "   ✅ Health check exitoso"
else
    echo "   ❌ Health check falló: $health_response"
    exit 1
fi

# Test 2: Página principal
echo "2️⃣  Probando página principal..."
main_page_response=$(curl -s -I "$APP_URL" | head -1)
if echo "$main_page_response" | grep -q "200"; then
    echo "   ✅ Página principal carga correctamente"
else
    echo "   ❌ Página principal falló: $main_page_response"
    exit 1
fi

# Test 3: Envío de formulario
echo "3️⃣  Probando envío de formulario..."
form_response=$(curl -s -X POST "${APP_URL}/submit" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "client_name=Test+Usuario&client_email=test@prueba.com&client_company=Empresa+Test&A1=A1O1&A2=A2O2&B1=B1O1")

if echo "$form_response" | grep -q '"success": true'; then
    echo "   ✅ Formulario procesado exitosamente"
    echo "   📊 Respuesta del servidor:"
    echo "$form_response" | jq . 2>/dev/null || echo "$form_response"
else
    echo "   ❌ Error en el formulario: $form_response"
fi

echo ""
echo "🏆 Prueba completa finalizada"
echo "🌐 Aplicación disponible en: $APP_URL"