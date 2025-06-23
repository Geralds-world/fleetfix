from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Customer
from .models import Job, JobMarker
from django.forms import modelformset_factory
import datetime
from django.shortcuts import get_object_or_404

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'service/login.html', {'error': 'Invalid credentials'})
    return render(request, 'service/login.html')

@login_required
def dashboard(request):
    customers = Customer.objects.prefetch_related('job_set')
    return render(request, 'service/dashboard.html', {'customers': customers})



@login_required
def add_customer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        if name:
            Customer.objects.create(name=name, email=email)
            return redirect('dashboard')
    return render(request, 'service/add_customer.html')



@login_required
def add_job(request):
    customers = Customer.objects.all()

    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        customer = Customer.objects.get(id=customer_id)
        license_plate = request.POST.get('license_plate')
        service_date = request.POST.get('service_date')
        kilometers = request.POST.get('kilometers')

        job = Job.objects.create(
            customer=customer,
            license_plate=license_plate,
            service_date=service_date,
            kilometers=kilometers
        )

        marker_count = int(request.POST.get('marker_count', 5))
        for i in range(1, marker_count + 1):
            desc = request.POST.get(f'desc_{i}')
            high_risk = f'high_risk_{i}' in request.POST
            image = request.FILES.get(f'image_{i}')
            if desc or image:
                JobMarker.objects.create(
                    job=job,
                    number=i,
                    description=desc,
                    image=image,
                    high_risk=high_risk
                )

        return redirect('dashboard')

    return render(request, 'service/add_job.html', {'customers': customers, 'today': datetime.date.today().isoformat()})





@login_required
def view_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    # Separate high-risk and normal markers
    high_risk_markers = job.jobmarker_set.filter(high_risk=True).order_by('number')
    normal_markers = job.jobmarker_set.filter(high_risk=False).order_by('number')

    return render(request, 'service/view_job.html', {
        'job': job,
        'high_risk_markers': high_risk_markers,
        'normal_markers': normal_markers,
    })


from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

@login_required
def download_pdf(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    high_risk_markers = job.jobmarker_set.filter(high_risk=True).order_by('number')
    normal_markers = job.jobmarker_set.filter(high_risk=False).order_by('number')

    template = get_template('service/pdf_template.html')
    html = template.render({
        'job': job,
        'high_risk_markers': high_risk_markers,
        'normal_markers': normal_markers,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{job.license_plate}_{job.service_date}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("PDF generation failed", status=500)
    return response



from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'service/register.html', {'form': form})



from django.shortcuts import get_object_or_404, redirect

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        job.delete()
    return redirect('dashboard')



from django.shortcuts import get_object_or_404, redirect
from .models import Customer

@login_required
def delete_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    customer.delete()  # Will delete related jobs 
    return redirect('dashboard')



from datetime import date

def dashboard(request):
    customers = Customer.objects.prefetch_related('job_set').all()
    return render(request, 'service/dashboard.html', {
        'customers': customers,
        'today': date.today().strftime("%A, %d %B %Y"),
    })

