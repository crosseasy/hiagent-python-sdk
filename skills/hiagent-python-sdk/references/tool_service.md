---
title: ToolService
---

# ToolService

## 使用场景

- 从工作空间中拉取“归档工具”定义，并在代码里调用执行（把工具当成函数）。
- 典型链路：`get_archived_tool(...)` 取到 `plugin_id` -> `exec_archived_tool(...)` 执行得到输出。

## 鉴权与配置

- Top/OpenAPI：通过 `VOLC_ACCESSKEY` / `VOLC_SECRETKEY` 做签名鉴权；构造 `ToolService(endpoint, region)` 即可。
- 部分场景可能走 App API：需要先设置 `set_app_base_url(...)` 并传 `app_key`（以实际接口为准）。

## 最小用法

```python
import os
from dotenv import load_dotenv

from hiagent_api.tool import ToolService
from hiagent_api.tool_types import ExecArchivedToolRequest, GetArchivedToolRequest

load_dotenv()

svc = ToolService(endpoint=os.getenv("HIAGENT_TOP_ENDPOINT") or "", region="cn-north-1")

workspace_id = "<WORKSPACE_ID>"
tool_id = "<TOOL_ID>"

tool = svc.get_archived_tool(GetArchivedToolRequest(workspace_id=workspace_id, id=tool_id))

resp = svc.exec_archived_tool(
    ExecArchivedToolRequest(
        workspace_id=workspace_id,
        plugin_id=tool.plugin_id,
        tool_id=tool_id,
        config="",
        input_data='{"query":"llm"}',
    )
)
print(resp)
```

## 关键类型与入口文件

- 请求/响应类型：`libs/api/hiagent_api/tool_types.py`
- 主要接口实现：`libs/api/hiagent_api/tool.py`
- 可直接运行的示例：`libs/api/examples/tool/get_and_exec_tool.py`

## 常见报错与排查

- 取不到工具：确认 `workspace_id/tool_id` 是否属于同一工作空间，且工具已归档可访问。
- exec 返回 success=false：检查 `input_data` 是否为 JSON 字符串，字段是否与工具 `input_schema` 匹配。
- 需要临时授权：使用 `config` 字段传入插件临时授权信息（不在对话里粘贴真实授权内容）。

