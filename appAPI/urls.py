from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from appAPI import views

urlpatterns = [
    #user
    path('login/', views.login_api),
    path('check_user_type/', views.user_check_type_api),
    path('check_user_id/', views.user_check_id_api),
    path('user_create/', views.user_create_api),
    path('user_detail/', views.user_detail_api),
    #pets
    path('pet_create/', views.pet_create_api),
    path('pet_get_all/', views.pet_get_all_api),
    path('pet_owner_get/<str:sta>', views.pet_owner_get_api),
    path('pet_detail/<int:pk>', views.pet_detail_api),
    path('pet_image/', views.pet_image_api),
    path('pet_image/<int:pk>', views.pet_images_get_api),
    #report
    path('report/', views.report_all_api),
    path('report/detail/<int:id>', views.report_detail_api),
    path('report/detail/userdetail/<int:id>', views.report_user_update_api),
    path('pet_owner_detail/<int:id>', views.user_owner_pet_detail),
    path('send_report/', views.user_owner_send_report),
    path('user_get_detail/<int:id>', views.user_get_detail),
    #chat
    path('crest_chat/', views.chat_crest),
]

urlpatterns = format_suffix_patterns(urlpatterns)
