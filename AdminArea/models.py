from django.db import models
from datetime import datetime 
from django.utils import timezone 
# Admin Area

class Admin_Registration(models.Model):
	fname=models.CharField(max_length=100)
	mname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	dob=models.DateField(max_length=8)
	GENDER_CHOICES = (("male",'male'),("female",'female'),)
	gender=models.CharField(max_length=10,choices=GENDER_CHOICES,default="")
	aadhar=models.CharField(max_length=12)

	address=models.TextField()
	city=models.CharField(max_length=100)
	pin=models.CharField(max_length=10)
	mobile=models.CharField(max_length=10)
	photo=models.ImageField(upload_to='StudentPhotos/',default="")
	
	status=models.CharField(max_length=100,default="activated")
	last_login=models.CharField(max_length=100,default="")
	email=models.CharField(max_length=100,primary_key=True)
	password=models.CharField(max_length=100,default="")
	cpassword=models.CharField(max_length=100,default="")
	sreenpin=models.CharField(max_length=100,default="")
	csreenpin=models.CharField(max_length=100,default="")

	def __str__(self):
		return self.mname+" "+self.email

class Student_Registration(models.Model):
	admin_user=models.ForeignKey(Admin_Registration,on_delete=models.CASCADE,null=True,blank=True)
	YEAR_CHOICES = (("2019-20",'2019-20'),("2020-21",'2020-21'),("2021-22",'2021-22'),)
	academic_year=models.CharField(max_length=20,choices=YEAR_CHOICES,default="")
	join_date=models.DateField(auto_now=True, blank=True)
	sid=models.CharField(primary_key=True,max_length=30)
	admission_num=models.CharField(max_length=30)

	fname=models.CharField(max_length=100)	
	mname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	dob=models.DateField(max_length=8)
	GENDER_CHOICES = (("male",'male'),("female",'female'),)
	gender=models.CharField(max_length=10,choices=GENDER_CHOICES,default="")
	BLOOD_GROUP_CHOICES = (("A+",'A+'),("A-",'A-'),("B+",'B+'),("B-",'B-'),("O-",'O-'),("O+",'O+'),("AB+",'AB+'),("AB-",'AB-'),)
	blood_group = models.CharField(max_length=20,choices=BLOOD_GROUP_CHOICES,default="")
	CATEGORY_CHOICES = (("General",'General'),("MCB",'MCB'),("OBC",'OBC'),("SC",'SC'),("ST",'ST'),("Other",'Other'),)
	category=models.CharField(max_length=50,choices=CATEGORY_CHOICES,default="")
	nationality=models.CharField(max_length=100)
	CAST_CHOICES = (("Hindus",'Hindus'),("Muslims",'Muslims'),("Christians",'Christians'),("Sikhs",'Sikhs'),("Jains",'Jains'),("Other",'Other'),)
	Cast=models.CharField(max_length=50,choices=CAST_CHOICES,default="")
	aadhar=models.CharField(max_length=12)
	permanent_address=models.TextField()
	present_address=models.TextField()
	city=models.CharField(max_length=100)
	pin=models.CharField(max_length=10)
	mobile=models.CharField(max_length=12)
	email=models.CharField(max_length=100)
	photo=models.ImageField(upload_to='StudentPhotos/',default="")

	father_name=models.CharField(max_length=100)
	father_mobile=models.CharField(max_length=12)
	father_job=models.CharField(max_length=100)
	father_aadhar=models.CharField(max_length=12)

	college=models.CharField(max_length=100)
	qualification=models.CharField(max_length=100)
	college_address=models.TextField()
	
	course_name=models.CharField(max_length=100)
	batch=models.CharField(max_length=100)
	COURSE_TYPE_CHOICES = (("fashion",'fashion'),("graphics",'graphics'),("fineart",'fineart'),("textile",'textile'),("jwellery",'jwellery'),("others",'others'),)
	course_type=models.CharField(max_length=200,choices=COURSE_TYPE_CHOICES,default="")
	
	status=models.CharField(max_length=100,default="activated")
	last_login=models.DateField(default=timezone.now)
	password=models.CharField(max_length=100,default="")
	cpassword=models.CharField(max_length=100,default="")

	final_fees=models.PositiveIntegerField(default=0)
	remaining_fees=models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.sid+" "+self.fname+" "+self.course_type

