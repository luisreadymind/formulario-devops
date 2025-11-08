#!/usr/bin/env bash
# Helper script to push repository to GitHub safely.
# Usage:
#   chmod +x git-push.sh
#   ./git-push.sh <remote-https-url>
# Example:
#   ./git-push.sh https://github.com/youruser/formulario-devops.git

set -euo pipefail

REMOTE_URL="${1:-}" # e.g. https://github.com/owner/repo.git
COMMIT_MSG="${2:-release: initial production}"

if [ -z "$REMOTE_URL" ]; then
  echo "Usage: $0 <remote-https-url> [commit-message]"
  exit 1
fi

# Security note: Do NOT paste personal access tokens (PAT) into this script or into chat.
# Recommended: export GITHUB_TOKEN as an environment variable before running.

if ! command -v git >/dev/null 2>&1; then
  echo "git not found; please install git"
  exit 1
fi

# Initialize repo if needed
if [ ! -d .git ]; then
  echo "Initializing git repository..."
  git init
  git checkout -b main || git checkout -B main
fi

# Ensure user.name and user.email are set
if ! git config user.name >/dev/null; then
  git config user.name "Your Name"
fi
if ! git config user.email >/dev/null; then
  git config user.email "you@example.com"
fi

# Stage, commit
git add --all
if git diff --cached --quiet; then
  echo "No changes to commit"
else
  git commit -m "$COMMIT_MSG"
fi

# Push strategy
# If GITHUB_TOKEN is set, use a temporary authenticated remote URL; otherwise rely on interactive auth.
if [ -n "${GITHUB_TOKEN:-}" ]; then
  echo "Detected GITHUB_TOKEN in environment. Using it to authenticate push (token not printed)."

  # Derive host/path from REMOTE_URL, expect https://github.com/owner/repo.git
  # Remove protocol
  host_path=${REMOTE_URL#https://}
  auth_remote="https://x-access-token:${GITHUB_TOKEN}@${host_path}"

  # Add or replace temporary remote
  if git remote | grep -q "^temp-auth-origin$"; then
    git remote remove temp-auth-origin
  fi
  git remote add temp-auth-origin "$auth_remote"

  # Push
  git push -u temp-auth-origin main --force

  # Make sure origin exists and points to clean URL
  if git remote | grep -q "^origin$"; then
    git remote set-url origin "$REMOTE_URL"
  else
    git remote add origin "$REMOTE_URL"
  fi

  # Remove temporary auth remote
  git remote remove temp-auth-origin

  echo "Push complete. Remote 'origin' set to: $REMOTE_URL"
else
  echo "No GITHUB_TOKEN detected. Attempting interactive push. You will be prompted for credentials if needed."

  if git remote | grep -q "^origin$"; then
    git remote set-url origin "$REMOTE_URL"
  else
    git remote add origin "$REMOTE_URL"
  fi

  git push -u origin main
fi

echo "Done. If this is the first time pushing, ensure the GitHub repo exists or create it via the GitHub web UI or 'gh repo create'."

exit 0
