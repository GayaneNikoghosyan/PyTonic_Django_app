''' PyTonic is WEB BASED Quiz Game, with a list of questions and 4 answers which are shown each time for user to select.
Only one option is correct. If player selects the correct option, he's passing to next question,
if player fail, he loose the game and need to start over.'''

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm
from django.contrib import messages
from .models import QuesModel
import random


# View for landing page
def landing(request):
    return render(request, "myapp/landing.html", {})


# View for registration page
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful.")
            return redirect("/login")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = RegisterForm()
    return render(request, "myapp/register.html", {"form": form})


# View for login page
def Login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/welcome')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'myapp/login.html', {})


# View for logout page
def Logout(request):
    logout(request)
    return redirect('/')


# View for welcome page
def welcome(request):
    return render(request, "myapp/welcome.html", {})


# View for home page
def home(request):
    return render(request, "myapp/home.html", {})


# defining random id number to display questions in random order and counting the score at the same time
id_set = {1}
def random_number():
    while len(id_set) < 50:
        quesID = random.randint(2, 50)
        if quesID not in id_set:
            score = len(id_set)
            data_list = [quesID, score]
            id_set.add(quesID)
            return data_list
        else:
            continue
    return [1, 50]

# track the score and count the average value
scoreList = []

def averageScore():
   average = sum(scoreList)/len(scoreList)
   if average <= 16.7:
       return f"You have LOW average score"
   elif 16.7 < average <= 33.4:
       return f"You have MIDDLE average score"
   elif 33.4 < average <= 50:
       return f"You have HIGH average score"


# function to display questions one by one
def question(request, question_id):

    # checking if request method is Post
    if request.method == 'POST':
        request.session['score'] = 0
        # calling random_number function
        ID, score = random_number()

        # comparing the request answer with the correct answer
        if QuesModel.objects.get(id=question_id).ans == request.POST.get(QuesModel.objects.get(id=question_id).question):
            request.session['score'] = score
            if score == 50:
                score, percent = 50, 100

                # add score to the score_list
                global scoreList
                scoreList.append(score)
                avgScore = averageScore()
                context = {'score': score, 'percent': percent, 'average': avgScore}

                # reset the score
                global id_set
                id_set = {1}
                request.session['score'] = 0
                return render(request, 'myapp/result.html', context)
            return redirect(f"/question/{ID}")
        else:
            score = score - 1

            # add score to the score_list
            scoreList.append(score)
            avgScore = averageScore()
            percent = int(score * 100 / 50)
            context = {'score': score, 'percent': percent, 'average': avgScore}

            # reset the score
            id_set = {1}

            request.session['score'] = 0
            return render(request, 'myapp/result.html', context)
    else:
        return render(request, 'myapp/question.html', {'question': QuesModel.objects.get(id=question_id)})


# 84 lines of code



