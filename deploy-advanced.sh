#!/bin/bash

# =============================================================================
# 🚀 SCRIPT DE DEPLOYMENT AVANZADO - FORMULARIO DEVOPS AZURE
# =============================================================================
# Autor: GitHub Copilot
# Fecha: 8 de noviembre de 2025
# Propósito: Deployment completo con compilación, validación y monitoreo
# Basado en: Análisis de deployments exitosos anteriores
# =============================================================================

set -e  # Exit on any error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Variables de configuración
PROJECT_NAME="formulario-devops-azure"
AZURE_APP_NAME="formulario-devops-s2uxxgzelbnnk"
AZURE_RESOURCE_GROUP="formulario-devops"
AZURE_LOCATION="southcentralus"
PACKAGE_NAME="formulario-devops-production.zip"
HEALTH_ENDPOINT="https://${AZURE_APP_NAME}.azurewebsites.net"
MAX_WAIT_TIME=300  # 5 minutos máximo para deployment
DEPLOYMENT_LOG="deployment-$(date +%Y%m%d_%H%M%S).log"

# Variables de estado
START_TIME=$(date +%s)
DEPLOYMENT_ID=""
BUILD_SUCCESS=false
DEPLOY_SUCCESS=false
VALIDATION_SUCCESS=false

# Banner inicial
echo -e "${PURPLE}"
echo "╔══════════════════════════════════════════════════════════════════════════════════╗"
echo "║                     🚀 DEPLOYMENT AVANZADO - DEVOPS AZURE                       ║"
echo "║                                                                                  ║"
echo "║  Este script garantiza un deployment completo con validación automática         ║"
echo "║  Incluye: Compilación → Build → Deploy → Validación → Monitoreo                 ║"
echo "╚══════════════════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo

# Función para logging
log() {
    local level=$1
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "${timestamp} [${level}] ${message}" | tee -a "$DEPLOYMENT_LOG"
}

# Función para mostrar progreso con spinner
show_spinner() {
    local pid=$1
    local message=$2
    local spin='-\|/'
    local i=0
    
    printf "${CYAN}%s ${NC}" "$message"
    while kill -0 $pid 2>/dev/null; do
        i=$(( (i+1) %4 ))
        printf "\r${CYAN}%s %s${NC}" "$message" "${spin:$i:1}"
        sleep 0.1
    done
    printf "\r${GREEN}%s ✓${NC}\n" "$message"
}

