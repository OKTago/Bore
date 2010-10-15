from django.core.management import setup_environ
from apps import settings
setup_environ(settings)

from django.core.exceptions import ObjectDoesNotExist 

from face.models import UserSession
from face.models import Friend 
from face.models import FriendCompare

from facebook import GraphAPI

us = UserSession.objects.filter(enabled=True)
for user in us:
    FriendCompare.truncate()
    token = user.token
    graph = GraphAPI(token)
    friends = graph.get_connections("me", "friends")
    friends = friends['data']
    for friend in friends:
        f = FriendCompare(user_id = user.uid, friend_id = friend['id'])
        f.save()

    # discover no more friends
    nomore = Friend.get_nomore()
    for item in nomore: 
        print item.friend_id
        tmp = Friend.objects.get(id=item.id)
        tmp.deleted = True
        tmp.save()
        #item.save()

    # sync friends
    for friend in friends:
        try:
            f = Friend.objects.get(user_id=user.uid, friend_id = friend['id'])
            tmp = Friend(id=f.id)
            tmp.deleted=False
            f.save()
        except ObjectDoesNotExist:
            f = Friend(user_id=user.uid, friend_id = friend['id'])
            f.save()


