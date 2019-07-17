from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth import get_user_model
from contacts.models import Contact
User = get_user_model()

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'You are logged in')
            return redirect('dashboard')
        else:
            messages.error(request,'Invalid credential')
            return redirect('login')
    else:
        return render(request,'accounts/login.html')

def register(request):

    if request.method == "POST":
        #Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        #Check if password match
        if password == password2:
            #check Username
            if User.objects.filter(username=username).exists():
                messages.error(request,'Username already taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'Email already used')
                    return redirect('register')
                else:
                    user = User.objects.create(username=username, password=password,
                    email=email, first_name=first_name, last_name=last_name)
                    # Login after Register
                    # auth.login(request,user)
                    # messages.success(request,'You are now logged in')
                    # return redirect('index')
                    user.save()
                    messages.success(request,'You are now registered and can log in')
                    return redirect('login')
        else:
            message.error(request,'Password did not match')
            return redirect('register')

    else:
        return render(request,'accounts/register.html')

def dashboard(request):
    user_contacts = Contact.object.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts':user_contacts
    }
    return render(request,'accounts/dashboard.html',context)

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,'You are logged out')
        return redirect('index')
