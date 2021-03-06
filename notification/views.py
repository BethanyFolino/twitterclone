from django.shortcuts import render, HttpResponseRedirect, reverse
from twitteruser.models import TwitterUser
from tweet.models import Tweet
from notification.models import Notification
from twitterclone.settings import AUTH_USER_MODEL
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.decorators import login_required
from django import forms

# Create your views here.
@login_required
def notification_view(request):
    notifications = Notification.objects.all().order_by('-id')
    for notification in notifications:
        notification.delete()
    return render(request, 'notification.html', {'notifications': notifications})
