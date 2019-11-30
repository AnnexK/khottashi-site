from django.shortcuts import render, get_object_or_404
from .models import Question, Choice
from django.utils import timezone

# Create your views here.
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_questions'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, q_id):
    question = get_object_or_404(Question, pk=q_id)
    try:
        selection = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice!"
        })
    else:
        selection.votes += 1
        selection.save()
        return HttpResponseRedirect(reverse('polls:results', args=(q_id,)))
