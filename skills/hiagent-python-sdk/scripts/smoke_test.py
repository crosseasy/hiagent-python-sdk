import os
import socket
from urllib.parse import urlparse

from dotenv import load_dotenv


def _require_env(name: str) -> str:
    v = os.getenv(name, "").strip()
    if not v:
        raise SystemExit(f"missing env: {name}")
    return v


def _check_dns(hostname: str) -> None:
    try:
        socket.getaddrinfo(hostname, None)
    except socket.gaierror as e:
        raise SystemExit(f"dns lookup failed: {hostname} ({e})")


def main() -> None:
    load_dotenv()

    endpoint = _require_env("HIAGENT_TOP_ENDPOINT")
    parsed = urlparse(endpoint)
    if not parsed.scheme or not parsed.hostname:
        raise SystemExit("invalid HIAGENT_TOP_ENDPOINT, expected full url like https://example.com")

    _require_env("VOLC_ACCESSKEY")
    _require_env("VOLC_SECRETKEY")

    _check_dns(parsed.hostname)

    from hiagent_api.chat import ChatService
    from hiagent_api.knowledgebase import KnowledgebaseService
    from hiagent_api.observe import ObserveService
    from hiagent_api.tool import ToolService
    from hiagent_api.workflow import WorkflowService

    region = os.getenv("HIAGENT_REGION", "cn-north-1")

    _ = ChatService(endpoint=endpoint, region=region)
    _ = WorkflowService(endpoint=endpoint, region=region)
    _ = ToolService(endpoint=endpoint, region=region)
    _ = KnowledgebaseService(endpoint=endpoint, region=region)
    _ = ObserveService(endpoint=endpoint, region=region)

    print("ok: env loaded, dns ok, services constructed")


if __name__ == "__main__":
    main()

