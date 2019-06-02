from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Article, Client, Hashtag, Comment

URL_LOGIN="/login/"
# Create your views here.
def common_signup(request, ctx, group):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.create_user(username, email, password)
        target_group = Group.objects.get(name=group)
        user.groups.add(target_group)

        if group == "client":
            Client.objects.create(user=user, name=username)

        return redirect("/signup_cong/")

    return render(request, "signup.html", ctx)

def signup(request):
    ctx = {"is_client":True}
    return common_signup(request, ctx, "client")

def signup_cong(request):
    ctx = {}
    return render(request, "signup_cong.html", ctx)

def login(request):
    ctx = {}
    if request.method == "GET":
        pass
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            next_value = request.GET.get("next")
            if next_value:
                return redirect(next_value)
            else:
                return redirect("/")

        else:
            ctx.update({"error" : "사용자가 없습니다."})

    return render(request, "login.html", ctx)

def logout(request):
    auth_logout(request)
    return redirect("/")

def index(request):
    category = request.GET.get("category")
    hashtag = request.GET.get("hashtag")

    if not category and not hashtag:
        article_list = Article.objects.all()
    elif category:
        article_list = Article.objects.filter(category=category)
    else:
        article_list = Article.objects.filter(hashtag__name=hashtag)

    category_list = ([
        article.category for article in article_list
    ])
    hashtag_list = Hashtag.objects.all()
    ctx = {
        "article_list" : article_list,
        "category_list" : category_list,
        "hashtag_list" : hashtag_list
    }
    return render(request, "index.html", ctx)

def detail(request, article_id):

    article = Article.objects.get(id=article_id)
    ctx = {
    "article" : article,
    }
    if request.method == "GET":
        pass
    elif request.method == "POST":
        content = request.POST.get("content")
        comment = Comment.objects.create(
            article=article,
            client=request.user.client,
            content=content
        )
        return redirect("/{}/".format(article_id))

    return render(request, "detail.html", ctx)

def userpage(request, username):
    client = Client.objects.get(name=username)
    article_list = Article.objects.filter(client=client)
    ctx = {
        "article_list" : article_list,
        "client" : client
    }
    return render(request, "userpage.html", ctx)

@login_required(login_url=URL_LOGIN)
def write(request):
    ctx = {}
    if request.method == "GET":
        pass
    elif request.method == "POST":
        category = request.POST.get("category")
        title = request.POST.get("title")
        subtitle = request.POST.get("subtitle")
        content = request.POST.get("content")
        article = Article.objects.create(
            client=request.user.client,
            category=category,
            title=title,
            subtitle=subtitle,
            content=content
        )
        return redirect("/")

    return render(request, "write.html", ctx)
