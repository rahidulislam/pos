from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from branches.models import Branch
from supplier.models import Supplier
from branches.forms import CreateBranchForm, UpdateBranchForm  

# Create your views here.


class BranchHomeView(PermissionRequiredMixin, TemplateView):
    permission_denied_message = 'You donot have permission to view branch'
    permission_required = ['branch.view_branch']
    raise_exception = True
    template_name = "branches/branch_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["branches"] = Branch.objects.all().order_by('-pk')
        return context
    


class CreateBranchView(PermissionRequiredMixin, CreateView):
    permission_denied_message = 'You donot have permission to create branch'
    permission_required = ['branch.add_branch']
    raise_exception = True
    form_class = CreateBranchForm
    model = Branch
    template_name = "branches/create_branch.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["branches"] = Branch.objects.all().order_by('-pk')[:25]
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        branches = Branch.objects.all()
        if form.is_valid():
            branch = form.save(commit=False)
            branch.branch_code = branch.name.replace('','_').lower()
            branch.save()
            # If this is first branch, automatically set current user's branch
            if branches.count() == 1:
                branch = branches.get()
                user = self.request.user
                user.branch_id = branch.pk
                user.save()

            supplier = Supplier(
                name = form.cleaned_data['name'],
                supplier_code = form.cleaned_data['name'].replace(" ", '_').lower(),
                primary_phone = form.cleaned_data['phone_number'],
                address = form.cleaned_data['location']
            )
            supplier.save()
            messages.success(request, 'Branch is created successfully', extra_tags='alert alert-info')
            return redirect('branches:create_branch')

class UpdateBranchView(PermissionRequiredMixin, UpdateView):
    permission_denied_message = 'You donot have permission to edit branch'
    permission_required = ['branch.change_branch']
    raise_exception = True
    form_class = UpdateBranchForm
    model = Branch 
    template_name = "branches/edit_branch.html"

    def post(self, request, *args, **kwargs):
        branch = self.get_object()
        form = self.form_class(data=request.POST, instance=branch)
        if form.is_valid():
            supplier, created = Supplier.objects.update_or_create(name=branch.name)
            if not created:
                supplier.name = form.cleaned_data['name']
                supplier.save()
            form.save()
            messages.success(request, "Branch is updated successfully", extra_tags='alert alert-success')
            return redirect('branches:update_branch', pk=branch.pk)
        else:
            context = {
                'form': form,
                'branch': branch
            }
            return render(request, self.template_name, context)


class DeleteBranchView(PermissionRequiredMixin, DeleteView):
    permission_denied_message = 'You donot have permission to delete branch'
    permission_required = ['branch.delete_branch']
    raise_exception = True
    model = Branch
    template_name = "branches/branch_confirm_delete.html"
    success_url = reverse_lazy('branches:branch_home')




