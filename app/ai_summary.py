import google.generativeai as genai
import os

print(os.getenv("GEMINI_API_KEY"))  # debug

# Configure API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def summarize_issues(issues):
    if not issues:
        return "No issues to summarize."

    issue_text = ""
    for issue in issues:
        issue_text += f"- {issue['title']} ({issue['state']})\n"

    prompt = f"""
    You are a DevOps assistant.

    Analyze the following GitHub issues and provide a short summary:
    - Total issues
    - How many are open vs closed
    - General theme (bugs, features, etc.)

    Issues:
    {issue_text}
    """

    model = genai.GenerativeModel("gemini-pro")

    response = model.generate_content(prompt)

    return response.text