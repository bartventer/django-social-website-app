from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Action(models.Model):
    '''
    Model to store user activities.
    The fields are as follows:
    user - the user performing the action (Foreign key to Django User model)
    verb - the action performed by the user, described in a verb
    target_ct - a Foreign key field pointing to the ContentType model
    target_id - a positive integer field to store the primary key of the related object 
    target - a generic foreign key field to the related object based on the combination of target_ct and target_id
    created - data and time the action was created
    '''
    user = models.ForeignKey(
        'auth.User',
         related_name='actions',
         db_index=True,
         on_delete=models.CASCADE
    )
    verb = models.CharField(max_length=255)
    target_ct = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name='target_obj',
        on_delete=models.CASCADE
    )
    target_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        db_index=True
    )
    target = GenericForeignKey('target_ct', 'target_id')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)