from django.shortcuts import render,redirect
from django.conf import settings
from .models import Student_Registration,Student_Attendence,Student_Certificate,Faculty_Salary,Student_Schedule,Faculty_Leave,Faculty_Registration,Student_Leave,ELibrary,Student_Suggestion,Submitions_Registration,Student_Inquiry,Admin_Registration,institute_Detaile,Event_Registration,StudentFees,Notice_Registration
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
from django.core.mail import BadHeaderError,send_mail
from datetime import datetime
from django.utils import timezone
import random


def index(request):
	return render(request,'Login/index.html')
def admin_login(request):
	if request.method=="POST":
		admin_email=request.POST['admin_email']
		admin_password=request.POST['admin_password']
		try:
			admin_user=Admin_Registration.objects.get(email=admin_email,password=admin_password)
			if admin_user.status == 'activated':
				request.session['admin_email']=admin_user.email
				request.session['mname']=admin_user.mname
				request.session['imageurl']=admin_user.photo.url
				return redirect('AdminArea:AdminDashboard')
			else:
				FailedMsg="Your Login is Not activated"
				return render(request,'Login/admin_login.html',{'FailedMsg':FailedMsg})
		except:
			FailedMsg="Encorect Email or Password"
			return render(request,'Login/admin_login.html',{'FailedMsg':FailedMsg})
	else:
		return render(request,'Login/admin_login.html')
	return render(request,'Login/admin_login.html')

def admin_logout(request):
	try:
		del request.session['admin_email']
		return render(request,'Login/admin_login.html')
	except:
		return render(request,'Login/admin_login.html')

def AdminDashboard(request):
	total_student=Student_Registration.objects.all().count()

	Batch=Student_Registration.objects.all()
	result = []
	for i in Batch:
		result.append(i.batch)
	mylist = list(dict.fromkeys(result))	
	total_batch=len(mylist)

	total_amount=[]
	total_fees=StudentFees.objects.all()
	for i in total_fees:
		total_amount.append(int(i.amount))
	total_feeslen = sum(total_amount)
	
	
	StudentLeaveReq=Student_Leave.objects.filter(status="Panding_Request").count()
	FacultyLeaveReq=Faculty_Leave.objects.filter(status="Panding_Request").count()
	AllEvents=Event_Registration.objects.all().count()
	AllNotice=Notice_Registration.objects.all().order_by('-notice_date')[0:3]
	AllLeavelist=Student_Leave.objects.all().order_by('-id')[0:5]
	StudentInquiryList=Student_Inquiry.objects.all().order_by('-inquiry_date')[0:5]
	return render(request,'AdminArea/AdminDashboard.html',{'FacultyLeaveReq':FacultyLeaveReq,'StudentLeaveReq':StudentLeaveReq,'total_feeslen':total_feeslen,'total_batch':total_batch,'total_student':total_student,'AllNotice':AllNotice,'AllLeavelist':AllLeavelist,'StudentInquiryList':StudentInquiryList,'AllEvents':AllEvents})

def AdminForgotPassword(request):
	if request.method=="POST":
		email=request.POST['email']
		try:
			AdminUser=Admin_Registration.objects.get(email=email)
			print(AdminUser.email)
			e=AdminUser.email
			otp=random.randint(100000,999999)
			message="Your OTP For Registration Is"+" "+str(otp)
			rec=[e,]
			subject="OTP Recived Successefully"                        
			email_from=settings.EMAIL_HOST_USER
			send_mail(subject,message,email_from,rec)
			SuccessMsg="Check Your Email For The OTP"

			return render(request,'AdminArea/AdminOTP.html',{'AdminUser':AdminUser,'otp':otp,'SuccessMsg':SuccessMsg})
		except Exception as e:
			print(e)
			FailedMsg="Admin Not Found"
			return render(request,'AdminArea/AdminForgotPassword.html',{'FailedMsg':FailedMsg})
	else:
		return render(request,'AdminArea/AdminForgotPassword.html')
def AdminOTP(request):
	if request.method=="POST":
		email=request.POST['email']
		user_otp=request.POST['user_otp']
		otp=request.POST['otp']
		if otp==user_otp:
			return render(request,'AdminArea/AdminNewPassword.html',{'email':email})
		else:
			FailedMsg="Invelid OTP"
			return render(request,'AdminArea/AdminOTP.html',{'email':email,'FailedMsg':FailedMsg,'otp':otp})
	else:
		return render(request,'AdminArea/AdminOTP.html')

def AdminNewPassword(request):
	if request.method=="POST":
		password=request.POST['password']
		repassword=request.POST['repassword']
		email=request.POST['email']
		if password==repassword:
			AdminUser=Admin_Registration.objects.get(email=email)
			AdminUser.password=password
			AdminUser.cpassword=password
			AdminUser.save()
			return redirect('AdminArea:admin_login')
		else:
			FailedMsg="Password and Confirm Password Does not Match"
			return render(request,'AdminArea/AdminNewPassword.html',{'email':email,'FailedMsg':FailedMsg})
	else:
		pass
def AdminProfile(request):
	AdminUser=Admin_Registration.objects.get(email = request.session['admin_email'])
	return render(request,'AdminArea/AdminProfile.html',{'AdminUser':AdminUser})

def AdminChangePassword(request):
	AdminUser=Admin_Registration.objects.get(email = request.session['admin_email'])
	if request.method=="POST":
		old_password=request.POST['old_password']
		password=request.POST['password']
		cpassword=request.POST['cpassword']
		try:
			AdminUser=Admin_Registration.objects.get(email = request.session['admin_email'])
			if AdminUser.password==old_password and password==cpassword:
				AdminUser.password=password
				AdminUser.cpassword=password
				AdminUser.save()
				return redirect('AdminArea:admin_logout')
			else:
				FailedMsg="Password & Confirm Password Does Not Matched"
				return render(request,'AdminArea/AdminChangePassword.html',{'FailedMsg':FailedMsg,'AdminUser':AdminUser})
		except:
			pass
	else:
		return render(request,'AdminArea/AdminChangePassword.html',{'AdminUser':AdminUser})
	
def AdminLockScreen(request):
	if request.method=="POST":
		passcode=request.POST['passcode']
		try:
			AdminUser=Admin_Registration.objects.get(email = request.session['admin_email'])
			if AdminUser.sreenpin==passcode:
				return redirect('AdminArea:AdminDashboard')
			else:
				FailedMsg="Envalid Passcode"
				return render(request,'AdminArea/AdminLockScreen.html',{'FailedMsg':FailedMsg})
		except:
			return redirect('AdminArea:admin_login')
	else:
		return render(request,'AdminArea/AdminLockScreen.html')


