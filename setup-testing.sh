#!/bin/bash
# Script de Configuración Rápida - Testing DevOps ReadyMind
# Configura el entorno de testing automatizado para el formulario

echo "🧪 CONFIGURACIÓN DE TESTING - FORMULARIO DEVOPS READYMIND"
echo "=========================================================="

# Crear entorno virtual para testing
echo "📦 Creando entorno virtual..."
python3 -m venv testing_env

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source testing_env/bin/activate

# Actualizar pip
echo "⬆️ Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install selenium==4.15.2 chromedriver-autoinstaller==0.6.2 webdriver-manager==4.0.1 requests==2.31.0 pillow==10.1.0

# Verificar instalación
echo "✅ Verificando instalación..."
python3 -c "import selenium; print(f'Selenium {selenium.__version__} instalado correctamente')"

# Instalar Chrome si no está disponible (para WSL)
if ! command -v google-chrome &> /dev/null; then
    echo "🌐 Chrome no encontrado. Instalando Chrome para WSL..."
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
    sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
    sudo apt update
    sudo apt install -y google-chrome-stable
fi

# Crear directorio para screenshots
echo "📸 Creando directorio para screenshots..."
mkdir -p test_screenshots

echo ""
echo "✅ CONFIGURACIÓN COMPLETADA"
echo "=========================="
echo "Para ejecutar el script de testing:"
echo ""
echo "1. Activar entorno virtual:"
echo "   source testing_env/bin/activate"
echo ""
echo "2. Ejecutar script de testing:"
echo "   python3 test_formulario_devops.py"
echo ""
echo "3. O ejecutar con opciones:"
echo "   # Modo headless (sin ventana de navegador)"
echo "   python3 test_formulario_devops.py"
echo "   # Luego seguir las instrucciones interactivas"
echo ""
echo "📋 Los resultados se guardarán en:"
echo "   - Screenshots: ./test_screenshots/"
echo "   - Log: ./test_formulario_devops.log"
echo ""
echo "🎉 ¡Listo para testing automatizado!"