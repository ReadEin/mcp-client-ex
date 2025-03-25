import asyncio
import json
import textwrap
from dotenv import load_dotenv
import os
from openai import OpenAI
from openai.types.shared_params.function_definition import FunctionDefinition
from lib.mcp_client import MCPClient

load_dotenv()

API_URL = "https://api.openai.com/v1/chat/completions"
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-mini-2024-07-18"
SYSTEM_PROMPT = textwrap.dedent(
    """
    You are a helpful assistant.
    you can use tools to help the user.
    you must use tools that are available.
    don't use tools if you don't need to.
    """
)

class McpOpenAIClient(MCPClient):
    def __init__(self):
        super().__init__()
        self._api_key = API_KEY
        self._api_url = API_URL
        self._model = MODEL
    
    async def connect_to_server(self, server_name: str):
        await super().connect_to_server(server_name)
    
    def process_query(self, query: str) -> dict:
        client = OpenAI(api_key=self._api_key)
        tools = [
            FunctionDefinition(
                name=tool.name,
                description=tool.description, 
                parameters = {
                    "type": "object",
                    "properties": tool.inputSchema['properties'],
                    "required": tool.inputSchema['required']
                }
            ) for tool in self.tools
        ]
        response = client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": query}
            ],
            functions=tools,
            function_call="auto",
        )
        if(response.choices[0].finish_reason == "function_call"):
            openai_original_function_call = response.choices[0].message.function_call
            tool_name = openai_original_function_call.name
            tool_args = json.loads(openai_original_function_call.arguments)

            return {
                "tool_name": tool_name,
                "tool_args": tool_args, 
                "content": None
            }
        else:
            return {
                "tool_name": None,
                "tool_args": None,
                "content": response.choices[0].message.content
            }
    
    async def cleanup(self):
        await super().cleanup()

    async def process_loop(self):
        while True:
            print("Enter a query: ")
            query = input()
            result = self.process_query(query)
            if(result["tool_name"]):
                print(f"Tool name: {result['tool_name']}, Tool args: {result['tool_args']}")
                print("수행하시겠습니까? (y/n)")
                if(input() == "y"):
                    tool_result = await self.session.call_tool(result['tool_name'], result['tool_args'])
                    print(f"Tool result: {tool_result}")
            else:
                print(result["content"])

async def main():
    client = McpOpenAIClient()
    await client.connect_to_server("mcp-server")
    print(client.tools)
    await client.process_loop()

if __name__ == "__main__":
    asyncio.run(main())
