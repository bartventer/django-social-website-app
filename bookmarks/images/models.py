from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

class Image(models.Model):
    '''
    Model to store images retreived from different sites.

    Fields include:
    user - the User object, which represent a foreign key, in a one-to-many relationship
    title - title for the image
    slug - short label that contains only letters, numbers, underscores, or hyphens (SEO-friendly). 
            Automatically generated based on the value in the title field, if no slug is provided.
    url - the original URL for the image
    image - the image file, which also has the jpeg image path accessible via a url attribute
    description - optional description of the image
    created - date and time when the object was created in the database, automatically done upon 
                creation of the object
    users_like - A many-to-many relationship to store the users who liked the image.
    '''
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='images_created',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='images_liked', blank=True)
    total_likes = models.PositiveIntegerField(db_index=True, default=0)

    def save(self, *args, **kwargs):
        '''
        Method to override the save() method of the Image model to automatically
        generate the slug field based on the value of the title field.
        '''
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        '''Canonical URL for an image object.'''
        return reverse('images:detail', args=[self.id, self.slug])

    def __str__(self):
        return self.title