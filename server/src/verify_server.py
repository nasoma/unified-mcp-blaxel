import sys
import os
import asyncio

# Add the src directory to the python path so absolute imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../server/src")))

async def main():
    try:
        # Import directly as if running from src
        import server
        from server import mcp
        print("Server imported successfully.")
        
        tools = await mcp.list_tools()
        print(f"Registered tools: {[t.name for t in tools]}")
        
        resources = await mcp.list_resources()
        print(f"Registered resources: {[r.uri for r in resources]}")
        
        prompts = await mcp.list_prompts()
        print(f"Registered prompts: {[p.name for p in prompts]}")

    except Exception as e:
        print(f"Error importing server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
