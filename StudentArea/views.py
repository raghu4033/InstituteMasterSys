from django.shortcuts import render,redirect
from django.conf import settings
from django.urls import reverse
from AdminArea.models import Student_Registration,Student_Attendence,Student_Certificate,Student_Schedule,Student_Leave,Student_Suggestion,ELibrary,Submitions_Registration,Student_Inquiry,Admin_Registration,institute_Detaile,Event_Registration,StudentFees,Notice_Registration
from datetime import datetime
from twilio.rest import Client
from django.core.mail import send_mail
from django.utils import timezone
import pytz
import random


# Create your views here.


def StudentLogin(request):
	if request.method=="POST":
		sid=request.POST['sid']
		password=request.POST['password']
		try:
			student=Student_Registration.objects.get(sid=sid,password=password)
			if student.status == 'activated':
				# student.last_login = datetime.now().strftime("%Y-%M-%d")
				
				# student.save()
				request.session['sid']=student.sid
				# request.session['last_login'] = student.last_login
				request.session['studentmname']=student.fname
				request.session['studentphoto']=student.photo.url
				return redirect('StudentArea:StudentDashboard')
			else:
				FailedMsg="Your Login is Not activated"
				print(msg)
				return render(request,'Login/index.html',{'FailedMsg':FailedMsg})
		except Exception as e:
			FailedMsg="Encorect Email or Password"
			return render(request,'Login/index.html',{'FailedMsg':FailedMsg})
	else:
		return render(request,'Login/index.html')
def StudentLogout(request):
	try:
		del request.session['sid']
		del request.session['studentmname']
		del request.session['studentphoto']
		return redirect('StudentArea:StudentLogin')
	except:
		return render(request,'Login/index.html')

def StudentDashboard(request):
	Student=Student_Registration.objects.get(sid=request.session['sid'])
	AllEvent=Event_Registration.objects.all().count()
	AllNotice=Notice_Registration.objects.all().count()
	AllBook=ELibrary.objects.all().count()
	AllSubmitions=Submitions_Registration.objects.all().count()

	Event=Event_Registration.objects.all().order_by('-id')[0:1]
	Notice=Notice_Registration.objects.all().order_by('-id')[0:1]
	Submitions=Submitions_Registration.objects.filter(batch=Student.batch).order_by('-id')[0:1]
	


	total_amount=[]
	student=Student_Registration.objects.get(sid=request.session['sid'])
	FeesDetaile=StudentFees.objects.filter(student_id=Student.sid).order_by('-recipt_no')

	Total_Fees_Amount = len(FeesDetaile)
	for i in FeesDetaile:
		total_amount.append(int(i.amount))
	Total_Fees_Amount = sum(total_amount)

	Rimainig_Fees=student.final_fees-Total_Fees_Amount


	
	YourClass=Student_Schedule.objects.filter(batch_nm=Student.batch).order_by('-id')[0:1]
	return render(request,'StudentArea/StudentDashboard.html',{'Submitions':Submitions,'Notice':Notice,'Event':Event,'Student':Student,'Total_Fees_Amount':Total_Fees_Amount,'Rimainig_Fees':Rimainig_Fees,'AllSubmitions':AllSubmitions,'AllBook':AllBook,'AllNotice':AllNotice,'AllEvent':AllEvent,'YourClass':YourClass})

def StudentForgotPassword(request):
	if request.method=="POST":
		sid=request.POST['sid']
		try:
			student=Student_Registration.objects.get(sid=sid)
			email=student.email
			otp=random.randint(100000,999999)
			message="Your OTP For Registration Is"+" "+str(otp)
			rec=[email,]
			subject="OTP Recived Successefully"                        
			email_from=settings.EMAIL_HOST_USER
			send_mail(subject,message,email_from,rec)
			SuccessMsg="Check Your Email For The OTP"

			# client = Client(settings.TWILIO['TWILIO_ACCOUNT_SID'],settings.TWILIO['TWILIO_AUTH_TOKEN'])
			# client.api.messages.create(to=f"+91{mobile}",from_=settings.TWILIO['TWILIO_NUMBER'],body=message)
			return render(request,'StudentArea/StudentOTP.html',{'student':student,'otp':otp,'SuccessMsg':SuccessMsg})
		except Exception as e:
			FailedMsg="Student Not Found"
			return render(request,'StudentArea/StudentForgotPassword.html',{'FailedMsg':FailedMsg})
	else:
		return render(request,'StudentArea/StudentForgotPassword.html')
