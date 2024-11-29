from django.shortcuts import render, redirect

from .models import HomieChatUser, Room, AttachedFile, CallModel, TranscriptsAndSummaries, UserDeviceData

from django.contrib.auth import get_user
# from .recordMeet import joinAsBot
from django.utils import timezone
from .forms import (
    HomieChatUserCreationForm,
    UserAuthenticationForm,
    HomieChatUserUpdateForm,
    RoomCreationForm,
    UploadFileForm
)

from django.contrib.auth import login, authenticate, logout

from django.views.generic import DetailView, ListView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required, user_passes_test
# from .paytm import generate_checksum, verify_checksum
from .utils import generate_room_code_new
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse, HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
import time

from PIL import ImageDraw
from django.contrib import messages 
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

config = {
    'admin_login': 'admin',
    'admin_pass': 'admin@123',
    'spectators': {'user1': 'pass1', 'user2': 'pass2'},
    'spectators_allowed': True,
    'spectators_allowed_without_password': False,
    'forbidden_ips': [],

    'host': '0.0.0.0',
    'port': 8502,
    'debug': True,

    'logged_users': {},
    'last_shot': time.time()
}

def user_creation_view(request):
    # go to profile
    # if already logged in
    if request.user.is_authenticated:
        return redirect('user_detail_view', pk=request.user.id)
    context = {}

    if request.method == 'POST':
        usercreationform = HomieChatUserCreationForm(request.POST, request.FILES)

        if usercreationform.is_valid():
            homiechatuser = usercreationform.save()

            email = usercreationform.cleaned_data.get('email')
            raw_password = usercreationform.cleaned_data.get('password1')

            authenticated_account = authenticate(email=email, password=raw_password)
            login(request, authenticated_account)

            return redirect('pricing')
            # return redirect('user_detail_view', pk=homiechatuser.id)
        else:
            context['form'] = usercreationform

    else: # GET request
        usercreationform = HomieChatUserCreationForm()

        context['form'] = usercreationform

    return render(request, 'rooms/user_creation_view.html', context=context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('user_detail_view', request.user.id)

    context = {}

    # initialize authentication form
    # to avoid UnboundLocalError
    # due to not assigning it
    if request.method == 'POST':
        form = UserAuthenticationForm(data=request.POST)
        print("Form is",form.is_valid())
        print(form.data)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('user_detail_view', pk=user.id)
        else:
            messages.error(request, "Error")

    else:
        form = UserAuthenticationForm()

    context['form'] = form

    return render(request, 'rooms/login_view.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('user_creation_view')

@login_required
def home_view(request):
    return render(request, 'rooms/landing.html')

def remote_desktop_route(request):
    if request.method == 'GET':
        return render(request, 'rooms/rdp.html')

def get_screenshot_route(request):
    if time.time() -config['last_shot']> 1.:
        shot = pyautogui.screenshot()
        draw = ImageDraw.Draw(shot)
        x, y = pyautogui.position()
        draw.ellipse((x - 10, y - 10, x + 10, y + 10), fill='green', outline='red')
        shot.save('screenshots/last.jpg')
        config['last_shot'] = time.time()
        
    return FileResponse(open('screenshots/last.jpg', 'rb'))


class UserDetailView(LoginRequiredMixin, DetailView):
    model = HomieChatUser
    template_name = 'rooms/user_detail_view.html'

    def get(self, request, pk):
        context = {}

        user = HomieChatUser.objects.get(id=pk)

        # only display the update button
        # if a user is view their own profile
        display_btn_update = False
        if request.user == user:
            display_btn_update = True

        context['user'] = user
        context['display_btn_update'] = display_btn_update
        context['username'] = request.user.username

        return render(request, self.template_name, context)


import subprocess
from django.core.serializers import serialize
class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'rooms/room_list_view.html'

    def get(self, request):
        context = {}
        # users can only view their own rooms
        rooms = Room.objects.filter(user=request.user)
        context['rooms'] = rooms
        context['json_rooms'] = rooms
        name = request.user.username
        order = Order.objects.filter(name=name).first()
 
        if order:
            context["plan"]= order.plan
            context["status"] = order.status
        

        return render(request, self.template_name, context)
    
    def post(self, request):
        room_code = request.POST['room_code']
        
        # print(request.POST)
        room = Room.objects.get(code=room_code)  # Replace your_room_id with the actual ID
        # room = Room.objects.filter(code=room_id)[0]
        room.created_at = timezone.localtime(datetime.now())
        # print("TIME NOW",datetime.now())
        room.save()
        

        if 'bot' in request.POST:
            proc = subprocess.run(["python", "C:\inetpub\wwwroot\homiechat\homiechat\rooms\recordMeet.py", room_code, f"{request.user.username}"])
            print(proc.args)
            return redirect('user_detail_view', pk=request.user.id)
        
        else:
            return redirect('meeting', room_code=room_code)
          



@login_required
def user_update_view(request):
    context = {}

    user = request.user

    if request.method == 'POST':
        form = HomieChatUserUpdateForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            homiechatuser = form.save()

            return redirect('user_detail_view', pk=request.user.id)
        else:
            context['form'] = form

    else: # GET request
        form = HomieChatUserUpdateForm(instance=user)

        context['form'] = form

    return render(request, 'rooms/user_update_view.html', context=context)



@login_required
def room_creation_view(request):
    context = {}
    user_order = Order.objects.get(name=request.user.username)
    plan = user_order.plan
    payment_status = user_order.status
    context['plan'] = plan
    if request.method == 'POST':
        roomcreationform = RoomCreationForm(request.POST)
        
        # Get the current user
        current_user = get_user(request) 
        print(plan, Room.objects.filter(created_at__date=timezone.now().date(), user=current_user).count())
        # Check if the current user has created 5 rooms on the current day
        if (plan == 'free' or payment_status == 'Pending') and Room.objects.filter(created_at__date=timezone.now().date(), user=current_user).count() >= 5:
            # Your logic to handle the case when the user has reached the limit
            # raise ValidationError("You can only create up to 5 rooms per day.")
            context['trial']="You can only create up to 5 rooms per day."
            context['form'] = roomcreationform
            print("this")
        
        else:

            if roomcreationform.is_valid():
                print('Room creation form validated.')

                rooms = Room.objects.all()

                # assume that this is the first room
                # hence id 0
                # this is safe because in case of empty Room queryset
                # first object's room will be signed with 0
                # those of subsequent ones will be signed by
                # the appropriate pk
                new_id = int(0)
                if rooms:
                    # if there are other rooms
                    # get the last room created
                    last_room = rooms[len(rooms) - 1]
                    # new id will be one greater
                    # than that of the last room
                    new_id = last_room.id + 1

                room = roomcreationform.save(commit=False)

                room.user = request.user
                print('room.id: ', new_id)
                room.code = generate_room_code_new(new_id)
                print('room.code: ', room.code)
                room.save()

                return redirect('room_list_view')
            else:
                print("Not a valid answer")
                context['form'] = roomcreationform

    else: # GET request
        roomcreationform = RoomCreationForm()

        context['form'] = roomcreationform

    
    return render(request, 'rooms/room_creation_view.html', context=context)

@login_required
def prepare_chat_view(request):
    context = {}

    return render(request, 'rooms/prepare_chat_view.html', context=context)


def features_view(request):
    context = {}

    return render(request, 'rooms/features.html', context=context)

@login_required
def join_chat_view(request, room_code):
    context = {}

    context['room_code'] = room_code

    return render(request, 'rooms/join_chat_view.html', context=context)

from django.http import JsonResponse

@login_required
def meeting(request, room_code):
    context = {}
    bot = False
    current_user = get_user(request)
    context['current_user'] = current_user
    context['room_code'] = room_code
    moderator = "none"
    try:
        room_name = Room.objects.filter(code=room_code)[0].name
        print(room_name)
        context['room_name'] = room_name
    except:
        context['room_name'] = room_code
    
    try:
        moderator = Room.objects.filter(code=room_code)[0].user
        moderator = HomieChatUser.objects.get(email=moderator).username 
        print("MODERATOR:",moderator)
    except:
        pass

    
    context['moderator'] = moderator
    
     # Handle file upload 
    # newfile = File()
    # if request.method == 'POST':
    #     form = FileForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         newfile = File(file=request.FILES['file'])
    #         newfile.name = request.FILES['file'].name
    #         newfile.urlname = generate_string()

    #         dur = request.POST['duration']
    #         d = get_duration(dur) # returns the correct duration as a timedelta
    #         newfile.duration = d
    #         newfile.expires_at = newfile.uploaded_at + d

    #         newfile.save()
    #         context.update({'file': newfile, 'form': form, 'download_url': newfile.urlname})

    #         # Redirect to the file list after POST
    #         # return HttpResponseRedirect('meeting', args=room_code)
    # else:
    #     form = FileForm()  # A empty, unbound form


    return render(request, 'rooms/meeting.html', context=context)


@login_required
def select_room_view(request):
    context = {}

    room_code = request.GET.get('room-input')
    print('room_code: ', room_code)
    
    context['placeholder'] = 'Enter room code ...'

    if room_code == None:
        context['warning'] = False
        return render(request, 'rooms/select_room_view.html', context=context)
    
    room_exists = (Room.objects.filter(code=room_code).count() == 1)

    if room_exists:
        return redirect('meeting', room_code=room_code)
    
    context['warning'] = True
    return render(request, 'rooms/select_room_view.html', context)


@login_required
def chatPage(request, username):
    user_obj = HomieChatUser.objects.get(username=username)
    users = HomieChatUser.objects.exclude(username=request.user.username)

    if request.user.id > user_obj.id:
        thread_name = f'chat_{request.user.id}-{user_obj.id}'
    else:
        thread_name = f'chat_{user_obj.id}-{request.user.id}'
    message_objs = CallModel.objects.filter(thread_name=thread_name)
    return render(request, 'rooms/main_chat.html', context={'user': user_obj, 'users': users, 'messages': message_objs})

@login_required
def calling_view(request):
    context = {}
    room_code=generate_room_code_new  
    # context['room_code'] = room_code  
    return render(request, 'rooms/calling.html', context=context)

# @login_required
# def pricing_view(request):
#     context = {}

#     return render(request, 'rooms/pricing.html', context=context)

# @api_view(['POST'])
# def file_upload(request):
#     print(request)
#     if request.method == 'POST' and request.FILES.get('file'):
#         file = request.FILES['file']
#         meeting_id = request.POST.get('meeting_id')  # Assume you pass the meeting ID from the frontend
#         user_id = request.POST.get('user_id')  # Assume you pass the user ID from the frontend
        
#         # Process the uploaded file as per your requirements
#         # For example, you can save it to the media folder or S3 bucket and store the URL in the database
#         # Here's an example of saving the file in the media folder:
#         file_path = f'media/{file.name}'  # This assumes you have a 'media' folder in your project's root directory
#         with open(file_path, 'wb') as destination:
#             for chunk in file.chunks():
#                 destination.write(chunk)

#         attached_file = AttachedFile.objects.create(file=file)
#         # Assuming you have defined a 'Meeting' model with a 'files' ManyToManyField for file attachments
#         meeting = Room.objects.get(code=meeting_id)
#         meeting.file.add(attached_file)

#         # Assuming you have defined a 'User' model with a 'files' ManyToManyField for file attachments
#         # user = HomieChatUser.objects.get(username=user_id)
#         # user.files.add(file_path)

#         # Return the file URL or any other response if needed
#         return Response({'message': 'File uploaded successfully'})
#     return Response({'error': 'File not found'}, status=400)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Room, AttachedFile
from .serializers import *

@api_view(['GET'])
def room_list(request):
    rooms = Room.objects.all()
    serializer = MeetingSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def file_list(request):
    files = AttachedFile.objects.all()
    serializer = FileSerializer(files, many=True)
    return Response(serializer.data)




from datetime import timedelta, datetime
from django.http import HttpResponseRedirect, HttpResponseNotFound
from .models import File
from .forms import FileForm
import random, string



def upload_file(request, meetingId):

    return render(request, 'rooms/fileshare.html', {"meetingId":meetingId})


def uploaded_file(request):
    # Handle file upload 
    newfile = File()
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            newfile = File(file=request.FILES['file'])
            newfile.name = request.FILES['file'].name
            newfile.urlname = generate_string()
            newfile.meetingId = request.POST["meetingId"]

            dur = request.POST['duration']
            d = get_duration(dur) # returns the correct duration as a timedelta
            newfile.duration = d
            newfile.expires_at = newfile.uploaded_at + d

            newfile.save()

            # Redirect to the file list after POST
            #return HttpResponseRedirect(reverse('upload'))
    else:
        form = FileForm()  # A empty, unbound form

    return render(request, 
        'rooms/yourfile.html',
       {'file': newfile, 'form': form, 'download_url': newfile.urlname, 'meetingId': request.POST["meetingId"]}
    )

def get_duration(dur):
    durations = {
        '5m' : timedelta(minutes=5),
        '1h' : timedelta(hours=1),
        '6h' : timedelta(hours=6),
        '24h' : timedelta(days=1),
        '3d' : timedelta(days=3)
    }

    for d in durations:
        if d == dur:
            return durations[d]
    return timedelta()

def generate_string():
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(10))

def serve_download_page(request, urltext):

    file_to_download = File.objects.get(urlname=urltext)

    if file_to_download != None:
        return render(request, 'rooms/download.html', {'download' : file_to_download})
    else:
        return HttpResponseNotFound('Nothing here soz')

from django.utils import timezone
def downloads_page(request, meetingId):
    files_to_download = File.objects.filter(meetingId = meetingId)
    for file in files_to_download:
        print("Time Now:",timezone.now(), " \tExpires at:",file.expires_at)
        if timezone.now() >= file.expires_at:
            file.delete()

    files_to_download = File.objects.filter(meetingId = meetingId)
    if files_to_download:
        return render(request, 'rooms/downloads.html', {'downloads' : files_to_download})
    else:
        return render(request, 'rooms/downloads.html', {})
        # return HttpResponseNotFound('No files here')
    

from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from .models import Order



from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


# # authorize razorpay client with API Keys.
# razorpay_client = razorpay.Client(
# 	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@login_required
def initiate_payment(request):
    name = request.user.username
    
    # print("CALLBACK URL::",str(request.get_host) + "/callback/")    
    existing_order = Order.objects.filter(name=name).first()
    if existing_order:
        context = {"existing_order":existing_order.plan, "status":existing_order.status}
    else:
        provider_order_id = "NA"
        payment_id = "NA"
        signature_id = "NA"
        amount = 0
        plan = "free"
        
        # Create a new order
        order = Order.objects.create(
        name=name, amount = amount,  provider_order_id=provider_order_id, plan = plan, payment_id = payment_id, signature_id =signature_id
        )
        order.save()
        context = {}
    if request.method == "GET":
        return render(request, 'rooms/pricing.html', context)
    # try:
    if request.method == "POST":
        plan = request.POST['plan']
        print("PLAN IS", plan)
        if plan=="free":
            amount = 0
        elif plan=="pro":
            amount = 39
        elif plan == "enterprise":
            amount = 89
        else:
            amount = 0

        if plan=="pro" or plan=="enterprise":
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            order_currency = 'INR'
            order_receipt = 'order_rcptid_11'
            notes = {'Shipping address': 'Bommanahalli, Bangalore'} #OPTIONAL
            razorpay_order = client.order.create(
                { 'amount' : int(amount*82.39)*100, 'currency' : order_currency, 'receipt' : order_receipt, 'payment_capture' : '1'}
            )

            if existing_order:
                # Update the existing order
                existing_order.amount = amount  # Update the necessary fields
                existing_order.provider_order_id = razorpay_order["id"]  # Update the necessary fields
                existing_order.plan = plan  # Update the necessary fields

                existing_order.save()
                order = existing_order
            else:
                # Create a new order
                order = Order.objects.create(
                    name=name, amount = amount, provider_order_id=razorpay_order["id"], plan = plan
                )
                order.save()
            return render(
                request,
                "rooms/payment.html",
                {
                    "callback_url":   "https://meet.overtideasandsolutions.in:8000" + "/callback/",
                    "razorpay_key": settings.RAZORPAY_KEY_ID,
                    "order": order,
                },
            )
        else:
               
            provider_order_id = "NA"
            payment_id = "NA"
            signature_id = "NA"
            if existing_order:
                # Update the existing order
                existing_order.amount = amount  # Update the necessary fields
                existing_order.provider_order_id = provider_order_id  # Update the necessary fields
                existing_order.plan = plan  # Update the necessary fields
                existing_order.payment_id = payment_id
                existing_order.signature_id = signature_id
                existing_order.save()
            else:
                # Create a new order
                order = Order.objects.create(
                name=name, amount = amount,  provider_order_id=provider_order_id, plan = plan, payment_id = payment_id, signature_id =signature_id
                )
                order.save()
            
            return redirect('user_detail_view', request.user.id)
    
    # except:
    # return render(request, 'rooms/pricing.html', context={'error': 'Wrong Accound Details or amount'})

    

from .models import PaymentStatus
import json

@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)
    print(request.POST)
    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if not verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            return render(request, "rooms/callback.html", context={"status": order.status})
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, "rooms/callback.html", context={"status": order.status})
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "rooms/callback.html", context={"status": order.status})
    



