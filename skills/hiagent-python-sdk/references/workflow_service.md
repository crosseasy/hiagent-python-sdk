---
title: WorkflowService
---

# WorkflowService

## 使用场景

- 把 HiAgent 的工作流（Workflow）当作一个可编排的“函数”来调用：输入 JSON，输出 JSON。
- 需要同步阻塞拿结果：`run_workflow(...)`。
- 需要异步触发并轮询状态：`run_workflow_async(...)` + `query_workflow_status(...)`。
- 需要查询工作流定义：`get_workflow(...)`。

## 鉴权与配置

- Top/OpenAPI：通过 `VOLC_ACCESSKEY` / `VOLC_SECRETKEY` 做签名鉴权；构造 `WorkflowService(endpoint, region)` 即可。
- App API：运行工作流通常需要 `set_app_base_url(...)`，并在调用时传 `app_key`。

## 最小用法

### 1) 同步运行工作流

```python
import json
import os

from dotenv import load_dotenv
from hiagent_api.workflow import WorkflowService
from hiagent_api.workflow_types import RunWorkflowRequest

load_dotenv()

svc = WorkflowService(endpoint=os.getenv("HIAGENT_TOP_ENDPOINT") or "", region="cn-north-1")
svc.set_app_base_url(os.getenv("HIAGENT_APP_BASE_URL") or "")

app_key = os.getenv("HIAGENT_APP_KEY") or "<HIAGENT_APP_KEY>"

resp = svc.run_workflow(
    app_key,
    RunWorkflowRequest(
        app_key=app_key,
        input_data=json.dumps({"query": "你好"}, ensure_ascii=False),
        user_id="test",
        no_debug=True,
    ),
)
print(resp)
```

### 2) 异步运行并轮询状态

```python
import json
import os
import time

from dotenv import load_dotenv
from hiagent_api.workflow import WorkflowService
from hiagent_api.workflow_types import QueryWorkflowStatusRequest, RunWorkflowRequest

load_dotenv()

svc = WorkflowService(endpoint=os.getenv("HIAGENT_TOP_ENDPOINT") or "", region="cn-north-1")
svc.set_app_base_url(os.getenv("HIAGENT_APP_BASE_URL") or "")

app_key = os.getenv("HIAGENT_APP_KEY") or "<HIAGENT_APP_KEY>"

async_resp = svc.run_workflow_async(
    app_key,
    RunWorkflowRequest(
        app_key=app_key,
        input_data=json.dumps({"query": "你好"}, ensure_ascii=False),
        user_id="test",
        no_debug=True,
    ),
)

run_id = async_resp.run_id

while True:
    status = svc.query_workflow_status(
        app_key,
        QueryWorkflowStatusRequest(run_id=run_id, app_key=app_key, user_id="test"),
    )
    print(status)
    if status.status in {"success", "failed", "stopped", "interrupted"}:
        break
    time.sleep(1)
```

## 关键类型与入口文件

- 请求/响应类型：`libs/api/hiagent_api/workflow_types.py`
- 主要接口实现：`libs/api/hiagent_api/workflow.py`
- 可直接运行的示例：`libs/api/examples/workflow/run_workflow.py`

## 常见报错与排查

- 401/403：确认 AK/SK 与 endpoint/region 是否正确。
- 运行返回 failed：优先检查 `input_data` 是否为 JSON 字符串、字段名是否与工作流入参一致。
- 一直 processing：改用异步模式并轮询 `query_workflow_status`，同时打印 `run_id` 便于定位。

