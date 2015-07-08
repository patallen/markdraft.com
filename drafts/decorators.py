from django.contrib.auth.decorators import user_passes_test
from django.conf import settings


def anonymous_required(function=None, redirect_to=None):
    """
    This decorator will redirect a logged in user to another
    location if the view requires them to be anonymous.
    """
    if not redirect_to:
        redirect_to = settings.LOGIN_REDIRECT_URL

    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous(),
        redirect_field_name=None,
        login_url=redirect_to
    )

    if function:
        return actual_decorator(function)
    return actual_decorator