def StudentOTP(request):
	if request.method=="POST":
		sid=request.POST['sid']
		user_otp=request.POST['user_otp']
		otp=request.POST['otp']
		if otp==user_otp:
			return render(request,'StudentArea/StudentNewPassword.html',{'sid':sid})
		else:
			FailedMsg="Invelid OTP"
			return render(request,'StudentArea/StudentOTP.html',{'sid':sid,'FailedMsg':FailedMsg,'otp':otp})
	else:
		return render(request,'StudentArea/StudentOTP.html')
	
def NewPassword(request):
	if request.method=="POST":
		password=request.POST['password']
		repassword=request.POST['repassword']
		sid=request.POST['sid']
		if password==repassword:
			student=Student_Registration.objects.get(sid=sid)
			student.password=password
			student.cpassword=password
			student.save()
			return redirect('StudentArea:StudentLogin')
		else:
			FailedMsg="Password and Confirm Password Does not Match"
			return render(request,'StudentArea/StudentNewPassword.html',{'sid':sid,'FailedMsg':FailedMsg})
	else:
		pass
	
def StudentChangePassword(request):
	studentinfo=Student_Registration.objects.get(sid = request.session['sid'])
	if request.method=="POST":
		old_password=request.POST['old_password']
		password=request.POST['password']
		cpassword=request.POST['cpassword']
		try:
			student=Student_Registration.objects.get(sid = request.session['sid'])
			if student.password==old_password and password==cpassword:
				student.password=password
				student.cpassword=password
				student.save()
				return redirect('StudentArea:StudentLogout')
			else:
				FailedMsg="Password & Confirm Password Does Not Matched"
				return render(request,'StudentArea/StudentChangePassword.html',{'FailedMsg':FailedMsg,'studentinfo':studentinfo})
		except:
			pass
	else:
		return render(request,'StudentArea/StudentChangePassword.html',{'studentinfo':studentinfo})
def StudentProfile(request):
	studentinfo=Student_Registration.objects.get(sid = request.session['sid'])
	return render(request,'StudentArea/StudentProfile.html',{'studentinfo':studentinfo})

def StudentApplyLeave(request):
	student=Student_Registration.objects.get(sid=request.session['sid'])
	PandingLeave=Student_Leave.objects.filter(status="Panding_Request",student_id=student.sid)
	if request.method=="POST":
		student_id=request.POST['student_id']
		student_name=request.POST['student_name']
		student_course=request.POST['student_course']
		from_date=request.POST['from_date']
		to_date=request.POST['to_date']
		leave_type=request.POST['leave_type']
		Leave_Reason=request.POST['Leave_Reason']
		Leave_Day=request.POST['Leave_Day']

		try:
			Student_Leave.objects.create(student_id=student_id,full_Name=student_name,course=student_course,from_date=from_date,to_date=to_date,Leave_catagory=leave_type,Leave_reason=Leave_Reason,Leave_day=Leave_Day)
			SuccessMsg="Leave Request sent Successefully"
			return render(request,'StudentArea/StudentApplyLeave.html',{'SuccessMsg':SuccessMsg,'student':student,'PandingLeave':PandingLeave})
		except:
			FailedMsg="Leave Request sent Failed"
			return render(request,'StudentArea/StudentApplyLeave.html',{'FailedMsg':FailedMsg,'student':student,'PandingLeave':PandingLeave})
	else:
		return render(request,'StudentArea/StudentApplyLeave.html',{'student':student,'PandingLeave':PandingLeave})
def StudentViewLeave(request):
	student=Student_Registration.objects.get(sid=request.session['sid'])
	YourAllLeave=Student_Leave.objects.filter(student_id=student.sid).order_by('-id')
	return render(request,'StudentArea/StudentViewLeave.html',{'YourAllLeave':YourAllLeave,'student':student})

