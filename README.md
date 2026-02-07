# 🏨 Full Stack Hotel AI Agent

**Deep Search System for Hotel Management Intelligence**

## 🚀 Quick Start

```bash
git clone https://github.com/nssuwan186-dev/fullstack-hotel-ai.git
cd fullstack-hotel-ai
cp .env.example .env
# Add your API keys to .env file
python hotel_ai_server.py
```

## 📚 API Endpoints

### 🔍 Health Check
```bash
curl http://localhost:8888/health
```

### 🎯 Deep Search
```bash
curl -X POST http://localhost:8888/deep-search \
  -H "Content-Type: application/json" \
  -d '{"query": "booking room 101 tomorrow"}'
```

### 📊 Analytics
```bash
curl http://localhost:8888/analytics
```

### 📚 Documentation
Visit: http://localhost:8888/docs

## 🎯 Features

- ✅ **Multi-LLM Support** - GROQ + Gemini
- ✅ **Deep Search System** - Multi-layer analysis
- ✅ **Hotel Intelligence** - Real-time insights
- ✅ **Real-time API** - Fast responses
- ✅ **Complete Documentation** - Ready to use

## 🔧 Configuration

Add your API keys to `.env` file:
```bash
GROQ_API_KEY=your_groq_key
GEMINI_API_KEY=your_gemini_key
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key
```

## 🏆 Project Status: ✅ PRODUCTION READY

**GitHub:** https://github.com/nssuwan186-dev/fullstack-hotel-ai
**API Version:** 4.5.0
**Status:** Active & Ready