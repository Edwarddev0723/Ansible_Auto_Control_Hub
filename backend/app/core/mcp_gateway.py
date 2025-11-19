"""
MCP Ollama Gateway - 整合 Ollama 與 Ansible MCP Server
將自然語言轉換為 Ansible 操作
"""
import asyncio
import json
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import httpx


class MCPOllamaGateway:
    """MCP + Ollama 整合閘道"""
    
    def __init__(
        self,
        ollama_url: str = "http://localhost:11434",
        model: str = "gpt-oss:20b",
        mcp_server_path: Optional[str] = None,
        ansible_project_root: Optional[str] = None,
        ansible_inventory: Optional[str] = None,
    ):
        self.ollama_url = ollama_url
        self.model = model
        self.mcp_server_path = mcp_server_path or self._get_default_mcp_path()
        self.ansible_project_root = ansible_project_root or self._get_default_project_root()
        self.ansible_inventory = ansible_inventory or self._get_default_inventory()
        
        # MCP 工具定義
        self.available_tools = self._load_mcp_tools()
        
    def _get_default_mcp_path(self) -> str:
        """獲取預設 MCP Server 路徑"""
        # 假設當前檔案在 backend/app/core/mcp_gateway.py
        # project_root 是 backend/.. -> Ansible_Auto_Control_Hub
        project_root = Path(__file__).parent.parent.parent.parent
        return str(project_root / "mcp-ansible" / "src" / "ansible_mcp" / "server.py")
    
    def _get_default_project_root(self) -> str:
        """獲取預設 Ansible 專案路徑"""
        project_root = Path(__file__).parent.parent.parent.parent
        # 優先使用 Infra_owner_demo
        infra_demo = project_root / "Infra_owner_demo" / "infra" / "ansible"
        if infra_demo.exists():
            return str(infra_demo)
        # 回退到 ansible_projects
        return str(project_root / "ansible_projects" / "infra_owner_deploy")
    
    def _get_default_inventory(self) -> str:
        """獲取預設 inventory 路徑"""
        return str(Path(self.ansible_project_root) / "inventory.ini")
    
    def _load_mcp_tools(self) -> List[Dict[str, Any]]:
        """載入 MCP 工具定義（符合 Ollama function calling 格式）"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "ansible_inventory",
                    "description": "顯示 Ansible inventory 中的所有主機和群組。用於查看可用的伺服器列表。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "inventory": {
                                "type": "string",
                                "description": "Inventory 檔案路徑（可選，預設使用專案 inventory）"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "ansible_ping",
                    "description": "測試 Ansible 主機連通性。檢查主機是否可以連接和執行命令。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "host_pattern": {
                                "type": "string",
                                "description": "主機模式，如 'all'（所有主機）、'web'（web 群組）、'localhost'（本機）"
                            }
                        },
                        "required": ["host_pattern"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "validate_playbook",
                    "description": "驗證 Ansible playbook 語法是否正確。在執行部署前檢查 playbook 語法。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "playbook_path": {
                                "type": "string",
                                "description": "Playbook 檔案路徑，如 'deploy_demo.yaml' 或完整路徑"
                            }
                        },
                        "required": ["playbook_path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "ansible_playbook",
                    "description": "執行 Ansible playbook 進行部署或配置。可選擇 check 模式（試運行）或實際執行。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "playbook_path": {
                                "type": "string",
                                "description": "Playbook 檔案路徑"
                            },
                            "check": {
                                "type": "boolean",
                                "description": "是否為 check 模式（試運行，不實際變更）。預設 false。"
                            },
                            "verbose": {
                                "type": "integer",
                                "description": "詳細程度 0-3，數字越大越詳細。預設 1。"
                            }
                        },
                        "required": ["playbook_path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_playbooks",
                    "description": "列出專案中所有可用的 playbooks。查看有哪些部署腳本可以執行。",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "ansible_galaxy_install",
                    "description": "安裝 Ansible Galaxy collection 或 role。用於安裝 playbook 所需的依賴。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "collection": {
                                "type": "string",
                                "description": "Collection 名稱，如 'community.docker'"
                            },
                            "requirements_file": {
                                "type": "string",
                                "description": "requirements.yml 路徑（如果使用檔案安裝）"
                            }
                        }
                    }
                }
            }
        ]
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        處理聊天請求，支援 Ollama function calling
        """
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                # 準備 Ollama 請求
                payload = {
                    "model": self.model,
                    "messages": messages,
                    "stream": stream,
                    "tools": self.available_tools,
                }
                
                response = await client.post(
                    f"{self.ollama_url}/api/chat",
                    json=payload
                )
                
                if response.status_code != 200:
                    return {
                        "role": "assistant",
                        "content": f"Ollama 服務錯誤: {response.text}",
                        "tool_calls": []
                    }
                
                result = response.json()
                message = result.get("message", {})
                
                # 檢查是否有工具調用
                tool_calls = message.get("tool_calls", [])
                
                if tool_calls:
                    # 執行所有工具調用
                    tool_results = []
                    for tool_call in tool_calls:
                        func = tool_call.get("function", {})
                        tool_name = func.get("name")
                        tool_args = func.get("arguments", {})
                        
                        print(f"[MCP Gateway] 執行工具: {tool_name}, 參數: {tool_args}")
                        
                        # 執行 MCP 工具
                        result = await self._execute_mcp_tool(tool_name, tool_args)
                        tool_results.append({
                            "tool": tool_name,
                            "arguments": tool_args,
                            "result": result
                        })
                    
                    # 將工具結果加入訊息歷史
                    messages.append({
                        "role": "tool",
                        "content": json.dumps(tool_results, ensure_ascii=False, indent=2)
                    })
                    
                    # 再次調用 Ollama 獲取總結
                    final_response = await client.post(
                        f"{self.ollama_url}/api/chat",
                        json={
                            "model": self.model,
                            "messages": messages,
                            "stream": False
                        }
                    )
                    
                    if final_response.status_code == 200:
                        final_result = final_response.json()
                        return {
                            "role": "assistant",
                            "content": final_result.get("message", {}).get("content", ""),
                            "tool_calls": tool_results
                        }
                
                # 無工具調用，直接返回
                return {
                    "role": "assistant",
                    "content": message.get("content", ""),
                    "tool_calls": []
                }
                
        except httpx.ConnectError:
            return {
                "role": "assistant",
                "content": "❌ 無法連接到 Ollama 服務。請確認:\n1. Ollama 已啟動 (ollama serve)\n2. 模型已下載 (ollama pull qwen2.5:7b)",
                "tool_calls": []
            }
        except Exception as e:
            return {
                "role": "assistant",
                "content": f"❌ 處理請求時發生錯誤: {str(e)}",
                "tool_calls": []
            }
    
    async def _execute_mcp_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """執行 MCP 工具"""
        try:
            # 設定環境變數
            env = os.environ.copy()
            venv_path = Path(self.mcp_server_path).parent.parent.parent / ".venv"
            env.update({
                "PYTHONPATH": str(Path(self.mcp_server_path).parent.parent),
                "MCP_ANSIBLE_PROJECT_ROOT": self.ansible_project_root,
                "MCP_ANSIBLE_INVENTORY": self.ansible_inventory,
                "MCP_ANSIBLE_PROJECT_NAME": "infra_owner_demo",
            })
            
            venv_python = venv_path / "bin" / "python3"
            
            # 注入預設參數
            if tool_name in ["ansible_ping", "validate_playbook", "ansible_playbook"]:
                if "inventory" not in arguments:
                    arguments["inventory"] = self.ansible_inventory
                if "project_root" not in arguments:
                    arguments["project_root"] = self.ansible_project_root
            
            if tool_name == "ansible_galaxy_install" and "project_root" not in arguments:
                arguments["project_root"] = self.ansible_project_root
            
            # 構建調用腳本
            script = f"""
import sys
import json
from ansible_mcp.server import (
    ansible_inventory,
    ansible_ping,
    validate_playbook,
    ansible_playbook,
    project_playbooks,
    galaxy_install
)

tool_name = {repr(tool_name)}
arguments = {repr(arguments)}

try:
    if tool_name == "ansible_inventory":
        result = ansible_inventory(**arguments)
    elif tool_name == "ansible_ping":
        result = ansible_ping(**arguments)
    elif tool_name == "validate_playbook":
        result = validate_playbook(**arguments)
    elif tool_name == "ansible_playbook":
        result = ansible_playbook(**arguments)
    elif tool_name == "list_playbooks":
        result = project_playbooks(**arguments)
    elif tool_name == "ansible_galaxy_install":
        result = galaxy_install(**arguments)
    else:
        result = {{"error": f"Unknown tool: {{tool_name}}"}}
    
    print(json.dumps(result, ensure_ascii=False))
except Exception as e:
    import traceback
    print(json.dumps({{"error": str(e), "traceback": traceback.format_exc()}}), file=sys.stderr)
    sys.exit(1)
"""
            
            # 執行
            process = await asyncio.create_subprocess_exec(
                str(venv_python),
                "-c",
                script,
                env=env,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "執行失敗"
                print(f"[MCP Gateway] 工具執行失敗: {error_msg}")
                return {
                    "success": False,
                    "error": error_msg
                }
            
            # 解析結果
            try:
                result = json.loads(stdout.decode())
                return {
                    "success": True,
                    "data": result
                }
            except json.JSONDecodeError:
                return {
                    "success": True,
                    "data": {"output": stdout.decode()}
                }
                
        except Exception as e:
            print(f"[MCP Gateway] 執行工具異常: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def check_health(self) -> Dict[str, Any]:
        """檢查服務健康狀態"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                # 檢查 Ollama
                try:
                    ollama_response = await client.get(f"{self.ollama_url}/api/tags")
                    ollama_ok = ollama_response.status_code == 200
                    models = ollama_response.json().get("models", []) if ollama_ok else []
                    model_available = any(self.model in m.get("name", "") for m in models)
                except:
                    ollama_ok = False
                    model_available = False
                
                # 檢查 MCP Server
                mcp_ok = Path(self.mcp_server_path).exists()
                
                # 檢查 Ansible 專案
                ansible_ok = Path(self.ansible_project_root).exists()
                inventory_ok = Path(self.ansible_inventory).exists()
                
                status = "healthy" if (ollama_ok and model_available and mcp_ok and ansible_ok) else "degraded"
                
                return {
                    "status": status,
                    "ollama": {
                        "status": "connected" if ollama_ok else "disconnected",
                        "url": self.ollama_url,
                        "model": self.model,
                        "model_available": model_available
                    },
                    "mcp_server": {
                        "status": "available" if mcp_ok else "missing",
                        "path": self.mcp_server_path
                    },
                    "ansible": {
                        "status": "available" if (ansible_ok and inventory_ok) else "missing",
                        "project_root": self.ansible_project_root,
                        "inventory": self.ansible_inventory,
                        "inventory_exists": inventory_ok
                    },
                    "tools_count": len(self.available_tools)
                }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }


# 單例
_gateway_instance: Optional[MCPOllamaGateway] = None


def get_gateway() -> MCPOllamaGateway:
    """獲取 Gateway 單例"""
    global _gateway_instance
    if _gateway_instance is None:
        _gateway_instance = MCPOllamaGateway(
            ollama_url=os.getenv("OLLAMA_URL", "http://localhost:11434"),
            model=os.getenv("OLLAMA_MODEL", "gpt-oss:20b")
        )
    return _gateway_instance
