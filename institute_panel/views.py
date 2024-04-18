from django.shortcuts import render, redirect
from admin_panel.models import Institute
from django.shortcuts import render, get_object_or_404, redirect
from .models import Student
from django.contrib import messages
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


def institute_login(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        password = request.POST.get('password')
        try:
            institute = Institute.objects.get(id=id, admin_password=password)
            # Store the institute ID in the session
            request.session['institute_id'] = institute.id
            return redirect('institute_dashboard')
        except Institute.DoesNotExist:
            error = "Invalid ID or password. Please try again."
            return render(request, 'institute_panel/login.html', {'error': error})
    return render(request, 'institute_panel/login.html')



from django.shortcuts import render
from admin_panel.models import AdminProfile

def institute_dashboard(request):
    # Fetch the logged-in user's profile
    if request.user.is_authenticated:
        try:
            admin_profile = AdminProfile.objects.get(user=request.user)
            institute_image_url = admin_profile.institute.image.url
        except AdminProfile.DoesNotExist:
            # Handle the case where the user does not have an associated profile
            institute_image_url = None
    else:
        # Handle the case where the user is not authenticated
        institute_image_url = None
    
    return render(request, 'institute_panel/institute_dashboard.html', {'institute_image_url': institute_image_url})



from django.shortcuts import render, redirect
from admin_panel.models import Institute
from .models import Student
from django.http import JsonResponse


def add_student(request):
    if request.method == 'POST':
        admission_number = request.POST.get('admission_number')
        student_name = request.POST.get('student_name')
        student_class = request.POST.get('class')
        section = request.POST.get('section')
        course = request.POST.get('course')
        contact_number = request.POST.get('contact_number')
        gender = request.POST.get('gender')
        admission_date = request.POST.get('admission_date')  # Retrieve admission date from the form

        # Retrieve the institute ID from the session
        institute_id = request.session.get('institute_id')

        # Get the Institute object using the institute ID
        institute = Institute.objects.get(pk=institute_id)

        # Fetch the corresponding CourseFee object based on the selected class and course
        try:
            course_fee = CourseFee.objects.get(class_name=student_class, course=course)
        except CourseFee.DoesNotExist:
            course_fee = None

        # Create a new Student object and save it to the database
        student = Student.objects.create(
            institute=institute,
            admission_number=admission_number,
            name=student_name,
            student_class=student_class,
            section=section,
            course=course,
            contact_number=contact_number,
            gender=gender,
            admission_date=admission_date,
            course_fee=course_fee  # Assign the fetched CourseFee object to the course_fee field
        )

        return redirect('student_list')  # Redirect to student list page after successful submission

    classes = CourseFee.objects.values_list('class_name', flat=True).distinct()
    courses = CourseFee.objects.values_list('course', flat=True).distinct()

    context = {
        'classes': classes,
        'courses': courses,
    }

    return render(request, 'institute_panel/add_student.html', context)


def get_fee_amount(request):
    if request.method == 'GET':
        selected_class = request.GET.get('class')
        selected_course = request.GET.get('course')

        # Query the CourseFee model to get the fee amount
        try:
            course_fee = CourseFee.objects.get(class_name=selected_class, course=selected_course)
            fee_amount = course_fee.fee_amount
        except CourseFee.DoesNotExist:
            fee_amount = None

        # Return the fee amount as JSON response
        return JsonResponse({'fee_amount': fee_amount})
    else:
        # Return an error response if the request method is not GET
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def student_list(request):
    # Retrieve the institute ID from the session
    institute_id = request.session.get('institute_id')

    # Filter students based on the institute ID
    students = Student.objects.filter(institute__pk=institute_id)
    
    return render(request, 'institute_panel/student_list.html', {'students': students})


def view_student1(request, student_id):
    student = get_object_or_404(Student, pk=student_id, institute__pk=request.session.get('institute_id'))
    return render(request, 'institute_panel/view_student1.html', {'student': student})


def edit_student(request, student_id):
    # Retrieve the student object with the provided ID and institute ID from the session
    student = get_object_or_404(Student, pk=student_id, institute__pk=request.session.get('institute_id'))

    if request.method == 'POST':
        # Update student data with the submitted form data
        student.admission_number = request.POST.get('admission_number')
        student.name = request.POST.get('student_name')
        student.student_class = request.POST.get('class')
        student.section = request.POST.get('section')
        student.course = request.POST.get('course')
        student.contact_number = request.POST.get('contact_number')
        student.gender = request.POST.get('gender')
        student.admission_date = request.POST.get('admission_date')
         
        try:
            course_fee = CourseFee.objects.get(class_name=student.student_class, course=student.course)
            student.course_fee = course_fee
        except CourseFee.DoesNotExist:
            student.course_fee = None

        # Save the updated student object to the database
        student.save()

        # Display success message
        messages.success(request, "Student information updated successfully.")

        # Redirect to the view student page for the updated student
        return redirect('student_list')

    classes = CourseFee.objects.values_list('class_name', flat=True).distinct()
    courses = CourseFee.objects.values_list('course', flat=True).distinct()

    # Pass student, classes, and courses data to the template
    context = {
        'student': student,
        'classes': classes,
        'courses': courses,
    }

    return render(request, 'institute_panel/edit_student.html', context)


def get_fee_amount(request):
    if request.method == 'GET':
        selected_class = request.GET.get('class')
        selected_course = request.GET.get('course')

        # Query the CourseFee model to get the fee amount
        try:
            course_fee = CourseFee.objects.get(class_name=selected_class, course=selected_course)
            fee_amount = course_fee.fee_amount
        except CourseFee.DoesNotExist:
            fee_amount = None

        # Return the fee amount as JSON response
        return JsonResponse({'fee_amount': fee_amount})
    else:
        # Return an error response if the request method is not GET
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def delete_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id, institute__pk=request.session.get('institute_id'))
    student.delete()
    messages.success(request, f"Student '{student.name}' has been deleted successfully.")
    return redirect('student_list')  # Redirect to student list page after deletion


