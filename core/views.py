import requests
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

ACCESS_TOKEN = 'EAA55oumuenQBOZBbWqaAIYIFZCKHZCkOA7CADC2nRsxUzSicd6bI8YZCxUAAIrcYCZA0mhgZCbI0hWPivlIKm5eLBI3t0CbPHig8WuIRfDYGurpCshT8kOURqA69mo07R9cck8VHuZCcBJx5rL4T94PpGnyIoqS6ZAE8YkMS1jFh9hYZADdDATAtQaHHxPtAz8bXhHEGckWyRVLWu37T0ZAD7bpUcxsjwRLMIGZCL4gQD8wzMcHGZCbvk4Pew0kkCwwVIxZCH7l4ZD'

def home(request):
    return render(request, 'core\home.html')

def dashboard(request):
    user_data = None
    error = None
    username = None
    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            base_url = f'https://graph.facebook.com/{username}?fields=id,name,link,picture.type(large),is_verified,followers_count,about,website,category&access_token={ACCESS_TOKEN}'
            response = requests.get(base_url)
            data = response.json()

            if 'error' in data:
                error = data['error']['message']
            else:
                user_data = data
                # Check if it's a page and get posts
                if 'category' in data:  # Pages have a category field
                    posts_url = f'https://graph.facebook.com/{username}/posts?access_token={ACCESS_TOKEN}'
                    posts_response = requests.get(posts_url)
                    posts_data = posts_response.json()
                    user_data['posts'] = posts_data.get('data', [])
    return render(request, 'dashboard.html', {
        'user_data': user_data, 
        'posts': user_data.get('posts', []) if user_data else [],
        'error': error, 
        'username': username
    })

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return render(request, 'home.html')