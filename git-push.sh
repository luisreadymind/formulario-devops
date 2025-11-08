#!/usr/bin/env bash
# Helper script to push repository to GitHub safely using SSH.
# Usage:
#   chmod +x git-push.sh
#   ./git-push.sh <ssh-remote-url>
# Example:
#   ./git-push.sh git@github.com:youruser/formulario-devops.git

set -euo pipefail

REMOTE_URL="${1:-}" # e.g. git@github.com:owner/repo.git
COMMIT_MSG="${2:-release: initial production}"

if [ -z "$REMOTE_URL" ]; then
  echo "Usage: $0 <ssh-remote-url> [commit-message]"
  echo "Example: $0 git@github.com:luisreadymind/formulario-devops.git"
  exit 1
fi

# Verificar que la URL sea SSH
if [[ ! "$REMOTE_URL" =~ ^git@github\.com: ]]; then
  echo "❌ Error: La URL debe ser SSH (git@github.com:owner/repo.git)"
  echo "📝 Ejemplo: git@github.com:luisreadymind/formulario-devops.git"
  exit 1
fi

if ! command -v git >/dev/null 2>&1; then
  echo "❌ git not found; please install git"
  exit 1
fi

# Verificar que SSH esté configurado
if [ ! -f ~/.ssh/id_rsa ] && [ ! -f ~/.ssh/id_ed25519 ]; then
  echo "❌ No se encontraron claves SSH. Genere una clave SSH primero:"
  echo "   ssh-keygen -t rsa -b 4096 -C 'your_email@example.com'"
  echo "   Luego agregue la clave pública a GitHub: https://github.com/settings/keys"
  exit 1
fi

# Verificar conectividad SSH a GitHub
echo "🔑 Verificando conectividad SSH con GitHub..."
ssh_test=$(ssh -T git@github.com 2>&1 || true)
if [[ "$ssh_test" == *"successfully authenticated"* ]]; then
  echo "✅ Conexión SSH con GitHub exitosa"
else
  echo "❌ Error de conexión SSH con GitHub."
  echo "📝 Respuesta SSH: $ssh_test"
  echo "📝 Asegúrese de que su clave SSH esté agregada a GitHub:"
  echo "   1. Copie su clave pública: cat ~/.ssh/id_rsa.pub"
  echo "   2. Vaya a: https://github.com/settings/keys"
  echo "   3. Haga clic en 'New SSH key' y pegue la clave"
  exit 1
fi

# Initialize repo if needed
if [ ! -d .git ]; then
  echo "🔧 Inicializando repositorio git..."
  git init
  git checkout -b main || git checkout -B main
fi

# Ensure user.name and user.email are set
if ! git config user.name >/dev/null; then
  echo "🔧 Configurando usuario git..."
  git config user.name "Luis Alberto Arenas"
fi
if ! git config user.email >/dev/null; then
  git config user.email "luisalberto@readymind.ms"
fi

# Stage, commit
echo "📦 Preparando commit..."
git add --all
if git diff --cached --quiet; then
  echo "ℹ️ No hay cambios para commit"
else
  git commit -m "$COMMIT_MSG"
  echo "✅ Commit creado: $COMMIT_MSG"
fi

# Configure remote
if git remote | grep -q "^origin$"; then
  git remote set-url origin "$REMOTE_URL"
  echo "🔧 Remoto 'origin' actualizado"
else
  git remote add origin "$REMOTE_URL"
  echo "🔧 Remoto 'origin' agregado"
fi

# Push
echo "🚀 Realizando push a GitHub..."
git push -u origin main

echo "✅ Push completado exitosamente!"
echo "🌐 Repositorio disponible en: ${REMOTE_URL/git@github.com:/https://github.com/}"

exit 0
