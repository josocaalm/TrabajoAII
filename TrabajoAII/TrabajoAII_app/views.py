# Create your views here.
from smtplib import SMTP_SSL, SMTPAuthenticationError
from email.header    import Header
from getpass import getpass
from email.mime.text import MIMEText
from django.shortcuts import render_to_response, get_object_or_404, render, HttpResponseRedirect
from TrabajoAII_app.models import *
from django.template import RequestContext
from TrabajoAII_app.forms import *
from TrabajoAII_app.recommendations import *
from launch.launch import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
from _codecs import encode

def cover(request):
    user= request.user
    return render_to_response("cover.html", {'cover':"active", "user":user})

def search(request):
    user= request.user
    return render_to_response("search.html", {"search": "active", "user":user})

def results(request):
    user= request.user
    query = request.GET["q"]
    driverAndGames = launch_game_list_search(query)
    quitWebdriver(driverAndGames[0])
    
    return render_to_response("results.html", {'games':driverAndGames[1], "query": query, "user":user})

def offers(request):
    user= request.user
    fullGameId = request.GET["fullId"]
    option = request.GET["option"]
    name = request.GET["name"]
    currency = request.GET["currency"]
    cover = request.GET["cover"]
    
    outpostOffers = launch_tf2outpost_offer_search(name, fullGameId, currency)
    if option == "complete":
        steamOffer = launch_steam_best_offer(fullGameId, currency)
        return render_to_response("offers.html", {'outpostOffers':outpostOffers, "steamOffer": steamOffer, "cover": cover, "currency": currency, "user":user})
    
    return render_to_response("offers.html", {'outpostOffers':outpostOffers, "cover": cover, "currency": currency, "user":user})

def signin(request):

    registered = False
    if request.user.is_authenticated():
        user= request.user
        registered = True
        return render_to_response('cover.html',{'registered': registered,"user":user})
    else:
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                user = UserApp(password =  make_password(form.cleaned_data['password']), username = form.cleaned_data['username'],
                                first_name = form.cleaned_data['first_name'], last_name = form.cleaned_data['last_name'],
                                email = form.cleaned_data['email'])
                user.save()
                user = auth.authenticate(username = form.cleaned_data['username'], password=form.cleaned_data['password'])
                login(request, user)
                user= request.user
                message= "Registration successfully completed!"
                return render_to_response('cover.html',{"cover":"active", "user":user, "message":message})
            else:
                return render_to_response('signin.html',{'form':form}, context_instance=RequestContext(request))
        else:
            form = UserForm()
            return render_to_response('signin.html',{'form':form}, context_instance=RequestContext(request))

#python -m smtpd -n -c DebuggingServer localhost:1025
def contact(request):
    user= request.user
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            
            login= "realgamerz2015@gmail.com"
            password = "popovici"

            recipients = ["jaylodet@gmail.com", "boliri@gmail.com"]
            subject = form.cleaned_data['subject'] 
            body = "Message from "+form.cleaned_data['sender'] + ": \n\n" + form.cleaned_data['body']
                
            msg = MIMEText(body, 'plain', 'utf-8')
            msg['Subject'] = Header(subject, 'utf-8')
            msg['From'] = login
            msg['To'] = ", ".join(recipients)
            
            try:
                s = SMTP_SSL('smtp.gmail.com', 465)
                s.set_debuglevel(1)
                s.login(login, password)
                s.sendmail(login, recipients, msg.as_string())
                s.quit()
                message="Message successfully sent. Thanks for helping us to improve our site!"
                return render_to_response('cover.html',{"cover":"active", "user":user, "message":message})
            except:
                errorMessage="Sorry, it wasn't possible to send the message, try again later."
                return render_to_response('cover.html',{"cover":"active", "user":user, "errorMessage":errorMessage})
        else:
            return render_to_response('contact.html',{"contact": "active",'form':form,"user":user}, context_instance=RequestContext(request))
    else:
        form = ContactForm()
    return render_to_response('contact.html',{"contact": "active",'form':form ,"user":user}, context_instance=RequestContext(request))

def enter(request):
    message = None
    user = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username = username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render_to_response('cover.html',{'user': user, "cover": "active"})
                else:
                    message = "Your user is inactive"
            else:
                message = "Incorrect name and/or password"
        
    else:
        form = LoginForm()
    return render_to_response('login.html',{'message': message,'form':form, "login": "active"}, context_instance= RequestContext(request))

@login_required(login_url="/enter")
def exitt(request):
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






