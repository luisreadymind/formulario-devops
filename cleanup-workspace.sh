#!/bin/bash

# =============================================================================
# 🧹 SCRIPT DE LIMPIEZA DEL WORKSPACE - FORMULARIO DEVOPS AZURE
# =============================================================================
# Autor: GitHub Copilot
# Fecha: 8 de noviembre de 2025
# Propósito: Eliminar archivos innecesarios y generar reporte de limpieza
# =============================================================================

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Variables globales
TOTAL_FILES_DELETED=0
TOTAL_SIZE_FREED=0
START_TIME=$(date +%s)

# Patrones a excluir (no eliminar)
EXCLUDE_PATTERNS=(
    "cleanup-workspace.sh"
    "cuestionario_devops_azure.json"
    "deploy-script.sh"
    "git-push.sh"
    "InvocaAssesmentDevOps.py"
)

# Comprueba si un archivo/directorio debe excluirse de la limpieza
is_excluded() {
    local target="$1"
    local base
    base=$(basename "$target")
    for p in "${EXCLUDE_PATTERNS[@]}"; do
        case "$base" in
            $p) return 0 ;;
        esac
    done
    return 1
}

# Banner inicial
echo -e "${PURPLE}"
echo "╔══════════════════════════════════════════════════════════════════════════════════╗"
echo "║                     🧹 LIMPIEZA DEL WORKSPACE DEVOPS AZURE                      ║"
echo "║                                                                                  ║"
echo "║  Este script eliminará archivos innecesarios manteniendo solo lo esencial       ║"
echo "║  para el funcionamiento de la aplicación en producción.                         ║"
echo "╚══════════════════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo

# Función para mostrar progreso
show_progress() {
    local step=$1
    local total=8
    local percent=$((step * 100 / total))
    local filled=$((step * 40 / total))
    local empty=$((40 - filled))
    
    printf "\r${BLUE}Progreso: [${GREEN}"
    printf "%*s" $filled | tr ' ' '█'
    printf "${BLUE}"
    printf "%*s" $empty | tr ' ' '░'
    printf "] %d%% (%d/%d)${NC}" $percent $step $total
}

# Función para calcular tamaño de archivo
get_file_size() {
    if [[ -f "$1" ]]; then
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            stat -f%z "$1" 2>/dev/null || stat -c%s "$1" 2>/dev/null || echo 0
        else
            powershell -command "(Get-Item '$1').Length" 2>/dev/null || echo 0
        fi
    else
        echo 0
    fi
}

# Función para eliminar archivo con reporte
delete_file() {
    local file=$1
    local reason=$2
    
    if is_excluded "$file"; then
        echo -e "  ${YELLOW}!${NC} Omitido (excluido): ${YELLOW}$(basename \"$file\")${NC} - $reason"
        return 0
    fi

    if [[ -f "$file" ]]; then
        local size=$(get_file_size "$file")
        rm -f "$file"
        if [[ $? -eq 0 ]]; then
            TOTAL_FILES_DELETED=$((TOTAL_FILES_DELETED + 1))
            TOTAL_SIZE_FREED=$((TOTAL_SIZE_FREED + size))
            echo -e "  ${GREEN}✓${NC} Eliminado: ${YELLOW}$(basename "$file")${NC} ($(numfmt --to=iec $size)) - $reason"
        else
            echo -e "  ${RED}✗${NC} Error eliminando: $file"
        fi
    fi
}

# Función para eliminar archivos por patrón
delete_pattern() {
    local pattern=$1
    local reason=$2
    
    for file in $pattern; do
        if is_excluded "$file"; then
            echo -e "  ${YELLOW}!${NC} Omitido (excluido): ${YELLOW}$(basename \"$file\")${NC} - $reason"
        elif [[ -f "$file" ]]; then
            delete_file "$file" "$reason"
        fi
    done
}

echo -e "${CYAN}🔍 Analizando estructura del proyecto...${NC}"
echo

# PASO 1: Eliminar archivos de screenshots y capturas
show_progress 1
echo -e "\n${CYAN}📸 PASO 1: Eliminando capturas de pantalla y imágenes de testing...${NC}"
delete_pattern "*.png" "captura de pantalla de testing"
delete_pattern "*.jpg" "imagen no necesaria para producción"
delete_pattern "*.jpeg" "imagen no necesaria para producción"
delete_pattern "*.gif" "imagen no necesaria para producción"

# PASO 2: Eliminar archivos de respaldo y versiones anteriores
show_progress 2
echo -e "\n${CYAN}💾 PASO 2: Eliminando archivos de respaldo y versiones anteriores...${NC}"
delete_file "cuestionario_devops_azure_backup.json" "archivo de respaldo"
delete_file "cuestionario_devops_azure_corregido.json" "versión anterior del cuestionario"
delete_file "complete_form_structure.json" "archivo de análisis temporal"

# PASO 3: Eliminar scripts de testing y desarrollo
show_progress 3
echo -e "\n${CYAN}🧪 PASO 3: Eliminando scripts de testing y desarrollo...${NC}"
delete_file "test-deployment.sh" "script de testing"
delete_file "setup-testing.sh" "script de configuración de testing"
delete_file "setup-chrome-testing.sh" "script específico de Chrome testing"
delete_file "test-api.sh" "script de testing API"

