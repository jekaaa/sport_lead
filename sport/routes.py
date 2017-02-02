from pyramid.renderers import JSON
def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_renderer('myjson', JSON(indent=4, ensure_ascii=False))

    config.add_route('tournament', '/new_tournament')
    config.add_route('profile','/my_tournaments')
    config.add_route('login','/')
    config.add_route('logout', '/logout')
    config.add_route('reg','/registration')
    config.add_route('allTournaments','/all_tournaments')
    config.add_route('tournamentDetail','/tournament/{name}')
    #config.add_route('favorites','/favorites_tournaments')
    config.add_route('apiAllTournaments','/api/v1/all_tournaments')
    config.add_route('apiTournamentDetail', '/api/v1/tournament/{name}')
    config.add_route('apiLogin','/api/v1/auth')
    config.add_route('apiFavorites','/api/v1/favorites')
    config.add_route('apiMy','/api/v1/my')
    config.add_route('apiType','/api/v1/types')

