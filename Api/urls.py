from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('posts/', views.post_list, name='post-list'),
    path('posts/<int:post_id>/', views.post_detail, name='post-detail'),
    path('users/', views.user_list_view, name='user-list-view'),
    path('users/add/', views.user_add_view, name='user-add-view'),
    path('users/edit/<int:user_id>/', views.user_edit_view, name='user-edit-view'),
    path('users/delete/<int:user_id>/', views.user_delete_view, name='user-delete-view'),
    path('users/<int:user_id>/', views.user_detail, name='user-detail'),
]
