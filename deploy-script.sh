#!/bin/bash
# =============================================================================
# SCRIPT DE DESPLIEGUE PARA FORMULARIO DEVOPS AZURE
# =============================================================================
# 
# Este script automatiza el proceso completo de despliegue de la aplicación
# Flask del formulario DevOps en Azure App Service.
#
# Autor: Luis Alberto Arenas
# Fecha: 2025-11-08
# Versión: 1.0
#
# =============================================================================

# Variables de configuración
RESOURCE_GROUP="FormularioDevOPs"
APP_NAME="formulario-devops-s2uxxgzelbnnk"
PROJECT_DIR="/mnt/c/Users/Luis Alberto Arenas/Documents/Python/formulario-devops-azure"
PACKAGE_NAME="formulario-devops-production.zip"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para logging
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Función para verificar prerequisitos
check_prerequisites() {
    log_info "Verificando prerequisitos..."
    
    # Verificar Azure CLI
    if ! command -v az &> /dev/null; then
        log_error "Azure CLI no está instalado"
        exit 1
    fi
    
    # Verificar login en Azure
    if ! az account show &> /dev/null; then
        log_error "No está logueado en Azure. Ejecute: az login"
        exit 1
    fi
    
    # Verificar zip
    if ! command -v zip &> /dev/null; then
        log_error "zip no está instalado"
        exit 1
    fi
    
    log_success "Todos los prerequisitos están disponibles"
}

# Función para limpiar archivos temporales
cleanup_project() {
    log_info "Realizando limpieza del proyecto..."
    
    cd "$PROJECT_DIR" || exit 1
    
    # Eliminar archivos temporales y de prueba
    rm -rf __pycache__ test_env *.pyc
    rm -f test_* analyze_* *.pdf
    rm -f deployment-*.zip formulario-devops-*.zip
    
    log_success "Limpieza completada"
}

# Función para validar archivos esenciales
validate_files() {
    log_info "Validando archivos esenciales..."
    
    local required_files=(
        "app.py"
        "requirements.txt"
        "cuestionario_devops_azure.json"
        "templates/form.html"
        "static/css/bootstrap-grid.min.css"
        "static/css/bundle.min.css"
    )
    
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            log_error "Archivo requerido no encontrado: $file"
            exit 1
        fi
    done
    
    log_success "Todos los archivos esenciales están presentes"
}

# Función para crear el paquete de despliegue
create_package() {
    log_info "Creando paquete de despliegue..."
    
    # Eliminar paquete anterior si existe
    rm -f "$PACKAGE_NAME"
    
    # Crear nuevo paquete
    zip -r "$PACKAGE_NAME" \
        app.py \
        requirements.txt \
        cuestionario_devops_azure.json \
        templates/ \
        static/ \
        .env.example \
        .gitignore \
        README.md \
        -x "__pycache__/*" "*.pyc" "test_*" "analyze_*" "*.pdf" "deployment-*.zip"
    
    if [ $? -eq 0 ]; then
        local size=$(stat -c%s "$PACKAGE_NAME" 2>/dev/null || stat -f%z "$PACKAGE_NAME" 2>/dev/null)
        log_success "Paquete creado: $PACKAGE_NAME ($(echo $size | awk '{print int($1/1024)}') KB)"
    else
        log_error "Error creando el paquete"
        exit 1
    fi
}

# Función para configurar Azure App Service
configure_app_service() {
    log_info "Configurando Azure App Service..."
    
    # Configurar comando de inicio correcto
    az webapp config set \
        --resource-group "$RESOURCE_GROUP" \
        --name "$APP_NAME" \
        --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 app:app"
    
    if [ $? -eq 0 ]; then
        log_success "Configuración de App Service actualizada"
    else
        log_error "Error configurando App Service"
        exit 1
    fi
}

# Función para desplegar
deploy_app() {
    log_info "Desplegando aplicación en Azure..."
    
    az webapp deploy \
        --resource-group "$RESOURCE_GROUP" \
        --name "$APP_NAME" \
        --src-path "$PACKAGE_NAME" \
        --type zip
    
    if [ $? -eq 0 ]; then
        log_success "Despliegue completado"
    else
        log_error "Error en el despliegue"
        exit 1
    fi
}

# Función para reiniciar la aplicación
restart_app() {
    log_info "Reiniciando aplicación..."
    
    az webapp restart \
        --resource-group "$RESOURCE_GROUP" \
        --name "$APP_NAME"
    
    if [ $? -eq 0 ]; then
        log_success "Aplicación reiniciada"
    else
        log_warning "Error reiniciando aplicación (puede que funcione igualmente)"
    fi
}

# Función para validar el despliegue
validate_deployment() {
    log_info "Validando despliegue..."
    
    local app_url="https://${APP_NAME}.azurewebsites.net"
    
    # Esperar un poco para que la aplicación inicie
    log_info "Esperando que la aplicación inicie (30 segundos)..."
    sleep 30
    
    # Probar health check
    local health_response=$(curl -s "${app_url}/health" 2>/dev/null)
    
    if echo "$health_response" | grep -q "healthy"; then
        log_success "Health check exitoso"
        log_success "Aplicación disponible en: $app_url"
        
        # Probar página principal
        local main_response=$(curl -s -I "$app_url" 2>/dev/null | head -1)
        if echo "$main_response" | grep -q "200"; then
            log_success "Página principal responde correctamente"
        else
            log_warning "Página principal puede tener problemas: $main_response"
        fi
    else
        log_error "Health check falló: $health_response"
        log_error "Revisar logs: az webapp log tail --resource-group $RESOURCE_GROUP --name $APP_NAME"
        exit 1
    fi
}

# Función para mostrar información final
show_final_info() {
    log_info "=== INFORMACIÓN DEL DESPLIEGUE ==="
    echo ""
    echo -e "🌐 ${GREEN}URL de la aplicación:${NC} https://${APP_NAME}.azurewebsites.net"
    echo -e "❤️  ${GREEN}Health check:${NC} https://${APP_NAME}.azurewebsites.net/health"
    echo -e "📊 ${GREEN}Resource Group:${NC} $RESOURCE_GROUP"
    echo -e "🚀 ${GREEN}App Service:${NC} $APP_NAME"
    echo ""
    echo -e "📋 ${BLUE}Comandos útiles:${NC}"
    echo "   • Ver logs: az webapp log tail --resource-group $RESOURCE_GROUP --name $APP_NAME"
    echo "   • Reiniciar: az webapp restart --resource-group $RESOURCE_GROUP --name $APP_NAME"
    echo "   • Estado: az webapp show --resource-group $RESOURCE_GROUP --name $APP_NAME --query state"
    echo ""
    log_success "¡Despliegue completado exitosamente!"
}

# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================
main() {
    log_info "=== INICIANDO DESPLIEGUE DEL FORMULARIO DEVOPS ==="
    echo ""
    
    # Ejecutar pasos del despliegue
    check_prerequisites
    cd "$PROJECT_DIR" || exit 1
    cleanup_project
    validate_files
    create_package
    configure_app_service
    deploy_app
    restart_app
    validate_deployment
    show_final_info
}

# Ejecutar función principal
main "$@"

# =============================================================================
# NOTAS DE USO:
# =============================================================================
# 
# Para ejecutar este script:
#   chmod +x deploy-script.sh
#   ./deploy-script.sh
#
# Para debugging, agregar set -x al inicio del script
#
# =============================================================================