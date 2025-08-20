import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """Trả về False nếu pub_date nằm trong tương lai."""
        future_time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=future_time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """Trả về False nếu pub_date > 1 ngày trước."""
        old_time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=old_time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """Trả về True nếu trong vòng 24h vừa qua."""
        recent_time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=recent_time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_future_question(self):
        """Detail của question tương lai -> 404."""
        future_q = create_question("Future question.", days=5)
        url = reverse("polls:detail", args=(future_q.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """Detail của question quá khứ -> hiển thị text."""
        past_q = create_question("Past question.", days=-5)
        url = reverse("polls:detail", args=(past_q.id,))
        response = self.client.get(url)
        self.assertContains(response, past_q.question_text)
class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        q = create_question("Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [q])

    def test_future_question(self):
        create_question("Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_and_past_questions(self):
        past_q = create_question("Past", days=-5)
        create_question("Future", days=5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_q])

    def test_two_past_questions(self):
        older = create_question("Older", days=-5)
        newer = create_question("Newer", days=-1)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [newer, older])

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_q = create_question("Future question.", days=5)
        url = reverse("polls:detail", args=(future_q.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_q = create_question("Past question.", days=-5)
        url = reverse("polls:detail", args=(past_q.id,))
        response = self.client.get(url)
        self.assertContains(response, past_q.question_text)