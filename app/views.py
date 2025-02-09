from django.shortcuts import render, redirect
from random import randint, randrange
from . models import *
from django.contrib import messages
from django.db import connection
from django.core.mail import EmailMessage
from django.conf import settings
from django.db.models import Sum, Count

def admin_login(request):
	if request.method == 'POST' and request.POST.get('name') == 'admin' and request.POST.get('password') == 'admin':
		return redirect('add_voter')
	else:
		return render(request,'index.html',{})
		messages.success(request,'Invalid Username or Password')
	return render(request,'index.html',{})
def home(request):
	return render(request,'home.html',{})
def add_voter(request):
	cursor=connection.cursor()
	# sql="SELECT v.face_id from app_voter_detail as v order by v.face_id DESC"
	# post = cursor.execute(sql)
	# row = cursor.fetchone()
	# face_ids = row[0]
	# a = int(face_ids)
	# fid=a+1
	if request.method == "POST":
		name = request.POST.get('name')
		email = request.POST.get('email')
		mobile = request.POST.get('mobile')
		face_id = request.POST.get('face_id')
		age = request.POST.get('age')
		dob = request.POST.get('dob')
		gender = request.POST.get('gender')
		city = request.POST.get('city')
		area = request.POST.get('area')
		address = request.POST.get('address')
		image = request.FILES['image']
		voter_id = request.FILES['voter_id']
		password = randint(10000, 99999)
		crt=Voter_Detail.objects.create(name=name,email=email,mobile=mobile,age=age,gender=gender,
		dob=dob,area=area,city=city,address=address,image=image,voter_id=voter_id,password=password,face_id=int(face_id))
		if crt:
			cursor = connection.cursor()
			sql=''' SELECT u.face_id,u.password from app_voter_detail as u order by u.face_id DESC'''
			query = cursor.execute(sql)
			row = cursor.fetchone()
			pwd = row[1]
			addFace(int(request.POST.get('face_id')))
			messages.success(request,"Voter Detail Added Successfully.")
			recipient_list = [email]
			email_from = settings.EMAIL_HOST_USER
			b = EmailMessage('Login Id and Password','Login Id:  ' + face_id  +  ' Password: ' + pwd ,email_from,recipient_list).send()
			redirect('home')
		else:
			messages.error(request,"Account registered failed")


	return render(request, 'add_voter.html', {})
def add_candidate(request):
	if request.method == "POST":
		name = request.POST.get('name')
		email = request.POST.get('email')
		mobile = request.POST.get('mobile')
		age = request.POST.get('age')
		dob = request.POST.get('dob')
		gender = request.POST.get('gender')
		city = request.POST.get('city')
		area = request.POST.get('area')
		address = request.POST.get('address')
		image = request.FILES['image']
		voter_id = request.FILES['img']
		crt=Candidate_Detail.objects.create(name=name,email=email,mobile=mobile,age=age,gender=gender,
		dob=dob,area=area,city=city,address=address,symbol=image,image=voter_id)
		if crt:
			messages.success(request,"Candidate Detail Added Successfully.")
	return render(request, 'add_candidate.html', {})
def view_voter(request):
	row=Voter_Detail.objects.all().order_by('-face_id')
	return render(request,'view_voter.html',{'row':row})
def view_candidate(request):
	row=Candidate_Detail.objects.all().order_by('-id')
	return render(request,'view_candidate.html',{'row':row})
import cv2
import os
# import sqlite3
import numpy as np
from PIL import Image

