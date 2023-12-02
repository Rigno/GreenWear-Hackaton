from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms import QuizForm
from .models import Quiz


# --- QUIZ --- #
def quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.get_questions()
    user = request.user

    if request.method == 'POST':
        form = QuizForm(request.POST, questions=questions)
                
        if form.is_valid():
            
            correct = 0
            for question in questions:
                selected_answer = form.cleaned_data[f'question_{question.id}']                
                if quiz.get_correct_answer(question) == selected_answer:
                    correct = correct + 1
                    
            if correct >= len(questions)*0.6:
                messages.info(request, 'Complimenti hai vinto +{} punti!'.format(quiz.points))
                user.green_points += quiz.points
                user.save()
                return redirect('account')
            else:
                messages.info(request, 'Mi dispiace non hai passato il quiz, riprova più tardi')
                if user.quiz_lives > 0:
                    user.quiz_lives = user.quiz_lives - 1
                    user.save()
                return redirect('account')

    else:
        form = QuizForm(questions=questions)

    context = {
        'quiz': quiz,
        'questions': questions,
        'form': form,
        'lives': user.quiz_lives,
    }
    
    return render(request, 'gamification/quiz.html', context)
