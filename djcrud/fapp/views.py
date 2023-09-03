from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Task


class CustomLogin(LoginView):
    template_name = 'fapp/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')
    

#List view already know what template it wants
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['tasks'] = contex['tasks'].filter(user=self.request.user)
        contex['count'] = contex['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''


        if search_input:
            contex['tasks'] = contex['tasks'].filter(title__icontains=search_input)

        return contex


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'fapp/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title','content', 'complete']
    template_name = 'fapp/task_forme.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title','content', 'complete']
    template_name = 'fapp/task-update.html'
    success_url = reverse_lazy('tasks')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    #this looks for (task_confirm_delete.html) by default