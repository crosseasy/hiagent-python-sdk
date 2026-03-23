---
title: KnowledgebaseService
---

# KnowledgebaseService

## 使用场景

- 对知识库数据集进行检索（RAG 的 retrieval 部分）。
- 典型用法：指定 `workspace_id`、`dataset_ids`、`keywords`，拿回命中文档片段与分数。

## 鉴权与配置

- Top/OpenAPI：通过 `VOLC_ACCESSKEY` / `VOLC_SECRETKEY` 做签名鉴权；构造 `KnowledgebaseService(endpoint, region)` 即可。

## 最小用法

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

## 关键参数说明（高频）

- `dataset_ids`：一个或多个数据集 ID。
- `keywords`：检索 query 列表；可以用一个元素表示单 query。
- `top_k`：召回条数。
- `score_threshold`：过滤阈值。
- `retrieval_search_method`：检索策略（具体取值以服务端为准；示例里给出了 0/1/2）。
- `rerank_id`：可选的 rerank 配置。

## 关键类型与入口文件

- 请求/响应类型：`libs/api/hiagent_api/knowledgebase_types.py`
- 主要接口实现：`libs/api/hiagent_api/knowledgebase.py`
- 可直接运行的示例：`libs/api/examples/knowledgebase/query.py`

## 常见报错与排查

- 返回空结果：降低 `score_threshold`，确认 `dataset_ids` 正确且数据集有可检索内容。
- 参数不生效：优先对照 `knowledgebase_types.py` 的字段名与序列化别名，确保传参类型正确。

