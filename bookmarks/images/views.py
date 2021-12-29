from .models import Image
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from actions.utils import create_action
import redis
from django.conf import settings

#Connect to redis
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)

@login_required
def image_create(request):
    '''
    View to save an image object to the database.
    The form expects initial data via GET in order to create the form instance.
    If the form is submitted, checks whether it is valid, if valid, create a new image instance, but prevent from being saved to the database.
    The current user is assigned to the image object, and then saved to the database.
    A success message is created and the user is redirected to the canonical URL of the image.
    '''
    if request.method=='POST':
        #form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            #form data is valid
            new_item = form.save(commit=False)

            #assign current user to the item
            new_item.user =request.user
            new_item.save()
            #create action in feed
            create_action(request.user,'bookmarked image',new_item)
            messages.success(request, 'Image added successfully')

            #redirect to new created item detail view
            return redirect(new_item.get_absolute_url())
    else:
        #build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)

    return render(request, 'images/image/create.html',{'section':'images','form':form})

def image_detail(request, id, slug):
    '''Canonical view for an image object. Paramaters include the image object id and slug'''
    image = get_object_or_404(Image, id=id, slug=slug)
    # redis - increment total image views by 1
    total_views = r.incr(f'image:{image.id}:views')
    # increment image ranking by 1
    r.zincrby('image_ranking', 1, image.id)
    return render(request,'images/image/detail.html',
                        {'section':'images',
                         'image':image,
                         'total_views':total_views})


@ajax_required
@login_required
@require_POST
def image_like(request):
    '''
    A view for users to like or unlike images, by using AJAX actions, to avoid reloading the entire page.
    Three decorators used; ajax_required which is a custom built decorator to restrict requests to only those
    generated via AJAX - returns a HTTP bad response if the request did not originate via AJAX, login_required 
    to prevent users that are not logged in from accessing the view, and require_POST which returns an 
    HttpResponseNotAllowed object (status code 405) if the HTTP request is no done via POST.
    
    Two POST paramaters are used in this view, including the image_id (id of the image object  on which the user
    is performing the action), and action (the action the user wants to perform - a string with the value of like 
    or unlike).
    '''
    # retrieving the id and action paramaters
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    # if both image_id and action is present
    if image_id and action:
        try:
            #instantiate the image object
            image = Image.objects.get(id=image_id)
            if action == 'like':
                #add the users like to Image model
                image.users_like.add(request.user)
                #create action in feed
                create_action(request.user, 'likes', image)
            else:
                #remove the users like (i.e. dislike) from the Image model
                image.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'error'})


@login_required
def image_list(request):
    '''
    Image list view that handles both standard browser requests and AJAX requests,
    including pagination. When user loads the image list page, displays the first page
    of images. Infinite scroll functionality, when scorlling to the bottom of the page,
    loads the following page of items via AJAX and appends to bottom of main page.
    '''
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range
            # return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'images/image/list_ajax.html', {'section':'images', 'images': images})
    return render(request, 'images/image/list.html', {'section':'images', 'images':images})


@login_required
def image_ranking(request):
    '''View to display the ranking of the most viewed images.'''
    # get in memory redis image ranking dictionary
    image_ranking = r.zrange('image_ranking',0, -1, desc=True)[:10]
    image_ranking_ids = [ int(id) for id in image_ranking ]
    # get most viewed images
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(request,'images/image/ranking.html',{'section':'images', 'most_viewed':most_viewed})