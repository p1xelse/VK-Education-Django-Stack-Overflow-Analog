from askme.settings import BASE_DIR
from django.core.management.base import BaseCommand
from app.models import Question, Profile, LikeQuestion, LikeAnswer, Tag, Answer

from faker import Faker
from collections import OrderedDict
import random

from django.contrib.auth.models import User

COUNT_USERS = 10001
COUNT_QUESTIONS = 100001
COUNT_ANSWERS = 1000001
COUNT_TAGS = 10001
LIKES = 2000001


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.faker = Faker()

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.users_generate(COUNT_USERS)
        self.tags_generate(COUNT_TAGS)
        self.questions_generate(COUNT_QUESTIONS)
        self.answers_generate(COUNT_ANSWERS)
        self.likes_generate(LIKES)
        print("SUCCESS")

    def user_generate(self):
        username = self.faker.unique.user_name()
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = self.faker.email()
        password = self.faker.password()
        user = User(username=username, first_name=first_name,
                    last_name=last_name, email=email, password=password)
        return user

    def users_generate(self, count):
        print("START GENERATING USERS")
        usrs_list = list()
        profiles_list = list()
        for i in range(count):
            if (i % 10000 == 0):
                print(f"PROGRESS {i / count * 100}%")
            cur_user = self.user_generate()
            usrs_list.append(cur_user)
            profiles_list.append(Profile(user=cur_user))

        User.objects.bulk_create(usrs_list)
        Profile.objects.bulk_create(profiles_list)
        print("USER DONE")

    def tags_generate(self, count):
        print("START GENERATING TAGS")
        tag_list = list()
        for i in range(count):
            if (i % 10000 == 0):
                print(f"PROGRESS {i / count * 100}%")
            tag_name = self.faker.word()
            tag_list.append(Tag(name=tag_name))
        Tag.objects.bulk_create(tag_list)

    def questions_generate(self, count):
        print("START GENERATING QUESIONS")
        min_id_prof = Profile.objects.order_by('id')[0].id
        max_id_prof = Profile.objects.order_by('-id')[0].id

        tag_id = Tag.objects.order_by('id')[0].id
        tags_cout = Tag.objects.all().count()

        question_list = list()
        for i in range(count):
            if (i % 10000 == 0):
                print(f"PROGRESS {i / count * 100}%")
            tags_count_quiestion = random.randint(1, 5)
            text = self.faker.paragraph(random.randint(7, 20))
            profile_id = random.randint(min_id_prof, max_id_prof)
            title = self.faker.paragraph(random.randint(7, 20))

            title = self.faker.paragraph(1)[:-1] + '?'
            tag_list = list()
            cur_question = Question(
                text=text, title=title,  profile_id=profile_id)
            question_list.append(cur_question)

        q_list = Question.objects.bulk_create(question_list)
        for i in range(count):
            tags_count_quiestion = random.randint(1, 5)
            for j in range(tags_count_quiestion):
                tag = Tag.objects.get(
                    id=random.randint(tag_id, tag_id+tags_cout-1))
                q_list[i].tags.add(tag)

        print("Question DONE")

    def answers_generate(self, count):
        print("START GENERATING ANSWERS")
        min_id_prof = Profile.objects.order_by('id')[0].id
        max_id_prof = Profile.objects.order_by('-id')[0].id
        min_id_que = Question.objects.order_by('id')[0].id
        max_id_que = Question.objects.order_by('-id')[0].id

        ans_list = list()
        for i in range(count):
            if (i % 10000 == 0):
                print(f"PROGRESS {i / count * 100}%")
            text = self.faker.paragraph(random.randint(5, 20))
            profile_id = random.randint(min_id_prof, max_id_prof)
            question_id = random.randint(min_id_que, max_id_que)
            cur_ans = Answer(text=text, question_id=question_id,
                             profile_id=profile_id)
            ans_list.append(cur_ans)
        Answer.objects.bulk_create(ans_list)

    def likes_generate(self, count):
        print("START GENERATING LIKES")
        min_profile_id = Profile.objects.order_by('id')[0].id
        max_profile_id = Profile.objects.order_by('-id')[0].id
        min_question_id = Question.objects.order_by('id')[0].id
        max_question_id = Question.objects.order_by('-id')[0].id
        like_q_list = list()
        for i in range(round(count / 2)):
            if (i % 10000 == 0):
                print(f"PROGRESS {i / count * 100}%")

            while True:
                profile_id = random.randint(min_profile_id, max_profile_id)
                question_id = random.randint(min_question_id, max_question_id)
                check = LikeQuestion.objects.filter(
                    question_id=question_id, profile_id=profile_id).count()
                if not check:
                    like_q_list.append(LikeQuestion(
                        question_id=question_id, profile_id=profile_id))
                    break
        print(f"BULK CREATE LIKES {like_q_list.count()}")
        LikeQuestion.objects.bulk_create(like_q_list)

        like_a_list = list()
        min_ans_id = Answer.objects.order_by('id')[0].id
        max_ans_id = Answer.objects.order_by('-id')[0].id
        for i in range(round(count / 2)):
            if (i % 10000 == 0):
                print(f"PROGRESS {i / count * 100}%")
            while True:
                profile_id = random.randint(min_profile_id, max_profile_id)
                ans_id = random.randint(min_ans_id, max_ans_id)

                check = LikeAnswer.objects. \
                    filter(answer_id=ans_id, profile_id=profile_id).count()
                if not check:
                    like_a_list.append(LikeAnswer(
                        answer_id=ans_id, profile_id=profile_id))
                    break

        print(f"BULK CREATE LIKES {like_a_list.count()}")
        LikeAnswer.objects.bulk_create(like_a_list)
        print("Likes Done")
