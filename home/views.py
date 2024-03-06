# views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import View
from django.views.generic.edit import FormView


class LoginView(View):
    template_name = "auth/login.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("/")
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            # Handle invalid login
            pass
        return render(request, self.template_name)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")


from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView

from .forms import AddToCartForm, UpdateCartForm
from .models import Category, Product


class ProductListView(ListView):
    model = Category
    template_name = "product\product_list.html"
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories_with_products = []
        for category in Category.objects.all():
            products = Product.objects.filter(categories=category)
            categories_with_products.append((category, products))
        context["categories_with_products"] = categories_with_products
        cart = self.request.session.get("cart", {})
        context["cart"] = cart
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "product/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get("cart", {})
        context["cart"] = cart
        return context


class AddToCartView(LoginRequiredMixin, FormView):
    def post(self, request, *args, **kwargs):
        product_id = kwargs["pk"]
        quantity = int(request.POST.get("quantity", 1))

        product = Product.objects.get(pk=product_id)

        if "cart" not in request.session:
            request.session["cart"] = {}
        cart = request.session["cart"]
        if product_id in cart:
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity

        if cart[product_id] > product.stock:
            cart[product_id] = product.stock

        request.session.modified = True
        return redirect("cart")


class RemoveFromCartView(LoginRequiredMixin, FormView):
    def post(self, request, *args, **kwargs):
        product_id = str(kwargs["pk"])
        quantity = int(request.POST.get("quantity", 1))

        if "cart" in request.session:
            cart = request.session["cart"]
            if product_id in cart:
                cart[product_id] -= quantity
                if cart[product_id] <= 0:
                    del cart[product_id]
                request.session.modified = True
        return redirect("cart")


class CartView(LoginRequiredMixin, ListView):
    template_name = "product/cart.html"
    context_object_name = "cart_products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get("cart", {})
        context["cart"] = cart
        return context

    def get_queryset(self):
        cart = self.request.session.get("cart", {})
        cart_product_ids = cart.keys()
        return Product.objects.filter(id__in=cart_product_ids)
