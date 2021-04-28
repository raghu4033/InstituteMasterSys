from django.urls import path
from . import views
StudentArea = "StudentArea"

urlpatterns = [
    path('StudentLogin/', views.StudentLogin,name='StudentLogin'),
    path('StudentLogout/',views.StudentLogout,name='StudentLogout'),
    path('StudentForgotPassword/',views.StudentForgotPassword,name='StudentForgotPassword'),
    path('StudentOTP/',views.StudentOTP,name='StudentOTP'),
    path('NewPassword/',views.NewPassword,name='NewPassword'),
    path('StudentChangePassword',views.StudentChangePassword,name='StudentChangePassword'),
    path('StudentProfile/',views.StudentProfile,name='StudentProfile'),
    path('StudentDashboard/',views.StudentDashboard,name='StudentDashboard'),

    path('StudentApplyLeave/',views.StudentApplyLeave,name='StudentApplyLeave'),
    path('StudentViewLeave/',views.StudentViewLeave,name='StudentViewLeave'),

    path('StudentViewAttendence/',views.StudentViewAttendence,name='StudentViewAttendence'),

    path('StudentPayFees/',views.StudentPayFees,name='StudentPayFees'),
    path('StudentFeesDetaile/',views.StudentFeesDetaile,name='StudentFeesDetaile'),

    path('StudentViewSchedual/',views.StudentViewSchedual,name='StudentViewSchedual'),

    path('StudentViewEvents/',views.StudentViewEvents,name='StudentViewEvents'),
    path('StudentViewHoliday/',views.StudentViewHoliday,name='StudentViewHoliday'),
    path('StudentViewNotice/',views.StudentViewNotice,name='StudentViewNotice'),

    path('StudentViewSubmitions',views.StudentViewSubmitions,name='StudentViewSubmitions'),

    path('StudentElibrary/',views.StudentElibrary,name='StudentElibrary'),

    path('StudentCertificate/',views.StudentCertificate,name='StudentCertificate'),

    path('StudentInsertSuggestion/',views.StudentInsertSuggestion,name='StudentInsertSuggestion'),
    path('StudentPrintInvoice/<int:pk>',views.StudentPrintInvoice,name='StudentPrintInvoice'),
]