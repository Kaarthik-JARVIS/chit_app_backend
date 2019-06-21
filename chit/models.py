from django.db import models,transaction
from django.conf import settings
from django.utils import timezone 
from datetime import datetime

from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
 
class UserManager(BaseUserManager):
 
    def _create_user(self, name, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not name:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(name=name, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise
 
    def create_user(self, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, password, **extra_fields)

    def create_superuser(self, name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
 
        return self._create_user(name, password=password, **extra_fields) 

class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
 
    """
    # email = models.EmailField(max_length=40, blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, unique=True)
    role = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(max_length=10,null=True) 
    #last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
 
    objects = UserManager()
 
    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['role']
 
    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

# Create your models here.
class Type(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=10, default="")
    status = models.IntegerField(default=1)
    published_date = models.DateTimeField(blank=True, null=True, default=timezone.now)

    def __str__(self):
        return self.name

class Chit(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.IntegerField()
    remarks = models.CharField(max_length=300, null=True)
    status = models.IntegerField(default=1)
    published_date = models.DateTimeField(blank=True, null=True, default=timezone.now)

    def __str__(self):
        s=str(self.amount)
        return s

class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    type_id = models.ForeignKey(Type, on_delete=models.CASCADE)
    remarks = models.CharField(max_length=300, null=True)
    chit_id = models.ForeignKey(Chit, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=datetime.now)
    status = models.IntegerField(default=1)
    published_date = models.DateTimeField(blank=True, null=True, default=timezone.now)

    def __str__(self):
        return self.name

class Members(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,unique=True)
    phone_number = models.CharField(max_length=10,null=True) 
    note = models.CharField(max_length=300, null=True)
    status = models.IntegerField(default=1)
    published_date = models.DateTimeField(blank=True, null=True, default=timezone.now)

    def __str__(self):
        return self.name

class GroupMembers(models.Model):
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    member_id = models.ForeignKey(Members, on_delete=models.CASCADE)

    published_date = models.DateTimeField(blank=True, null=True, default=timezone.now)

    def __str__(self):
        s=str(self.group_id)
        return s


# class Users(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100,unique=True)
#     phone_number = models.CharField(max_length=10,null=True) 
#     role = models.CharField(max_length=100)
#     pin = models.CharField(max_length=4)
#     status = models.IntegerField(default=1)
#     published_date = models.DateTimeField(blank=True, null=True, default=timezone.now)

#     def __str__(self):
#         return self.name+" - "+self.role

class ExpenseCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,unique=True)
    remarks = models.CharField(max_length=300,null=True)
    status = models.IntegerField(default=1)
    published_date = models.DateTimeField(blank=True, null=True, default=timezone.now)

    def __str__(self):
        return self.name

class Expense(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(blank=True, null=True, default=datetime.now)
    category_id = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        s=str(self.amount)
        return s

class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(blank=True, null=True)
    member_id = models.ForeignKey(Members, on_delete=models.CASCADE)
    amount = models.IntegerField()
    remarks = models.CharField(max_length=300,blank=True, null=True)
    payment_mode = models.CharField(max_length=50)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE)
    published_date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    
    def publish(self):
        self.date = datetime.now()
        self.save()

class Commission(models.Model):
    profit_commission = models.FloatField()
    auction_commission = models.FloatField()
    
    def __str__(self):
        s=str(self.profit_commission)
        return s
    
class GroupAuction(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(blank=True, null=True)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    member_id = models.ForeignKey(Members, on_delete=models.CASCADE)
    auction_amount = models.IntegerField(default=0)
    payable = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    remarks = models.CharField(max_length=300,blank=True, null=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE)
    published_date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    status = models.IntegerField(default=0)

    def publish(self):
        self.date = datetime.now()
        self.save()

class PayableAuction(models.Model):
    id = models.AutoField(primary_key=True)
    auction_id = models.ForeignKey(GroupAuction, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    member_id = models.ForeignKey(Members, on_delete=models.CASCADE)
    total_payable = models.IntegerField(default=0)
    paid_amount = models.IntegerField(default=0)
    payment_status = models.IntegerField(default=0)
    updated_date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    
    def publish(self):
        self.updated_date = datetime.now()
        self.save()