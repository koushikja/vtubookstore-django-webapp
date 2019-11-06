from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage

from django.http import JsonResponse



from vtujedi.models import *

 
def anonymousHome(request):
    showbooks = Book.objects.all()
    branches = Branch.objects.all()
    sems = Sem.objects.all()
    return render(request , "home.html" , {"books": showbooks , "branches":branches , "sems":sems})

def signup(request):
    branches = Branch.objects.all()
    sem = Sem.objects.all()
    if request.method=="POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        email = request.POST.get("email")
        user_phone=request.POST.get("user_phone")
        user_address=request.POST.get("user_address")
        user_branch=request.POST.get("user_branch")
        user_sem=request.POST.get("user_sem")
        
        sem = Sem.objects.get(pk = int(user_sem))
        branch = Branch.objects.get(pk = int(user_branch))
        exists = User.objects.filter(username=username).exists()
        
        if not exists:
            user_info = User.objects.create_user(username,email,password)
            profile=UserDetail.objects.create(user_info=user_info,user_sem=sem,user_branch=branch,user_address=user_address,user_phone=user_phone)
            profile.save()
            return redirect('/login/')
    return render(request,"signup.html",{"branches":branches , "sem":sem})

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect(f'/home/{user.username}/')
        elif user is None:
            return redirect(f'/login/')
        else:
            # Return an 'invalid login' error message.
            return HttpResponse('invalid user')
    return render(request,"signin.html")

def signout(request):

    logout(request)
    return redirect(f'/')

@login_required
def loggedUser(request,username):
    if request.user.is_authenticated:
        user = request.user
        userdetail = user.userdetail
        branches = Branch.objects.all()
        sems = Sem.objects.all()
        showbooks = Book.objects.all()
        return render(request , "home.html" , {"books": showbooks, "user":user , "userdetail":userdetail ,"branches":branches , "sems":sems})
    else:
        return redirect(f'/login/')

def loggedUserAccount(request,username):
    user=request.user
    userdetail = user.userdetail
    sem = Sem.objects.all()
    branch = Branch.objects.all()
    return render(request, "account.html",{"user":user , "userdetail":userdetail ,"branch":branch , "sem":sem})

@login_required
def sellBook(request,username):
    user = request.user
    branches = Branch.objects.all()
    sem = Sem.objects.all()
    if request.method == "POST":
        book_img = request.FILES['book_img']
        book_title = request.POST['book_title']
        book_description = request.POST['book_description']
        book_price = request.POST['book_price']
        book_branch = request.POST['book_branch']
        book_sem = request.POST['book_sem']

        sem = Sem.objects.get(pk = int(book_sem))
        branch = Branch.objects.get(pk = int(book_branch))

        book=Book.objects.create(book_img=book_img,book_title=book_title,book_branch=branch,book_description=book_description,book_price=book_price,book_sem=sem,book_seller = user)
        return redirect(f"/home/{user.username}/")

    return render(request, "sellbookform.html",{"user":user,"branches":branches , "sem":sem})

@login_required
def add_to_cart(request, book_id):
    user = request.user 
    if request.method == "POST":
        quantity = int(request.POST.get("quantity"))
        print(quantity)
        print(type(quantity))
        book = Book.objects.get(pk=book_id)
        
        cart_items = Cart.objects.filter(item=book, buyer=user)
        if not cart_items.exists():
            cart = Cart.objects.create(buyer=user, item=book, quantity=quantity)
            message = "Item added to cart"
        else:
            message = "Item already exist in cart"
        
        # return redirect(f"/home/{user.username}/{book.id}/")
        return JsonResponse({"message":message})
    
        
def showbook(request,book_id):
    book = Book.objects.get(pk = book_id)
    return render(request, "showbook.html",{"book": book})


def cartView(request,username):
    user = request.user
    cart = Cart.objects.filter(buyer=user)
    total = 0
    for items in cart:
        q=items.quantity
        p=items.item.book_price
        total_item = p*q
        total = total + total_item
    return render(request,"cart.html" , {"user":user , "cart":cart , "total":total})


def deletefromcart(request,item):
    user = request.user
    item = Cart.objects.get(pk=item)
    item.delete()
    return redirect(f"/cart/{user.username}/")

@login_required
def checkoutPage(request,username):
    user=request.user
    cart = Cart.objects.filter(buyer=user)
    total = 0
    for items in cart:
        q=items.quantity
        p=items.item.book_price
        total_item = p*q
        total = total + total_item
    return render(request,"checkout.html",{"user":user , "cart":cart , "total":total})

@login_required
def editAccount(request,username):
    user = request.user
    userdetail = user.userdetail
    branches = Branch.objects.all()
    sem = Sem.objects.all()
    if request.method == "POST":
        username=request.POST["username"]
        email=request.POST["email"]
        user_address=request.POST["user_address"]
        user_phone=request.POST["user_phone"]
        user_branch=request.POST["user_branch"]
        user_sem=request.POST["user_sem"]

        user.email = email
        userdetail.user_address = user_address
        userdetail.user_phone = user_phone
        userdetail.user_branch = user_branch
        userdetail.user_sem = user_sem

        return redirect(f"/account/{username}/")
    return render(request,"account.html",{"user":user,"userdetail":userdetail,"branches":branches , "sem":sem})

@login_required
def placeOrder(request,username):
    user=request.user
    email = user.email
    message = "We Have confirmed your order and will be delivered in 3 to 4 business days"
    msg = EmailMessage("Purchase Order", message, to=[email])
    msg.send()
    cartitems = Cart.objects.filter(buyer=user)
    print(cartitems)
    cartitems.delete()
    return redirect(f"/home/{user.username}/")