from django.shortcuts import render


# --- QUIZ --- #
def quiz(request, slug):
    
    context = {
        
    }
    return render(request, 'gamification/quiz.html', context)
