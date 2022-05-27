from readline import insert_text
from django.forms import model_to_dict
from django.shortcuts import redirect, render
from django.http import HttpResponse
from paginator import paginate
from app.models import *
from django.contrib import auth
from app.forms import LoginForm, SignUpForm, SettingsForm, QuestionForm, AnswerForm
from django.urls import reverse
from django.core.cache import cache
from askme.settings import LOGIN_URL
from django.core.paginator import Paginator


from django.contrib.auth.decorators import login_required


top_users = Profile.objects.get_top_users(10)


USER = {"is_auth": True}


def index(request):
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
    if request.method == "GET":
        form = QuestionForm()
    if request.method == "POST":
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            profile = Profile.objects.get(user=request.user)
            question = form.save(profile)
            return redirect("question", i=question.id)

    context = {
        "best_memb_list": top_users,
        "tags_list": Tag.objects.top_tags(10),
        "form": form
    }

    return render(request, "ask.html", context)


def question(request, i: int):
    context = {
        "best_memb_list": top_users,
        "tags_list": Tag.objects.top_tags(10),
    }
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(f'{LOGIN_URL}?continue={request.path}')
        else:
            form = AnswerForm(data=request.POST)
            if (form.is_valid):
                ans = form.save(commit=False)
                profile = Profile.objects.get(user=request.user)
                question = Question.objects.get(id=i)
                ans.profile = profile
                ans.question = question
                ans.save()

                answers = Paginator(Answer.objects.answer_by_question(i), 10)
                return redirect(f"{request.path}?page={answers.num_pages}#{ans.id}")

    if request.method == "GET":
        try:
            question = Question.objects.by_id(i)
            answers = paginate(Answer.objects.answer_by_question(i), request, 10)
            form = AnswerForm()
            context.update({
                "page_obj": answers,
                "question": question,
                "form": form
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
            profile = form.save()
            auth.login(request, profile.user)
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

    if request.user.is_authenticated:
        return redirect(next)
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
    if request.method == "GET":
        initial_data = model_to_dict(request.user)
        initial_data['avatar'] = request.user.profile.avatar
        form = SettingsForm(initial=initial_data)
    if request.method == "POST":
        initial_data = request.POST
        instance = request.user
        form = SettingsForm(request.POST, instance=instance, files=request.FILES)
        if form.is_valid():  # add check existing
            form.save()
            return redirect("settings")

    context = {
        "best_memb_list": top_users,
        "tags_list": Tag.objects.top_tags(10),
        "form": form
    }

    return render(request, "settings.html", context)


@login_required(login_url="login", redirect_field_name="continue")
def logout(request):
    auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER'))
