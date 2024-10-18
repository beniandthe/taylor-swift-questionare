from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Question, Choice, Answer

# List view for displaying all poll questions
def index(request):
    # Define the variables to be passed to the template
    welcome = "Welcome to the Taylor Swift Song Questionnaire!"
    action = "/questionare/start/"  # This is the URL where the user can start the questionnaire

    # Pass the context to the template
    context = {
        'welcome': welcome,
        'action': action
    }

    # Render the 'index.html' template with the context data
    return render(request, 'questionare/index.html', context)


def start(request):
    # Fetch the first question from the database
    first_question = get_object_or_404(Question, pk=1)
    
    # Check if the question has choices
    choices = first_question.choice_set.all() if first_question else []

    # Debugging print statements (you can check these in the console)
    print("Question:", first_question)
    print("Choices:", choices)

    if request.method == 'POST':
        # Retrieve the selected choice
        selected_choice_id = request.POST.get('choice')
        selected_choice = get_object_or_404(Choice, id=selected_choice_id)

        # Create a new Answer object
        Answer.objects.create(
            question=first_question,
            selected_choice=selected_choice,
            session_id=request.session.session_key
        )

        # Redirect to the next question or results
        return redirect('questionare:next_question', question_id=first_question.id)

    return render(request, 'questionare/start.html', {
        'question': first_question,
        'choices': choices
    })


from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Choice, Answer

def next_question(request, question_id):
    # Get the current question based on the question_id parameter
    question = get_object_or_404(Question, pk=question_id)

    # Check if a POST request is being made, indicating a form submission
    if request.method == 'POST':
        selected_choice_id = request.POST.get('choice')

        if selected_choice_id:
            # Fetch the user's selected choice
            selected_choice = get_object_or_404(Choice, pk=selected_choice_id)
            # Save the answer
            Answer.objects.create(
                session_id=request.session.session_key,
                question=question,
                choice=selected_choice
            )
            
            # Find the next question if it exists
            next_question = Question.objects.filter(id__gt=question.id).first()

            if next_question:
                # Redirect to the next question if there is one
                return redirect('questionare:next_question', question_id=next_question.id)
            else:
                # Redirect to results if no more questions
                return redirect('questionare:results')

    # Render the template with the current question and its choices
    return render(request, 'questionare/next_question.html', {
        'question': question,
        'choices': question.choice_set.all(),
    })



def results(request):
    # Get all answers for the current user (or session, if not logged in)
    user_answers = Answer.objects.filter(
        session_id=request.session.session_key
    )

    # Prepare a list to hold all the songs based on user's choices
    recommended_songs = []

    # Loop through all the answers and aggregate the associated song recommendations
    for answer in user_answers:
        # Assuming the 'selected_choice' has a 'song_recommendations' field that stores the Taylor Swift songs
        recommended_songs.extend(answer.selected_choice.song_recommendations.split(','))

    # Remove any duplicates from the recommended songs
    recommended_songs = list(set(recommended_songs))

    # Render the results page with the list of recommended songs
    return render(request, 'questionare/results.html', {'recommended_songs': recommended_songs})