# Función para verificar prerequisitos
check_prerequisites() {
    log "INFO" "🔍 Verificando prerequisitos..."
    
    local missing_tools=()
    
    # Verificar herramientas necesarias
    command -v az >/dev/null 2>&1 || missing_tools+=(azure-cli)
    command -v python3 >/dev/null 2>&1 || missing_tools+=(python3)
    command -v zip >/dev/null 2>&1 || missing_tools+=(zip)
    command -v curl >/dev/null 2>&1 || missing_tools+=(curl)
    command -v jq >/dev/null 2>&1 || missing_tools+=(jq)
    
    if [ ${#missing_tools[@]} -ne 0 ]; then
        log "ERROR" "❌ Herramientas faltantes: ${missing_tools[*]}"
        log "INFO" "Instale las herramientas faltantes antes de continuar"
        exit 1
    fi
    
    # Verificar autenticación Azure
    if ! az account show >/dev/null 2>&1; then
        log "ERROR" "❌ No está autenticado en Azure. Ejecute: az login"
        exit 1
    fi
    
    # Verificar archivos esenciales
    local required_files=("app.py" "requirements.txt" "cuestionario_devops_azure.json" "templates/form.html")
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            log "ERROR" "❌ Archivo requerido no encontrado: $file"
            exit 1
        fi
    done
    
    log "SUCCESS" "✅ Todos los prerequisitos verificados correctamente"
}

# Función para compilar y validar aplicación
compile_and_validate() {
    log "INFO" "🔧 Iniciando compilación y validación..."
    
    # Validar sintaxis Python
    log "INFO" "📝 Validando sintaxis de Python..."
    if ! python3 -m py_compile app.py; then
        log "ERROR" "❌ Error de sintaxis en app.py"
        exit 1
    fi
    
    # Validar JSON del cuestionario
    log "INFO" "📋 Validando JSON del cuestionario..."
    if ! python3 -c "
import json
try:
    with open('cuestionario_devops_azure.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f'✓ JSON válido: {len(data.get(\"areas\", []))} áreas encontradas')
except Exception as e:
    print(f'❌ Error en JSON: {e}')
    exit(1)
"; then
        log "ERROR" "❌ Error validando JSON del cuestionario"
        exit 1
    fi
    
    # Validar templates HTML
    log "INFO" "🎨 Validando templates HTML..."
    if [[ ! -f "templates/form.html" ]]; then
        log "ERROR" "❌ Template form.html no encontrado"
        exit 1
    fi
    
    # Verificar que el logo ReadyMind esté presente
    if [[ ! -f "static/logo_readymind.webp" ]]; then
        log "WARNING" "⚠️  Logo ReadyMind no encontrado, pero continuando..."
    else
        log "SUCCESS" "✅ Logo ReadyMind encontrado"
    fi
    
    # Validar requirements.txt
    log "INFO" "📦 Validando requirements.txt..."
    if ! python3 -c "
import pkg_resources
try:
    with open('requirements.txt', 'r') as f:
        requirements = f.read().strip().split('\n')
    for req in requirements:
        if req and not req.startswith('#'):
            pkg_resources.Requirement.parse(req)
    print('✓ Requirements.txt válido')
except Exception as e:
    print(f'❌ Error en requirements.txt: {e}')
    exit(1)
"; then
        log "ERROR" "❌ Error validando requirements.txt"
        exit 1
    fi
    
    BUILD_SUCCESS=true
    log "SUCCESS" "✅ Compilación y validación completadas exitosamente"
}

# Función para crear package de deployment
create_deployment_package() {
    log "INFO" "📦 Creando package de deployment..."
    
    # Limpiar package anterior
    [[ -f "$PACKAGE_NAME" ]] && rm -f "$PACKAGE_NAME"
    
    # Crear directorio temporal para build
    BUILD_DIR=$(mktemp -d)
    trap "rm -rf $BUILD_DIR" EXIT
    
    # Copiar archivos esenciales
    local essential_files=(
        "app.py"
        "requirements.txt"
        "cuestionario_devops_azure.json"
        ".env.example"
        ".gitignore"
        "README.md"
    )
    
    for file in "${essential_files[@]}"; do
        if [[ -f "$file" ]]; then
            cp "$file" "$BUILD_DIR/"
            log "INFO" "  ✓ Copiado: $file"
        fi
    done
    
    # Copiar directorios
    if [[ -d "templates" ]]; then
        cp -r templates "$BUILD_DIR/"
        log "INFO" "  ✓ Copiado: templates/"
    fi
    
    if [[ -d "static" ]]; then
        cp -r static "$BUILD_DIR/"
        log "INFO" "  ✓ Copiado: static/"
    fi
    
    # Crear el ZIP desde el directorio temporal
    (cd "$BUILD_DIR" && zip -r "../$PACKAGE_NAME" .) >/dev/null 2>&1
    
    local package_size=$(ls -lh "$PACKAGE_NAME" | awk '{print $5}')
    log "SUCCESS" "✅ Package creado: $PACKAGE_NAME ($package_size)"
    
    # Mostrar contenido del package
    log "INFO" "📋 Contenido del package:"
    unzip -l "$PACKAGE_NAME" | tail -n +4 | head -n -2 | while read -r line; do
        log "INFO" "    $line"
    done
}

# Función para verificar conectividad con Azure
test_azure_connectivity() {
    log "INFO" "🌐 Verificando conectividad con Azure..."
    
    # Verificar resource group
    if ! az group show --name "$AZURE_RESOURCE_GROUP" >/dev/null 2>&1; then
        log "ERROR" "❌ Resource group '$AZURE_RESOURCE_GROUP' no encontrado"
        exit 1
    fi
    
    # Verificar app service
    if ! az webapp show --name "$AZURE_APP_NAME" --resource-group "$AZURE_RESOURCE_GROUP" >/dev/null 2>&1; then
        log "ERROR" "❌ App Service '$AZURE_APP_NAME' no encontrado"
        exit 1
    fi
    
    # Obtener información del app service
    local app_info=$(az webapp show --name "$AZURE_APP_NAME" --resource-group "$AZURE_RESOURCE_GROUP" --query "{state:state, location:location, sku:appServicePlanId}" -o json)
    local app_state=$(echo "$app_info" | jq -r '.state')
    local app_location=$(echo "$app_info" | jq -r '.location')
    
    log "INFO" "  🔍 App Service Estado: $app_state"
    log "INFO" "  🌍 Ubicación: $app_location"
    
    if [[ "$app_state" != "Running" ]]; then
        log "WARNING" "⚠️  App Service no está en estado 'Running': $app_state"
    fi
    
    log "SUCCESS" "✅ Conectividad con Azure verificada"
}

# Función para realizar deployment
deploy_to_azure() {
    log "INFO" "🚀 Iniciando deployment a Azure..."
    
    # Mostrar estado previo
    local current_deployment=$(az webapp deployment list --name "$AZURE_APP_NAME" --resource-group "$AZURE_RESOURCE_GROUP" --query "[0].{id:id, status:status, startTime:startTime}" -o json 2>/dev/null || echo '{"id":"none"}')
    local current_id=$(echo "$current_deployment" | jq -r '.id // "none"')
    
    log "INFO" "  📋 Deployment anterior: $current_id"
    
    # Realizar deployment usando ZIP deploy
    log "INFO" "  📤 Subiendo package..."
    local deploy_output
    deploy_output=$(az webapp deployment source config-zip \
        --name "$AZURE_APP_NAME" \
        --resource-group "$AZURE_RESOURCE_GROUP" \
        --src "$PACKAGE_NAME" \
        --query "{id:id, status:status, startTime:startTime}" \
        -o json 2>&1)
    
    if [[ $? -ne 0 ]]; then
        log "ERROR" "❌ Error durante deployment: $deploy_output"
        exit 1
    fi
    
    DEPLOYMENT_ID=$(echo "$deploy_output" | jq -r '.id // "unknown"')
    log "SUCCESS" "✅ Deployment iniciado - ID: $DEPLOYMENT_ID"
    
    # Esperar a que el deployment complete
    wait_for_deployment_completion
}

# Función para esperar completion del deployment
wait_for_deployment_completion() {
    log "INFO" "⏳ Esperando completion del deployment..."
    
    local wait_time=0
    local status="Unknown"
    
    while [[ $wait_time -lt $MAX_WAIT_TIME ]]; do
        # Obtener estado del deployment
        local deployment_info=$(az webapp deployment list \
            --name "$AZURE_APP_NAME" \
            --resource-group "$AZURE_RESOURCE_GROUP" \
            --query "[0].{status:status, endTime:endTime, statusText:statusText}" \
            -o json 2>/dev/null)
        
        status=$(echo "$deployment_info" | jq -r '.status // "Unknown"')
        local end_time=$(echo "$deployment_info" | jq -r '.endTime // null')
        
        case "$status" in
            "Success"|"4")
                log "SUCCESS" "✅ Deployment completado exitosamente"
                DEPLOY_SUCCESS=true
                return 0
                ;;
            "Failed"|"3")
                local status_text=$(echo "$deployment_info" | jq -r '.statusText // "Sin detalles"')
                log "ERROR" "❌ Deployment falló: $status_text"
                return 1
                ;;
            "Running"|"1")
                printf "\r${BLUE}⏳ Deployment en progreso... ${wait_time}s ${NC}"
                ;;
            *)
                printf "\r${YELLOW}⏳ Estado desconocido: $status... ${wait_time}s ${NC}"
                ;;
        esac
        
        sleep 5
        wait_time=$((wait_time + 5))
    done
    
    log "ERROR" "❌ Timeout esperando deployment después de ${MAX_WAIT_TIME}s"
    return 1
}

# Función para validar deployment
validate_deployment() {
    log "INFO" "🔍 Validando deployment..."
    
    # Esperar un momento para que el servicio se inicialice
    log "INFO" "  ⏳ Esperando inicialización del servicio..."
    sleep 15
    
    # Test 1: Health check endpoint
    log "INFO" "  🏥 Verificando health endpoint..."
    local health_response
    local health_status
    
    for attempt in {1..5}; do
        health_response=$(curl -s -w "HTTPSTATUS:%{http_code}" "$HEALTH_ENDPOINT" 2>/dev/null || echo "HTTPSTATUS:000")
        health_status=$(echo "$health_response" | grep -o "HTTPSTATUS:[0-9]*" | cut -d: -f2)
        
        if [[ "$health_status" == "200" ]]; then
            log "SUCCESS" "  ✅ Health check OK (intento $attempt)"
            break
        else
            log "WARNING" "  ⚠️  Health check falló - intento $attempt/5 (HTTP: $health_status)"
            if [[ $attempt -lt 5 ]]; then
                sleep 10
            fi
        fi
    done
    
    if [[ "$health_status" != "200" ]]; then
        log "ERROR" "❌ Health check falló después de 5 intentos"
        return 1
    fi
    
    # Test 2: Verificar contenido de la respuesta
    log "INFO" "  📋 Verificando contenido de respuesta..."
    local health_body=$(echo "$health_response" | sed 's/HTTPSTATUS:[0-9]*$//')
    
    if echo "$health_body" | jq . >/dev/null 2>&1; then
        local app_status=$(echo "$health_body" | jq -r '.status // "unknown"')
        local app_version=$(echo "$health_body" | jq -r '.version // "unknown"')
        
        log "INFO" "  📊 Estado de aplicación: $app_status"
        log "INFO" "  🏷️  Versión: $app_version"
        
        if [[ "$app_status" == "healthy" ]]; then
            log "SUCCESS" "  ✅ Aplicación reporta estado saludable"
        else
            log "WARNING" "  ⚠️  Aplicación reporta estado: $app_status"
        fi
    else
        log "WARNING" "  ⚠️  Respuesta no es JSON válido"
    fi
    
    # Test 3: Verificar formulario principal
    log "INFO" "  📝 Verificando formulario principal..."
    local form_response=$(curl -s -w "HTTPSTATUS:%{http_code}" "$HEALTH_ENDPOINT/" 2>/dev/null || echo "HTTPSTATUS:000")
    local form_status=$(echo "$form_response" | grep -o "HTTPSTATUS:[0-9]*" | cut -d: -f2)
    
    if [[ "$form_status" == "200" ]]; then
        log "SUCCESS" "  ✅ Formulario principal accesible"
        
        # Verificar que contiene elementos esperados
        local form_body=$(echo "$form_response" | sed 's/HTTPSTATUS:[0-9]*$//')
        
        if echo "$form_body" | grep -q "ReadyMind"; then
            log "SUCCESS" "  ✅ Logo ReadyMind detectado"
        else
            log "WARNING" "  ⚠️  Logo ReadyMind no detectado en el HTML"
        fi
        
        if echo "$form_body" | grep -q "Assessment DevOps"; then
            log "SUCCESS" "  ✅ Contenido del cuestionario detectado"
        else
            log "WARNING" "  ⚠️  Contenido del cuestionario no detectado"
        fi
        
    else
        log "ERROR" "❌ Formulario principal no accesible (HTTP: $form_status)"
        return 1
    fi
    
    # Test 4: Verificar recursos estáticos
    log "INFO" "  🎨 Verificando recursos estáticos..."
    
    local css_response=$(curl -s -w "HTTPSTATUS:%{http_code}" "$HEALTH_ENDPOINT/static/css/bundle.min.css" 2>/dev/null || echo "HTTPSTATUS:000")
    local css_status=$(echo "$css_response" | grep -o "HTTPSTATUS:[0-9]*" | cut -d: -f2)
    
    if [[ "$css_status" == "200" ]]; then
        log "SUCCESS" "  ✅ CSS cargando correctamente"
    else
        log "WARNING" "  ⚠️  CSS no accesible (HTTP: $css_status)"
    fi
    
    local logo_response=$(curl -s -w "HTTPSTATUS:%{http_code}" "$HEALTH_ENDPOINT/static/logo_readymind.webp" 2>/dev/null || echo "HTTPSTATUS:000")
    local logo_status=$(echo "$logo_response" | grep -o "HTTPSTATUS:[0-9]*" | cut -d: -f2)
    
    if [[ "$logo_status" == "200" ]]; then
        log "SUCCESS" "  ✅ Logo ReadyMind cargando correctamente"
    else
        log "WARNING" "  ⚠️  Logo ReadyMind no accesible (HTTP: $logo_status)"
    fi
    
    VALIDATION_SUCCESS=true
    log "SUCCESS" "✅ Validación de deployment completada"
    return 0
}

# Función para generar reporte final
generate_final_report() {
    local end_time=$(date +%s)
    local duration=$((end_time - START_TIME))
    
    echo -e "\n${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════════════════════════╗"
    echo "║                           📊 REPORTE FINAL DE DEPLOYMENT                         ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    echo -e "${CYAN}⏱️  TIEMPO TOTAL DE DEPLOYMENT: ${GREEN}${duration}s${NC}"
    echo
    
    echo -e "${CYAN}📋 RESUMEN DE ETAPAS:${NC}"
    echo -e "  • Prerequisitos: ${GREEN}✅ Completado${NC}"
    
    if [[ "$BUILD_SUCCESS" == "true" ]]; then
        echo -e "  • Compilación: ${GREEN}✅ Exitoso${NC}"
    else
        echo -e "  • Compilación: ${RED}❌ Falló${NC}"
    fi
    
    if [[ "$DEPLOY_SUCCESS" == "true" ]]; then
        echo -e "  • Deployment: ${GREEN}✅ Exitoso${NC}"
    else
        echo -e "  • Deployment: ${RED}❌ Falló${NC}"
    fi
    
    if [[ "$VALIDATION_SUCCESS" == "true" ]]; then
        echo -e "  • Validación: ${GREEN}✅ Exitoso${NC}"
    else
        echo -e "  • Validación: ${RED}❌ Falló${NC}"
    fi
    
    echo
    echo -e "${CYAN}🔗 ENLACES ÚTILES:${NC}"
    echo -e "  • Aplicación: ${GREEN}$HEALTH_ENDPOINT${NC}"
    echo -e "  • Health Check: ${GREEN}$HEALTH_ENDPOINT/health${NC}"
    echo -e "  • Azure Portal: ${BLUE}https://portal.azure.com/#@/resource/subscriptions/$(az account show --query id -o tsv)/resourceGroups/$AZURE_RESOURCE_GROUP/providers/Microsoft.Web/sites/$AZURE_APP_NAME${NC}"
    
    echo
    echo -e "${CYAN}📄 LOG DE DEPLOYMENT: ${GREEN}$DEPLOYMENT_LOG${NC}"
    
    if [[ "$BUILD_SUCCESS" == "true" && "$DEPLOY_SUCCESS" == "true" && "$VALIDATION_SUCCESS" == "true" ]]; then
        echo
        echo -e "${GREEN}🎉 DEPLOYMENT COMPLETADO EXITOSAMENTE${NC}"
        return 0
    else
        echo
        echo -e "${RED}💥 DEPLOYMENT FALLÓ - Revisar logs para detalles${NC}"
        return 1
    fi
}

# Función principal
main() {
    log "INFO" "🚀 Iniciando deployment avanzado..."
    
    check_prerequisites
    compile_and_validate
    create_deployment_package
    test_azure_connectivity
    deploy_to_azure
    validate_deployment
    
    generate_final_report
}

# Manejo de señales para cleanup
cleanup() {
    log "INFO" "🧹 Ejecutando cleanup..."
    [[ -f "$PACKAGE_NAME" ]] && rm -f "$PACKAGE_NAME"
    exit 1
}

trap cleanup SIGINT SIGTERM

# Ejecutar función principal
main "$@"