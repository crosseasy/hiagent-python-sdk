---
name: "hiagent-python-sdk"
description: "HiAgent Python SDK 调通助手：从 0 配好环境变量与鉴权，跑通 workflow/tool/knowledgebase/observe/eva 示例并排错。用户提到 HiAgent SDK、hiagent_api、工作流、工具、知识库、Trace/Observe/Eva 时必须优先使用。"
---

# HiAgent Python SDK 调通助手

## 目标

把这个仓库的 SDK 从“装好”变成“能跑通一次真实请求”，并给出可复用的最小代码与排错路径。

## 回答输出要求

- 优先输出可直接复制运行的步骤与代码片段。
- 不确定用户环境/版本时，先让用户贴：操作系统、Python 版本、以及执行命令与完整报错。
- 不要回显任何真实 AK/SK/AppKey/Token；示例用占位符。

## 你需要的信息（向用户索取）

- `HIAGENT_TOP_ENDPOINT`（Top/OpenAPI endpoint）
- `VOLC_ACCESSKEY`、`VOLC_SECRETKEY`
- （可选）`HIAGENT_APP_BASE_URL`、`HIAGENT_APP_KEY`（跑 workflow App API 需要）
- `WORKSPACE_ID`（跑 observe/knowledgebase/tool 常用）
- 具体要调通哪个能力：workflow / tool / knowledgebase / observe / eva

## 快速调通（推荐路径）

### 1) 安装依赖

本仓库是 uv workspace：

```bash
uv sync --group dev
```

### 2) 配置 .env

根目录已有 `.env-sample`。让用户复制成 `.env` 并填值（不要把真实值贴到对话里）：

```bash
cp .env-sample .env
```

至少需要：

- `HIAGENT_TOP_ENDPOINT`
- `VOLC_ACCESSKEY`
- `VOLC_SECRETKEY`

### 3) 先跑 Smoke Test（不暴露密钥）

运行本 skill 附带脚本（仅检查 import/配置存在与基础连通性，不打印敏感值）：

```bash
python skills/hiagent-python-sdk/scripts/smoke_test.py
```

### 4) 跑通一个真实示例（按场景）

#### Workflow（App API）

需要额外配置：

- `HIAGENT_APP_BASE_URL`
- `HIAGENT_APP_KEY`

直接运行示例：

```bash
python libs/api/examples/workflow/run_workflow.py
```

#### Tool（归档工具）

直接运行示例，并按需替换 `workspace_id/tool_id`：

```bash
python libs/api/examples/tool/get_and_exec_tool.py
```

#### Knowledgebase（检索）

```bash
python libs/api/examples/knowledgebase/query.py
```

#### Observe（创建 API Token）

需要 `WORKSPACE_ID`：

```bash
python libs/api/examples/observe/create_api_token.py
```

## SDK 关键点（排错时用）

### 鉴权方式

- Top/OpenAPI：使用 `VOLC_ACCESSKEY` / `VOLC_SECRETKEY` 做签名鉴权（由 `hiagent_api.base.Service` 统一处理）
- App API：使用 `Apikey: <HIAGENT_APP_KEY>` header（需先 `set_app_base_url()`）
- Webhook：`Authorization: Bearer <BEARER_TOKEN>`（仅特定接口需要）

### endpoint / region

大多数 service 构造函数形如：

```python
svc = XxxService(endpoint="<HIAGENT_TOP_ENDPOINT>", region="cn-north-1")
```

如果报签名/权限/路由相关错误，优先让用户确认：

- endpoint 是否为正确环境
- region 是否与 endpoint 匹配

## 参考文档（按 Service）

- ChatService：`skills/hiagent-python-sdk/references/chat_service.md`
- WorkflowService：`skills/hiagent-python-sdk/references/workflow_service.md`
- ToolService：`skills/hiagent-python-sdk/references/tool_service.md`
- KnowledgebaseService：`skills/hiagent-python-sdk/references/knowledgebase_service.md`
- ObserveService：`skills/hiagent-python-sdk/references/observe_service.md`

## 高频问题与处理

- 401/403：检查 AK/SK 是否生效（环境变量或 ~/.volc），以及 endpoint/region 是否匹配
- App API 报错：确认 `set_app_base_url()` 已调用且 `app_key` 入参正确
- import 报错：确认 `uv sync --group dev` 成功且在仓库根目录执行