def show_plans(request):
    
    if request.method == "GET":
        return render(request, 'rooms/anon_pricing.html', {})
    # try:
    if request.method == "POST":
        return redirect('login_as')
    
def contact(request):
    return render(request, 'rooms/contact.html', {})


    
def index_view(request):
    return render(request, 'rooms/index.html', {})


def terms_view(request):
    return render(request, 'rooms/terms.html', {})

def remote_session_view(request):
    return render(request, 'rooms/remote_session.html', {})

import os
@login_required
def recordings_view(request):
    path = settings.MEDIA_ROOT
    myfolders = os.path.join(path, 'recordings')
    print(myfolders)
    context = {}
    foldernames= os.listdir(myfolders)
    print(foldernames)
    context["bot"] = False
    x = 0
    d = {}
    for foldername in foldernames: # loop through all the files and folders
        filepath = os.path.join(myfolders,foldername)
        os.chdir(filepath)
        print(filepath)
        username = str(foldername).split("_")[0]

        
        order = Order.objects.filter(name=username).first()
        if request.user.username == username and order.plan == "enterprise":
            context["bot"] = True
            for file in os.listdir('.'):
                name = str(file).split("_",1)
                d[x] = {
                    "name" : name[1].split(".",1)[1],
                    "date": name[1].split(".")[0],
                    "meetingId": name[0],
                    "filepath": settings.MEDIA_URL + 'recordings/' + foldername + "/" + file,
                }
                
                x = x + 1
        # if os.path.isdir(os.path.join(os.path.abspath("."), filename)): # check whether the current object is a folder or not
            

    print(d)
    context["recordings"]=d
    return render(request, 'rooms/recordings.html', context)

