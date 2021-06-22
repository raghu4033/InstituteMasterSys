from django.urls import path
from . import views
AdminArea = "AdminArea"
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index,name='index'),
    path('AdminLogin/',views.admin_login,name='admin_login'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('AdminForgotPassword/',views.AdminForgotPassword,name='AdminForgotPassword'),
    path('AdminOTP/',views.AdminOTP,name='AdminOTP'),
    path('AdminNewPassword/',views.AdminNewPassword,name='AdminNewPassword'),

    path('AdminProfile/',views.AdminProfile,name='AdminProfile'),
    path('AdminChangePassword/',views.AdminChangePassword,name='AdminChangePassword'),
    path('AdminLockScreen/',views.AdminLockScreen,name='AdminLockScreen'),
    path('AdminDashboard/',views.AdminDashboard,name='AdminDashboard'),

    path('Users/',views.Users,name='Users'),
    path('InstituteDetailes/',views.InstituteDetailes,name='InstituteDetailes'),
    path('AddAdminUser/',views.AddAdminUser,name='AddAdminUser'),

    path('StudentAdmission/',views.StudentAdmission,name='StudentAdmission'),
    path('StudentList/',views.StudentList,name='StudentList'),

    path('EnrollStudentInquiry/',views.EnrollStudentInquiry,name='EnrollStudentInquiry'),
    path('InquiryLists/',views.InquiryLists,name='InquiryLists'),

    path('AddSubmitions/',views.AddSubmitions,name='AddSubmitions'),
    path('SubmitionsList/',views.SubmitionsList,name='SubmitionsList'),
    
    path('Student_profile/<int:id>',views.Student_profile,name='Student_profile'),
    path('stud_update/<int:id>',views.stud_update,name='stud_update'),
    path('Student_Delete_profile/<int:id>',views.Student_Delete_profile,name='Student_Delete_profile'),

    path('ScheduleEvent/',views.ScheduleEvent,name='ScheduleEvent'),    
    path('EventList/',views.EventList,name='EventList'),

    path('AddNotice/',views.AddNotice,name='AddNotice'),
    path('NoticeList/',views.NoticeList,name='NoticeList'),

    path('FacultyLeaveRequest/',views.FacultyLeaveRequest,name='FacultyLeaveRequest'),
    path('FacultyLeaveList/',views.FacultyLeaveList,name='FacultyLeaveList'),

    path('ShowStudentIdList/',views.ShowStudentIdList,name='ShowStudentIdList'),

    path('ViewNewSuggestions/',views.ViewNewSuggestions,name='ViewNewSuggestions'),
    path('AllSuggestions/',views.AllSuggestions,name='AllSuggestions'),

    path('FeesCollection/',views.FeesCollection,name='FeesCollection'),

    path('ViewLeaveRequest',views.ViewLeaveRequest,name='ViewLeaveRequest'),
    path('ViewleaveList',views.ViewleaveList,name='ViewleaveList'),

    path('GenarateCertificate/',views.GenarateCertificate,name='GenarateCertificate'),
    path('ViewAllCertificate/',views.ViewAllCertificate,name='ViewAllCertificate'),

    path('AddFees/',views.AddFees,name='AddFees'),
    path('PrintInvoice/',views.PrintInvoice,name='PrintInvoice'),

    path('AddBook/',views.AddBook,name='AddBook'),
    path('BookList/',views.BookList,name='BookList'),

    path('AddClassSchedule/',views.AddClassSchedule,name='AddClassSchedule'),
    path('ViewClassSchedule/',views.ViewClassSchedule,name='ViewClassSchedule'),

    path('AdminScheduleClass/',views.AdminScheduleClass,name='AdminScheduleClass'),

    path('Addfacultysalary/',views.Addfacultysalary,name='Addfacultysalary'),
    path('Viewfacultysalary/',views.Viewfacultysalary,name='Viewfacultysalary'),
    path('AddSalary',views.AddSalary,name='AddSalary'),

    path('ShowFacultyIdList/',views.ShowFacultyIdList,name='ShowFacultyIdList'),
    path('PrintSalaryInvoice/',views.PrintSalaryInvoice,name='PrintSalaryInvoice'),

    path('TakeStudentAttendence/',views.TakeStudentAttendence,name='TakeStudentAttendence'),
    path('ViewStudentAttandence/',views.ViewStudentAttandence,name='ViewStudentAttandence'),

    path('ViewStudentAttandenceList/',views.ViewStudentAttandenceList,name='ViewStudentAttandenceList'),

    path('Addemployee/',views.Addemployee,name='Addemployee'),
    path('Viewemployee/',views.Viewemployee,name='Viewemployee'),
     
    path('FillStudentAttendence/',views.FillStudentAttendence,name='FillStudentAttendence'),   
    path('SubmitStudentAttendence/', views.SubmitStudentAttendence, name='SubmitStudentAttendence'),
    path('test/',views.test,name='test'),

    path('CertificateGrade/',views.CertificateGrade,name='CertificateGrade'),

    path('UserStatus/',views.UserStatus,name='UserStatus'),

    path('Student_profile/<int:id>',views.Student_profile,name='Student_profile'),
    path('stud_update/<int:id>',views.stud_update,name='stud_update'),
    path('Student_Delete_profile/<int:id>',views.Student_Delete_profile,name='Student_Delete_profile'),

    path('facultyviewprofile/<slug:slug>',views.facultyviewprofile,name='facultyviewprofile'),
    path('faculty_profile_update/<slug:slug>',views.faculty_profile_update,name='faculty_profile_update'),
    path('deleteprofile/<slug:slug>',views.deleteprofile,name='deleteprofile'),
]