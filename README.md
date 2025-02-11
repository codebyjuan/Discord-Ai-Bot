# 🤖 Discord AI Chatbot (Powered by Gemini AI)

A **Discord bot** that interacts with users using **Google Gemini AI**, maintaining conversation history and responding intelligently. **Designed for Replit**, but can also run locally.

---

## 📌 Features
✅ AI-powered responses using **Google Gemini API**  
✅ **Memory persistence** (remembers last 20 interactions)  
✅ **Mention-triggered responses** (`@bot`) or `!chat` command  
✅ **Message splitting** to fit within Discord’s 2000-character limit  
✅ **Fully compatible with Replit deployment**  

---

## 🚀 Setup & Installation

### **1️⃣ Fork or Clone the Repository**
```sh
git clone <repo-url>
cd <repo-folder>
```

### **2️⃣ Set Up Environment Variables**
Since this project is designed for **Replit**, you need to add your API keys in **Secrets (Environment Variables)**:

| Key             | Value                           |
|----------------|--------------------------------|
| `DISCORD_TOKEN` | Your Discord bot token        |
| `GEMINI_API_KEY` | Your Google Gemini API key   |

Alternatively, if running **locally**, create a `.env` file in the project root:
```env
DISCORD_TOKEN=your_discord_bot_token
GEMINI_API_KEY=your_google_gemini_api_key
```

---

### **3️⃣ Install Dependencies**
For **Replit**, dependencies are automatically managed via `pyproject.toml`.  
If running **locally**, install them manually:
```sh
pip install -r requirements.txt
```
or using Poetry:
```sh
poetry install
```

---

### **4️⃣ Run the Bot**
#### **On Replit:**  
- Simply **click "Run"** in Replit’s interface.

#### **Locally (if not using Replit):**  
```sh
python main.py
```

---

## 📡 Commands & Usage

### **Trigger the AI**
You can chat with the bot using:  
- `!chat <your message>`  
- Mentioning the bot: `@Bot <your message>`  

### **Examples**
```
User: !chat How does AI work?
Bot: AI works by using machine learning models to process and analyze data...
```

---

## 📝 Memory System
- The bot **remembers the last 20 messages** per user.
- Memory is stored in **`memory.json`** and persists across reboots.
- Conversations are stored in this format:
  ```json
  {
    "user_id": [
      "You: How does AI work?",
      "AI: AI is a technology that..."
    ]
  }
  ```

---

## 🛠 Project Structure
```
/project-root
│── main.py                # Main bot script
│── memory.json            # Stores user chat history
│── .env                   # Environment variables (Discord & Gemini API keys)
│── .replit                # Replit-specific configuration
│── generated-icon.png     # Bot profile icon (if used)
│── requirements.txt       # Dependencies (if applicable)
│── pyproject.toml         # Poetry dependency management (for Replit)
│── uv.lock                # Dependency lock file (Replit)
```
