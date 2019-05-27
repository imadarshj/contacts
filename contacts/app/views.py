# For class based views
from django.views.generic import ListView, DetailView

from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
#   For complex query search
from django.db.models import Q
from .models import Contact

from django.views.generic.edit import CreateView,UpdateView,DeleteView

# IDEA: we can create new user from our template
from django.contrib.auth.forms import UserCreationForm

# IDEA: FOR CLASS BASED VIEWS WE CAN WRITE THIS
from django.contrib.auth.mixins import LoginRequiredMixin

# IDEA: FOR FUNCTION BASED VIEW WE NEED This:
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy
from django.contrib import messages
#   we'll use generic class based view provided by django
#   to Create an obj from frontend
# Create your views here.

"""
def home (request):

    context = {
        'contacts' : Contact.objects.all()
    }

    #return HttpResponse("Hello, world. You're at the polls index.")
    #return render(request,'index.html')  -- old version

    contexts = {'status': 'Working on the Project'}
    return render(request,'index.html', context  )
"""

"""
def detail(request , id):
    context = {
        'contact' :  get_object_or_404(Contact , pk = id)   #it thakes the name of the model and primary key value
    }
    return render(request , 'detail.html' , context)
"""
#   IDEA: It must inherit from ListViews
#   IDEA: But this ListView contains the getQuerySet()
#   IDEA: which returns all the contacts so we need to override it
#   IDEA: so that it'll display only the required contacts
class HomePageView(LoginRequiredMixin,ListView):
    #   what template we want to render this content
    template_name = 'index.html'
    #   mention the model from where we are going to show the list of objects
    model = Contact
    #   we have configured our homepage by giving it an name contacts
    #   to all the fetched contact object so have to tell Django to
    #   call all those objects in our contact models
    context_object_name = 'contacts'
    def get_queryset(self):
        """
        we'll create all the contact obj that would have sent to us when we try
        to visit the home page when we visit the get_queryset() method
        """
        contacts = super().get_queryset()
        # IDEA: NOW WE'LL filter -> it takes the name of model field and
        # IDEA: set it's value to current login user
        return contacts.filter(manager = self.request.user)
# Similarly, we make the contact detailview
class ContactDetailView(LoginRequiredMixin,DetailView):
    template_name = 'detail.html'
    model = Contact
    context_object_name = 'contact'
# function based view needs a "request" argument and here,
# we have to return a template
@login_required
def search(request):
    if request.GET:
            #variable = name of input tag
        search_term = request.GET['search_term']
        search_results = Contact.objects.filter(
            Q(name__icontains = search_term) |
            Q(email__icontains = search_term) |
            Q(info__icontains = search_term) |
            Q(phone__iexact = search_term)
        )
        context = {
        #we are assiging its value as the variable search_term
            'search_term' : search_term ,
            # IDEA: we dont write self.request.user as this is not Class based
            'contacts' : search_results.filter(manager = request.user )
                # after adding this , we make the changes
                # in the value accordingly
        }
        return render(request , 'search.html' , context)
    else:
        return redirect('home')
#    this CreateView contains all the function req to
#   Create an obj from the frontend
class ContactCreateView(LoginRequiredMixin,CreateView):
    model = Contact
    template_name = 'create.html'
    #list of values that will include the form input that will be there in the template
    fields = ['name' , 'email' , 'phone' , 'info' , 'gender' , 'image']
    # success_url = '/'
    """
        in the front end we have ['name' , 'email' , 'phone' , 'info' , 'gender' , 'image']
        model fields but we have another model field -> manager, we cannot manually add it,
        we need to automate it so we use this form_valid().
        + We cannot make a drop down for the list of users
    """
    # we have the form argument
    # we are saving all the form values
    # in the instance variable
    def form_valid(self,form):
        # we don't want it to be saved to the database isntead
        # we want it to be saved it into our instance variable
        # for it we set commit = False and the follwing next line
        instance = form.save(commit=False)
        # we can set the manager model field
        instance.manager = self.request.user
        # now we can save the instance variables
        instance.save()

        messages.success(self.request,'Your contact has been successfully created.')
        # we want it to redirect the home page
        return redirect('home')


class ContactUpdateView(LoginRequiredMixin,UpdateView):
    model = Contact
    template_name = 'update.html'
    #list of values that will include the form input that will be there in the template
    fields = ['name' , 'email' , 'phone' , 'info' , 'gender' , 'image']
    #   This was taking us to the home page but we want to
    #   go to the detail page so :: success_url = '/'

    def form_valid(self,form):
        #   we have to create an instance that will have the
        #   contact object that we are trying to update
        instance = form.save()
        messages.success(self.request,'Your contact has been successfully updated.')
        return redirect('detail',instance.pk)

class ContactDeleteView(LoginRequiredMixin,DeleteView):
    model = Contact
    template_name = 'delete.html'
    success_url = '/'
    def delete(self,request,*args,**kwargs):
        messages.success(self.request,'Your contact has been successfully deleted.')
        # IDEA: WE NEED TO ACTUALLY RUN THE delete() TO ACTUALLY DELETE THE CONTACT
        return super().delete(self,request,*args,**kwargs)

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    #messages.success(self.request,'Registration successful')
    success_url = reverse_lazy('home')
