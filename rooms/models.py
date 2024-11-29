from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.templatetags.static import static
from django.utils import timezone
from django.core.exceptions import ValidationError
# Create your models here.

# Pass these as two-tuple values
# in GENDER_CHOICES
MALE_NUMBER = 1
FEMALE_NUMBER = 2
MALE = 'Male'
FEMALE = 'Female'

GENDER_CHOICES = [
    (MALE_NUMBER, MALE),
    (FEMALE_NUMBER, FEMALE),
]

class MyAccountManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a username;)")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(self, using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user=self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )


        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)





class HomieChatUser(AbstractBaseUser):
    # required to include
    email = models.EmailField(verbose_name='email', unique=True, max_length=60, error_messages={'required': 'Please let us know your email id!', "unique": ("A user with this email already exists."),})
    username = models.CharField(max_length=60, unique=True, error_messages={'required': 'Please let us know what to call you!', "unique": ("This username is already taken."),})
    date_joined = models.DateField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # new
    # name = models.CharField(max_length=60, verbose_name='name')
    # bio = models.CharField(max_length=60, verbose_name='bio', null=True, blank=True, default=None)
    image = models.ImageField(upload_to='user_images', null=True, blank=True)
    # gender = models.SmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            # if self.gender == FEMALE_NUMBER:
            #     url = static('images/default_female_picture.png')
            # elif self.gender == MALE_NUMBER:
            #     url = static('images/default_male_picture.png')
            # else:
                url = static('images/default_profile_picture.png')

        return url

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name_plural = "Homie Chat Users"

from django.db import models

class AttachedFile(models.Model):
    file = models.FileField(upload_to='files/')  # This assumes you want to store the files in the 'files/' directory within your media storage
    # You can add other fields to the AttachedFile model as needed


class UserProfileModel(models.Model):
    user = models.OneToOneField(to=HomieChatUser, on_delete=models.CASCADE)
    name = models.CharField(blank=True, null = True, max_length= 100)
    online_status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username


class Room(models.Model):
    # code generated using signer
    # will be trimmed to get a unique code
    # of length 43
    code = models.CharField(max_length=44, unique=True)
    name = models.CharField(max_length=40, null=True, blank=True, default=None)
    user = models.ForeignKey(to=HomieChatUser, on_delete=models.CASCADE)
    file = models.ManyToManyField(AttachedFile, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def save(self, *args, **kwargs):
        # Ensure the created_at field only gets its default value
        if not self.pk:
            self.created_at = timezone.now()
       
        super(Room, self).save(*args, **kwargs)


class Video(models.Model):
    video_file = models.FileField(upload_to='room_videos')
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)

    @property
    def video_url(self):
        url = self.video_file.url

        return url


from datetime import timedelta
from django.utils import timezone

class File(models.Model):

    name = models.CharField(max_length=500)

    uploaded_at = models.DateTimeField(default=timezone.now)

    duration = models.DurationField(default=timedelta())

    expires_at = models.DateTimeField(default=timezone.now() + timedelta(minutes=5))

    urlname = models.CharField(max_length=10, unique=True)
    file = models.FileField(upload_to='files')
    meetingId = models.CharField(max_length=500)
    # room = models.ForeignKey(to=Room, on_delete=models.CASCADE)

    def file_link(self):
      if self.file:
        return "<a href='%s'> Download </a>" % (self.file.url)
      else:
        return "No attatchement"

    file_link.allow_tags = True


class PaymentStatus:
    SUCCESS = "Success"
    FAILURE = "Failure"
    PENDING = "Pending"

class Order(models.Model):
    name =  models.CharField(("Customer Name"), max_length=254, blank=False, null=False)
    amount = models.FloatField(("Amount"), null=False, blank=False)
    plan = models.CharField(("Plan"), max_length=254, blank=False, null=True)
    status =  models.CharField(
        ("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField(
        ("Order ID"), max_length=40, null=False, blank=False
    )
    payment_id = models.CharField(
        ("Payment ID"), max_length=36, null=False, blank=False
    )
    signature_id = models.CharField(
        ("Signature ID"), max_length=128, null=False, blank=False
    )

    def __str__(self):
        return f"{self.id}-{self.name}-{self.status}"

class CallModel(models.Model):
    sender = models.ForeignKey(to=HomieChatUser, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank = True)
    thread_name = models.CharField(null=True, blank = True, max_length=50)
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self) -> str:
        return self.message
    
class CallNotifications(models.Model):
    chat = models.ForeignKey(to=CallModel, on_delete=models.CASCADE)
    user = models.ForeignKey(to=HomieChatUser, on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username
    

class TranscriptsAndSummaries(models.Model):
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    uploaded_on = models.DateTimeField(default=timezone.now)
    # expires_at = models.DateTimeField(default=timezone.now() + timedelta(minutes=5))
    transcript = models.JSONField(default="No Transcript Available")
    summary = models.TextField(default="No Summary Available")
    
    # room = models.ForeignKey(
    def __str__(self) -> str:
        return self.summary
    

class UserDeviceData(models.Model):
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    user = models.ForeignKey(to=HomieChatUser, on_delete=models.CASCADE)
    updated_on = models.DateTimeField(default=timezone.now)
    # expires_at = models.DateTimeField(default=timezone.now() + timedelta(minutes=5))
    devices = models.JSONField(default="No Data Available")
    tracker = models.JSONField(default="No Data Available")
    
   
    def __str__(self) -> str:
        return str(self.devices)

    