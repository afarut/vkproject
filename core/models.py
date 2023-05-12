from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class FriendChain(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="from_user",
    )
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    is_friend = models.BooleanField(default=False)
    was_rejected = models.BooleanField(
        default=False
    )  # For filtration of rejected user (subscribers)

    def __str__(self):
        if self.is_friend:
            return f"{self.from_user}:{self.to_user} - friend"
        else:
            return f"{self.from_user}:{self.to_user} - request"
