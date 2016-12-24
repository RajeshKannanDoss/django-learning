# points variable
WIN_POINT = 3
DRAW_POINT = 1


def url_to_id(link, model):
    """
    :param link: string, shortcut for django model
    :param model: django model
    :return: django model where shortcut = link
    """
    try:
        return model.objects.get(shortcut=link)
    except model.DoesNotExist:
        return None


def add_points_to_team(team, goals_scored, goals_conceded):
    """
    :param team: team_stat model object
    :param goals_scored: integer, goals that team scored
    :param goals_conceded: integer, goals that team conceded
    :return: None
    """
    team.match_count += 1
    team.goals_scored += goals_scored
    team.goals_conceded += goals_conceded
    if goals_scored > goals_conceded:
        team.wins += 1
        team.points += WIN_POINT
    elif goals_scored < goals_conceded:
        team.loses += 1
    else:
        team.draws += DRAW_POINT
        team.points += 1
