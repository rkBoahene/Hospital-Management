from django import forms
from .models import *
from django.forms import widgets
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': "form-control", 'placeholder': "Enter email"}))
    password = forms.CharField(widget=forms.widgets.PasswordInput(
        attrs={'class': "form-control", 'placeholder': "Enter password"}))

    def clean(self):
        email = self.cleaned_data('email')
        password = self.cleaned_data('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)

            if self.user_cache is None:
                raise forms.ValidationError('invalid login')
            elif not self.user_cache.is_active:
                raise forms.ValidationError('inactive')
        return self.cleaned_data


class HMUsersForm(forms.ModelForm):

    STATUS_TYPES = (
        ('1', 'HM Admin SuperUser'),
        ('2', 'HM Administrator'),
        ('3', 'HM Auditor'),
        ('4', 'Doctor'),
        ('5', 'Pharmacy'),
        ('6', 'Finance'),
        ('7', 'Residence'),
    )

    email = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control", 'required': True, 'placeholder': "Email"}))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control", 'required': True, 'placeholder': "First Name"}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control", 'required': True, 'placeholder': "Last Name"}))
    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control", 'required': True, 'placeholder': "Phone Number"}))
    permission = forms.ChoiceField(widget=forms.Select(
        attrs={'class': "form-control", 'required': True, 'placeholder': "Permission"}), choices=STATUS_TYPES)

    class Meta:
        model = HMUser
        fields = ['email', 'first_name', 'last_name',
                  'phone_number', 'permission', ]


class ULClientForm(forms.ModelForm):
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={'class': "form-control",
                   'required': True, 'placeholder': "Email"}
        )
    )
    name_of_client = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': "form-control",
                   'required': True, 'placeholder': "Name"}
        )
    )
    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control", 'required': True, 'placeholder': "Phone Number"}))
    overdraft_limit = forms.CharField(initial=0.0,
                                      widget=forms.TextInput(
                                          attrs={'class': "form-control"}
                                      ),
                                      required=False
                                      )

    class Meta:
        model = ULUser
        fields = ['email', 'name_of_client', 'phone_number', 'overdraft_limit']


class ULClientReviewForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ['overdraft_limit', 'name', 'email',
                  'wallet_balance', 'momo', 'account_name', 'account_number', ]

    overdraft_limit = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': "form-control", 'required': True}
        )
    )
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': "form-control", 'required': True}
        )
    )
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={'class': "form-control", 'required': True}
        )
    )

    hospital_name = forms.CharField(required=False,
                                    widget=forms.TextInput(
                                        attrs={'class': "form-control"}
                                    )
                                    )
    hospital_branch = forms.CharField(required=False,
                                      widget=forms.TextInput(
                                          attrs={'class': "form-control"}
                                      )
                                      )


class ClientEditForm(forms.ModelForm):

    class Meta:
        model = EditClient
        fields = ['name', 'hospital_name', 'hospital_branch']

        name = forms.CharField(

            widget=forms.TextInput(
                attrs={'class': "form-control", 'required': True}
            )
        )

        hospital_name = forms.CharField(required=False,
                                        widget=forms.TextInput(
                                            attrs={'class': "form-control"}
                                        )
                                        )
        hospital_branch = forms.CharField(required=False,
                                          widget=forms.TextInput(
                                              attrs={'class': "form-control"}
                                          )
                                          )


class ClientReviewEditForm(forms.ModelForm):

    class Meta:
        model = EditClient
        fields = ['name', 'hospital_name', 'hospital_branch']

    name = forms.CharField(

        widget=forms.TextInput(
            attrs={'class': "form-control", 'required': True}
        )
    )

    hospital_name = forms.CharField(required=False,
                                    widget=forms.TextInput(
                                        attrs={'class': "form-control"}
                                    )
                                    )
    hospital_branch = forms.CharField(required=False,
                                      widget=forms.TextInput(
                                          attrs={'class': "form-control"}
                                      )
                                      )
