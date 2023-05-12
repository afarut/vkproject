from django.contrib.auth import get_user_model
from rest_framework import generics
from core.serializers import UserSerializer, UserCreateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import FriendChain
from django.db.models import Q


User = get_user_model()


class UserApiView(generics.ListAPIView):  # List of all users
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateAPIView(generics.CreateAPIView):  # Registration
    serializer_class = UserCreateSerializer
    authentication_classes = []
    permission_classes = []

    # def post(self, request):
    #    request.data["password"] = make_password(request.data["password"])
    #    return super().post(request)


class UserFriendListAPIView(generics.ListAPIView):  # Getting friend list
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        result = []
        for friendchain in user.from_user.all().filter(is_friend=True):
            result.append(friendchain.to_user)
        for friendchain in user.to_user.all().filter(is_friend=True):
            result.append(friendchain.from_user)
        return result


class UserSubscriberListAPIView(
    generics.ListAPIView
):  # Getting list of people, which user rejected in last
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        result = []
        for friendchain in user.to_user.all().filter(is_friend=True, was_rejected=True):
            result.append(friendchain.from_user)
        return result


class RequestListAPIView(APIView):  # All request to friend related with authorizan user
    def get(self, request):
        result = []
        for friendchain in request.user.from_user.all().filter(is_friend=False):
            user = friendchain.to_user
            data = UserSerializer(user).data
            data.update({"tome": False, "status": "outgoing friend request"})
            result.append(data)
        for friendchain in request.user.to_user.all().filter(is_friend=False):
            user = friendchain.from_user
            data = UserSerializer(user).data
            data.update({"tome": True, "status": "incoming friend request"})
            result.append(data)
        return Response(result)


class UserLinkInfoAPIView(APIView):  # Info about relation with another user
    # friend/outgoing request/incoming friend request/no requests
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        result = UserSerializer(user).data
        if request.user.pk != pk:
            result["status"] = "No requests"
            try:
                chain = FriendChain.objects.get(to_user=user, from_user=request.user)
                if chain.is_friend:
                    result["status"] = "friend"
                else:
                    result["status"] = "outgoing friend request"
            except FriendChain.DoesNotExist:
                pass
            try:
                chain = FriendChain.objects.get(from_user=user, to_user=request.user)
                if chain.is_friend:
                    result["status"] = "friend"
                else:
                    result["status"] = "incoming friend request"
            except FriendChain.DoesNotExist:
                pass
        return Response(result)


class UserDeleteFriendAPIView(APIView):  # Delete friend
    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        chain = FriendChain.objects.get(
            Q(to_user=user, from_user=request.user)
            | Q(to_user=request.user, from_user=user)
        )
        chain.delete()
        return Response({"status": "ok"})


class UserGoFriendAPIView(APIView):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        status = "outgoing friend request"
        try:
            chain = FriendChain.objects.get(
                Q(to_user=user, from_user=request.user)
                | Q(to_user=request.user, from_user=user)
            )
            if chain.to_user == request.user:
                chain.is_friend = True
                chain.save()
                status = "You are friends"
        except FriendChain.DoesNotExist:
            FriendChain.objects.create(from_user=request.user, to_user=user)
        return Response({"status": status})
