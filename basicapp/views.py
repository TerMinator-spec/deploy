from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import  render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import  render, redirect
from django.contrib.auth import login, authenticate #add this
from django.contrib.auth.forms import AuthenticationForm
from .models import client
from home.models import Profile
from ecommerceapp.models import Product
from .scraper2 import FyersApiClient
from .scalping_noon import FyersTradingBot
from fyers_api import fyersModel
from fyers_api import accessToken
import numpy as np
import pandas as pd
import numpy as np
from datetime import datetime, date, time, timedelta
import time as t
import requests
import json
import requests
import pyotp
from urllib import parse
import sys
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def other(request):
    return render(request,"basicapp/other.html")

def relative(request):
    return render(request,"basicapp/relative_url.html")



from .forms import ClientForm


@login_required
def add_client(request):
    if request.method == 'POST':
        # cli = client.objects.filter(user=request.user)
        # if(len(cli)==0):
            
        form = ClientForm(request.POST)
        if form.is_valid():
            # instance = form.save(commit=False)
            # instance.user = request.user  # Assign the logged-in user to the 'user' field
            # instance.save()
            form.instance.user = request.user
            form.save()
            return redirect('/relative')
    else:
        form = ClientForm()
    return render(request, 'basicapp/add_client.html', {'form_client': form})




from django.http import JsonResponse


def run_bot(request):
    profile = Profile.objects.filter(user = request.user).first()
    cli = client.objects.filter(user=request.user)

    if(profile.is_pro == False):
        messages.warning(request,"Take Subscription first")
        return redirect('/become_pro/')

    #if request.method == 'POST' and 'run_script' in request.POST and profile.is_pro == True:
    if request.user.is_authenticated and profile.is_pro == True:

        day=datetime.now()
        tday=datetime.strftime(day, '%Y-%m-%d')
        yday=datetime.strftime(day - timedelta(1), '%Y-%m-%d')  

        if(day.strftime("%A")=='Sunday'):
            tday=datetime.strftime(day - timedelta(2), '%Y-%m-%d') 
            yday=datetime.strftime(day - timedelta(3), '%Y-%m-%d')
            
        elif(day.strftime("%A")=='Saturday'):
            tday=datetime.strftime(day - timedelta(1), '%Y-%m-%d') 
            yday=datetime.strftime(day - timedelta(2), '%Y-%m-%d')
            
        elif(day.strftime("%A")=='Monday'):
            yday=datetime.strftime(day - timedelta(3), '%Y-%m-%d')
        
        #token=get_access()
        
        #extra
        #user_profile = UserProfil.objects.get(user=request.user)

        # Use the retrieved UserProfile to query related objects in YourAnotherModel
        print(request.user)
        cli = client.objects.filter(user=request.user)
        print(cli[0].user)
        fy_id = cli[0].fy_id
        app_id_type = cli[0].app_id_type
        totp_key = cli[0].totp_key
        pin = cli[0].pin
        app_id = cli[0].app_id
        redirect_uri = cli[0].redirect_uri
        app_type = cli[0].app_type
        app_id_hash = cli[0].app_id_hash

        fyers_api_client = FyersApiClient(fy_id, app_id_type, totp_key, pin, app_id, redirect_uri, app_type, app_id_hash)
        token = fyers_api_client.get_access_token()
        #extra
        print(token)
        #cli=client.objects.all().values()
        client_id=cli[0].Client_id
        secret_key=cli[0].Secret_key
        access_token=token[15:]
        trading_bot = FyersTradingBot(client_id, access_token,tday)
        trading_bot.two_five()

    # else:
    #     messages.warning(request,"Take Subscription first")
    #     return redirect('/become_pro/')


    return render(request, 'basicapp/run_code.html')
         
def straddle_bot(request):
    profile = Profile.objects.filter(user = request.user).first()
    cli = client.objects.filter(user=request.user)

    if(profile.is_pro == False):
        messages.warning(request,"Take Subscription first")
        return redirect('/become_pro/')

    #if request.method == 'POST' and 'run_script' in request.POST and profile.is_pro == True:
    if request.user.is_authenticated and profile.is_pro == True:

        day=datetime.now()
        tday=datetime.strftime(day, '%Y-%m-%d')
        yday=datetime.strftime(day - timedelta(1), '%Y-%m-%d')  

        if(day.strftime("%A")=='Sunday'):
            tday=datetime.strftime(day - timedelta(2), '%Y-%m-%d') 
            yday=datetime.strftime(day - timedelta(3), '%Y-%m-%d')
            
        elif(day.strftime("%A")=='Saturday'):
            tday=datetime.strftime(day - timedelta(1), '%Y-%m-%d') 
            yday=datetime.strftime(day - timedelta(2), '%Y-%m-%d')
            
        elif(day.strftime("%A")=='Monday'):
            yday=datetime.strftime(day - timedelta(3), '%Y-%m-%d')
        
        #token=get_access()
        
        #extra
        #user_profile = UserProfil.objects.get(user=request.user)

        # Use the retrieved UserProfile to query related objects in YourAnotherModel
        print(request.user)
        cli = client.objects.filter(user=request.user)
        print(cli[0].user)
        fy_id = cli[0].fy_id
        app_id_type = cli[0].app_id_type
        totp_key = cli[0].totp_key
        pin = cli[0].pin
        app_id = cli[0].app_id
        redirect_uri = cli[0].redirect_uri
        app_type = cli[0].app_type
        app_id_hash = cli[0].app_id_hash

        fyers_api_client = FyersApiClient(fy_id, app_id_type, totp_key, pin, app_id, redirect_uri, app_type, app_id_hash)
        token = fyers_api_client.get_access_token()
        #extra
        print(token)
        #cli=client.objects.all().values()
        client_id=cli[0].Client_id
        secret_key=cli[0].Secret_key
        access_token=token[15:]
        trading_bot = FyersTradingBot(client_id, access_token,tday)
        trading_bot.straddle()

    # else:
    #     messages.warning(request,"Take Subscription first")
    #     return redirect('/become_pro/')


    return render(request, 'basicapp/run_code.html')
         


def prod(request):

    allProds = []
    catprods = Product.objects.values('category','id')
    print(catprods)
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod= Product.objects.filter(category=cat)
        # n=len(prod)
        # nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod])

    params= {'allProds':allProds}

    return render(request,"run_code.html",params)
