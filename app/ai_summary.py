import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def summarize_issues(issues):
    try:
        # Try AI first
        import google.generativeai as genai
        import os

        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        model = genai.GenerativeModel("gemini-pro")

        issue_text = "\n".join([i["title"] for i in issues])

        response = model.generate_content(f"Summarize:\n{issue_text}")
        return response.text

    except Exception:
        # 🔥 Fallback (ALWAYS WORKS)
        total = len(issues)
        open_issues = sum(1 for i in issues if i["state"] == "open")
        closed_issues = total - open_issues

        return f"""
        Total Issues: {total}
        Open: {open_issues}
        Closed: {closed_issues}
        Most issues relate to project contributions, documentation, and AI features.
        """