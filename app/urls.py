from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('new-car', views.new_car_view, name="new_car"),
    path('used-car', views.used_car_view, name="used_car"),
]
