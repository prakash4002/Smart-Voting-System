from django.conf import settings
from django.db import models
from django.utils import timezone

class Voter_Detail(models.Model):
    face_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    mobile = models.CharField(max_length=30)
    age = models.CharField(max_length=30)
    dob = models.CharField(max_length=30)
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=200)
    gender = models.CharField(max_length=20)
    password = models.CharField(max_length=20,null=True)
    address = models.TextField(max_length=1000)
    voter_id = models.FileField('Voter Id',upload_to='documents/',null=True)
    image = models.FileField('Upload Image',upload_to='documents/',null=True)
    def __str__(self):
    	return self.name
class Candidate_Detail(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    mobile = models.CharField(max_length=30)
    age = models.CharField(max_length=30)
    dob = models.CharField(max_length=30)
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=200)
    gender = models.CharField(max_length=20)
    address = models.TextField(max_length=1000)
    symbol = models.FileField('Symbol',upload_to='documents/',null=True)
    image = models.FileField('Upload Image',upload_to='documents/',null=True)
    def __str__(self):
        return self.name
class Vote(models.Model):
    voter_id = models.ForeignKey(Voter_Detail, on_delete=models.CASCADE)
    candidate_id = models.ForeignKey(Candidate_Detail, on_delete=models.CASCADE)
    vote = models.IntegerField()
    date = models.DateField('Posted Date',default=timezone.now())
    def __str__(self):
        return self.voter_id.name
    def publish(self):
        self.date = timezone.now()
        self.save()