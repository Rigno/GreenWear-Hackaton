from django import forms
from .models import Quiz


class QuizForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        # Pass the 'questions' parameter when initializing the form
        questions = kwargs.pop('questions', None)
        super(QuizForm, self).__init__(*args, **kwargs)

        # Add a choice field for each question
        for question in questions:
            self.fields[f'question_{ question.id }'] = forms.ModelChoiceField(
                queryset=question.answer.all(), # asnwers
                widget=forms.RadioSelect(attrs={'class': 'quiz-answer'}),
                label=question.text, # question
                empty_label=None,
                to_field_name="text"
            )
