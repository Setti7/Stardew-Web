from .models import UserData

def score_processor(request):

    try:
        user_scores = UserData.objects.filter(user=request.user)
        user_total_score = sum([obj.score for obj in user_scores])

    except:
        user_total_score = 0

    return {'score': user_total_score}

