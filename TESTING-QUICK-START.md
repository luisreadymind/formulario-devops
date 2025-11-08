# Quick Start - Testing Script para Formulario DevOps ReadyMind

## 🚀 Configuración Rápida

### Opción 1: Script Automatizado (Recomendado)
```bash
# Ejecutar script de configuración automática
./setup-testing.sh
```

### Opción 2: Configuración Manual
```bash
# 1. Crear entorno virtual
python3 -m venv testing_env

# 2. Activar entorno virtual
source testing_env/bin/activate

# 3. Instalar dependencias
pip install -r requirements_testing.txt

# 4. Crear directorio para screenshots
mkdir -p test_screenshots
```

## 🧪 Ejecutar Testing

```bash
# Activar entorno (si no está activo)
source testing_env/bin/activate

# Ejecutar script de testing
python3 test_formulario_devops.py
```

### Opciones Interactivas

El script solicita:

1. **URL del formulario**: 
   - Presiona Enter para usar: `https://formulario-devops-s2uxxgzelbnnk.azurewebsites.net/`
   - O ingresa una URL personalizada

2. **Modo headless**:
   - `N` (recomendado): Muestra el navegador durante el testing
   - `Y`: Ejecuta sin interfaz gráfica (más rápido)

## 📊 Resultados Esperados

### Testing Exitoso:
```
✅ TEST EXITOSO - Modal de despedida funcionando correctamente
📸 Screenshots guardados en: ./test_screenshots/
📋 Log detallado en: ./test_formulario_devops.log
```

### Archivos Generados:
- **Screenshots**: `./test_screenshots/` (9 imágenes del proceso)
- **Log**: `./test_formulario_devops.log` (registro detallado)

## 🎯 Qué Testea el Script

1. ✅ **Carga del formulario** con sección de bienvenida ReadyMind
2. ✅ **Llenado automático** de datos del cliente
3. ✅ **Respuesta a todas las preguntas** del cuestionario (60+)
4. ✅ **Validación del progreso** al 100%
5. ✅ **Envío del formulario** y aparición del modal
6. ✅ **Validación del modal** con elementos ReadyMind
7. ✅ **Testing del cierre** y funcionalidad de auto-close

## 🔧 Troubleshooting

### Error: Chrome no encontrado
```bash
# Instalar Chrome en WSL/Ubuntu
sudo apt update
sudo apt install google-chrome-stable
```

### Error: Dependencias faltantes
```bash
# Reinstalar dependencias
pip install --upgrade -r requirements_testing.txt
```

### Error: Timeout
- Verificar conectividad a internet
- Verificar que la URL del formulario esté activa
- Aumentar timeout en el script si es necesario

## 🎯 Uso en CI/CD

Para integrar en pipelines de CI/CD:

```bash
# Modo headless automático
python3 test_formulario_devops.py << EOF


y
EOF
```

---

**¡El script está listo para validar completamente la funcionalidad del formulario DevOps ReadyMind!** 🚀