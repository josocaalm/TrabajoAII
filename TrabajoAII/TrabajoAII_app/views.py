# Create your views here.
from django.shortcuts import render_to_response, render, HttpResponseRedirect
from django.http import HttpResponse
from TrabajoAII_app.models import *
from django.template import RequestContext
from TrabajoAII_app.forms import *
from TrabajoAII_app.recommendations import *
from launch.launch import *
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

def cover(request):
    return render_to_response("cover.html", {'cover':"active"})

def search(request):
    return render_to_response("search.html", {"search": "active"})

def results(request):
    query = request.GET["q"]
    games = launch_game_list_search(query)[1]
    
    return render_to_response("results.html", {'games':games, "query": query})

def offers(request):
    fullGameId = request.GET["fullId"]
    option = request.GET["option"]
    name = ""
    
    if option == "option_1":
        outpostOffers = launch_fast_offer_search(name, fullGameId)
        
    return render_to_response("offers.html", {'outpostOffers':outpostOffers})

def contact(request):
    return render_to_response("contact.html", {"contact": "active"})

def login(request):
    message = None
    user = None
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username = username, password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return render_to_response('cover.html',{'user': user})
                else:
                    message = "Tu usuario esta inactivo"
            else:
                message = "Nombre de usuario y/o password incorrectos"
    else:
        form = loginForm()
        return render_to_response('login.html',{'message': message,'form':form}, context_instance= RequestContext(request))
    pass 

def logout(request):
    auth.logout(request)
    return render_to_response('cover.html')
  
# #Apartado b)
# def list_users(request):
#     users = UserApp.objects.all()
#     itemRats = ItemRating.objects.all()
#      
#     return render_to_response("users.html", {'users':users, 'itemRats':itemRats})
#  
# #Apartado c)
#  
# def recommend(request):
#     if request.method == 'POST':
#         form = SearchUserForm(request.POST)
#         if form.is_valid():
#             username2 = request.POST['username']    
#             userEntrada = UserApp.objects.all().filter(username = username2)
#             co=""
#             for userAux in userEntrada:
#                 co=userAux
#              
#             users = UserApp.objects.all()      
#      
#             ratingDic1 = {}    
#              
#             for user in users:
#                 itemsRating = ItemRating.objects.all().filter(user = user)
#                 ratingDic2 = {}       
#                 for rating in itemsRating:
#                     ratingDic2[rating.item.name] = (rating.rating * 1.0)
#                 ratingDic1[user] = ratingDic2  
#                       
#             itemMatch = calculateSimilarItems(ratingDic1)
#                  
#             recommendations = getRecommendedItems(ratingDic1, itemMatch, co)
#               
#                       
#             return render_to_response('recommend.html', {'recommendations':recommendations,'showForm':False}, 
#                                       context_instance=RequestContext(request))       
#                      
#     else:
#         form = SearchUserForm()
#      
#     return render_to_response('recommend.html',{'form':form,'showForm':True}, context_instance=RequestContext(request))






