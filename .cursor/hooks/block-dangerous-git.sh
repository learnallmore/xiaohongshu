#!/usr/bin/env bash
# Block dangerous git operations and accidental home-directory git usage.
set -euo pipefail

input=$(cat || true)
command=$(printf '%s' "$input" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("command") or "")' 2>/dev/null || true)

deny() {
  local msg="$1"
  python3 -c 'import json,sys; print(json.dumps({"permission":"deny","user_message":sys.argv[1],"agent_message":sys.argv[1]}, ensure_ascii=False))' "$msg"
  exit 0
}

allow() {
  echo '{"permission":"allow"}'
  exit 0
}

# Empty command — allow
if [[ -z "${command}" ]]; then
  allow
fi

# Normalize for matching
lower=$(printf '%s' "$command" | tr '[:upper:]' '[:lower:]')

# Dangerous git patterns
if printf '%s' "$lower" | grep -Eq '(^|[;&|[:space:]])git[[:space:]]+push[[:space:]]+[^;&|]*--force|(^|[;&|[:space:]])git[[:space:]]+push[[:space:]]+[^;&|]*-f([[:space:]]|$)|git[[:space:]]+push[[:space:]]+--force-with-lease'; then
  deny "已拦截 force push。若确需执行，请用户在对话中明确授权后再改 hook 或手工执行。"
fi

if printf '%s' "$lower" | grep -Eq 'git[[:space:]]+config'; then
  deny "已拦截 git config 修改（项目宪法禁止 Agent 改 git 配置）。"
fi

if printf '%s' "$lower" | grep -Eq 'git[[:space:]]+reset[[:space:]]+--hard'; then
  deny "已拦截 git reset --hard（破坏性操作，需用户明确要求）。"
fi

if printf '%s' "$lower" | grep -Eq 'git[[:space:]]+(commit|push|add)[[:space:]]+.*--no-verify'; then
  deny "已拦截跳过 hooks 的 git 操作（--no-verify）。"
fi

# Prevent operating on the home-directory accidental git root
if printf '%s' "$command" | grep -Eq 'git[[:space:]]+-C[[:space:]]+(/Users/[^/]+|/home/[^/]+)[[:space:]]'; then
  deny "已拦截针对用户家目录的 git -C 操作，请只在本项目目录内使用 git。"
fi

allow
