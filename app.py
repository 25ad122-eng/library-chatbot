from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Simple keyword-based response logic (No NLP/LLM required)
def get_bot_response(user_input):
    text = user_input.lower()
    
    if any(word in text for word in ["hour", "timing", "open", "close", "time"]):
        return "Library Hours: Monday to Friday (8:00 AM – 8:00 PM), Saturday (9:00 AM – 5:00 PM), and Sunday (Closed)."
    elif any(word in text for word in ["borrow", "checkout", "issue", "take"]):
        return "You can borrow up to 5 books at a time for a standard duration of 14 days."
    elif any(word in text for word in ["fine", "late", "penalty", "overdue"]):
        return "The overdue fine is $0.50 per day for each book past its due date."
    elif any(word in text for word in ["renew", "extend"]):
        return "You can renew your books twice online through your library member portal."
    elif any(word in text for word in ["wifi", "internet", "connect"]):
        return "Free guest Wi-Fi is available throughout the building. Look for 'Library-Guest'."
    elif any(word in text for word in ["print", "scan", "copy"]):
        return "Printing and scanning stations are located on the 2nd floor ($0.10/page)."
    elif any(word in text for word in ["hi", "hello", "hey", "greetings"]):
        return "Hello! Welcome to the Public Library virtual assistant. How can I help you today?"
    else:
        return "I'm sorry, I didn't quite catch that. You can ask me about library hours, borrowing rules, fines, Wi-Fi, or printing services!"

# Single-page HTML template with embedded CSS and JavaScript
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Library Chatbot</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f7f6; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .chat-container { width: 400px; background: white; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); display: flex; flex-direction: column; overflow: hidden; }
        .chat-header { background: #2c3e50; color: white; padding: 15px; text-align: center; font-size: 18px; font-weight: bold; }
        .chat-box { flex: 1; padding: 15px; overflow-y: auto; height: 350px; display: flex; flex-direction: column; gap: 10px; }
        .message { padding: 10px 14px; border-radius: 15px; max-width: 75%; font-size: 14px; line-height: 1.4; }
        .user-message { background: #3498db; color: white; align-self: flex-end; border-bottom-right-radius: 2px; }
        .bot-message { background: #ecf0f1; color: #2c3e50; align-self: flex-start; border-bottom-left-radius: 2px; }
        .chat-input-area { display: flex; border-top: 1px solid #ddd; padding: 10px; background: #fff; }
        .chat-input-area input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 4px; outline: none; font-size: 14px; }
        .chat-input-area button { background: #2c3e50; color: white; border: none; padding: 10px 15px; margin-left: 8px; border-radius: 4px; cursor: pointer; }
        .chat-input-area button:hover { background: #34495e; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">📚 Library Assistant</div>
        <div class="chat-box" id="chatBox">
            <div class="message bot-message">Hello! Welcome to the Public Library virtual assistant. How can I help you today?</div>
        </div>
        <div class="chat-input-area">
            <input type="text" id="userInput" placeholder="Type your message..." onkeypress="handleKey(event)">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        async function sendMessage() {
            const inputField = document.getElementById("userInput");
            const chatBox = document.getElementById("chatBox");
            const text = inputField.value.trim();
            
            if (!text) return;

            // Append user message
            chatBox.innerHTML += `<div class="message user-message">${escapeHtml(text)}</div>`;
            inputField.value = "";
            chatBox.scrollTop = chatBox.scrollHeight;

            // Send to Flask backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            const data = await response.json();

            // Append bot response
            chatBox.innerHTML += `<div class="message bot-message">${escapeHtml(data.response)}</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function handleKey(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        function escapeHtml(text) {
            return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/chat", methods=["POST"])
def chat():
    user_data = request.get_json()
    user_message = user_data.get("message", "")
    bot_reply = get_bot_response(user_message)
    return jsonify({"response": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)