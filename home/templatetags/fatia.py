from django import template

register = template.Library()

results = []
def fatia_lista(results):
    lista = results[0:10]
    return f"{lista}"

register.filter('fatia_lista', fatia_lista)