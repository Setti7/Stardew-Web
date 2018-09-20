from StardewWeb.settings import EMAIL_ADMIN
from .models import Profile


def score_processor(request):
    try:

        user_total_score = Profile.objects.get(user=request.user).score
        rank = Profile.objects.filter(score__gt=user_total_score).count() + 1

    except:
        user_total_score = 0
        rank = 'last'

    return {'score': user_total_score, 'admin_email': EMAIL_ADMIN, 'rank': rank}
