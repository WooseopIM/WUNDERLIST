from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo

# Create your views here.

def index(request):
    todos = Todo.objects.all()
    context = {
        'todos': todos
    }
    return render(request, 'todos/index.html', context)

def create(request):
    # data 가져오기
    if request.method == 'POST':
        title = request.POST.get('title')
        due_date = request.POST.get('due-date')

        Todo.objects.create(title=title, due_date=due_date)
        return redirect('todos:index')
    else:
        return render(request, 'todos/create.html')



def update(request, pk):
    todo = get_object_or_404(Todo, id=pk)


    if request.method == 'POST':
        # 갱신된 최신 data 가져오기
        title = request.POST.get('title')
        due_date = request.POST.get('due-date')
        todo.title = title
        todo.due_date = due_date
        todo.save()

        return redirect('todos:index')
    else:
        # 기존 data 가져오기
        context = {
        'todo': todo
        }

        return render(request, 'todos/update.html',context)


def delete(request,pk):
    todo = get_object_or_404(Todo, id=pk)
    todo.delete()
    return redirect('todos:index')