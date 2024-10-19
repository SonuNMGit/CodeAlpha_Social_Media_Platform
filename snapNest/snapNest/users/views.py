from .models import Follow
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm, UserProfileForm, LoginForm, PasswordResetForm
from django.contrib.auth.forms import UserChangeForm
from .forms import PostForm
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.models import User 
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from .models import Post, UserProfile, Comment, User
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from .models import Message

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, "Your account has been created successfully!")
            return redirect('login')
    else:
        form = RegistrationForm()
        profile_form = UserProfileForm()

    return render(request, 'register.html', {'form': form, 'profile_form': profile_form})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

@login_required
def home(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(user=request.user) 
        followed_users = Follow.objects.filter(follower=request.user).values('followed')
        followed_posts = Post.objects.filter(user__in=followed_users) 

        all_posts = posts | followed_posts
        all_posts = all_posts.order_by('-created_at')

        user_profile = UserProfile.objects.get(user=request.user)

        following_users = user_profile.following.all()
        posts = Post.objects.filter(user__in=following_users).order_by('-created_at')

        context = {
            'posts': posts,
            'users': None,  
        }

        return render(request, 'home.html', context)
    else:
        return redirect('login')
    
def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            try:
                user = User.objects.get(username=username)
                new_password = form.cleaned_data['new_password1']
                user.set_password(new_password)
                user.save()
                return redirect('login') 
            except User.DoesNotExist:
                form.add_error(None, "User does not exist.")
    else:
        form = PasswordResetForm()
    return render(request, 'password_rest.html', {'form': form})

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        username = request.POST.get('username')
        email = request.POST.get('email')

        if user.username != username:
            user.username = username
        if user.email != email:
            user.email = email

        profile_photo = request.FILES.get('profile_photo')
        if profile_photo:
            user_profile.profile_photo = profile_photo

        user_profile.bio = request.POST.get('bio')
        user_profile.privacy = request.POST.get('privacy')

        user.save()
        user_profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('update_profile') 

    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'update_profile.html', {'user': request.user, 'user_profile': user_profile})

@login_required
def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    followers = user.userprofile.followers.all()  
    following = user.userprofile.following.all() 

    context = {
        'user': user,
        'followers': followers,
        'following': following,
    }
    return render(request, 'profile.html', context)

@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user 
            post.save()
            return redirect('profile', user_id=request.user.id)
    else:
        form = PostForm()
    
    return render(request, 'add_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('profile', user_id=request.user.id)

    return render(request, 'confirm_delete.html', {'post': post})

@login_required
def search_user(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(Q(username__icontains=query)) if query else []

    return render(request, 'home.html', {'users': users})

@login_required
def follow_user(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)

    if profile_user.userprofile.privacy == 'private':
        message_content = f"{request.user.username} wants to follow you."
        Message.objects.create(sender=request.user, recipient=profile_user, content=message_content)
        return HttpResponseRedirect(reverse('profile', args=[user_id]))
    else:
        if request.user != profile_user:
            request.user.userprofile.following.add(profile_user)
            profile_user.userprofile.followers.add(request.user)
            request.user.userprofile.save()
            profile_user.userprofile.save()

    return redirect(reverse('profile', args=[user_id]))

@login_required
def unfollow_user(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    
    if request.user != profile_user:
        request.user.userprofile.following.remove(profile_user)
        profile_user.userprofile.followers.remove(request.user)

        request.user.userprofile.save()
        profile_user.userprofile.save()

    return redirect(reverse('profile', args=[user_id])) 

@login_required
def remove_follower(request, follower_id):
    follower_to_remove = get_object_or_404(User, id=follower_id)
    current_user_profile = request.user.userprofile
    follower_profile = follower_to_remove.userprofile

    if follower_to_remove in current_user_profile.followers.all():
        current_user_profile.followers.remove(follower_to_remove)
        follower_profile.following.remove(request.user)

    else:
        return HttpResponseForbidden("You cannot remove this follower.")

    return redirect('profile', user_id=request.user.id)

@login_required
def public_posts_view(request):
    public_posts = Post.objects.filter(user__userprofile__privacy='public').order_by('-created_at')
    return render(request, 'posts.html', {'posts': public_posts})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    
    if user in post.likes.all():
        post.likes.remove(user)  
    else:
        post.likes.add(user)  

    return redirect('profile', user_id=request.user.id) 

@login_required
def toggle_like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        content = request.POST.get('comment')
        Comment.objects.create(post=post, user=request.user, content=content)
    return redirect(request.META.get('HTTP_REFERER', '/'))    

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user:
        comment.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def msg_req(request):
    return render(request, 'msg_reg.html')

def accept_follow_request(request, message_id):
    profile_user = get_object_or_404(User, id=request.user.id)
    message = get_object_or_404(Message, id=message_id)
    if message.recipient == request.user:
        message.sender.userprofile.following.add(request.user)
        profile_user.userprofile.followers.add(message.sender)
        message.sender.userprofile.save()            
        profile_user.userprofile.save()
        message.is_accepted = True
        message.save()
        message.delete()
    return HttpResponseRedirect(reverse('messages'))

def reject_follow_request(request, message_id):
    profile_user = get_object_or_404(User, id=request.user.id)
    message = get_object_or_404(Message, id=message_id)
    if message.recipient == request.user:
        message.sender.userprofile.following.remove(request.user)
        profile_user.userprofile.followers.remove(message.sender)
        message.sender.userprofile.save()            
        profile_user.userprofile.save()
        message.delete()
    return HttpResponseRedirect(reverse('messages'))

from .models import Message

def delete_message(request, message_id):
    if request.method == 'POST':
        message = get_object_or_404(Message, id=message_id)
        if message.recipient == request.user:
            message.delete()
    return redirect('messages')
