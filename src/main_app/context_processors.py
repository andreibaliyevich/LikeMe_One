from likeme_one.settings import SITE_NAME
from .models import Region, UserAccess, PhotographerOrder


def main_context(request):
    """ main context """
    context = {
        'SITE_NAME': SITE_NAME,
        'regions': Region.objects.all(),
        'user_region': request.session['user_region'],
    }
    return context


def user_access(request):
    """ User Access context """
    region = Region.objects.get(slug=request.session['user_region'])
    try:
        user_access = UserAccess.objects.get(user=request.user, region=region)
    except:
        context = {
            'user_is_admin': False,
            'user_is_photographer': False,
        }
    else:
        context = {
            'user_is_admin': user_access.is_admin,
            'user_is_photographer': user_access.is_photographer,
        }
        if user_access.is_admin:
            context['po_new_count'] = PhotographerOrder.objects.filter(
                region=region, viewed=False).count()
    finally:
        return context
