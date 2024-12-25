from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.
from django.views.generic import View
from tours.forms import SignupForm,SigninForm,UserProfileEditForm,BookingForm

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from tours.models import TourPackage,UserProfile,Booking,BookingConfirmation

from django.core.paginator import Paginator
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import razorpay

RZP_KEY_ID="rzp_test_Nk0j3idyzouTa5"
RZP_KEY_SECRET="QAsp7kLslcuSxR9alwpYKEBb"



class SignupView(View):
    template_name="register.html"
    form_class=SignupForm

    def get(self,request,*args,**kwargs):
        form_instance=self.form_class()
        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):
        form_instance=self.form_class(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect("signin")
        else:
            return render(request,self.template_name,{"form":form_instance})
        

class SigninView(View):
    form_class=SigninForm
    template_name="login.html"

    def get(self,request,*args,**kwargs):
        form_instance=self.form_class()
        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):
        form_instance=self.form_class(request.POST)
        if form_instance.is_valid():
            uname=form_instance.cleaned_data.get("username")
            pword=form_instance.cleaned_data.get("password")

            user_object=authenticate(request,username=uname,password=pword)

            if user_object:
                login(request,user_object)
                return redirect("tour-list")

            else:
               
              
                return render(request,self.template_name,{"form":form_instance})
        
        return render(request,self.template_name,{"form":form_instance})
    

class UserProfileEditView(View):
    template_name="profile_edit.html"
    form_class=UserProfileEditForm

    def get(self,request,*args,**kwargs):
        user_profile_instance=UserProfile.objects.get(user=request.user)
        form_instance=self.form_class(instance=user_profile_instance)
        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):
        user_profile_instance=UserProfile.objects.get(user=request.user)
        form_instance=self.form_class(request.POST,instance=user_profile_instance,files=request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect("tour-list")
        return render(request,self.template_name,{"form":form_instance})



 

class TourListView(View):
    template_name="tour_list.htm"
    def get(self,request,*args,**kwargs):

        search_text=request.GET.get("search_text")
        if search_text !=None:
            qs=TourPackage.objects.filter(package_name__contains=search_text)
        else:
            qs=TourPackage.objects.all()
        
        # paginator_object:
        paginator=Paginator(qs,4)
        page_number=request.GET.get("page")
        page_obj=paginator.get_page(page_number)

        return render(request,self.template_name,{"page_obj":page_obj})


class TourDetailView(View):
    template_name="tour_details.html"
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=TourPackage.objects.get(id=id)
        return render(request,self.template_name,{"data":qs})
    



#class BookingView(View):
#     form_class = BookingForm
#     template_name = "booking.html"
   
#     def get(self, request, *args, **kwargs):
       
#         id = kwargs.get("pk")
#         tour_package = TourPackage.objects.get(id=id)
       
#         form_instance = self.form_class()
#         user=request.user
#         return render(request, self.template_name, {
#              "data": form_instance,
#             "tour_package": tour_package,"user":user
#         })

#     def post(self, request, *args, **kwargs):
       
#         id = kwargs.get("pk")
#         tour_package = TourPackage.objects.get(id=id)
#         user=request.user
       
#         form_instance = self.form_class(request.POST)
        
#         if form_instance.is_valid():
           
#             form_instance.instance.tour_package = tour_package
#             form_instance.instance.user = request.user  
#             form_instance.price=tour_package.price
#             form_instance.save()
#             return redirect("booking-confirm")
#         else:


#             return render(request, self.template_name, {
#                 "data": form_instance,
#                 "tour_package": tour_package,"user":user
#             })
class BookingConfirmView(View):
    form_class=BookingForm
    def get(self, request, *args, **kwargs):
        
        id = kwargs.get("pk")
        user=request.user
        tour_package = TourPackage.objects.get(id=id)
        form_instance = self.form_class()
        
        return render(request,"booking.html", {"data":form_instance,"user":user})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        number_of_people=request.POST.get("number_of_people")
        tour_package=TourPackage.objects.get(id=id)
        price=TourPackage.price
        total_price=Booking.total_price

        user=User.objects.get(username=request.user)
        Booking.objects.create(
            user=user,
            tour_package=tour_package,
            number_of_people=number_of_people,
            
        )   
    
        return redirect("booking-detail")
    









   
    

class BookingDetailsView(View):
    template_name="booking_detail.html"
    def get(self,request,*args,**kwargs):
        qs=Booking.objects.filter(user=request.user)
        return render(request,self.template_name,{"data":qs})
class BookingDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Booking.objects.get(id=id).delete()

        

        return redirect("tour-list")
    
class BookingUpdateView(View):
    template_name="booking_update.html"
    form_class=BookingForm
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        tour_package=TourPackage.objects.get(id=id)
        booking_obj=Booking.objects.get(id=id)
        
        form_instance=self.form_class(instance=tour_package)
        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        number_of_people=request.POST.get("number_of_people")
        tour_package=TourPackage.package_name
        price=TourPackage.price
        total_price=Booking.total_price

        user=User.objects.get(username=request.user)
        Booking.objects.create(
            user=user,
            tour_package=tour_package,
            number_of_people=number_of_people,
            
        )   
    
        return redirect("booking-detail")


class CheckoutView(View):

    template_name="checkout.html"
    def get(self,request,*args,**kwargs):
        RZP_KEY_ID="rzp_test_Nk0j3idyzouTa5"
        RZP_KEY_SECRET="QAsp7kLslcuSxR9alwpYKEBb"
        
        client=razorpay.Client(auth=(RZP_KEY_ID,RZP_KEY_SECRET))
        # id = kwargs.get("pk")  
        # booking_obj = get_object_or_404(Booking, id=id)  
        # tour_object = booking_obj.tour_package
       
        # total_price=tour_object.price*booking_obj.number_of_people
        booking_obj=request.user.user_booking.first()
        tour_package=booking_obj.tour_package
        total_price=booking_obj.total_price

       

        data = { "amount": total_price * 100, "currency": "INR", "receipt": "order_rcptid_dreamway" }
        payment = client.order.create(data=data)
        print(payment)
        booking_id=payment.get("id")


        BookingConfirmation.objects.create(
            booking_id=booking_id,
            user=request.user,
            tour_object=tour_package)

        return render(request,self.template_name,{
            "key_id":RZP_KEY_ID,
            "amount":total_price,
            "booking_id":booking_id})


@method_decorator(csrf_exempt,name="dispatch")
class PaymentVerificationView(View):
    def post(self,request,*args,**kwargs):
        
        print(request.POST)


        return("signin")


    
    


    
       



    






   
    

