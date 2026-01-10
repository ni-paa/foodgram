def file_generation(shoppinglist):
    """Метод генерирует список для скачивания/файл."""

    shopping_list = list()
    shopping_list.append('Ваш список покупок в Foodgram:\n')
    for ingredient in shoppinglist:
        shopping_list.append(
            f'{ingredient["ingredient__name"]} - '
            f'{ingredient["ingredient__measurement_unit"]} - '
            f'{ingredient["amount"]}')
    return '\n'.join(shopping_list)
