#!/usr/bin/env bash
# Safely install/copy skill folders into an explicitly provided local target.
set -euo pipefail
if [[ "$#" -ne 2 || "$1" != "--target" ]];then
 echo 'Usage: bash INSTALL.sh --target /path/to/skills-directory' >&2
 echo 'Codex: ~/.agents/skills  |  Claude: ~/.claude/skills' >&2
 exit 2
fi
TARGET="$2"; HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -z "$TARGET" || "$TARGET" == "/" ]];then echo 'Invalid target' >&2;exit 2;fi
mkdir -p "$TARGET"
count=0
for item in "$HERE"/skills/awwwards-*; do
 name="$(basename "$item")"
 if [[ -e "$TARGET/$name" ]]; then
  echo "SKIP already exists: $TARGET/$name"; continue
 fi
 cp -R "$item" "$TARGET/$name";echo "INSTALLED: $TARGET/$name";count=$((count+1))
done
echo "Installed $count new skill folders; no existing folder overwritten."
