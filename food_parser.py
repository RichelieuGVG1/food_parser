import requests
from bs4 import BeautifulSoup

# URL главной страницы сайта
url = 'https://food.ru'  # Замените на актуальный URL
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Глобальные списки для хранения результатов
alt_texts = []
href_links = []
recipies_pages_numbers = []

def prepare_links_for_recipies():
    # Ищем <footer> элемент
    footer = soup.find('footer')
    
    # Ищем все <div> с нужным классом внутри <footer>
    divs = footer.find_all('div', class_='accordion_item__7pPNL navigation_accordionItem__H2LlR')
    
    # Проходим по каждому найденному <div>
    for div in divs:
        # Находим все <img> и сохраняем их атрибуты alt
        imgs = div.find_all('img')
        for img in imgs:
            alt_text = img.get('alt')
            if alt_text:
                alt_texts.append(alt_text)

        # Находим все <a> с нужным классом и сохраняем их href
        links = div.find_all('a', class_='navigation_linkToCategory__SLAkq')
        for link in links:
            href = link.get('href')
            if href:
                href_links.append(href)
    
    return alt_texts, href_links

def get_pagination_numbers(href_links):
    # Проходим по каждой ссылке в href_links
    for link in href_links:
        # Строим полный URL для каждой страницы
        full_url = url + link
        response = requests.get(full_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Ищем все <div> с нужным классом для пагинации
        pagination_divs = soup.find_all('div', class_='pagination_button__aFUEc pagination_point__YdGsp')
        
        if pagination_divs:
            # Берем самый последний элемент
            last_pagination_div = pagination_divs[-1]
            # Сохраняем содержимое этого <div> в список recipies_pages_numbers
            recipies_pages_numbers.append(last_pagination_div.text.strip())




# Вызываем функцию и выводим списки
alt_texts, href_links = prepare_links_for_recipies()

get_pagination_numbers(href_links)


print("ALT атрибуты изображений:", alt_texts)
print("Ссылки категорий:", href_links)
print("Номера страниц пагинации:", recipies_pages_numbers)
