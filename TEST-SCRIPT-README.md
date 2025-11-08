# Script de Testing Automatizado - Formulario DevOps ReadyMind

Este script automatiza completamente el proceso de testing del formulario DevOps, incluyendo la validación del modal de despedida con funcionalidad de cierre automático de ventana.

## 🎯 Características del Script

### ✅ Funcionalidades Implementadas

1. **Automatización Completa del Formulario**
   - Llenado automático de datos del cliente
   - Respuesta inteligente a todas las 60+ preguntas del cuestionario
   - Validación de progreso en tiempo real

2. **Testing del Modal de Despedida**
   - Validación de aparición del modal después del envío
   - Verificación de elementos ReadyMind (logo, branding)
   - Testing de funcionalidad de cierre con confirmación

3. **Logging y Screenshots Comprehensivos**
   - Log detallado de cada paso del proceso
   - Screenshots automáticos en puntos clave
   - Manejo de errores con capturas de pantalla

4. **Configuración Avanzada**
   - Modo headless configurable
   - URL personalizable
   - Configuración optimizada del navegador

## 🚀 Instalación y Configuración

### 1. Instalar Dependencias

```bash
# Instalar dependencias de Python
pip install -r requirements_testing.txt

# O instalar manualmente
pip install selenium==4.15.2 chromedriver-autoinstaller==0.6.2 webdriver-manager==4.0.1
```

### 2. Configurar Chrome Driver

El script utiliza Chrome WebDriver. Asegúrate de tener Chrome instalado:

- **Windows**: Chrome se detecta automáticamente
- **WSL/Linux**: Instalar Chrome y configurar path

```bash
# Para WSL/Ubuntu
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
sudo apt update
sudo apt install google-chrome-stable
```

## 🧪 Uso del Script

### Ejecución Básica

```bash
python test_formulario_devops.py
```

### Parámetros Interactivos

