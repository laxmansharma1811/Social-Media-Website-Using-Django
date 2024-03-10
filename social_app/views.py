from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeDoneView
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from .models import *

# Create your views here.
@login_required(login_url='login')
def home(request):
    images = UploadedImage.objects.all()
    return render(request, 'home.html', {'images':images})



def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        
        else:
            return render(request, 'login.html', {'error': 'Invalid login credentials'})

    return render(request, 'login.html')




def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'Username already exists.')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.warning(request, 'Email already exists.')
            else:
                user = User.objects.create_user(username=username, email=email, password=confirm_password)
                user.save()

                user = authenticate(username=username, password=confirm_password)
                login(request, user)

                messages.success(request, 'Account created successfully. You are now logged in.')
                return redirect('login')
        else:
            messages.warning(request, 'Passwords do not match.')
            return redirect('signup')

    return render(request, 'signup.html')


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')



#Upload Image
@login_required(login_url='login')
def upload_image(request):
    if request.method == 'POST' and request.user.is_authenticated:
        if 'image' in request.FILES:
            image = request.FILES['image']
            desc = request.POST['desc']
            author = request.user 
            uploaded_image = UploadedImage(author=author, image=image, desc=desc, user=request.user)
            uploaded_image.save()
            return redirect('home')
        else:
            return render(request, 'upload.html', {'required': 'Please choose a file to upload'})
    else:
        return render(request, 'upload.html')
    




#Edit Delete Post
@login_required(login_url='login')
def edit_image(request, image_id):
    image = get_object_or_404(UploadedImage, id=image_id)

    if request.user == image.author:
        if request.method == 'POST':
            new_desc = request.POST.get('new_desc')
            image.desc = new_desc

            if 'newImage' in request.FILES:
                new_image = request.FILES['newImage']
                image.image.save(new_image.name, new_image, save=True)

            image.save()
            messages.success(request, 'Post edited successfully.')
            return redirect('home')

        return render(request, 'edit_image.html', {'image': image})

    messages.error(request, 'You are not allowed to edit this post.')
    return redirect('home')


#Delete image
@login_required(login_url='login')
def delete_image(request, image_id):
    image = get_object_or_404(UploadedImage, id=image_id)

    if request.user == image.author:
        image.delete()
        messages.success(request, 'Post deleted successfully.')
    else:
        messages.error(request, 'You are not allowed to delete this post.')

    return redirect('home')



#LikePost
@login_required(login_url='login')
def like(request, image_id):
    if request.method == 'POST':
        image = UploadedImage.objects.get(pk=image_id)
        image.like(request.user)
    return redirect('home')



#Comment
def add_comment(request, image_id):
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        image = UploadedImage.objects.get(pk=image_id)
        Comment.objects.create(author=request.user, image=image, text=comment_text)

    return redirect('show_comments', image_id=image_id)


#Show Comments
def show_comments(request, image_id):
    image = get_object_or_404(UploadedImage, id=image_id)
    comments = Comment.objects.filter(image=image)
    return render(request, 'show_comments.html', {'image': image, 'comments': comments})


#edit delete comments
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        new_text = request.POST.get('new_text')
        comment.text = new_text
        comment.save()
        messages.success(request, 'Comment edited successfully.')
        return redirect('show_comments', image_id=comment.image.id)

    return render(request, 'edit_comment.html', {'comment': comment})


#Delete Comment
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        image_id = comment.image.id  # Get the associated image_id
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
        return redirect(reverse('show_comments', kwargs={'image_id': image_id}))

    return render(request, 'delete_comment.html', {'comment': comment})



#Change Password
class MyPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'password_change_done.html'

@login_required(login_url='login')
def settings(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if request.user.check_password(old_password):
            if new_password1 == new_password2:
                request.user.set_password(new_password1)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Password changed successfully.')
                return redirect('settings')
            else:
                messages.error(request, 'New passwords do not match.')
        else:
            messages.error(request, 'Incorrect old password.')

    return render(request, 'settings.html')



#Profile
@login_required(login_url='login')
def profile(request):
    try:
        profile = request.user.profile

    except ObjectDoesNotExist:
        profile = None

    return render(request, 'profile.html', {'profile': profile})



#Update Profile
@login_required(login_url='login')
def update_profile(request):
    try:
        profile = request.user.profile
    except ObjectDoesNotExist:
        profile = Profile(user=request.user)
        profile.save()

    if request.method == 'POST':
        profile.bio = request.POST.get('bio', '')
        profile.address = request.POST.get('address', '')
        profile.contact = request.POST.get('contact', '')  
        profile.email = request.POST.get('email', '')

        new_profile_picture = request.FILES.get('profile_picture')

        if new_profile_picture:
            if profile.profile_picture:
                profile.profile_picture.delete()

            profile.profile_picture = new_profile_picture

        profile.save()
        return redirect('profile')

    return render(request, 'update_profile.html', {'profile': profile})



#Upload Video
@login_required(login_url='login')
def upload_video(request):
    if request.method == 'POST':
        video_file = request.FILES.get('video')
        desc = request.POST.get('desc', '')

        if video_file:
            uploaded_video = UploadedVideo.objects.create(
                author=request.user,
                video=video_file,
                desc=desc,
                user=request.user
            )

            return redirect('reels')

    return render(request, 'upload_video.html')


#reels
def reels(request):
    videos = UploadedVideo.objects.all()
    return render(request, 'reels.html', {'videos': videos})



#liked video
@login_required(login_url='login')
def like_video(request, video_id):
    if request.method == 'POST':
        video = get_object_or_404(UploadedVideo, id=video_id)
        video.like(request.user)
    return JsonResponse({'likes': video.likes.count()})


#Edit and delete video
@login_required(login_url='login')
def edit_video(request, video_id):
    video = get_object_or_404(UploadedVideo, id=video_id)

    if request.user == video.author:
        if request.method == 'POST':
            new_desc = request.POST.get('new_desc')
            video.desc = new_desc
            video.save()
            messages.success(request, 'Video edited successfully.')
            return redirect('reels')

        return render(request, 'edit_video.html', {'video': video})

    messages.error(request, 'You are not allowed to edit this video.')
    return redirect('reels')



#Delete video
@login_required(login_url='login')
def delete_video(request, video_id):
    video = get_object_or_404(UploadedVideo, id=video_id)

    if request.user == video.author:
        video.delete()
        messages.success(request, 'Video deleted successfully.')
    else:
        messages.error(request, 'You are not allowed to delete this video.')

    return redirect('reels')



#View Profile
def view_profile(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    other_user_profile = other_user.profile  
    return render(request, 'view_profile.html', {'other_user': other_user, 'other_user_profile': other_user_profile})




#Follow and Unfollow
@login_required(login_url='login')
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    profile = request.user.profile

    if request.user != user_to_follow:
        if user_to_follow in profile.followers.all():
            profile.unfollow(user_to_follow)
            followed = False
        else:
            profile.follow(user_to_follow)
            followed = True

        return JsonResponse({'followed': followed})