class Faculty_Registration(models.Model):
	admin_user=models.ForeignKey(Admin_Registration,blank=True,on_delete=models.CASCADE,null=True)
	faculty_id=models.CharField(primary_key=True,max_length=100)
	joing_date= models.DateField(max_length=8)
	COURSE_TYPE_CHOICES = (("fashion",'fashion'),("graphics",'graphics'),("fineart",'fineart'),("textile",'textile'),("jwellery",'jwellery'),("others",'others'),)
	department_catagory=models.CharField(max_length=200,choices=COURSE_TYPE_CHOICES,default="")
	qulification = models.CharField(max_length=80)
	total_Experiance=models.CharField(max_length=80)

	# personal details

	first_name= models.CharField(max_length=50)
	middel_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	birth_date = models.DateField(max_length=8)
	GENDER_CHOICES = (("male",'male'),("female",'female'),)
	gender=models.CharField(max_length=10,choices=GENDER_CHOICES,default="")
	BLOOD_GROUP_CHOICES = (("A+",'A+'),("A-",'A-'),("B+",'B+'),("B-",'B-'),("O-",'O-'),("O+",'O+'),("AB+",'AB+'),("AB-",'AB-'),)
	blood_group = models.CharField(max_length=20,choices=BLOOD_GROUP_CHOICES,default="")
	CATEGORY_CHOICES = (("General",'General'),("MCB",'MCB'),("OBC",'OBC'),("SC",'SC'),("ST",'ST'),("Other",'Other'),)
	category=models.CharField(max_length=50,choices=CATEGORY_CHOICES,default="")
	nationality=models.CharField(max_length=100)
	CAST_CHOICES = (("Hindus",'Hindus'),("Muslims",'Muslims'),("Christians",'Christians'),("Sikhs",'Sikhs'),("Jains",'Jains'),("Other",'Other'),)
	Cast=models.CharField(max_length=50,choices=CAST_CHOICES,default="")
	aadhar=models.CharField(max_length=12)
	salary = models.CharField(max_length=50)

	# contect_details

	permanent_address=models.TextField()
	present_address=models.TextField()
	city=models.CharField(max_length=100,default="")
	pin=models.CharField(max_length=10,default="")
	mobile=models.CharField(max_length=12,default="")
	email=models.CharField(max_length=30,default="")
	photo=models.ImageField(upload_to='FacultyPhotos/',default="")
	
    # bank_details

	holder_name=models.CharField(max_length=100,default="")
	ifsc=models.CharField(max_length=100,default="")
	bank_name = models.CharField(max_length=50,default="")
	account_no= models.CharField(max_length=50,default="")

	
	status=models.CharField(max_length=100,default="activated")
	last_login=models.DateField(default=timezone.now)
	password=models.CharField(max_length=100,default="")
	cpassword=models.CharField(max_length=100,default="")

	def __str__(self):
		return self.faculty_id


class Student_Inquiry(models.Model):
	admin_user=models.ForeignKey(Admin_Registration,on_delete=models.CASCADE,null=True,blank=True)
	faculty_user=models.ForeignKey(Faculty_Registration,blank=True,on_delete=models.CASCADE,null=True)
	inquiry_num=models.AutoField(primary_key=True)
	inquiry_date=models.DateField(max_length=8)
	full_name=models.CharField(max_length=100)
	dob=models.DateField(max_length=8)
	CHOICES = (("male",'male'),("female",'female'),)
	gender=models.CharField(max_length=200,choices=CHOICES,default="")
	address=models.TextField()
	mobile=models.CharField(max_length=100)
	whatsapp=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	edu_que=models.CharField(max_length=100)
	COURSE_CHOICES = (("fashion",'fashion'),("graphics",'graphics'),("fineart",'fineart'),("textile",'textile'),("jwellery",'jwellery'),("Art & Cart",'Art & Cart'),("PhotoShop",'PhotoShop'),("Corel Drew",'Corel Drew'),("Illustrator",'Illustrator'),("Motifs Design",'Motifs Design'),)
	course=models.CharField(max_length=200,choices=COURSE_CHOICES,default="")
	REFERENCE_CHOICES = (("Social Media",'Social Media'),("Google",'Google'),("News Paper",'News Paper'),("Others",'Others'),)
	reference=models.CharField(max_length=200,choices=REFERENCE_CHOICES,default="")
	

	def __str__(self):
		return self.full_name


class institute_Detaile(models.Model):
	ins_name=models.CharField(max_length=100,default="Enter Institute Name")
	ins_id=models.CharField(max_length=100,default="Enter Institute Code")
	ins_address=models.TextField(default="Enter Address")
	ins_fb=models.URLField(max_length = 200,blank = True,default="https://www.Instagram.com/")
	ins_insta=models.URLField(max_length = 200,blank = True,default="https://www.facebook.com/")
	ins_google=models.URLField(max_length = 200,blank = True,default="https://www.google.com/")
	ins_phone=models.CharField(max_length=12,default="Enter Institution Phone Number")
	ins_email=models.CharField(max_length=100,default="Enter Institution Email")
	ins_web=models.URLField(max_length = 200,blank = True,default="Enter Web Site URL")
	logo=models.FileField(upload_to='InstituteLogo/',default="")

	def __str__(self ):
		return self.ins_name

