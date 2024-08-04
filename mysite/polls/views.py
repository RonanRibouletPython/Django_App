# Django imports
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import F
from django.urls import reverse

# Models imports
from .models import Question, Choice

# First view used to display the 5 latest questions
def index(request):
    #return HttpResponse("Hello, world")
    # Display the 5 latest questions separated with a comma
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {
        "latest_question_list": latest_question_list
        }
    
    return render(request, "polls/index.html", context)

# Second view to show the details of the questions
def detail(request, question_id):
    
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

# Thrid view to show the results of the poll
def results(request, question_id):
    
    question = get_object_or_404(Question, pk=question_id)
    
    return render(request, "polls/results.html", {"question": question})
# Fourth view to display the question you answer
def vote(request, question_id):
    
    question = get_object_or_404(Question, pk=question_id)
    
    try:
        # request.POST is a dictionary-like object that lets you access submitted data 
        # by key name. 
        # In this case, request.POST['choice'] returns the ID of the selected choice, 
        # as a string. request.POST values are always strings.
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    
    # request.POST['choice'] will raise KeyError if choice wasn’t provided in POST data.
    # The above code checks for KeyError and redisplays the question form with an error
    # message if choice isn’t given.    
    except (KeyError, Choice.DoesNotExist):
        
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        # Instruct the DB to add the value 1 to the right entry of the table
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    
        # We are using the reverse() function in the HttpResponseRedirect constructor 
        # in this example. 
        # This function helps avoid having to hardcode a URL in the view function. 
        # It is given the name of the view that we want to pass control to and the 
        # variable portion of the URL pattern that points to that view. 
        # In this case, using the URLconf we set up in Tutorial 3, this reverse()
        # call will return a string like "/polls/3/results/" where the 3 is the value 
        # of question.id. 
        # This redirected URL will then call the 'results' view to display the final page.
