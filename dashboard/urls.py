from django.urls import path
from .views import create_post, register, user_login, create_comment, post_detail, quest_ans

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('', create_post, name='create_post'),
    path('comment/create/<int:post_id>/', create_comment, name='create_comment'),
    path('posts/', post_detail, name='post_detail'),
    path('chat/', quest_ans, name='quest_ans')

]
