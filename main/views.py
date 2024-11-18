from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Product, Like, Comment, Cart


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product_list')
        else:
            return redirect('login')
    return render(request, 'main/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')



def product_list(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort_by', 'name')

    # Qidiruv va sortlash
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'name':
        products = products.order_by('name')

    # Pagination
    paginator = Paginator(products, 5)  # Har bir sahifada 5 mahsulot
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/product_list.html', {
        'products': page_obj,  # Mahsulotlar sahifaga bo'linadi
        'query': query,
        'paginator': paginator,
        'page_obj': page_obj,
    })
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    likes = Like.objects.filter(product=product)
    comments = Comment.objects.filter(product=product)
    return render(request, 'main/product_detail.html', {'product': product, 'likes': likes, 'comments': comments})


@login_required
def liked_products(request):

    liked_products = Like.objects.filter(user=request.user, liked=True).values_list('product', flat=True)
    products = Product.objects.filter(id__in=liked_products)
    return render(request, 'main/liked_products.html', {'liked_products': products})

@login_required
def like_product(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    user_like, created = Like.objects.get_or_create(product=product, user=request.user)

    if user_like:
        user_like.liked = not user_like.liked
        user_like.save()

    return redirect('liked_products')

@login_required
def add_comment(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        comment_text = request.POST['comment_text']
        Comment.objects.create(product=product, user=request.user, comment_text=comment_text)
        return redirect('product_detail', product_id=product.id)


@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'main/cart.html', {'cart_items': cart_items})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(product=product, user=request.user)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_view')
