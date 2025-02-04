from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from items.models import Items
from cart.models import Cart

from django.contrib.auth.models import User

from conversation.models import Conversation
# Create your views here.


# @login_required
# def index(request):
#     items = Items.objects.filter(created_by=request.user)
#     return render(request, 'dashboard/index.html', {'items': items})



@login_required
def index(request, username):
    user = get_object_or_404(User, username=username)
    
    # Check if the user has any items created by them
    items = Items.objects.filter(created_by=user)

    # Handle conversations
    conversations = Conversation.objects.filter(members__in=[request.user.id])
    conversation_count = conversations.count()

    # Determine if the logged-in user is viewing their own dashboard
    is_owner = request.user == user

    # Get the cart item count for the authenticated user
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    cart_item_count = sum(item.quantity for item in cart_items)

    return render(request, 'dashboard/index.html', {
        'items': items,
        'user': user,
        'conversation_count': conversation_count,
        'is_owner': is_owner,
        'cart_item_count': cart_item_count,
        'cart_items': cart_items,
    })