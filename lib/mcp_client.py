import asyncio
import json
import sys
from typing import List, Optional, Dict, Any
from contextlib import AsyncExitStack
 
from mcp import ClientSession, StdioServerParameters, Tool
from mcp.client.stdio import stdio_client
from mcp.types import Prompt

class MCPClient:
    session: Optional[ClientSession] = None
    exit_stack = AsyncExitStack()
    config: Optional[Dict[str, Any]] = None
    tools : List[Tool] = []
    prompts : List[Prompt] = []

    def __init__(self, config_path="mcp-config.json"):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.config_path = config_path
        self.config = self._load_config()
        if not self._check_config():
            print("유효한 mcp 서버 설정이 없습니다.")
            sys.exit(1)
    
    async def connect_to_server(self, server_name: str):
        server_params = self._build_server_params(server_name)
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        await self.session.initialize()
        await self._check_tools()
        await self._check_prompts()
        return True
    
    async def process_query(self, query: str) -> str:
        """Process a query using Claude and available tools"""
        return "mock response"
    
    def _load_config(self) -> Dict[str, Any]:
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"설정 파일 로드 중 오류 발생: {e}")
            return {"mcpServers": {}}

    def _check_config(self) -> bool:
        if not self.config or "mcpServers" not in self.config:
            print("유효한 mcp 서버 설정이 없습니다.")
            return False
        if not self.config["mcpServers"]:
            print("설정에 mcp 서버가 지정되지 않았습니다.")
            return False
        return True
    
    def _build_server_params(self, server_name: str) -> StdioServerParameters:
        server_config = self.config["mcpServers"][server_name]
        command = server_config.get("command")
        args = server_config.get("args", [])
        cwd = server_config.get("cwd")
        
        if not command:
            print("실행 명령어가 지정되지 않았습니다.")
            return False

        if isinstance(command, list):
            cmd = command[0]
            args = command[1:] + args
        else:
            cmd = command
        
        print(f"실행할 명령어: {cmd} {' '.join(args)}")
        print(f"작업 디렉토리: {cwd}")
        
        server_params = StdioServerParameters(
            command=cmd,  # 문자열로 전달
            args=args,    # 리스트로 전달
            env=None,
            cwd=cwd
        )
        return server_params

    async def _check_prompts(self) -> bool:
        response = await self.session.list_prompts()
        self.prompts = response.prompts
        print("\n=== 사용 가능한 프롬프트 목록 ===")
        for prompt in self.prompts:
            print(f"\n프롬프트 이름: {prompt.name}")
            print(f"설명: {prompt.description}")
            print(f"프롬프트 인자: {prompt.arguments}")
        return True
    
    async def _check_tools(self) -> bool:
        # List available tools
        response = await self.session.list_tools()
        self.tools = response.tools
        print("\n=== 사용 가능한 도구 목록 ===")
        for tool in self.tools:
            print(f"\n도구 이름: {tool.name}")
            print(f"설명: {tool.description}")
            print(f"입력 스키마: {tool.inputSchema}")
        return True

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

async def main():
    client = MCPClient()
    server_name = "mcp-server"  # 기본값 (또는 명령줄 인수에서 가져올 수 있음)
    
    try:
        success = await client.connect_to_server(server_name)
        if success:
            print("서버 연결 성공")
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())