detector = cv2.CascadeClassifier('app/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()


# # Create a connection witn databse
# conn = sqlite3.connect('db.sqlite3')
# if conn != 0:
#     print("Connection Successful")
# else:
#     print('Connection Failed')
#     exit()

# Creating table if it doesn't already exists
# conn.execute('''create table if not exists facedata ( id int primary key, name char(20) not null)''')

class FaceRecognition:    

    def faceDetect(self, Entry1,):
        face_id = Entry1
        cam = cv2.VideoCapture(0)
        

        count = 0

        while(True):

            ret, img = cam.read()
            # img = cv2.flip(img, -1) # flip video image vertically
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)

            for (x,y,w,h) in faces:

                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
                count += 1

                # Save the captured image into the datasets folder
                cv2.imwrite('app/dataset/User.' + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

                cv2.imshow('Register Face', img)

            k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                break
            elif count >= 30: # Take 30 face sample and stop video
                break
    
    
        cam.release()
        cv2.destroyAllWindows()

    
    def trainFace(self):
        # Path for face image database
        path = 'app/dataset'

        # function to get the images and label data
        def getImagesAndLabels(path):

            imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
            faceSamples=[]
            ids = []

            for imagePath in imagePaths:

                PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
                img_numpy = np.array(PIL_img,'uint8')

                face_id = int(os.path.split(imagePath)[-1].split(".")[1])
                print("face_id",face_id)
                faces = detector.detectMultiScale(img_numpy)

                for (x,y,w,h) in faces:
                    faceSamples.append(img_numpy[y:y+h,x:x+w])
                    ids.append(face_id)

            return faceSamples,ids

        print ("\n Training faces. It will take a few seconds. Wait ...")
        faces,ids = getImagesAndLabels(path)
        recognizer.train(faces, np.array(ids))

        # Save the model into trainer/trainer.yml
        recognizer.save('app/trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi

        # Print the numer of faces trained and end program
        print("\n {0} faces trained. Exiting Program".format(len(np.unique(ids))))


    def recognizeFace(self):
        recognizer.read('app/trainer/trainer.yml')
        cascadePath = 'app/haarcascade_frontalface_default.xml'
        faceCascade = cv2.CascadeClassifier(cascadePath)

        font = cv2.FONT_HERSHEY_SIMPLEX

        confidence = 0
        cam = cv2.VideoCapture(0)

        # Define min window size to be recognized as a face
        minW = 0.1*cam.get(3)
        minH = 0.1*cam.get(4)

        while True:

            ret, img =cam.read()

            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale( 
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(minW), int(minH)),
            )

            for(x,y,w,h) in faces:

                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

                face_id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

                # Check if confidence is less then 100 ==> "0" is perfect match 
                if (confidence < 100):
                    name = 'Detected'
                else:
                    name = "Unknown"
                
                cv2.putText(img, str(name), (x+5,y-5), font, 1, (255,255,255), 2)
                cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
            
            cv2.imshow('Detect Face',img) 

            k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                break
            if confidence > 50:
                break

        print("\n Exiting Program")
        cam.release()
        cv2.destroyAllWindows()
        print(face_id)
        return face_id
faceRecognition = FaceRecognition()
def addFace(face_id):
    face_id = face_id
    faceRecognition.faceDetect(face_id)
    faceRecognition.trainFace()
    return redirect('home')
def voter_login(request):
	if request.session.has_key('user'):
		return redirect("dashboard")
	else:
		if request.method == 'POST':
			username = request.POST.get('name')
			password =  request.POST.get('password')
			post = Voter_Detail.objects.filter(face_id=int(username),password=password)
			if post:
				uid = request.POST.get('name')
				request.session['user'] = uid
				a = request.session['user']
				return redirect("dashboard")
			else:
				messages.success(request, 'Invalid Username or Password')
	return render(request,'voter_login.html',{})
def dashboard(request):
	if request.session.has_key('user'):
		return render(request,'dashboard.html',{})
	else:
		return render(request,'voter_login.html',{})
def logout(request):
    try:
        del request.session['user']
    except:
     pass
    return render(request, 'voter_login.html', {})
def candidate_list(request):
	if request.session.has_key('user'):
		row = Candidate_Detail.objects.all()
		return render(request,'candidate_list.html',{'row':row})
	else:
		return render(request,'voter_login.html',{})
def pool_vote(request):
	face_id = faceRecognition.recognizeFace()
	print(face_id)
	user_id=request.session['user']
	uid=int(user_id)
	fid=int(face_id)
	if uid==fid:
		candidate_id=request.GET.get('candidate_id')
		cid=Candidate_Detail.objects.get(id=int(candidate_id))
		voter_id=Voter_Detail.objects.get(face_id=fid)
		vote=1
		already_exist=Vote.objects.filter(voter_id=fid)
		if already_exist:
			return redirect('voted')
		else:
			crt=Vote.objects.create(voter_id=voter_id,candidate_id=cid,vote=vote)
			if crt:
				cursor=connection.cursor()
				sql1='''SELECT app_voter_detail.email from app_voter_detail where  app_voter_detail.face_id='%d' ''' % (fid)
				post1=cursor.execute(sql1)
				row1=cursor.fetchone()
				if row1:
					em_id = row1[0]
					recipient_list = [em_id]
					email_from = settings.EMAIL_HOST_USER
					b = EmailMessage('Voting Message','You Have Voted Successfully. Thanks For Your Contribution..!!!',email_from,recipient_list).send()
				cursor=connection.cursor()
				sql='''SELECT Count(v.vote),v.candidate_id_id,c.name,c.image,c.area from app_vote as v INNER JOIN app_candidate_detail as c
				ON v.candidate_id_id=c.id GROUP BY v.candidate_id_id'''
				post=cursor.execute(sql)
				row=cursor.fetchall()
				for i in row:
					candidate_name = i[2]
					area =i[4]
					tot = str(i[0])
					email = 'nitroware.projects@gmail.com'
					recipient_list = [email]
					email_from = settings.EMAIL_HOST_USER
					b = EmailMessage('Voting Count Per Candidate','Candidate Name:  ' + candidate_name  +  ' Area: ' + area  +  ' Total Vote: ' + tot,email_from,recipient_list).send()
				return redirect('greeting' ,str(face_id))
	else:
		return render(request,'voter_login.html',{})

def Greeting(request,face_id):
    face_id = int(face_id)
    context ={
        'user' : Voter_Detail.objects.get(face_id = face_id)
    }
    return render(request,'greeting.html',context=context)
def voted(request):
	return render(request,'voted.html',{})
def my_vote(request):
	if request.session.has_key('user'):
		user_id=request.session['user']
		row = Vote.objects.filter(voter_id=int(user_id))
		return render(request,'my_vote.html',{'row':row})
	else:
		return render(request,'voter_login.html',{})
def all_vote(request):
	row=Vote.objects.all()
	return render(request,'all_vote.html',{'row':row})
def result(request):
	cursor=connection.cursor()
	sql='''SELECT Count(v.vote),v.candidate_id_id,c.name,c.image,c.area from app_vote as v INNER JOIN app_candidate_detail as c
	ON v.candidate_id_id=c.id GROUP BY v.candidate_id_id'''
	post=cursor.execute(sql)
	row=cursor.fetchall()
	for i in row:
		candidate_name = i[2]
		area =i[4]
		tot = str(i[0])
		email = 'nitroware.projects@gmail.com'
		recipient_list = [email]
		email_from = settings.EMAIL_HOST_USER
		b = EmailMessage('Voting Count Per Candidate','Candidate Name:  ' + candidate_name  +  ' Area: ' + area  +  ' Total Vote: ' + tot,email_from,recipient_list).send()
	return render(request,'result.html',{'row':row})