import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question
from django.contrib.auth.models import User

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionModelTests(TestCase):
    def tests_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        self.client.force_login(User.objects.create_user("testuser"))
        response = self.client.get(reverse("testpolls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])

    def test_past_question(self):
        self.client.force_login(User.objects.create_user("testuser"))
        question = create_question(question_text="Past question", days=-30)
        response = self.client.get(reverse("testpolls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[question])

    def test_future_question(self):
        self.client.force_login(User.objects.create_user("testuser"))
        create_question(question_text="Future Question", days=30)
        response = self.client.get(reverse("testpolls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])

    def test_future_question_and_past_question(self):
        self.client.force_login(User.objects.create_user("testuser"))
        question = create_question(question_text="Past question", days=-30)
        create_question(question_text="Future Question", days=30)
        response = self.client.get(reverse("testpolls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[question])

    def test_two_past_question(self):
        self.client.force_login(User.objects.create_user("testuser"))
        question1 = create_question(question_text="Past question 1", days=-30)
        question2 = create_question(question_text="Past question 2", days=-5)
        response = self.client.get(reverse("testpolls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[question2, question1])

    def test_no_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("testpolls:index"))
        self.assertEqual(response.url, reverse("testpolls:login"))

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        self.client.force_login(User.objects.create_user("testuser"))
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("testpolls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        self.client.force_login(User.objects.create_user("testuser"))
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("testpolls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_no_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("testpolls:index"))
        self.assertEqual(response.url, reverse("testpolls:login"))
