from django.shortcuts import render,redirect
from customers.models import Customer
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from customers.forms import CreateCustomerForm, UpdateCustomerForm



# Create your views here.

class CustomerCreateView(PermissionRequiredMixin, CreateView):
    permission_denied_message = 'you do not have permission to add customer'
    permission_required = ['customers.add_customer']
    raise_exception = True
    model = Customer
    template_name = "customers/create_customer.html"
    form_class = CreateCustomerForm

    def get_success_url(self):
        messages.success(self.request, 'Customer have been created successfully', extra_tags='alert alert-success')
        return reverse_lazy('customers:create_customer')


class CustomerHomeView(PermissionRequiredMixin, ListView):
    permission_denied_message = 'you do not have permission to view customer'
    permission_required = ['customers.view_customer']
    raise_exception = True

    model = Customer
    template_name = "customers/customer_home.html"
    context_object_name =  'customers'


class CustomerDetailView(PermissionRequiredMixin, DetailView):
    permission_denied_message = 'you do not have permission to view customer'
    permission_required = ['customers.view_customer']
    raise_exception = True
    model = Customer
    template_name = "customers/customer_detail.html"
    

class CustomerUpdateView(PermissionRequiredMixin, UpdateView):
    permission_denied_message = 'you do not have permission to change customer'
    permission_required = ['customers.change_customer']
    raise_exception = True
    model = Customer
    template_name = "customers/edit_customer.html"
    form_class = UpdateCustomerForm
    
    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, 'Customer have been Updated successfully', extra_tags='alert alert-success')
        return reverse_lazy('customers:edit_customer', kwargs={'pk': self.kwargs['pk']})


class CustomerDeleteView(PermissionRequiredMixin, DeleteView):
    permission_denied_message = 'you do not have permission to delete customer'
    permission_required = ['customers.delete_customer']
    raise_exception = True
    model = Customer
    template_name = "customers/customer_confirm_delete.html"

    def get_success_url(self):
        messages.success(self.request, 'Customer have been Delete successfully', extra_tags='alert alert-success')
        return reverse_lazy('customers:customer_home')
