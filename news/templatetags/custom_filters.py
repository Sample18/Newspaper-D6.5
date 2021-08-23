from django import template

register = template.Library()

@register.filter(name='censorship')
def censorship(value, arg):
    censor = ['предупреждение', 'Windows'] #заполняем список любыми плохими словами, для проверки заполнено словами из новости
    val = value.split()
    if arg:
        filtered_str = ' '.join((filter(lambda s: s not in censor, val)))
        return filtered_str
    else:
        return value