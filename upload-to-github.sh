#!/bin/bash
# Script para subir archivos al repositorio usando GitHub API
# NOTA: Este script requiere configurar GITHUB_TOKEN como variable de entorno
# Uso: export GITHUB_TOKEN="your_token_here" && ./upload-to-github.sh

if [ -z "${GITHUB_TOKEN:-}" ]; then
  echo "❌ Error: GITHUB_TOKEN no está configurado"
  echo "📝 Configure el token como variable de entorno:"
  echo "   export GITHUB_TOKEN='your_personal_access_token'"
  exit 1
fi

REPO="luisreadymind/formulario-devops"

# Función para crear archivo en GitHub
create_file() {
    local file_path=$1
    local github_path=$2
    
    if [ ! -f "$file_path" ]; then
        echo "❌ Archivo no encontrado: $file_path"
        return 1
    fi
    
    echo "📄 Subiendo: $github_path"
    
    # Codificar archivo en base64
    content=$(base64 -w 0 "$file_path")
    
    # Crear archivo usando GitHub API
    curl -s -X PUT \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        "https://api.github.com/repos/$REPO/contents/$github_path" \
        -d "{
            \"message\": \"Add $github_path\",
            \"content\": \"$content\"
        }" > /dev/null
    
    if [ $? -eq 0 ]; then
        echo "✅ $github_path subido exitosamente"
    else
        echo "❌ Error subiendo $github_path"
    fi
}

echo "🚀 Subiendo archivos al repositorio GitHub..."
echo ""

# Subir archivos principales
create_file "README.md" "README.md"
create_file "app.py" "app.py"
create_file "requirements.txt" "requirements.txt"
create_file "cuestionario_devops_azure.json" "cuestionario_devops_azure.json"
create_file ".gitignore" ".gitignore"
create_file ".env.example" ".env.example"
create_file "deploy-script.sh" "deploy-script.sh"
create_file "git-push.sh" "git-push.sh"

# Subir templates
create_file "templates/form.html" "templates/form.html"

# Subir archivos CSS
create_file "static/css/bootstrap-grid.min.css" "static/css/bootstrap-grid.min.css"
create_file "static/css/bundle.min.css" "static/css/bundle.min.css"

echo ""
echo "✅ ¡Todos los archivos han sido subidos al repositorio!"
echo "🌐 Ver en: https://github.com/$REPO"