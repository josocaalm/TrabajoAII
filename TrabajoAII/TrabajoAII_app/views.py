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
from currency.currencies import *
from _codecs import encode
from django.contrib.auth import get_user

def cover(request):
    user= request.user
    return render_to_response("cover.html", {'cover':"active", "user":user})

def search(request):
    user= request.user
    return render_to_response("search.html", {"search": "active", "user":user})

def results(request):
    user=request.user
    try:
        query = request.GET["q"]
        if query is "":
            errorMessage = "You didn't type the name of the game."
            return render_to_response("cover.html", {"cover":"active","user":user, "errorMessage": errorMessage})
            
        driverAndGames = launch_game_list_search(query)
        currencies = ['AED','AFN','ALL','AMD','ANG','AOA','ARS','AUD','AWG','AZN','BAM','BBD','BDT','BGN','BHD','BIF','BMD','BND','BOB','BRL', 'BSD', 'BTC', 'BTN', 'BWP', 'BYR', 'BZD', 'CAD', 'CDF', 'CHF', 'CLF', 'CLP', 'CNH', 'CNY', 'COP', 'CRC', 'CUP', 'CVE', 'CZK', 'DEM', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'EUR', 'FIM', 'FJD', 'FKP', 'FRF', 'GBP', 'GEL', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG', 'HUF', 'IDR', 'IEP', 'ILS', 'INR', 'IQD', 'IRR', 'ISK', 'ITL', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF', 'KPW', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LTL', 'LVL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRO', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZN', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKG', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLL', 'SOS', 'SRD', 'STD', 'SVC', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND',
                      'TOP', 'TRY', 'TTD', 'TWD', 'TZS', 'UAH', 'UGX','USD','UYU','UZS','VEF','VND','VUV','WST','XAF','XCD','XDR','XOF','XPF','YER','ZAR','ZMK','ZMW','ZWL']
        
        gamesPrimitive = driverAndGames[1]
        games=[]
        for elem in gamesPrimitive:
            driverAndSteamID = fromTF2OutpostIDToSteamID(driverAndGames[0],elem[3])
            if driverAndSteamID != None:
                steamId = driverAndSteamID[1]
                game = Game(name = elem[0], coverString = elem[1], tf2outpostPartialID = elem[2], tf2outpostFullID = elem[3], steamID = steamId)
                if Game.objects.filter(steamID = steamId).exists() != True:
                    game.save()
                games.append(game)
        
        quitWebdriver(driverAndGames[0])
        
        return render_to_response("results.html", {'games':games, "search":"active", "query": query, "user":user, "currencies": currencies})
    except:
        errorMessage = "There was a problem while searching the game. Please do not interact with the Firefox emergent window."
        return render_to_response("cover.html", {"cover":"active","user":user, "errorMessage": errorMessage})

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
        link = "http://steampowered.com/app/" + str(steamOffer[1]) + "/?cc=" + steamOffer[2]
        return render_to_response("offers.html", {'outpostOffers':outpostOffers, "steamOffer": steamOffer, "cover": cover, "currency": currency, "user":user, "link": link, "name": name})
        
    return render_to_response("offers.html", {'outpostOffers':outpostOffers, "cover": cover, "currency": currency, "user":user, "name": name})

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

@login_required(login_url="/enter")
def rate(request):
    user = request.user
    userApp = UserApp.objects.filter(username = user.username).first()
    
    try:
        rat = request.GET["r"]
        steamId = request.GET["gameSteamId"]
        gam = Game.objects.filter(steamID = steamId).first()
        
        gameRating = Rating(rating = rat, game = gam, userApp = userApp)
        gameRating.save()
        
        message = "Game successfully rated."
        return render_to_response("cover.html", {"cover":"active","user":user, "message": message})
    except:
        errorMessage = "There was a problem while searching the game. Please do not interact with the Firefox emergent window."
        return render_to_response("cover.html", {"cover":"active","user":user, "errorMessage": errorMessage})

@login_required(login_url="/enter")
def recommend(request):
    user = request.user
    principal = UserApp.objects.filter(username = user.username).first()
    
    ratingDic1 = {}    
      
    for u in UserApp.objects.all():
        ratings = Rating.objects.all().filter(userApp = u)
        ratingDic2 = {}       
        for rating in ratings:
            ratingDic2[rating.game.name] = (rating.rating * 1.0)
        ratingDic1[u] = ratingDic2  
               
    gameMatch = calculateSimilarItems(ratingDic1)
          
    recommendations = getRecommendedItems(ratingDic1, gameMatch, principal)
    games=[]
    for rec in recommendations:
        game = Game.objects.filter(name = rec[1]).first()
        games.append(game)
            
    return render_to_response('recommend.html', {'recommendations':games, "recommend":"active", "user":user})




