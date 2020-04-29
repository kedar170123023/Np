from django import template

register = template.Library()

# {% load custom_tenplate_tags %}
# USES : {{ mydict|get_item:item.NAME }}
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)   #returns None if not present
    

