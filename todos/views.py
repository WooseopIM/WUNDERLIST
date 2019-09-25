from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Todo
import requests
from decouple import config
import json
from django.views.decorators.csrf import csrf_exempt

token1 = config('TELEGRAM_TOKEN1')
token2 = config('TELEGRAM_TOKEN2')


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
        
        url1 = "https://api.telegram.org/bot" + token1 + "/getUpdates"
        url2 = "https://api.telegram.org/bot" + token2 + "/getUpdates"
        res1 = requests.get(url1)
        res2 = requests.get(url2)
        dict_result1 = res1.json()
        dict_result2 = res2.json()
        chat_id1 = dict_result1["result"][0]["message"]["from"]["id"]
        chat_id2 = dict_result2["result"][0]["message"]["from"]["id"]
        
        base = "https://api.telegram.org/"
        method = "/sendMessage"
        text = "새로운 todo가 생성되었습니다."
        url1 = base + "bot" + token1 + method + "?" + "text=" + text + "&chat_id=" + chat_id1
        url2 = base + "bot" + token2 + method + "?" + "text=" + text + "&chat_id=" + chat_id2
        requests.get(url1)
        requests.get(url2)

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

@csrf_exempt
def telegram(request):
    print(request.method)
    res = json.loads(request.body)

    print(request)
    return HttpResponse('아무메세지')