def Users(request):
	AdminUserList=Admin_Registration.objects.all()
	StudentUserList=Student_Registration.objects.all()
	FacultyUserList=Faculty_Registration.objects.all()
	return render(request,'AdminArea/Users.html',{'AdminUserList':AdminUserList,'StudentUserList':StudentUserList,'FacultyUserList':FacultyUserList})
def UserStatus(request):
	if request.method=="POST":
		UserType=request.POST['UserType']
		try:
			if UserType == 'StudentUser':
				student=Student_Registration.objects.get(sid=request.POST['sid'])
				if student.status == 'activated':
					student.status = "Dectivated"
					student.save()
					return redirect('AdminArea:Users')
				else:
					student.status = "activated"
					student.save()
					return redirect('AdminArea:Users')

			elif UserType == 'FacultyUser':
				Faculty=Faculty_Registration.objects.get(faculty_id=request.POST['faculty_id'])
				if Faculty.status == 'activated':
					Faculty.status = "Dectivated"
					Faculty.save()
					return redirect('AdminArea:Users')
				else:
					Faculty.status = "activated"
					Faculty.save()
					return redirect('AdminArea:Users')
			elif UserType == 'AdminUser':
				Admin=Admin_Registration.objects.get(email=request.POST['fid'])
				if Admin.status == 'activated':
					Admin.status = "Dectivated"
					Admin.save()
					return redirect('AdminArea:Users')
				else:
					Admin.status = "activated"
					Admin.save()
					return redirect('AdminArea:Users')
		except:
			return redirect('AdminArea:Users')
	else:
		return redirect('AdminArea:Users')

def InstituteDetailes(request):
	if request.method=="POST":
		tabledata=institute_Detaile.objects.all()
		if tabledata:
			uid=request.POST['uid']
			institute_name=request.POST['institute_name']
			institute_code=request.POST['institute_code']
			institute_address=request.POST['institute_address']
			fb_url=request.POST['fb_url']
			insta_url=request.POST['insta_url']
			google_url=request.POST['google_url']
			institute_phone=request.POST['ins_phone']
			institute_email=request.POST['institute_email']
			website_url=request.POST['website_url']

			try:
				institute=institute_Detaile.objects.get(id=uid)
				institute.ins_name=institute_name
				institute.ins_id=institute_code
				institute.ins_address=institute_address
				institute.ins_fb=fb_url
				institute.ins_insta=insta_url
				institute.ins_google=google_url
				institute.ins_phone=institute_phone
				institute.ins_email=institute_email
				institute.ins_web=website_url
		
				try:
					if request.FILES['logo']:
						institute.logo=request.FILES['logo']
				except:
					pass
				institute.save()
				SuccessMsg="Profile Upadate Successefully"
				InstituteInfo=institute_Detaile.objects.latest('id')
				return render(request,'AdminArea/InstituteDetailes.html',{'InstituteInfo':InstituteInfo,'SuccessMsg':SuccessMsg})
			except Exception as e:
				print(e)
				FailedMsg="Profile Upadate Failed"
				InstituteInfo=institute_Detaile.objects.latest('id')
				return render(request,'AdminArea/InstituteDetailes.html',{'InstituteInfo':InstituteInfo,'FailedMsg':FailedMsg})
		else:
			institute_name=request.POST['institute_name']
			institute_code=request.POST['institute_code']
			institute_address=request.POST['institute_address']
			fb_url=request.POST['fb_url']
			insta_url=request.POST['insta_url']
			google_url=request.POST['google_url']
			institute_phone=request.POST['ins_phone']
			institute_email=request.POST['institute_email']
			website_url=request.POST['website_url']
			logo=request.FILES['logo']

			try:
				institute_Detaile.objects.create(ins_name=institute_name,ins_id=institute_code,ins_address=institute_address,ins_fb=fb_url,ins_insta=insta_url,ins_google=google_url,ins_phone=institute_phone,ins_email=institute_email,ins_web=website_url,logo=logo)
				SuccessMsg="Profile Upadate Successefully"
				InstituteInfo=institute_Detaile.objects.latest('id')
				return render(request,'AdminArea/InstituteDetailes.html',{'InstituteInfo':InstituteInfo,'SuccessMsg':SuccessMsg})
			except Exception as e:
				FailedMsg="Profile Upadate Failed"
				print(e)
				InstituteInfo=institute_Detaile.objects.latest('id')
				return render(request,'AdminArea/InstituteDetailes.html',{'InstituteInfo':InstituteInfo,'FailedMsg':FailedMsg})
	else:
		try:
			InstituteInfo=institute_Detaile.objects.latest('id')
			return render(request,'AdminArea/InstituteDetailes.html',{'InstituteInfo':InstituteInfo,'InstituteInfo':InstituteInfo})
		except Exception as e:
			
			return render(request,'AdminArea/InstituteDetailes.html')
def AddAdminUser(request):
	if request.method=="POST":
		email=request.POST['email']
		password=request.POST['password']
		cpassword=request.POST['cpassword']
		sreenpin=request.POST['sreenpin']
		csreenpin=request.POST['csreenpin']

		fname=request.POST['fname']
		dob=request.POST['dob']
		aadhar_num=request.POST['aadhar_num']
		mname=request.POST['mname']
		gender=request.POST['gender']
		lname=request.POST['lname']

		address=request.POST['address']
		city=request.POST['city']
		pin=request.POST['pin']
		mobile=request.POST['mobile']
		photo=request.FILES['photo']

		
		# print(std_photo,academic_year,sid,join_date,admission_num,fname,category,aadhar_num,mname,gender,nationality,lname,blood_group,cast,permanent_address,present_address,city,pin,mobile,email,father_name,job,father_mobile,father_aadhar,college_name,qualifications,college_address,course_name,dob,batch_name,course_type)

		try:
			admin=Admin_Registration.objects.get(email=email)
			FailedMsg="Admin Email Alredy Registered"
			return render(request,'AdminArea/StudentAdmission.html',{'FailedMsg':FailedMsg})
		except:
			Admin_Registration.objects.create(
												email=email,
												password=password,
												cpassword=cpassword,
												sreenpin=sreenpin,
												csreenpin=csreenpin,
												mname=mname,
												lname=lname,
												fname=fname,
												dob=dob,
												gender=gender,
												aadhar=aadhar_num,
												address=address,
												city=city,
												pin=pin,
												mobile=mobile,
												photo=photo,
												)
			SuccessMsg="Admin Registered Successefully"
			return render(request,'AdminArea/AddAdminUser.html',{'SuccessMsg':SuccessMsg})
	else:
		return render(request,'AdminArea/AddAdminUser.html')

