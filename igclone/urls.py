from django.urls import path
from . import views


urlpatterns = [
  path('', views.index, name="home"),
  path('user_page/<int:pk>/', views.userPage, name="user_page"),
  path('add_photo/', views.add_photo, name="add_photo"),
  path('edit_profile/<int:pk>/', views.edit_profile, name="edit_profile"),
  path('delete_profile/<int:pk>/', views.delete_profile, name="delete_profile"),
  path('follow_user/<int:pk>/', views.follow_user, name="follow_user"),
  path('post/<int:pk>/', views.post_user, name="post"),
  path('delete_post/<int:pk>/', views.delete_post, name="delete_post"),
  path('user_page/<int:pk>/following/', views.followingPage, name="following"),
  path('user_page/<int:pk>/followers/', views.followersPage, name="followers"),
  path('following-list/<int:pk>/', views.followingList, name="followingList"),
  path('follower-list/<int:pk>/', views.followerList, name="followerList"),
  path('user_page/<int:u_pk>/publication/<int:p_pk>/', views.publicationDetail, name="publication"),
]