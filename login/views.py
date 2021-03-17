import json

from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.decorators import api_view
from .tokens import account_activation_token

from login.models import user


@api_view(["POST"])
def user_registration(request):
    to_email = json.loads(request.body).get('email')
    present = list(user.object.get(email=to_email))
    if len(present):
        return JsonResponse(data="User already exists", safe=False, status=400)
    current_site = get_current_site(request)
    mail_subject = 'Activate your account.'
    message = render_to_string('acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })

    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
    return JsonResponse(data="Please confirm your email address", safe=False, status=201)


@api_view(["GET"])
def get_user(request, email):
    user_details = list(user.objects.get(email=email))
    if len(user_details):
        user_details = user_details[0]
        del (user_details['password'])
        if not user_details['is_active']:
            return JsonResponse(data='Please activate your email', safe=False)
    else:
        return JsonResponse(data='User not found', safe=False)
    return JsonResponse(data=user_details, safe=False)


@api_view(['PUT'])
def update_user(request, email):
    request_body = json.loads(request.body)
    try:
        user.objects.filter(email=email).update(firstName=request_body.get('firstName'),
                                                           lastName=request_body.get('lastName'),
                                                           phone=request_body.get('phoneNumber'))
        return JsonResponse(data='User updated successfully', status=200)
    except:
        return JsonResponse(data='User not found', status=400)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user_detail = user.objects.get(pk=uid)
    except:
        user_detail = None
    if user_detail is not None and account_activation_token.check_token(user_detail, token):
        user_detail.is_active = True
        user_detail.save()
        login(request, user_detail)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
