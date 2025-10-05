from django.db import models


class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """ Filters unread messages for a specific user """
        return (
            self.filter(receiver=user, read=False)
                .only("id", "content", "sender", "timestamp")
        )