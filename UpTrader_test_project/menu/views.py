from django.shortcuts import render


def index(request, pk=None):
    """Return index page or menu related page."""
    template = 'menu/index.html'
    context = {'request': request,
               'pk': pk}
    return render(request, template, context=context)
