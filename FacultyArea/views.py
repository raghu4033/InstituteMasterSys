from django.shortcuts import render,redirect
from django.conf import settings
from django.urls import reverse
from AdminArea.models import Student_Registration,Faculty_Salary,Student_Schedule,Faculty_Leave,Faculty_Registration,Student_Leave,Student_Suggestion,ELibrary,Submitions_Registration,Student_Inquiry,Admin_Registration,institute_Detaile,Event_Registration,StudentFees,Notice_Registration
from datetime import datetime
from django.utils import timezone
import pytz
import random
from twilio.rest import Client
from django.core.mail import send_mail

def index(request):
	return render(request,'FacultyArea/FacultyDashborad.html')
def FacultyLogin(request):
	if request.method=="POST":
		fid=request.POST['fid']
		password=request.POST['password']
		try:
			faculty_user=Faculty_Registration.objects.get(faculty_id=fid,password=password)
			if faculty_user.status == 'activated':
				request.session['faculty_id']=faculty_user.faculty_id
	 
				request.session['middle_name']=faculty_user.middel_name
				request.session['imageurlfaculty']=faculty_user.photo.url
				return redirect('FacultyArea:FacultyDashborad')
			else:
				FailedMsg="Your Login is Not activated"
				return render(request,'Login/FacultyLogin.html',{'FailedMsg':FailedMsg})
		except:
			FailedMsg="Encorect Email or Password"
			return render(request,'Login/FacultyLogin.html',{'FailedMsg':FailedMsg})
	else:
		return render(request,'Login/FacultyLogin.html')
def FacultyLogout(request):
	try:
		del request.session['faculty_id']
		del request.session['middle_name']
		del request.session['imageurlfaculty']
		del request.session['faculty_id']
		return render(request,'Login/FacultyLogin.html')
	except:
		return render(request,'Login/FacultyLogin.html')

def FacultyDashborad(request):
	total_student=Student_Registration.objects.all().count()
	total_Inqueiry=Student_Inquiry.objects.all().count()
	AllEvents=Event_Registration.objects.all().count()

	Batch=Student_Registration.objects.all()
	result = []
	for i in Batch:
		result.append(i.batch)
	mylist = list(dict.fromkeys(result))	
	total_batch=len(mylist)

	FacultyAllLeavelist=Faculty_Leave.objects.filter(faculty_user_id=request.session['faculty_id']).order_by('-id')[0:3]
	AllLeavelist=Student_Leave.objects.all().order_by('-id')[0:5]
	StudentInquiryList=Student_Inquiry.objects.all().order_by('-inquiry_date')[0:5]

	return render(request,'FacultyArea/FacultyDashborad.html',{'FacultyAllLeavelist':FacultyAllLeavelist,'StudentInquiryList':StudentInquiryList,'AllLeavelist':AllLeavelist,'total_batch':total_batch,'total_Inqueiry':total_Inqueiry,'total_student':total_student,'AllEvents':AllEvents})


def FacultyForgotPassword(request):
	if request.method=="POST":
		fid=request.POST['fid']
		try:
			Faculty=Faculty_Registration.objects.get(faculty_id=fid)
			email=Faculty.email
			otp=random.randint(100000,999999)
			message="Your OTP For Registration Is"+" "+str(otp)
			rec=[email,]
			subject="OTP Recived Successefully"                        
			email_from=settings.EMAIL_HOST_USER
			send_mail(subject,message,email_from,rec)
			SuccessMsg="Check Your Email For The OTP"

			# client = Client(settings.TWILIO['TWILIO_ACCOUNT_SID'],settings.TWILIO['TWILIO_AUTH_TOKEN'])
			# client.api.messages.create(to=f"+91{mobile}",from_=settings.TWILIO['TWILIO_NUMBER'],body=message)
			return render(request,'FacultyArea/FacultyOTP.html',{'Faculty':Faculty,'otp':otp,'SuccessMsg':SuccessMsg})
		except Exception as e:
			print(e)
			FailedMsg="Student Not Found"
			return render(request,'FacultyArea/FacultyForgotPassword.html',{'FailedMsg':FailedMsg})
	else:
		return render(request,'FacultyArea/FacultyForgotPassword.html')
