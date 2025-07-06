from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from django.db.models import Sum
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from decimal import Decimal, InvalidOperation

from .models import Customer, Product, Invoice, InvoiceItem
from .forms import CustomerForm, ProductForm, InvoiceForm, InvoiceItemForm

# -------------------- Dashboard --------------------
@login_required
def dashboard(request):
    total_customers = Customer.objects.count()
    total_products = Product.objects.count()
    total_invoices = Invoice.objects.count()
    total_unpaid = Invoice.objects.filter(status='Unpaid').count()
    total_paid_amount = Invoice.objects.filter(status='Paid').aggregate(Sum('total'))['total__sum'] or 0
    total_unpaid_amount = Invoice.objects.filter(status='Unpaid').aggregate(Sum('total'))['total__sum'] or 0

    latest_invoices = Invoice.objects.select_related('customer').order_by('-date')[:5]
    recent_customers = Customer.objects.order_by('-id')[:5]

    overview_cards = [
        {"title": "Total Customers", "value": total_customers, "color": "primary", "icon": "bi-people-fill"},
        {"title": "Total Products", "value": total_products, "color": "success", "icon": "bi-box-seam"},
        {"title": "Total Invoices", "value": total_invoices, "color": "dark", "icon": "bi-receipt"},
        {"title": "Unpaid Invoices", "value": total_unpaid, "color": "warning", "icon": "bi-exclamation-circle"},
        {"title": "Total Paid Amount", "value": total_paid_amount, "color": "success", "icon": "bi-currency-rupee"},
        {"title": "Total Unpaid Amount", "value": total_unpaid_amount, "color": "danger", "icon": "bi-cash-stack"},
    ]

    context = {
        'overview_cards': overview_cards,
        'latest_invoices': latest_invoices,
        'recent_customers': recent_customers,
    }
    return render(request, 'invoice_app/home.html', context)


# -------------------- Customer Views --------------------
@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, "invoice_app/customer_list.html", {"customers": customers})

@login_required
def customer_create(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("customer_list")
    else:
        form = CustomerForm()
    return render(request, "invoice_app/customer_form.html", {"form": form, "title": "Add Customer"})

@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect("customer_list")
    else:
        form = CustomerForm(instance=customer)
    return render(request, "invoice_app/customer_form.html", {"form": form, "title": "Edit Customer"})

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
        return redirect("customer_list")
    return render(request, "invoice_app/customer_confirm_delete.html", {"customer": customer})

# -------------------- Product Views --------------------
@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, "invoice_app/product_list.html", {"products": products})

@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "invoice_app/product_form.html", {"form": form, "title": "Add Product"})

@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)
    return render(request, "invoice_app/product_form.html", {"form": form, "title": "Edit Product"})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("product_list")
    return render(request, "invoice_app/product_confirm_delete.html", {"product": product})

# -------------------- Invoice Views --------------------
@login_required
def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, "invoice_app/invoice_list.html", {"invoices": invoices})

@login_required
def create_invoice(request):
    InvoiceItemFormSet = inlineformset_factory(
        Invoice, InvoiceItem, form=InvoiceItemForm, extra=1, can_delete=False
    )

    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.total = Decimal('0.00')  # Default total
            invoice.save()

            formset = InvoiceItemFormSet(request.POST, instance=invoice)

            if formset.is_valid():
                total = Decimal('0.00')
                for item_form in formset:
                    if item_form.cleaned_data:  # Ensure not empty
                        try:
                            item = item_form.save(commit=False)
                            item.invoice = invoice
                            item.item_total = Decimal(item.product.price) * Decimal(item.quantity)
                            item.save()
                            total += item.item_total
                        except (TypeError, InvalidOperation, AttributeError):
                            messages.error(request, "Invalid product or quantity.")
                            return render(request, "invoice_app/create_invoice.html", {
                                'form': form,
                                'formset': formset,
                            })
                invoice.total = total
                invoice.save()
                messages.success(request, "Invoice created successfully!")
                return redirect("invoice_list")
            else:
                messages.error(request, "Please fix the invoice item errors.")
        else:
            formset = InvoiceItemFormSet()  # If invoice form is invalid
            messages.error(request, "Please fill in the invoice form correctly.")
    else:
        form = InvoiceForm()
        formset = InvoiceItemFormSet()

    return render(request, "invoice_app/create_invoice.html", {
        "form": form,
        "formset": formset
    })


@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    items = invoice.items.all()
    return render(request, 'invoice_app/invoice_detail.html', {
        'invoice': invoice,
        'items': items,
    })
