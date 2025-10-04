from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def delete_user(request):
    """
    View to delete the currently logged-in user.
    """
    user = request.user
    user.delete()
    return redirect("/")