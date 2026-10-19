import streamlit as st
import json
from google import genai


client = genai.Client(api_key="AQ.Ab8RN6IHs-cjSx68K3gPOoYrb3VFfDRVCcR1A1VvI2-m-I7LZg")

# Загружаем JSON только один раз для скорости
@st.cache_data
def load_data():
    with open("astana_poi.json", "r", encoding="utf-8") as f:
        return json.load(f)

poi_data = load_data()

# Настройки интерфейса
st.title("🏙️ ИИ-Гид по Астане")
st.caption("Прототип RAG-системы для Smart City | Build with AI")

# Пользователь может сам указать, где он находится
user_location = st.text_input("Где вы сейчас находитесь?", value="возле Экспо")

# Храним историю переписки в памяти сессии
if "messages" not in st.session_state:
    st.session_state.messages = []

# Отрисовываем предыдущие сообщения
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Поле для ввода нового запроса
if user_query := st.chat_input("Например: Ищу тихое место с розеткой..."):
    # Показываем запрос пользователя
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)
        
    # Формируем промпт с учетом новой локации и запроса
    prompt = f"""
    Ты умный ИИ-помощник по прогулкам в городе Астана. 
    Пользователь находится здесь: {user_location}. Его запрос: "{user_query}"
    
    Вот доступная база мест (POI):
    {json.dumps(poi_data, ensure_ascii=False)}
    
    Задача: Выбери 1-3 подходящих места. Для каждого напиши:
    1. Название, примерное расстояние и время в пути.
    2. Почему: короткая мотивация.
    3. План действий: конкретное действие.
    Отвечай кратко, человеческим языком.
    """
    
    # Показываем анимацию загрузки, пока ИИ думает
    with st.chat_message("assistant"):
        with st.spinner("Ищу лучшие места..."):
            response = client.models.generate_content(
                model='gemini-3.8-flash',
                contents=prompt,
            )
            st.markdown(response.text)
            
    # Сохраняем ответ в историю
    st.session_state.messages.append({"role": "assistant", "content": response.text})
