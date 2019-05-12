from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm
from campaigns.models import SubmittedCampaign, Vote
# from accounts.models import ProfilePictures
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import login, authenticate

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token

from django.contrib.auth import login
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode




#def register(request):
 #   if request.method == 'POST':
  #      form = UserRegistrationForm(request.POST)
   #     if form.is_valid():
    #        form.save()
     #       username = form.cleaned_data.get('username')
      #      raw_password = form.cleaned_data.get('password1')
       #     user = authenticate(username=username, password=raw_password)
        #    login(request, user)

         #   messages.success(request, 'Your account has been created successfully')
          #  return render(request, 'accounts/register_done.html')
    #else:
     #   form = UserRegistrationForm()
    #return render(request, 'accounts/signup.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Nutritious Kenya Account'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('accounts:account_activation_sent')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def account_activation_sent(request):
    template = 'accounts/account_activation_sent.html'

    return render(request, template)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        messages.success(request, 'You account has been successfully activated, you can now login, upload campaign proposals and report malnutrition cases.')
        return redirect('/')
    else:
        return render(request, 'accounts/account_activation_invalid.html')


def user_profile_view(request, user_id):
    #user_details = User.objects.get(id=user_id)
    user_details = request.user
    #campaigns = Campaign.objects.filter(campaign_owner_id=user_id)
    #campaigns = SubmittedCampaign.objects.filter(campaign_owner_id=request.user.id)
    user = request.user.id
    votes = Vote.objects.filter(voter_id=user)

    #profile = ProfilePictures.objects.all()

    title = 'Dashboard'
    template = 'accounts/profile.html'

    #if request.method == 'POST':
     #   form = forms.ProfilePictureForm(request.POST, request.FILES)

      #  if form.is_valid():
       #     form.save()

        #else:
         #   messages.error(request, "Cannot update profile image")
    #else:
     #   form = forms.ProfilePictureForm

    context = {
        'user_details': user_details,
        'title': title,
        #'campaigns': campaigns,
        'votes': votes,
        #'form': form,
        # 'profile': profile,
    }
    return render(request, template, context)


def edit_profile_view(request, user_id):
    template = 'accounts/edit_profile.html'
    title = 'Edit Profile'

    if request.method == 'POST':
        form = forms.EditProfileForm(request.POST, instance=request.user)
        #more_details_form = forms.EditProfileForm2(request.POST, instance=request.user, files=request.FILES)
        #if form.is_valid() and more_details_form.is_valid():
        if form.is_valid():
            form.save()
         #   more_details_form.save()

            messages.success(request, "You profile has been successfully updated")
            #return redirect('/accounts/profile')

        else:
            messages.error(request, "Invalid form data")
    else:
        form = forms.EditProfileForm(instance=request.user)
        #more_details_form = forms.EditProfileForm2(instance=request.user)

    context = {
        'template': template,
        'title': title,
        'form': form,
        #'more_details_form': more_details_form
    }

    return render(request, template, context)

