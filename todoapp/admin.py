import imp
from django.contrib import admin
from todoapp.models import *
# Register your models here.
admin.site.register(ToDoItem)
admin.site.register(ToDoList)
