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


# def booksearch(request):
#     return


# def book_details(request):
#     return


# def bookshelf(request):
#     return


def mybooks(request):
    userId=request.session.get('userId')
    email=request.session.get('email')
    if  request.session.get('role')=='user':
        cursor = connection.cursor()
        cursor.execute("""SELECT Name,Unpaid_fees FROM user WHERE email= %s""", [email])
        row = cursor.fetchall()
        name=row[0][0]
        unpaid_fees=row[0][1]
        cursor = connection.cursor()
        cursor.execute("""SELECT ISBN,Title,Year_of_Publication,copy_number,Genre,Rating,date_of_hold FROM on_hold JOIN book ON on_hold.Book_ID=book.Book_ID WHERE User_ID= %s""", [userId])
        row = cursor.fetchall()
        a=cursor.rowcount
        onhold=[]
        for n in range(a):
            onhold.append({
                'ISBN':row[n][0],
                'Title':row[n][1],
                'Year_of_Publication':row[n][2],
                'Copy_Number':row[n][3],
                'Genre':row[n][4],
                'Rating':row[n][5],
                'date_of_hold':row[n][6]
            })
        onloan=[]
        cursor = connection.cursor()
        cursor.execute("""SELECT ISBN,Title,Year_of_Publication,copy_number,Genre,Rating,Date_of_Issue,Fine FROM on_loan JOIN book ON on_loan.Book_ID=book.Book_ID WHERE User_ID= %s""", [userId])
        row = cursor.fetchall()
        a=cursor.rowcount
        for n in range(a):
            onhold.append({
                'ISBN':row[n][0],
                'Title':row[n][1],
                'Year_of_Publication':row[n][2],
                'Copy_Number':row[n][3],
                'Genre':row[n][4],
                'Rating':row[n][5],
                'date_of_issue':row[n][6],
                'Fine':row[n][7]
            })
        onloan_onhold=[] 
        cursor = connection.cursor()
        cursor.execute("""SELECT  ISBN,Title,Year_of_Publication,Genre,Rating,Time_stamp FROM on_loan_on_hold JOIN book ON on_loan_on_hold.Book_ID=book.Book_ID WHERE User_ID= %s""", [userId])
        row = cursor.fetchall()
        a=cursor.rowcount
        for n in range(a):
            onhold.append({
                'ISBN':row[n][0],
                'Title':row[n][1],
                'Year_of_Publication':row[n][2],
                'Genre':row[n][3],
                'Rating':row[n][4],
                'timestamp':row[n][5],
            })  
        data={
            'Name':name,
            'Unpaid_fees':unpaid_fees,
            'onhold':onhold,
            'onloan':onloan,
            'onloan_onhold':onloan_onhold
        }
        return render(request,'library/mybooks.html',data)
    elif request.session.get('email')!=None:
        return render(request,'authentication/page_not_found.html')
    else:
        return render(request,'authentication/error.html')



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
