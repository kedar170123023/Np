from    django.shortcuts                import render, redirect
from    django.http                     import HttpResponse
from    django.contrib.auth.decorators  import login_required
from    django.contrib.auth.models      import User
from    django.contrib.auth             import login                as auth_login   #as it clashes with other login term
from    django.template                 import RequestContext
from    django.shortcuts                import get_object_or_404 
from    .forms                          import * #all the components from .form
from    django.views.decorators.csrf    import csrf_exempt
from    navprayas                       import checksum             as Checksum
from    django.contrib                  import messages
from    django.core.mail                import send_mail
from    secret                          import *
from    django.utils.crypto             import get_random_string 
from    django.conf                     import settings
from    django.core.files.storage       import FileSystemStorage
from    .models                         import *
from    .dictUtils                      import ADFP as MAP
import  json
import  string
import  random
#from django.contrib.auth.models import User

TRN_DIGITS = 10


def OID(size=TRN_DIGITS, chars=string.digits):
    return get_random_string(TRN_DIGITS, chars)





# Create your views here.
def index(request):
    return render(request, 'navprayas/home_links/index.html', {})

def edit_profile(request):
    statuses = status(request.user)    
    if request.method == 'GET' :
        U_form = UserForm()
        u_form = UserDetailsForm()
        e_form = EducationForm()
        a_form = AddressForm()

        context = {

            'U_form': U_form,
            'u_form': u_form,
            'e_form': e_form,
            'a_form': a_form, 
            'status': statuses,
        }
    return render(request, 'navprayas/users/edit_profile.html', context)

def about(request):
    return render(request, 'navprayas/home_links/about.html', {})

def pay(request):
    return render(request, 'navprayas/paytm/pay.html', {})

def events(request):
    return render(request, 'navprayas/home_links/events.html', {})

def notifications(request):
    return render(request, 'navprayas/home_links/notifications.html', {})

def team(request):
    return render(request, 'navprayas/home_links/team.html', {})

def status(user):
    # contains status of each exam
    status_dict ={}

    for name, values in MAP.items():
        ALLOWED             = values['allowed']

        if not ALLOWED :
            status_dict[name]   = "<b>Coming Soon </b>"
        #if exam is allowed to register
        else : 
            PAYMENT_REQUIRED    = values['payment_required'] 
            # Initially set if user has not paid
            status_dict[name] = "<a href = '/{ExamName}_register/'> <b>Click Here </b></a> to Register".format(ExamName = name)
            #If user has registered for the exam
            if hasattr(user, name.lower()): 
                status_dict[name] = '<span class="text-success">SUCCESSFUL</span> '
                EXAM                = getattr(user, name.lower())
                # If Payment is required
                if PAYMENT_REQUIRED and not EXAM.success: 
                    status_dict[name] = "<a href = '/{ExamName}_register/'> <b>Click Here </b></a> to Pay".format(ExamName = name)

    return status_dict

# *************************
# signup form
# *************************
@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    np_email = USERID_FOR_EMAIL
    if request.method == 'POST':
        form = request.POST
        checksum = form['CHECKSUMHASH']
        TXNAMOUNT  = form['TXNAMOUNT']
        response_dict = form.dict()
        oid = response_dict['ORDERID']
        TRN   = Transaction.objects.filter(tid=oid).first()
        PRICE = TRN.amount
        MODEL = eval(TRN.trn_type)


        verified = Checksum.verify_checksum(response_dict, PAYMENT_MERCHANT_KEY, checksum)
        if verified:
            if response_dict['RESPCODE'] == '01' :
                if TXNAMOUNT == PRICE:
                    txndate = response_dict['TXNDATE']
                    EXAM = MODEL.objects.filter(user=TRN.user).first()
                    if EXAM is not None:
                        EXAM.success = True
                        EXAM.save()
                        email = EXAM.user.email
                        sub = "Confirmation for your registration"
                        mgs = "You  have succesfullly registered for {ExamName}.\n Your application ID is ".format(MAP[TRN.trn_type]['description']) + str(oid) + ".\n\n\n\n\n\n\n\n" + "NAVPRAYAS OFFICE\n 1st floor Durga Asthan Market \nManpur Patwatoli Gaya,PIN-823003\nBihar, India"
                        send_mail(sub, mgs, np_email, [email])
                    else :
                        return HttpResponse('ORDER AMOUNT WAS CHANGED IN BETWEEN\n we will send you your refund')
            else:
                print('order was not successful')
        return render(request, 'navprayas/paytm/status.html', {'response': response_dict})
    return redirect('index')


def pay(user_id,price, name):
    #continue to create a transaction until valid Transaction id is created 
    while(True):
        try:
            oid = 'O20'+OID()
            Transaction.objects.create(
                user_id     = user_id,
                tid         = oid,
                trn_type    = name,
                amount      = float(price),
                )
            break
        except :
            pass


    param_dict = {
            'MID': PAYMENT_MERCHANT_ID,
            'ORDER_ID': oid,
            'TXN_AMOUNT': str(price),
            'CUST_ID': str(user_id),
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'DEFAULT',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://localhost:8000/handlerequest/',
            'INDUSTRY_TYPE_ID' : 'Retail',
            'CHANNEL_ID' : 'WEB',

            }
    print(param_dict)
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, PAYMENT_MERCHANT_KEY)
    return param_dict


@login_required
def profile(request):
    statuses=status(request.user)
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST,instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            return redirect('profile')

    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'p_form': p_form,
        'status': statuses,
    }

    return render(request, 'navprayas/users/profile.html', context)