def stt_view(request):
    return render(request, 'rooms/stt.html', {})

from . import summaryAI

@csrf_exempt
@api_view(['GET'])
def summary_view(request, meetingId):
#     summary = summaryAI.summarize()
    room_id = Room.objects.filter(code=meetingId)[0]
    summaries = TranscriptsAndSummaries.objects.filter(room_id=room_id)
    print("SUMMARY:", summaries)
    if len(summaries)!=0:
        data = serialize('json', summaries)
    else:
        data = ''
    # print(data)
    return JsonResponse({'summaries': data}, safe=False)
    # return render(request, 'rooms/summary.html', {'meetingId':meetingId,
    #                                               "summary":summary})

# List to store transcripts
transcripts = [] # Not work for different meetings happening at the same time
real_time_transcripts = {} # Not work for different meetings happening at the same time
# const csrftoken = getCookie('csrftoken'); // Implement a function to get the CSRF token

# fetch('http://your-django-server/your-endpoint/', {
#     method: 'POST',
#     headers: {
#         'Content-Type': 'application/json',
#         'X-CSRFToken': csrftoken,
#     },
#     // body: JSON.stringify(data) // Include this line if using POST with a request body
# })
@csrf_exempt
@api_view(['POST'])
def clean_transcript(request):
    global transcripts
    #reinitiallized
    transcripts = []
    return JsonResponse({"message": "Transcript cleared successfully"})



