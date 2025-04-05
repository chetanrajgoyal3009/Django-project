from django.shortcuts import render ,get_object_or_404 ,redirect
from django.contrib.auth.decorators import login_required
from .models import BlogPost
from .forms import BlogPostForm
from .models import BlogPost, Like
from django.http import JsonResponse



def blog_homepage(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')
def landing(request):
    return render(request,'Landing.html')

def login(request):
    return render(request,'login.html')

def profile(request):
    return render(request,'profile.html')
def blog_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')  # Get all posts sorted by date
    return render(request, 'Blog.html', {'posts': posts})

def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    return render(request, 'blog_detail.html', {'post': post})

def write_blog(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user  # Assign logged-in user as author
            blog_post.save()
            return redirect('blog_list')  # Redirect to blog list after posting
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









