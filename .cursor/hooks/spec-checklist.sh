#!/usr/bin/env bash
# Optional helper: print a Spec consistency checklist to stdout for agents/scripts.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

echo "=== Spec 一致性检查清单 ==="
echo "项目根: $ROOT"
echo
echo "[ ] 已阅读 AGENTS.md"
echo "[ ] 相关 specs/00x-*.md 已更新（若有行为变更）"
echo "[ ] 无 .env / 密钥文件进入暂存区"
echo "[ ] 无非官方抓包发帖代码"
echo "[ ] 未擅自 commit/push（除非用户明确要求）"
echo
echo "现有 Spec 文件:"
ls -1 "$ROOT/specs" 2>/dev/null || echo "(specs 目录缺失)"
