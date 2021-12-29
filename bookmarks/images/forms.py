from django import forms
from django.forms import widgets
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify

class ImageCreateForm(forms.ModelForm):
    '''
    A form to submit new images, which is built from the Image model.
    Users will not enter the image URL directly in the form.
    They will use the JavaScript tool to choose an image from an external site, and the from will 
    receive the URL paramater.
    Fields include title, url (hidden input per the above), and description.
    '''
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {'url': forms.HiddenInput,}

    def clean_url(self):
        '''
        Method to verify that the image url is valid, by checking that the filename ends with .jpg or .jpeg extensions.
        Either raises a validation error, or returns the cleaned url.
        '''
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        #Split the url extension from the right using a full stop, and slice the extension name from the returned output
        extension = url.rsplit('.',1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid image extensions.')
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        '''
        Method to override the ModelForm save method, in order to retrieve the given image and save it.
        '''
        #create an image instance
        image = super().save(commit=False)
        #get the url from the cleaned form data
        image_url = self.cleaned_data['url']
        #generate the image name by obtaining the image title slug, and combining it with the original file extension
        name = slugify(image.title)
        extension = image_url.rsplit('.',1)[1].lower()
        image_name = f'{name}.{extension}'
        #download the image from the given url, and save to the file to the media directory of the project (and not yet to the database)
        response = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(response.read()),save=False)
        #save the form to the database only when the commit paramater is True
        if commit:
            image.save()
        return image