@csrf_exempt
@api_view(['POST'])
def receive_transcript(request):
    data = json.loads(request.body.decode('utf-8'))
    if 'username' not in data or 'transcription' not in data or 'timestamp' not in data:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    username = data['username']
    transcription = data['transcription']
    timestamp = data['timestamp']
    # Store the received transcript
    transcripts.append({"username": username, "transcription": transcription, "timestamp": timestamp})
    # Sort the transcripts based on timestamps
    transcripts.sort(key=lambda x: datetime.fromisoformat(x['timestamp']))
    

    return JsonResponse({"message": "Transcript received successfully"})
    # return JsonResponse({username: transcription})

@csrf_exempt
@api_view(['POST'])
def stop_transcripts(request):
    # Save transcripts to a file, database, or perform any desired action
    # Get the JSON data from the request
    data = json.loads(request.body)

    # Access the 'roomId' variable from the data
    room_id = data.get('roomId', None)

    if room_id is not None:
        save_transcripts_to_file(request, room_id)
        return JsonResponse({"message": "Transcripts stopped and saved successfully"})
    else:
        return JsonResponse({'error': 'Invalid data. Missing roomId.'}, status=400)
            
    
@csrf_exempt
@api_view(['POST'])
def send_realtime_transcripts(request):
    global real_time_transcripts
    data = json.loads(request.body.decode('utf-8'))
    if 'username' not in data or 'transcription' not in data or 'timestamp' not in data:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    username = data['username']
    transcription = data['transcription']
    timestamp = data['timestamp']
    # Store the received transcript
    # real_time_transcripts.append({"username": username, "transcription": transcription, "timestamp": timestamp})
    real_time_transcripts[username] = { "transcription": transcription, "timestamp": timestamp}
    # Sort the transcripts based on timestamps
    
    # sorted_real_transcripts = sorted(real_time_transcripts, key=lambda x: datetime.fromisoformat(x['timestamp']))
    sorted_real_transcripts = dict(sorted(real_time_transcripts.items(), key=lambda x: x[1]["timestamp"]))
    # print("SORTED:",sorted_real_transcripts)
    # Group transcripts by username
    # combined_transcripts = {}
    # for entry in sorted_real_transcripts:
    #     username = entry.get("username")
    #     transcription = entry.get("transcription")

    #     if username and transcription:
    #         if username not in combined_transcripts:
    #             combined_transcripts[username] = []

    #         combined_transcripts[username].append(transcription)

    # Format the transcripts into user conversation
    combined_formatted_data = ""
    for username, data in sorted_real_transcripts.items():
        combined_formatted_data += f"{username}: {data['transcription']} </br>"

    # real_time_transcripts = []
    return JsonResponse({'text':combined_formatted_data})



