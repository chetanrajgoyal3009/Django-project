from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_homepage, name='blog_homepage'),
    path('about/', views.about, name='about'),
    path('landing/', views.landing, name='landing'),  # Changed 'Landing' to lowercase
    path('login/', views.login_view, name='login'),
    path('write/', views.write_blog, name='write_blog'),
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/update/', views.update_profile, name='update_profile'),
    # Blog functionality
    path('blog/', views.blog_list, name='blog_list'),  # Show all blog posts
    path('blog/<int:post_id>/', views.blog_detail, name='blog_detail'),  # View a single blog post
     path('like/<int:post_id>/', views.like_post, name='like_post'),
     path('post/<int:post_id>/', views.post_detail, name='post_detail'),
     path('signup/', views.signup_view, name='signup'),
]