El script solicita:
1. **URL del formulario** (default: https://formulario-devops-s2uxxgzelbnnk.azurewebsites.net/)
2. **Modo headless** (y/N para ejecutar sin interfaz gráfica)

### Ejemplo de Ejecución

```
🧪 SCRIPT DE TESTING - FORMULARIO DEVOPS READYMIND
============================================================
🌐 URL del formulario (Enter para default): 
🖥️ ¿Ejecutar en modo headless? (y/N): n

🎯 Iniciando test en: https://formulario-devops-s2uxxgzelbnnk.azurewebsites.net/
👁️ Modo headless: No
------------------------------------------------------------
```

## 📊 Proceso de Testing

### 1. Configuración Inicial
- ✅ Configuración del WebDriver de Chrome
- ✅ Inicialización de timeouts y opciones
- ✅ Creación de directorio para screenshots

### 2. Carga y Validación de Página
- 🌐 Carga de la URL del formulario
- ✅ Validación de elementos de la página
- 📸 Screenshot inicial
- ✅ Verificación de sección de bienvenida ReadyMind

### 3. Llenado de Datos del Cliente
- 📝 Cliente: "ReadyMind Testing Suite"
- 📧 Email: "testing@readymind.com"
- 🏢 Empresa: "ReadyMind Tecnología"
- 📸 Screenshot de datos completados

### 4. Automatización del Cuestionario
- 🔍 Detección automática de todas las preguntas
- 🎲 Selección inteligente de respuestas:
  - **Radio buttons**: Selección aleatoria consistente
  - **Checkboxes**: Selección múltiple (1-3 opciones)
- 📊 Validación de progreso al 100%
- 📸 Screenshots cada 10 preguntas

### 5. Envío y Testing del Modal
- 🚀 Envío del formulario completo
- ⏳ Monitoreo del loading overlay
- 📋 Validación de aparición del modal
- 🔍 Verificación de elementos del modal:
  - Logo ReadyMind
  - Mensaje de despedida
  - Lista de próximos pasos
  - Aviso de cierre de ventana

### 6. Testing de Funcionalidad de Cierre
- 🔲 Click en botón "Cerrar"
- 📢 Manejo de confirmaciones del navegador
- ✅ Validación del comportamiento post-cierre

## 📸 Screenshots Generados

El script genera automáticamente screenshots en `./test_screenshots/`:

```
test_screenshots/
├── 01_pagina_inicial.png          # Página inicial cargada
├── 02_datos_cliente.png           # Datos del cliente completados
├── 03_progreso_10_preguntas.png   # Progreso cada 10 preguntas
├── 04_cuestionario_completo.png   # Cuestionario 100% completado
├── 05_antes_envio.png             # Antes del envío
├── 06_modal_resultados.png        # Modal de resultados aparecido
├── 07_modal_validacion.png        # Validación del modal completo
├── 08_antes_cerrar_modal.png      # Antes de cerrar modal
└── 09_despues_cerrar_modal.png    # Después del cierre
```

## 📋 Logging Detallado

El script genera un log completo en `./test_formulario_devops.log`:

```
2025-11-08 10:30:15 - INFO - ✅ Driver de Chrome configurado exitosamente
2025-11-08 10:30:18 - INFO - 🌐 Cargando página: https://formulario-devops-s2uxxgzelbnnk.azurewebsites.net/
2025-11-08 10:30:22 - INFO - ✅ Página cargada exitosamente
2025-11-08 10:30:22 - INFO - ✅ Sección de bienvenida ReadyMind encontrada
2025-11-08 10:30:23 - INFO - 📝 Llenando información del cliente...
2025-11-08 10:30:24 - INFO - ✅ Nombre: ReadyMind Testing Suite
...
```

## ⚡ Características Avanzadas

### Manejo Inteligente de Errores
- Timeouts configurables
- Reintentos automáticos
- Screenshots de errores
- Logging detallado de fallos

### Optimización de Performance
- Configuración optimizada del navegador
- Minimización de pauses innecesarias
- Scroll inteligente hacia elementos
- Detección automática de elementos

### Compatibilidad Multi-Plataforma
- Windows nativo
- WSL (Windows Subsystem for Linux)
- Linux/Ubuntu
- Detección automática de Chrome

## 🔧 Personalización

### Modificar Datos de Prueba

```python
self.test_data = {
    'client_name': 'Tu Empresa Testing',
    'client_email': 'test@tuempresa.com',
    'client_company': 'Tu Empresa S.A.S.'
}
```

### Ajustar Timeouts

```python
self.wait = WebDriverWait(self.driver, 30)  # Aumentar timeout
```

### Configurar Screenshots

```python
# Cambiar frecuencia de screenshots
if i % 5 == 0:  # Cada 5 preguntas en lugar de 10
    self.driver.save_screenshot(f'screenshots/progress_{i}.png')
```

## 🎯 Casos de Uso

### 1. Validación Pre-Deployment
Ejecutar antes de cada deployment para asegurar que todas las funcionalidades están operativas.

### 2. Testing de Regresión
Verificar que cambios en el código no afecten la funcionalidad del modal.

### 3. Validación de Performance
Monitorear tiempos de respuesta y carga del formulario.

### 4. Testing Cross-Browser
Base para extender a otros navegadores (Firefox, Safari, Edge).

## 🚨 Troubleshooting

### Error: Chrome Driver No Encontrado
```bash
pip install --upgrade chromedriver-autoinstaller
```

### Error: Selenium TimeoutException
- Verificar conectividad a internet
- Aumentar timeout en configuración
- Verificar URL del formulario

### Error: Modal No Aparece
- Verificar que todas las preguntas estén respondidas
- Revisar logs para errores de validación
- Verificar estado del servidor

## 📈 Métricas de Testing

El script proporciona métricas completas:
- ⏱️ **Tiempo total de ejecución**
- 📊 **Preguntas respondidas vs total**
- 📸 **Screenshots generados**
- ✅ **Status de validaciones del modal**
- 🔍 **Errores encontrados y resueltos**

## 🎉 Resultado Esperado

```
✅ TEST EXITOSO - Modal de despedida funcionando correctamente
📸 Screenshots guardados en: ./test_screenshots/
📋 Log detallado en: ./test_formulario_devops.log
🎉 Gracias por usar ReadyMind Testing Suite
```

---

**Nota**: Este script está diseñado específicamente para validar la funcionalidad completa del formulario DevOps ReadyMind, con especial énfasis en el modal de despedida y su funcionalidad de cierre automático de ventana.