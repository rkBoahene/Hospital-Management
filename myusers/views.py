from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.http import Http404
from .forms import *
from .forms import DivErrorList
from django.template.response import TemplateResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import *
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from geoip import geolite2
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Create your views here.


def log_user_activity(module, description, user_id, device, ip_address, client_id):
    user = HMUser.objects.get(id=int(user_id))
    myactivity = UserActivity.objects.create(module=module,
                                             description=description,
                                             user=user,
                                             client=user.client,
                                             device=device,
                                             ip_address=ip_address
                                             )
    if client_id:
        myclient = Client.objects.get(id=int(client_id))
        myactivity.client = myclient
        myactivity.save()
    try:
        match = geolite2.lookup(myactivity.ip_address)
        myactivity.country = match.get_info_dict()['country']['names']['en']
        myactivity.latitude = match.get_info_dict()['location']['latitude']
        myactivity.longitude = match.get_info_dict()['location']['longitude']
        myactivity.save()
    except:
        print('failed')


@login_required
def user_activity_view(request):
    if request.user.is_authenticated():
        if request.user.permission == '0' or request.user.permission == '1' or request.user.permission == '2' or request.user.permission == '3':
            activities = UserActivity.objects.select_related('client', 'user').filter(Q(user__permission='0') |
                                                                                      Q(user__permission='1') |
                                                                                      Q(user__permission='2') |
                                                                                      Q(user__permission='3')).order_by('-id')
            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1

            p = Paginator(activities, request=request, per_page=10)

            activities = p.page(page)

            context = {
                'activities': activities,
            }
            return render(request, 'user_activity.html', context)
        elif request.user.permission == '4' or request.user.permission == '5' or request.user.permission == '6':
            activities = UserActivity.objects.select_related('client', 'user').filter(Q(user__permission='4') |
                                                                                      Q(user__permission='5') |
                                                                                      Q(user__permission='6')).order_by('-id')
            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1

            p = Paginator(activities, request=request, per_page=10)

            activities = p.page(page)

            context = {
                'activities': activities,
            }
            return render(request, 'user_activity.html', context)
        else:
            raise Http404


@login_required
def client_user_activity_view(request):
    if request.user.is_authenticated():
        if request.user.permission == '0' or request.user.permission == '1' or request.user.permission == '2' or request.user.permission == '3':
            activities = UserActivity.objects.select_related('client', 'user').filter(Q(user__permission='4') |
                                                                                      Q(user__permission='5') |
                                                                                      Q(user__permission='6')).order_by('-id')
            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1

            p = Paginator(activities, request=request, per_page=10)

            activities = p.page(page)

            context = {
                'activities': activities,
            }
            return render(request, 'client_user_activity.html', context)
        else:
            raise Http404


@login_required
def client_activity_view(request):
    if request.user.is_authenticated():
        if request.user.permission == '4' or request.user.permission == '5' or request.user.permission == '6':
            activities = UserActivity.objects.select_related('client', 'user').filter(Q(user__permission='4') |
                                                                                      Q(user__permission='5') |
                                                                                      Q(user__permission='6'), client=request.user.client).order_by('-id')
            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1

            p = Paginator(activities, request=request, per_page=10)

            activities = p.page(page)

            context = {
                'activities': activities,
            }
            return render(request, 'client_activity.html', context)
        else:
            raise Http404


# def handler500(request):
#     return JsonResponse({'response_code': 500, 'response_message': 'The server encountered an error. Our engineers have been notified and will fix it shortly'}, status=500)


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


# @ratelimit(key='ip', rate='10/m')
# def home(request):
#     next = request.GET.get('next')
#     if request.user.is_authenticated():
#         if request.user.permission == '0' or request.user.permission == '1' or request.user.permission == '2' or request.user.permission == '3':
#             redirect('/dashboard/')

#     if request.method == "POST":
#         form = LoginForm(request.POST, error_class=DivErrorList)
#         # if form.is_valid():
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         try:
#             myuser = HMUser.objects.get(email=email)

