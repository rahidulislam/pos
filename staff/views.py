from django.shortcuts import render,redirect,get_object_or_404
from staff.models import Staff
from staff.utils import get_all_permission, selected_perms
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import FormView, TemplateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.models import Permission
from django.contrib import messages
from staff.forms import CreateStaffForm, UpdateStaffForm, ChangeBranchForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
# Create your views here.


class HomeView(PermissionRequiredMixin, TemplateView):
    template_name = "staff/staff_home.html"
    permission_required = ['staff.view_staff']
    permission_denied_message = 'You dont have permission to view staff'
    raise_exception = True
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["staffs"] = Staff.objects.all().order_by('-pk')
        return context
    
class ChangeBranch(PermissionRequiredMixin, FormView):
    permission_required = ['staff.change_staff']
    permission_denied_message = 'You dont have permission to change staff'
    raise_exception = True
    template_name = 'staff/change_branch.html'
    form_class = ChangeBranchForm

    def post(self, request, *args, **kwargs):
        staff = get_object_or_404(Staff, pk=self.kwargs['pk'])
        form = self.form_class(data=request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, 'Branch is updated successfully', extra_tags='alert alert-success')
        return redirect('staff:update_staff', pk=staff.pk)



class SetPermissions(PermissionRequiredMixin, FormView):
    template_name = "staff/set_permissions.html"
    perm_list = get_all_permission()

    def has_permission(self):
        #only allow superuser to access this view
        if self.request.user.is_superuser:
            return True
        else:
            return False
    def get(self, request, *args, **kwargs):
        staff = get_object_or_404(Staff, pk=self.kwargs['pk'])
        staff_perms_query = staff.user_permissions.all()
        staff_perms = [staff_perm.codename for staff_perm in staff_perms_query]

        context={
            'staff': staff,
            'staff_perms_query': staff_perms_query,
            'staff_perms': staff_perms,
            'perm_list': self.perm_list,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        staff = get_object_or_404(Staff, pk=self.kwargs['pk'])
        perms_selected = selected_perms(form_data=request.POST)
        staff_perms_query = staff.user_permissions.all()
        staff_perms = [staff_perm.codename for staff_perm in staff_perms_query]

        #remove existing perm that is not select
        for perm in staff_perms:
            if perm not in perms_selected:
                staff.user_permissions.remove(Permission.objects.get(codename=perm))
        
        #add selected perm
        for perm in perms_selected:
            if perm not in staff_perms:
                staff.user_permissions.add(Permission.objects.get(codename=perm))
        
        messages.success(request, f'success, updated permission for {staff.last_name}', extra_tags='alert alert-success')
        return redirect('staff:set_permission', pk=self.kwargs['pk'])

class CreateStaff(PermissionRequiredMixin, FormView):
    """Model definition for CreateStaff."""
    template_name = 'staff/create_staff.html'
    permission_required = ['staff.add_staff']
    permission_denied_message = 'You dont have permission to add staff'
    form_class = CreateStaffForm
    # TODO: Define fields here
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["staff"] = Staff.objects.all().order_by('-pk')[:10]
        context['form'] = self.form_class
        return context


    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            staff_obj = form.save(commit=False)
            #set default password
            staff_obj.set_password(raw_password=form.cleaned_data['phone_number'])
            staff_obj.save()
            messages.success(request, 'Successfully staff created', extra_tags='alert alert-success')
            return redirect('staff:staff_home')

class StaffUpdate(PermissionRequiredMixin, FormView):
    template_name = "staff/edit_staff.html"
    permission_required = ['staff.change_staff']
    permission_denied_message = 'You dont have permission to change staff'
    form_class = UpdateStaffForm
    password_form = PasswordChangeForm

    def post(self, request, *args, **kwargs):
        person = get_object_or_404(Staff, pk=self.kwargs['pk'])
        form = self.form_class(data=request.POST, instance=person)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff Details Updated", extra_tags='alert alert-info')
            return redirect("staff:update_staff", pk=self.kwargs['pk'])
        else:
            context={
              'form' : self.form_class(data=request.POST, instance=person),
              'person' : person,
              'password_form' : self.password_form, 
            }
            messages.error(request, "Error Occoured", extra_tags="alert alert-danger")
            return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        person = get_object_or_404(Staff, pk=self.kwargs['pk'])
        password_form = self.password_form(user=person)
        password_form.fields['old_password'].widget.attrs.pop("autofocus",None)

        context={
              'form' : self.form_class(instance=person),
              'person' : person,
              'password_forms' : self.password_form, 
            }
        return render(request, self.template_name, context)


class DeleteStaff(PermissionRequiredMixin, DeleteView):
    permission_required = ['staff.delete_staff']
    permission_denied_message = "You Dont Have Permission to Delete Staff"
    raise_exception = True
    model = Staff
    template_name = 'staff/staff_confirm_delete.html'
    success_url = reverse_lazy('staff:staff_home')

class Login(FormView):
    form_class = AuthenticationForm
    template_name = 'staff/login.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)


        return redirect('staff:staff_home')

class Logout(LoginRequiredMixin, FormView):
    form_class = AuthenticationForm
    template_name = 'staff/login.html'
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('staff:login')

class StaffPageView(LoginRequiredMixin, TemplateView):
    template_name = "staff/staffpage.html"

class UpdatePassword(PermissionRequiredMixin, FormView):
    permission_denied_message = "You dont have permission to change staff"
    raise_exception = True
    form_class = PasswordChangeForm

    def has_permission(self):
        staff = get_object_or_404(Staff, pk=self.kwargs['pk'])
        if staff.pk == self.request.user.pk or self.request.user.is_superuser:
            return True
        else:
            return Flase

    def post(self, request, *args, **kwargs):
        staff = get_object_or_404(Staff, pk=self.kwargs['pk'])
        form = self.form_class(user=Staff, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password is updated', extra_tags='alert alert-info')
        else:
            messages.error(request, 'Password is not updated', extra_tags='alert alert-danger')

        return redirect('staff:update_staff', pk=self.kwargs['pk'])

    

    
                

    