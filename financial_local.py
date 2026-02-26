import requests
import json
import re

# ============================================
# ПУНКТ 2: Промпт для финансового аналитика
# ============================================

FINANCIAL_ANALYST_PROMPT = """
Ты — профессиональный финансовый аналитик с опытом работы в инвестиционном банке.
Проанализируй новость и извлеки из неё структурированные финансовые метрики.

НОВОСТЬ:
{news_text}

ИЗВЛЕКИ СЛЕДУЮЩИЕ МЕТРИКИ И ВЕРНИ ИХ В ФОРМАТЕ JSON:

1. entity — информация о компании/активе:
   - name: название компании
   - ticker: биржевой тикер (если известен)
   - sector: сектор экономики

2. sentiment_analysis — анализ тональности:
   - score: число от -1.0 до 1.0
   - confidence: уверенность от 0 до 1
   - keywords: ключевые слова

3. market_impact — влияние на рынок:
   - level: "low", "medium" или "high"
   - time_horizon: "short_term", "medium_term" или "long_term"

4. fear_greed_analysis — уровень страха/жадности:
   - score: число от 0 до 100
   - driver: что вызывает этот уровень

5. trading_signals — торговые сигналы:
   - primary_signal: "bullish", "bearish" или "neutral"
   - signal_strength: число от 0 до 1
   - contrarian_potential: true/false

6. summary:
   - one_line: суть новости одной строкой
   - actionable_insight: конкретная рекомендация трейдеру

ВЕРНИ ТОЛЬКО JSON, БЕЗ ПОЯСНЕНИЙ.
"""

def analyze_news_local(news_text):
    """
    Отправляет запрос к локальному Ollama API
    """
    
    # Формируем полный промпт
    full_prompt = FINANCIAL_ANALYST_PROMPT.format(news_text=news_text)
    
    # Локальный адрес Ollama
    API_URL = "http://localhost:11434/api/generate"
    
    # Тело запроса
    payload = {
        "model": "mistral",
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 1500
        }
    }
    
    print("🔄 Отправляю запрос к локальной Ollama...")
    print("   (Это может занять 20-40 секунд)")
    
    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            text = result.get('response', '')
            
            # Ищем JSON в ответе
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                try:
                    analysis = json.loads(json_match.group())
                    print("✅ Анализ успешно получен!")
                    return analysis
                except json.JSONDecodeError as e:
                    print(f"❌ Ошибка парсинга JSON: {e}")
                    print("📄 Ответ модели:")
                    print(text[:500])
                    return None
            else:
                print("❌ Не удалось найти JSON в ответе")
                print("📄 Ответ модели:")
                print(text[:500])
                return None
        else:
            print(f"❌ Ошибка: {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Ошибка подключения к Ollama")
        print("   Убедитесь, что Ollama запущена (иконка в трее)")
        return None
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

import requests
import json
import re

# ============================================
# TASK 2: Financial Analyst Prompt
# ============================================

FINANCIAL_ANALYST_PROMPT = """
You are a professional financial analyst with experience in an investment bank.
Analyze the news and extract structured financial metrics from it.

NEWS:
{news_text}

EXTRACT THE FOLLOWING METRICS AND RETURN THEM IN JSON FORMAT:

1. entity — information about the company/asset:
   - name: company name
   - ticker: stock ticker (if known)
   - sector: economic sector

2. sentiment_analysis — sentiment analysis:
   - score: number from -1.0 to 1.0
   - confidence: confidence from 0 to 1
   - keywords: key words

3. market_impact — market impact:
   - level: "low", "medium" or "high"
   - time_horizon: "short_term", "medium_term" or "long_term"

4. fear_greed_analysis — fear/greed level:
   - score: number from 0 to 100
   - driver: what causes this level

5. trading_signals — trading signals:
   - primary_signal: "bullish", "bearish" or "neutral"
   - signal_strength: number from 0 to 1
   - contrarian_potential: true/false

6. summary:
   - one_line: the essence of the news in one line
   - actionable_insight: specific recommendation for a trader

RETURN ONLY JSON, NO EXPLANATIONS.
"""

def analyze_news_local(news_text):
    """
    Sends a request to the local Ollama API
    """
    
    # Form the full prompt
    full_prompt = FINANCIAL_ANALYST_PROMPT.format(news_text=news_text)
    
    # Local Ollama address
    API_URL = "http://localhost:11434/api/generate"
    
    # Request body
    payload = {
        "model": "mistral",
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 1500
        }
    }
    
    print("🔄 Sending request to local Ollama...")
    print("   (This may take 20-40 seconds)")
    
    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            text = result.get('response', '')
            
            # Look for JSON in the response
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                try:
                    analysis = json.loads(json_match.group())
                    print("✅ Analysis successfully received!")
                    return analysis
                except json.JSONDecodeError as e:
                    print(f"❌ JSON parsing error: {e}")
                    print("📄 Model response:")
                    print(text[:500])
                    return None
            else:
                print("❌ Failed to find JSON in response")
                print("📄 Model response:")
                print(text[:500])
                return None
        else:
            print(f"❌ Error: {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error to Ollama")
        print("   Make sure Ollama is running (icon in system tray)")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("=" * 60)
    print("📊 LOCAL FINANCIAL ANALYST (Ollama)")
    print("=" * 60)
    
    # Test news
    test_news = """
    Apple reported record revenue of $124 billion in the first quarter of 2026,
    exceeding analyst forecasts by 8%. iPhone sales grew by 10% year-over-year.
    The company also announced the launch of a new iPhone model with AI support.
    Shares rose 5% in pre-market trading.
    """
    
    print("\n📰 NEWS:")
    print("-" * 60)
    print(test_news.strip())
    print("-" * 60)
    
    # Analyze
    result = analyze_news_local(test_news)
    
    if result:
        print("\n✅ ANALYSIS RESULT:")
        print("=" * 60)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("=" * 60)
        
        # Trading signal
        signal = result.get('trading_signals', {})
        sentiment = result.get('sentiment_analysis', {})
        
        print("\n📊 TRADING SIGNAL:")
        if signal:
            signal_map = {"bullish": "🟢 BUY", "bearish": "🔴 SELL", "neutral": "⚪ HOLD"}
            print(f"{signal_map.get(signal.get('primary_signal'), '⚪ N/A')}")
            print(f"Signal strength: {signal.get('signal_strength', 0)}")
        
        if sentiment:
            print(f"\n😊 Sentiment score: {sentiment.get('score', 0)}")
    else:
        print("\n❌ ANALYSIS FAILED")
        print("\n🔍 WHAT TO CHECK:")
        print("1. Is Ollama running? (icon in system tray)")
        print("2. Is the model downloaded? (ollama pull mistral)")
        print("3. Is the port busy? (http://localhost:11434)")

if __name__ == "__main__":
    main()
