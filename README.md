# 🤖 WhatsApp Bot Login (Python + Selenium)

A Python-based automation script that logs into [WhatsApp Web](https://web.whatsapp.com) using **Selenium**, with session reuse support and modular code design.

---

## 🧰 Features

- 🔐 **Login Automation** via phone number and QR code  
- 💾 **Session Persistence** to avoid repeated logins  
- 🧠 Modular structure for easy extensibility  
- 💻 Keeps browser open after login for manual use or further automation  
- 🌐 JavaScript integration via `whatsapp_agent.js` for advanced DOM interactions (optional)

---

## 📁 Project Structure

```
📦 project-root/
 ┣ 📂 .idea/               ← IDE settings (ignored by Git)
 ┣ 📂 __pycache__/         ← Python cache (ignored by Git)
 ┣ 📂 js/
 ┃ ┗ 📄 whatsapp_agent.js  ← Optional JS helpers for DOM interaction
 ┣ 📂 models/
 ┃ ┣ 📂 __pycache__/
 ┃ ┗ 📄 __init__.py        ← (Reserved for future models/data structures)
 ┣ 📄 login.py             ← Main WhatsApp login logic (QR/session handling)
 ┣ 📄 main.py              ← Entry point: prompts input & launches browser
 ┣ 📄 .gitignore           ← Ignores cache, sessions, envs, etc.
 ┣ 📄 .gitattributes
 ┗ 📄 README.md            ← You're reading it 😎
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/kianpaknemat/whatsapp-bot-login-python.git
cd whatsapp-bot-login-python
```

### 2. Install requirements

```bash
pip install selenium
```

If you prefer using a `requirements.txt`, create one with:

```
selenium>=4.0.0
```

### 3. Make sure [ChromeDriver](https://chromedriver.chromium.org/downloads) is installed  
It must match your Chrome version and be added to your system `PATH`.

---

## ⚙️ Usage

```bash
python main.py
```

You will be prompted to enter:

- **Country code** (e.g., `1` for US, `98` for Iran)  
- **Phone number** (without `+` or spaces)

The script will:

1. Open WhatsApp Web in a browser  
2. Load session if it exists (from `sessions/`)  
3. If not, show QR code for login  
4. Keep the browser open for manual use

---

## 🔌 JavaScript Integration (Optional)

The `js/whatsapp_agent.js` file is designed for advanced WhatsApp Web interactions:

- DOM manipulation  
- Message parsing  
- UI automation

You can inject it into the browser with Selenium if needed.

---

## ❗ Troubleshooting

- 🧩 **Browser won’t open?** → Check ChromeDriver installation and version  
- 🧩 **Session not loading?** → Delete the `sessions/` folder and try a fresh login  
- 🧩 **WhatsApp UI changed?** → Update element selectors in `login.py`

---

## 📜 License

MIT License – Use freely but **respect WhatsApp's Terms of Service**

---

## ✍️ Author

Made with ☕ by [Kian Paknemat](https://github.com/kianpaknemat)
