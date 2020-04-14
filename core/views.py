from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
import requests,json
from django.urls import reverse
import os

def env_var(key, default=None):
    """Retrieves env vars and makes Python boolean replacements"""
    val = os.environ.get(key, default)
    if val == 'True':
        val = True
    elif val == 'False':
        val = False
    return val

AUTH_URL = "https://www.instagram.com/oauth/authorize/?"
REQUEST_ACCESS_URL = "https://api.instagram.com/oauth/access_token/?"
REDIRECT_URI = "https://localhost:8000/auth/insta"
INSTAGRAM_KEY = env_var('INSTAGRAM_KEY')
INSTAGRAM_SECRET = env_var('INSTAGRAM_SECRET')

# Create your views here.
def login(request):
  return render(request, 'login.html')

@ login_required
def home(request):
	return render(request, 'home.html')

def insta(request):
	url = f"{AUTH_URL}client_id={INSTAGRAM_KEY}&redirect_uri={REDIRECT_URI}&scope=user_profile,user_media&response_type=code"
	return HttpResponseRedirect(url)

def grant_access(request):
    # Get access token for the user
    code = request.GET.get('code')
    payload = {'client_id': INSTAGRAM_KEY , 'client_secret': INSTAGRAM_SECRET , 'grant_type':'authorization_code','redirect_uri': REDIRECT_URI, 'code': code}
    res = requests.post(REQUEST_ACCESS_URL, data= payload)
    response = json.loads(res.text) 
    
    # Auth failed then redirect to login
    if 'code' in response.keys():
    	if(response['code']==400):
    		return HttpResponseRedirect(reverse('login'))

    # Get user name
    url = f"https://graph.instagram.com/{response['user_id']}?fields=id,username&access_token={response['access_token']}"
    res =requests.get(url)
    user_dictionary = json.loads(res.text) 

    # Get followers count
    url = f"https://www.instagram.com/{user_dictionary['username']}/?__a=1"
    res =requests.get(url)
    res = json.loads(res.text)
    user_dictionary['followers_count'] = res['graphql']['user']['edge_followed_by']['count']

    return render(request,'home.html',context=user_dictionary)

    
