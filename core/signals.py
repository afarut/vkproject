from django.db.models.signals import pre_save
from django.dispatch import receiver
from core.models import FriendChain
from django.conf import settings
from core.exceptions import LinkExistsException, OneUserException


@receiver(pre_save, sender=FriendChain)
def maybedelete_receiver(sender, instance, *args, **kwargs):
    to_user = instance.to_user
    from_user = instance.from_user
    if instance.is_friend:
        instance.was_rejected = False
    try:
        chain = FriendChain.objects.get(to_user=from_user, from_user=to_user)
        if chain.id != instance.id:
            raise LinkExistsException("This link between two users is already exists.")
    except FriendChain.DoesNotExist:
        pass
    try:
        chain = FriendChain.objects.get(to_user=to_user, from_user=from_user)
        if chain.id != instance.id:
            raise LinkExistsException("This link between two users is already exists.")
    except FriendChain.DoesNotExist:
        pass
    if to_user == from_user:
        raise OneUserException("This is the same user")