# points variable
WIN_POINT = 3
DRAW_POINT = 1


def add_points_to_teams(sender, instance, **kwargs):
    """
    :param instance: Match object
    :return: if kwargs['created'] is True, return None
    """

    home = instance.team_home
    guest = instance.team_guest

    home.match_count += 1
    instance.team_guest.match_count += 1

    home.goals_scored += instance.team_home_goals
    home.goals_conceded += instance.team_guest_goals
    guest.goals_scored += instance.team_guest_goals
    guest.goals_conceded += instance.team_home_goals

    if instance.team_home_goals > instance.team_guest_goals:
        home.wins += 1
        home.points += WIN_POINT
        guest.loses += 1
    elif instance.team_home_goals < instance.team_guest_goals:
        guest.wins += 1
        guest.points += WIN_POINT
        home.loses += 1
    else:
        home.draws += 1
        guest.draws += 1
        home.points += DRAW_POINT
        guest.points += DRAW_POINT

    home.save()
    guest.save()
