from django.shortcuts import get_list_or_404
from django.http.request import HttpRequest
from django.views import generic
from django.views.generic.edit import CreateView

from .models import Questionnaire, ShortAnswer, LongAnswer, FileAnswer, QuestionChoice
from .forms import QuestionnaireForm


# Create your views here.
class QuestionnairesList(generic.ListView):
    model = Questionnaire
    template_name = 'questionnaire_list.html'


class QuestionnaireDetail(generic.DetailView):
    model = Questionnaire
    template_name = 'questionnaires/questionnaire_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url = HttpRequest.get_full_path(self.request)
        urlend = url.split('/')
        urlfinish = urlend[-2]
        questions = []
        sh_answers = ShortAnswer.objects.all()
        l_a = LongAnswer.objects.all()
        f_a = FileAnswer.objects.all()
        c_a = QuestionChoice.objects.all()
        print("Choices: ", c_a)
        for question in sh_answers:
            if question.questionnaire.pk == int(urlfinish):
                index = int(question.position) - 1
                questions.insert(index, question)
        for question in l_a:
            if question.questionnaire.pk == int(urlfinish):
                index = int(question.position) - 1
                questions.insert(index, question)
        for question in f_a:
            if question.questionnaire.pk == int(urlfinish):
                index = int(question.position) - 1
                questions.insert(index, question)


        context['questions'] = questions
        return context


class QuestionnaireCreate(CreateView):
    model = Questionnaire
    form_class = QuestionnaireForm
    template_name = 'questionnaires/create_questionnaires.html'
    success_url = '/questionnaires/'
