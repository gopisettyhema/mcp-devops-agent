import re
from app.ai_summary import summarize_issues
from app.mcp_client import MCPClient


class DevOpsAgent:

    def __init__(self):
        self.mcp = MCPClient()

    def extract_repo_from_query(self, query: str):
        """
        Extract repository in format username/repo from user input
        Supports flexible natural language inputs
        """

        patterns = [
            r'repo\s+([\w\-]+/[\w\-]+)',
            r'issues\s+for\s+([\w\-]+/[\w\-]+)',
            r'github\s+([\w\-]+/[\w\-]+)',
            r'([\w\-]+/[\w\-]+)'  # fallback
        ]

        for pattern in patterns:
            match = re.search(pattern, query.lower())
            if match:
                return match.group(1)

        return None

    def handle_query(self, user_input: str):
        """
        Main handler for user queries
        """

        # Check if query is related to GitHub issues
        if "github" in user_input.lower() or "issues" in user_input.lower():

            repo = self.extract_repo_from_query(user_input)

            if not repo:
                return "Please mention repository like: username/repo (e.g., octocat/Hello-World)"

            # Call MCP tool
            data = self.mcp.call_tool("github_issues", {"repo": repo})

            # Handle errors from tool
            if isinstance(data, dict) and "error" in data:
                return f"GitHub Error: {data['error']}"

            return self.generate_response(repo, data)

        return "I can help with GitHub issues. Try: 'Show issues for octocat/Hello-World'"

def generate_response(self, repo: str, data):

    if not data:
        return f"No issues found for {repo}"

    # AI Summary
    summary = summarize_issues(data)

    response = f"📊 AI Summary for {repo}:\n\n{summary}\n\n"

    response += "📌 Recent Issues:\n"
    for issue in data:
        response += f"- {issue['title']} ({issue['state']})\n"

    return response