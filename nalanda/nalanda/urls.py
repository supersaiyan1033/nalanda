"""nalanda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from authentication import views as auth_views
from library import views as lib_views

urlpatterns = [
    # auth views
    path('admin/', admin.site.urls),
    path('', auth_views.Home, name='home'),
    path('contactus', auth_views.Contact_us, name="Contact-us"),
    path('aboutus', auth_views.About_us, name="about-us"),
    path('login/', auth_views.Log_In, name='auth-login'),
    path('login/emailverification',
         auth_views.Verify_User_by_website, name='auth-verify'),
    path('login/forgotpassword', auth_views.Forgot_Password, name='forgot_password'),
    path('login/forgotpassword/<role>/<email>/resetpassword',
         auth_views.Reset_Password, name='reset password'),
    path('signup/', auth_views.Sign_Up, name='auth-signup'),
    path('profile', auth_views.Profile, name='profile'),
    path('home', auth_views.user, name='user'),
    path('librarian/home', auth_views.librarian, name='librarian'),
    path('changepassword', auth_views.ChangePassword, name="changepassword"),
    path('librarian/changepassword', lib_views.librarian_ChangePassword,name="librarian-changepassword"),

    #     # user views
    path('booksearch/', lib_views.booksearch, name='booksearch'),
    #     path('booksearch/<isbn>/', lib_views.book_details, name='book_details'),
    path('bookshelf', lib_views.bookshelf, name='bookshelf'),
    path('mybooks', lib_views.mybooks, name='mybooks'),
    #     # friends urls
    #     path('friends', lib_views.friends, name='friends'),
    #     path('friends/list', lib_views.friends_list, name='friends_list'),
    #     path('friends/pending', lib_views.pending_requests, name='pending_requests'),
    #     path('friends/add', lib_views.add_friend, name='add_friend'),
    #     path('friends/list/<userId>/bookshelf',
    #          lib_views.friends_bookshelf, name='friends_bookshelf'),

    #     # librarian urls
    path('librarian/book', lib_views.book, name='book'),
    path('librarian/book/add', lib_views.add_book, name='add_book'),
    path('librarian/book/update', lib_views.update_book, name='update_book'),
    # path('librarian/book/update/<isbn>/',
    #      lib_views.update_book_isbn, name='update_book_isbn'),
    # path('librarian/book/delete', lib_views.delete, name='delete'),

        path('librarian/issue', lib_views.issue, name='issue'),
        path('librarian/issue/available',
             lib_views.issue_available, name='issue_available'),
        path('librarian/issue/onhold/',
             lib_views.issue_onHold, name='issue_onHold'),
        path('librarian/return', lib_views.return_book, name='return'),

    #     # shelf urls
        path('librarian/shelf', lib_views.shelf, name='shelf'),
        path('librarian/shelf/update', lib_views.shelf_update, name='shelf_update'),
        path('librarian/shelf/add', lib_views.shelf_add, name='shelf_add'),
        # path('librarian/shelf/delete', lib_views.shelf_delete, name='shelf_delete'),






]
