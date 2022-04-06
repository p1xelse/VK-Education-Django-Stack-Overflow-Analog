import struct
from django.shortcuts import render
from django.http import HttpResponse
from paginator import paginate
# Create your views here.

TEXT = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
ANSWERS = ["It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English."] * 20
TAGS = ["OOP", "Math", "Cg", "Web"]
BEST_MEMBS = ["Lina", "Pudge", "You", "MrFreeman"]

QUESTIONS = [
    {
        "title": f"How to build a moon park? {i}",
        "text": f"This is text for question #{i}\n{TEXT}",
        "number": i,
        "tag": {"Math", "OOP" if i % 2 else "Cg"},
        "hot": True if (i % 2 == 0) else False,
        "answers_count": 20,
        "answers": ANSWERS
    } for i in range(20)
]

USER = {"is_authenticated": True, "name": "Vasya Pipkin"}


def index(request):
    page_obj = paginate(list(QUESTIONS), request, 5)
    return render(request, "index.html", {"page_obj": page_obj, "page_title": "New questions", "tags_list": TAGS, "user": USER, "best_memb_list": BEST_MEMBS})


def ask(request):
    return render(request, "ask.html", {"tags_list": TAGS, "best_memb_list": BEST_MEMBS})


def question(request, i: int):
    answers = paginate(list(QUESTIONS[i]["answers"]), request, 5)
    return render(request, "question.html", {"page_obj": answers, "question": QUESTIONS[i], "tags_list": TAGS, "best_memb_list": BEST_MEMBS})


def hot_questions(request):
    questions_hot = filter(lambda x: x["hot"] == True, QUESTIONS)
    page_obj = paginate(list(questions_hot), request, 5)
    return render(request, "index.html", {"page_obj": page_obj, "page_title": "Hot questions", "tags_list": TAGS, "best_memb_list": BEST_MEMBS})


def questions_with_tag(request, tag: str):
    question_with_tag = filter(lambda x: tag in x["tag"], QUESTIONS)
    page_obj = paginate(list(question_with_tag), request, 5)
    return render(request, "index.html", {"page_obj": page_obj, "page_title": f"Tag: {tag}", "tags_list": TAGS, "best_memb_list": BEST_MEMBS})


def signup(request):
    return render(request, "signup.html", {"tags_list": TAGS, "best_memb_list": BEST_MEMBS})


def login(request):
    return render(request, "login.html", {"tags_list": TAGS, "best_memb_list": BEST_MEMBS})
