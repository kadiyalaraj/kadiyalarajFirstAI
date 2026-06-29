#!/usr/bin/env python3
import json
import os
import sys
from typing import Any, Dict, Generator


def send_message(message: Dict[str, Any]) -> None:
    payload = json.dumps(message, ensure_ascii=False).encode("utf-8")
    header = f"Content-Length: {len(payload)}\r\n\r\n".encode("ascii")
    sys.stdout.buffer.write(header)
    sys.stdout.buffer.write(payload)
    sys.stdout.buffer.flush()


def read_messages() -> Generator[Dict[str, Any], None, None]:
    while True:
        header_line = sys.stdin.buffer.readline()
        if not header_line:
            break
        if not header_line.startswith(b"Content-Length:"):
            continue

        length = int(header_line.decode("ascii").split(":", 1)[1].strip())
        blank_line = sys.stdin.buffer.readline()
        if blank_line != b"\r\n" and blank_line != b"\n":
            pass

        body = sys.stdin.buffer.read(length)
        if not body:
            break

        message = json.loads(body.decode("utf-8"))
        yield message


def build_tool_list() -> Dict[str, Any]:
    return {
        "tools": [
            {
                "name": "leanix_search_factsheet",
                "description": "Search a LeanIX factsheet by query string.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search term for the factsheet"}
                    },
                    "required": ["query"],
                },
            },
            {
                "name": "leanix_get_factsheet_by_id",
                "description": "Retrieve a LeanIX factsheet using a specific identifier.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "description": "LeanIX factsheet identifier"}
                    },
                    "required": ["id"],
                },
            },
        ]
    }


def handle_tool_call(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    base_url = os.getenv("LEANIX_BASE_URL", "<not-configured>")
    token = os.getenv("LEANIX_API_TOKEN", "<not-configured>")

    if name == "leanix_search_factsheet":
        query = arguments.get("query", "")
        text = (
            f"LeanIX search placeholder for '{query}'.\n"
            f"Configured base URL: {base_url}\n"
            f"Token configured: {'yes' if token != '<not-configured>' else 'no'}\n"
            "Replace the placeholder integration with your real LeanIX API call to enable live lookups."
        )
        return {"content": [{"type": "text", "text": text}]}

    if name == "leanix_get_factsheet_by_id":
        factsheet_id = arguments.get("id", "")
        text = (
            f"LeanIX factsheet lookup placeholder for id '{factsheet_id}'.\n"
            f"Configured base URL: {base_url}\n"
            f"Token configured: {'yes' if token != '<not-configured>' else 'no'}\n"
            "Replace the placeholder integration with your real LeanIX API call to enable live lookups."
        )
        return {"content": [{"type": "text", "text": text}]}

    raise ValueError(f"Unknown tool: {name}")


def main() -> None:
    for message in read_messages():
        if not isinstance(message, dict):
            continue

        msg_id = message.get("id")
        method = message.get("method")

        if method == "initialize":
            send_message(
                {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": "leanix-mcp-server", "version": "1.0.0"},
                        "capabilities": {"tools": {"listChanged": False}},
                    },
                }
            )
            continue

        if method == "notifications/initialized":
            continue

        if method == "tools/list":
            send_message({"jsonrpc": "2.0", "id": msg_id, "result": build_tool_list()})
            continue

        if method == "tools/call":
            params = message.get("params", {}) or {}
            name = params.get("name")
            arguments = params.get("arguments", {}) or {}
            try:
                result = handle_tool_call(name, arguments)
                send_message({"jsonrpc": "2.0", "id": msg_id, "result": result})
            except Exception as exc:  # pragma: no cover - simple error handling
                send_message({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32000, "message": str(exc)}})
            continue

        if method == "ping":
            send_message({"jsonrpc": "2.0", "id": msg_id, "result": {}})
            continue

        if method == "shutdown":
            send_message({"jsonrpc": "2.0", "id": msg_id, "result": {}})
            break

        send_message({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})


if __name__ == "__main__":
    main()
