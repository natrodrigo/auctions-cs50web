from xml.etree.ElementTree import Comment
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from .models import Category, User, AuctionListing, Comment, Bid
from .forms import AuctionListingForm, CommentForm

def index(request):
    auctions = AuctionListing.objects.all()
    return render(request, "auctions/index.html",{
        "auctions":auctions
    })

@login_required(login_url="login")
def create_new_listing(request):

    if request.method == 'POST':

        form = AuctionListingForm(request.POST, request.FILES)
        if form.is_valid():
            
            auction = form.save(commit=False)
            auction.user = User.objects.get(id=request.user.id)
            auction.save()
            return HttpResponseRedirect(reverse("auction",kwargs={"auction_id": auction.id}))

        else:
            return render(request, "auctions/createnewlisting.html", {
                "form": form
            })

    else:
        return render(request, "auctions/createnewlisting.html",{
            "form": AuctionListingForm()
        })

@login_required(login_url="login")
def my_auctions(request):
    my_auctions = AuctionListing.objects.filter(user = request.user)
    return render(request,"auctions/my_auctions.html", {
        "my_auctions" : my_auctions
    })

@login_required(login_url="login")
def my_watchlist(request):
    user = User.objects.get(id=request.user.id)
    return render(request,"auctions/my_watchlist.html",{
        "my_watchlist" : user.watchlist.all()
    })

@login_required(login_url="login")
def remove_from_watchlist(request, auction_id):
    auction = AuctionListing.objects.get(id = auction_id)
    user = User.objects.get(id=request.user.id)
    user.watchlist.remove(auction)

    return render(request,"auctions/my_watchlist.html",{
        "my_watchlist" : user.watchlist.all()
    })

@login_required(login_url="login")
def add_to_watchlist(request, auction_id):
    auction = AuctionListing.objects.get(id = auction_id)
    user = User.objects.get(id=request.user.id)
    user.watchlist.add(auction)

    return render(request,"auctions/my_watchlist.html",{
        "my_watchlist" : user.watchlist.all()
    })

@login_required(login_url="login")
def add_comment (request, auction_id):

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = User.objects.get(id=request.user.id)
        comment.auctionListing = AuctionListing.objects.get(id = auction_id)
        comment.save()
        return HttpResponseRedirect(reverse("auction", kwargs={"auction_id": auction_id}))


def auction(request, auction_id):
    auction = AuctionListing.objects.get(id = auction_id)
    user = User.objects.get(id=request.user.id)
    comments = Comment.objects.filter(auctionListing = auction).all()
    comment_form = CommentForm()
    auction_already_on_watchlist = user.watchlist.filter(id = auction_id).all().exists()
    

    last_bid = auction.bids.order_by('createDate').last()
    return render(request, "auctions/auction.html",{
        "auction":auction,
        "last_bid":last_bid,
        "auction_already_on_watchlist": auction_already_on_watchlist,
        "comments": comments,
        "comment_form": comment_form
    })

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories" : categories
    })

def category_auctions(request,category_id):
    category = Category.objects.get(id=category_id)
    auctions = category.auctions.all()
    return render(request,"auctions/auction_category.html",{
        "auctions": auctions
    })

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

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
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
        
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

