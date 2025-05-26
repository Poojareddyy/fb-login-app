import requests
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

ACCESS_TOKEN = 'EAA55oumuenQBOZBe1SAXZBSZBDqNoh8nhdpoE6aeQ368wK5hQPx7fFHP1FljNo4AyF5Fs8gqxI64cBJjbz63akZAQN7qIpiwObdUeHL4xE6ZCKPBFRe7KgIu33ZBFQz1MccbdxBVkHiBGZBBxM2mN2GLu27ZAPeAcEiRwNzqw4sjJ1d6kANRIEGNDeNhXnfinpP3SW5BcQkhSgCLvRti4AmycNdXnUKWnZAbx'

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
