from django.urls import path , include
from vtujedi.views import *



urlpatterns = [
    
    path('', anonymousHome),

    path('login/', signin),

    path('signup/', signup),

    path('logout/', signout),

    path('home/<slug:username>/', loggedUser),

    path('account/<slug:username>/', loggedUserAccount),

    path('sellbook/<slug:username>/', sellBook),

    path('addtocart/<int:book_id>/',add_to_cart),

    path('showbook/<int:book_id>/',showbook),

    path('cart/<slug:username>/',cartView),

    path('delete-from-cart/<int:item>/',deletefromcart),

    path('checkout/<slug:username>/',checkoutPage),

    path('placeorder/<slug:username>/',placeOrder),

    path('edit/<slug:username>/',editAccount),


    # path('updateprofile/<slug:username>/',updateProfile),

]