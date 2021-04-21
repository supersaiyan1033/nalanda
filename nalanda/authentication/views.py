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

# # Create your views here.


def Home(request):
    if request.session.get('role') == 'user':
        url = "http://127.0.0.1:8000/home"
        return redirect(url)
    elif request.session.get('role') == 'librarian':
        url = "http://127.0.0.1:8000/librarian/home"
        return redirect(url)
        return render(request, 'library/librarian.html')
    elif request.session.get('role') != None:
        return render(request, 'authentication/page_not_found.html')
    else:
        return render(request, 'authentication/home.html')


def About_us(request):
    return render(request, 'authentication/about_us.html')


def Contact_us(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        message = request.POST.get('message')
        cursor = connection.cursor()
        cursor.execute(
            """SELECT email FROM librarian WHERE librarian_ID=%d""", ['1'])
        a = cursor.rowcount
        row = cursor.fetchall()
        admins = []
        for n in range(a):
            admins.append(row[n][0])

        send_mail(subject='Contact us', from_email='nalanda3306@gmail.com', recipient_list=admins,
                  html_message='<h4>from:{}</h4><br><h4>to:Respected Admins</h4><br><h3>{}</h3>'.format(email, message), message=message)
        messages.success(request, 'sent successfully')
        return render(request, 'authentication/contact_us.html')
    else:
        return render(request, 'authentication/contact_us.html')


def Log_In(request):
    request.session.flush()
    request.session.clear_expired()
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        if role == "user":
            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM user WHERE email= %s""", [email])
            row = cursor.fetchall()
            if cursor.rowcount == 1:
                dbpassword = row[0][4]
                userId = row[0][0]
                category = row[0][5]
                if bcrypt.checkpw(password.encode('utf8'), dbpassword.encode('utf8')):
                    request.session['userId'] = userId
                    request.session['email'] = email
                    request.session['role'] = role
                    request.session['category'] = category
                    messages.success(request, 'Login successful!!')
                    url = "http://127.0.0.1:8000/home"
                    return redirect(url)

                else:

                    messages.success(
                        request, 'incorrect password please try again!!')
                    # return render(request, 'authentication/login.html')
            else:
                messages.error(
                    request, 'Account does not exist with the entered credentials!! signup to create an account')
                # return render(request, 'authentication/login.html')
        else:
            cursor = connection.cursor()
            cursor.execute(
                """SELECT * FROM librarian WHERE email= %s""", [email])
            row = cursor.fetchall()
            if cursor.rowcount == 1:
                dbpassword = row[0][2]
                librarianId = row[0][0]
                if bcrypt.checkpw(password.encode('utf8'), dbpassword.encode('utf8')):

                    request.session['librarianId'] = row[0][0]
                    request.session['role'] = role
                    request.session['email'] = email
                    messages.success(request, 'Login successful!!')
                    url = "http://127.0.0.1:8000/librarian/home"
                    return redirect(url)

                else:

                    messages.error(
                        request, 'incorrect password please try again!!')
                    # return render(request, 'authentication/login.html')
            else:
                messages.error(
                    request, 'Account does not exist with the entered credentials!!')
                return render(request, 'authentication/login.html')
    return render(request, 'authentication/login.html')


def Sign_Up(request):
    if request.method == "POST":
        Name = request.POST.get('Name')
        category = request.POST.get('Category')
        address = request.POST.get('address')
        DOB = request.POST.get('DOB')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM user WHERE email = %s""", [email])
        row = cursor.fetchall()
        if cursor.rowcount == 0:
            request.session['name'] = Name
            request.session['category'] = category
            request.session['address'] = address
            request.session['DOB'] = DOB
            request.session['email'] = email
            request.session['password'] = password
            otp = get_random_string(6, allowed_chars='0123456789')
            request.session['otp'] = otp
            send_mail(subject='{} is your Pack your bags OTP'.format(otp), message='click on the below link to Verify your email.Note that this link will only be active for 10minutes.', from_email='nalanda3306@gmail.com', recipient_list=[email], fail_silently=True,
                      html_message="<h2>Please enter the below OTP to complete your verification.Note that this OTP will only be active for 10minutes.</h2><br><h2>{}</h2>".format(otp))
            request.session['email_link_is_active'] = True
            messages.success(
                request, 'OTP sent to your email please check your inbox!!')
            return redirect('http://127.0.0.1:8000/login/emailverification')
        else:
            messages.success(
                request, 'User with the entered email already exists please login to continue!!!')
            return redirect('http://127.0.0.1:8000/login')

    else:
        return render(request, 'authentication/signup.html')