@csrf_exempt
def save_transcripts_to_file(request, room_id):
    # For simplicity, this example saves transcripts to a file
    filename = f"transcripts_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    with open(filename, 'w') as json_file:
        json.dump(transcripts, json_file, indent=4)
    
        
    formatted_result = sort_and_format_transcripts(filename) ### Put transcripts in nice string format
    text = summaryAI.summarize(formatted_result) 
    with open(f"summary_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt",'w') as f:
        f.write(str(text))

    
    print("ROOM CODE:", room_id)
    json_instance = TranscriptsAndSummaries(room=Room.objects.filter(code=room_id)[0], uploaded_on=timezone.now(), transcript=transcripts,summary=str(text))
    json_instance.save()
    print("Transcription and Summary Saved!")

import json
from datetime import datetime


def sort_and_format_transcripts(filename):
    # Sort transcripts based on timestamps
    try:
        with open(filename, 'r') as json_file:
            transcripts = json.load(json_file)
        sorted_transcripts = sorted(transcripts, key=lambda x: datetime.fromisoformat(x['timestamp']))

        # Group transcripts by username
        user_transcripts = {}
        for entry in sorted_transcripts:
            username = entry.get("username")
            transcription = entry.get("transcription")

            if username and transcription:
                if username not in user_transcripts:
                    user_transcripts[username] = []

                user_transcripts[username].append(transcription)

        # Format the transcripts into user conversation
        formatted_conversation = ""
        for username, transcripts_list in user_transcripts.items():
            formatted_conversation += f"{username}: {' '.join(transcripts_list)} "

        return formatted_conversation
    except:
        return "FILE ERROR"



