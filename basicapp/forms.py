from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import client

# Create your forms here.

# class NewUserForm(UserCreationForm):
# 	email = forms.EmailField(required=True)
# 	# Client_id = forms.CharField(required=True)
# 	# Secret_key = forms.CharField(required=True)

# 	class Meta:
# 		model = User
# 		fields = ("username", "email", "password1", "password2")

# 	def save(self, commit=True):
# 		user = super(NewUserForm, self).save(commit=False)
# 		user.email = self.cleaned_data['email']
# 		# user.Client_id = self.cleaned_data['Client_id']
# 		# user.Secret_key = self.cleaned_data['Secret_key']
# 		if commit:
# 			user.save()
# 		return user
	

# class AuthorForm(forms.ModelForm):
#     class Meta:
#         model = Author
#         fields = ['name', 'bio']
	
class ClientForm(forms.ModelForm):
    class Meta:
        model = client
        #fields = "__all__"s
        fields = ['Client_id', 'Secret_key','fy_id', 'app_id_type','totp_key',
                  'pin', 'app_id', 'redirect_uri', 'app_type', 'app_id_hash']
