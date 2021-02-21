from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from appAPI import views

urlpatterns = [
    path('login/', views.login_api),
    path('user_post/', views.user_create_api),
    path('user_detail/<int:pk>', views.user_detail_api),
]

urlpatterns = format_suffix_patterns(urlpatterns)