#             if myuser.is_blocked:
#                 cooloff = (timezone.now(
#                 ) - myuser.failed_login_attempts.all().latest('id').datecreated).seconds
#                 if cooloff > 300:
#                     myuser.is_blocked = False
#                     myuser.temporal_login_fails = 0
#                     myuser.save()
#                 else:
#                     left = int(300) - int(cooloff)
#                     return render(request, 'login.html', {'form': form, 'detail': 'You have attempted to login 5 times, with no success. Your account is locked for %s seconds' % left})

#             user = authenticate(username=email, password=password)
#             if user is not None:
#                 if user.is_active:
#                     userobject = authenticate(email=email, password=password)
#                     if userobject is not None and userobject.is_active == True:
#                         login(request, userobject)
#                         myuser.temporal_login_fails = 0
#                         myuser.save()
#                         if request.user.permission == '0' or request.user.permission == '1' or request.user.permission == '2' or request.user.permission == '3' or request.user.permission == '4' or request.user.permission == '5' or request.user.permission == '6' or request.user.permission == '7':
#                             return redirect('/dashboard/')
#                     else:
#                         return render(request, 'login.html', {'form': form})
#                 else:
#                     if user.is_blocked:
#                         return render(request, 'login.html', {'form': form, 'detail': 'Your account is locked permanently. Contact Support'})

#             else:
#                 FailedLogin.objects.create(
#                     author=myuser, ip_address=request.META['HTTP_X_FORWARDED_FOR'])
#                 myuser.temporal_login_fails += 1
#                 myuser.save()
#                 if int(myuser.temporal_login_fails) == 5:
#                     myuser.is_blocked = True
#                     myuser.permanent_login_fails += 1
#                     myuser.save()
#                     if int(myuser.permanent_login_fails) >= 5:
#                         myuser.is_active = False
#                         myuser.save()

#                     return render(request, 'login.html', {'form': form, 'detail': 'You have attempted to login 5 times, with no success. "Your account is locked for 300 seconds'})
#                 left = 5 - myuser.temporal_login_fails
#                 return render(request, 'login.html', {'form': form, 'detail': 'Your Password is incorrect. %s tries left' % left})

#         except HMUser.DoesNotExist:
#             print('dettol')
#             return render(request, 'login.html', {'form': form, 'detail': 'Your email does not exist.'})
#         return render(request, 'login.html', {'form': form})
#     ''' user is not submitting any form, show the login form '''
#     form = LoginForm()
#     context = {
#         'next': next,
#         'form': form,
#     }
#     return render(request, 'login.html', context)


# def disabled_view(request):
#     return render(request, 'disabled.html')


# @login_required
# def overview(request):
#     if request.user.is_authenticated():
#         if request.user.is_active:
#             if request.user.permission == '0' or request.user.permission == '1' or request.user.permission == '2' or request.user.permission == '3' or request.user.permission == '7':
#                 no_of_clients = Client.objects.all().count()
#                 no_of_users = HMUser.objects.filter(Q(permission='1') |
#                                                     Q(permission='2') |
#                                                     Q(permission='3')
#                                                     ).count()
#                 transactions = Transaction.objects.select_related('client', 'channel').filter(
#                     is_sandbox=False).exclude(transaction_type='OVACR')
#                 no_of_transactions = transactions.count()
#                 total_amount = transactions.filter(transaction_status='success').aggregate(
#                     Sum('credit_amt'))['credit_amt__sum']
#                 today = timezone.now() - relativedelta(days=7)
#                 mypossibles = transactions.filter(
#                     time_created__gte=today, transaction_status='success').order_by('-id')
#                 mygraph = mypossibles.annotate(date=TruncDate('time_created')).values('date').annotate(
#                     amount=Sum('credit_amt')).annotate(count=Count('date')).order_by('date')

