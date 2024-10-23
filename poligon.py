import requests
from bs4 import BeautifulSoup
import time
import re
import math

# URL главной страницы сайта
url = 'https://food.ru/recipes/227769-sochnye-frikadelki-s-lukovym-sousom'
recipe_data ={}
recipe_response = requests.get(url)
recipe_soup = BeautifulSoup(recipe_response.text, 'html.parser')

def clean_recipe_soup(recipe_soup):
    # Преобразуем объект soup в строку
    soup_str = str(recipe_soup)
    
    # Заменяем все множественные пробелы на один пробел
    soup_cleaned = re.sub(r'\s+', ' ', soup_str)
    
    # Возвращаем обратно в объект BeautifulSoup
    return BeautifulSoup(soup_cleaned, 'html.parser')



recipe_soup = BeautifulSoup(str(recipe_soup).replace('<!-- -->', ' '), 'html.parser')
recipe_soup = BeautifulSoup(str(recipe_soup).replace('\xa0', ' '), 'html.parser')
    
recipe_soup = clean_recipe_soup(recipe_soup)

ingredients_info = {}

ingredients = recipe_soup.find_all(['a', 'span'], class_='ingredientsTable_text__3ILFA')
quantities = []

# Добавляем каждый чётный элемент из ingredients в quantities и удаляем его из ingredients
even_ingredients = []
for i in range(len(ingredients)):
    if i % 2 != 0:  # Если индекс чётный
        even_ingredients.append(ingredients[i])  # Добавляем в quantities
        quantities.append(ingredients[i])  # Добавляем элемент в quantities

# Удаляем чётные элементы из ingredients
ingredients = [ingredient for i, ingredient in enumerate(ingredients) if i % 2 == 0]

# Теперь ingredients содержит только нечётные элементы, а quantities дополнен чётными элементами из ingredients

'''
for _ in ingredients:
	print(_)

print('\n\n\n')
for _ in quantities:
	print(_)
'''
if len(ingredients) == len(quantities):
    for ingredient, quantity in zip(ingredients, quantities):
        # Спускаемся в самый глубокий вложенный элемент внутри тега ingredient
        deepest_element = ingredient
        while deepest_element.find(True):
            deepest_element = deepest_element.find(True)
        
            # Извлекаем текст из самого глубокого элемента
        ingredient_text = deepest_element.text.strip()
            # Обработка количества, если содержит знак '=', отсекаем всё слева
        quantity_text = quantity.text.strip()
        if '=' in quantity_text:
            quantity_text = quantity_text.split('=')[-1]
        
            # Убираем все символы, которые не являются цифрами
        if re.search(r'\d', quantity_text):
        	quantity_clean = ''.join(re.findall(r'\d+', quantity_text))
        else:
        	quantity_clean = quantity_text
        
            # Записываем в словарь ингредиентов
        ingredients_info[ingredient_text] = quantity_clean

# Сохраняем результат в словарь данных рецепта
recipe_data['ingredients'] = ingredients_info




servings_input = recipe_soup.find('input', class_='input yield default yield')

if servings_input:
    servings_value = servings_input.get('value')
    print(servings_value)
        
    if servings_value.isdigit():
        servings_value = int(servings_value)
            
            # Коррекция значений ингредиентов (каждый четный элемент словаря делим на servings_value)
        for i, (ingredient, quantity) in enumerate(ingredients_info.items()):
            if 1:  # Только четные элементы (индекс с 1)
                try:
                    corrected_quantity = math.ceil(int(quantity) / servings_value)
                    ingredients_info[ingredient] = corrected_quantity
                except (ValueError, ZeroDivisionError):
                    continue
    
    # Обновляем данные ингредиентов в словаре



print(recipe_data)