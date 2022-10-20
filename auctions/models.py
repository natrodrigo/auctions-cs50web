from email.policy import default
from statistics import mode
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('AuctionListing',related_name="watchers")
    def __str__(self):
        return f"{self.username}"

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="auctions")
    image = models.URLField()
    duration = models.DateTimeField()
    initialBid = models.DecimalField(max_digits=19, decimal_places=4)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name = "auctions")

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    value = models.DecimalField(max_digits=19, decimal_places=4)
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    createDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.auction} - {self.value}"


class Comment(models.Model):
    text = models.TextField()
    createDate = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "comments")
    auctionListing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name = "auctions")

    def __str__(self):
        return f"{self.createDate} - {self.user}"
