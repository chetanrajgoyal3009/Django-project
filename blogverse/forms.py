from django import forms
from .models import BlogPost,Profile

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'content']  # Fields shown in the form


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'profession', 'gender', 'birthdate', 'address', 'email', 'phone', 'profile_image']