#                 myreports = transactions.order_by('-id')[:10]
#                 context = {
#                     'myreports': myreports,
#                     'no_of_clients': no_of_clients,
#                     'no_of_users': no_of_users,
#                     'no_of_transactions': no_of_transactions,
#                     'total_amount': total_amount,
#                     'mygraph': mygraph,
#                 }
#                 try:
#                     log_user_activity('OVERVIEW', 'accessed overview ', request.user.id,
#                                       request.META['HTTP_USER_AGENT'], request.META['HTTP_X_FORWARDED_FOR'], '')
#                     return render(request, 'dashboard.html', context)
#                 except:
#                     log_user_activity('OVERVIEW', 'accessed overview ', request.user.id,
#                                       request.META['HTTP_USER_AGENT'], 'LOCALHOST', '')
#                     return render(request, 'dashboard.html', context)

#             elif request.user.permission == '4' or request.user.permission == '5' or request.user.permission == '6':
#                 no_of_users = HMUser.objects.filter(Q(permission='5') |
#                                                     Q(permission='6'), client=request.user.client).count()
#                 transactions = Transaction.objects.select_related('client', 'channel').filter(
#                     client=request.user.client, is_sandbox=False).exclude(transaction_type='OVACR')
#                 no_of_transactions = transactions.count()
#                 total_amount = transactions.filter(transaction_status='success').aggregate(
#                     Sum('credit_amt'))['credit_amt__sum']
#                 myreports = transactions.order_by('-id')[:10]
#                 today = timezone.now() - relativedelta(days=7)
#                 mypossibles = transactions.filter(
#                     time_created__gte=today, client=request.user.client, transaction_status='success').order_by('-id')
#                 mygraph = mypossibles.annotate(date=TruncDate('time_created')).values('date').annotate(
#                     amount=Sum('credit_amt')).annotate(count=Count('date')).order_by('date')
#                 context = {
#                     'myreports': myreports,
#                     'no_of_users': no_of_users,
#                     'no_of_transactions': no_of_transactions,
#                     'total_amount': total_amount,
#                     'mygraph': mygraph,
#                 }
#                 try:
#                     log_user_activity('OVERVIEW', 'accessed overview ', request.user.id,
#                                       request.META['HTTP_USER_AGENT'], request.META['HTTP_X_FORWARDED_FOR'], '')
#                     return render(request, 'dashboard.html', context)
#                 except:
#                     log_user_activity('OVERVIEW', 'accessed overview ', request.user.id,
#                                       request.META['HTTP_USER_AGENT'], 'LOCALHOST', '')
#                     return render(request, 'dashboard.html', context)
#             else:
#                 raise Http404
#         else:
#             return redirect('/disabled/')


# @login_required
# def users_view(request):
#     if request.user.is_authenticated():
#         if request.user.is_active:
#             if request.user.permission == '0' or request.user.permission == '1':
#                 myusers = HMUser.objects.filter(Q(permission='1') |
#                                                 Q(permission='2') |
#                                                 Q(permission='3')
#                                                 )
#                 form = HMUsersForm()
#                 if request.method == "POST":
#                     form = HMUsersForm(request.POST or None,
#                                        error_class=DivErrorList)
#                     if form.is_valid():
#                         my_user = form.save(commit=False)
#                         my_user.save()
#                         char_set = string.ascii_lowercase + string.ascii_uppercase + \
#                             string.digits + string.punctuation
#                         mypassword = ''.join(random.sample(char_set*6, 10))
#                         my_user.set_password(mypassword)
#                         my_user.save()

#                         if my_user.permission == '1':
#                             permission = 'UNITY LINK Admin Viewer'
#                         elif my_user.permission == '2':
#                             permission = 'UNITY LINK Admin Maker'
#                         elif my_user.permission == '3':
#                             permission = 'UNITY LINK Admin Checker'
#                         elif my_user.permission == '7':
#                             permission = 'UNITY LINK Director'

