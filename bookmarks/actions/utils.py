from django.contrib.contenttypes.models import ContentType
from .models import Action
import datetime
from django.utils import timezone

def create_action(user, verb, target=None):
    '''A shortcut function to create actions that optionally include a target object. 

    Args:
        user (obj): A user object from the Django User Model.
        verb (str): The action performed by the User.
        target (obj): Optional, a generic foreign key to the related object based 
            on the combination of target_ct and target_id.
    
    Returns:
        bool: True if Action object created, False if not created.
    '''
    #check for any simmilar action made in the last minute
    now = timezone.now()
    last_minute = now -datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(
        user_id=user.id,
        verb=verb,
        created__gte=last_minute
    )
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(
            target_ct=target_ct,
            target_id=target.id
        )
    if not similar_actions:
        #no existing actions found in last minute--> create and commit 
        # action object to the Model
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False