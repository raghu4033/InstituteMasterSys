from django.urls import path
from . import views
AdminArea = "FacultyArea"
urlpatterns = [
    path('', views.index,name='index'),
    path('FacultyLogin/',views.FacultyLogin,name='FacultyLogin'),

    path('FacultyForgotPassword/',views.FacultyForgotPassword,name='FacultyForgotPassword'),
    path('FacultyOTP/',views.FacultyOTP,name='FacultyOTP'),
    path('FacultyNewPassword/',views.FacultyNewPassword,name='FacultyNewPassword'),

    path('FacultyDashborad/',views.FacultyDashborad,name='FacultyDashborad'),
    path('FacultyProfile/',views.FacultyProfile,name='FacultyProfile'),
    path('FacultyApplyLeave/',views.FacultyApplyLeave,name='FacultyApplyLeave'),
    path('FacultyViewLeave/',views.FacultyViewLeave,name='FacultyViewLeave'),
    path('FacultySalaryDetailes/',views.FacultySalaryDetailes,name='FacultySalaryDetailes'),
    path('FacultyChangePassword/',views.FacultyChangePassword,name='FacultyChangePassword'),
    path('FacultyLogout/',views.FacultyLogout,name='FacultyLogout'),
    path('FacultyEnrollStudentInquiry/',views.FacultyEnrollStudentInquiry,name='FacultyEnrollStudentInquiry'),
    path('FacultytInquiryList/',views.FacultytInquiryList,name='FacultytInquiryList'),
    path('FacultyAddSubmitions/',views.FacultyAddSubmitions,name='FacultyAddSubmitions'),
    path('FacultySubmitionsList/',views.FacultySubmitionsList,name='FacultySubmitionsList'),
    path('FacultyAddBook/',views.FacultyAddBook,name='FacultyAddBook'),
    path('FacultyBookList/',views.FacultyBookList,name='FacultyBookList'),
    
    path('FacultyAddClassSchedule/',views.FacultyAddClassSchedule,name='FacultyAddClassSchedule'),
    path('FacultyViewClassSchedule/',views.FacultyViewClassSchedule,name='FacultyViewClassSchedule'),
    path('FacultyScheduleClass/',views.FacultyScheduleClass,name='FacultyScheduleClass'),
]