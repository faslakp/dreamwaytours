from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save





class BaseModel(models.Model):

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

class UserProfile(BaseModel):

    user=models.OneToOneField(User,on_delete=models.CASCADE)

    address=models.TextField()

    phone_number=models.CharField(max_length=20)

    profile_picture=models.ImageField(upload_to='profile-pic',blank=True,null=True)

    
    
    def __str__(self):
        return self.user
    


class TourPackage(BaseModel):

    package_name=models.CharField(max_length=200)

    description=models.TextField()

    price=models.IntegerField()

    start_date=models.DateTimeField()

    end_date=models.DateTimeField()

    destination=models.CharField(max_length=200)

    available_slots=models.IntegerField()

    image=models.ImageField(upload_to='tour-image',null=True,blank=True)

    imagetwo=models.ImageField(upload_to='tour-imagetwo',null=True,blank=True)



    


    def __str__(self):
        return self.package_name
    


class Booking(BaseModel):

    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_booking")

    tour_package=models.ForeignKey(TourPackage,on_delete=models.CASCADE,related_name="tour_booking")

    booking_date=models.DateTimeField(auto_now=True)

    number_of_people=models.IntegerField()

     
    @property
    def total_price(self):
        return self.tour_package.price*self.number_of_people
   

    def __str__(self):
        return str(self.tour_package)
    


class BookingConfirmation(BaseModel):

    tour_object=models.ForeignKey(TourPackage,on_delete=models.CASCADE,related_name="tour_confirm")

    booking_id=models.CharField(max_length=200,null=True)

    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_confirm")

     

class Review(BaseModel):

    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_review")

    tour=models.ForeignKey(TourPackage,on_delete=models.CASCADE,related_name="tour_review")

    rating=models.PositiveIntegerField()

    comment=models.TextField(blank=True,null=True)



    def __str__(self):
        return self.rating



def create_userprofile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(create_userprofile,sender=User)