def StudentViewAttendence(request):
	AttendeceList=Student_Attendence.objects.filter(student_id=request.session['sid']).order_by('-take_date')
	TotalSesion = Student_Attendence.objects.filter(student_id=request.session['sid'])
	TatalClass = len(TotalSesion)
	PresentSesion = Student_Attendence.objects.filter(student_id=request.session['sid'],ap = 'P' )
	PresentClass = len(PresentSesion)
	AbsentSesion = Student_Attendence.objects.filter(student_id=request.session['sid'],ap = 'A' )
	AbsentClass = len(AbsentSesion)


	return render(request,'StudentArea/StudentViewAttendence.html',{'AttendeceList':AttendeceList,'AbsentClass':AbsentClass,'PresentClass':PresentClass,'TatalClass':TatalClass})

def StudentPayFees(request):
	return render(request,'StudentArea/StudentPayFees.html')

def StudentFeesDetaile(request):
	total_amount=[]
	student=Student_Registration.objects.get(sid=request.session['sid'])
	FeesDetaile=StudentFees.objects.filter(student_id=student.sid).order_by('-recipt_no')

	Total_Fees_Amount = len(FeesDetaile)
	for i in FeesDetaile:
		total_amount.append(int(i.amount))
	Total_Fees_Amount = sum(total_amount)

	Rimainig_Fees=student.final_fees-Total_Fees_Amount

	return render(request,'StudentArea/StudentFeesDetaile.html',{'FeesDetaile':FeesDetaile,'student':student,'Total_Fees_Amount':Total_Fees_Amount,'Rimainig_Fees':Rimainig_Fees})
	Student=StudentFees.objects.filter(sid=request.session['sid'])
	return render(request,'StudentArea/StudentFeesDetaile.html',{'Student':Student})

def StudentViewSchedual(request):
	Student=Student_Registration.objects.get(sid=request.session['sid'])
	YourClass=Student_Schedule.objects.filter(batch_nm=Student.batch).order_by('-id')[0:1]
	return render(request,'StudentArea/StudentViewSchedual.html',{'YourClass':YourClass})

def StudentViewEvents(request):
	AllEvent=Event_Registration.objects.all().order_by('-id')
	return render(request,'StudentArea/StudentViewEvents.html',{'AllEvent':AllEvent})
def StudentViewNotice(request):
	student=Student_Registration.objects.get(sid=request.session['sid'])
	AllNotice=Notice_Registration.objects.filter(notice_for=student.course_type)
	return render(request,'StudentArea/StudentViewNotice.html',{'AllNotice':AllNotice})	

def StudentViewHoliday(request):
	return render(request,'StudentArea/StudentViewHoliday.html')


def StudentViewSubmitions(request):
	AllSubmitions=Submitions_Registration.objects.all()
	return render(request,'StudentArea/StudentViewSubmitions.html',{'AllSubmitions':AllSubmitions})

def StudentElibrary(request):
	AllBooks=ELibrary.objects.all()
	return render(request,'StudentArea/StudentElibrary.html',{'AllBooks':AllBooks})

def StudentCertificate(request):
	MyCertificateList=Student_Certificate.objects.filter(student_id=request.session['sid'])
	return render(request,'StudentArea/StudentCertificate.html',{'MyCertificateList':MyCertificateList})

def StudentInsertSuggestion(request):
	if request.method=="POST":
		suggestions_msg=request.POST['suggestions_msg']
		sid=request.session['sid']
		Student_Suggestion.objects.create(student_id=sid,Student_Suggestion=suggestions_msg)
		SuccessMsg="Suggestion Added Successefully"
		return render(request,'StudentArea/StudentInsertSuggestion.html',{'SuccessMsg':SuccessMsg})	
	else:
		return render(request,'StudentArea/StudentInsertSuggestion.html')

def StudentPrintInvoice(request,pk):
	StudentInvoiceInfo=StudentFees.objects.get(pk=pk)
	student=Student_Registration.objects.get(sid=StudentInvoiceInfo.student_id)
	return render(request,'StudentArea/StudentPrintInvoice.html',{'StudentInvoiceInfo':StudentInvoiceInfo,'student':student})