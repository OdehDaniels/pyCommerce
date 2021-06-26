from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listings, Bids, Comments
from .forms import ListingForm, BidForm


def index(request):
    return render(request, "auctions/index.html", {
        'listings': Listings.objects.filter(closed=False),
        'title': 'Active Listings'
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='/login')
def createListing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        try:
            new_listing = form.save(commit=False)
            assert request.user.is_authenticated
            new_listing.owner = request.user
            new_listing.save()
            messages.success(request, "Thanks, your listing has been saved!")
            return HttpResponseRedirect(reverse("index"))

        except ValueError:
            pass

    else:
        form = ListingForm()
    return render(request, "auctions/create-listing.html", {
        "form": form
    })

def list(request, list_id, bid_form=None):

    listing = Listings.objects.get(pk=list_id)
    print(listing.closed)
    if request.user.is_authenticated:
        is_watch_list = request.user.watchlist_items.filter(pk=list_id).exists()

        # if bid form was passed to us already, we likely want to produce an error from create bid route.
        if not bid_form:
            bid_form = BidForm()

        is_mine = listing.owner == request.user
    else:
        is_watch_list = None
        bid_form = None
        is_mine = None

    return render(request, "auctions/listing.html", {
        'listing': listing,
        'is_watchlist': is_watch_list,
        'form': bid_form,
        'is_mine': is_mine
    })


