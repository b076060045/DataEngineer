from django.urls import path
from . import views

urlpatterns = [
    # Create a new player
    path("players/create/", views.create_player, name="create_player"),
    # Update player details by player ID
    path("players/<int:id>/update/", views.update_player, name="update_player"),
    # Delete player by player ID
    path("players/<int:id>/delete/", views.delete_player, name="delete_player"),
    path("players/<int:id>/", views.get_player, name="get_player"),
    # Get players by team name with an option (details, items)
    path(
        "teams/<str:team_name>/players/<str:option>/",
        views.get_player_by_team,
        name="get_player_by_team",
    ),
    # Get items by position and item name
    path(
        "positions/<str:position>/items/<str:item>/",
        views.get_item_by_position,
        name="get_item_by_position",
    ),
    # Get team ID by team name
    path(
        "teams/by-name/<str:name>/id/",
        views.get_team_id_by_name,
        name="get_team_id_by_name",
    ),
    # Get the state of a team by team name
    path("teams/state/<str:name>/", views.get_team_state, name="get_team_state"),
    # Get player profile by player name
    path(
        "players/profile/<str:name>/", views.get_profile_player, name="player_profile"
    ),
    # Search players by team name
    path(
        "teams/<str:team_name>/players/",
        views.search_players_by_team,
        name="search_players_by_team",
    ),
    # 登入
    path("login", views.login, name="login"),
]
