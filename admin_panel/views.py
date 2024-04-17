from django.shortcuts import render
from django.contrib import messages

def Index_function(request):
    return render(request , "index.html")



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:  # Check if user is staff (admin)
            login(request, user)
            return redirect('admin_dashboard')  # Redirect to admin dashboard after login
        else:
            error = "Invalid username or password. Please try again."
            return render(request, 'admin_panel/admin_login.html', {'error': error})
    else:
        return render(request, 'admin_panel/login.html')




def admin_logout(request):
    logout(request)
    return redirect('admin_login')



def admin_dashboard(request):
    return render(request , "admin_panel/admin_dashboard.html")




from django.shortcuts import render, redirect
from .models import Institute
from django.contrib import messages

def add_institute(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        contact_number = request.POST.get('contact_number')
        image = request.FILES.get('image')
        admin_password = request.POST.get('password')  # Changed from 'password' to 'admin_password'
        # Generate unique ID for institute
        last_id = Institute.objects.all().order_by('-id').first()
        if last_id:
            last_id = last_id.id.split('_')[1]
            new_id = f"VD_{str(int(last_id) + 1).zfill(2)}"
        else:
            new_id = "VD_01"
        institute = Institute.objects.create(id=new_id, name=name, location=location, contact_number=contact_number, image=image, admin_password=admin_password)  
        messages.success(request, "Institute added successfully.")
        return redirect('institute_list')  # Redirect to admin dashboard after adding institute
    else:
        # Generate unique ID for institute
        last_id = Institute.objects.all().order_by('-id').first()
        if last_id:
            last_id = last_id.id.split('_')[1]
            new_id = f"VD_{str(int(last_id) + 1).zfill(2)}"
        else:
            new_id = "VD_01"
        # Pass the generated ID along with an empty Institute object to the template context
        return render(request, 'admin_panel/add_institute.html', {'institute': Institute(id=new_id), 'disable_id': True})



from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Institute

def institute_list(request):
    institutes = Institute.objects.all()
    return render(request, 'admin_panel/institute_list.html', {'institutes': institutes})


def view_institute(request, institute_id):
    institute = get_object_or_404(Institute, id=institute_id)
    return render(request, 'admin_panel/view_institute.html', {'institute': institute})


def edit_institute(request, institute_id):
    institute = get_object_or_404(Institute, id=institute_id)
    
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        location = request.POST.get('location')
        contact_number = request.POST.get('contact_number')
        change_image = request.FILES.get('change_image')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        
        # Update institute details
        institute.name = name
        institute.location = location
        institute.contact_number = contact_number
        
        # Check if a new image is uploaded
        if change_image:
            institute.image = change_image
        
        # Check if new password is provided
        if new_password:
            # Check if the current password matches
            if current_password == institute.admin_password:
                institute.admin_password = new_password
            else:
                # Add an error message if the current password is incorrect
                messages.error(request, "Incorrect current password. Password not updated.")
                return render(request, 'admin_panel/edit_institute.html', {'institute': institute})
        
        # Save changes to the database
        institute.save()
        
        # Add a success message
        messages.success(request, "Institute details updated successfully.")
        
        # Redirect to institute list page or any other page as needed
        return redirect('institute_list')
    
    return render(request, 'admin_panel/edit_institute.html', {'institute': institute})


def delete_institute(request, institute_id):
    institute = get_object_or_404(Institute, id=institute_id)
    institute_name = institute.name
    institute.delete()
    messages.success(request, f"Institute '{institute_name}' has been deleted successfully.")
    return redirect('institute_list')




from institute_panel.models import Student

def institute_student_list(request):
    # Retrieve all institutes from the database
    institutes = Institute.objects.all()
    
    # Calculate total number of students for each institute
    for institute in institutes:
        institute.total_students = Student.objects.filter(institute=institute).count()
    
    return render(request, 'admin_panel/institute_student_list.html', {'institutes': institutes})


def view_student_list(request, institute_id):
    institute = get_object_or_404(Institute, id=institute_id)
    return render(request, 'admin_panel/view_student_list.html', {'institute': institute})


def view_student_1(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    return render(request, 'admin_panel/view_student_list_2.html', {'student': student})


def edit_student_list(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        # Retrieve form data
        admission_number = request.POST.get('admission_number')
        student_name = request.POST.get('student_name')
        student_class = request.POST.get('class')
        section = request.POST.get('section')
        course = request.POST.get('course')
        contact_number = request.POST.get('contact_number')
        gender = request.POST.get('gender')
        admission_date = request.POST.get('admission_date')
        
        # Update student data
        student.admission_number = admission_number
        student.name = student_name
        student.student_class = student_class
        student.section = section
        student.course = course
        student.contact_number = contact_number
        student.gender = gender
        student.admission_date = admission_date
        student.save()
        
        
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
        return redirect('view_student_list', institute_id=student.institute_id)

    classes = CourseFee.objects.values_list('class_name', flat=True).distinct()
    courses = CourseFee.objects.values_list('course', flat=True).distinct()

    # Pass student, classes, and courses data to the template
    context = {
        'student': student,
        'classes': classes,
        'courses': courses,
    }
    
    return render(request, 'admin_panel/edit_student_list.html', context)


def delete_student_list(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    student.delete()
    messages.success(request, "Student deleted successfully.")
    return redirect('view_student_list', institute_id=student.institute_id)



from django.shortcuts import render, redirect
from .models import CourseFee

def add_bse_fees(request):
    if request.method == 'POST':
        course = 'BSE'
        fee_amount = request.POST.get('fee_amount')
        class_name = request.POST.get('class_name')  # Get the selected class from the form
        CourseFee.objects.create(course=course, fee_amount=fee_amount, class_name=class_name)
        messages.success(request, 'BSE Fee has been added successfully.')
        return redirect('view_bse_fees')
    return render(request, 'admin_panel/add_bse_fees.html')


def view_bse_fees(request):
    bse_fees = CourseFee.objects.filter(course='BSE')
    return render(request, 'admin_panel/view_bse_fees.html', {'bse_fees': bse_fees})


def edit_bse_fee(request, fee_id):
    fee = CourseFee.objects.get(id=fee_id)
    if request.method == 'POST':
        fee.fee_amount = request.POST.get('fee_amount')
        fee.save()
        messages.success(request, 'BSE Fee has been updated successfully.')
        return redirect('view_bse_fees')
    # Assuming you have some logic to fetch class options
    class_options = ["Class 1", "Class 2", "Class 3", "Class 4", "Class 5", "Class 6", "Class 7", "Class 8", "Class 9", "Class 10"]
    return render(request, 'admin_panel/edit_bse_fee.html', {'fee': fee, 'class_options': class_options})


def delete_bse_fee(request, fee_id):
    fee = CourseFee.objects.get(id=fee_id)
    fee.delete()
    messages.success(request, 'BSE Fee has been deleted successfully.')
    return redirect('view_bse_fees')



def add_cbse_fees(request):
    if request.method == 'POST':
        course = 'CBSE'
        fee_amount = request.POST.get('fee_amount')
        class_name = request.POST.get('class_name')  # Get the selected class from the form
        CourseFee.objects.create(course=course, fee_amount=fee_amount, class_name=class_name)
        messages.success(request, 'CBSE fee has been successfully added.')
        return redirect('view_cbse_fees')
    return render(request, 'admin_panel/add_cbse_fees.html')

def view_cbse_fees(request):
    cbse_fees = CourseFee.objects.filter(course='CBSE')
    return render(request, 'admin_panel/view_cbse_fees.html', {'cbse_fees': cbse_fees})

def edit_cbse_fee(request, fee_id):
    fee = CourseFee.objects.get(id=fee_id)
    if request.method == 'POST':
        fee.fee_amount = request.POST.get('fee_amount')
        fee.save()
        messages.success(request, 'CBSE fee has been successfully updated.')
        return redirect('view_cbse_fees')
    class_options = ["Class 1", "Class 2", "Class 3", "Class 4", "Class 5", "Class 6", "Class 7", "Class 8", "Class 9", "Class 10"]
    return render(request, 'admin_panel/edit_cbse_fee.html', {'fee': fee, 'class_options': class_options})

def delete_cbse_fee(request, fee_id):
    fee = CourseFee.objects.get(id=fee_id)
    fee.delete()
    messages.success(request, 'CBSE fee has been successfully deleted.')
    return redirect('view_cbse_fees')


def add_competitive_fees(request):
    if request.method == 'POST':
        course = 'Competitive'
        fee_amount = request.POST.get('fee_amount')
        duration = request.POST.get('duration')  # Get duration from the form
        subject = request.POST.get('subject')  # Get subject from the form
        qualification = request.POST.get('qualification')  # Get qualification from the form
        
        CourseFee.objects.create(course=course, fee_amount=fee_amount, duration=duration, subject=subject, qualification=qualification)
        
        messages.success(request, 'Competitive fee has been successfully added.')
        return redirect('view_competitive_fees')
    
    return render(request, 'admin_panel/add_competitive_fees.html')



def view_competitive_fees(request):
    # Retrieve all competitive fees from the database
    competitive_fees = CourseFee.objects.filter(course='Competitive')
    
    return render(request, 'admin_panel/view_competitive_fees.html', {'competitive_fees': competitive_fees})


def edit_competitive_fee(request, fee_id):
    fee = CourseFee.objects.get(id=fee_id)
    if request.method == 'POST':
        # Assuming you have form fields for editing
        fee.fee_amount = request.POST.get('fee_amount')
        fee.duration = request.POST.get('duration')
        fee.subject = request.POST.get('subject')
        fee.qualification = request.POST.get('qualification')
        fee.save()
        messages.success(request, 'Competitive fee has been updated successfully.')
        return redirect('view_competitive_fees')
    return render(request, 'admin_panel/edit_competitive_fee.html', {'fee': fee})


def delete_competitive_fee(request, fee_id):
    fee = CourseFee.objects.get(id=fee_id)
    fee.delete()
    messages.success(request, 'Competitive fee has been deleted successfully.')
    return redirect('view_competitive_fees')