def Verify_User_by_website(request):
    if request.session.get('email_link_is_active'):
        if request.method == 'POST':
            otp = request.POST.get('otp')
            cursor = connection.cursor()
            if request.session.get('otp') != None:
                otp_from_email = request.session.get('otp')
                if otp == otp_from_email:
                    name = request.session.get('name')
                    email = request.session.get('email')
                    DOB = request.session.get('DOB')
                    category = request.session.get('category')
                    address = request.session.get('address')
                    password = request.session.get('password')
                    password = bcrypt.hashpw(password.encode(
                        'utf8'), bcrypt.gensalt(rounds=12))
                    cursor.execute("""INSERT INTO user(Name,email,DOB,Password,Category,Address) VALUES (%s,%s,%s,%s,%s,%s)""", (
                        name, email, DOB, password, category, address))
                    messages.success(
                        request, 'verification successful!!please  login to continue')
                    return redirect('/login')
                else:
                    messages.success(request, 'invalid otp try again!!')
                    return redirect('/login/emailverification')

            else:
                messages.success(request, 'Signup before email verification!!')
                return redirect('/signup')
        else:
            return render(request, 'authentication/verify_email.html')
    else:
        return render(request, 'authentication/error.html')


def Forgot_Password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        role = request.POST.get('role')
        if role == 'user':
            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM user WHERE email= %s""", [email])
        else:
            cursor = connection.cursor()
            cursor.execute(
                """SELECT * FROM librarian WHERE email= %s""", [email])
        if cursor.rowcount == 1:
            send_mail(subject='reset password request', message='click on the below link to reset your password.Note that this link will only be active for 10minutes.', from_email='nalanda3306@gmail.com', recipient_list=[email], fail_silently=False,
                      html_message="<h1> click on the below link to reset your password.Note that this link will only be active for 10minutes.</h1><br><a href='http://127.0.0.1:8000/login/forgotpassword/{}/{}/resetpassword'>to reset your password click here</a>".format(role, email))
            request.session['link_is_active'] = True
            messages.success(
                request, 'reset link sent to the entered mail please check your inbox!!')
            return render(request, 'authentication/forgotpassword.html')
        else:
            messages.success(
                request, 'account with the entered email doesnt exist')
            return render(request, 'authentication/forgotpassword.html')
    else:
        return render(request, 'authentication/forgotpassword.html')


def Profile(request):
    UserId = request.session.get('userId')
    email = request.session.get('email')
    if request.session.get('role') == 'user':
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM user WHERE email= %s""", [email])
        row = cursor.fetchall()

        dateOfBirth = row[0][3].strftime("%Y-%m-%d")
        data = {
            'userId': row[0][0],
            'Name': row[0][1],
            'email': row[0][2],
            'DOB': dateOfBirth,
            'Password': row[0][4],
            'address': row[0][6]
        }
        if request.method == "POST":
            Name = request.session.get('Name')
            email = request.session.get('email')
            DOB = request.session.get('DOB')
            Category = request.session.get('Category')
            address = request.session.get('Address')
            password = request.session.get('Password')
            if bcrypt.checkpw(password.encode('utf8'), data['Password'].encode('utf8')):
                messages.success(request, 'Profile is Updated Successfully!')
                cursor.execute("""UPDATE user SET Name=%s,Address=%s,email=%s,DOB=%s WHERE UserId=%s """,
                               (Name, address, email, DOB, data['userId']))
                return redirect('http://127.0.0.1:8000/home')
            else:
                messages.success(
                    request, 'incorrect password please try again!!')
                return render(request, 'authentication/profile.html', data)
        else:
            return render(request, "authentication/profile.html", data)
    else:
        return render(request, 'authentication/error.html')


