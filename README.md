# Formulario DevOps Azure

Aplicación web Flask para evaluación de madurez DevOps con generación automática de reportes PDF.

## Características

- ✅ Formulario web interactivo con validaciones
- ✅ Estilo basado en la paleta de Azure
- ✅ Generación automática de reportes PDF
- ✅ Envío por email automático
- ✅ Cálculo de puntuación de madurez DevOps
- ✅ Responsive design

## Estructura del Proyecto

```
formulario-devops-azure/
├── app.py                          # Aplicación Flask principal
├── startup.py                      # Punto de entrada para Azure
├── requirements.txt                # Dependencias Python
├── azure-deploy.bicep             # Template de infraestructura
├── cuestionario_devops_azure.json # Estructura del cuestionario
├── templates/
│   └── form.html                  # Template del formulario
└── .env.example                   # Variables de ambiente ejemplo
```

## Instalación Local

1. Clonar el repositorio
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configurar variables de ambiente:
   ```bash
   cp .env.example .env
   # Editar .env con tus configuraciones
   ```
4. Ejecutar la aplicación:
   ```bash
   python app.py
   ```

## Despliegue en Azure

### Usando Azure CLI

1. Crear el grupo de recursos:
   ```bash
   az group create --name FormularioDevOPs --location southcentralus
   ```

2. Desplegar la infraestructura:
   ```bash
   az deployment group create \
     --resource-group FormularioDevOPs \
     --template-file azure-deploy.bicep \
     --parameters emailPassword="tu-password-email"
   ```

3. Subir el código:
   ```bash
   az webapp up \
     --name formulario-devops-[unique-string] \
     --resource-group FormularioDevOPs \
     --runtime "PYTHON:3.11"
   ```

### Usando Azure Portal

1. Crear un nuevo App Service
2. Configurar runtime: Python 3.11
3. Configurar variables de ambiente
4. Subir código via Git o ZIP

## Configuración de Email

Para habilitar el envío de emails, configura las siguientes variables de ambiente:

- `EMAIL_USER`: Usuario SMTP (ej: formularios@readymind.ms)
- `EMAIL_PASSWORD`: Contraseña del email o app password
- `SMTP_SERVER`: Servidor SMTP (ej: smtp.gmail.com)
- `SMTP_PORT`: Puerto SMTP (ej: 587)
- `DEFAULT_EMAIL_RECIPIENT`: Email destino por defecto

## API Endpoints

- `GET /` - Formulario principal
- `POST /submit` - Procesar formulario y generar PDF
- `GET /download/<filename>` - Descargar PDF generado
- `GET /health` - Health check

## Estructura del Cuestionario

El cuestionario evalúa 6 áreas de madurez DevOps:

1. **Planificación y Gestión Ágil (ALM)**
2. **Código, Control de Versiones y Calidad**
3. **CI/CD y Gestión de Releases**
4. **Infraestructura como Código y Configuración**
5. **Seguridad y Cumplimiento**
6. **Observabilidad, Monitoreo y Operación**

## Tecnologías Utilizadas

- **Backend**: Flask (Python 3.11)
- **PDF**: ReportLab
- **Styling**: CSS3 con paleta de Azure
- **Cloud**: Azure App Service (Linux)
- **Email**: SMTP con soporte para Gmail/Outlook

## Autor

Luis Alberto Arenas - ReadyMind
Email: luisalberto@readymind.ms
Fecha: Noviembre 2025

## Publicar en GitHub (proceso seguro con SSH)

Se recomienda usar SSH para mayor seguridad y simplicidad. Configuración una sola vez, sin necesidad de tokens.

### 1) Configuración inicial SSH (solo una vez):

**Paso 1: Generar clave SSH (si no existe)**
```bash
ssh-keygen -t rsa -b 4096 -C "luisalberto@readymind.ms"
# Presionar Enter para usar ubicación por defecto
# Opcional: agregar passphrase para mayor seguridad
```

**Paso 2: Agregar clave pública a GitHub**
```bash
cat ~/.ssh/id_rsa.pub
# Copiar la salida completa
```
- Ve a: https://github.com/settings/keys
- Click "New SSH key"
- Pegar la clave pública
- Título: "WSL Development Key" (o similar)
- Click "Add SSH key"

**Paso 3: Verificar conectividad**
```bash
ssh -T git@github.com
# Debe mostrar: "Hi username! You've successfully authenticated..."
```

### 2) Usar el script para subir código:

```bash
chmod +x git-push.sh
./git-push.sh git@github.com:luisreadymind/formulario-devops.git "commit message"
```

### 3) Alternativas (métodos previos mantenidos):

**Opción A: Usando `GITHUB_TOKEN` (HTTPS)**
```bash
export GITHUB_TOKEN="<your_personal_access_token>"
# Cambiar script a usar HTTPS si es necesario
```

**Opción B: CLI de GitHub interactiva**
```bash
gh auth login
gh repo create owner/formulario-devops --public --source=. --remote=origin
git push -u origin main
```

### Ventajas de SSH:
- ✅ No requiere tokens en comandos
- ✅ Configuración una sola vez
- ✅ Más seguro (clave local vs token en variables)
- ✅ Funciona con todos los comandos git
- ✅ No expira como los tokens

Archivos útiles añadidos:

- `git-push.sh` - Script helper para git push con SSH, incluye verificación de conectividad
