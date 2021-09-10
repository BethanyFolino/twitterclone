from django.shortcuts import render, HttpResponseRedirect, reverse
from twitteruser.models import TwitterUser
from tweet.forms import CreateTweetForm
from tweet.models import Tweet
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from twitterclone.settings import AUTH_USER_MODEL
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django import forms

# Create your views here.
@login_required
def homepage(request):
    # all tweets
    tweets = Tweet.objects.all().order_by('-id')
    # only current user's tweets
    users_tweets = Tweet.objects.filter(created_by=request.user)
    # count of tweets created by current user
    tweet_count = users_tweets.count()
    # tweets from users current user is following
    following = request.user.following.values_list('id')
    following_tweets = []
    for item in following:
        follow_id = item[0]
        individual_tweets = Tweet.objects.filter(created_by_id=follow_id)
        following_tweets.append(individual_tweets[0])
    print(following_tweets)
    return render(request, 'homepage.html', {'tweets': tweets, 'users_tweets': users_tweets, 'following_tweets': following_tweets, 'tweet_count': tweet_count})

def create_tweet(request):
    if request.method == 'POST':
        form = CreateTweetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Tweet.objects.create(
                text=data['text'],
                created_by=request.user,
            )
            return HttpResponseRedirect(reverse('home'))
    form = CreateTweetForm()
    return render(request, 'tweet_form.html', {'form': form})


def tweet_detail(request, id):
    tweet = Tweet.objects.get(id=id)
    return render(request, 'tweet_detail.html', {'tweet': tweet})
