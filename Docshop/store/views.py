from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from store.models import Product, Cart, Order


def accueil(request):
    products = Product.objects.all()
    return render(request,'store/accueil.html', context={"products": products})


def index(request):
    products = Product.objects.all()
    return render(request,'store/index.html', context={"products": products})

def Livraison(request):
    return render(request, 'store/Livraison.html')


def contact(request):
    return render(request, 'store/contact.html')


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/detail.html', context={"product": product})


def add_to_cart(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug= slug)
    cart, _ = Cart.objects.get_or_create(user=user)
    order, created = Order.objects.get_or_create(user=user,ordered=False, product=product)

    if created:
        cart.orders.add(order)
        cart.save()
    else:
        order.quantity += 1
        order.save()

    return redirect(reverse("product", kwargs={"slug": slug}))


def cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    total = cart.somme_totale()
    orders = cart.orders.all()

    context = {
        'orders': orders,
        'total': total,
    }

    # context={"orders": cart.orders.all()}
    return render(request, 'store/cart.html',context)


def delete_cart(request):
    if cart:=request.user.cart:
        cart.delete()

    return redirect('index')


def product_list(request):
    query = request.GET.get('q')
    products = []
    if query:
        #products = Product.objects.filter(name__icontains=query)
        products = Product.objects.filter(name__icontains=query) | Product.objects.filter(description__icontains=query)

    else:
        products = Product.objects.all()
    
    return render(request, 'index.html', {'products': products, 'query': query})







