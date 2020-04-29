from    django.db                           import models
from    django.contrib.auth.models          import User
from    django.dispatch                     import receiver
from    django.db.models.signals            import post_save
from    django.core.validators              import MaxValueValidator, MinValueValidator
from    .dictUtils                          import (ADFP, CHOICES)
import  datetime

# user        = models.ForeignKey(User, on_delete=models.CASCADE)
# transaction     = models.ForeignKey(Transaction, on_delete=models.CASCADE)

class Transaction(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    amount          = models.DecimalField(max_digits=8, decimal_places=2)
    tid             = models.CharField(max_length=12, unique=True)
    success         = models.BooleanField(default=False)
    date            = models.DateTimeField(auto_now_add=True)
    trn_type        = models.CharField(max_length=20)
    remarks         = models.CharField(max_length=50, default="NA")

    

class UserDetails(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    mother_name     = models.CharField(verbose_name="Mother Name",max_length=50, blank=True, null=True)
    father_name     = models.CharField(verbose_name="Father Name",max_length=50, blank=True, null=True)
    gender          = models.CharField(verbose_name="Gender", default = 'Male', max_length=50, blank=True, null=False,choices = CHOICES['GENDER'])
    birth_date      = models.DateField(("Date of birth"),null = False,blank = False, default=datetime.date.today)
    contact         = models.PositiveIntegerField(verbose_name="Contact",validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)] , blank=False,null = True)
    class Meta:
        abstract = True

class Education(models.Model):
    class_study     = models.PositiveIntegerField(verbose_name="Class Study",default=5, null=True, validators=[MinValueValidator(4), MaxValueValidator(10)])
    school          = models.CharField(max_length=50)
    class Meta:
        abstract = True

class Address(models.Model):
    landmark        = models.CharField(verbose_name="Landmark", max_length=50, blank=True, null=True)
    addess          = models.CharField(verbose_name="Address", max_length=100, blank=True, null=True)
    ditrict         = models.CharField(verbose_name="District",max_length=50, blank=True, null=True)
    pin             = models.PositiveIntegerField(verbose_name="Pin",validators=[MinValueValidator(100000), MaxValueValidator(999999)], blank=True, null=True)
    house_number    = models.CharField(verbose_name="Home Number",max_length=10, blank=True, null=True)
    class Meta:
        abstract = True
    
class PrUser(UserDetails, Education, Address):
    pass

class RangotsavUser(UserDetails, Address):
    pass



class PR(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE,)
    user2WithDetails= models.OneToOneField(PrUser, on_delete=models.CASCADE, related_name='+', related_query_name='+')
    user3WithDetails= models.OneToOneField(PrUser, on_delete=models.CASCADE)
    # 1 - Details
    # 0 - Id
    # N - Not Taken
    # 11 - user2 user3 both taken with details
    userInput       = models.CharField(max_length=2, default="11")
    category        = models.CharField(verbose_name="Category", default="VII/VIII" ,choices=CHOICES['P_CATEGORY'], max_length=12, blank=False)
    # False : Incomplte - Filled but not paid
    # True  : Complete
    # when object is created then it is set False that is form is filled but yet to be paid
    # Free forms need not to be paid, once filled is successful
    success         = models.BooleanField(default=False)

class RANGOTSAV (models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE,)
    user2WithDetails= models.OneToOneField(RangotsavUser, on_delete=models.CASCADE, related_name='+', related_query_name='+')
    user3WithDetails= models.OneToOneField(RangotsavUser, on_delete=models.CASCADE)
    # 1 - Details
    # 0 - Id
    # N - Not Taken
    # 11 - user2 user3 both taken with details
    userInput       = models.CharField(max_length=2, default="11")
    category        = models.CharField(verbose_name="Category",choices=CHOICES['R_CATEGORY'], max_length=12, blank=False)


class MTSE (models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    qpl             = models.CharField(max_length = 9, choices = CHOICES['QPL'],blank = False, null = False,verbose_name = 'Paper langauge')
    success         = models.BooleanField(default=False)

class FHS (models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    success         = models.BooleanField(default=False)
    category        = models.CharField(verbose_name="Category",choices=CHOICES['F_CATEGORY'], max_length=12, blank=False)


class CC (models.Model):
    user            = models.OneToOneField(User, on_delete     = models.CASCADE,)
    category        = models.CharField(verbose_name="Category",choices=CHOICES['CC_CATEGORY'], max_length=12, blank=False)


class CHESS (models.Model):
    user            = models.OneToOneField(User, on_delete = models.CASCADE,)
    category        = models.CharField(verbose_name="Category",choices=CHOICES['C_CATEGORY'], max_length=12, blank=False)
    success         = models.BooleanField(default=False)

# ------------------------------------------------------------------------------------------------
class Profile (UserDetails, Education, Address):
    completeProfile = models.BooleanField(default=False)
    allowEdit       = models.CharField(max_length=3, default="000")
    blocked         = models.BooleanField(default=False)


    # def __str__(self):
    #     return f'{self.user.first_name}'

#   --------------------------------------------------------------------------------------------------------------  # 

def create_profile(sender, **kwargs):
    if(kwargs["created"]):
        user_profile = Profile.objects.create(user = kwargs["instance"])

post_save.connect(create_profile,sender=User)



#   --------------------------------------------------------------------------------------------------------------  # 

class Document  (models.Model):
    uploader    = models.ForeignKey(User,on_delete = models.SET_NULL, null = True)
    title       = models.CharField(max_length = 40, blank = False, null = False)
    description = models.CharField(max_length=255, blank=True)
    document    = models.FileField(upload_to='media/navprayas/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)