@api_view(['POST'])
def get_summary_from_db(request, room_id):
    # Get the room object or return a 404 if it doesn't exist
    # room = get_object_or_404(Room, id=room_id)
    room = Room.objects.filter(code=room_id)[0]

    # Query all transcripts and summaries for the given room
    transcripts_and_summaries = TranscriptsAndSummaries.objects.filter(room=room)

    # You can pass the data to a template or return a JsonResponse
    # Example using a template:
    context = {
        'room': room,
        'transcripts_and_summaries': transcripts_and_summaries,
    }
    return render(request, 'your_template.html', context)

    # Example using JsonResponse:
    # data = [{'transcript': item.transcript, 'summary': item.summary} for item in transcripts_and_summaries]
    # return JsonResponse(data, safe=False)





@csrf_exempt
@api_view(['POST'])
def update_usersystem_data(request, room_code):
    data = json.loads(request.body)

    current_user = get_user(request) 
    # json_instance = UserDeviceData(room=Room.objects.filter(code=room_code)[0], user=current_user, updated_on=timezone.now(), devices=data["devices"],tracker=data["trackingInfo"])
    # Update or create UserDeviceData
    user_device_data, created = UserDeviceData.objects.get_or_create(
        room=Room.objects.filter(code=room_code)[0],
        user=current_user,
        defaults={
            'updated_on': timezone.now(),
            'devices': data["devices"],
            'tracker': data["trackingInfo"],
            # Add other fields as needed
        }
    )

    if not created:
        # Update the existing record
        user_device_data.updated_on = timezone.now()
        user_device_data.devices = data["devices"]
        user_device_data.tracker = data["trackingInfo"]
        # Update other fields as needed
        # user_device_data.save()

        user_device_data.save()
    # Update user data in the database (replace this with your actual update logic)

    return JsonResponse({'status': 'success'})

