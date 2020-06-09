from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from datetime import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView, FormView, CreateView, UpdateView, DeleteView, DetailView, ListView
from products.models import Products, Transfer, TransferProduct, BranchProduct
from products.forms import CreateProductForm, UpdateProductForm, TransferFiltersForm, SetTransferToForm, ProductTransferForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from deliveries.models import Delivery, Stock

# Create your views here.

class ProductHomeView(PermissionRequiredMixin, TemplateView):
    permission_denied_message = "you do not have permission to view products"
    permission_required = ['products.view_product']
    raise_exception = True
    template_name = "products/product_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Products.objects.all().order_by('-pk')
        return context
    

class CreateProductView(PermissionRequiredMixin, CreateView):
    permission_denied_message = 'You do not have permissions to add products'
    permission_required = ['products.add_product']
    raise_exception = True
    form_class = CreateProductForm
    model = Products
    template_name = "products/create_product.html"

    def get(self, request, *args, **kwargs):
        products = Products.objects.all().order_by('-pk')[:25]
        context = {
            'products': products,
            'form': self.form_class
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product is created successfully', extra_tags='alert alert-success')
            return redirect('products:create_product')
        else:
            messages.error(request, 'Product is not added', extra_tags='alert alert-danger')
            return redirect('products:create_product')


class ProductDetailView(DetailView):
    permission_denied_message ='You do not have permission to view the product'
    permission_required = ['products.view_product']
    raise_exception =True
    model = Products
    template_name = "products/product_detail.html"
    context_object_name = 'product'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context['product']
        
    

        branch_stock,created = BranchProduct.objects.get_or_create(
            branch_id = self.request.user.branch_id,
            product_id = product.pk, 
            
        )
        try:
            stock = Stock.objects.filter(
                product_id = product.pk,
                current_branch_id = self.request.user.branch_id,
                home_branch_id = self.request.user.branch_id
            ).latest('posted')
            buying_price = Stock.buying_price
            retail_price = Stock.retail_price
            wholesale_price = Stock.wholesale_price
            supplier = Stock.delivery.received_from.name

        except ObjectDoesNotExist:
            buying_price = 0.00
            retail_price = 0.00
            wholesale_price = 0.00
            supplier = product.supplier.name
        
        context['Stock_Vals'] = {
            'cost_value': buying_price*branch_stock.quantity,
            'retail_value': retail_price*branch_stock.quantity,
            'retail_price': retail_price,
            'wholesale_value': wholesale_price*branch_stock.quantity,
            'wholesale_price': wholesale_price,
            'quantity': branch_stock.quantity,
            'buying_price': buying_price,
            'supplier': supplier,
        }

        return context


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    permission_denied_message = "you do not have permission to change product"
    permission_required = ['products.change_product']
    raise_exception = True
    model = Products
    template_name = "products/update_product.html"
    form_class = UpdateProductForm
    success_url = 'products:update_product'
    context_object_name = 'product'

    def get_success_url(self):
        messages.success(self.request, "Product is Updated successfully", extra_tags='alert alert-success')
        return reverse_lazy('products:update_product', kwargs={'pk': self.kwargs['pk']})


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    permission_denied_message = 'you do not have permission to delete product'
    permission_required = ['products.delete_product']
    raise_exception = True
    model = Products
    template_name = "products/product_confirm_delete.html"
    success_url = reverse_lazy('products:product_home')


class ProductAddTransfer(PermissionRequiredMixin, FormView):
    permission_denied_message = "you do not have permission to add product"
    permission_required = ['transfer.add_transfer']
    raise_exception = True
    form_class = ProductTransferForm
    template_name = 'products/product_add_transfer.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        
        if form.is_valid():
            product = get_object_or_404(Products, pk=form.cleaned_data['product'])
            
            try:
                stock = Stock.objects.filter(
                    product_id = product.pk,
                    current_branch_id = request.user.branch_id,
                    home_branch_id = request.user.branch_id
                ).latest('posted')

            except ObjectDoesNotExist:
                messages.error(request, 'Out of Stock, No purchase on record', extra_tags='alert alert-warning')
                return redirect('products:transfer_product')

            if stock.quantity < form.cleaned_data['quantity']:
                messages.error(request, f"Out of range. only {stock.quantity} available", extra_tags='alert alert-warning')
                return redirect('products:transfer_product')

            new_product = {
                'product_name' : product.name,
                'product_id' : product.pk,
                'unit_cost' : stock.buying_price,
                'quantity' : form.cleaned_data['quantity'],
                'total': form.cleaned_data['quantity'] * stock.buying_price,
            }

            if "products" not in request.session:
                request.session['products'] = list()
                request.session['products'].append(new_product)
                request.session['products_total'] = new_product['total']

            else:
                cart_products = request.session['products']
                product_id = [pk['product_id'] for pk in cart_products]

                if new_product['product_id'] not in product_id:
                    cart_products.append(new_product)
                else:
                    for item in cart_products:
                        if item['product_id'] == new_product['product_id']:
                            item['quantity'] = item['quantity'] + new_product['quantity']
                            item['total'] = item['quantity'] * item['unit_cost']

                request.session['products'] = cart_products
                request.session['products_total'] = sum(item['total'] for item in cart_products)

        return redirect('products:product_home')

class TransferProduct(PermissionRequiredMixin, FormView):
    permission_denied_message = "you do not have permission to add product"
    permission_required = ['transfer.add_transfer']
    raise_exception = True
    form_class = ProductTransferForm
    template_name = 'products/product_add_transfer.html'

    def get(self, request, *args, **kwargs):
        if 'transfer_to_id' not in self.request.session.keys():
            return redirect('products:set_transfer_to')

        else:
            return render(request, self.template_name, context=self.get_context_data())


class SetTransferTO(PermissionRequiredMixin, FormView):
    permission_denied_message = "you do not have permission  set transfer to product"
    permission_required = ['transfer.add_transfer']
    raise_exception = True
    form_class = SetTransferToForm
    template_name = 'products/set_transfer_to.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            if form.cleaned_data['transfer_to'].pk == request.user.branch_id:
                messages.error(request, "Can not Transfer to same branch", extra_tags='alert alert-info')
                return redirect('products:set_transfer_to')
            request.session['transfer_to'] = form.cleaned_data['transfer_to'].name
            request.session['transfer_to_id'] = form.cleaned_data['transfer_to'].pk
            return redirect('products:add_transfer')

        else:
            return render(request, self.template_name, context=self.get_context_data())

class DeleteCartProduct(PermissionRequiredMixin, TemplateView):
    permission_denied_message = "you do not have permission  to add transfer"
    permission_required = ['transfer.add_transfer']
    raise_exception = True

    def get(self, request, *args, **kwargs):
        if not kwargs['product_id']:
            return redirect('products:transfer_product')

        if 'products' in request.session.keys():
            if self.kwargs['product_id'] in [p['product_id'] for p in request.session['products']]:
                cart_products = request.session['products']
                for product in cart_products:
                    if product['product_id'] == self.kwargs['product_id']:
                        cart_products.remove(product)
                        request.session['products'] = cart_products
                        request.session['products_total'] = sum([item['total'] for item in cart_products])
                        messages.success(request, 'product has been removed successfully', extra_tags='alert alert-success')

            else:
                messages.error(request, 'Product not in list', extra_tags='alert alert-danger')
        else:
            messages.info(request, 'Alert! List is empty.', extra_tags='alert alert-info')

        return redirect('products:transfer_product')

class ClearList(PermissionRequiredMixin, TemplateView):
    permission_denied_message = "you do not have permission  to add transfer"
    permission_required = ['transfer.add_transfer']
    raise_exception = True

    def get(self, request, *args, **kwargs):
        if 'products' in request.session.keys():
            del request.session['products']

        return redirect('products:transfer_product')

class ReceiveTransfer(PermissionRequiredMixin, TemplateView):
    permission_denied_message = 'you do not have permission to receive transfer'
    permission_required = ['transfer.receive_transfer']
    raise_exception = True
    template_name = 'products/receive_transfer.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        transfer = get_object_or_404(Transfer, pk=self.kwargs['transfer_id'])
        transfer_product = TransferProduct.objects.filter(transfer_id = self.kwargs['transfer_id'])
        context['transfer'] = transfer
        context['transfer_product'] = transfer_product

