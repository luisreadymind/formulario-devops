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

## Publicar en GitHub (proceso seguro)

Se recomienda no incluir tokens en scripts ni en chats. Use una de estas opciones para subir el código al repositorio remoto:

1) Usar `GITHUB_TOKEN` en la sesión (recomendado para CI/local):

   - En WSL / Linux / macOS:
     ```bash
     export GITHUB_TOKEN="<your_personal_access_token>"
     ./git-push.sh https://github.com/<owner>/formulario-devops.git
     ```
   - El script `git-push.sh` añadirá un remoto temporal autenticado para hacer `git push` y lo limpiará después. No se guarda el token en el repositorio.

2) Usar la CLI de GitHub interactiva `gh` (recomendado para usuarios):

   ```bash
   gh auth login
   gh repo create <owner>/formulario-devops --public --source=. --remote=origin
   git push -u origin main
   ```

3) Usar la interfaz web de GitHub para crear el repositorio y luego ejecutar:

   ```bash
   git remote add origin https://github.com/<owner>/formulario-devops.git
   git push -u origin main
   ```

Importante: Nunca pegue su PAT en un chat público o en un repositorio. Mantenga las credenciales en variables de entorno o el administrador de credenciales de su sistema.

Archivos útiles añadidos:

- `git-push.sh` - Script helper para inicializar/commitar y empujar al remoto usando `GITHUB_TOKEN` opcional.
