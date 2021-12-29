from django.contrib import admin
from .models import Profile
from django.forms.widgets import DateInput
from django.db import models
import datetime

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    '''
    Registering the Profile model in the administration site.
    '''
    list_display = ['user', 'date_of_birth', 'photo']
    formfield_overrides = {
        models.DateField :{
            'widget':DateInput(
                attrs={
                    'type':'date',
                    'min':f'{datetime.datetime.today().year-150}-01-01',
                    'max':f'{datetime.datetime.today().strftime("%Y-%m-%d")}'
                    }
                )
        }
    }