import json
from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from games_app.models.tournament_history_model import TournamentHistoryModel

class TournamentHistoryView(View):
    def get(self, request):
        roomCode = request.GET.get('roomCode', None)
        if not roomCode:
            return JsonResponse({"error": "O parâmetro 'roomCode' é obrigatório."}, status=400)

        player_name = request.GET.get('player_name', None)
        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('pageSize', 10)

        if player_name:
            tournament_history = TournamentHistoryModel.objects.filter(
                Q(red__name__icontains=player_name) | Q(blue__name__icontains=player_name)
            )
        else:
            tournament_history = TournamentHistoryModel.objects.filter(roomCode=roomCode)

        if not tournament_history:
            return JsonResponse({"error": "Histórico de torneio não encontrado."}, status=404)

        paginator = Paginator(tournament_history, page_size)
        try:
            current_page = paginator.page(page_number)
        except PageNotAnInteger:
            current_page = paginator.page(1)
        except EmptyPage:
            current_page = paginator.page(paginator.num_pages)

        data = [
            {
                "winner": game.winner,
                "red": {
                    "name": game.red.name,
                    "score": game.red.score,
                    "profileImage": game.red.profileImage
                },
                "blue": {
                    "name": game.blue.name,
                    "score": game.blue.score,
                    "profileImage": game.blue.profileImage
                }
            }
            for game in current_page
        ]

        response = {
            'currentPage': current_page.number,
            'pageSize': paginator.per_page,
            'nextPage': current_page.next_page_number() if current_page.has_next() else None,
            'previousPage': current_page.previous_page_number() if current_page.has_previous() else None,
            'hasNextPage': current_page.has_next(),
            'hasPreviousPage': current_page.has_previous(),
            'games': data
        }

        return JsonResponse(response)
