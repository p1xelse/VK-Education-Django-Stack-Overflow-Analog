from django.shortcuts import redirect, render
from django.http import HttpResponse
from paginator import paginate
from app.models import *
from django.contrib import auth
from app.forms import LoginForm, SignUpForm
from django.urls import reverse
from django.core.cache import cache

from django.contrib.auth.decorators import login_required


top_users = Profile.objects.get_top_users(10)


USER = {"is_auth": True}


def index(request):
    print(request.user)
    questions = Question.objects.new()
    page_obj = paginate(questions, request, 10)
    top_tags = Tag.objects.top_tags(10)
    context = {
        "page_obj": page_obj,
        "best_memb_list": top_users,
        "page_title": "New questions",
        "tags_list": top_tags,
    }

    return render(request, "index.html", context)


@login_required(login_url="login", redirect_field_name="continue")
def ask(request):
    print(request.user)
    return render(request, "ask.html", {"tags_list": Tag.objects.top_tags(10),
                                        "best_memb_list": top_users})


def question(request, i: int):
    context = {
        "best_memb_list": top_users,
        "tags_list": Tag.objects.top_tags(10),
        "auth": USER['is_auth']
    }
    try:
        question = Question.objects.by_id(i)
        answers = paginate(Answer.objects.answer_by_question(i), request, 10)
        context.update({
            "page_obj": answers,
            "question": question,
        })
    except Exception:
        return render(request, "not_found.html", context, status=404)
    return render(request, "question.html", context)


def hot_questions(request):
    questions = Question.objects.hot()
    page_obj = paginate(questions, request, 10)
    top_tags = Tag.objects.top_tags(10)
    context = {
        "page_obj": page_obj,
        "best_memb_list": top_users,
        "page_title": "Hot questions",
        "tags_list": top_tags,
    }

    return render(request, "index.html", context)


def questions_with_tag(request, tag: str):
    context = {
        "best_memb_list": top_users,
        "tags_list": Tag.objects.top_tags(10),
        "auth": USER['is_auth']
    }
    try:
        questions = Question.objects.by_tag(tag)
        print(questions.count())
        if (questions.count() == 0):
            raise Question.DoesNotExist("asdasd")
        page_obj = paginate(questions, request, 10)
        context.update({
            "page_obj": page_obj,
            "page_title": f"Tag: {tag}",
        })
    except Exception:
        return render(request, "not_found.html", context, status=404)

    return render(request, "index.html", context)


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "GET":
        form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(data=request.POST)
        if form.is_valid():  # add check existing
            user = form.save()
            auth.login(request, user)
            return redirect("home")

    context = {
        "best_memb_list": top_users,
        "tags_list": Tag.objects.top_tags(10),
        "form": form
    }
    return render(request, "signup.html", context)


def login(request):
    next = request.GET.get("continue")
    if not next:
        next = "home"
    print("next = ", next)

    if request.user.is_authenticated:
        return redirect(next)
    # print(request.POST)
    if request.method == "GET":
        form = LoginForm()
        cache.set("continue", next)
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)

            if user:
                auth.login(request, user)

                next_url = cache.get('continue')
                if not next_url:
                    next_url = "home"

                cache.delete('continue')
                print("next = ", next_url)
                return redirect(next_url)
            else:
                form.add_error(None, "Invalid password or login!")
                form.add_error('username', "")
                form.add_error('password', "")

    context = {
        "best_memb_list": top_users,
        "tags_list": Tag.objects.top_tags(10),
        "form": form
    }
    return render(request, "login.html", context)


@login_required(login_url="login", redirect_field_name="continue")
def settings(request):
    context = {
        "best_memb_list": top_users,
        "tags_list": Tag.objects.top_tags(10),
        "auth": True
    }
    return render(request, "settings.html", context)


def logout(request):
    auth.logout(request)
    return redirect(reverse("home"))
