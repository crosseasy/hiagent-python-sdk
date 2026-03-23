---
title: ObserveService
---

# ObserveService

## 使用场景

- 生成 Observe API Token：用于 Trace/观测相关接口访问（业务 token，不是签名用的 AK/SK）。
- 查询 Trace spans：用于排查一次运行的链路、耗时、token 使用等（以 ListTraceSpans 为入口）。

## 鉴权与配置

- Top/OpenAPI：通过 `VOLC_ACCESSKEY` / `VOLC_SECRETKEY` 做签名鉴权；构造 `ObserveService(endpoint, region)` 即可。
- `CreateApiToken` 返回的 `Token` 是后续 Observe 相关调用的业务 token（有效期见 `ExpiresIn`），不要写进代码仓库或日志。

## 最小用法

### 1) 创建 API Token

```python
import os
from dotenv import load_dotenv

from hiagent_api.observe import ObserveService

load_dotenv()

svc = ObserveService(endpoint=os.getenv("HIAGENT_TOP_ENDPOINT") or "", region="cn-north-1")

resp = svc.CreateApiToken(
    {
        "WorkspaceID": os.getenv("WORKSPACE_ID") or "<WORKSPACE_ID>",
    }
)
print(resp)
```

### 2) 查询 Trace Spans（示例结构）

```python
import os
from dotenv import load_dotenv

from hiagent_api.observe import ObserveService

load_dotenv()

svc = ObserveService(endpoint=os.getenv("HIAGENT_TOP_ENDPOINT") or "", region="cn-north-1")

resp = svc.ListTraceSpans(
    {
        "WorkspaceID": os.getenv("WORKSPACE_ID") or "<WORKSPACE_ID>",
        "PageSize": 10,
        "LastID": "",
        "Sort": [{"SortOrder": "Desc", "SortBy": "StartTime"}],
    }
)
print(resp)
```

## 关键类型与入口文件

- 类型定义：`libs/api/hiagent_api/observe_types.py`
- 主要接口实现：`libs/api/hiagent_api/observe.py`
- 可直接运行的示例：
  - `libs/api/examples/observe/create_api_token.py`
  - `libs/api/examples/observe/list_trace_spans.py`

## 常见报错与排查

- CreateApiToken 报错：确认 `WorkspaceID` 存在且调用账号有该工作空间权限。
- ListTraceSpans 返回空：先缩小时间范围/排序字段（以服务端支持为准），并确认 Trace 已上报到对应 workspace。