def StudentAdmission(request):
	if request.method=="POST":
		academic_year=request.POST['academic_year']
		sid=request.POST['sid']
		join_date=request.POST['join_date']
		admission_num=request.POST['admission_num']
		fname=request.POST['fname']
		category=request.POST['category']
		aadhar_num=request.POST['aadhar_num']
		mname=request.POST['mname']
		gender=request.POST['gender']
		nationality=request.POST['nationality']
		lname=request.POST['lname']
		blood_group=request.POST['blood_group']
		cast=request.POST['cast']
		permanent_address=request.POST['permanent_address']
		present_address=request.POST['present_address']
		city=request.POST['city']
		pin=request.POST['pin']
		mobile=request.POST['mobile']
		email=request.POST['email']
		std_photo=request.FILES['photo']
		father_name=request.POST['father_name']
		job=request.POST['job']
		father_mobile=request.POST['father_mobile']
		father_aadhar=request.POST['father_aadhar']
		college_name=request.POST['college_name']
		qualifications=request.POST['qualifications']
		college_address=request.POST['college_address']
		course_name=request.POST['course_name']
		dob=request.POST['dob']
		batch_name=request.POST['batch_name']
		course_type=request.POST['course_type']
		fees=request.POST['fees']

		password=request.POST['sid']
		cpassword=request.POST['sid']
		admin_user=request.session['admin_email']
		

		try:
			student=Student_Registration.objects.get(sid=sid)
			FailedMsg="Student Id Alredy Registered"
			return render(request,'AdminArea/StudentAdmission.html',{'FailedMsg':FailedMsg})
		except:
			Student_Registration.objects.create(
												academic_year=academic_year,
												join_date=join_date,
												sid=sid,
												mname=mname,
												lname=lname,
												admission_num=admission_num,
												fname=fname,
												dob=dob,
												gender=gender,
												blood_group=blood_group,
												category=category,
												nationality=nationality,
												Cast=cast,
												aadhar=aadhar_num,
												permanent_address=permanent_address,
												present_address=present_address,
												city=city,
												pin=pin,
												mobile=mobile,
												email=email,
												photo=std_photo,
												father_name=father_name,
												father_mobile=father_mobile,
												father_job=job,
												father_aadhar=father_aadhar,
												college=college_name,
												qualification=qualifications,
												college_address=college_address,
												course_name=course_name,
												batch=batch_name,
												course_type=course_type,
												final_fees=fees,
												last_login="2021-01-01",
												password=password,
												cpassword=cpassword,
												admin_user_id=admin_user,
												)
			
			rec=[email,]
			subject="Admission Successefully"
			full_name=fname+" "+lname
			website="https://student.kalaveethi.com/"
			message=f" \n Dear {full_name},  \n \n Your SID Number is : {sid} \n Password is : {password} \n \n   Welcome to Kalaveethi!  Thank you, for being part of Kalaveethi family. Kalaveethi Institute Of Design Enhance your knowledge towards designing, personality development skill, will as sure you the best guidance in the field of {course_type}  and will give you an opportunity to meet with different skill expertise in your respective field. Wish you very all the best and hope to build better career. \n From, Kalaveethi Institute of Design. \n Visit Now :-\n {website} "                                
			email_from=settings.EMAIL_HOST_USER
			send_mail(subject,message,email_from,rec)
			print(message)

			# client = Client(settings.TWILIO['TWILIO_ACCOUNT_SID'],settings.TWILIO['TWILIO_AUTH_TOKEN'])
			# client.api.messages.create(to=f"+91{mobile}",from_=settings.TWILIO['TWILIO_NUMBER'],body=message)


			SuccessMsg="Student Registered Successefully"
			return render(request,'AdminArea/StudentAdmission.html',{'SuccessMsg':SuccessMsg})
	else:
		return render(request,'AdminArea/StudentAdmission.html')
def StudentList(request):
	StudentList=Student_Registration.objects.all()
	return render(request,'AdminArea/StudentList.html',{'StudentList':StudentList})
def EnrollStudentInquiry(request):
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
		admin_user=request.session['admin_email']
		print("admin user detaile")
		print(admin_user,date,full_name,dob,gender,address,mobile_number,whatsapp_number,email,edu_que,course,reference)
		try:
			Student_Inquiry.objects.create(inquiry_date=date,full_name=full_name,dob=dob,gender=gender,address=address,mobile=mobile_number,whatsapp=whatsapp_number,email=email,edu_que=edu_que,course=course,reference=reference,admin_user_id=admin_user)
			msg="Student Inquery Registered Successefully"
			subject="Thanks for visiting Kalaveethi Institute"
			website="https://kalaveethi.com/"
			booklate="https://kalaveethi.com/courses/kalaveethibook/"
			message=f"Hi {full_name}\n \nThank you for reaching out to Kalaveethi Institue Of Design. I’m Trupal, your admissions counselor. I look forward to working with you. Please feel free to text me here or my colleagues at  if you have any questions. \n \n \n Phone: +91 8160892915 \n Website: {website} \n \nDownload Booklate:{booklate}"
			
			# client = Client(settings.TWILIO['TWILIO_ACCOUNT_SID'],settings.TWILIO['TWILIO_AUTH_TOKEN'])
			# client.api.messages.create(to=f"+91{mobile_number}",from_=settings.TWILIO['TWILIO_NUMBER'],body=message)

			rec=[email,]
			email_from=settings.EMAIL_HOST_USER
			send_mail(subject,message,email_from,rec)

			SuccessMsg="Student Inquery Successefully Added"
			return render(request,'AdminArea/EnrollStudentInquiry.html',{'SuccessMsg':SuccessMsg})
		except Exception as e:
			FailedMsg="Student Inquery Added Failed!"
			return render(request,'AdminArea/EnrollStudentInquiry.html',{'FailedMsg':FailedMsg})
	else:
		return render(request,'AdminArea/EnrollStudentInquiry.html')
