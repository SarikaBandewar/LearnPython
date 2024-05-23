from django.http import HttpResponse, HttpRequest
import json
from .models import User


def users(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        users = User.objects.all()
        serialized_users = [user.name for user in users]
        return HttpResponse(json.dumps(serialized_users))

    if request.method == 'POST':
        body = json.loads(request.body)
        user = User(name=body['name'], email=body['email'], age=body['age'])
        user.save()
        return HttpResponse(json.dumps({'id': user.id, 'name': user.name}))


def updateOrDeleteUser(request: HttpRequest, id: int) -> HttpResponse:
    if request.method == 'PUT':
        body = json.loads(request.body)
        user = User.objects.get(id=id)
        user.name = body['name']
        user.age = body['age']
        user.email = body['email']
        user.save()
        return HttpResponse(json.dumps({'id': user.id, 'name': user.name}))

    if request.method == 'DELETE':
        user = User.objects.get(id=id)
        user.delete()
        return HttpResponse(json.dumps({'id': user.id, 'deleted': true}))
