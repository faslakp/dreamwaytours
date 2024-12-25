from django import forms

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm
 
from tours.models import Booking,UserProfile

class SignupForm(UserCreationForm):

    class Meta:
        model=User
        fields=["username","email","password1","password2"]

        widget={
             "username": forms.TextInput(attrs={"class": 
            "w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" }),
            "email":forms.EmailInput(attrs=
            {"class": "w-full p-2 border-2 border-gray-300 rounded-md  focus:ring-2 focus:ring-blue-500"}),
            "password1":forms.PasswordInput(attrs=
            {"class": "w-full p-2 border-2 border-gray-300 rounded-md  focus:ring-2 focus:ring-blue-500"}),
            "password2":forms.PasswordInput(attrs=
            {"class": "w-full p-2 border-2 border-gray-300 rounded-md  focus:ring-2 focus:ring-blue-500"}),

        }



class SigninForm(forms.Form):

    username=forms.CharField()
    password=forms.CharField()



class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=["address","phone_number","profile_picture"]

        widgets = {
            "address": forms.TextInput(attrs={
                "class": "w-full p-2 border border-gray-300 rounded-md focus:outline focus:ring-2 focus:ring-blue-500"
            }),
            "phone_number": forms.NumberInput(attrs={
                "class": "w-full p-2 border border-gray-300 rounded-md focus:outline focus:ring-2 focus:ring-blue-500"
            }),
            "profile_picture": forms.ClearableFileInput(attrs={
                "class": "w-full p-2 border border-gray-300 rounded-md focus:outline focus:ring-2 focus:ring-blue-500"
            }),}




class BookingForm(forms.ModelForm):
    class Meta:
        model=Booking
        fields=["number_of_people"]
        widgets={
        "number_of_people": forms.NumberInput(attrs={"class": 
            "w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" })}


    

