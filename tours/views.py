from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from tours.forms import SignupForm



class SignupView(View):
    template_name="register.html"
    form_class=SignupForm

    def get(self,request,*args,**kwargs):
        form_instance=self.form_class()
        return render(request,self.template_name,{"form":form_instance})