#                         web_link = request.get_host()
#                         email_body = '<p>Hello %s %s, <br><br>Welcome to Unity Link GPS. <br/><br/>Your %s account has been created. Please visit this <a href="http://%s/">link</a> and use the following credentials to login </p><br/>Email: %s <br/> Password: %s<br/><br/><p> Kind regards,<br/> Unity Link GPS Team.' % (
#                             my_user.first_name, my_user.last_name, permission, web_link, my_user.email, mypassword)
#                         msg = EmailMultiAlternatives(
#                             subject="Welcome to Unity Link GPS",
#                             body='Welcome to Unity Link GPS',
#                             from_email="Unity Link GPS <hello@korbaweb.com>",
#                             to=[my_user.email],
#                             headers={'Reply-To': "Support <911@korbaweb.com>"}
#                         )
#                         msg.attach_alternative(email_body, "text/html")
#                         msg.send()

#                         return HttpResponseRedirect('/dashboard/users/')
#                     else:
#                         context = {
#                             'myusers': myusers,
#                             'form': form
#                         }
#                         return render(request, 'users.html', context)
#                 context = {
#                     'myusers': myusers,
#                     'form': form
#                 }
#                 return render(request, 'users.html', context)
#             elif request.user.permission == '4':
#                 myusers = HMUser.objects.filter(Q(permission='5') |
#                                                 Q(permission='6'), client=request.user.client)
#                 form = ClientForm()
#                 if request.method == "POST":
#                     form = ClientForm(request.POST or None,
#                                       error_class=DivErrorList)
#                     if form.is_valid():
#                         my_user = form.save(commit=False)
#                         my_user.client = request.user.client
#                         my_user.name_of_client = request.user.name_of_client
#                         my_user.save()

#                         char_set = string.ascii_lowercase + string.ascii_uppercase + \
#                             string.digits + string.punctuation
#                         mypassword = ''.join(random.sample(char_set*6, 10))
#                         my_user.set_password(mypassword)
#                         my_user.save()

#                         if my_user.permission == '5':
#                             permission = 'UNITY LINK Viewer'
#                         elif my_user.permission == '6':
#                             permission = 'UNITY LINK Developer'

#                         web_link = request.get_host()
#                         email_body = '<p>Hello %s %s, <br><br>Welcome to Unity Link GPS. <br/><br/>Your %s account has been created. Please visit this <a href="http://%s/">link</a> and use the following credentials to login </p><br/>Email: %s <br/> Password: %s<br/><br/><p> Kind regards,<br/> Unity Link GPS Team.' % (
#                             my_user.first_name, my_user.last_name, permission, web_link, my_user.email, mypassword)
#                         msg = EmailMultiAlternatives(
#                             subject="Welcome to Unity Link GPS",
#                             body='Welcome to Unity Link GPS',
#                             from_email="Unity Link GPS <hello@korbaweb.com>",
#                             to=[my_user.email],
#                             headers={'Reply-To': "Support <911@korbaweb.com>"}
#                         )
#                         msg.attach_alternative(email_body, "text/html")
#                         msg.send()

#                         return HttpResponseRedirect('/dashboard/users/')
#                     else:
#                         context = {
#                             'form': form,
#                             'myusers': myusers,
#                         }
#                         return render(request, 'users.html', context)
#                 context = {
#                     'form': form,
#                     'myusers': myusers,
#                 }
#                 try:
#                     log_user_activity('USER MANAGEMENT', 'accessed users ', request.user.id,
#                                       request.META['HTTP_USER_AGENT'], request.META['HTTP_X_FORWARDED_FOR'], '')
#                     return render(request, 'users.html', context)
#                 except:
#                     log_user_activity('USER MANAGEMENT', 'accessed users ',
#                                       request.user.id, request.META['HTTP_USER_AGENT'], 'LOCALHOST', '')
#                     return render(request, 'users.html', context)
#                 context = {
#                     'form': form,
#                     'myusers': myusers,
#                 }
#                 return render(request, 'users.html', context)
#             else:
#                 raise Http404
#         else:
#             return redirect('/disabled/')


