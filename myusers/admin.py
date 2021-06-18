from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import *
# Register your models here.


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = HMUser
        fields = ('email', 'username', 'first_name', 'last_name', 'is_admin',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with contacts's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = HMUser
        fields = ('email', 'username', 'first_name', 'last_name',)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class MyUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('full_name', 'username', 'email', 'phone_number')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'username',
                                      'client', 'country', 'branch', 'unique_code', 'name_of_client', 'permission')}),
        ('Permissions', {'fields': ('is_admin',
                                    'is_active', 'is_returned', 'first_passwd')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'is_admin')}
         ),
    )
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email', 'username')
    filter_horizontal = ()

    def full_name(self, obj):
        return ("{0} {1}".format(obj.first_name.encode("utf8"), obj.last_name.encode("utf8"))).title()


admin.site.register(HMUser, MyUserAdmin)
admin.site.register(Client)
admin.site.register(EditClient)
admin.site.register(UserActivity)
