from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from django.utils import timezone
from django.db.models import Sum, F, ExpressionWrapper, FloatField

import src.apps.core.forms as forms
import src.core.models as core_models
import src.documents.models as document_models


def home(request):
    today = timezone.now().date()
    doc_order = document_models.DocOrder.objects.filter(added_at__year=today.year)
    total_sold_sum = doc_order.filter(
        added_at__year=today.year, status="completed").aggregate(total_sold_sum=Sum("total_sum"))["total_sold_sum"]
    total_paid_sum = doc_order.filter(
        added_at__year=today.year, status="completed").aggregate(total_paid_sum=Sum("paid_amount"))["total_paid_sum"]

    total_order_return_sum = document_models.DocOrderReturn.objects.filter(
        added_at__year=today.year).aggregate(total_sum=Sum("total_sum"))["total_sum"]

    total_purchase_sum = document_models.DocPurchase.objects.filter(
        added_at__year=today.year, status="completed").aggregate(
        purchase_sum=Sum("total_purchase_sum"))["purchase_sum"]

    total_debt = core_models.CustomerDebt.objects.aggregate(debts=Sum("total_debt"))["debts"]
    total_product_price = document_models.Warehouse.objects.annotate(
        total_sell_price=ExpressionWrapper(
            F('quantity') * F('sell_price'),
            output_field=FloatField()
        )
    ).aggregate(total_price=Sum('total_sell_price'))["total_price"]

    count_customer = core_models.Customer.objects.count()
    count_orders = doc_order.count()
    count_orders_pending = doc_order.filter(status="pending", added_at__year=today.year).count()

    little_of_products = document_models.Warehouse.objects.order_by("quantity")[:10]

    organization_debt = core_models.OrganizationDebt.objects.aggregate(total_debt=Sum("debt_amount"))["total_debt"]

    context = {
        "total_purchase_sum": f"{total_purchase_sum if total_purchase_sum else 0:,.2f}",
        "total_sold_sum": f"{total_sold_sum if total_sold_sum else 0:,.2f}",
        "total_paid_sum": f"{total_paid_sum if total_paid_sum else 0:,.2f}",
        "organization_debt": f"{organization_debt if organization_debt else 0:,.2f}",
        "total_order_return_sum": f"{total_order_return_sum if total_order_return_sum else 0:,.2f}",
        "total_debt": f"{total_debt if total_debt else 0:,.2f}",
        "total_product_price": f"{total_product_price if total_product_price else 0:,.2f}",
        "count_customers": f"{count_customer}",
        "count_orders": f"{count_orders}",
        "count_orders_pending": f"{count_orders_pending}",
        "last_orders": doc_order[:11],
        "little_of_products": little_of_products,
    }

    return render(request, 'pages/dashboard.html', context)


def custom_login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = forms.CustomLoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username,
                                password=password)  # Foydalanuvchini autentifikatsiya qilish
            if user is not None:
                login(request, user)  # Bu yerda 'user' obyektini login() ga uzatamiz
                messages.success(request, 'You are now logged in!')
                return redirect('home')  # Muvaffaqiyatli login bo'lgandan keyin
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')

    else:
        form = forms.CustomLoginForm()

    return render(request, 'auth/login.html', {'form': form})