def register(request):
    if request.method == 'POST':
        gender = request.POST.get("gender")
        birth_date = request.POST.get("birth_date")
        form = SignUpForm(request.POST)
        form2 = SignUpFormProfile(request.POST)
        if form.is_valid() and form2.is_valid():
            email       = form.cleaned_data['email']

            #check if username already exits
            if User.objects.filter(email = email).exists():
                messages.warning(request, 'username already exists')
                form = SignUpForm(request.POST)
                context = {
                'form' : form,
                'form2' : form2,
                }
                return render(request, 'navprayas/users/signup.html',context)
            #create user
            password1   = form.cleaned_data['password1']
            password2   = form.cleaned_data['password2']
            # check if passwords are same
            if not (password1 == password2):
                messages.warning(request, 'Passwords do not match')
                form = SignUpForm(request.POST)
                context = {
                'form' : form,
                'form2' : form2,
                }
                return render(request, 'navprayas/users/signup.html',context)
            #finally creating user with same email and username
            user = User.objects.create_user(email,email,password1)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            a = Profile.objects.filter(user = user).first()
            a.gender = gender
            a.birth_date = birth_date
            a.save()
            return redirect('index')
        else:
            messages.warning(request, 'Please Enter Valid Details')
            form = SignUpForm(request.POST)
            context = {
            'form' : form,
            'form2' : form2,
            }
            return render(request, 'navprayas/users/signup.html',context)
        
    else:
        form = SignUpForm()
        form2 = SignUpFormProfile()
    context = {
        'form' : form,
        'form2' : form2,
    }    
    return render(request, 'navprayas/users/signup.html',context)



def exam_register(request, name):
    VALUES              = MAP[name]
    ALLOWED             = VALUES['allowed']

    if not ALLOWED : 
        return redirect('index')

    MODEL               = eval(name)
    PAYMENT_REQUIRED    = VALUES['payment_required']
    FORM                = eval(name+"_form")
    PRICE               = VALUES['fee'] 



    EXAM = MODEL.objects.filter(user=request.user).first() 
    #if form is not filled
    if EXAM is None: 
        if request.method == 'POST':
            form = FORM(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user=request.user
                form.save()
                #form filled
                #proceed for paymment
                if PAYMENT_REQUIRED :
                    param_dict = pay(request.user.id, PRICE, name)
                    print(param_dict)
                    return render(request, 'navprayas/paytm/paytm.html', {'param_dict': param_dict})
                #If payment is not required directly send to index no need to pay 
                else:
                    return redirect('index')
                    
            else:
                messages.warning(request, 'Please enter valid details')
                form = FORM(request.POST)
                return render(request, 'navprayas/exam_forms/{ExamName}_register.html'.format(ExamName=name), {'form': form})
        #GET METHOD 
        else:
            form = FORM()
            return render(request, 'navprayas/exam_forms/{ExamName}_register.html'.format(ExamName=name), {'form': form})  
    # If Form is Filled
    if not PAYMENT_REQUIRED :
        return redirect('index')
    # Payment is required and Form is filled 
    # needs to check whether payment is DONE or not
    # Only needs to be paid

    if EXAM.success is False:
        if request.method == 'POST' :
            form = FORM(request.POST,instance=getattr(request.user, name.lower()))
            if form.is_valid() :
                form = form.save()
                param_dict = pay(request.user.id, PRICE, name)
                print(param_dict)
                return render(request, 'navprayas/exam_forms/{ExamName}_register.html'.format(ExamName=name), {'form': form})
            else:
                messages.warning(request, 'Please enter valid details')
                form = FORM(instance=request.user.mtse)
                return render(request, 'navprayas/exam_forms/{ExamName}_register.html'.format(ExamName=name), {'form': form})
        #GET METHOD 
        else:
            form = FORM(instance=getattr(request.user, name.lower()))
            return render(request, 'navprayas/exam_forms/{ExamName}_register.html'.format(ExamName=name), {'form': form})
    else :
        return render(request, 'navprayas/home_links/submitted.html', {})

# /////////////////////////
# Exam_forms
# /////////////////////////



@login_required
def MTSE_register(request):
    return exam_register(request,"MTSE")
@login_required
def CC_register(request):
    return exam_register(request,"CC")
@login_required
def CHESS_register(request):
    return exam_register(request,"CHESS")
@login_required
def RANGOTSAV_register(request):
    return exam_register(request,"RANGOTSAV")
@login_required
def FHS_register(request):
    return exam_register(request,"FHS")


@login_required
def PR_register(request):
    return exam_register(request,"PR")

# /////////////////////////
# Result
# /////////////////////////

def results_out(request):
    return render(request,'navprayas/results/results.html')

def results_out_19(request):
    return render(request,'navprayas/results/results_eventwise.html')



def videos_list(request):
    videos = Document.objects.all()
    context = []
    for video in videos:
        context.append(('/play/' + str(video.id),
                        video.title,
                        video.uploader,
                        video.uploaded_at,
        ))
    print(context)
    return render(request, 'navprayas/video/videos.html', {'videos' : context})

@login_required
def file_upload(request):
    if(not request.user.is_superuser):
        messages.warning(request, 'You are not allowed to upload videos')
        return redirect('index')

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            unsaved_form = form.save(commit = False)
            unsaved_form.uploader = request.user
            unsaved_form.save()           

            return redirect('index')
    else:
        form = DocumentForm()
        # print("form",form)
    return render(request, 'navprayas/video/file_upload.html', {
        'form': form
    })

def play(request,video_id):
    try: 
        video = get_object_or_404(Document,pk=video_id)
    except : 
        return redirect('videos_list')

    return render(request, 'navprayas/video/play.html', {'video' : video})