def InquiryLists(request):
	StudentInquiryList=Student_Inquiry.objects.all().order_by('-inquiry_date')
	return render(request,'AdminArea/InquiryLists.html',{'StudentInquiryList':StudentInquiryList})

def AddSubmitions(request):
	if request.method=="POST":
		course=request.POST['course']
		batch_name=request.POST['batch_name']
		subject=request.POST['subject']
		desc=request.POST['desc']
		date=request.POST['date']
		notice_file=request.FILES['file']
		admin_user=request.session['admin_email']
		try:
			Submitions_Registration.objects.create(course=course,batch=batch_name,subject=subject,desc=desc,last_date=date,submitions_file=notice_file,admin_user_id=admin_user)
			SuccessMsg="Submitions Added Successefully"
			return render(request,'AdminArea/AddSubmitions.html',{'SuccessMsg':SuccessMsg})
		except:
			FailedMsg="Submitions Added Failed"
			return render(request,'AdminArea/AddSubmitions.html',{'FailedMsg':FailedMsg})
	else:
		return render(request,'AdminArea/AddSubmitions.html')
def SubmitionsList(request):
	AllSubmitions=Submitions_Registration.objects.all().order_by('-last_date')
	return render(request,'AdminArea/SubmitionsList.html',{'AllSubmitions':AllSubmitions})
def test(request):
	return render(request,'AdminArea/test.html')


#update profile

def Student_profile(request,id):
    student_profile=Student_Registration.objects.get(pk=id)
    return render(request,'AdminArea/student_profile.html',{'student_profile':student_profile})

def stud_update(request,id):
	if request.method=="POST":
		academic_year=request.POST['academic_year']
		sid=request.POST['sid']
		join_date=request.POST['join_date']
		admission_num=request.POST['admission_num']
		fname=request.POST['fname']
		category=request.POST['category']
		aadhar_num=request.POST['aadhar_num']
		mname=request.POST['mname']
		gender=request.POST['gender']
		nationality=request.POST['nationality']
		lname=request.POST['lname']
		blood_group=request.POST['blood_group']
		cast=request.POST['cast']
		permanent_address=request.POST['permanent_address']
		present_address=request.POST['present_address']
		city=request.POST['city']
		pin=request.POST['pin']
		mobile=request.POST['mobile']
		email=request.POST['email']
		father_name=request.POST['father_name']
		job=request.POST['job']
		father_mobile=request.POST['father_mobile']
		father_aadhar=request.POST['father_aadhar']
		college_name=request.POST['college_name']
		qualifications=request.POST['qualifications']
		college_address=request.POST['college_address']
		course_name=request.POST['course_name']
		dob=request.POST['dob']
		batch_name=request.POST['batch_name']
		course_type=request.POST['course_type']
		fees=request.POST['fees']
		UpdateUser=Student_Registration.objects.get(pk=sid)
		UpdateUser.academic_year=academic_year
		UpdateUser.sid=sid 
		UpdateUser.join_date=join_date 
		UpdateUser.admission_num=admission_num 
		UpdateUser.fname=fname 
		UpdateUser.mname=mname 
		UpdateUser.lname=lname 
		UpdateUser.dob=dob 
		UpdateUser.gender=gender 
		UpdateUser.blood_group=blood_group 
		UpdateUser.nationality=nationality 
		UpdateUser.Cast=cast 
		UpdateUser.aadhar=aadhar_num 
		UpdateUser.permanent_address=permanent_address 
		UpdateUser.present_address=present_address 
		UpdateUser.city=city
		UpdateUser.pin=pin 
		UpdateUser.mobile=mobile 
		UpdateUser.email=email  
		UpdateUser.father_name=father_name 
		UpdateUser.father_mobile=father_mobile 
		UpdateUser.father_job=job 
		UpdateUser.father_aadhar=father_aadhar 
		UpdateUser.college=college_name 		 
		UpdateUser.qualification=qualifications 
		UpdateUser.college_address=college_address 
		UpdateUser.course_name=course_name, 
		UpdateUser.batch=batch_name 
		UpdateUser.course_type=course_type 
		UpdateUser.final_fees=fees
		try:
			if request.FILES['photo']:
				UpdateUser.photo=request.FILES['photo']
		except:
			pass
		UpdateUser.save() 	
		student_update=Student_Registration.objects.get(pk=id)
		return render(request,'AdminArea/student_profile.html',{'student_update':student_update})   
	else:
		student_update=Student_Registration.objects.get(pk=id)
		return render(request,'AdminArea/stud_update.html',{'student_update':student_update})
    	
    
def Student_Delete_profile(request,id):
    delete_profile= Student_Registration.objects.get(pk=id)
    delete_profile.delete()
    StudentList=Student_Registration.objects.all()
    return render(request,'AdminArea/StudentList.html',{'StudentList':StudentList})    

#Schedule
def AddClassSchedule(request):
	if request.method=="POST":
		class_for=request.POST['class_for']
		Batch=Student_Registration.objects.filter(course_type=class_for)
		result = []
		for i in Batch:
			result.append(i.batch)
		mylist = list(dict.fromkeys(result))
		return render(request,'AdminArea/AddClassSchedule.html',{'mylist':mylist})
	else:
		return render(request,'AdminArea/AddClassSchedule.html')

def AdminScheduleClass(request):
	if request.method=="POST":
		batch_for=request.POST['batch_for']
		from_date=request.POST['from_date']
		to_date=request.POST['to_date']
		from_time=request.POST['from_time']
		to_time=request.POST['to_time']
		subject=request.POST['subject']
		class_type=request.POST['class_type']
		organizer=request.POST['organizer']
		admin_user=request.session['admin_email']
		try:
			Student_Schedule.objects.create(from_date=from_date,to_date=to_date,from_time=from_time,to_time=to_time,subject=subject,classtype=class_type,batch_nm=batch_for,organizer=organizer,admin_user_id=admin_user)
			SuccessMsg="class Added Successefully"
			return render(request,'AdminArea/AddClassSchedule.html',{'SuccessMsg':SuccessMsg})
		except:
			FailedMsg="class Added Failed"
			return render(request,'AdminArea/AddClassSchedule.html',{'FailedMsg':FailedMsg})
	else:
		return render(request,'AdminArea/AddClassSchedule.html')

def ViewClassSchedule(request):
	AllClass=Student_Schedule.objects.all().order_by('-id')
	return render(request,'AdminArea/ViewClassSchedule.html',{'AllClass':AllClass})


