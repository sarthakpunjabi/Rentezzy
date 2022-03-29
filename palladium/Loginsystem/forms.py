'''Creating forms for displaying in frontend'''
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth import get_user_model

class RegisterForm(UserCreationForm):
    '''Creating custom Register form and overriding'''
    class Meta:
        '''obligating meta configuration and deciding model to be used'''
        model = get_user_model()
        fields = ('user_name','first_name',
        'middle_name','last_name','phone_number',
        'type','subscription',
        )


class RegisterChangeForm(UserChangeForm):
    '''Creating custom Register change form and overriding'''
    class Meta:
        '''obligating meta configuration and deciding model to be used'''
        model = get_user_model()
        fields = ('user_name','first_name','middle_name',
        'last_name','phone_number',
        'type','subscription',
        )