class Event_Registration(models.Model):
	admin_user=models.ForeignKey(Admin_Registration,on_delete=models.CASCADE,null=True,blank=True)
	event_name=models.CharField(max_length=100)
	event_place=models.CharField(max_length=100,default="")
	event_date=models.DateField(max_length=8)
	event_time=models.TimeField(auto_now=False, auto_now_add=False)

	def __str__(self ):
		return self.event_name+" "+self.event_place

class Notice_Registration(models.Model):
	admin_user=models.ForeignKey(Admin_Registration,on_delete=models.CASCADE,null=True,blank=True)
	COURSE_CHOICES = (("fashion",'fashion'),("graphics",'graphics'),("fineArt",'fineArt'),("fextile",'fextile'),("jwellery",'jwellery'),("All",'All'))
	notice_for=models.CharField(max_length=200,choices=COURSE_CHOICES,default="all")
	notice_sub=models.CharField(max_length=100)
	notice_date=models.DateField(max_length=8)
	notice_desc=models.TextField()
	notice_file=models.FileField(upload_to='NoticeFiles/',default="")
	notice_status=models.CharField(max_length=100,default="active")

	def __str__(self ):
		return self.notice_sub+" "+self.notice_for

class StudentFees(models.Model):
	admin_user=models.ForeignKey(Admin_Registration,on_delete=models.CASCADE,null=True,blank=True)
	student=models.ForeignKey(Student_Registration,on_delete=models.CASCADE,null=True,blank=True)
	installment_no=models.PositiveIntegerField()
	amount=models.PositiveIntegerField()
	payment_date=models.DateField(max_length=8)
	payment_type=models.CharField(max_length=100)
	recipt_no=models.AutoField(primary_key=True)
	fees_invoice=models.FileField(upload_to='FeesInvoice/',default="")

	def __str__(self ):
		return self.student_id

class Submitions_Registration(models.Model):
	faculty_user=models.ForeignKey(Faculty_Registration,blank=True,on_delete=models.CASCADE,null=True)
	admin_user=models.ForeignKey(Admin_Registration,on_delete=models.CASCADE,null=True,blank=True)
	COURSE_CHOICES = (("Fashion",'Fashion'),("Graphics",'Graphics'),("FineArt",'FineArt'),("Textile",'Textile'),("Jwellery",'Jwellery'),("All",'All'))
	course=models.CharField(max_length=200,choices=COURSE_CHOICES,default="all")
	batch=models.CharField(max_length=100)
	subject=models.CharField(max_length=100)
	desc=models.TextField()
	last_date=models.DateField(max_length=8)
	submitions_file=models.FileField(upload_to='SubmitionsFiles/',default="")
	

	def __str__(self ):
		return self.course+" "+self.subject

class Student_Leave(models.Model):
	student=models.ForeignKey(Student_Registration,on_delete=models.CASCADE,null=True,blank=True)
	full_Name=models.CharField(max_length=100)
	course=models.CharField(max_length=100)
	from_date=models.DateField(max_length=8)
	to_date=models.DateField(max_length=8)
	LEAVE_CHOICES = (("Sick_Leave",'Sick Leave ( 1 to 2 days )'),("Extended_Sick",'Extended Sick Leave'),("Emergency_Leave",'Emergency Leave'),("Long_Leave",'Long Leave'),("Others",'Others'),)
	Leave_catagory=models.CharField(max_length=200,choices=LEAVE_CHOICES,default="")
	Leave_reason=models.CharField(max_length=100)
	Leave_day=models.CharField(max_length=100)
	status=models.CharField(max_length=100,default="Panding_Request")

	def __str__(self ):
		return self.full_Name+" "+self.Leave_reason

class Student_Suggestion(models.Model):
	student=models.ForeignKey(Student_Registration,on_delete=models.CASCADE,null=True,blank=True)
	Student_Suggestion=models.TextField()
	suggestion_date=models.DateField(auto_now=True, blank=True)

	def __str__(self ):
		return self.student.sid

class ELibrary(models.Model):
	faculty_user=models.ForeignKey(Faculty_Registration,blank=True,on_delete=models.CASCADE,null=True)
	admin_user=models.ForeignKey(Admin_Registration,on_delete=models.CASCADE,null=True,blank=True)
	COURSE_CHOICES = (("Fashion",'Fashion'),("Graphics",'Graphics'),("FineArt",'FineArt'),("Textile",'Textile'),("Jwellery",'Jwellery'),("All",'All'))
	book_for=models.CharField(max_length=200,choices=COURSE_CHOICES,default="all")
	book_title=models.CharField(max_length=100)
	book_link=models.URLField(max_length = 200,blank = True,)
	book_photo=models.FileField(upload_to='ELibraryBookPhoto/',default="")
	book_pdf=models.FileField(upload_to='ELibraryBookPDF/',default="")

	def __str__(self ):
		return self.book_title