# Events
def ScheduleEvent(request):
	if request.method=="POST":
		event_name=request.POST['event_name']
		event_place=request.POST['event_place']
		event_date=request.POST['event_date']
		event_time=request.POST['event_time']
		admin_user=request.session['admin_email']
		try:
			Event_Registration.objects.create(event_name=event_name,event_place=event_place,event_date=event_date,event_time=event_time,admin_user_id=admin_user)
			SuccessMsg="Event Registered Successefully"
			return render(request,'AdminArea/ScheduleEvent.html',{'SuccessMsg':SuccessMsg})
		except:
			FailedMsg="Event Registered Failed"
			return render(request,'AdminArea/ScheduleEvent.html',{'FailedMsg':FailedMsg})
	else:
		return render(request,'AdminArea/ScheduleEvent.html')
def EventList(request):
	AllEvents=Event_Registration.objects.all().order_by('-event_date')
	return render(request,'AdminArea/EventList.html',{'AllEvents':AllEvents})
# Notice
def NoticeList(request):
	AllNotice=Notice_Registration.objects.all().order_by('-notice_date')
	return render(request,'AdminArea/NoticeList.html',{'AllNotice':AllNotice})

def AddNotice(request):
	if request.method=="POST":
		notice_for=request.POST['notice_for']
		notice_sub=request.POST['notice_sub']
		notice_date=request.POST['notice_date']
		Notice_description=request.POST['Notice_description']
		notice_file=request.FILES['notice_file']
		admin_user=request.session['admin_email']
		try:
			Notice_Registration.objects.create(notice_for=notice_for,notice_sub=notice_sub,notice_date=notice_date,notice_desc=Notice_description,notice_file=notice_file,admin_user_id=admin_user)
			SuccessMsg="Notice Registered Successefully"
			return render(request,'AdminArea/AddNotice.html',{'SuccessMsg':SuccessMsg})
		except:
			FailedMsg="Notice Registered Failed"
			return render(request,'AdminArea/AddNotice.html',{'FailedMsg':FailedMsg})
	else:
		return render(request,'AdminArea/AddNotice.html')
#suggestions



def AllSuggestions(request):
	AllSuggestionsList=Student_Suggestion.objects.all()
	return render(request,'AdminArea/AllSuggestions.html',{'AllSuggestionsList':AllSuggestionsList})
def ViewNewSuggestions(request):
	NewSuggestionsList=Student_Suggestion.objects.all().order_by('-id')[0:3]
	return render(request,'AdminArea/ViewNewSuggestions.html',{'NewSuggestionsList':NewSuggestionsList})

# Fees
def FeesCollection(request):
	if request.method=="POST":
		sid=request.POST['sid']
		try:
			student = Student_Registration.objects.get(sid=sid)
			feesdetails = StudentFees.objects.filter(student_id=sid)
			return render(request,'AdminArea/StudentFeesDetails.html',{'student':student,'feesdetails':feesdetails})
		except:
			msg="Student Data not Found"
			return render(request,'AdminArea/FeesCollection.html',{'msg':msg})
	else:
		return render(request,'AdminArea/FeesCollection.html')
def AddFees(request):
	if request.method=="POST":
		sid=request.POST['sid']
		date=request.POST['date']
		amount=request.POST['amount']
		ins_num=request.POST['ins_num']
		ptype=request.POST['ptype']
		try:
			StudentFees.objects.create(student_id=sid,installment_no=ins_num,amount=amount,payment_date=date,payment_type=ptype)
			student = Student_Registration.objects.get(sid=sid)

			email=student.email
			mobile_number=student.mobile
			full_name=student.fname+" "+student.mname

			rec=[email,]
			subject="Fees installment paid successefully"
			website="https://kalaveethi.com/"
			message=f" \n Hello {full_name}, \n \n This is a confirmation that we have just received your secure payment. \n \n Thank you for the recent payment that you made on {date} for the amount of Rs: {amount}. This is a confirmation that amount has been successfully received.\n \n \n Kalaveethi Institue Of Design. \n {website} "
			email_from=settings.EMAIL_HOST_USER
			send_mail(subject,message,email_from,rec)
		

			# client = Client(settings.TWILIO['TWILIO_ACCOUNT_SID'],settings.TWILIO['TWILIO_AUTH_TOKEN'])
			# client.api.messages.create(to=f"+91{mobile_number}",from_=settings.TWILIO['TWILIO_NUMBER'],body=message)

			feesdetails = StudentFees.objects.filter(student_id=sid)
			SuccessMsg="Student Fees Paid Successefully"
			return render(request,'AdminArea/StudentFeesDetails.html',{'student':student,'feesdetails':feesdetails,'SuccessMsg':SuccessMsg})	
		except Exception as e:
			print(e)
			FailedMsg="Student Fees Paid Failed"
			student = Student_Registration.objects.get(sid=sid)
			feesdetails = StudentFees.objects.filter(student_id=sid)
			return render(request,'AdminArea/StudentFeesDetails.html',{'student':student,'feesdetails':feesdetails,'FailedMsg':FailedMsg})
	else:
		pass
def PrintInvoice(request):
	pk=request.POST['pk']
	InvoiceInfo=StudentFees.objects.get(pk=pk)
	student=Student_Registration.objects.get(sid=InvoiceInfo.student_id)
	return render(request,'AdminArea/PrintInvoice.html',{'InvoiceInfo':InvoiceInfo,'student':student})
#Certificate
def GenarateCertificate(request):
	if request.method=="POST":
		sid=request.POST['sid']
		try:
			student=Student_Certificate.objects.get(student_id=sid)
			FailedMsg="Student Certificate Alredy Genarated"
			return render(request,'AdminArea/GenarateCertificate.html',{'FailedMsg':FailedMsg})
		except:
			try:
				student = Student_Registration.objects.get(sid=sid)
				return render(request,'AdminArea/CertificateGrad.html',{'student':student})
			except Exception as e:
				FailedMsg="Student Data not Found"
				return render(request,'AdminArea/GenarateCertificate.html',{'FailedMsg':FailedMsg})
	else:
		return render(request,'AdminArea/GenarateCertificate.html')