from admin_panel.models import CourseFee

def view_bse_fees1(request):
    bse_fees = CourseFee.objects.filter(course='BSE')
    return render(request, 'institute_panel/view_bse_fees1.html', {'bse_fees': bse_fees})


def view_cbse_fees1(request):
    cbse_fees = CourseFee.objects.filter(course='CBSE')
    return render(request, 'institute_panel/view_cbse_fees1.html', {'cbse_fees': cbse_fees})


def view_competitive_fees1(request):
    # Retrieve all competitive fees from the database
    competitive_fees = CourseFee.objects.filter(course='Competitive')
    
    # Pass the retrieved fees to the template for rendering
    return render(request, 'institute_panel/view_competitive_fees1.html', {'competitive_fees': competitive_fees})


def fee_payment_page(request):
    # Retrieve the institute ID from the session
    institute_id = request.session.get('institute_id')

    # Filter students based on the institute ID
    students = Student.objects.filter(institute__pk=institute_id)
    
    return render(request, 'institute_panel/fee_payment.html', {'students': students})



def show_payment_details(request):
    return JsonResponse("Hello")

def pay_now(request,student_id):
    return render(request,'payment.html')


@csrf_exempt
def initiate_payment(request):
    if request.method == "POST":
        amount = int(request.POST["amount"]) * 100  # Amount in paise
        

        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

        payment_data = {
            "amount": amount,
            "currency": "INR",
            "receipt": "order_receipt",
            "notes": {
                "email": "user_email@example.com",
            },
        }

        order = client.order.create(data=payment_data)
        
        # Include key, name, description, and image in the JSON response
        response_data = {
            "id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"],
            "key": settings.RAZORPAY_API_KEY,
            "name": "Vidya Bhaban",
            "description": "Payment Monthly fees",
            "image": "https://vidyabhaban.com/uploads/school_content/logo/1711654172-16878526516605c51c1f461!BAN1.jpg",  # Replace with your logo URL
            
        }
        
        return JsonResponse(response_data)
    
    return render(request, "payment.html")

def payment_success(request):
    return render(request, "payment_success.html")

def payment_failed(request):
    return render(request, "payment_failed.html")


from .models import Payment

def payment_report(request):
    # Retrieve the institute ID from the session
    institute_id = request.session.get('institute_id')
    
    # Retrieve associated students for the institute
    associated_students = Student.objects.filter(institute__pk=institute_id)
    
    # Retrieve successful payments for the associated students
    successful_payments = Payment.objects.filter(student__in=associated_students, payment_status=1)
    
    return render(request, 'institute_panel/payment_report.html', {'successful_payments': successful_payments})

