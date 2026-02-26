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

def main():
    print("=" * 60)
    print("📊 ЛОКАЛЬНЫЙ ФИНАНСОВЫЙ АНАЛИТИК (Ollama)")
    print("=" * 60)
    
    # Тестовая новость
    test_news = """
    Apple сообщила о рекордной выручке в $124 млрд в первом квартале 2026 года,
    превысив прогнозы аналитиков на 8%. Продажи iPhone выросли на 10% в годовом исчислении.
    Компания также объявила о запуске новой модели iPhone с поддержкой ИИ.
    Акции выросли на 5% на предварительных торгах.
    """
    
    print("\n📰 НОВОСТЬ:")
    print("-" * 60)
    print(test_news.strip())
    print("-" * 60)
    
    # Анализируем
    result = analyze_news_local(test_news)
    
    if result:
        print("\n✅ РЕЗУЛЬТАТ АНАЛИЗА:")
        print("=" * 60)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("=" * 60)
        
        # Торговый сигнал
        signal = result.get('trading_signals', {})
        sentiment = result.get('sentiment_analysis', {})
        
        print("\n📊 ТОРГОВЫЙ СИГНАЛ:")
        if signal:
            signal_map = {"bullish": "🟢 ПОКУПКА", "bearish": "🔴 ПРОДАЖА", "neutral": "⚪ ДЕРЖАТЬ"}
            print(f"{signal_map.get(signal.get('primary_signal'), '⚪ Н/Д')}")
            print(f"Сила сигнала: {signal.get('signal_strength', 0)}")
        
        if sentiment:
            print(f"\n😊 Тональность: {sentiment.get('score', 0)}")
    else:
        print("\n❌ АНАЛИЗ НЕ ВЫПОЛНЕН")
        print("\n🔍 ЧТО ПРОВЕРИТЬ:")
        print("1. Запущена ли Ollama? (иконка в трее)")
        print("2. Скачана ли модель? (ollama pull mistral)")
        print("3. Не занят ли порт? (http://localhost:11434)")

if __name__ == "__main__":
    main()