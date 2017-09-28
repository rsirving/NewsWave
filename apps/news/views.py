from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers
from datetime import datetime
from .models import *

def start(request):
    init_session(request)
    if request.session['user_id'] != "":
        return redirect("/homepage")
    context = {
        'name': request.session['name'],
        'username': request.session['username'],
        'user_id': request.session['user_id']
    }
    return render(request, "start.html", context)

def login(request):
    init_session(request)
    if request.session['user_id'] != "" or request.method != "POST":
        return redirect("/homepage")
    login_result = User.objects.login(request.POST)
    errors = login_result['errors']
    request.session['username'] = request.POST['username']
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error)
        return redirect("/")
    else:
        request.session['user_id'] = login_result['user'].id
        request.session['first_name'] = extract_first_name(login_result['user'].name)
        return redirect("/homepage")

def register(request):
    init_session(request)
    if request.session['user_id'] != "" or request.method != "POST":
        return redirect("/homepage")
    register_result = User.objects.register(request.POST)
    errors = register_result['errors']
    request.session['username'] = request.POST['username']
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error)
        request.session['name'] = request.POST['name']
        return redirect("/")
    else:
        request.session['user_id'] = register_result['user'].id
        request.session['first_name'] = extract_first_name(register_result['user'].name)
        return redirect("/settings")

def logout(request):
    reset_session(request)
    return redirect("/")

def home(request):
    init_session(request)
    # get all locations, outlets, and notes connected to the specific user
    if request.session['user_id'] == "":
        return redirect("/")
    user = User.objects.get(id=request.session['user_id'])
    print user.outlets
    locations = user.locations.all()
    outlets = user.outlets.all()
    notes = user.notes.all()
    if len(locations) == 0:
        locations = None
    print outlets
    if len(outlets) == 0:
        outlets = None
    if len(notes) == 0:
        notes = None


    context = {
        'first_name': request.session['first_name'],
        'locations': locations,
        'outlets': outlets,
        'notes': notes
    }
    return render(request, "home.html", context)

def get_news(request): # maybe do this 100% on the client side
    init_session(request)

def notes(request):
    init_session(request)
    # return all notes as JSON to the client using AJAX

def reading_list(request, username):
    init_session(request)
    # TODO: add a privacy check (whether the user has indicated a preference for privacy)
    if request.session['user_id'] == "":
        return redirect("/")
    stories = User.objects.get(id=request.session['user_id']).stories.all()
    context = {
        'stories': stories
    }
    return render(request, "reading_list.html", context)

def settings(request):
    init_session(request)
    if request.method == "GET":
        outlets = User.objects.get(id=request.session['user_id']).outlets.all()
        context = {
            'outlets': outlets
        }
        return render(request, "settings.html", context)
    if request.method == "POST":
        outlet_errors = NewsOutlet.objects.outlet_validator(request.POST, request.session['user_id'])
        if len(outlet_errors):
            for tag, error in outlet_errors.iteritems():
                messages.error(request, error)
            return redirect("/settings")
        return redirect("/")

def add_story(request): # need to refactor home.html to use AJAX for this
    init_session(request)
    if request.session['user_id'] == "" or request.method != "POST":
        return redirect("/homepage")  
    story_errors = Story.objects.story_validator(request.POST, request.session['user_id'])
    if len(story_errors):
        for tag, error in story_errors.iteritems():
            messages.error(request, error)
    storys_json = serializers.serialize('json', Story.objects.all())
    return HttpResponse(storys_json, content_type='application/json')


def delete_story(request): # want to delete story entirely if only one user has saved it. Otherwise, just remove it from the specific user.stories
    init_session(request)
    if request.session['user_id'] == "" or request.method != "POST":
        return redirect("/")

def weather(request):
    init_session(request)
    
def new_note(request): 
    init_session(request)

def delete_note(request):
    init_session(request)

def init_session(request):
    if not 'user_id' in request.session:
        reset_session(request)

def reset_session(request):
        request.session['user_id'] = ""
        request.session['name'] = ""
        request.session['username'] = ""
    
def extract_first_name(name):
    try:
        space_index = name.index(" ")
        if space_index > 0:
            return name[:space_index]
    except:
        pass
    return name