# @login_required
# def user_detail_view(request, pk):
#     if request.user.is_authenticated():
#         if request.user.is_active:
#             if request.user.permission == '0':
#                 myuser = HMUser.objects.get(
#                     Q(permission='1', id=int(pk)) |
#                     Q(permission='2', id=int(pk)) |
#                     Q(permission='3', id=int(pk))
#                 )
#                 form = HMUsersForm()
#                 if request.method == "POST":
#                     form = HMUsersForm(request.POST or None,
#                                        error_class=DivErrorList)
#                     if form.is_valid():
#                         my_user = form.save(commit=False)
#                         my_user.save()
#                         return HttpResponseRedirect('/dashboard/user_detail/%s/' % (pk))
#                     else:
#                         context = {
#                             'form': form,
#                             'myuser': myuser,
#                         }
#                         return render(request, 'user_detail.html', context)
#                 context = {
#                     'form': form,
#                     'myuser': myuser,
#                 }
#                 return render(request, 'user_detail.html', context)
#             if request.user.permission == '4':
#                 myuser = HMUser.objects.get(
#                     Q(permission='5') |
#                     Q(permission='6'), id=int(pk)
#                 )
#                 form = ClientForm(instance=myuser)
#                 if request.method == "POST":
#                     form = ClientForm(request.POST or None,
#                                       error_class=DivErrorList, instance=myuser)
#                     if form.is_valid():
#                         my_user = form.save(commit=False)
#                         my_user.save()
#                         return HttpResponseRedirect('/dashboard/user_detail/%s/' % (pk))
#                     else:
#                         context = {
#                             'form': form,
#                             'myuser': myuser,
#                         }
#                         return render(request, 'user_detail.html', context)
#                 context = {
#                     'form': form,
#                     'myuser': myuser,
#                 }
#                 try:
#                     log_user_activity('USER MANAGEMENT', 'accessed detail page of %s %s ' % (
#                         myuser.first_name, myuser.last_name), request.user.id, request.META['HTTP_USER_AGENT'], request.META['HTTP_X_FORWARDED_FOR'], '')
#                     return render(request, 'user_detail.html', context)
#                 except:
#                     log_user_activity('USER MANAGEMENT', 'accessed detail page of %s %s ' % (
#                         myuser.first_name, myuser.last_name), request.user.id, request.META['HTTP_USER_AGENT'], 'LOCALHOST', '')
#                     return render(request, 'user_detail.html', context)
#             else:
#                 raise Http404
#         else:
#             return redirect('/disabled/')


# @login_required
# def disable_user_view(request, pk):
#     if request.user.is_authenticated():
#         if request.user.is_active:
#             if request.user.permission == '0':
#                 if request.method == 'POST':
#                     myuser = HMUser.objects.get(
#                         Q(permission='1', id=int(pk)) |
#                         Q(permission='2', id=int(pk)) |
#                         Q(permission='3', id=int(pk))
#                     )
#                     myuser.is_active = False
#                     myuser.save()
#                     try:
#                         log_user_activity('USER MANAGEMENT', 'disabled %s %s ' % (myuser.first_name, myuser.last_name),
#                                           request.user.id, request.META['HTTP_USER_AGENT'], request.META['HTTP_X_FORWARDED_FOR'], '')
#                         return HttpResponseRedirect('/dashboard/user_detail/%s/' % (pk))
#                     except:
#                         log_user_activity('USER MANAGEMENT', 'disabled %s %s ' % (
#                             myuser.first_name, myuser.last_name), request.user.id, request.META['HTTP_USER_AGENT'], 'LOCALHOST', '')
#                         return HttpResponseRedirect('/dashboard/user_detail/%s/' % (pk))
#             elif request.user.permission == '4':
#                 if request.method == 'POST':
#                     myclient = HMUser.objects.get(Q(permission='5') |
#                                                   Q(permission='6'), id=int(pk), client=request.user.client
#                                                   )
#                     myclient.is_active = False
#                     myclient.save()
#                     return HttpResponseRedirect('/dashboard/user_detail/%s/' % (pk))
#             else:
#                 raise Http404
#         else:
#             return redirect('/disabled/')
