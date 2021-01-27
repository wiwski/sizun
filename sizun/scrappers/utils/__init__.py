def formatted_price_to_int(formatted_price: str) -> int:
    return int(formatted_price.replace(' ', '').replace('€', '').replace(u'\xa0', '').strip())


def formatted_area_to_int(formatted_area: str, square_unit: str = '²') -> int:
    return int(formatted_area.replace(square_unit, '').split(',')[0].strip())
