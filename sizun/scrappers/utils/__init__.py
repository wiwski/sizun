import re


def formatted_price_to_int(formatted_price: str) -> int:
    price = formatted_price.replace(' ', '').replace(
        '€', '').replace(u'\xa0', '').strip()
    if ',' in price:
        price = price.split(',')[0]
    elif '.' in price:
        price = price.split('.')[0]
    return int(price)


def formatted_area_to_int(formatted_area: str, square_unit: str = 'm²', comma_char=',') -> int:
    return int(formatted_area.replace(square_unit, '').split(comma_char)[0].strip())


def extract_area(html_element: str, regex_pattern: str = None, square_unit: str = 'm²', comma_char=',') -> int:
    if not regex_pattern:
        regex_pattern = f'\d+ {square_unit}'
    match = re.search(
        regex_pattern, html_element)
    if match:
        return formatted_area_to_int(match.group(), square_unit=square_unit, comma_char=comma_char)
