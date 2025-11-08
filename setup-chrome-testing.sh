#!/bin/bash
# Setup Chrome Testing - Formulario DevOps ReadyMind
# Configuración automática para testing con Chrome WebDriver

echo "🧪 SETUP CHROME TESTING - FORMULARIO DEVOPS READYMIND"
echo "====================================================="
echo "Configuración automática para testing visual con Chrome"
echo ""

# Función para verificar comando
check_command() {
    if command -v "$1" &> /dev/null; then
        echo "✅ $1 está disponible"
        return 0
    else
        echo "❌ $1 no está disponible"
        return 1
    fi
}

# Verificar Python
echo "🐍 Verificando Python..."
if check_command python3; then
    python3 --version
else
    echo "❌ Python3 es requerido. Instálalo primero."
    exit 1
fi

# Crear entorno virtual para Chrome testing
echo ""
echo "📦 Creando entorno virtual para Chrome testing..."
python3 -m venv chrome_testing_env

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source chrome_testing_env/bin/activate

# Actualizar pip
echo "⬆️ Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "📥 Instalando dependencias para Chrome testing..."
pip install -r requirements_chrome_testing.txt

# Verificar instalación de Selenium
echo ""
echo "✅ Verificando instalación..."
python3 -c "
import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
print(f'✅ Selenium {selenium.__version__} instalado')
print(f'✅ Requests disponible')
print('✅ WebDriver Manager disponible')
print('✅ Todas las dependencias instaladas correctamente')
"

# Verificar Chrome/Chromium
echo ""
echo "🌐 Verificando navegador Chrome..."
if check_command google-chrome; then
    google-chrome --version
elif check_command chromium-browser; then
    chromium-browser --version
elif check_command chromium; then
    chromium --version
else
    echo "⚠️ Chrome no detectado. Instalando Chrome..."
    
    # Detectar sistema operativo
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux/WSL
        if command -v apt &> /dev/null; then
            echo "📦 Instalando Chrome en Ubuntu/Debian..."
            wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
            echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
            sudo apt update
            sudo apt install -y google-chrome-stable
        elif command -v yum &> /dev/null; then
            echo "📦 Instalando Chrome en CentOS/RHEL..."
            sudo yum install -y google-chrome-stable
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            echo "📦 Instalando Chrome en macOS..."
            brew install --cask google-chrome
        else
            echo "ℹ️ Instala Chrome manualmente desde: https://www.google.com/chrome/"
        fi
    else
        echo "ℹ️ Sistema no reconocido. Instala Chrome manualmente."
    fi
fi

# Crear directorio para screenshots
echo ""
echo "📸 Creando directorio para screenshots..."
mkdir -p chrome_test_screenshots

# Test rápido de conectividad
echo ""
echo "🔗 Probando conectividad con el formulario..."
python3 -c "
import requests
try:
    response = requests.get('https://formulario-devops-s2uxxgzelbnnk.azurewebsites.net/', timeout=10)
    if response.status_code == 200:
        print('✅ Formulario accesible')
    else:
        print(f'⚠️ Formulario responde con código: {response.status_code}')
except Exception as e:
    print(f'❌ Error de conectividad: {e}')
"

echo ""
echo "✅ SETUP CHROME TESTING COMPLETADO"
echo "=================================="
echo ""
echo "🚀 Para ejecutar el test Chrome:"
echo ""
echo "1. Activar entorno virtual:"
echo "   source chrome_testing_env/bin/activate"
echo ""
echo "2. Ejecutar test Chrome completo:"
echo "   python3 test_chrome_completo.py"
echo ""
echo "📋 Opciones del test:"
echo "   - Modo visual: Verás Chrome abrirse y ejecutar el test"
echo "   - Modo headless: Ejecución en segundo plano"
echo "   - Screenshots automáticos en cada paso"
echo "   - Validación completa del modal ReadyMind"
echo ""
echo "📸 Los resultados se guardarán en:"
echo "   - Screenshots: ./chrome_test_screenshots/"
echo "   - Log: ./test_chrome_completo.log"
echo ""
echo "🎉 ¡Listo para testing Chrome con validación visual!"