def ChangePassword(request):
    userId = request.session.get('userId')
    email = request.session.get('email')
    if request.session.get('email') == email:
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM user WHERE email= %s """, [email])
        row = cursor.fetchall()
        dbPassword = row[0][4]
        if request.method == "POST":
            oldPassword = request.POST.get('oldpassword')
            newPassword = request.POST.get('newpassword')
            confirmPassword = request.POST.get('confirmpassword')
            if bcrypt.checkpw(oldPassword.encode('utf8'), dbPassword.encode('utf8')):
                if newPassword == confirmPassword:
                    dbPassword = bcrypt.hashpw(newPassword.encode(
                        'utf8'), bcrypt.gensalt(rounds=12))
                    cursor.execute(
                        """UPDATE user SET Password=%s WHERE email=%s""", (dbPassword, email))
                    messages.success(request, 'Password changed successfully!')
                    return redirect('http://127.0.0.1:8000/home')
                else:
                    messages.success(
                        request, 'new password and confirm password must be the same!!')
                    return render(request, 'authentication/changepassword.html')
            else:
                messages.success(request, 'incorrect password!!')
                return render(request, 'authentication/changepassword.html')

        else:
            return render(request, 'authentication/changepassword.html')
    else:
        return render(request, 'authentication/error.html')


def Reset_Password(request, role, email):
    if request.session.get('link_is_active'):
        if request.method == 'POST':
            newpassword = request.POST.get('newpassword')
            confirmpassword = request.POST.get('confirmpassword')
            if newpassword == confirmpassword:
                cursor = connection.cursor()
                dbPassword = bcrypt.hashpw(newpassword.encode(
                    'utf8'), bcrypt.gensalt(rounds=12))
                if role == 'user':
                    cursor.execute(
                        """UPDATE user SET Password=%s WHERE email=%s""", (dbPassword, email))
                else:
                    cursor.execute(
                        """UPDATE librarian SET Password=%s WHERE email=%s""", (dbPassword, email))
                messages.success(request, 'Password changed successfully!')
                return redirect('http://127.0.0.1:8000/login')
            else:
                messages.success(request, 'both fileds must be the same!!')
                return render(request, 'authentication/reset_password.html')

        else:
            return render(request, 'authentication/reset_password.html')
    else:
        return render(request, 'authentication/error.html')


def user(request):
    userId = request.session.get('userId')
    email = request.session.get('email')
    if request.session.get('role') == 'user':
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM user WHERE email= %s""", [email])
        row = cursor.fetchall()
        dateOfBirth = row[0][3].strftime("%Y-%m-%d")
        fees = row[0][7]
        if fees == None:
            fees = 0
        data = {
            'Name': row[0][1],
            'Unpaid_fees': fees
        }

        return render(request, 'library/user.html', data)
    elif request.session.get('role') != None:
        return render(request, 'authentication/page_not_found.html')
    else:
        return render(request, 'authentication/error.html')


def librarian(request):
    librarianId = request.session.get('librarianId')
    email = request.session.get('email')
    if request.session.get('role') == 'librarian':
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM librarian WHERE email= %s""", [email])
        row = cursor.fetchall()
        dateOfBirth = row[0][5].strftime("%Y-%m-%d")
        data = {
            'librarianId': row[0][0],
            'Name': row[0][1],
            'address': row[0][3],
            'email': row[0][4],
            'DOB': dateOfBirth,

        }

        return render(request, 'library/librarian.html', data)
    elif request.session.get('role') != None:
        return render(request, 'authentication/page_not_found.html')
    else:
        return render(request, 'authentication/error.html')