def CertificateGrade(request):
	if request.method=="POST":
		sid=request.POST['sid']
		grade=request.POST['grade']
		date=request.POST['date']
		admin_user=request.session['admin_email']
		try:
			Student_Certificate.objects.create(admin_user_id=admin_user,student_id=sid,grade=grade,take_date=date)
			SuccessMsg="Certificate Successefully Genarated"
			student=Student_Registration.objects.get(sid=sid)
			return render(request,'AdminArea/CertificateGrad.html',{'student':student,'SuccessMsg':SuccessMsg})
		except:
			FailedMsg="Genarated Failed"
			student=Student_Registration.objects.get(sid=sid)
			return render(request,'AdminArea/CertificateGrad.html',{'student':student,'FailedMsg':FailedMsg})
	else:
		return render(request,'AdminArea/CertificateGrad.html')

def ViewAllCertificate(request):
	CertificateList=Student_Certificate.objects.all().order_by('-id')
	return render(request,'AdminArea/ViewAllCertificate.html',{'CertificateList':CertificateList})

# Leave

def ViewLeaveRequest(request):
	ApplyLeaveRequest=Student_Leave.objects.filter(status="Panding_Request")
	if request.method=='POST':
		status=request.POST['btn-status']
		leave_pk=request.POST['leave_pk']
		print(leave_pk)
		if status == "Approw":
			LeaveStudent=Student_Leave.objects.get(pk=leave_pk)
			LeaveStudent.status = "Approw"
			LeaveStudent.save()
			return render(request,'AdminArea/ViewLeaveRequest.html',{'ApplyLeaveRequest':ApplyLeaveRequest})
		else:
			LeaveStudent=Student_Leave.objects.get(pk=leave_pk)
			LeaveStudent.status = "Reject"
			LeaveStudent.save()
			return render(request,'AdminArea/ViewLeaveRequest.html',{'ApplyLeaveRequest':ApplyLeaveRequest})
	else:
		return render(request,'AdminArea/ViewLeaveRequest.html',{'ApplyLeaveRequest':ApplyLeaveRequest})

def ViewleaveList(request):
	AllLeavelist=Student_Leave.objects.all().order_by('-id')
	return render(request,'AdminArea/ViewleaveList.html',{'AllLeavelist':AllLeavelist})



def ShowStudentIdList(request):
	StudentList=Student_Registration.objects.all()
	return render(request,'AdminArea/ShowStudentIdList.html',{'StudentList':StudentList})
# Elibrary
def AddBook(request):
	if request.method=="POST":
		book_for=request.POST['book_for']
		book_title=request.POST['book_title']
		book_link=request.POST['book_link']
		book_photo=request.FILES['book_photo']
		book_pdf=request.FILES['book_pdf']
		admin_user=request.session['admin_email']
		try:
			ELibrary.objects.create(book_for=book_for,book_title=book_title,book_link=book_link,book_photo=book_photo,book_pdf=book_pdf,admin_user_id=admin_user)
			SuccessMsg="Book Added Successefully"
			return render(request,'AdminArea/AddBook.html',{'SuccessMsg':SuccessMsg})
		except:
			FailedMsg="Book Added Failed"
			return render(request,'AdminArea/AddBook.html',{'FailedMsg':FailedMsg})
	else:
		return render(request,'AdminArea/AddBook.html')
	
def BookList(request):
	AllBooks=ELibrary.objects.all()
	return render(request,'AdminArea/BookList.html',{'AllBooks':AllBooks})


def Addfacultysalary(request):
	if request.method=="POST":
		fid=request.POST['fid']
		try:
			faculty = Faculty_Registration.objects.get(faculty_id=fid)
			Salarysdetails = Faculty_Salary.objects.filter(faculty_user_id=fid)
			return render(request,'AdminArea/FacultySalaryDetails.html',{'faculty':faculty,'Salarysdetails':Salarysdetails})
		except:
			msg="Student Data not Found"
			return render(request,'AdminArea/Addfacultysalary.html',{'msg':msg})
	else:
		return render(request,'AdminArea/Addfacultysalary.html')	

def ShowFacultyIdList(request):
	FacultyList=Faculty_Registration.objects.all()
	return render(request,'AdminArea/ShowFacultyIdList.html',{'FacultyList':FacultyList})

def Viewfacultysalary(request):
	return render(request,'AdminArea/Viewfacultysalary.html')
def AddSalary(request):
	if request.method=="POST":
		fid=request.POST['fid']
		salary_year=request.POST['salary_year']
		salary_month=request.POST['salary_month']
		payment_date=request.POST['payment_date']
		from_date=request.POST['from_date']
		to_date=request.POST['to_date']
		amount=request.POST['amount']
		payment_type=request.POST['payment_type']
		admin_user=request.session['admin_email']
		try:
			Faculty_Salary.objects.create(faculty_user_id=fid,month=salary_month,amount=amount,payment_date=payment_date,payment_type=payment_type,from_date=from_date,year=salary_year,to_date=to_date,admin_user_id=admin_user)
			
			faculty = Faculty_Registration.objects.get(faculty_id=fid)
			Salarysdetails = Faculty_Salary.objects.filter(faculty_user_id=fid)
			
			email=faculty.email
			mobile_number=faculty.mobile
			full_name=faculty.first_name+" "+faculty.middel_name

			rec=[email,]
			subject="Fees installment paid successefully"
			website="https://kalaveethi.com/"
			message=f" \n Hello {full_name} \n \n This is a confirmation that we have just received your secure payment. \n \n Thank you for the recent payment that you made on {from_date} for the amount of Rs: {amount}. This is a confirmation that amount has been successfully received.\n \n \n Kalaveethi Institue Of Design. \n {website} "
			email_from=settings.EMAIL_HOST_USER
			send_mail(subject,message,email_from,rec)
			

			# client = Client(settings.TWILIO['TWILIO_ACCOUNT_SID'],settings.TWILIO['TWILIO_AUTH_TOKEN'])
			# client.api.messages.create(to=f"+91{mobile_number}",from_=settings.TWILIO['TWILIO_NUMBER'],body=message)

			
			SuccessMsg="Salary Paid Successefully"
			return render(request,'AdminArea/FacultySalaryDetails.html',{'faculty':faculty,'Salarysdetails':Salarysdetails,'SuccessMsg':SuccessMsg})	
		except Exception as e:
			print(e)
			FailedMsg="Salary Paid Failed"
			faculty = Faculty_Registration.objects.get(faculty_id=fid)
			Salarysdetails = Faculty_Salary.objects.filter(faculty_id=fid)
			return render(request,'AdminArea/FacultySalaryDetails.html',{'faculty':faculty,'Salarysdetails':Salarysdetails,'FailedMsg':FailedMsg})
	else:
		pass

