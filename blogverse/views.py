from django.shortcuts import render ,get_object_or_404 ,redirect
from django.contrib.auth.decorators import login_required
from .forms import BlogPostForm,ProfileForm
from .models import BlogPost, Profile, Like
from django.http import JsonResponse
from datetime import date
from django.db.models import Q 
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from datetime import date
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

def signup_view(request):
     if request.method == 'POST':


        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')


        if password != cpassword:
            messages.error(request, 'Passwords do not match')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already used')
        else:
            try:
                validate_password(password)
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                messages.success(
                    request, 'Registration successful! You can now login.')
                return redirect('login')
            except ValidationError as e:
                for error in e:
                    messages.error(request, error)
     return render(request, 'signup.html')


 


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('blog_homepage')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')



def blog_homepage(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')
def landing(request):
    return render(request,'Landing.html')



from django.db.models import Q  # Add this import at the top

def blog_list(request):
    query = request.GET.get('q')  # Get search query from the URL
    if query:
        posts = BlogPost.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by('-created_at')
    else:
        posts = BlogPost.objects.all().order_by('-created_at')
    
    return render(request, 'Blog.html', {'posts': posts, 'query': query})


def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    return render(request, 'blog_detail.html', {'post': post})

def write_blog(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.user = request.user  # Fixed field name
            blog_post.save()
            return redirect('blog_list')
    else:
        form = BlogPostForm()

    return render(request, 'write_blog.html', {'form': form})

def like_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()  # Unlike if already liked
        liked = False
    else:
        liked = True

    return JsonResponse({'liked': liked, 'like_count': post.likes.count()})

def post_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    like_count = post.likes.count()
    return render(request, 'post_detail.html', {'post': post, 'like_count': like_count})




@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={'birthdate': date(2000, 1, 1)}  # or date.today(), anything valid
    )
    blogs = BlogPost.objects.filter(user=request.user)
    return render(request, 'profile.html', {'profile': profile, 'blogs': blogs})



@login_required
def update_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'update_profile.html', {'form': form})








