from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
import requests,json

user_dictionary={}
# Create your views here.
def login(request):
  return render(request, 'login.html')


def home(request):
	print(user_dictionary,"insideee")
	return render(request, 'home.html', context=user_dictionary)


REQUEST_ACCESS = "https://api.instagram.com/oauth/access_token/?"
def grant_access(request):
    code = request.GET.get('code')
    payload = {'client_id': CLIENT_ID, 'client_secret':CLIENT_SECRET, 'grant_type':'authorization_code','redirect_uri': REDIRECT_URI, 'code': code}
    resp = requests.post(REQUEST_ACCESS, data= payload)
    response = json.loads(resp.text)

def insta(request):
	# https://www.instagram.com/oauth/authorize?client_id=2651264628452014&redirect_uri=https://localhost:8000/auth/insta&scope=user_profile,user_media&response_type=code
	BASE_URL = "https://www.instagram.com/oauth/authorize/?"
	REDIRECT_URI = "https://localhost:8000/auth/insta"
	url = BASE_URL + "client_id={}&redirect_uri={}&scope=user_profile,user_media&response_type=code".format('2651264628452014',REDIRECT_URI)
	print(url)
	return HttpResponseRedirect(url)

REQUEST_ACCESS = "https://api.instagram.com/oauth/access_token/?"
REDIRECT_URI = "https://localhost:8000/auth/insta"
def grant_access(request):
    print("something")
    code = request.GET.get('code')
    payload = {'client_id': '2651264628452014', 'client_secret':'69caad94f800eac62357bc5783b164c6', 'grant_type':'authorization_code','redirect_uri': REDIRECT_URI, 'code': code}
    resp = requests.post(REQUEST_ACCESS, data= payload)
    response = json.loads(resp.text) 
    # print(response['user_id'],resp['access_token'],"Thisssss")
    # print(response)
    url=('https://graph.instagram.com/{}?fields=id,username&access_token={}').format(response['user_id'],response['access_token'])
    # print( HttpResponseRedirect(url))
    resp=requests.get(url)
    user_dictionary = json.loads(resp.text) 
    print(user_dictionary)
    # url2 = f"https://graph.instagram.com/{user_dictionary['id']}?fields=followers_count&access_token={response['access_token']}"
    url2 = f"https://www.instagram.com/{user_dictionary['username']}/?__a=1"
    resp2=requests.get(url2)
    res = json.loads(resp2.text)
    print(res)
    user_dictionary['followers_count'] = res['graphql']['user']['edge_followed_by']['count']

	# return HttpResponseRedirect("https://localhost:8000/")
    return render(request,'home.html',context=user_dictionary)

    
	# return HttpResponseRedirect(url)

	# return HttpResponse(response)