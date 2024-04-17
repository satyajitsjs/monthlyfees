from django.urls import path
from .views import institute_login, institute_dashboard,add_student,student_list,view_student1,edit_student,delete_student,view_bse_fees1,view_cbse_fees1,view_competitive_fees1
from .views import get_fee_amount,fee_payment_page
from institute_panel import views as v
from . import views

urlpatterns = [
    path('login/', institute_login, name='institute_login'),
    path('dashboard/', institute_dashboard, name='institute_dashboard'),

    path('add_student/', add_student, name='add_student'),
    path('student-list/', student_list, name='student_list'),
    path('student/<int:student_id>/', view_student1, name='view_student1'),
    path('student/<int:student_id>/edit/', edit_student, name='edit_student1'),
    path('student/<int:student_id>/delete/', delete_student, name='delete_student1'),
    
    path('view-bse-fees1/', view_bse_fees1, name='view_bse_fees1'),
    path('view-cbse-fees1/', view_cbse_fees1, name='view_cbse_fees1'),
    path('view-competitive-fees1/', view_competitive_fees1, name='view_competitive_fees1'),
    

    path('get_fee_amount/', get_fee_amount, name='get_fee_amount'),
    path('fee-payment/', fee_payment_page, name='fee_payment'),
    
    path("get-payment-details/",v.show_payment_details, name='show_payment_details'),
    path("pay-now/<int:student_id>/",v.pay_now, name='pay_now'),


    path("initiate-payment/", views.initiate_payment, name="initiate_payment"),
    path("payment-success/", views.payment_success, name="payment_success"),
    path("payment-failed/", views.payment_failed, name="payment_failed"),

    
    
    
    
]