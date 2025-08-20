from django.db import models

# Ví dụ: Tag cho câu hỏi (ManyToMany)
class Tag(models.Model):
    name = models.CharField("Tên nhãn", max_length=50)

    def __str__(self):
        return self.name

class Question(models.Model):
    question_text = models.CharField("Câu hỏi", max_length=200)
    pub_date = models.DateTimeField("Ngày phát hành")
    tags = models.ManyToManyField(Tag, related_name="questions", blank=True)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    choice_text = models.CharField("Phương án", max_length=200)
    votes = models.IntegerField("Số phiếu", default=0)

    def __str__(self):
        return self.choice_text
