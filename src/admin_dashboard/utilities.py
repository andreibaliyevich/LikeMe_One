from main_app.models import Region, UserAccess


def user_is_superadmin(user):
    region_count = Region.objects.all().count()
    user_all_access = UserAccess.objects.filter(user=user)

    user_admin_count = 0
    for user_access in user_all_access:
        if user_access.is_admin:
            user_admin_count += 1

    if user_admin_count == region_count:
        return True
    else:
        return False
