from django.shortcuts import redirect, render
from django.http import HttpResponse
from paginator import paginate
from app.models import *


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
        "auth": USER['is_auth']
    }

    return render(request, "index.html", context)


def ask(request):
    return render(request, "ask.html", {"tags_list": Tag.objects.top_tags(10),
                                        "best_memb_list": top_users, "user": USER, })


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
        return render(request, "not_found.html", context)
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
        "auth": USER['is_auth']
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
        return render(request, "not_found.html", context)

    return render(request, "index.html", context)


def signup(request):
    context = {
        "best_memb_list": top_users,
        "tags_list": Tag.objects.top_tags(10),
        "auth": False
    }
    return render(request, "signup.html", context)


def login(request):
    context = {
        "best_memb_list": top_users,
        "tags_list": Tag.objects.top_tags(10),
        "auth": False
    }
    return render(request, "login.html", context)


def settings(request):
    context = {
        "best_memb_list": top_users,
        "tags_list": Tag.objects.top_tags(10),
        "auth": True
    }
    return render(request, "settings.html", context)


def logout(request):
    USER['is_auth'] = False
    return redirect(index)
