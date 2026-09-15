# 005 — Publisher 适配器（真实发布）

## 目标

以适配器模式对接 **官方开放平台或用户指定的合规第三方**，实现真实笔记发布与后续数据查询。禁止非官方 Cookie / 逆向签名方案。

## 接口契约（逻辑）

```typescript
interface PublishRequest {
  title: string
  body: string
  tags: string[]
  images: Array<{
    localPathOrUrl: string
    width: number
    height: number
    mimeType: string
    source: string
    license: string
  }>
  dryRun?: boolean
}

interface PublishResult {
  ok: boolean
  externalNoteId?: string
  raw?: unknown
  errorCode?: string
  errorMessage?: string
}

interface NoteMetrics {
  externalNoteId: string
  views: number
  likes: number
  collects: number
  comments: number
  shares?: number
  capturedAt: string
}

interface PublisherAdapter {
  name: string
  publish(req: PublishRequest): Promise<PublishResult>
  fetchMetrics(externalNoteId: string): Promise<NoteMetrics>
  refreshAuthIfNeeded(): Promise<void>
}
```

## 实现策略

| Adapter | 说明 |
|---------|------|
| `OfficialXhsPublisher` | 官方 OAuth / Device Grant + 文档中的发布与数据 API |
| `ThirdPartyPublisher` | 用户指定的合规 SaaS（API Key） |
| `NoopPublisher` | 开发态干跑，只记日志不发帖 |

运行时通过环境变量 `PUBLISHER_DRIVER=official|third_party|noop` 选择。

## 合规与版权

- 图片：`AI 生成` / `自有拍摄` / `授权图库`；每张图必须有 `source` + `license`。
- 禁止未授权转载他人笔记原图原文。
- 不实现、不文档化抓包发帖步骤。

## 账号连接（当前搁置）

- 如何把本机运营台绑到用户的小红书账号（OAuth / Device Grant / 合规第三方具体步骤）**暂不清楚则先不做**。
- Phase 2–3：默认 `PUBLISHER_DRIVER=noop`；「通过并发布」只走干跑，UI 可提示「账号未绑定」。
- 用户日后提供官方文档或指定第三方后，再实现 `OfficialXhsPublisher` / `ThirdPartyPublisher` 与鉴权存储。
- Adapter 实现落在 **Spring Boot**（见 `006`）；契约语言无关，可用 Java interface 表达同等字段。

## 权限缺口处理

若开放平台应用类型 **未开放个人创作者发笔记**：

1. Adapter 实现保留，`publish` 返回明确 `errorCode: PUBLISH_SCOPE_MISSING`。
2. 产品 UI 提示缺口，不降级到非官方方案。
3. 等待用户提供具备发布权限的应用或第三方。

## 配置（仅环境变量）

```bash
XHS_APP_ID=
XHS_APP_SECRET=
XHS_ACCESS_TOKEN=          # 或由 refresh 流程写入安全存储
XHS_REFRESH_TOKEN=
PUBLISHER_DRIVER=noop
THIRD_PARTY_PUBLISH_URL=
THIRD_PARTY_API_KEY=
```

具体字段以用户提供的官方文档为准，本 Spec 只定契约。
