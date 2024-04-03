from django.db import models

# Create your models here.
class notesTable(models.Model):
    subject = models.CharField(max_length=100,null=True)
    image = models.ImageField(null=True)
    note = models.CharField(max_length=500,null=True)
    author = models.CharField(max_length=50,null=True)
    time = models.DateTimeField(auto_now_add=True)
    isPublic = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

class notesDraftTable(models.Model):
    subject = models.CharField(max_length=100,null=True)
    image = models.ImageField(null=True)
    note = models.CharField(max_length=500,null=True)
    author = models.CharField(max_length=50,null=True)
    time = models.DateTimeField(auto_now_add=True)
    saved = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

class booksTable(models.Model):
    title = models.CharField(max_length=50,null=True)
    author = models.CharField(max_length=50,null=True)
    uploadedBy = models.CharField(max_length=50,null=True)
    price = models.IntegerField(null=True)
    coverImage = models.ImageField(null=True)
    book = models.FileField(null=True)

    def __str__(self):
        return self.title
    
class bookPaymentTable(models.Model):
    user = models.CharField(max_length=50,null=True)
    uploadedBy = models.CharField(max_length=50,null=True)
    book = models.CharField(max_length=50,null=True)
    amount = models.IntegerField(null=True)
    approved = models.BooleanField(default=False)    

    def __str__(self):
        return self.user
    
class userProfileTable(models.Model):
    user = models.CharField(max_length=50,null=True)
    college = models.CharField(max_length=100,null=True)
    designation = models.CharField(max_length=50,null=True)
    isPrivate = models.BooleanField(default=False)

    def __str__(self):
        return self.user

class assignmentTable(models.Model):
    user = models.CharField(max_length=50,null=True)
    subject = models.CharField(max_length=100,null=True)
    assignment = models.FileField(null=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
    
class privateNoteTable(models.Model):
    user = models.CharField(max_length=50,null=True)
    uploadedBy = models.CharField(max_length=50,null=True)
    note = models.CharField(max_length=100,null=True)
    approved = models.BooleanField(default=False)    

    def __str__(self):
        return self.user