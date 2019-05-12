from django.shortcuts import render, HttpResponse
from .models import SubmittedCampaign, County, Vote, OpenCampaign
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .forms import VoterForm, CampaignForm
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail


def index(request):
    title = 'Open Campaigns'
    template = 'campaigns/index.html'
    campaigns = OpenCampaign.objects.filter(registration_status='open')

    context = {
        'title': title,
        'campaigns': campaigns,
    }

    return render(request, template, context)


def posted_campaigns(request):
    title = 'Proposed Campaigns'
    template = 'campaigns/campaigns.html'
    campaigns = SubmittedCampaign.objects.all().order_by('-published')
    voting = OpenCampaign.objects.filter(voting_status='open')

    #open_camapaign_title = OpenCampaign.campaign_title

    context = {
        'title': title,
        'campaigns': campaigns,
        'voting': voting,
    }

    return render(request, template, context)


def details(request, campaign_id):
    campaign = SubmittedCampaign.objects.get(id=campaign_id)
    context = {
        'campaign': campaign,
    }
    return render(request, 'campaigns/details.html', context)


def vote(request, campaign_id):
    campaign = SubmittedCampaign.objects.get(id=campaign_id)
    #open_campaign = SubmittedCampaign.open_campaign_id
    #voting_status = open_campaign
    title = "Confirm your vote"
    template = 'campaigns/vote.html'
    date = timezone.now
    current_user = request.user

    if request.method == 'POST':
        form = VoterForm(request.POST)

        if form.is_valid():
            user = Vote.objects.filter(voter_id=current_user.id)
            if user:
                messages.warning(request, 'You can only vote once.')
                return HttpResponseRedirect('vote')
            else:
                form.save()

                campaign = get_object_or_404(SubmittedCampaign, pk=campaign_id)

                campaign.total_votes += 1
                campaign.save()

                messages.success(request, 'Your vote was successfully submitted.')
                return HttpResponseRedirect('../')

    else:

        form = VoterForm

    context = {
        'form': form,
        'title': title,
        'campaign': campaign,
        'date': date,
        'current_user': current_user,
        #'voting_status': voting_status,
    }

    return render(request, template, context)

    # campaign = get_object_or_404(Campaign, pk=campaign_id)

    # campaign.total_votes += 1
    # campaign.save()

    # return HttpResponseRedirect(reverse('campaigns:details', args=(campaign.id,)))
    # return HttpResponse("Voting for campaign with an ID of %s" % campaign_id)


def add_campaign(request, open_campaign_id):
    campaign = OpenCampaign.objects.get(id=open_campaign_id)
    open_campaigns = OpenCampaign.objects.all()
    title = 'Submit your campaign'
    template = 'campaigns/add_campaign.html'
    date = timezone.now

    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES)

        if form.is_valid():
            campaign_save = form.save(commit=False)
            campaign_save.save()

            # Email sending
            subject = "Campaign Proposal Submitted"
            message = "Your campaign proposal has been received and is awaiting the voting period."
            from_email = settings.EMAIL_HOST_USER
            to_list = [campaign_save.email_address]

            send_mail(subject, message, from_email, to_list, fail_silently=False)

            subject2 = "New Campaign Proposal"
            message2 = "A new campaign proposal has been submitted to your system"
            from_email2 = settings.EMAIL_HOST_USER
            to_list2 = [settings.EMAIL_HOST_USER]

            send_mail(subject2, message2, from_email2, to_list2, fail_silently=False)

            messages.success(request, "Your campaign has been received, wait for the voting period")
            return HttpResponseRedirect('../')
        else:
            messages.error(request, "Invalid data! Please correct the errors below")
    else:
        form = CampaignForm

    context = {
        'campaign': campaign,
        'open_campaigns': open_campaigns,
        'title': title,
        'date': date,
        'form': form,
    }
    return render(request, template, context)

    #return HttpResponse('Add new campaigns page')