class Faculty_Leave(models.Model):
	faculty_user=models.ForeignKey(Faculty_Registration,on_delete=models.CASCADE,null=True,blank=True)
	full_Name=models.CharField(max_length=100)
	department=models.CharField(max_length=100)
	from_date=models.DateField(max_length=8)
	to_date=models.DateField(max_length=8)
	LEAVE_CHOICES = (("Sick_Leave",'Sick Leave ( 1 to 2 days )'),("Extended_Sick",'Extended Sick Leave'),("Emergency_Leave",'Emergency Leave'),("Long_Leave",'Long Leave'),("Others",'Others'),)
	Leave_catagory=models.CharField(max_length=200,choices=LEAVE_CHOICES,default="")
	Leave_reason=models.CharField(max_length=100)
	Leave_day=models.CharField(max_length=100)
	status=models.CharField(max_length=100,default="Panding_Request")

	def __str__(self ):
		return self.full_Name+" "+self.faculty_user_id

class Student_Schedule(models.Model):
	faculty_user=models.ForeignKey(Faculty_Registration,blank=True,on_delete=models.CASCADE,null=True)
	admin_user=models.ForeignKey(Admin_Registration,on_delete=models.CASCADE,null=True,blank=True)
	from_date=models.DateField(max_length=8,default="")
	to_date=models.DateField(max_length=8,default="")
	from_time=models.TimeField(max_length=8,default="")
	to_time=models.TimeField(max_length=8,default="")
	subject=models.CharField(max_length=100,default="")
	CLASS_CHOICES = (("lab",'lab'),("skeching",'skeching'),("theory",'theory'),("CAD",'CAD'))
	classtype=models.CharField(max_length=200,choices=CLASS_CHOICES,default="")
	batch_nm=models.CharField(max_length=100,default="")
	organizer=models.CharField(max_length=100,default="")
	

	def __str__(self ):
		return self.batch_nm+" "+self.organizer

class Faculty_Salary(models.Model):
	admin_user=models.ForeignKey(Admin_Registration,on_delete=models.CASCADE,null=True,blank=True)
	faculty_user=models.ForeignKey(Faculty_Registration,on_delete=models.CASCADE,null=True,blank=True)
	MONTH_CHOICES = (("January",'January'),("February",'February'),("March",'March'),("April",'April'),("May",'May'),("June",'June'),("July",'July'),("August",'August'),("September",'September'),("October",'October'),("November",'November'),("December",'December'),)
	month=models.CharField(max_length=200,choices=MONTH_CHOICES,default="")
	amount=models.PositiveIntegerField()
	payment_date=models.DateField(max_length=8)
	payment_type=models.CharField(max_length=100)
	from_date=models.DateField(max_length=8,default="")
	YEAR_CHOICES = (("2021",'2021'),("2022",'2022'),("2022",'2022'),)
	year=models.CharField(max_length=200,choices=YEAR_CHOICES,default="")
	to_date=models.DateField(max_length=8,default="")
	recipt_no=models.AutoField(primary_key=True)
	salary_invoice=models.FileField(upload_to='SalaryInvoice/',default="")

	def __str__(self ):
		return self.faculty_user_id

class Student_Attendence(models.Model):
	attendence_choice = (
		("A","Absent"),
		("P","Present")
		)

	admin_user=models.ForeignKey(Admin_Registration,on_delete=models.CASCADE,null=True,blank=True)
	faculty_user=models.ForeignKey(Faculty_Registration,on_delete=models.CASCADE,null=True,blank=True)
	student=models.ForeignKey(Student_Registration,on_delete=models.CASCADE,null=True,blank=True)
	take_date=models.DateField(max_length=8,default="")
	batch=models.CharField(max_length=100)
	ap=models.CharField(default="A",choices=attendence_choice,max_length=1)

	def __str__(self ):
		return self.student_id
		
class Student_Certificate(models.Model):
	admin_user=models.ForeignKey(Admin_Registration,on_delete=models.CASCADE,null=True,blank=True)
	student=models.ForeignKey(Student_Registration,on_delete=models.CASCADE,null=True,blank=True)
	grade=models.CharField(max_length=10,default="")
	take_date=models.DateField(max_length=8,default="")
	certificate_pdf=models.FileField(upload_to='StudenCertificate/',default="")
	
	def __str__(self ):
		return self.student_id









                                       