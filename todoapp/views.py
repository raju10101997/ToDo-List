giimport imp
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from . models import ToDoList, ToDoItem
from django.urls import reverse, reverse_lazy
# Create your views here.


class ListListView(ListView):
    model = ToDoList
    template_name = "todoapp/index.html"


class ItemListView(ListView):
    model = ToDoItem
    template_name = "todoapp/todo_list.html"

    def get_queryset(self):
        query_set = ToDoItem.objects.filter(
            todo_list_id=self.kwargs["list_id"])
        return query_set

    def get_context_data(self):
        context = super().get_context_data()
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        return context

# queryset
# <QuerySet [<ToDoItem: Start my to-do list: due 2022-04-22 07:54:01+00:00>,
# <ToDoItem: 2nd work: due 2022-04-23 11:43:27+00:00>]>

# context
# {'paginator': None, 'page_obj': None, 'is_paginated': False,
# 'object_list': <QuerySet [<ToDoItem: Next day works: due 2022-04-23 11:44:07+00:00>]>,
# 'todoitem_list': <QuerySet [<ToDoItem: Next day works: due 2022-04-23 11:44:07+00:00>]>,
# 'view': <todoapp.views.ItemListView object at 0x7f332dadeca0>}

# {'paginator': None, 'page_obj': None, 'is_paginated': False,
# 'object_list': < QuerySet [< ToDoItem: Next day works: due 2022-04-23 11:44:07+00:00 > ] > ,
# 'todoitem_list': < QuerySet [< ToDoItem: Next day works: due 2022-04-23 11:44:07+00:00 > ] > ,
#  'view': < todoapp.views.ItemListView object at 0x7f725741a850 >, 'todo_list': < ToDoList: Tomorrow > }


class ListCreate(CreateView):
    model = ToDoList
    fields = ["title"]

    def get_context_data(self):
        context = super(ListCreate, self).get_context_data()
        context["title"] = "Add a new list"
        return context

# initial
# {'todo_list': <ToDoList: Day AfterTomorrow>}

# context
# {'form': <ToDoItemForm bound=False, valid=Unknown, fields=(todo_list;title;description;due_date)>,
# 'view': <todoapp.views.ItemCreate object at 0x7f3b91b040d0>}

# context
# {'form': <ToDoItemForm bound=False, valid=Unknown, fields=(todo_list;title;description;due_date)>,
# 'view': <todoapp.views.ItemCreate object at 0x7f23a26f18b0>, 'todo_list': <ToDoList: Day AfterTomorrow>,
# 'title': 'Create a new item'}


class ItemCreate(CreateView):
    model = ToDoItem
    fields = [
        "todo_list", "title", "description", "due_date"
    ]

    def get_initial(self):
        initial_data = super(ItemCreate, self).get_initial()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        initial_data["todo_list"] = todo_list
        return initial_data

    def get_context_data(self):
        context = super(ItemCreate, self).get_context_data()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        context["todo_list"] = todo_list
        context["title"] = "Create a new item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])


class ItemUpdate(UpdateView):
    model = ToDoItem
    fields = ["todo_list", "title", "description", "due_date"]

    def get_context_data(self):
        context = super(ItemUpdate, self).get_context_data()
        context["todo_list"] = self.object.todo_list
        context["title"] = "Edit item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])


class ListDelete(DeleteView):
    model = ToDoList
    # You have to use reverse_lazy() instead of reverse(),
    # as the urls are not loaded when the file is imported.
    success_url = reverse_lazy("index")


class ItemDelete(DeleteView):
    model = ToDoItem

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context
