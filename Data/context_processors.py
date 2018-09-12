from .models import UserData, Profile
from StardewWeb.settings import EMAIL_ADMIN

def score_processor(request):

    try:

        user_total_score = Profile.objects.get(user=request.user).score

    except:
        user_total_score = 0

    return {'score': user_total_score, 'admin_email': EMAIL_ADMIN}

