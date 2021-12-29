from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

class Profile(models.Model):
    '''
    An extension of the django authentication frameworks User model.
    This model contains all the additional fields and a one-to-one relationship with
    the Django User model. Additional fields for the Profile model includes data of 
    birth and photo fields. No required fields. Optional fields include date_of_birth and photo.
    '''
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth= models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'


class Contact(models.Model):
    '''
    An intermediary model to build relationships between users.
    Fields include:
    user_from - a foreign key for the user who creates the relationship
    user_to - a foreign key for the user being followed
    created - a DateTimeField field with auto_now_add=True to store the time when the relationship was created
    '''
    user_from = models.ForeignKey('auth.User', related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User', related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return f'{ self.user_from } follows { self.user_to }.'


# Add 'following' field to User dynamically, to avoid creating a custom user model
user_model = get_user_model()
user_model.add_to_class('following', models.ManyToManyField(
    'self',
    through=Contact,
    related_name='followers',
    symmetrical=False
))