def PrintSalaryInvoice(request):
	pk=request.POST['pk']
	InvoiceInfo=Faculty_Salary.objects.get(pk=pk)
	faculty=Faculty_Registration.objects.get(faculty_id=InvoiceInfo.faculty_user_id)
	return render(request,'AdminArea/PrintSalaryInvoice.html',{'InvoiceInfo':InvoiceInfo,'faculty':faculty})

def TakeStudentAttendence(request):
	if request.method=="POST":
		class_for=request.POST['class_for']
		Batch=Student_Registration.objects.filter(course_type=class_for)
		result = []
		for i in Batch:
			result.append(i.batch)
		mylist = list(dict.fromkeys(result))
		return render(request,'AdminArea/TakeStudentAttendence.html',{'mylist':mylist})
	else:
		return render(request,'AdminArea/TakeStudentAttendence.html')
def FillStudentAttendence(request):
	if request.method=="POST":
		batch_for=request.POST['batch_for']
		try:
			StudentList=Student_Registration.objects.filter(batch=batch_for)
			print(StudentList)
			return render(request,'AdminArea/FillStudentAttendence.html',{'StudentList':StudentList})
		except:
			return render(request,'AdminArea/TakeStudentAttendence.html')
	else:
		return render(request,'AdminArea/FillStudentAttendence.html')
def ViewStudentAttandence(request):
	return render(request,'AdminArea/ViewStudentAttandence.html')

def Addemployee(request):
    if request.method=="POST":
        admin_user=request.session['admin_email']
        fid=request.POST['fid']
        experience=request.POST['experience']
        join_date=request.POST['join_date']
        Deparment=request.POST['Deparment']
        que=request.POST['que']
        Salary=request.POST['Salary']
        fname=request.POST['fname']
        dob=request.POST['dob']
        category=request.POST['category']
        aadhar_num=request.POST['aadhar_num']
        mname=request.POST['mname']
        gender=request.POST['gender']
        nationality=request.POST['nationality']
        lname=request.POST['lname']
        blood_group=request.POST['blood_group']
        cast=request.POST['cast']
        permanent_address=request.POST['permanent_address']
        present_address=request.POST['present_address']
        city=request.POST['city']
        pin=request.POST['pin']
        mobile=request.POST['mobile']
        photo=request.FILES['photo']
        email=request.POST['email']
        bank_name=request.POST['bank_name']
        bank_holder=request.POST['bank_holder']
        ifsc_code=request.POST['ifsc_code']
        account_number=request.POST['account_number']
        password=request.POST['mobile']
        cpassword=request.POST['mobile']
        try:
            Faculty_Registration.objects.create(admin_user_id=admin_user,faculty_id=fid,joing_date=join_date,category=category,department_catagory=Deparment,qulification=que,total_Experiance=experience,first_name=fname,middel_name=mname,last_name=lname,birth_date=dob,gender=gender,blood_group=blood_group,nationality=nationality,Cast=cast,aadhar=aadhar_num,salary=Salary,permanent_address=permanent_address,present_address=present_address,city=city,pin=pin,mobile=mobile,email=email,photo=photo,holder_name=bank_holder,ifsc=ifsc_code,bank_name=bank_name,account_no=account_number,password=password,cpassword=cpassword)
            SuccessMsg="Add Faculty Successefully"

            rec=[email,]
            subject="Joining Successefully"
            full_name=fname+" "+lname
            website="https://student.kalaveethi.com/"
            message=f" \n Dear {full_name},  \n \n Your SID Number is : {fid} \n Password is : {password} \n \n   Welcome to Kalaveethi!  Thank you, for being part of Kalaveethi family. Kalaveethi Institute Of Design Enhance your knowledge towards designing, personality development skill, will as sure you the best guidance in the field of  and will give you an opportunity to meet with different skill expertise in your respective field. Wish you very all the best and hope to build better career. \n From, Kalaveethi Institute of Design. \n Visit Now :-\n {website} "
            email_from=settings.EMAIL_HOST_USER
            send_mail(subject,message,email_from,rec)
			
			# client = Client(settings.TWILIO['TWILIO_ACCOUNT_SID'],settings.TWILIO['TWILIO_AUTH_TOKEN'])
			# client.api.messages.create(to=f"+91{mobile}",from_=settings.TWILIO['TWILIO_NUMBER'],body=message)


            return render(request,'AdminArea/Addemployee.html',{'SuccessMsg':SuccessMsg})
        except Exception as e:
            print("Faculty")
            print(e)
            FailedMsg="Add Faculty Failed"
            return render(request,'AdminArea/Addemployee.html',{'FailedMsg':FailedMsg})
    else:
        return render(request,'AdminArea/Addemployee.html')

  
def Viewemployee(request):
    Faculty=Faculty_Registration.objects.all()
    return render(request,'AdminArea/Viewemployeedetail.html',{'Faculty':Faculty})	


def FacultyLeaveRequest(request):
	ApplyLeaveRequest=Faculty_Leave.objects.filter(status="Panding_Request")
	if request.method=='POST':
		status=request.POST['btn-status']
		leave_pk=request.POST['leave_pk']
		print(leave_pk)
		if status == "Approw":
			LeaveStudent=Faculty_Leave.objects.get(pk=leave_pk)
			LeaveStudent.status = "Approw"
			LeaveStudent.save()
			return render(request,'AdminArea/FacultyLeaveRequest.html',{'ApplyLeaveRequest':ApplyLeaveRequest})
		else:
			LeaveStudent=Student_Leave.objects.get(pk=leave_pk)
			LeaveStudent.status = "Reject"
			LeaveStudent.save()
			return render(request,'AdminArea/FacultyLeaveRequest.html',{'ApplyLeaveRequest':ApplyLeaveRequest})
	else:
		return render(request,'AdminArea/FacultyLeaveRequest.html',{'ApplyLeaveRequest':ApplyLeaveRequest})

def FacultyLeaveList(request):
	AllLeavelist=Faculty_Leave.objects.all()
	return render(request,'AdminArea/FacultyLeaveList.html',{'AllLeavelist':AllLeavelist})

def Student_profile(request,id):
    UpdateUser=Student_Registration.objects.get(pk=id)
    return render(request,'AdminArea/student_profile.html',{'UpdateUser':UpdateUser})

