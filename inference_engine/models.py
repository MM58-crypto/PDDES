from django.db import models


# Create your models here.
class GHQ12Question(models.Model):
    question_text = models.CharField(max_length=200)
    def __str__(self):
        return self.question_text

class GHQ12Response(models.Model):
    question = models.ForeignKey(GHQ12Question, on_delete=models.CASCADE)
    response = models.IntegerField(choices=((0, 'Better than usual'), (1, 'No more than usual'), (2, 'Rather more than usual'), (3, 'Much more than usual')))

    def __str__(self):
        return f"{self.question}: {self.response}"
