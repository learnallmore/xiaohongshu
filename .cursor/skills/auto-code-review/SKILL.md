---
name: auto-code-review
description: >-
  自动 Code Review：对照 Spec、安全、Publisher 合规与语言规范审查改动。
  在收工、开 PR、用户要求 review/CR、或合并前自检时使用。每次改码后强制执行。
---

# 自动 Code Review

## 何时使用

- **强制**：Agent 本轮有任何代码 / 配置 / Schema / Spec 变更时，收工前必须执行（不等用户催）
- 用户说「review / CR / 查一下改动 / 合并前检查」
- 开 PR 前的本地自检

## 与推送的关系

- 本 Skill **不**触发 `git push`。
- 仓库规范：**禁止自动推送**；仅用户明确授权后才可 push。

## 必读上下文

1. `AGENTS.md` 与相关 `specs/00x-*.md`（含 `007-frontend-design.md` 若涉 UI）
2. `.cursor/rules/project-constitution.mdc`、`security-secrets.mdc`、`mandatory-self-cr.mdc`
3. 若改动含 Java：加载 `alibaba-java-coding-guidelines` Skill
4. 若涉及发布：加载 `publisher-checklist` Skill

## 审查流程

1. **范围**：列出变更文件（逻辑分组：Spec / 配置 / 应用代码 / 测试）。
2. **正确性**：行为是否与 Spec 一致；状态机、边界、错误路径是否覆盖。
3. **安全**：无密钥、无 `.env`、无 Cookie/逆向发帖、无危险 shell。
4. **质量**：命名、重复、过宽抽象、缺少校验；Java 走阿里规范；Python 类型提示友好。
5. **前端**：若改 UI，对照 `007-frontend-design.md`（第一视口构图、字体色板、禁止项）；宿主为 FastAPI。
6. **Java**：凡 `*.java` 必须按阿里巴巴 Java 规范逐项扫；领域逻辑应在 Spring Boot，勿堆进 FastAPI。
7. **测试与门禁**：该补测是否缺失；CI 守卫是否仍会通过。
8. **栈对齐**：对照 `006-tech-stack.md`（FastAPI 运营台 + Spring Boot + 本机 MySQL；无 Docker 云部署）。

## 输出格式（固定）

用中文，按严重级别分组，每条带文件路径：

```markdown
## CR 结论
- 总体：通过 | 有条件通过 | 不通过
- 一句话理由：…

## 阻塞（必须修）
- `path`: 问题 → 建议

## 建议（非阻塞）
- `path`: …

## Spec 对齐
- 已核对 / 需更新的 Spec：…

## 安全
- 通过 | 问题列表
```

无问题时也要写「阻塞：无」，避免空报告。

## 禁止

- 不要因为「只是基建」跳过安全检查。
- 不要把风格偏好写成阻塞，除非违反项目规则、007 强制项或阿里巴巴强制项（Java）。
- 不要在报告中粘贴真实密钥内容。
- 不要在 CR 后自动 push。
