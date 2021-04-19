from django.shortcuts import render, redirect
from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.db import connection
from django.contrib import messages
import bcrypt
import hashlib
import sys
import base64
from datetime import datetime
from datetime import date
from django.http import HttpResponse
from django.template.loader import get_template
import smtplib
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.utils.crypto import get_random_string

# Create your views here.


def booksearch(request):
    userId = request.session.get('userId')
    email = request.session.get('email')
    category = request.session.get('category')
    if category == 'Student' or category == 'Faculty':
        cursor = connection.cursor()
        user = cursor.execute(
            """ select Unpaid_fees from user where User_Id=%s""", [userId])
        print(user)
        fines = user
        if fines == None:
            fines = 0

        if 'review' in request.POST:
            isbn = request.POST.get('review')
            rating = request.POST.get('rating'),
            review = request.POST.get('review_content')
            cursor.execute(
                """ select User_Id from review where User_Id =%s and ISBN=%s""", (userId, isbn))
            c = cursor.rowcount
            if c > 0:
                messages.error(request, "You have already reviewed this book")
            else:
                cursor.execute(
                    """ insert into review(Review,ISBN,User_Id,Rating) values(%s,%s,%s,%s) """, (review, isbn, userId, rating))
                messages.success(
                    request, 'rating and review submitted successfully!')
        elif 'hold' in request.POST:
            isbn = request.POST.get('hold')
            cursor.execute(
                """ select User_Id from on_hold where User_Id = %s and """)
        elif 'add_to_shelf' in request.POST:
            isbn = request.POST.get('add_to_shelf')
            print(userId)
            cursor.execute(
                """ select User_Id from reading_list where User_Id=%s and ISBN=%s""", (userId, isbn))
            b = cursor.rowcount
            if b > 0:
                messages.error(request, "Book already in your shelf!!")
            cursor.execute(
                """insert into reading_list(User_Id,ISBN) values(%s,%s) """, (userId, isbn))
            messages.success(request, "Book added to shelf")
        search_category = request.GET.get('search_category')
        search_key = request.GET.get('search_key')
        if search_category == 'ISBN':
            cursor.execute(
                """ select * from  isbn where ISBN=%s""", [search_key])
        if search_category == 'Genre':
            cursor.execute(
                """  select * from isbn where Genre=%s""", [search_key])
        if search_category == 'Title':
            cursor.execute(
                """ select * from isbn where Title=%s""",  [search_key])
        if search_category == 'catalogue':
            cursor.execute(
                """ select * from isbn where Genre=%s or Title=%s or ISBN=%s """, [search_key, search_key, search_key])
        if search_category == None:
            cursor.execute("""select * from isbn""")
        row = cursor.fetchall()
        a = cursor.rowcount
        if a != 0:

            books = []
            for n in range(a):
                cursor.execute(
                    """ select  count(*) from review where ISBN=%s""", [row[n][0]])
                col = cursor.fetchall()
                if row[n][6] == None:
                    range_of_rating = 0
                else:
                    range_of_rating = row[n][6]
                books.append({
                    'ISBN': row[n][0],
                    'Title': row[n][1],
                    'Year': row[n][2],
                    'Genre': row[n][3],
                    'Author': row[n][4],
                    'Publisher': row[n][5],
                    'stars': range(1, range_of_rating+1),
                    'no_stars': range(1, 5-range_of_rating+1),
                    'votes': col[0][0]
                })
        if a != 0:
            data = {
                'books': books,
                'category': search_category,
                'key': search_key,
                'fines': fines
            }
        else:
            data = {
                'books': None,
                'category': None,
                'key': None,
                'fines': fines
            }

        return render(request, 'library/book_search.html', data)

    elif request.session.get('email') != None:
        # return render(request, 'library/book_search.html')
        return render(request, 'authentication/page_not_found.html')
    else:
        return render(request, 'authentication/error.html')


# def book_details(request):
#     return


# def bookshelf(request):
#     return


def mybooks(request):
    userId = request.session.get('userId')
    email = request.session.get('email')
    if request.session.get('role') == 'user':
        cursor = connection.cursor()
        cursor.execute(
            """SELECT Name,Unpaid_fees FROM user WHERE email= %s""", [email])
        row = cursor.fetchall()
        name = row[0][0]
        unpaid_fees = row[0][1]
        cursor = connection.cursor()
        cursor.execute(
            """SELECT ISBN,Title,Year_of_Publication,copy_number,Genre,Rating,date_of_hold FROM on_hold JOIN book ON on_hold.Book_ID=book.Book_ID WHERE User_ID= %s""", [userId])
        row = cursor.fetchall()
        a = cursor.rowcount
        onhold = []
        for n in range(a):
            onhold.append({
                'ISBN': row[n][0],
                'Title': row[n][1],
                'Year_of_Publication': row[n][2],
                'Copy_Number': row[n][3],
                'Genre': row[n][4],
                'Rating': row[n][5],
                'date_of_hold': row[n][6]
            })
        onloan = []
        cursor = connection.cursor()
        cursor.execute(
            """SELECT ISBN,Title,Year_of_Publication,copy_number,Genre,Rating,Date_of_Issue,Fine FROM on_loan JOIN book ON on_loan.Book_ID=book.Book_ID WHERE User_ID= %s""", [userId])
        row = cursor.fetchall()
        a = cursor.rowcount
        for n in range(a):
            onhold.append({
                'ISBN': row[n][0],
                'Title': row[n][1],
                'Year_of_Publication': row[n][2],
                'Copy_Number': row[n][3],
                'Genre': row[n][4],
                'Rating': row[n][5],
                'date_of_issue': row[n][6],
                'Fine': row[n][7]
            })
        onloan_onhold = []
        cursor = connection.cursor()
        cursor.execute(
            """SELECT  ISBN,Title,Year_of_Publication,Genre,Rating,Time_stamp FROM on_loan_on_hold JOIN book ON on_loan_on_hold.Book_ID=book.Book_ID WHERE User_ID= %s""", [userId])
        row = cursor.fetchall()
        a = cursor.rowcount
        for n in range(a):
            onhold.append({
                'ISBN': row[n][0],
                'Title': row[n][1],
                'Year_of_Publication': row[n][2],
                'Genre': row[n][3],
                'Rating': row[n][4],
                'timestamp': row[n][5],
            })
        data = {
            'Name': name,
            'Unpaid_fees': unpaid_fees,
            'onhold': onhold,
            'onloan': onloan,
            'onloan_onhold': onloan_onhold
        }
        return render(request, 'library/mybooks.html', data)
    elif request.session.get('email') != None:
        return render(request, 'authentication/page_not_found.html')
    else:
        return render(request, 'authentication/error.html')


# def friends(request):
#     return


# def friends_list(request):
#     return


# def pending_requests(request):
#     return


# def add_friend(request):
#     return


# def friends_bookshelf(request):
#     return


# librarian rocks