from django.urls import resolve
@csrf_exempt
@api_view(['GET'])
def get_otherusersystem_data(request, room_code):
    # Get the path from the request

    room = Room.objects.filter(code=room_code)[0]
    # moderator = HomieChatUser.objects.get(email=moderator).username
    # Query all transcripts and summaries for the given room
    # Assuming my_queryset is your QuerySet
    # Get the meeting started time for the room
    meeting_started_at = room.created_at
    

    # Construct the queryset for UserDeviceData
    users_data = UserDeviceData.objects.filter(
        room=room,
        updated_on__gt=meeting_started_at  # Add this filter condition
    )

    # print(meeting_started_at, users_data)
    # users_data = UserDeviceData.objects.filter(room=room)
    data_dict = {}
    # users_data = list(users_data.values())
    
    for user_data in users_data:
        # print(user_data)
        # Assuming username is a field in your UserDeviceData model
        username = HomieChatUser.objects.get(id=user_data.user_id).username

        data_dict[username] = {
            'devices': {
                'audio': user_data.devices['audio'],
                'video': user_data.devices['video'],
                'display': user_data.devices['display'],
            },
            'id': user_data.id,
            'room_id': user_data.room_id,
            'tracker': {
                'awayTimes': user_data.tracker['awayTimes'],
                'awayMinutes': user_data.tracker['awayMinutes'],
                'awaySeconds': user_data.tracker['awaySeconds'],
                'inactivityTimes': user_data.tracker['inactivityTimes'],
                'mouseOutMinutes': user_data.tracker['mouseOutMinutes'],
                'mouseOutSeconds': user_data.tracker['mouseOutSeconds'],
                # Add other fields as needed
            },
            'updated_on': user_data.updated_on,
            'user_id': user_data.user_id,
        }

    # print(data_dict)
    return JsonResponse({'usersData': data_dict})

    # return JsonResponse({'usersData':data_list})
