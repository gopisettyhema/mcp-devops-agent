from fastapi import FastAPI
from pydantic import BaseModel
from app.agent import DevOpsAgent
from fastapi.responses import HTMLResponse

app = FastAPI()
agent = DevOpsAgent()

class Query(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "MCP DevOps Agent Running"}

@app.post("/chat")
def chat(query: Query):
    try:
        response = agent.handle_query(query.question)
        return {"response": response}
    except Exception as e:
        import traceback
        return {
            "response": f"Error: {str(e)}",
            "details": traceback.format_exc()
        }

@app.get("/ui", response_class=HTMLResponse)
def ui():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>MCP DevOps AI Agent</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #343541;
            color: white;
            margin: 0;
        }

        .chat-container {
            max-width: 800px;
            margin: auto;
            padding: 20px;
        }

        .chat-box {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-bottom: 80px;
        }

        .message {
            padding: 12px;
            border-radius: 10px;
            max-width: 75%;
            white-space: pre-wrap;
        }

        .user {
            align-self: flex-end;
            background-color: #10a37f;
        }

        .bot {
            align-self: flex-start;
            background-color: #444654;
        }

        .input-box {
            position: fixed;
            bottom: 0;
            width: 100%;
            background: #40414f;
            padding: 15px;
            display: flex;
            gap: 10px;
        }

        input {
            flex: 1;
            padding: 10px;
            border-radius: 5px;
            border: none;
            font-size: 16px;
        }

        button {
            padding: 10px 20px;
            border: none;
            background-color: #10a37f;
            color: white;
            border-radius: 5px;
            cursor: pointer;
        }

        button:hover {
            background-color: #0e8c6a;
        }

        .loader {
            font-style: italic;
            opacity: 0.7;
        }
    </style>
</head>
<body>

<div class="chat-container">
    <h2>🤖 MCP DevOps AI Agent</h2>

    <div id="chat" class="chat-box"></div>
</div>

<div class="input-box">
    <input id="question" placeholder="Ask something..." />
    <button onclick="sendQuery()">Send</button>
</div>

<script>
    async function sendQuery() {
        const input = document.getElementById("question");
        const chat = document.getElementById("chat");

        const userText = input.value;
        if (!userText) return;

        // Add user message
        const userMsg = document.createElement("div");
        userMsg.className = "message user";
        userMsg.innerText = userText;
        chat.appendChild(userMsg);

        input.value = "";

        // Loader
        const loader = document.createElement("div");
        loader.className = "message bot loader";
        loader.innerText = "Thinking...";
        chat.appendChild(loader);

        chat.scrollTop = chat.scrollHeight;

        try {
            const res = await fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ question: userText })
            });

            const data = await res.json();

            loader.remove();

            const botMsg = document.createElement("div");
            botMsg.className = "message bot";
            botMsg.innerText = data.response;

            chat.appendChild(botMsg);
            chat.scrollTop = chat.scrollHeight;

        } catch (error) {
            loader.innerText = "Error occurred";
        }
    }
</script>

</body>
</html>
"""