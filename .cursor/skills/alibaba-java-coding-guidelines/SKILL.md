---
name: alibaba-java-coding-guidelines
description: >-
  阿里巴巴 Java 开发手册规范：命名、OOP、集合、并发、异常、日志、MySQL、安全。
  编写或审查任何 Java 代码时必须使用。
---

# 阿里巴巴 Java 开发手册（Agent 执行版）

本项目业务后端为 Spring Boot / Java（见 `specs/006-tech-stack.md`）。**凡 `*.java`** 必须遵守本 Skill。审查时与 `auto-code-review` 联用。

依据：《阿里巴巴 Java 开发手册》常见强制/推荐项（Agent 落地浓缩）。冲突时：**手册强制项 > 个人偏好**。

## 何时使用

- 新建/修改 `*.java`
- CR 发现 Java 变更
- 用户提到「阿里规范 / Java 规约 / P3C」

## 1. 命名

- 类名 `UpperCamelCase`；方法/变量 `lowerCamelCase`；常量 `UPPER_SNAKE_CASE`。
- 抽象类优先 `Abstract`/`Base` 前缀；异常类以 `Exception` 结尾。
- 包名全小写，点分隔，单义英语；禁止下划线与大写。
- 接口勿加 `I` 前缀；实现类可用 `Impl` 或业务名。
- **禁止**拼音与英文混用（国际通用除外如 alibaba、taobao）。

## 2. 常量与魔法值

- 禁止未定义含义的魔法值直接出现在业务逻辑；提取为有名常量。
- `long` 字面量用大写 `L`（禁止小写 `l`）。
- 固定范围用枚举，优于裸 `int` 状态码散落。

## 3. OOP 与类设计

- 覆写必须加 `@Override`。
- equals / hashCode 成对重写；用对象比较时注意 `null`。
- 对外 API 勿暴露受保护可变字段；优先不可变或拷贝。
- 构造方法禁止写业务逻辑；复杂初始化用静态工厂或 Builder。
- 慎用继承，优先组合；`final` 用于防覆写/防继承当有明确意图时。

## 4. 集合与并发

- `ArrayList`/`HashMap` 等指定初始容量（可预估时）。
- foreach 中禁止 `remove`；用 `Iterator.remove` 或 `removeIf`。
- `hashCode` 变更的对象勿作 `HashMap` key。
- 线程池必须用 `ThreadPoolExecutor` 显式创建，**禁止** `Executors` 便捷工厂（风险：OOM / 无界队列）。
- `SimpleDateFormat` 线程不安全 → `DateTimeFormatter` 或 ThreadLocal。
- 锁：锁范围最小化；多锁按固定顺序；`wait/notify` 在循环中判断条件。

## 5. 异常与日志

- 捕获后禁止空 `catch`；要么处理要么向上抛，并带上下文。
- 不要用异常做流程控制。
- 日志用门面（SLF4J）；`{}` 占位，禁止字符串拼接后再判断级别。
- 异常日志必须带堆栈（`log.error("msg", e)`）；禁止只 `e.getMessage()`。
- 对外吞异常时记录日志并返回明确错误。

## 6. MySQL / 数据访问（若涉及）

- 禁止 `select *`；明确字段列表。
- 更新/删除必须带 `WHERE`；注意批量与索引。
- 表达是否：`is_xxx` → 字段 `tinyint`；Java 布尔属性注意与 ORM 映射。
- 小数用 `decimal`；金额勿用 `float`/`double`。
- 外键约束慎用（手册倾向应用层控制）；但一致性方案需写明。

## 7. 安全

- 用户输入必须校验与转义；防 SQL 注入（参数绑定）、XSS。
- 敏感数据脱敏；禁止日志打印密码、完整证件号、密钥。
- 上传校验类型与大小；路径穿越防护。

## 8. 工程结构

- 应用分层清晰：`controller` / `service` / `repository`（或 `dao`）职责不串。
- Controller 不做复杂业务；Service 事务边界明确。
- 工具类 `XxxUtils` 应为静态方法 + 私有构造，或明确无状态。

## CR 时如何报

按手册优先级标注：

- **【强制】** → `auto-code-review` 的「阻塞」
- **【推荐】/【参考】** → 「建议」

每条格式：`` `File.java:行或符号`: 【强制】问题 → 改法 ``

## 快速自检清单

- [ ] 命名与常量合规
- [ ] 无裸魔法值、无空 catch
- [ ] 集合修改方式安全
- [ ] 线程池非 Executors 创建
- [ ] 日志占位符 + 异常堆栈
- [ ] SQL/输入安全
- [ ] 分层未被破坏
