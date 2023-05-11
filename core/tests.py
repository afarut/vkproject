from django.test import TestCase
from core.models import FriendChain
from django.contrib.auth import get_user_model
from core.exceptions import LinkExistsException


User = get_user_model()


class FriendChainTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="test", email="test@mail.ru", password="testpassword"
        )
        self.user2 = User.objects.create_user(
            username="test2", email="test2@mail.ru", password="testpassword"
        )

    def test_create_chain(self):
        FriendChain.objects.create(from_user=self.user1, to_user=self.user2)
        self.assertEqual(len(FriendChain.objects.all()), 1)

    def test_create_two_equals_chains(self):
        FriendChain.objects.create(from_user=self.user1, to_user=self.user2)
        try:
            FriendChain.objects.create(from_user=self.user1, to_user=self.user2)
        except LinkExistsException:
            pass
        self.assertEqual(len(FriendChain.objects.all()), 1)

    def test_create_two_another_but_equals_chains(self):
        FriendChain.objects.create(from_user=self.user1, to_user=self.user2)
        try:
            FriendChain.objects.create(from_user=self.user2, to_user=self.user1)
        except LinkExistsException:
            pass
        self.assertEqual(len(FriendChain.objects.all()), 1)

    def test_base_with_3_users(self):
        user = User.objects.create_user(
            username="test3", email="test3@mail.ru", password="testpassword"
        )
        FriendChain.objects.create(from_user=self.user1, to_user=self.user2)
        FriendChain.objects.create(from_user=self.user1, to_user=user)
        self.assertEqual(len(FriendChain.objects.all()), 2)

    def test_with_2_friends(self):
        FriendChain.objects.create(from_user=self.user1, to_user=self.user2)
        FriendChain.objects.create(from_user=self.user2, to_user=self.user1)
        self.assertEqual(len(FriendChain.objects.all()), 1)
        self.assertTrue(FriendChain.objects.get(pk=1).is_friend)

    def test_with_2_reject(self):
        FriendChain.objects.create(from_user=self.user1, to_user=self.user2)
        FriendChain.objects.get(pk=1).was_rejected = True
        FriendChain.objects.create(from_user=self.user2, to_user=self.user1)
        self.assertEqual(len(FriendChain.objects.all()), 1)
        self.assertFalse(FriendChain.objects.get(pk=1).was_rejected)

    def test_with_3_circled_requests(self):
        user = User.objects.create_user(
            username="test3", email="test3@mail.ru", password="testpassword"
        )
        FriendChain.objects.create(from_user=self.user1, to_user=self.user2)
        FriendChain.objects.create(from_user=self.user2, to_user=user)
        FriendChain.objects.create(from_user=user, to_user=self.user1)
        self.assertEqual(len(FriendChain.objects.all()), 3)

    def test_with_3_circled_friends(self):
        user = User.objects.create_user(
            username="test3", email="test3@mail.ru", password="testpassword"
        )
        FriendChain.objects.create(from_user=self.user1, to_user=self.user2)
        FriendChain.objects.create(from_user=self.user2, to_user=self.user1)

        FriendChain.objects.create(from_user=self.user2, to_user=user)
        FriendChain.objects.create(from_user=user, to_user=self.user2)

        FriendChain.objects.create(from_user=user, to_user=self.user1)
        FriendChain.objects.create(from_user=self.user1, to_user=user)

        self.assertEqual(len(FriendChain.objects.all()), 3)
        for chain in FriendChain.objects.all():
            self.assertTrue(chain.is_friend)
            self.assertFalse(chain.was_rejected)
