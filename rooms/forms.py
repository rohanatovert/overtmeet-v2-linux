from django import forms

from .models import HomieChatUser, Room, AttachedFile

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.contrib.auth import authenticate
from string import Template
from django.utils.safestring import mark_safe
from django.forms import ImageField
from django.template import loader
from django.core.exceptions import ValidationError
from django.utils import timezone

# class ImagePreviewWidget(forms.widgets.Widget):

#     template_name = 'rooms/user_update_view.html'

#     def get_context(self, name, value, attrs=None):

#         return {'widget': {
#             'name': name,
#             'value': '/media/' + value,
#         }}

#     def render(self, name, value, attrs=None, renderer = None):
#         context = self.get_context(name, value, attrs)
#         template = loader.get_template(self.template_name).render(context)
#         return mark_safe(template)

class HomieChatUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address.') 
    # bio = forms.CharField(max_length=60, widget=forms.Textarea, help_text='Type something about yourself.', required=False)
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        icons = getattr(self.Meta, 'icons', dict())
        for field_name, field in self.fields.items():
            if field_name in icons:
                field.icon = icons[field_name]
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class']='form-control'

    class Meta:
        model = HomieChatUser
        
        fields = [
            'email',
            'username',
            'password1',
            'password2',
            'image',
        ]
        icons = {'username': 'user',
                 'email': 'envelope',
                 'password1': 'lock',
                 'password2': 'key',
                 'image': 'user-circle'
                 }
        # error_messages = {
        #     'username': {
        #         'unique': 'This mail id is already registered with a user.'
        #     },
        #     'email': {
        #         'unique': 'This username is already taken.'
        #     }
        # }
        
        

class UserAuthenticationForm(forms.Form):
    email = forms.EmailField(label='Email',  required = True, widget=forms.EmailInput(attrs={'class': "form-control"}))
    email.widget.attrs['required'] = 'required'
    password = forms.CharField(label='Password', required = True, widget=forms.PasswordInput(attrs={'class': "form-control"}))
    password.widget.attrs['required'] = 'required'

    class Meta:
        model = HomieChatUser
        fields = (
            'email',
            'password',
        )

    def clean(self):
        # email = self.cleaned_data.get('email', None)
        # password = self.cleaned_data.get('password', None) 
        cleaned_data = super(UserAuthenticationForm, self).clean()

        email = self.cleaned_data.get('email', None)
        password = self.cleaned_data.get('password', None) 
        
        print("Auth is:",authenticate(email=email, password=password))
        if not HomieChatUser.objects.filter(email__iexact=email).exists():
            msg = ("There is no user registered with the specified E-Mail address.")
            # self.add_error('email', msg)
            raise forms.ValidationError(msg)

        if not authenticate(email=email, password=password):
            raise forms.ValidationError('Invalid login.')
      
        return cleaned_data


class HomieChatUserUpdateForm(forms.ModelForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address.')
    image = forms.ImageField(widget= forms.FileInput)
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        icons = getattr(self.Meta, 'icons', dict())
        for field_name, field in self.fields.items():
            if field_name in icons:
                field.icon = icons[field_name]
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class']='form-control'
    # bio = forms.CharField(max_length=60, widget=forms.Textarea, help_text='Type something about yourself.', required=False)
    # image = forms.ImageField(widget=ImagePreviewWidget,)
    class Meta:
        model = HomieChatUser
        fields = (
            'email',
            'username',
            'image',
        )
        icons = {'username': 'user',
                 'email': 'envelope',
                 'image': 'user-circle'
                 }
        # error_messages = {
        #     'username': {
        #         'unique': 'This mail id is already registered with a user.'
        #     },
        #     'email': {
        #         'unique': 'This username is already taken.'
        #     }
        # }

class RoomCreationForm(forms.ModelForm):
    name = forms.CharField(max_length=40, required=True)
    class Meta:
        model = Room
        fields = (
            'name',
        )

    def clean(self):
        cleaned_data = super(RoomCreationForm, self).clean()
        # Check if the user has already created 5 rooms on the current day
        # if Room.objects.filter(created_at__date=timezone.now().date()).count() > 5:
        #     raise ValidationError("You can only create up to 5 rooms per day.")
        return cleaned_data



class UploadFileForm(forms.ModelForm):
    class Meta:
        model = AttachedFile
        fields = '__all__'




class FileForm(forms.Form):
    file = forms.FileField(label='Select a file :)')


