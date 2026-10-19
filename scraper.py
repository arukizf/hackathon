from playwright.sync_api import sync_playwright
import json

urls = [
    "https://2gis.kz/astana/collection/627698a9-248b-474c-84d5-deb997efed89",
    "https://2gis.kz/astana/collection/2fc341aa-e641-4be5-ac4b-2c99dac74691"
    # Добавь остальные ссылки
]

def scrape_2gis(urls):
    data = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        for url in urls:
            page.goto(url)
            page.wait_for_selector('h2', timeout=5000) # Ждем загрузки контента
            
            # Собираем названия и описания (селекторы нужно будет подогнать под верстку 2GIS)
            items = page.query_selector_all('div[class^="_"]') 
            for item in items:
                title_elem = item.query_selector('h2')
                if title_elem:
                    title = title_elem.inner_text()
                    data.append({
                        "name": title,
                        "description": "Описание точки из коллекции", 
                        "coordinates": "51.12, 71.43", # Заглушка, если 2GIS не отдает легко координаты
                        "category": "интересное место",
                        "working_hours": "10:00-22:00"
                    })
        browser.close()
    return data

if __name__ == "__main__":
    dataset = scrape_2gis(urls)
    with open("astana_poi.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4)
    print("Датасет собран!")
