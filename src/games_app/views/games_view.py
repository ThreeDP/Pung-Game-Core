from django.views import View
from django.http import JsonResponse, HttpResponse

class GameView(View):
    def get(self, request):
        return HttpResponse({"message": "Hello, World!"}, status=200)