def FacultyOTP(request):
	if request.method=="POST":
		fid=request.POST['fid']
		user_otp=request.POST['user_otp']
		otp=request.POST['otp']
		if otp==user_otp:
			return render(request,'FacultyArea/FacultyNewPassword.html',{'fid':fid})
		else:
			FailedMsg="Invelid OTP"
			return render(request,'FacultyArea/AdmintOTP.html',{'fid':fid,'FailedMsg':FailedMsg,'otp':otp})
	else:
		return render(request,'FacultyArea/FacultyOTP.html')
def FacultyNewPassword(request):
	if request.method=="POST":
		password=request.POST['password']
		repassword=request.POST['repassword']
		fid=request.POST['fid']
		if password==repassword:
			faculty=Faculty_Registration.objects.get(faculty_id=fid)
			faculty.password=password
			faculty.cpassword=password
			faculty.save()
			return redirect('FacultyArea:FacultyLogin')
		else:
			FailedMsg="Password and Confirm Password Does not Match"
			return render(request,'FacultyArea/FacultyNewPassword.html',{'fid':fid,'FailedMsg':FailedMsg})
	else:
		pass
def FacultyChangePassword(request):
	FacultyUser=Faculty_Registration.objects.get(faculty_id = request.session['faculty_id'])
	if request.method=="POST":
		old_password=request.POST['old_password']
		password=request.POST['password']
		cpassword=request.POST['cpassword']
		try:
			FacultyUser=Faculty_Registration.objects.get(faculty_id = request.session['faculty_id'])
			if FacultyUser.password==old_password and password==cpassword:
				FacultyUser.password=password
				FacultyUser.cpassword=password
				FacultyUser.save()
				return redirect('FacultyArea:FacultyLogout')
			else:
				FailedMsg="Password & Confirm Password Does Not Matched"
				return render(request,'dminArea/AdminChangePassword.html',{'FailedMsg':FailedMsg,'FacultyUser':FacultyUser})
		except Exception as e:
			print(e)
			pass
	else:
		return render(request,'FacultyArea/FacultyChangePassword.html',{'FacultyUser':FacultyUser})
	

def FacultyProfile(request):
	FacultyUser=Faculty_Registration.objects.get(faculty_id=request.session['faculty_id'])
	return render(request,'FacultyArea/FacultyProfile.html',{'FacultyUser':FacultyUser})

def FacultyApplyLeave(request):
	Faculty=Faculty_Registration.objects.get(faculty_id=request.session['faculty_id'])
	PandingLeave=Faculty_Leave.objects.filter(status="Panding_Request",faculty_user_id=Faculty.faculty_id)
	if request.method=="POST":
		faculty_id=request.POST['faculty_id']
		faculty_name=request.POST['faculty_name']
		faculty_department=request.POST['faculty_department']
		from_date=request.POST['from_date']
		to_date=request.POST['to_date']
		leave_type=request.POST['leave_type']
		Leave_Reason=request.POST['Leave_Reason']
		Leave_Day=request.POST['Leave_Day']

		try:
			Faculty_Leave.objects.create(faculty_user_id=faculty_id,full_Name=faculty_name,department=faculty_department,from_date=from_date,to_date=to_date,Leave_catagory=leave_type,Leave_reason=Leave_Reason,Leave_day=Leave_Day)
			SuccessMsg="Leave Request sent Successefully"
			return render(request,'FacultyArea/FacultyApplyLeave.html',{'SuccessMsg':SuccessMsg,'Faculty':Faculty,'PandingLeave':PandingLeave})
		except:
			FailedMsg="Leave Request sent Failed"
			return render(request,'FacultyArea/FacultyApplyLeave.html',{'FailedMsg':FailedMsg,'Faculty':Faculty,'PandingLeave':PandingLeave})
	else:
		return render(request,'FacultyArea/FacultyApplyLeave.html',{'Faculty':Faculty,'PandingLeave':PandingLeave})
