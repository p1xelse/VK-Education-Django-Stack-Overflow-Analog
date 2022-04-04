import struct
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

TEXT = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
ANSWERS = ["It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English."] * 10

QUESTIONS = [
    {
        "title": f"How to build a moon park? {i}",
        "text": f"This is text for question #{i}\n{TEXT}",
        "number": i,
        "tag": {"math", "oop" if i % 2 else "pudge"},
        "hot": True if (i % 2 == 0) else False,
        "answers_count": 10,
        "answers": ANSWERS
    } for i in range(10)
]


def index(request):
    return render(request, "index.html", {"questions": QUESTIONS, "page_title": "New questions"})


def ask(request):
    return render(request, "ask.html")


def question(request, i: int):
    return render(request, "question.html", {"question": QUESTIONS[i]})


def hot_questions(request):
    questions_hot = filter(lambda x: x["hot"] == True, QUESTIONS)
    return render(request, "index.html", {"questions": questions_hot, "page_title": "Hot questions"})


def questions_with_tag(request, tag: str):
    question_with_tag = filter(lambda x: tag in x["tag"], QUESTIONS)
    return render(request, "index.html", {"questions": question_with_tag, "page_title": f"Tag: {tag}"})


def signup(request):
    return render(request, "signup.html")


def login(request):
    return render(request, "login.html")