def stud_update(request,id):
	if request.method=="POST":
		academic_year=request.POST['academic_year']
		sid=request.POST['sid']
		join_date=request.POST['join_date']
		admission_num=request.POST['admission_num']
		fname=request.POST['fname']
		category=request.POST['category']
		aadhar_num=request.POST['aadhar_num']
		mname=request.POST['mname']
		gender=request.POST['gender']
		nationality=request.POST['nationality']
		lname=request.POST['lname']
		blood_group=request.POST['blood_group']
		cast=request.POST['cast']
		permanent_address=request.POST['permanent_address']
		present_address=request.POST['present_address']
		city=request.POST['city']
		pin=request.POST['pin']
		mobile=request.POST['mobile']
		email=request.POST['email']
		father_name=request.POST['father_name']
		job=request.POST['job']
		father_mobile=request.POST['father_mobile']
		father_aadhar=request.POST['father_aadhar']
		college_name=request.POST['college_name']
		qualifications=request.POST['qualifications']
		college_address=request.POST['college_address']
		course_name=request.POST['course_name']
		dob=request.POST['dob']
		batch_name=request.POST['batch_name']
		course_type=request.POST['course_type']
		fees=request.POST['fees']
		UpdateUser=Student_Registration.objects.get(pk=id)
		UpdateUser.academic_year=academic_year
		UpdateUser.sid=sid 
		UpdateUser.join_date=join_date 
		UpdateUser.admission_num=admission_num 
		UpdateUser.fname=fname 
		UpdateUser.mname=mname 
		UpdateUser.lname=lname 
		UpdateUser.dob=dob 
		UpdateUser.gender=gender 
		UpdateUser.blood_group=blood_group 
		UpdateUser.nationality=nationality 
		UpdateUser.Cast=cast 
		UpdateUser.aadhar=aadhar_num 
		UpdateUser.permanent_address=permanent_address 
		UpdateUser.present_address=present_address 
		UpdateUser.city=city
		UpdateUser.pin=pin 
		UpdateUser.mobile=mobile 
		UpdateUser.email=email  
		UpdateUser.father_name=father_name 
		UpdateUser.father_mobile=father_mobile 
		UpdateUser.father_job=job 
		UpdateUser.father_aadhar=father_aadhar 
		UpdateUser.college=college_name 		 
		UpdateUser.qualification=qualifications 
		UpdateUser.college_address=college_address 
		UpdateUser.course_name=course_name, 
		UpdateUser.batch=batch_name 
		UpdateUser.course_type=course_type 
		UpdateUser.final_fees=fees
		try:
			if request.FILES['photo']:
				UpdateUser.photo=request.FILES['photo']
		except:
			pass
		UpdateUser.save()
		UpdateUser=Student_Registration.objects.get(pk=id)
		return render(request,'AdminArea/student_profile.html',{'UpdateUser':UpdateUser})   
	else:
		student_update=Student_Registration.objects.get(pk=id)
		return render(request,'AdminArea/stud_update.html',{'student_update':student_update})
    	
    
def Student_Delete_profile(request,id):
    delete_profile= Student_Registration.objects.get(pk=id)
    delete_profile.delete()
    StudentList=Student_Registration.objects.all()
    return render(request,'AdminArea/StudentList.html',{'StudentList':StudentList})

def facultyviewprofile(request,slug):
	faculty_profile=Faculty_Registration.objects.get(pk=slug)
	return render(request,'AdminArea/facultyviewprofile.html',{'faculty_profile':faculty_profile})

def faculty_profile_update(request,slug):
	faculty=Faculty_Registration.objects.get(pk=slug)
	if request.method=="POST":
		Deparment=request.POST['Deparment']
		experience=request.POST['experience']
		join_date=request.POST['join_date']
		que=request.POST['que']
		Salary=request.POST['Salary']
		fname=request.POST['fname']
		dob=request.POST['dob']
		category=request.POST['category']
		aadhar_num=request.POST['aadhar_num']
		mname=request.POST['mname']
		gender=request.POST['gender']
		nationality=request.POST['nationality']
		lname=request.POST['lname']
		blood_group=request.POST['blood_group']
		Cast=request.POST['Cast']
		permanent_address=request.POST['permanent_address']
		present_address=request.POST['present_address']
		city=request.POST['city']
		pin=request.POST['pin']
		mobile=request.POST['mobile']
		email=request.POST['email']
		bank_name=request.POST['bank_name']
		bank_holder=request.POST['bank_holder']
		ifsc_code=request.POST['ifsc_code']
		account_number=request.POST['account_number']
		faculty_profile=Faculty_Registration.objects.get(pk=slug)
		faculty_profile.department_catagory=Deparment
		faculty_profile.total_Experiance=experience
		faculty_profile.joing_date=join_date
		faculty_profile.qulification=que
		faculty_profile.salary=Salary
		faculty_profile.first_name=fname
		faculty_profile.birth_date=dob
		faculty_profile.category=category
		faculty_profile.aadhar=aadhar_num
		faculty_profile.middel_name=mname
		faculty_profile.gender=gender
		faculty_profile.nationality=nationality
		faculty_profile.last_name=lname
		faculty_profile.blood_group=blood_group
		faculty_profile.Cast=Cast
		faculty_profile.permanent_address=permanent_address
		faculty_profile.present_address=present_address
		faculty_profile.city=city
		faculty_profile.pin=pin
		faculty_profile.mobile=mobile
		faculty_profile.email=email
		faculty_profile.bank_name=bank_name
		faculty_profile.holder_name=bank_holder
		faculty_profile.ifsc=ifsc_code
		faculty_profile.account_no=account_number
		try:
			if request.FILES['photo']:
				faculty_update.photo=request.FILES['photo']
		except Exception as e:
			print(e)
			pass
		faculty_profile.save()
		return render(request,'AdminArea/facultyviewprofile.html',{'faculty_profile':faculty_profile})
	else:
		faculty=Faculty_Registration.objects.get(pk=slug)
		return render(request,'AdminArea/faculty_profile_update.html',{'faculty':faculty})

	


def deleteprofile(request,slug):
	delete_profile= Faculty_Registration.objects.get(pk=slug)
	delete_profile.delete()
	FacultyList=Faculty_Registration.objects.all()
	return render(request,'AdminArea/Viewemployeedetail.html',{'FacultyList':FacultyList})
