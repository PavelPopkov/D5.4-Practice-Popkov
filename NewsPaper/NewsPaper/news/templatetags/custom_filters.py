from django import template

register = template.Library()

@register.filter(name='multiply')

def multiply(value, arg):
    if isinstance(value,str) and isinstance(arg, int):
        return str(value)*arg
    else:
        raise ValueError(f'Нельзя умножить {type(value)} на {type(arg)}')

@register.filter(name='censor')
def censor(value, arg):
    words = value.split()
    value1 = ''
    for word in words:
        if isinstance(word, str) and isinstance(arg, str):
            if word == arg:
                word = '*****'
            value1 += word + ' '
        else:
            raise ValueError(f'Нельзя {type(word)}!')
    return value1