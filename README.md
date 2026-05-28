# Code Council Bot

20 ta eng kuchli AI koderlari bitta Telegram botda! Barcha agentlar birgalikda muhokama qiladi, fikr almashadi va eng mukammal kodni yozadi.

## Arxitektura

```
Foydalanuvchi prompt yuboradi
         |
    [Code Council]
         |
    Round 1: Barcha agentlar kod yozadi
         |
    Round 2: Agentlar bir-birining kodini tahlil qiladi
         |
    Director: Eng yaxshi kodni tanlaydi va birlashtiradi
         |
    Mukammal kod qaytariladi
```

## 20 ta AI Agent

| # | Agent | Provider | Mutaxassislik |
|---|-------|----------|---------------|
| 1 | GPT-4o | OpenAI | Full-stack development |
| 2 | Codex | OpenAI | Tez kod generatsiya |
| 3 | GitHub Copilot | OpenAI | Kontekstli kod |
| 4 | Claude | Anthropic | Chuqur fikrlash |
| 5 | Devin | Anthropic | Avtonom dasturlash |
| 6 | Gemini Pro | Google | Katta loyihalar |
| 7 | DeepSeek Coder | DeepSeek | Algoritmlar |
| 8 | Codestral | Mistral | Tez va samarali |
| 9 | CodeLlama | Together | Kod to'ldirish |
| 10 | StarCoder | Together | Ko'p tillar |
| 11 | Llama 3.3 | Groq | Tez inference |
| 12 | Qwen Coder | OpenRouter | Web development |
| 13 | Cursor AI | OpenRouter | Refaktoring |
| 14 | Replit AI | OpenRouter | Full-stack |
| 15 | Codeium | OpenRouter | Kod qidirish |
| 16 | Phind | OpenRouter | Research |
| 17 | Tabnine | OpenRouter | Jamoa patternlari |
| 18 | JetBrains AI | OpenRouter | Java/Kotlin |
| 19 | Sourcegraph Cody | OpenRouter | Katta bazalar |
| 20 | Aider | OpenRouter | Git integratsiya |

## O'rnatish

### 1. Klonlash
```bash
git clone https://github.com/YOUR_USERNAME/code-council-bot.git
cd code-council-bot
```

### 2. Virtual muhit
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Konfiguratsiya
```bash
cp .env.example .env
```

`.env` faylini tahrirlab, kalitlarni qo'shing:

**Minimal sozlash (1 ta provider):**
```
TELEGRAM_BOT_TOKEN=your_token
GROQ_API_KEY=your_groq_key  # Bepul va tez!
```

**To'liq sozlash (barcha 20 agent):**
```
TELEGRAM_BOT_TOKEN=your_token
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
GOOGLE_API_KEY=your_key
DEEPSEEK_API_KEY=your_key
MISTRAL_API_KEY=your_key
TOGETHER_API_KEY=your_key
GROQ_API_KEY=your_key
OPENROUTER_API_KEY=your_key
```

> **Maslahat:** `OPENROUTER_API_KEY` bilan eng ko'p agent (9 ta!) faollashadi. `GROQ_API_KEY` bepul va juda tez ishlaydi.

### 4. Telegram bot yaratish
1. [@BotFather](https://t.me/BotFather) ga boring
2. `/newbot` buyrug'ini yuboring
3. Bot nomini kiriting
4. Tokenni `.env` fayliga yozing

### 5. Ishga tushirish
```bash
python main.py
```

## Buyruqlar

| Buyruq | Tavsif |
|--------|--------|
| `/start` | Botni boshlash |
| `/help` | Yordam |
| `/agents` | Barcha agentlar ro'yxati |
| `/status` | Bot holati |
| `/settings` | Sozlamalar |

## Foydalanish

Oddiy matn yuboring:
```
Python'da binary search tree yoz
```

Bot:
1. Barcha faol agentlar kod yozadi
2. Agentlar bir-birining kodini tahlil qiladi
3. Director eng yaxshi variantni tanlaydi
4. Mukammal kod sizga yuboriladi

## API kalitlarini olish

| Provider | Link | Narx |
|----------|------|------|
| Groq | [console.groq.com](https://console.groq.com) | Bepul |
| OpenRouter | [openrouter.ai](https://openrouter.ai) | Arzon |
| OpenAI | [platform.openai.com](https://platform.openai.com) | Pullik |
| Anthropic | [console.anthropic.com](https://console.anthropic.com) | Pullik |
| Google | [aistudio.google.com](https://aistudio.google.com) | Bepul tier bor |
| DeepSeek | [platform.deepseek.com](https://platform.deepseek.com) | Arzon |
| Mistral | [console.mistral.ai](https://console.mistral.ai) | Bepul tier bor |
| Together | [api.together.xyz](https://api.together.xyz) | Arzon |

## Texnologiyalar

- Python 3.11+
- python-telegram-bot
- aiohttp (async API calls)
- Multi-agent arxitektura
- Round-robin muhokama tizimi
- Director pattern
