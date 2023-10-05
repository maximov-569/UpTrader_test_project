from django import template

from menu.models import Menu

register = template.Library()


@register.inclusion_tag('menu/menus.html', takes_context=True)
def draw_menu(context, category_name):
    """Draw root menu and fill context with data from db."""
    data = [
        item for item in Menu.objects.select_related('parent').filter(
            category__name=category_name
        )
    ]
    main_object = [item for item in data if item.name == category_name][0]

    active = None
    for item in data:
        if item.id == context['pk']:
            active = item

    context['active'] = active
    data.remove(main_object)
    context['objects'] = data
    context['main_object'] = main_object
    context['children'] = [item for item in data if item.parent == main_object]
    return context


@register.inclusion_tag('menu/menus.html', takes_context=True)
def draw_children(context, child_id):
    """Draw child with data from context
    and prepare context for next iteration."""
    main_object = [
        item for item in context['objects'] if item.id == child_id
    ][0]

    context['objects'].remove(main_object)
    context['main_object'] = main_object

    active = context['active']
    context['children'] = None if (active.parent == main_object.parent
                                   and active != main_object) else [
        item for item in context['objects'] if item.parent == main_object
    ]

    return context
