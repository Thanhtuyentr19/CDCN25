from django.db import models

class Question(models.Model):
    question_text = models.CharField("Câu hỏi", max_length=200)
    pub_date = models.DateTimeField("Ngày phát hành")

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    choice_text = models.CharField("Phương án", max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
