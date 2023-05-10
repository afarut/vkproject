from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Friends(models.Model):
	from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        #related_name="user",
    )
    to_user = models.ForeignKey(
    	User,
    	on_delete=models.CASCADE,
    	#related_name="user"
    )
    is_friend = models.BooleanField(default=False)


    def set_status(self, status):
    	pass