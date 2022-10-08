
from django.urls import path

from accounts.views import *
from . import views
urlpatterns = [
    path('login/', Login.as_view(), name="login"),
    path('register/', Register.as_view(), name="Register"),
    path('forget_password/',Forget_password.as_view(), name="forget_password"),
    path('change-password/<token>/',views.ChangePassword, name="change_password"),
    path('user_post/',User_Post.as_view(),name='user_post'),
    path('post_view_user/<int:pk>/', views.Post_view_user,name='Post_view_user'),
    path('post_view/',Post_view.as_view(),name='view_post'),
    path('user_social/', User_Social.as_view(),name='user_social'),
    path('user_social_view/',views.User_Social_view,name='user_social'),
    path('user_social_update/<int:pk>/',views.User_Social_Update,name='User_Social_Update'),
    path('user_about/', User_About.as_view(),name='User_About'),
    path('user_about_view/', views.User_About_View,name='View_User_About'),
    path('user_about_update/<int:pk>/', views.User_About_Update,name='User_About_Update'),
    path('user_profile_pic/', User_Profile_Pic.as_view(),name='user_profile_pic'),
    path('user_profile_pic_update/<int:pk>/', views.User_Profile_pic_Update,name='User_Profile_Pic_Update'),
    path('like/<int:id>/',views.Like_Post,name='like_post'),
    path('user_comment/',User_Comment.as_view(),name='user_comment'),
    path('postdetail/<int:pk>/',views.PostDetail,name='PostDetail'),
    path('create_blog/',BlogPost.as_view(),name='blog'),
    path('blog_view/',views.Blog_view,name='blog_view'),
    path('blog_update/<int:pk>/',views.Blog_update,name='blog_update'),
    path('blog_delete/<int:pk>/',views.Blog_delete,name='blog_delete'),
]