from django.urls import path
from .views import user_messages, inbox, delete_user

urlpatterns = [
    path('my-messages/', user_messages, name='user_messages'),
    path('inbox/', inbox, name='inbox'),
    path('delete-account/', delete_user, name='delete_user')
]
