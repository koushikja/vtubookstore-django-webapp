from django.db import models
from django.contrib.auth.models import User

class Branch(models.Model):
    branch_name = models.CharField(max_length=100 , null=True , blank = True )

    def __str__(self):
        return self.branch_name
        

class Sem(models.Model):
    semester = models.CharField(max_length=100 , blank=True , null=True)

    def __str__(self):
        return self.semester


class UserDetail(models.Model):
    user_info = models.OneToOneField(User , on_delete = models.CASCADE , null=True , blank=True)
    user_phone = models.IntegerField(blank=True , null=True)
    user_address = models.TextField()
    user_branch = models.ForeignKey(Branch , on_delete=models.CASCADE , null=True , blank=True)
    user_sem = models.ForeignKey(Sem , on_delete=models.CASCADE , null = True , blank=True)


    def __str__(self):
        return self.user_info.username



class Book(models.Model):
    book_img = models.ImageField(null=True, blank=True, upload_to="projects-images/")
    book_title = models.CharField(max_length=100 , blank=True , null=True)
    book_description = models.TextField()
    book_price = models.IntegerField(blank=True , null=True)
    book_branch = models.ForeignKey(Branch , on_delete=models.CASCADE , null = True , blank = True)
    book_sem = models.ForeignKey(Sem , on_delete = models.CASCADE , null = True , blank = True)
    book_seller = models.ForeignKey(User , on_delete=models.CASCADE , blank = True , null = True)


    def __str__(self):
        return self.book_title


class Cart(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    
    def __str__(self):
        return f"{self.buyer} | {self.item}"
    

