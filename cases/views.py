from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from .forms import AlertForm
from .models import Case


def index(request):
    template = "cases/index.html"
    title = "Reported Malnutrition Cases"
    recent_cases = Case.objects.all().order_by('-published')[0:3]

    context = {
        'template': template,
        'title': title,
        'recent_cases': recent_cases,
    }
    return render(request, template, context)


def add_case(request):
    template = "cases/add_case.html"
    title = "Malnutrition Alerts"
    recent_cases = Case.objects.all().order_by('-published')[0:3]

    if request.method == 'POST':
        form = AlertForm(request.POST, request.FILES)

        if form.is_valid():
            save_case = form.save(commit=False)
            save_case.save()

            #Email sending
            subject = "Thank you for Reporting a Malnutrition Case"
            message = "Your malnutrition alert has been received and we are following up on the issue, you will be contacted within 48 hours for further clarification."
            from_email = settings.EMAIL_HOST_USER
            to_list = [save_case.email_address]

            send_mail(subject, message, from_email, to_list, fail_silently=False)

            subject2 = "Malnutrition Alert"
            message2 = "A malnutrition case has been reported, please check as soon as you can"
            from_email2 = settings.EMAIL_HOST_USER
            to_list2 = [settings.EMAIL_HOST_USER]

            send_mail(subject2, message2, from_email2, to_list2, fail_silently=False)

            messages.success(request, 'Your case was successfully submitted, '
                                      'please note that you may be contacted for more information.')
            return HttpResponseRedirect('new')

    else:
        form = AlertForm

    context = {
        'template': template,
        'title': title,
        'form': form,
        'recent_cases': recent_cases,
    }
    return render(request, template, context)
