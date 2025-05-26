import requests
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

ACCESS_TOKEN = 'EAA55oumuenQBO15XwdaLpo5Nf5yDnegHmXCZCuqJWqSOTqKtsJzy36xFuopi7geIZCGFZCePlsy3y7nZBlwoqzSO5xyLgrmg28XKYsWFIGDboJZCm0JGyxRyoXtPGL2UZBjxwAb5YaLa5kYigsXD7z8FCxyIp0vZC0zbqIAGQ7aR3cv1pmSaxfnj5RiuWnTda6KQEN4H5ZATXRnjRVYdLRxh6bmXbN6dcUvaxGB8fZCC4vG7ozZApHeZC8aUu0RkBCV5StXZCwZDZD'

def home(request):
    return render(request, 'core/home.html')

def dashboard(request):
    user_data = None
    posts = []
    error = None
    username = ""

    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            fields = 'id,name,link,picture.type(large),is_verified,followers_count,about,website,category'
            url = f'https://graph.facebook.com/{username}?fields={fields}&access_token={ACCESS_TOKEN}'
            response = requests.get(url)
            data = response.json()

            if 'error' in data:
                error = data['error']['message']
            else:
                user_data = data

                # If it's a Page, try to get posts
                if 'category' in data:
                    posts_url = f'https://graph.facebook.com/{username}/posts?access_token={ACCESS_TOKEN}'
                    posts_response = requests.get(posts_url)
                    posts_data = posts_response.json()

                    if 'data' in posts_data:
                        posts = posts_data['data']

    return render(request, 'core/dashboard.html', {
        'user_data': user_data,
        'posts': posts,
        'error': error,
        'username': username
    })

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return render(request, 'core/home.html')