def FacultyViewLeave(request):
	Faculty=Faculty_Registration.objects.get(faculty_id=request.session['faculty_id'])
	YourAllLeave=Faculty_Leave.objects.filter(faculty_user_id=Faculty.faculty_id).order_by('-id')
	return render(request,'FacultyArea/FacultyViewLeave.html',{'Faculty':Faculty,'YourAllLeave':YourAllLeave})

def FacultySalaryDetailes(request):
	faculty=Faculty_Registration.objects.get(faculty_id=request.session['faculty_id'])
	Salarysdetails=Faculty_Salary.objects.filter(faculty_user_id=faculty.faculty_id)
	return render(request,'FacultyArea/FacultySalaryDetailes.html',{'Salarysdetails':Salarysdetails})


def FacultyEnrollStudentInquiry(request):
	if request.method=="POST":
		date=request.POST['date']
		full_name=request.POST['full_name']
		dob=request.POST['dob']
		gender=request.POST['gender']
		address=request.POST['address']
		mobile_number=request.POST['mobile_number']
		whatsapp_number=request.POST['whatsapp_number']
		email=request.POST['email']
		edu_que=request.POST['edu_que']
		course=request.POST['course']
		reference=request.POST['reference']
		faculty_user=request.session['faculty_id']
		print("admin user detaile")
		print(faculty_user,date,full_name,dob,gender,address,mobile_number,whatsapp_number,email,edu_que,course,reference)
		try:
			Student_Inquiry.objects.create(inquiry_date=date,full_name=full_name,dob=dob,gender=gender,address=address,mobile=mobile_number,whatsapp=whatsapp_number,email=email,edu_que=edu_que,course=course,reference=reference,faculty_user_id=faculty_user)
			msg="Student Inquery Registered Successefully"
			# rec=[email,]
			# subject="Thanks for visiting Kalaveethi Institute"
			# website="https://kalaveethi.com/"
			# booklate="https://kalaveethi.com/courses/kalaveethibook/"
			# message=f"Hi {full_name}\n \nThank you for reaching out to Kalaveethi Institue Of Design. I’m Trupal Gajera, your admissions counselor. I look forward to working with you. Please feel free to text me here or my colleagues at  if you have any questions. \n \n \n Phone: +91 8160892915 \n Website: {website} \n \nDownload Booklate:{booklate}"
			# email_from=settings.EMAIL_HOST_USER
			# send_mail(subject,message,email_from,rec)

			# client = Client(settings.TWILIO['TWILIO_ACCOUNT_SID'],settings.TWILIO['TWILIO_AUTH_TOKEN'])
			# client.api.messages.create(to=f"+91{mobile_number}",from_=settings.TWILIO['TWILIO_NUMBER'],body=message)

			SuccessMsg="Student Inquery Successefully Added"
			return render(request,'FacultyArea/FacultyEnrollStudentInquiry.html',{'SuccessMsg':SuccessMsg})
		except Exception as e:
			print(e)
			FailedMsg="Student Inquery Added Failed!"
			return render(request,'FacultyArea/FacultyEnrollStudentInquiry.html',{'FailedMsg':FailedMsg})
	else:
		return render(request,'FacultyArea/FacultyEnrollStudentInquiry.html')

def FacultytInquiryList(request):
	StudentInquiryList=Student_Inquiry.objects.all().order_by('-inquiry_date')
	return render(request,'FacultyArea/FacultytInquiryList.html',{'StudentInquiryList':StudentInquiryList})

