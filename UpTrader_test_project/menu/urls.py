from django.urls import path
from menu.views import index

app_name = 'menu'

urlpatterns = [
    path('<int:pk>/', index, name='index'),
    path('', index, name='index'),
]
