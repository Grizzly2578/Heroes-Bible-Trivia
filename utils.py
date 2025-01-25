def get_percent(int, percent):
    product = int * percent / 100
    return product


def taxify(int, percent):
    product = int * percent / 100
    taxed = int - product
    return taxed


print("hello")