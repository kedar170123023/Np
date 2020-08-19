from    django.contrib.auth.forms   import UserCreationForm
from    django.contrib.auth.models  import User
from    django                      import forms
from    .models                     import (CHESS, MTSE, PR, FHS, CC, RANGOTSAV, Profile)
from    django.utils.translation    import gettext, gettext_lazy as _
from    .models                     import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title', 'description', 'document')

# *************
# User Signup Form
# *************
class SignUpForm(forms.ModelForm):
    first_name = forms.CharField(max_length = 20,required = True)
    last_name = forms.CharField(max_length = 20,required = True)


    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        min_length = 8,
        widget=forms.PasswordInput,
        help_text = 'minimum 8 characters are required ',
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    email  = forms.EmailField(
        required=True,
        help_text="Enter the corrrect Email\n",
    )
    class Meta:
        model = User
        fields = ( 'first_name', 'last_name', 'email', 'password1', 'password2',)


# *************
# Profile Signup Form
# *************
class SignUpFormProfile(forms.ModelForm):
    birth_date = forms.DateTimeField(
        help_text=_("year-month-day"),
        widget=forms.DateTimeInput(attrs={'placeholder': 'yyyy-mm-dd'},),
        )
    class Meta:
        model = Profile
        fields = ( 'birth_date', 'gender', )


#    user upadate form and profile update form 
# 
#  


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


class UserDetailsForm(forms.ModelForm):
    class Meta:
        fields = ('mother_name', 'father_name', 'gender', 'birth_date', 'contact')
        model = Profile

class EducationForm(forms.ModelForm):
    class Meta:
        fields = ('school' , 'class_study')
        model = Profile

class AddressForm(forms.ModelForm):
    class Meta:
        fields = ('landmark', 'addess', 'ditrict', 'pin', 'house_number',)
        model = Profile

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ( 'first_name', 'last_name', 'email',)


# *************
# Free hand sketching Form
# *************
class FHS_form(forms.ModelForm):
    class Meta:
        model = FHS
        fields = '__all__'

# *************
# Rangotsav Form
# *************
class RANGOTSAV_form(forms.ModelForm):
    class Meta:
        model = RANGOTSAV
        fields = '__all__'

# ****************
# Puzzle Race Form
# ****************
class PR_form(forms.ModelForm):
    class Meta:
        model = PR
        widgets = {'user2WithDetails': forms.HiddenInput(),
                    'user3WithDetails': forms.HiddenInput(),
                    'userInput' : forms.HiddenInput(),
                }
        fields = '__all__'
        exclude = ('user', 'success', )



# *************
# MTSE Form
# *************
class MTSE_form(forms.ModelForm):
    class Meta:
        model = MTSE
        fields = '__all__'

# Career Counselling
class CC_form(forms.ModelForm):
    class Meta:
        model = CC
        fields = '__all__'
# *************
# Chess Competition Form
# *************
class CHESS_form(forms.ModelForm):
    class Meta:
        model = CHESS
        fields = '__all__'


    


   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
    # class ArticleForm(forms.ModelForm):
    # headline = MyFormField(
    #     max_length=200,
    #     required=False,
    #     help_text='Use puns liberally',
    # )

    # class Meta:
    #     model = Article
    #     fields = ['headline', 'content']
