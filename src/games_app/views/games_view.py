from django.views import View
from django.http import JsonResponse, HttpResponse
from games_app.models.game_model import GameModel
from games_app.models.player_model import PlayerModel
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum, Count, Q

class GameView(View):
    def get(self, request):
        player_stats = PlayerModel.objects.values('name').annotate(
            total_points=Sum('score'),
            total_wins=Count('win', filter=Q(win=2)),
            total_losses=Count('win', filter=Q(win=1)),
            total_draws=Count('win', filter=Q(win=0))
        ).order_by('-total_wins', '-total_points')

        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('pageSize', 10)

        paginator = Paginator(player_stats, page_size)
        current_page = paginator.get_page(page_number)

        try:
            paginated_players = paginator.page(current_page)
        except PageNotAnInteger:
            paginated_players = paginator.page(1)
        except EmptyPage:
            paginated_players = paginator.page(paginator.num_pages)

        # Corrigido para acessar os valores diretamente do dicionário retornado
        data = [
            {
                "name": player['name'],
                "total_points": player['total_points'],
                "total_wins": player['total_wins'],
                "total_losses": player['total_losses'],
                "total_draws": player['total_draws']
            }
            for player in paginated_players
        ]

        response = {
            'paginatedItems': {
                'Data': data,  # Lista de estatísticas dos jogadores na página atual
                'totalPages': paginator.num_pages,  # Total de páginas
                'currentPage': current_page.number,  # Número da página atual
                'hasPreviousPage': current_page.has_previous(),  # Se existe uma página anterior
                'previousPage': current_page.previous_page_number() if current_page.has_previous() else None,
                'nextPage': current_page.next_page_number() if current_page.has_next() else None,
                'pageSize': paginator.per_page,  # Tamanho da página
                'hasNextPage': current_page.has_next(),  # Se existe uma próxima página
            }
        }
        return JsonResponse(response)