from django.urls import path
from geospoc import views

app_name = 'geospoc'

urlpatterns = [
    path('', views.index, name='index'),
    path('validate_email/', views.validate_email, name='validate_email'),

]
