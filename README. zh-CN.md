---

### `README.zh-CN.md`

```markdown
# Public Repository Policy

**版本:** 1.0  
**日期:** 2026-08-20  
**状态:** DEVELOPMENT

## 1. 目的

本仓库是公开文档与 AI 记忆展示层。

公开内容仅用于：

- 项目概念说明
- 架构摘要
- 开发记录
- 可公开的测试与模拟结果
- AI 记忆索引

本仓库不作为私有核心源代码的存储位置。

## 2. 公开层

公开层原则上只提供 Markdown 文档：

- `README.md`
- `README.zh-TW.md`
- `README.zh-CN.md`
- `README.en-US.md`
- `docs/*.md`
- 概念性图表与公开说明

文档不得包含：

- 私钥
- API Token
- 密码
- 私有域名
- 私有 IP
- 模型权重
- 私有 Prompt
- 完整核心算法
- 私有 Agent 路由规则
- 可直接部署的核心实现

## 3. 私有核心

完整开发环境应存放在受控的私有环境，包括：

- 源代码
- 私有 Git Repository
- CI/CD
- 模型与权重
- 私有 AI / Agent 配置
- 私有记忆数据
- 备份文件
- 内部测试数据

公开文档可以保留索引或摘要，但不应因此暴露私有实现。

## 4. AI Memory

公开 Markdown 可以作为开发记忆的摘要层。

记忆资料应明确区分：

`CLAIM` → 单方描述  
`SIMULATION` → 模拟数据  
`VERIFIED` → 已验证数据  
`PRIVATE` → 私有开发数据

“AI 记得某项开发内容”并不代表该内容已经在现实世界完成。

## 5. 公开安全原则

公开 Repository 应避免提交：

- 压缩文件
- 可执行文件
- 机密配置
- 私有证书
- CI/CD 工作流程
- 可以还原核心实现的完整代码

真正的安全措施应依靠 Repository 权限、访问控制、Secrets 管理与私有环境，而不是单纯将文件内容转换成乱码。

## 6. 状态

```text
Repository: PUBLIC DOCUMENTATION
Core Implementation: PRIVATE
Status: DEVELOPMENT
