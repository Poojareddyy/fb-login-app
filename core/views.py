import requests
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
def home(request):
    return render(request, 'core/home.html')
@login_required
def dashboard(request):
    username = request.GET.get('username')
    context = {}

    if username:
        access_token = 'EAA55oumuenQBO3kZBrr0VjVcGDz6nh4eOeVhyPxUSlqpJVWLRmiAQzD2LDX0arnFZAxNi8zr6TNhGljeQkuyZAHTWhNJWlf24qXz7RHaUFRhHyrzjdWzdteT7xo3ZAcPISAtgv9ZBqu8RG0ZBwenM0N6eNZAFHsu5Nubzon2bendDZBRRZCFBQdkw8x4t3aOi3b2B7uOp0ITziZCGA16LUVNJlGXxEpZClwYa5109lDY4YendwEEZC5XmUy3JLa7em20kL08RAZDZD'
        fields = 'id,name,first_name,last_name,email,link,verified,picture.width(200).height(200),category'
        graph_url = f'https://graph.facebook.com/v18.0/{username}?fields={fields}&access_token={access_token}'

        try:
            response = requests.get(graph_url)
            data = response.json()

            if 'error' in data:
                context['data'] = {'error': {'message': data['error']['message']}}
            else:
                context['data'] = data
                context['is_page'] = 'category' in data
                context['username'] = username

        except requests.exceptions.RequestException as e:
            context['data'] = {'error': {'message': str(e)}}

    return render(request, 'core/dashboard.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')