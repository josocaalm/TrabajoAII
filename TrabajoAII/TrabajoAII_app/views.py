# Create your views here.
from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from TrabajoAII_app.models import *
from django.template import RequestContext
from TrabajoAII_app.forms import SearchUserForm
from TrabajoAII_app.recommendations import *


def index(request):
    return render_to_response("index.html")

#Apartado a)
# def list_items(request):
#     items = Item.objects.all()
#     return render_to_response("items.html", {'items':items})
#  
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






