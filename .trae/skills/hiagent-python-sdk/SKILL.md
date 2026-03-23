---
name: "hiagent-python-sdk"
description: "HiAgent Python SDK（hiagent-api/components/observe/eva）接入助手：初始化、鉴权、调用示例与排错。用户提到 HiAgent/hiagent_api/Workflow/Tool/Knowledgebase/Observe/Eva 时优先使用。"
---

# HiAgent Python SDK 接入助手

## 输出要求（你对用户的回答）

- 优先给“可直接粘贴运行”的最小代码片段，并标出需要替换的占位符。
- 不要臆造不存在的 API/参数；不确定时先让用户贴报错、接口定义或示例文件路径。
- 涉及 AK/SK/AppKey/Token 时不要回显明文；示例统一用 `<VOLC_ACCESSKEY>` / `<VOLC_SECRETKEY>` / `<HIAGENT_APP_KEY>` / `<BEARER_TOKEN>` 占位符。

## 安装

### 使用本仓库源码（推荐）

本仓库是 uv workspace（根目录 `pyproject.toml` 的 `[tool.uv.workspace]`），常见用法：

```bash
uv sync --group dev
```

### 仅安装子包（按需）

子包名以各目录 `pyproject.toml` 的 `project.name` 为准：

- `libs/api` -> `hiagent-api`
- `libs/components` -> `hiagent-components`
- `libs/observe` -> `hiagent-observe`
- `libs/eva` -> `hiagent-eva`

## 鉴权与环境变量

### OpenAPI（Top Endpoint）签名鉴权

`hiagent_api.base.Service` 默认会从以下位置加载 AK/SK（优先级：环境变量 > 本地配置文件）：

- 环境变量：`VOLC_ACCESSKEY`、`VOLC_SECRETKEY`
- 本地文件：`~/.volc/credentials`（`access_key_id` / `secret_access_key`）或 `~/.volc/config`（`ak` / `sk`）

### App API（AppKey Header）

部分服务方法走 App API，需要：

- `svc.set_app_base_url("<HIAGENT_APP_BASE_URL>")`
- 调用时传 `app_key="<HIAGENT_APP_KEY>"`（请求 header `Apikey`）

### 常用环境变量（仓库内示例使用）

参考根目录 `.env-sample`：

- `HIAGENT_TOP_ENDPOINT`
- `HIAGENT_TRACE_ENDPOINT`
- `HIAGENT_UP_UPLOAD_ENDPOINT` / `HIAGENT_UP_DOWNLOAD_ENDPOINT`
- `VOLC_ACCESSKEY` / `VOLC_SECRETKEY`
- `CUSTOM_APP_ID`
- `HIAGENT_APP_BASE_URL`
- `HIAGENT_APP_KEY`（workflow app key）
- `HIAGENT_AGENT_APP_KEY`（agent app key）

## 最小可运行示例

### 1) Workflow：运行一个工作流

```python
import json
import os

from dotenv import load_dotenv
from hiagent_api.workflow import WorkflowService
from hiagent_api.workflow_types import RunWorkflowRequest

load_dotenv()

svc = WorkflowService(
    endpoint=os.getenv("HIAGENT_TOP_ENDPOINT") or "",
    region="cn-north-1",
)
svc.set_app_base_url(os.getenv("HIAGENT_APP_BASE_URL") or "")

app_key = os.getenv("HIAGENT_APP_KEY") or "<HIAGENT_APP_KEY>"

resp = svc.run_workflow(
    app_key,
    RunWorkflowRequest(
        input_data=json.dumps({"query": "你好"}, ensure_ascii=False),
        user_id="test",
        app_key=app_key,
    ),
)
print(resp)
```

### 2) Tool：拉取并执行归档工具

```python
import os

from dotenv import load_dotenv
from hiagent_api.tool import ToolService
from hiagent_api.tool_types import ExecArchivedToolRequest, GetArchivedToolRequest

load_dotenv()

svc = ToolService(endpoint=os.getenv("HIAGENT_TOP_ENDPOINT") or "", region="cn-north-1")

workspace_id = "<WORKSPACE_ID>"
tool_id = "<TOOL_ID>"

tool = svc.get_archived_tool(GetArchivedToolRequest(id=tool_id, workspace_id=workspace_id))

resp = svc.exec_archived_tool(
    ExecArchivedToolRequest(
        workspace_id=workspace_id,
        plugin_id=tool.plugin_id,
        tool_id=tool_id,
        config="",
        input_data='{"query": "llm"}',
    )
)
print(resp)
```

### 3) Knowledgebase：检索问答

```python
import os

from dotenv import load_dotenv
from hiagent_api.knowledgebase import KnowledgebaseService
from hiagent_api.knowledgebase_types import QueryRequest

load_dotenv()

svc = KnowledgebaseService(endpoint=os.getenv("HIAGENT_TOP_ENDPOINT") or "", region="cn-north-1")

resp = svc.query(
    QueryRequest(
        workspace_id="<WORKSPACE_ID>",
        dataset_ids=["<DATASET_ID>"],
        keywords=["大熊猫的生活习性"],
        top_k=3,
        score_threshold=0.4,
        type=1,
        retrieval_search_method=0,
        rerank_id=None,
    )
)
print(resp)
```

## 排错清单（高频）

- 401/403：检查 `VOLC_ACCESSKEY` / `VOLC_SECRETKEY` 是否生效（或 ~/.volc 配置），以及 `endpoint/region` 是否匹配环境。
- App API 报错：确认已 `set_app_base_url()`，并且调用入参里带 `app_key`。
- 参数字段不对：优先对照 `libs/api/examples/*` 下的示例脚本与 `*_types.py` 的请求结构。

