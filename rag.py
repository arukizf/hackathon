import json
from google import genai

# Вставь сюда свой ключ (получить бесплатно: https://aistudio.google.com/app/apikey)
client = genai.Client(api_key="AQ.Ab8RN6IHs-cjSx68K3gPOoYrb3VFfDRVCcR1A1VvI2-m-I7LZg")

def get_recommendations(user_query, user_location="Астана"):
    # 1. Загружаем нашу базу локаций
    with open("astana_poi.json", "r", encoding="utf-8") as f:
        poi_data = json.load(f)
    
    # 2. Формируем системный промпт
    prompt = f"""
    Ты умный ИИ-помощник по прогулкам в городе Астана. 
    Пользователь находится здесь: {user_location}.
    Его запрос: "{user_query}"
    
    Вот доступная база мест (POI):
    {json.dumps(poi_data, ensure_ascii=False, indent=2)}
    
    Задача:
    Выбери 1-3 наиболее подходящих места из базы. 
    Для каждого места напиши:
    1. Название, расстояние (примерно) и время в пути.
    2. Почему: короткая мотивация.
    3. План действий: конкретное действие или рекомендация.
    Отвечай кратко, человеческим языком.
    """
    
    # 3. Отправляем запрос в новую версию API
    response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=prompt,
    )
    
    return response.text

if __name__ == "__main__":
    test_query = "Еду с ребёнком, где рядом есть детские площадки или музей с интерактивами?"
    print(f"Запрос: {test_query}\n")
    print(get_recommendations(test_query, user_location="возле Экспо"))
