from django.contrib import admin
from .models import BlogPost,Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'profession', 'email', 'phone')
    search_fields = ('name', 'email', 'profession')
    list_filter = ('profession', 'gender')
    

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title','user', 'created_at')  
    search_fields = ('title', 'content')  
    list_filter = ('created_at',)  
    

admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Profile, ProfileAdmin)