from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from conversation.models import Conversation
from .forms import SignupForm, EditProfileForm, UserProfileForm, ChangePasswordForm  # Imported UserProfileForm
from payment.forms import ShippingAddressForm
from payment.models import ShippingAddress
from cart.models import Cart
from . models import UserProfile
from items.models import Category, Items

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        username = request.user.username
        user = get_object_or_404(User, username=username)
        conversations = Conversation.objects.filter(members__in=[request.user.id])
        conversation_count = conversations.count()

        # Get the cart item count for the authenticated user
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item_count = cart.items.count()
    else:
        user = None
        conversation_count = 0
        cart_item_count = 0

    items = Items.objects.filter(is_sold=False).order_by('-created_at')[0:6]
    categories = Category.objects.all()
    items = Items.objects.filter(is_sold=False).order_by('-created_at')

    return render(request, 'core/index.html', {
        'items': items,
        'categories': categories,
        'conversation_count': conversation_count,
        'user': user,
        'cart_item_count': cart_item_count,
    })

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            return redirect('/login/')
    else:
        form = SignupForm()
        profile_form = UserProfileForm()

    return render(request, 'core/signup.html', {
        'form': form,
        'profile_form': profile_form,
    })

def login_user(request):
    # if user is already logged in, redirect to index page
    if request.user.is_authenticated:
        messages.success(request, "You are already logged in")
        return redirect('core:index')
    # log in user
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Ensure user profile exists
            UserProfile.objects.get_or_create(user=user)
            return redirect('core:index')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('/login/')
    return render(request, 'core/login.html')

@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    UserProfile.objects.get_or_create(user=user)
    
    # Check if the user has any items created by them
    items = Items.objects.filter(created_by=user)

    # Handle conversations
    conversations = Conversation.objects.filter(members__in=[request.user.id])
    conversation_count = conversations.count()

    # Determine if the logged-in user is viewing their own dashboard
    is_owner = request.user == user

    # Cart item count for user
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item_count = cart.items.count()

    return render(request, 'core/profile.html', {
        'items': items,
        'user': user,
        'conversation_count': conversation_count,
        'is_owner': is_owner,
        'cart_item_count': cart_item_count,
    })

@login_required
def update_user(request): 
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        UserProfile.objects.get_or_create(user=current_user)

        # Conversations
        conversations = Conversation.objects.filter(members__in=[request.user.id])
        conversation_count = conversations.count()

        # Retrieve or create the user's shipping address
        shipping_user, created = ShippingAddress.objects.get_or_create(user=current_user)

        # Forms
        user_form = EditProfileForm(request.POST or None, instance=current_user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=current_user.userprofile)
        shipping_form = ShippingAddressForm(request.POST or None, instance=shipping_user)

        if request.method == 'POST':
            print(user_form.errors)  # Debug: Print user form errors
            print(shipping_form.errors)  # Debug: Print shipping form errors

            if user_form.is_valid() and profile_form.is_valid() and shipping_form.is_valid():
                user_form.save()
                profile_form.save()
                shipping_form.save()
                
                login(request, current_user)
                messages.success(request, 'Your profile has been updated successfully.')
                return redirect('core:index')  # Keep for redirect after successful save

        # Cart item count for user
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item_count = cart.items.count()

        return render(request, "core/update_user.html", {
            'user_form': user_form, 
            'profile_form': profile_form,
            'shipping_form': shipping_form, 
            'conversation_count': conversation_count,
            'cart_item_count': cart_item_count,
        })
    
    else:
        messages.error(request, "You must be logged in to access that page!")
        return redirect('home')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        # Get the cart item count for the authenticated user

        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item_count = cart.items.count()
        # was form filled out
        if request.method == 'POST':
            # do stuff
            form = ChangePasswordForm(current_user, request.POST)
            # check if form is valid and password matches current user's password
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been updated successfully. PLease log in again.')
                return redirect('core:login')  # Keep for redirect after successful save
            else:
                messages.error(request, 'Invalid password or new password. Please try again.')
                return render(request, "core/update_password.html", {'form': form},)
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "core/update_password.html", {'form': form, 'cart_item_count': cart_item_count},)
    else:
        messages.success(request, 'You must be logged in to change your password!')
        return redirect('/login/')




def shipping_address(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('/login/')
