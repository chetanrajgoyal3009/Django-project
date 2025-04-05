from django.contrib import admin
from .models import BlogPost

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')  
    search_fields = ('title', 'content')  
    list_filter = ('created_at',)  
    

admin.site.register(BlogPost, BlogPostAdmin)
    

