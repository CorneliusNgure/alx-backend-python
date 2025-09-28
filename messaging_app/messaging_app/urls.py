from django.contrib import admin
from django.urls import path, include
from chats import auth


"""
Project-level config for the messaging_app app.
"""
urlpatterns = [
    path("admin/", admin.site.urls),

    # Browsable API login/logout (optional)
    path("api-auth/", include("rest_framework.urls")),

    # Chats API
    path("api/chats/", include("chats.urls")),

    # JWT auth endpoints
    path("api/auth/", include(auth.urlpatterns)),
]
