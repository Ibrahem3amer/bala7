from django.contrib.auth import get_user_model

from .models import BasicAd

User = get_user_model()


def basic_ads(request):
    """
    Returns the ads associated with current request's user.
    :param request: An HttpRequest instance.
    :return: Dict
    """
    try:
        user = request.user
        user_ads = BasicAd.objects.filter(department_id=user.profile.department_id)
        return {'basic_ads': user_ads}
    except User.DoesNotExist:
        return {}