# PASO 4: Eliminar scripts de Python de desarrollo
show_progress 4
echo -e "\n${CYAN}🐍 PASO 4: Eliminando scripts de Python temporales...${NC}"
delete_file "corregir_inconsistencias.py" "script de corrección temporal"
delete_file "tropicalizar_cuestionario.py" "script de tropicalización temporal"

# PASO 5: Eliminar archivos de documentación temporal
show_progress 5
echo -e "\n${CYAN}📄 PASO 5: Eliminando documentación temporal...${NC}"
delete_file "CORRECCIONES-INCONSISTENCIAS.md" "documentación temporal"
delete_file "LIMPIEZA-EXITOSA.md" "documentación temporal"
delete_file "PUSH-SSH-EXITOSO.md" "documentación temporal"
delete_file "DEPLOYMENT-FINAL-EXITOSO.md" "documentación temporal"

# PASO 6: Eliminar archivos ZIP de deployment
show_progress 6
echo -e "\n${CYAN}📦 PASO 6: Eliminando archivos comprimidos temporales...${NC}"
delete_pattern "*.zip" "archivo comprimido temporal"
delete_pattern "*.tar.gz" "archivo comprimido temporal"
delete_pattern "*.tar" "archivo comprimido temporal"

# PASO 7: Eliminar archivos de logs y temporales
show_progress 7
echo -e "\n${CYAN}📋 PASO 7: Eliminando logs y archivos temporales...${NC}"
delete_pattern "*.log" "archivo de log"
delete_pattern "*.tmp" "archivo temporal"
delete_pattern "*.temp" "archivo temporal"
delete_pattern ".DS_Store" "archivo del sistema macOS"
delete_pattern "Thumbs.db" "archivo del sistema Windows"

# PASO 8: Eliminar directorios temporales vacíos
show_progress 8
echo -e "\n${CYAN}📁 PASO 8: Verificando directorios vacíos...${NC}"

# Función para verificar si un directorio está vacío
check_empty_dirs() {
    for dir in */; do
        if [[ -d "$dir" ]]; then
            if [[ -z "$(ls -A "$dir" 2>/dev/null)" ]]; then
                echo -e "  ${GREEN}✓${NC} Directorio vacío encontrado: ${YELLOW}$dir${NC}"
                rmdir "$dir" 2>/dev/null && echo -e "    ${GREEN}Eliminado${NC}" || echo -e "    ${RED}Error eliminando${NC}"
            fi
        fi
    done
}

check_empty_dirs

echo -e "\n${GREEN}✅ Limpieza completada!${NC}"
echo

# REPORTE FINAL
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo -e "${PURPLE}"
echo "╔══════════════════════════════════════════════════════════════════════════════════╗"
echo "║                           📊 REPORTE DE LIMPIEZA FINAL                           ║"
echo "╚══════════════════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${CYAN}📈 ESTADÍSTICAS DE LIMPIEZA:${NC}"
echo -e "  • Archivos eliminados: ${GREEN}$TOTAL_FILES_DELETED${NC}"
echo -e "  • Espacio liberado: ${GREEN}$(numfmt --to=iec $TOTAL_SIZE_FREED)${NC}"
echo -e "  • Tiempo de ejecución: ${GREEN}${DURATION}s${NC}"
echo

echo -e "${CYAN}📂 ARCHIVOS CONSERVADOS (ESENCIALES):${NC}"
echo -e "  ${GREEN}✓${NC} app.py - Aplicación Flask principal"
echo -e "  ${GREEN}✓${NC} cuestionario_devops_azure.json - Datos del cuestionario"
echo -e "  ${GREEN}✓${NC} requirements.txt - Dependencias Python"
echo -e "  ${GREEN}✓${NC} deploy-script.sh - Script de deployment a Azure"
echo -e "  ${GREEN}✓${NC} git-push.sh - Script de push a GitHub"
echo -e "  ${GREEN}✓${NC} upload-to-github.sh - Script de upload"
echo -e "  ${GREEN}✓${NC} templates/ - Templates HTML de la aplicación"
echo -e "  ${GREEN}✓${NC} static/ - Recursos estáticos (CSS, logo)"
echo -e "  ${GREEN}✓${NC} README.md - Documentación principal"
echo -e "  ${GREEN}✓${NC} .env.example - Template de configuración"
echo -e "  ${GREEN}✓${NC} .gitignore - Configuración de Git"
echo -e "  ${GREEN}✓${NC} CUESTIONARIO-TROPICALIZADO.md - Documentación importante"

echo

echo -e "${CYAN}🎯 SIGUIENTES PASOS RECOMENDADOS:${NC}"
echo -e "  1. ${YELLOW}Verificar funcionalidad:${NC} Probar la aplicación localmente"
echo -e "  2. ${YELLOW}Hacer commit:${NC} git add . && git commit -m \"cleanup: Limpieza del workspace\""
echo -e "  3. ${YELLOW}Deploy a producción:${NC} ./deploy-script.sh"
echo

echo -e "${GREEN}🎉 Workspace limpio y optimizado para producción!${NC}"
echo

# Mostrar estructura final
echo -e "${CYAN}📁 ESTRUCTURA FINAL DEL PROYECTO:${NC}"
tree -a -I '.git' . 2>/dev/null || ls -la