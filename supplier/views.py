from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from supplier.models import Supplier
from supplier.forms import CreateSupplierForm, UpdateSupplierForm
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages

# Create your views here.

class SupplierHomeView(PermissionRequiredMixin, TemplateView):
    template_name = "supplier/supplier_home.html"
    permission_denied_message = 'You donot have permission to view supplier'
    permission_required = ['supplier.view_supplier']
    raise_exception = True

    def get(self, request, *args, **kwargs):
        suppliers = Supplier.objects.all()
        context = {
            'suppliers': suppliers,
        }
        return render(request, self.template_name, context)

class CreateSupplierView(PermissionRequiredMixin, CreateView):
    model = Supplier
    template_name = "supplier/create_supplier.html"
    permission_denied_message = 'You donot have permission to create supplier'
    permission_required = ['supplier.add_supplier']
    raise_exception = True
    form_class = CreateSupplierForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.supplier_code = supplier.name.replace(',','_').lower()
            supplier.save()
            messages.success(request, 'Supplier is created successfully', extra_tags='alert alert-info')
        return redirect('supplier:create_supplier')
    
    def get(self, request, *args, **kwargs):
        existing_suppliers = Supplier.objects.all().order_by('-pk')[:10]
        context = {
            'suppliers': existing_suppliers,
            'suppliers_form': self.form_class
        }
        return render(request, self.template_name, context)



class UpdateSupplierView(PermissionRequiredMixin, UpdateView):
    model = Supplier
    template_name = "supplier/edit_supplier.html"
    permission_denied_message = 'You donot have permission to change supplier'
    permission_required = ['supplier.change_supplier']
    raise_exception = True
    form_class = UpdateSupplierForm

    def post(self, request, *args, **kwargs):
        supplier = get_object_or_404(Supplier, pk=self.kwargs['pk'])
        form = self.form_class(data=request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier is updated successfully', extra_tags='alert alert-info')
        return redirect('supplier:update_supplier', pk=supplier.pk)

    def get(self, request, *args, **kwargs):
        supplier = get_object_or_404(Supplier, pk=self.kwargs['pk'])
        context = {
            'supplier': supplier,
            'form': self.form_class(instance=supplier)
        }
        return render(request, self.template_name, context)


class DeleteSupplierView(PermissionRequiredMixin, DeleteView):
    model = Supplier
    template_name = "supplier/supplier_confirm_delete.html"
    permission_required = ['supplier.delete_supplier']
    permission_denied_message = "You Dont Have Permission to Delete Supplier"
    raise_exception = True
    success_url = reverse_lazy('supplier:supplier_home')

class DetailSupplierView(DetailView):
    model = Supplier
    template_name = "supplier/supplier_detail.html"
    context_object_name = 'supplier'


