from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .forms import MyUserCreationForm
from .models import Profile, FriendManager
from .forms import ProfileForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class SignUpView(CreateView):
    form_class = MyUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def profileview(request):
    profiles = Profile.objects.all()
    profile_updated_user = []
    for i in profiles:
        profile_updated_user.append(i.user)
    if request.method == 'POST':
        forms = ProfileForm
        form = forms(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            print("in is valid")
            instances = form.save(commit=False)
            instances.user = request.user
            instances.save()
            return redirect('accounts:home')
    elif request.user not in profile_updated_user:
        print("in elif")
        form = ProfileForm
        return render(request, 'profile/profile.html', {'form': form})
    else:
        print("in else")
        profile = get_object_or_404(Profile, user=request.user)
        return render(request, 'profile/profiledetails.html', {'profile': profile})


@login_required
def myfriends(request):
    user = request.user
    fr = FriendManager.objects.filter(approval=True)
    friends = fr.filter((Q(first_user__id__iexact=user.id)
                         | Q(second_user__id__iexact=user.id)))
    return render(request, 'friends/myfriends.html', {'friend_list': friends})

# rest done


@login_required
def friend_request(request, id):
    user2 = get_object_or_404(User, id=id)
    fr = FriendManager.objects.all()
    # add logic for existing request
    friends = fr.filter(((Q(first_user__id__iexact=user2.id) & Q(second_user__id__iexact=request.user.id)) | (
        Q(first_user__id__iexact=request.user.id) & Q(second_user__id__iexact=user2.id))))
    if len(friends) != 0:
        return redirect('accounts:home')
    else:
        FriendManager.objects.create(
            first_user=request.user, second_user=user2)
        return redirect('accounts:home')


@login_required
def friend_approve(request, id):
    query = get_object_or_404(FriendManager, id=id)
    query_instances = query
    query_instances.approval = True
    query_instances.save()
    return redirect('accounts:requestslist')


@login_required
def friend_reject(request, id):
    FriendManager.objects.filter(id=id).delete()
    return redirect('accounts:requestslist')


@login_required
def requestlist(request):
    user = request.user
    fr = FriendManager.objects.filter(approval=False)
    friends = fr.exclude(first_user=user)

    return render(request, 'friends/request.html', {'friend_list': friends})

# done find friend section


@login_required
def find_friends(request):
    profiles = Profile.objects.all()
    my_profile = Profile.objects.get(user=request.user)
    profiles = profiles.exclude(user=request.user)
    q_profile = profiles.filter(interest=my_profile.interest)

    user = request.user
    fr = FriendManager.objects.all()
    friends = fr.filter((Q(first_user__id__iexact=user.id)
                         | Q(second_user__id__iexact=user.id)))
    for req_fr in friends:
        for i in q_profile:
            if (req_fr.first_user.id == i.user.id)or(req_fr.second_user.id == i.user.id):
                q_profile = q_profile.exclude(user=i.user)
    return render(request, 'friends/index.html', {'friend_list': q_profile})


def landing(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')
    else:
        return render(request, 'landing.html')
