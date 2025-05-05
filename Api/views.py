from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
import json
import logging
from rest_framework.decorators import api_view 
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer, UserSerializer
from django.urls import reverse


logger = logging.getLogger(__name__)


FLASK_API_URL = 'https://blog-verse.up.railway.app/api'


@login_required
def dashboard(request):
  
    try:
       
        posts_response = requests.get(f'{FLASK_API_URL}/posts')
        posts = posts_response.json() if posts_response.status_code == 200 else []
        
       
        users_response = requests.get(f'{FLASK_API_URL}/students')
        users = users_response.json() if users_response.status_code == 200 else []
        
        
        total_likes = sum(post.get('likes', 0) for post in posts)
        
        
        search_query = request.GET.get('search', '')
        
     
        if search_query:
            posts = [post for post in posts if search_query.lower() in post.get('title', '').lower() or 
                    search_query.lower() in post.get('content', '').lower()]
            users = [user for user in users if search_query.lower() in user.get('name', '').lower() or 
                    search_query.lower() in user.get('email', '').lower()]
        
        context = {
            'posts': posts,
            'users': users,
            'total_likes': total_likes,
            'search_query': search_query
        }
        return render(request, 'dashboard.html', context)
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Flask API: {str(e)}")
        return render(request, 'dashboard.html', {
            'posts': [],
            'users': [],
            'total_likes': 0,
            'search_query': '',
            'error': 'Could not connect to API server'
        })


@login_required
@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        try:
         
            response = requests.get(f'{FLASK_API_URL}/posts')
            if response.status_code == 200:
                posts = response.json()
                serializer = PostSerializer(posts, many=True)
                return Response(serializer.data)
            return Response({'error': 'Failed to fetch posts'}, status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Failed to connect to Flask API: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'POST':
        try:
          
            print("Received POST data:", request.data)
            
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
            
                data = serializer.validated_data
                if 'author' not in data or not data['author']:
                    if request.user.is_authenticated:
                        data['author'] = request.user.username
                    else:
                        data['author'] = 'Anonymous'
                if 'likes' not in data:
                    data['likes'] = 0
                
                response = requests.post(
                    f'{FLASK_API_URL}/posts',
                    json=data,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code in [200, 201]:
                    return Response(response.json(), status=status.HTTP_201_CREATED)
                return Response({'error': f'Failed to create post: {response.text}'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Failed to connect to Flask API: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@login_required
@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, post_id):
    logger.debug(f"Received request for post_id: {post_id}")
    try:
    
        flask_url = f'{FLASK_API_URL}/posts/{post_id}'
        logger.debug(f"Calling Flask API: {flask_url}")
        
        response = requests.get(flask_url)
        logger.debug(f"Flask API response status: {response.status_code}")
        
        if response.status_code != 200:
            logger.error(f"Flask API error: {response.text}")
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        
        post = response.json()
        logger.debug(f"Received post data: {post}")
        
        if request.method == 'GET':
            serializer = PostSerializer(post)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                # Preserve existing values if not provided
                data = serializer.validated_data
                if 'author' not in data:
                    data['author'] = post.get('author', 'Anonymous')
                if 'likes' not in data:
                    data['likes'] = post.get('likes', 0)
                
                # Send to Flask API
                response = requests.put(
                    f'{FLASK_API_URL}/posts/{post_id}',
                    json=data,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 200:
                    return Response(response.json())
                return Response({'error': 'Failed to update post'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            
            response = requests.delete(f'{FLASK_API_URL}/posts/{post_id}')
            if response.status_code == 200:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'error': 'Failed to delete post'}, status=status.HTTP_400_BAD_REQUEST)
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        return Response({'error': f'Failed to connect to Flask API: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@login_required
@api_view(['GET', 'POST'])
def user_list(request):
    if request.method == 'GET':
        try:
            response = requests.get(f'{FLASK_API_URL}/students')
            if response.status_code == 200:
                users = response.json()
                serializer = UserSerializer(users, many=True)
                return Response(serializer.data)
            return Response({'error': 'Failed to fetch users'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'POST':
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data
                response = requests.post(
                    f'{FLASK_API_URL}/students',
                    json=data,
                    headers={'Content-Type': 'application/json'}
                )
                if response.status_code in [200, 201]:
                    return Response(response.json(), status=status.HTTP_201_CREATED)
                return Response({'error': f'Failed to create user: {response.text}'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@login_required
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, user_id):
    flask_url = f'{FLASK_API_URL}/students/{user_id}'
    response = requests.get(flask_url)
    print("Flask API status:", response.status_code)
    print("Flask API response:", response.text)
    if response.status_code != 200:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    user = response.json()
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            response = requests.put(
                f'{FLASK_API_URL}/students/{user_id}',
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code == 200:
                return Response(response.json())
            return Response({'error': 'Failed to update user'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        response = requests.delete(f'{FLASK_API_URL}/students/{user_id}')
        if response.status_code == 200:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Failed to delete user'}, status=status.HTTP_400_BAD_REQUEST)


@login_required
def user_list_view(request):
    response = requests.get(f'{FLASK_API_URL}/students')
    users = response.json() if response.status_code == 200 else []
    return render(request, 'user_list.html', {'users': users})


@login_required
def user_add_view(request):
    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'profile_picture': request.POST.get('profile_picture', None)
        }
        requests.post(f'{FLASK_API_URL}/students', json=data)
        return redirect(reverse('api:user-list-view'))
    return render(request, 'user_form.html')


@login_required
def user_edit_view(request, user_id):
    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'profile_picture': request.POST.get('profile_picture', None)
        }
        requests.put(f'{FLASK_API_URL}/students/{user_id}', json=data)
        return redirect(reverse('api:user-list-view'))
    response = requests.get(f'{FLASK_API_URL}/students/{user_id}')
    user = response.json() if response.status_code == 200 else None
    return render(request, 'user_form.html', {'user': user})


@login_required
def user_delete_view(request, user_id):
    if request.method == 'POST':
        requests.delete(f'{FLASK_API_URL}/students/{user_id}')
        return redirect(reverse('api:user-list-view'))
    response = requests.get(f'{FLASK_API_URL}/students/{user_id}')
    user = response.json() if response.status_code == 200 else None
    return render(request, 'user_confirm_delete.html', {'user': user})
