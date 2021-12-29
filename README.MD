<!-- markdownlint-disable -->
# Django Social Application

This is a social application developed with Django. A custom bookmarklet can be added by users to their bookmark manager (of their respective web browser), which they can then use to bookmark/add images to their profile. A Redis cache is used to track user actions, e.g. image viewing and any like/unlike actions.


# Features

 - Social Authentication
 - Personal dashboard and activity feed
 - Add personalised content
 - Like system and profile viewing tracking (redis cache)
 - Follow system
 - Admin site



## Installation and setup

Download/clone/fork the repository and install the `requirements.txt` file in your virtual environment.

## Social Authentication
- User registration
![enter image description here](https://github.com/bartventer/django-social-website-app/blob/master/bookmarks/github_images/user_register.png?raw=true)
- User Login
![enter image description here](https://github.com/bartventer/django-social-website-app/blob/master/bookmarks/github_images/user_login.png?raw=true)

## Personal dashboard and activity feed
![enter image description here](https://github.com/bartventer/django-social-website-app/blob/master/bookmarks/github_images/user_home_dashboard.png?raw=true)

## Add personalised content
 Custom jQuery bookmarklet (integrated with AJAX views) for bookmarking images.
1. Drag the bookmarklet to your bookmark toolbar
![enter image description here](https://github.com/bartventer/django-social-website-app/blob/master/bookmarks/github_images/user_bookmarklet.png?raw=true)
2. Navigate to any site containing images
3. Click on the bookmarklet bookmark. All bookmarkable images appear in the pop-up box.
![enter image description here](https://github.com/bartventer/django-social-website-app/blob/master/bookmarks/github_images/user_bookmark_add_image.png?raw=true)
4. In the pop-up box, click on any image to bookmark, you will be redirected to the social site (see 5 below).
	
5. You are redirected to the social site, fill out the title and description (optional), and click on 'BOOKMARK IT'.  
	![enter image description here](https://github.com/bartventer/django-social-website-app/blob/master/bookmarks/github_images/user_bookmark_add_image_redirect.png?raw=true)
6. Your bookmark has been successfully added. The image has been committed to the database and added to your profile.
	![enter image description here](https://github.com/bartventer/django-social-website-app/blob/master/bookmarks/github_images/user_image_success_added.png?raw=true)
7. Bookmark will appear on your profile.
![enter image description here](https://github.com/bartventer/django-social-website-app/blob/master/bookmarks/github_images/user_bookmark_add_last.png?raw=true)

## Like system and profile viewing tracking
Click on the image and you can like or unlike, and see the number of views. Redis is used as a cache to keep track of any views and like/unlike actions (see 7 above for screenshot of like/unlike feature).
![enter image description here](https://github.com/bartventer/django-social-website-app/blob/master/bookmarks/github_images/user_image_success_added.png?raw=true)

## Follow system
You can view the profile of other and choose to follow them. Anyone you follow will now appear in your activity feed/home dashboard.
- Follow
![enter image description here](https://github.com/bartventer/django-social-website-app/blob/master/bookmarks/github_images/follow_1.png?raw=true)
- Unfollow
![enter image description here](https://github.com/bartventer/django-social-website-app/blob/master/bookmarks/github_images/follow_2.png?raw=true)
## Admin site
- Login
![enter image description here](https://github.com/bartventer/django-social-website-app/blob/master/bookmarks/github_images/admin_login.png?raw=true)

- Home dashboard
![enter image description here](https://github.com/bartventer/django-social-website-app/blob/master/bookmarks/github_images/admin_home.png?raw=true)

- Modify any content
![enter image description here](https://github.com/bartventer/django-social-website-app/blob/master/bookmarks/github_images/admin_actions.png?raw=true)

