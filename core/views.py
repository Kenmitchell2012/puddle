from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.models import User


from conversation.models import Conversation

from .forms import SignupForm

from items.models import Category, Items
# Create your views here.

def index(request):
    username = request.user.username
    user = get_object_or_404(User, username=username)
    items = Items.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()
    items = Items.objects.filter(is_sold=False).order_by('-created_at')
    conversations = Conversation.objects.filter(members__in=[request.user.id])
    conversation_count = conversations.count()

    return render(request, 'core/index.html', {'items':items, 'categories':categories, 'conversation_count':conversation_count, 'user':user})

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {'form':form})

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('/login/')