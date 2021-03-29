from django.urls import path
from . import views

app_name = 'blocks'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('delete/<int:party_pk>/', views.delete, name='delete'),
    path('update/<int:party_pk>/', views.update, name='update'),
    path('<int:party_pk>/', views.detail, name='detail'),
    path('<int:party_pk>/participate', views.participate, name='participate'),
    path('<int:party_pk>/participate/<int:participate_pk>/delete/', views.participate_delete, name='participate_delete'),
]
