from .models import Stock


def symbol_choices():
    values = Stock.objects.values_list('symbol', 'name')
    # Include the symbol and name in the display
    ret = [(item[0], f"{item[0]}: {item[1]}") for item in values]
    return ret
