from django.db import models


class Quiz(models.Model):
    points = models.PositiveIntegerField(default=5)
    data = models.DateField(auto_now_add=True, editable=False)
    
    def __str__(self):
        return 'Quiz{0}'.format(self.id)
    
    def get_questions(self):
        return self.question.all()

    def get_correct_answer(self, question):
        return question.answer.get(is_correct=True)
    
    class Meta:
        verbose_name = "quiz"
        verbose_name_plural = "quiz"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='question')
    text = models.TextField(max_length=255)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
