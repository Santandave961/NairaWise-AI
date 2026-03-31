# 💰 Naira Wise AI — Nigerian Personal Finance Advisor

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-deployed-FF4B4B?style=flat-square&logo=streamlit)
![Gemini](https://img.shields.io/badge/Google%20Gemini-AI%20Powered-4285F4?style=flat-square&logo=google)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)

> An AI-powered personal finance chatbot built specifically for Nigerians. Ask anything about budgeting, saving, investing, and managing your money in Naira — powered by Google Gemini.

---

## 🌐 Live Demo

👉 **[Try Naira Wise AI on Streamlit Cloud](https://nairawise-ai-rnebh88pckjqg6wjkvcinf.streamlit.app)**

---

## 📌 Overview

Naira Wise AI is a conversational financial advisor designed for the Nigerian context. Unlike generic finance chatbots, it understands Nigerian financial realities — Naira inflation, local investment options, Nigerian bank products, and the everyday money challenges Nigerians face.

Whether you're asking how to save on a ₦150,000 salary, where to invest in Nigeria, or how to build an emergency fund, Naira Wise AI gives you practical, Nigeria-specific guidance.

---

## ✨ Features

- 💬 **Conversational AI Chatbot** — Natural language financial Q&A powered by Google Gemini
- 🇳🇬 **Nigeria-Specific Advice** — Tailored to Naira, Nigerian banks, and local investment options
- 📊 **Budget Planning Guidance** — Practical budgeting advice for Nigerian income levels
- 💹 **Investment Advice** — Info on Nigerian stocks, treasury bills, real estate, crypto and more
- 💡 **Savings Tips** — Strategies for saving in a high-inflation Nigerian economy
- 📈 **Exchange Rate Awareness** — Advice factoring in USD/NGN exchange rate realities
- ⚡ **Fast Responses** — Powered by Gemini Flash for near-instant answers

---

## 🧠 How It Works

1. User types a financial question in plain English (or Pidgin!)
2. The question is sent to Google Gemini with a Nigeria-specific system prompt
3. Gemini returns contextual, practical financial advice
4. Response is displayed in a clean chat interface

The system prompt instructs Gemini to always frame advice in the Nigerian context — referencing Naira amounts, Nigerian financial institutions, and local economic realities.

---

## 💬 Example Questions You Can Ask

- *"How do I budget on a ₦200,000 monthly salary?"*
- *"What are the best investment options in Nigeria right now?"*
- *"How do I start saving with PiggyVest or Cowrywise?"*
- *"Should I invest in Nigerian treasury bills or dollar savings?"*
- *"How do I build a 6-month emergency fund in Nigeria?"*
- *"What is the 50/30/20 budgeting rule and how do I apply it in Nigeria?"*

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **AI Model:** Google Gemini (via `google-genai` SDK)
- **Language:** Python
- **Deployment:** Streamlit Cloud
- **API:** Google Gemini API

---

## 🚀 Run Locally

```bash
# Clone the repo
git clone https://github.com/Santandave961/nairawise-ai.git
cd nairawise-ai

# Install dependencies
pip install -r requirements.txt

# Add your Gemini API key
# Create a .streamlit/secrets.toml file:
# GEMINI_API_KEY = "your-api-key-here"

# Run the app
streamlit run app.py
```

### Getting a Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com)
2. Click **Get API Key**
3. Create a new key and copy it
4. Add it to `.streamlit/secrets.toml` as shown above

---

## 📁 Project Structure

```
nairawise-ai/
│
├── app.py                      # Main Streamlit chatbot app
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── secrets.toml            # API keys (not committed to GitHub)
└── README.md                   # Project documentation
```

---

## ⚙️ Requirements

```
streamlit
google-genai
```

---

## 🔒 Security Note

Never commit your Gemini API key to GitHub. Always store it in:
- `.streamlit/secrets.toml` for local development
- Streamlit Cloud **Secrets** settings for deployment

Add `.streamlit/secrets.toml` to your `.gitignore`.

---

## 🔮 Future Improvements

- [ ] Add real-time NGN exchange rate display
- [ ] Nigerian stock market data integration (NGX)
- [ ] Savings goal tracker
- [ ] Multi-turn memory for longer conversations
- [ ] Voice input support
- [ ] Pidgin English mode 🇳🇬

---

## 👨‍💻 Built By

**Okparaji Wisdom**  
Data Science & AI Engineering Portfolio Project  
📍 Nigeria | 🎯 Targeting NYSC placement in Nigerian Fintech  

[![GitHub](https://img.shields.io/badge/GitHub-Santandave961-black?style=flat-square&logo=github)](https://github.com/Santandave961)

---

## 📄 License

MIT License — free to use, modify, and distribute.
