from app.tools.github_tool import get_github_issues

class MCPClient:

    def call_tool(self, tool_name, params):
        if tool_name == "github_issues":
            return get_github_issues(params["repo"])

        return {"error": "Tool not found"}