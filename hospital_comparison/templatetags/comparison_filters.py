from django import template

#: Registering the custom template library.
register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Template filter to safely retrieve a value from a dictionary by key.

    :param dictionary: The dictionary object (e.g., stats_map).
    :param key: The key to look up in the dictionary.
    :return: The value corresponding to the key or None if not found.
    :rtype: Any
    """
    return dictionary.get(key)


@register.filter
def get_attr(obj, attr):
    """
    Template filter to get an attribute from an object dynamically.

    :param obj: The object to fetch the attribute from.
    :param attr: The name of the attribute as a string.
    :return: Value of the attribute or None if not found.
    :rtype: Any
    """
    return getattr(obj, attr, None)
