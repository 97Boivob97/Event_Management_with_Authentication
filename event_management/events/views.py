from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile,Event,Booking,Category
from .forms import UserProfileForm,EventForm
from django.contrib import messages
from django.db.models import Q

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']


# Create your views here.

def home(request):
    events = Event.objects.all()
    return render(request, 'home.html', {'events': events})

def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        
    form = UserRegistrationForm()
    context={
        "form":form
    }
    return render(request,'registration.html',context)

def log_in(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('home')
        
    form = AuthenticationForm()
    context = {
        "form":form
    }
    return render(request,'login.html',context)

@login_required
def log_out(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    user = request.user
    # profile = UserProfile.objects.get(user=user)
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        form = UserProfileForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
           form = UserProfileForm(instance=profile)
        
    context = {
        "form":form,
        "user":user,
    }
    return render(request,'profile.html',context)


def event_list(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    events = Event.objects.all()

    if query:
        events = events.filter(
            Q(title__icontains=query) |
            Q(date__icontains=query) |
            Q(location__icontains=query)
        )

    if category_id:
        events = events.filter(category_id=category_id)

    categories = Category.objects.all()
    return render(request, 'event_list.html', {'events': events, 'categories': categories})



@login_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form})

@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk, created_by=request.user)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'event_form.html', {'form': form})

@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk, created_by=request.user)
    if request.method == "POST":
        event.delete()
        return redirect('event_list')
    
@login_required
def event_book(request, pk):
    # event = get_object_or_404(Event, pk=pk)
    # Booking.objects.get_or_create(user=request.user, event=event)
    # return redirect('home')
    event = get_object_or_404(Event, pk=pk)
    if not event.is_fully_booked():
        event.bookings += 1
        event.save()
        messages.success(request, 'Booking successful!')
    else:
        messages.error(request, 'Event is fully booked.')
    return redirect('event_detail', event_id=event.id)

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'my_bookings.html', {'bookings': bookings})
    