def FacultyAddSubmitions(request):
	if request.method=="POST":
		course=request.POST['course']
		batch_name=request.POST['batch_name']
		subject=request.POST['subject']
		desc=request.POST['desc']
		date=request.POST['date']
		notice_file=request.FILES['file']
		faculty_user=request.session['faculty_id']
		try:
			Submitions_Registration.objects.create(course=course,batch=batch_name,subject=subject,desc=desc,last_date=date,submitions_file=notice_file,faculty_user_id=faculty_user)
			SuccessMsg="Submitions Added Successefully"
			return render(request,'FacultyArea/FacultyAddSubmitions.html',{'SuccessMsg':SuccessMsg})
		except:
			FailedMsg="Submitions Added Failed"
			return render(request,'FacultyArea/FacultyAddSubmitions.html',{'FailedMsg':FailedMsg})
	else:
		return render(request,'FacultyArea/FacultyAddSubmitions.html')
def FacultySubmitionsList(request):
	AllSubmitions=Submitions_Registration.objects.all().order_by('-last_date')
	return render(request,'FacultyArea/FacultytSubmitionsList.html',{'AllSubmitions':AllSubmitions})

def FacultyAddClassSchedule(request):
	if request.method=="POST":
		class_for=request.POST['class_for']
		Batch=Student_Registration.objects.filter(course_type=class_for)
		result = []
		for i in Batch:
			result.append(i.batch)
		mylist = list(dict.fromkeys(result))
		print(mylist)
		return render(request,'FacultyArea/FacultyAddClassSchedule.html',{'mylist':mylist})
	else:
		return render(request,'FacultyArea/FacultyAddClassSchedule.html')

def FacultyScheduleClass(request):
	if request.method=="POST":
		batch_for=request.POST['batch_for']
		from_date=request.POST['from_date']
		to_date=request.POST['to_date']
		from_time=request.POST['from_time']
		to_time=request.POST['to_time']
		subject=request.POST['subject']
		class_type=request.POST['class_type']
		organizer=request.POST['organizer']
		faculty_user=request.session['faculty_id']
		try:
			Student_Schedule.objects.create(from_date=from_date,to_date=to_date,from_time=from_time,to_time=to_time,subject=subject,classtype=class_type,batch_nm=batch_for,organizer=organizer,faculty_user_id=faculty_user)
			SuccessMsg="class Added Successefully"
			return render(request,'FacultyArea/FacultyAddClassSchedule.html',{'SuccessMsg':SuccessMsg})
		except:
			FailedMsg="class Added Failed"
			return render(request,'FacultyArea/FacultyAddClassSchedule.html',{'FailedMsg':FailedMsg})
	else:
		return render(request,'FacultyArea/FacultyAddClassSchedule.html')

def FacultyViewClassSchedule(request):
	AllClass=Student_Schedule.objects.all().order_by('-id')
	return render(request,'FacultyArea/FacultyViewClassSchedule.html',{'AllClass':AllClass})

def FacultyAddBook(request):
	if request.method=="POST":
		book_for=request.POST['book_for']
		book_title=request.POST['book_title']
		book_link=request.POST['book_link']
		book_photo=request.FILES['book_photo']
		book_pdf=request.FILES['book_pdf']
		faculty_user=request.session['faculty_id']
		try:
			ELibrary.objects.create(book_for=book_for,book_title=book_title,book_link=book_link,book_photo=book_photo,book_pdf=book_pdf,faculty_user_id=faculty_user)
			SuccessMsg="Book Added Successefully"
			return render(request,'FacultyArea/FacultyAddBook.html',{'SuccessMsg':SuccessMsg})
		except:
			FailedMsg="Book Added Failed"
			return render(request,'FacultyArea/FacultyAddBook.html',{'FailedMsg':FailedMsg})
	else:
		return render(request,'FacultyArea/FacultyAddBook.html')
def FacultyBookList(request):
	AllBooks=ELibrary.objects.all()
	return render(request,'FacultyArea/FacultyBookList.html',{'AllBooks':AllBooks})

