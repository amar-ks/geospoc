from django.shortcuts import render
from .models import UserProfile
import socket
import geocoder
from nocaptcha_recaptcha.fields import NoReCaptchaField
from django.http import JsonResponse


DOC_FILE_TYPES = ['doc', 'docx', 'pdf']


def index(request):
    name = ''
    email = ''
    web_address = ''
    cover_letter = ''
    attachment = ''
    working = ''
    message = 0

    if request.POST:
        if 'name' in request.POST:
            name = request.POST['name']
        if 'email' in request.POST:
            email = request.POST['email']
        if 'web_address' in request.POST:
            web_address = request.POST['web_address']
        if 'cover_letter' in request.POST:
            cover_letter = request.POST['cover_letter']
        if request.FILES and 'attachment' in request.FILES:
            attachment = request.FILES['attachment']
            if attachment != '':
                filename = attachment.name
                file_type = filename.split('.')
                if len(file_type) > 1:
                    file_name = file_type[0]
                    file_type = file_type[-1].lower()
                    if file_type not in DOC_FILE_TYPES:
                        context = {
                            'message': 4,
                        }
                        return render(request, 'geospoc/index.html', context)

        if 'working' in request.POST:
            working = request.POST['working']

        if name != '' and email != '' and web_address != '' and cover_letter != '' and attachment != '' and working != '':
            query = UserProfile.objects.filter(email__iexact=email)
            if query:
                context = {
                    'message': 2,
                }
                return render(request, 'geospoc/index.html', context)
            else:
                message = 1
                ip_address, ip_location = get_Host_location()
                captcha = NoReCaptchaField()
                # print(captcha)
                query = UserProfile(
                    name=name,
                    email=email,
                    web_address=web_address,
                    cover_letter=cover_letter,
                    attachment=attachment,
                    working=working,
                    ip_address=ip_address,
                    location=ip_location,
                )
                query.save()

        else:
            message = 3

    context = {
        'page_header': 'Geospoc Form',
        'page_title': 'User Form',
        'message': message
    }

    return render(request, "geospoc/index.html", context)


def get_Host_name_IP():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)

        return host_ip
    except:
        return 0


def get_Host_location():
    g = geocoder.ip('me')
    ip_address = g.ip
    ip_location_city = g.city
    ip_location_country = g.country
    ip_location_state = g.state
    ip_location_postal = g.postal
    # # ip_location_lat = g.lat
    # # ip_location_lng = g.lng

    ip_location = ip_location_city + ',' + ip_location_state + ',' + ip_location_country + ',' + ip_location_postal
    return ip_address, ip_location


def validate_email(request):
    message = 0
    if request.method == "POST" and request.is_ajax():
        user_exist = UserProfile.objects.filter(email__iexact=request.POST['email'])
        if user_exist:
            message = 1
        else:
            message = 2

    return JsonResponse({'message': message}, safe=False)
