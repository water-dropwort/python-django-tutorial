from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from .models import Question, Choice,Answer
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

class PollsLoginRequiredMixin(LoginRequiredMixin):
    login_url = "testpolls:login"
    redirect_field_name = None

class IndexView(PollsLoginRequiredMixin, generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

@login_required(redirect_field_name=None, login_url="testpolls:login")
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # future question
    if question.pub_date > timezone.now():
        raise Http404("This question has not been published.")
    users_answer = Answer.objects.filter(user=request.user, question=question)
    if len(users_answer) >= 1:
        return render(request, "polls/details.html",
                      {
                          "question" : question,
                          "current_choice" : users_answer[0].choice
                      })
    else:
        return render(request, "polls/details.html",
                      {
                          "question" : question,
                      })

class ResultsView(PollsLoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = "polls/results.html"

@login_required(redirect_field_name=None, login_url="testpolls:login")
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/details.html",
                      {
                          "question" : question,
                          "error_message": "You didn't select a choice.",})
    else:
        users_answer = Answer.objects.filter(user=request.user, question=question)
        # already answered with other choice
        if len(users_answer) >= 1 and users_answer[0].choice.id != selected_choice.id:
            users_answer[0].choice.votes -= 1
            users_answer[0].choice.save()
            users_answer[0].choice = selected_choice
            users_answer[0].save()
            selected_choice.votes += 1
            selected_choice.save()
        # first answer
        elif len(users_answer) == 0:
            Answer(user=request.user, question=question, choice=selected_choice).save()
            selected_choice.votes += 1
            selected_choice.save()
        # already answered with same choice
        #else:
            # nothing to do
        return HttpResponseRedirect(reverse("testpolls:results", args=(question.id,)))
