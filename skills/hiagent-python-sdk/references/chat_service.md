---
title: ChatService
---

# ChatService

## 使用场景

- 把 HiAgent 应用当作对话式能力使用：创建会话、发起对话、获取消息列表、停止/清理消息。
- 需要阻塞式拿到最终答案：`chat_blocking(...)`。
- 需要流式增量输出（SSE）：`chat_streaming(...)`。
- 需要会话管理能力：`create_conversation(...)`、`get_conversation_list(...)`、`get_conversation_messages(...)` 等。
- 需要通过 webhook 触发事件：`event_trigger_webhook(...)`。

## 鉴权与配置

- Top/OpenAPI（默认）：通过 `VOLC_ACCESSKEY` / `VOLC_SECRETKEY` 做签名鉴权；构造 `ChatService(endpoint, region)` 即可。
- App API（部分接口使用）：需要先设置 `set_app_base_url(...)`，并在调用时传 `app_key`（会写入 `Apikey` header）。
- Webhook：调用 `event_trigger_webhook(...)` 需要 `Authorization: Bearer <webhook_token>`（不要把真实 token 写进日志或对话）。

## 最小用法

### 1) 创建会话

```python
import os
from dotenv import load_dotenv

from hiagent_api.chat import ChatService
from hiagent_api.chat_types import CreateConversationRequest

load_dotenv()

svc = ChatService(endpoint=os.getenv("HIAGENT_TOP_ENDPOINT") or "", region="cn-north-1")
svc.set_app_base_url(os.getenv("HIAGENT_APP_BASE_URL") or "")

app_key = os.getenv("HIAGENT_AGENT_APP_KEY") or "<HIAGENT_AGENT_APP_KEY>"

resp = svc.create_conversation(
    app_key,
    CreateConversationRequest(
        app_key=app_key,
        inputs={"name": "assistant"},
        user_id="test",
    ),
)
print(resp)
```

### 2) 阻塞式对话（拿最终答案）

```python
import os
from dotenv import load_dotenv

from hiagent_api.chat import ChatService
from hiagent_api.chat_types import ChatRequest

load_dotenv()

svc = ChatService(endpoint=os.getenv("HIAGENT_TOP_ENDPOINT") or "", region="cn-north-1")
svc.set_app_base_url(os.getenv("HIAGENT_APP_BASE_URL") or "")

app_key = os.getenv("HIAGENT_AGENT_APP_KEY") or "<HIAGENT_AGENT_APP_KEY>"
conversation_id = "<APP_CONVERSATION_ID>"

resp = svc.chat_blocking(
    app_key,
    ChatRequest(
        app_key=app_key,
        app_conversation_id=conversation_id,
        query="你好",
        response_mode="blocking",
        user_id="test",
    ),
)
print(resp)
```

### 3) 流式对话（SSE）

```python
import os
from dotenv import load_dotenv

from hiagent_api.chat import ChatService
from hiagent_api.chat_types import ChatRequest

load_dotenv()

svc = ChatService(endpoint=os.getenv("HIAGENT_TOP_ENDPOINT") or "", region="cn-north-1")
svc.set_app_base_url(os.getenv("HIAGENT_APP_BASE_URL") or "")

app_key = os.getenv("HIAGENT_AGENT_APP_KEY") or "<HIAGENT_AGENT_APP_KEY>"
conversation_id = "<APP_CONVERSATION_ID>"

events = svc.chat_streaming(
    app_key,
    ChatRequest(
        app_key=app_key,
        app_conversation_id=conversation_id,
        query="请流式回答",
        response_mode="streaming",
        user_id="test",
    ),
)

for e in events:
    print(e)
```

## 关键类型与入口文件

- 请求/响应类型：`libs/api/hiagent_api/chat_types.py`
- 主要接口实现：`libs/api/hiagent_api/chat.py`
- 如果只想快速跑通：优先参考仓库根目录 `README.md` / `README.zh_CN.md` 的 Quick Start。

## 常见报错与排查

- 401/403：确认 `VOLC_ACCESSKEY` / `VOLC_SECRETKEY` 生效；检查 `HIAGENT_TOP_ENDPOINT` 与 `region` 是否匹配环境。
- App API 相关错误：确认已 `set_app_base_url()` 且传入正确的 `app_key`（header `Apikey`）。
- 流式无输出/中途断开：先确认网络到 endpoint 可达，再把 `chat_streaming` 返回事件逐条打印出来定位是哪个 event 停止。

