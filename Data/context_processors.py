from .models import UserData
from StardewWeb.settings import EMAIL_ADMIN

def score_processor(request):

    try:
        user_scores = UserData.objects.filter(user=request.user)
        user_total_score = sum([obj.score for obj in user_scores])

    except:
        user_total_score = 0

    return {'score': user_total_score, 'admin_email': EMAIL_ADMIN}

