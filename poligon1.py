# coding=utf-8
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
import requests
from bs4 import BeautifulSoup
import time
import re
import math


url = 'https://food.ru/recipes/209506-detoks-sup-posle-prazdnikov'
recipe_data ={}
recipe_response = requests.get(url)
recipe_soup = BeautifulSoup(recipe_response.text, 'html.parser')

ingredients_info={}



ingredients_info = {}
ingredients = recipe_soup.find_all(['a', 'span'], class_='ingredientsTable_text__3ILFA')
quantities = []

even_ingredients = []
for i in range(len(ingredients)):
    if i % 2 != 0:  # Если индекс чётный
        even_ingredients.append(ingredients[i])  # Добавляем в quantities
        quantities.append(ingredients[i])  # Добавляем элемент в quantities
        #print(ingredients[i])

# Удаляем чётные элементы из ingredients
ingredients = [ingredient for i, ingredient in enumerate(ingredients) if i % 2 == 0]

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
        #print(quantity_text)
        if '=' in quantity_text:
            quantity_text = quantity_text.split('=')[-1]
        
            # Убираем все символы, которые не являются цифрами
        if re.search(r'\d', quantity_text):
            quantity_clean = ''.join(re.findall(r'\d+', quantity_text))

    # Проверяем наличие точки
            if '.' in quantity_text:
                try:
            # Преобразуем в целое число, делим на 10 и обратно в строку
                    quantity_clean = str(int(quantity_clean) // 10)
                except ValueError:
            # Обработка ошибки преобразования в целое число
                    pass
        else:
            quantity_clean = quantity_text
            # Записываем в словарь ингредиентов
        ingredients_info[ingredient_text] = '1' if quantity_clean == '0' else quantity_clean
        #ingredients_info[ingredient_text] = quantity_clean

# Сохраняем результат в словарь данных рецепта
recipe_data['ingredients'] = ingredients_info


servings_input = recipe_soup.find('input', class_='input yield default yield')

flag=False

if servings_input:
    servings_value = servings_input.get('value')
    #print(servings_value)
        
    if servings_value.isdigit():
        servings_value = int(servings_value)
        #print(servings_input)    
            # Коррекция значений ингредиентов (каждый четный элемент словаря делим на servings_value)
        for i, (ingredient, quantity) in enumerate(ingredients_info.items()):
            #print(1)
            if 1: 
                try:
                    #print(quantity, type(ingredient))
                    corrected_quantity = math.ceil(int(quantity) / servings_value)
                    ingredients_info[ingredient] = corrected_quantity
                except (ValueError, ZeroDivisionError):
                    continue
print(ingredients_info)