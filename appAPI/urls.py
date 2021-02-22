from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from appAPI import views

urlpatterns = [
    path('login/', views.login_api),
    path('check_user_type/', views.user_check_type_api),
    path('check_user_id/', views.user_check_id_api),
    path('user_post/', views.user_create_api),
    path('user_detail/', views.user_detail_api),
]

urlpatterns = format_suffix_patterns(urlpatterns)
