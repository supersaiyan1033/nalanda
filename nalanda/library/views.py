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
    if request.session.get('role') == 'user':
        cursor = connection.cursor()
        user = cursor.execute(
            """ select Unpaid_fees from user where User_Id=%s""", [userId])
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
                    """ insert into review(Review,ISBN,User_ID,Rating) values(%s,%s,%s,%s) """, (review, isbn, userId, rating))
                cursor.execute(
                    """select avg(Rating) from review where isbn=%s""", [isbn])
                average = cursor.fetchall()
                cursor.execute(
                    """update isbn set Rating=%s where isbn=%s""", (average, isbn))
                messages.success(
                    request, 'rating and review submitted successfully!')
        elif 'hold' in request.POST:
            isbn = request.POST.get('hold')
            cursor.execute(
                """ select * from on_hold join book on on_hold.Book_ID=book.Book_ID where book.ISBN=%s and on_hold.User_ID = %s """, (isbn, userId))
            if cursor.rowcount > 0:
                messages.error(request, "You have this book On hold already!!")
            else:
                cursor.execute(
                    """select * from on_loan_on_hold where ISBN=%s and User_ID=%s""", (isbn, userId))
                if cursor.rowcount > 0:
                    messages.error(
                        request, "You have this book On Loan On Hold already!!")
                else:
                    cursor.execute(
                        """ select book.Copy_number,book.Book_ID from isbn join book on isbn.ISBN=book.ISBN where book.ISBN=%s and book.Status=%s""", (isbn, "On shelf"))
                    if cursor.rowcount > 0:
                        records = cursor.fetchall()
                        print(records)
                        copy_no = records[0][0]
                        book_id = records[0][1]
                        now = datetime.now()
                        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
                        cursor.execute(
                            """ insert into on_hold(date_of_hold,User_ID,Book_ID) values(%s,%s,%s)""", (date_time, userId, book_id))
                        messages.success(
                            request, "Book hold successful valid for 10days from now!!")
                    else:
                        now = datetime.now()
                        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
                        cursor.execute(
                            """update book set Status=%s where isbn=%s and Status=%s""", ('On loan and On hold', isbn, 'On loan'))
                        cursor.execute(
                            """ insert into on_loan_on_hold(User_Id,Time_stamp,ISBN) values(%s,%s,%s) """, (userId, date_time, isbn))
                        messages.success(
                            request, "Book in On Loan and On hold. Book will be alloted according to the waiting list")
        elif 'add_to_shelf' in request.POST:
            isbn = request.POST.get('add_to_shelf')
            cursor.execute(
                """ select User_Id from reading_list where User_Id=%s and ISBN=%s""", (userId, isbn))
            b = cursor.rowcount
            if b > 0:
                messages.error(request, "Book already in your shelf!!")
            else:
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
                    'votes': col[0][0],
                    'image_url': row[n][8]
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

    elif request.session.get('role') != None:
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
            """SELECT isbn.ISBN,Title,Year_of_Publication,Copy_number,Genre,Rating,date_of_hold,Author,Publisher FROM on_hold JOIN book ON on_hold.Book_ID=book.Book_ID JOIN isbn ON book.ISBN=isbn.ISBN WHERE User_ID= %s""", [userId])
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
                'date_of_hold': row[n][6],
                'Author': row[n][7],
                'Publisher': row[n][8]
            })
        onloan = []
        cursor = connection.cursor()
        cursor.execute(
            """SELECT isbn.ISBN,Title,Year_of_Publication,Copy_number,Genre,Rating,Date_of_Issue,Fine,Author,Publisher FROM on_loan JOIN book ON on_loan.Book_ID=book.Book_ID JOIN isbn ON book.ISBN=isbn.ISBN WHERE User_ID= %s""", [userId])
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
                'Fine': row[n][7],
                'Author': row[n][8],
                'Publisher': row[n][9]
            })
        onloan_onhold = []
        cursor = connection.cursor()
        cursor.execute(
            """SELECT  isbn.ISBN,Title,Year_of_Publication,Genre,Rating,Time_stamp,Author,Publisher FROM on_loan_on_hold JOIN isbn ON on_loan_on_hold.ISBN=isbn.ISBN WHERE User_ID= %s""", [userId])
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
                'Author': row[n][6],
                'Publisher': row[n][7]
            })
        cursor = connection.cursor()
        cursor.execute(
            """SELECT isbn.ISBN,Title,Year_of_Publication,Copy_number,Genre,Rating,Date_of_issue,Date_of_return,Fine,Author,Publisher FROM previous_books JOIN book ON previous_books.Book_ID=book.Book_ID JOIN isbn ON book.ISBN=isbn.ISBN WHERE User_ID= %s""", [userId])
        row = cursor.fetchall()
        a = cursor.rowcount
        previous = []
        for n in range(a):
            previous.append({
                'ISBN': row[n][0],
                'Title': row[n][1],
                'Year_of_Publication': row[n][2],
                'Copy_Number': row[n][3],
                'Genre': row[n][4],
                'Rating': row[n][5],
                'date_of_issue': row[n][6],
                'date_of_return': row[n][7],
                'Fine': row[0][8],
                'Author': row[n][9],
                'Publisher': row[n][10]
            })
        data = {
            'Name': name,
            'Unpaid_fees': unpaid_fees,
            'onhold': onhold,
            'onloan': onloan,
            'onloan_onhold': onloan_onhold,
            'previous': previous
        }
        return render(request, 'library/mybooks.html', data)
    elif request.session.get('role') != None:
        return render(request, 'authentication/page_not_found.html')
    else:
        return render(request, 'authentication/error.html')


def bookshelf(request):
    userId = request.session.get('userId')
    email = request.session.get('email')
    if request.session.get('role') == 'user':
        if 'delete' in request.POST:
            isbn = request.POST.get('delete')
            cursor = connection.cursor()
            cursor.execute(
                """DELETE FROM reading_list WHERE User_ID=%s AND ISBN=%s""", (userId, isbn))
            cursor = connection.cursor()
            cursor.execute(
                """SELECT Name,Unpaid_fees FROM user WHERE email= %s""", [email])
            row = cursor.fetchall()
            name = row[0][0]
            unpaid_fees = row[0][1]
            cursor = connection.cursor()
            cursor.execute(
                """SELECT isbn.ISBN,Title,Year_of_Publication,Genre,Rating,Author,Publisher FROM reading_list JOIN isbn ON reading_list.ISBN=isbn.ISBN  WHERE User_ID= %s""", [userId])
            row = cursor.fetchall()
            a = cursor.rowcount
            reading_list = []
            for n in range(a):
                cursor.execute(
                    """ select  count(*) from review where ISBN=%s""", [row[n][0]])
                col = cursor.fetchall()
                if row[n][4] == None:
                    range_of_rating = 0
                else:
                    range_of_rating = row[n][4]
                reading_list.append({
                    'ISBN': row[n][0],
                    'Title': row[n][1],
                    'Year_of_Publication': row[n][2],
                    'Genre': row[n][3],
                    'Rating': row[n][4],
                    'Author': row[n][5],
                    'Publisher': row[n][6],
                    'stars': range(1, range_of_rating+1),
                    'no_stars': range(1, 5-range_of_rating+1),
                    'votes': col[0][0],
                    'image_url': row[n][8]
                })
            data = {
                'Name': name,
                'Unpaid_fees': unpaid_fees,
                'list': reading_list
            }
            messages.success(
                request, 'Book Removed From Shelf successfully !')
            return render(request, 'library/bookshelf.html', data)
        else:
            cursor = connection.cursor()
            cursor.execute(
                """SELECT Name,Unpaid_fees FROM user WHERE email= %s""", [email])
            row = cursor.fetchall()
            name = row[0][0]
            unpaid_fees = row[0][1]
            cursor = connection.cursor()
            cursor.execute(
                """SELECT isbn.ISBN,Title,Year_of_Publication,Genre,Rating,Author,Publisher,Img_link FROM reading_list JOIN isbn ON reading_list.ISBN=isbn.ISBN  WHERE User_ID= %s""", [userId])
            row = cursor.fetchall()
            a = cursor.rowcount
            reading_list = []
            for n in range(a):
                cursor.execute(
                    """ select  count(*) from review where ISBN=%s""", [row[n][0]])
                col = cursor.fetchall()
                if row[n][4] == None:
                    range_of_rating = 0
                else:
                    range_of_rating = row[n][4]
                reading_list.append({
                    'ISBN': row[n][0],
                    'Title': row[n][1],
                    'Year_of_Publication': row[n][2],
                    'Genre': row[n][3],
                    'Rating': row[n][4],
                    'Author': row[n][5],
                    'Publisher': row[n][6],
                    'stars': range(1, range_of_rating+1),
                    'no_stars': range(1, 5-range_of_rating+1),
                    'votes': col[0][0],
                    'image_url': row[n][7]
                })
            data = {
                'Name': name,
                'Unpaid_fees': unpaid_fees,
                'list': reading_list
            }
            return render(request, 'library/bookshelf.html', data)
    elif request.session.get('role') != None:
        return render(request, 'authentication/page_not_found.html')
    else:
        return render(request, 'authentication/error.html')


def librarian_ChangePassword(request):
    librarianId = request.session.get('librarianId')
    email = request.session.get('email')
    if request.session.get('role') == 'librarian':
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM librarian WHERE email= %s """, [email])
        row = cursor.fetchall()
        dbPassword = row[0][2]
        if request.method == "POST":
            oldPassword = request.POST.get('oldpassword')
            newPassword = request.POST.get('newpassword')
            confirmPassword = request.POST.get('confirmpassword')
            if bcrypt.checkpw(oldPassword.encode('utf8'), dbPassword.encode('utf8')):
                if newPassword == confirmPassword:
                    dbPassword = bcrypt.hashpw(newPassword.encode(
                        'utf8'), bcrypt.gensalt(rounds=12))
                    cursor.execute(
                        """UPDATE librarian SET Password=%s WHERE email=%s""", (dbPassword, email))
                    messages.success(request, 'Password changed successfully!')
                    return redirect('http://127.0.0.1:8000/librarian/home')
                else:
                    messages.success(
                        request, 'new password and confirm password must be the same!!')
                    return render(request, 'library/changepassword.html')
            else:
                messages.success(request, 'incorrect password!!')
                return render(request, 'library/changepassword.html')

        else:
            return render(request, 'library/changepassword.html')
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

def book(request):
    userId = request.session.get('userId')
    email = request.session.get('email')
    if request.session.get('role') == 'librarian':

        return render(request, 'library/librarian_books.html')
    elif request.session.get('role') != None:
        return render(request, 'authentication/page_not_found.html')
    else:
        return render(request, 'authentication/error.html')

    # return render(request,'library/page_not_found.html')


def add_book(request):
    userId = request.session.get('userId')
    email = request.session.get('email')
    category = request.session.get('category')
    if request.session.get('role') == 'librarian':
        if 'add_details' in request.POST:
            author = request.POST.get('author')
            genre = request.POST.get('genre')
            publisher = request.POST.get('publisher')
            isbn = request.POST.get('isbn')
            year = request.POST.get('year')
            title = request.POST.get('title')
            image = request.POST.get('image')
            cursor = connection.cursor()
            cursor.execute("""select * from isbn where ISBN=%s""",
                           [isbn])
            if cursor.rowcount > 0:
                messages.error(request, "Book details already exist!!")
            else:
                cursor.execute("""insert into isbn(ISBN,Title,Year_of_Publication,Genre,Author,Publisher,Img_link) values(%s,%s,%s,%s,%s,%s,%s)""",
                               (isbn, title, year, genre, author, publisher, image))
                messages.success(request, "Book details added successfully!!")
        elif 'add_copy' in request.POST:
            isbn = request.POST.get('isbn')
            copy = request.POST.get('copy')
            shelf = request.POST.get('shelf')
            cursor = connection.cursor()
            cursor.execute(
                """select * from book where ISBN=%s and Copy_number=%s and Shelf_ID=%s""", (isbn, copy, shelf))
            if cursor.rowcount > 0:
                messages.error(request, "This copy already exists!!")
            else:
                cursor.execute(
                    """select Shelf_ID,Capacity from shelf where Shelf_ID=%s """, (shelf))
                if cursor.rowcount == 0:
                    messages.error(request, "Shelf doesn't exist")
                else:
                    cursor.execute(
                        """select * from isbn where ISBN=%s""", [isbn])
                    if cursor.rowcount == 0:
                        messages.error(
                            request, "Book details for the book does not exist add them first!!")
                    else:
                        cursor.execute(
                            """select A.Shelf_ID from shelf A where A.Shelf_ID=%s and (select count(*) from book where Shelf_ID=A.Shelf_ID)<A.Capacity""", [shelf])
                        if cursor.rowcount > 0:
                            cursor.execute(
                                """ insert into book(ISBN,Copy_number,Shelf_ID,Status) values(%s,%s,%s,%s)""", (isbn, copy, shelf, "On shelf"))
                            messages.success(
                                request, "Copy added successfully!!")
                        else:
                            messages.error(request, "shelf capacity full!!")
        return render(request, 'library/add_book.html')
    elif request.session.get('role') != None:
        return render(request, 'authentication/page_not_found.html')
    else:
        return render(request, 'authentication/error.html')


def update_book(request):
    userId = request.session.get('userId')
    email = request.session.get('email')
    category = request.session.get('category')
    if request.session.get('role') == 'librarian':
        cursor = connection.cursor()
        if 'delete' in request.POST:
            book_id = request.POST.get('delete')
            cursor.execute("""delete from book where Book_ID=%s""", [book_id])
            messages.success(request, "Copy deletion successful!!")
        elif 'update_copy' in request.POST:
            book_id = request.POST.get('update_copy')
            shelf_input = request.POST.get('shelf_input')
            cursor.execute(
                """ select * from shelf where Shelf_ID=%s""", [shelf_input])
            if cursor.rowcount > 0:
                records = cursor.fetchall()
                capacity = records[0][1]
                cursor.execute(
                    """ select count(*) from book where Shelf_ID=%s""", [shelf_input])
                if cursor.rowcount < capacity:
                    cursor.execute(
                        """ update book set Shelf_ID=%s where Book_ID=%s""", (shelf_input, book_id))
                    messages.success(request, "update successful")
                else:
                    messages.error(request, "capacity reached!!")
            else:
                messages.error(request, "shelf does not exist")
        search_key = request.GET.get('search_key')
        if search_key != None:
            cursor.execute(
                """ select * from  book where ISBN=%s""", [search_key])
        if search_key == None:
            cursor.execute("""select * from book""")
        row = cursor.fetchall()
        a = cursor.rowcount
        if a != 0:

            books = []
            for n in range(a):
                books.append({
                    "ISBN": row[n][1],
                    "book_id": row[n][0],
                    "shelf_id": row[n][2],
                    "copy_number": row[n][3],
                    "status": row[n][4]
                })
        if a != 0:
            data = {
                "books": books,
                "key": search_key,
            }
        else:
            data = {
                "books": None,
                "category": None,
                "key": None,
            }

        return render(request, 'library/edit_book.html', data)

    elif request.session.get('role') != None:
        return render(request, 'authentication/page_not_found.html')
    else:
        return render(request, 'authentication/error.html')


def issue(request):
    librarianId = request.session.get('librarianId')
    email = request.session.get('email')
    if request.session.get('role') == 'librarian':
        cursor = connection.cursor()
        cursor.execute(
            """SELECT Name FROM librarian WHERE email= %s""", [email])
        row = cursor.fetchall()
        data = {
            'Name': row[0][0]
        }
        return render(request, 'library/issue.html', data)
    elif request.session.get('role') != None:
        return render(request, 'authentication/page_not_found.html')
    else:
        return render(request, 'authentication/error.html')


def issue_available(request):
    librarianId = request.session.get('librarianId')
    email = request.session.get('email')
    if request.session.get('role') == 'librarian':
        if request.method == "POST":
            userId = request.method.get('userId')
            isbn = request.method.get('isbn')
            copy_number = request.method.get('copy_number')
            cursor = connection.cursor()
            cursor.execute(
                """SELECT Unpaid_fees FROM user Where User_ID=%s""", [userId])
            row = cursor.fetchall()
            unpaid_fees = row[0][0]
            cursor = connection.cursor()
            cursor.execute(
                """SELECT Loan_ID FROM on_loan WHERE User_ID=%s """, [userId])
            row = cursor.fetchall()
            b = cursor.rowcount
            if b >= 3 or unpaid_fees > 1000:
                cursor = connection.cursor()
                cursor.execute(
                    """SELECT Name FROM librarian WHERE email= %s""", [email])
                data = {
                    'Name': row[0][0]
                }
                if b >= 3 and unpaid_fees > 1000:
                    messages.success(
                        request, 'Maximum Isuue Limit  Exceeded and Unpaid Fines exceeds 1000 rupees ! Book Cannot Be Issued')
                elif b >= 3:
                    messages.success(
                        request, 'Maximum Isuue Limit  Exceeded ! Book Cannot Be Issued')
                else:
                    messages.success(
                        request, 'Unpaid Fines Exceed 1000 rupees ! Book Cannot Be Issued')
                return redirect('http://127.0.0.1:8000/librarian/home')
            else:
                cursor = connection.cursor()
                cursor.execute(
                    """SELECT Book_ID FROM book WHERE ISBN=%s AND Copy_number=%s AND Status=%s""", (isbn, copy_number, 'On shelf'))
                row = cursor.fetchall()
                a = cursor.rowcount
                if a > 0:
                    bookId = row[0][0]
                    cursor = connection.cursor()
                    cursor.execute(
                        """UPDATE book SET Status=%s WHERE Book_ID=%s""", ('On loan', bookId))
                    now = datetime.now()
                    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
                    cursor = connection.cursor()
                    cursor.execute("""INSERT into on_loan(Book_ID,User_ID,Date_of_Issue,librarian_ID)""", (
                        bookId, userId, date_time, librarianId))
                    cursor = connection.cursor()
                    cursor.execute(
                        """SELECT Name FROM librarian WHERE email= %s""", [email])
                    row = cursor.fetchall()
                    data = {
                        'Name': row[0][0]
                    }
                    messages.success(
                        request, 'Book Issued successfully !')
                    return redirect('http://127.0.0.1:8000/librarian/home')
                else:
                    cursor.execute(
                        """SELECT Name FROM librarian WHERE email= %s""", [email])
                    row = cursor.fetchall()
                    data = {
                        'Name': row[0][0]
                    }
                    messages.success(
                        request, 'Book Is On Hold by Other User! Cannot Be Issued !')
                    return redirect('http://127.0.0.1:8000/librarian/home')

        else:
            cursor = connection.cursor()
            cursor.execute(
                """SELECT Name FROM librarian WHERE email= %s""", [email])
            row = cursor.fetchall()
            data = {
                'Name': row[0][0]
            }
            return render(request, 'library/issueavailable.html', data)
    elif request.session.get('role') != None:
        return render(request, 'authentication/page_not_found.html')
    else:
        return render(request, 'authentication/error.html')


def issue_onHold(request):
    librarianId = request.session.get('librarianId')
    email = request.session.get('email')
    if request.session.get('role') == 'librarian':
        cursor = connection.cursor()
        cursor.execute(
            """SELECT Name FROM librarian WHERE email= %s""", [email])
        row = cursor.fetchall()
        name = row[0][0]
        if 'userId' in request.POST:
            userId = request.method.get('userId')
            cursor = connection.cursor()
            cursor.execute(
                """SELECT isbn.ISBN,Title,Year_of_Publication,Copy_number,Genre,Rating,date_of_hold,Author,Publisher,on_hold.Hold_ID FROM on_hold JOIN book ON on_hold.Book_ID=book.Book_ID JOIN isbn ON book.ISBN=isbn.ISBN WHERE User_ID= %s""", [userId])
            row = cursor.fetchall()
            a = cursor.rowcount
            books = []
            for n in range(a):
                books.append({
                    'ISBN': row[n][0],
                    'Title': row[n][1],
                    'Year_of_Publication': row[n][2],
                    'Copy_Number': row[n][3],
                    'Genre': row[n][4],
                    'Rating': row[n][5],
                    'date_of_hold': row[n][6],
                    'Author': row[n][7],
                    'Publisher': row[n][8],
                    'Hold_ID': row[n][9]
                })
            data = {
                'Name': name,
                'books': books
            }
            return render(request, 'library/issueonhold.html', data)
        elif 'issue' in request.POST:
            holdId = request.method.get('issue')
            cursor = connection.cursor()
            cursor.execute(
                """SELECT User_ID,Book_ID FROM on_hold Where Hold_ID=%s""", [holdId])
            row = cursor.fetchall()
            userId = row[0][0]
            bookId = row[0][1]
            cursor = connection.cursor()
            cursor.execute(
                """SELECT Unpaid_fees FROM user Where User_ID=%s""", [userId])
            row = cursor.fetchall()
            unpaid_fees = row[0][0]
            cursor = connection.cursor()
            cursor.execute(
                """SELECT Loan_ID FROM on_loan WHERE User_ID=%s """, [userId])
            row = cursor.fetchall()
            b = cursor.rowcount
            if b >= 3 or unpaid_fees > 1000:
                cursor = connection.cursor()
                cursor.execute(
                    """SELECT Name FROM librarian WHERE email= %s""", [email])
                data = {
                    'Name': row[0][0]
                }
                if b >= 3 and unpaid_fees > 1000:
                    messages.success(
                        request, 'Maximum Isuue Limit  Exceeded and Unpaid Fines exceeds 1000 rupees ! Book Cannot Be Issued')
                elif b >= 3:
                    messages.success(
                        request, 'Maximum Isuue Limit  Exceeded ! Book Cannot Be Issued')
                else:
                    messages.success(
                        request, 'Unpaid Fines Exceed 1000 rupees ! Book Cannot Be Issued')
                return redirect('http://127.0.0.1:8000/librarian/home')
            else:
                cursor = connection.cursor()
                cursor.execute(
                    """DELETE FROM on_hold Where Hold_ID=%s""", [holdId])
                now = datetime.now()
                date_time = now.strftime("%Y-%m-%d %H:%M:%S")
                cursor = connection.cursor()
                cursor.execute(
                    """UPDATE book SET Status=%s WHERE Book_ID=%s""", ('On loan', bookId))
                cursor = connection.cursor()
                cursor.execute("""INSERT into on_loan(Book_ID,User_ID,Date_of_Issue,librarian_ID)""", (
                    bookId, userId, date_time, librarianId))
                data = {
                    'Name': name
                }
                messages.success(
                    request, 'Book Issued successfully !')
                return redirect('http://127.0.0.1:8000/librarian/home')
        else:
            data = {
                'Name': name
            }
            return render(request, 'library/issueonhold.html', data)
    elif request.session.get('role') != None:
        return render(request, 'authentication/page_not_found.html')
    else:
        return render(request, 'authentication/error.html')


def shelf(request):
    userId = request.session.get('userId')
    email = request.session.get('email')
    if request.session.get('role') == 'librarian':

        return render(request, 'library/librarian_shelf.html')
    elif request.session.get('role') != None:
        return render(request, 'authentication/page_not_found.html')
    else:
        return render(request, 'authentication/error.html')

    # return render(request,'library/page_not_found.html')


def shelf_add(request):
    userId = request.session.get('userId')
    email = request.session.get('email')
    # category = request.session.get('category')
    if request.session.get('role') == 'librarian':
        if 'add_shelf' in request.POST:
            shelf_id = request.POST.get('shelf_ID')
            capacity = request.POST.get('capacity')
            cursor = connection.cursor()
            cursor.execute("""select * from shelf where Shelf_ID=%s""",
                           [shelf_id])
            if cursor.rowcount > 0:
                messages.error(
                    request, "Shelf with given details already exist!!")
            else:
                cursor.execute("""insert into shelf(Shelf_ID,Capacity) values(%s,%s)""",
                               (shelf_id, capacity))
                messages.success(request, "Shelf details added successfully!!")
        return render(request, 'library/add_shelf.html')
    elif request.session.get('role') != None:
        return render(request, 'authentication/page_not_found.html')
    else:
        return render(request, 'authentication/error.html')


def shelf_update(request):
    userId = request.session.get('userId')
    email = request.session.get('email')
    category = request.session.get('category')
    if request.session.get('role') == 'librarian':
        cursor = connection.cursor()
        if 'delete' in request.POST:
            shelf_id = request.POST.get('delete')
            cursor.execute(
                """delete from shelf where Shelf_ID=%s""", [shelf_id])
            messages.success(request, "Shelf deletion successful!!")
        elif 'update_shelf' in request.POST:
            shelf_id = request.POST.get('update_shelf')
            capacity = request.POST.get('capacity_input')
            cursor.execute(
                """ select * from shelf where Shelf_ID=%s""", [shelf_id])
            if cursor.rowcount > 0:
                records = cursor.fetchall()
                capacity = records[0][1]
                cursor.execute(
                    """ update shelf set Capacity=%s where Shelf_ID=%s""", (capacity, shelf_id))
                messages.success(request, "update successful")

            else:
                messages.error(request, "shelf does not exist")

        cursor.execute("""select * from shelf""")
        row = cursor.fetchall()
        a = cursor.rowcount
        if a != 0:

            shelves = []
            for n in range(a):
                shelves.append({
                    "shelf_id": row[n][0],
                    "capacity": row[n][1],

                })
        if a != 0:
            data = {
                "shelves": shelves

            }
        else:
            data = {
                "shelves": None,

            }

        return render(request, 'library/edit_shelf.html', data)

    elif request.session.get('role') != None:
        return render(request, 'authentication/page_not_found.html')
    else:
        return render(request, 'authentication/error.html')


def return_book(request):
    librarianId = request.session.get('librarianId')
    email = request.session.get('email')
    if request.session.get('role') == 'librarian':
        cursor = connection.cursor()
        cursor.execute(
            """SELECT Name FROM librarian WHERE email= %s""", [email])
        row = cursor.fetchall()
        data = {
            'Name': row[0][0]
        }
        if request.method == "POST":
            isbn = request.method.get('isbn')
            copy_number = request.method.get('copy_number')
            cursor = connection.cursor()
            cursor.execute(
                """SELECT Book_ID FROM book WHERE ISBN=%s AND Copy_number=%s""", (isbn, copy_number))
            row = cursor.fetchall()
            bookId = row[0][0]
            cursor = connection.cursor()
            cursor.execute(
                """SELECT Loan_ID,User_ID FROM on_loan WHERE Book_ID=%s""", (bookId))
            row = cursor.fetchall()
            loanId = row[0][0]
            userId = row[0][1]
            cursor = connection.cursor()
            cursor.execute(
                """SELECT Unpaid_fees FROM user Where User_ID=%s""", [userId])
            row = cursor.fetchall()
            unpaid_fees = row[0][0]
            cursor = connection.cursor()
            cursor.execute(
                """SELECT Fine,Date_of_Issue FROM on_loan Where Loan_ID=%s""", [loanId])
            row = cursor.fetchall()
            fine = row[0][0]
            Date_Of_Issue = row[0][1]
            unpaid_fees = unpaid_fees+fine
            cursor = connection.cursor()
            cursor.execute(
                """UPDATE user SET Unpaid_fees=%s WHERE User_ID=%s""", (unpaid_fees, userId))
            cursor = connection.cursor()
            cursor.execute(
                """DELETE FROM on_loan Where Loan_ID=%s""", [loanId])
            now = datetime.now()
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")
            cursor = connection.cursor()
            cursor.execute("""INSERT into previous_books(User_ID,Book_ID,Date_of_issue,Date_of_return,Fine)""",
                           (userId, bookId, Date_Of_Issue, date_time, fine))
            cursor = connection.cursor()
            cursor.execute(
                """SELECT User_Id FROM on_loan_on_hold WHERE ISBN= %s ORDER BY Time_stamp""", [isbn])
            row = cursor.fetchall()
            a = cursor.rowcount
            if a > 0:
                newuserId = row[0][0]
                cursor = connection.cursor()
                cursor.execute(
                    """UPDATE book SET Status=%s WHERE Book_ID=%s""", ('On hold', bookId))
                cursor = connection.cursor()
                now = datetime.now()
                date_time = now.strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute(
                    """INSERT into on_hold(date_of_hold,User_ID,Book_ID)""", (date_time, newuserId, bookId))
                #####################      Email to newuser about hold ##################
                messages.success(
                    request, 'Book returned successfully !')
                return redirect('http://127.0.0.1:8000/librarian/home')
            else:
                cursor = connection.cursor()
                cursor.execute(
                    """UPDATE book SET Status=%s WHERE Book_ID=%s""", ('On shelf', bookId))
                messages.success(
                    request, 'Book returned successfully !')
                return redirect('http://127.0.0.1:8000/librarian/home')
        else:
            return render(request, 'library/returnbook.html', data)
    elif request.session.get('role') != None:
        return render(request, 'authentication/page_not_found.html')
    else:
        return render(request, 'authentication/error.html')


def friends_list(request):
    userId = request.session.get('userId')
    cursor = connection.cursor()
    if request.method == "POST":

        id = request.POST.get('RemoveFriend')
        cursor.execute(
            """DELETE  FROM friend_list WHERE (Friend_ID = %s AND User_ID = %s) OR (Friend_ID = %s AND User_ID = %s) """, [id, userId, userId, id])
        messages.success(request, "Friend removed successfully")

    row = cursor.execute(
        """ SELECT Friend_ID,User_ID,Status FROM friend_list WHERE User_ID =%s OR Friend_ID=%s""", [userId, userId])
    row = cursor.fetchall()
    a = cursor.rowcount
    FriendIds = []
    FriendNames = []

    if a != 0:
        for n in range(a):
            if row[n][2] == 'Accepted':
                if row[n][0] not in FriendIds:
                    FriendIds.append(row[n][0])

                if row[n][1] not in FriendIds:
                    FriendIds.append(row[n][1])
    for id in FriendIds:
        if id == userId:
            FriendIds.remove(userId)

    for friendId in FriendIds:
        cursor.execute(
            """ SELECT Name FROM user WHERE User_ID = %s""", [friendId])
        row = cursor.fetchall()
        k = cursor.rowcount
        for m in range(k):
            FriendNames.append(row[m][0])
    friends = []
    for i in range(0, len(FriendIds)):
        friends.append({
            'friendId': FriendIds[i],
            'friendName': FriendNames[i]
        })

    data = {
        'friends': friends
    }

    if request.GET.get('Search_by') == 'Roll No':

        FriendIds = request.GET.get('SearchData')

        cursor.execute(
            """SELECT Name FROM user WHERE User_ID = %s""", [FriendIds])
        row = cursor.fetchall()
        FriendNames = row[0][0]
        cursor.execute("""SELECT Status FROM friend_list WHERE (Friend_ID = %s AND User_ID = %s) OR (Friend_ID = %s AND User_ID = %s) """, [
            FriendIds, userId, userId, FriendIds])
        col = cursor.fetchall()
        friends = []
        if cursor.rowcount > 0:
            Status = col[0][0]
            if Status == 'Accepted':
                friends = []
                for i in range(0, 1):
                    friends.append({
                        'friendId': FriendIds,
                        'friendName': FriendNames
                    })

        data = {
            'friends': friends
        }
        # return render(request, 'library/friend_list.html', data)

    if request.GET.get('Search_by') == 'Name':

        FriendNames = request.GET.get('SearchData')

        cursor.execute(
            """SELECT User_ID FROM user WHERE Name = %s""", [FriendNames])
        row = cursor.fetchall()
        a = cursor.rowcount
        FriendIds = []

        if(a != 0):
            for n in range(a):
                cursor.execute("""SELECT Status FROM friend_list WHERE (Friend_ID = %s AND User_Id = %s) OR (Friend_ID = %s AND User_Id = %s) """, [
                    row[n][0], userId, userId, row[n][0]])
                col = cursor.fetchall()
                if cursor.rowcount > 0:
                    Status = col[0][0]
                    if Status == 'Accepted':
                        FriendIds.append(row[n][0])
        friends = []
        for i in range(0, len(FriendIds)):
            friends.append({
                'friendId': FriendIds[i],
                'friendName': FriendNames
            })

        data = {
            'friends': friends
        }

    return render(request, 'library/friend_list.html', data)


def pending_requests(request):

    userId = request.session.get('userId')
    cursor = connection.cursor()
    if request.POST.get('AcceptRequest'):

        ID = request.POST.get('AcceptRequest')
        cursor.execute(
            """UPDATE friend_list SET Status = 'Accepted' WHERE User_ID = %s AND Friend_ID = %s""", [ID, userId])
        messages.success(request, "Friend request accepted!!")

    if request.POST.get('RejectRequest'):
        ID = request.POST.get('RejectRequest')
        cursor.execute(
            """DELETE  FROM friend_list WHERE User_ID = %s AND Friend_ID = %s""", [ID, userId])
        messages.error(request, "Request removed successfully!")
    cursor.execute(
        """SELECT User_ID,Status FROM friend_list WHERE %s = Friend_ID""", [userId])
    row = cursor.fetchall()
    a = cursor.rowcount
    print(a)
    friends = []
    FriendIds = []
    FriendNames = []
    Status = []
    if a != 0:
        for n in range(a):
            if row[n][1] == 'Pending':
                FriendIds.append(row[n][0])
                Status.append(row[n][1])
    for i in range(0, len(FriendIds)):
        if FriendIds[i] == userId:
            FriendIds.remove(userId)
            del Status[i]
    for friendId in FriendIds:
        cursor.execute(
            """ SELECT Name FROM user WHERE User_ID = %s""", [friendId])
        row = cursor.fetchall()
        k = cursor.rowcount
        for m in range(k):
            FriendNames.append(row[m][0])

    friends = []
    for i in range(0, len(FriendIds)):
        friends.append({
            'friendId': FriendIds[i],
            'friendName': FriendNames[i],
            'status': Status[i]
        })

    data = {
        'friends': friends
    }
    if request.GET.get('Search_by') == 'Roll No':

        FriendIds = request.GET.get('SearchData')
        cursor.execute(
            """SELECT Name,Status FROM user INNER JOIN friend_list ON user.User_ID = friend_list.Friend_ID WHERE friend_list.Friend_ID= %s AND friend_list.User_ID=%s""", (userId, FriendIds))
        row = cursor.fetchall()
        FriendNames = row[0][0]
        Status = row[0][1]
        friends = []
        for i in range(0, len(FriendIds)):
            friends.append({
                'friendId': FriendIds,
                'friendName': FriendNames,
                'status': Status
            })

        data = {
            'friends': friends
        }

    if request.GET.get('Search_by') == 'Name':

        FriendNames = request.GET.get('SearchData')
        cursor.execute(
            """SELECT user.User_ID,Status FROM user INNER JOIN friend_list ON user.User_ID = friend_list.User_ID WHERE user.Name = %s AND friend_list.Friend_ID=%s""", (FriendNames, userId))
        row = cursor.fetchall()
        a = cursor.rowcount
        FriendIds = []
        Status = []
        friends = []

        if a != 0:
            for n in range(a):
                if row[n][1] == 'Pending':
                    FriendIds.append(row[n][0])
                    Status.append(row[n][1])

        for i in range(0, len(FriendIds)):
            friends.append({
                'friendId': FriendIds[i],
                'friendName': FriendNames,
                'status': Status
            })

        data = {
            'friends': friends
        }

    return render(request, 'library/friends_pending.html', data)


def friends_bookshelf(request, friendId):
    userId = request.session.get('userId')
    email = request.session.get('email')
    if request.session.get('role') == 'user':
        cursor = connection.cursor()
        cursor.execute(
            """SELECT Name,Unpaid_fees FROM user WHERE email= %s""", [email])
        row = cursor.fetchall()
        name = row[0][0]
        unpaid_fees = row[0][1]
        cursor.execute(
            """SELECT Name FROM user WHERE User_ID= %s""", [friendId])
        row = cursor.fetchall()
        friendName = row[0][0]
        cursor.execute(
            """SELECT isbn.ISBN,Title,Year_of_Publication,Genre,Rating,Author,Publisher,Img_link FROM reading_list JOIN isbn ON reading_list.ISBN=isbn.ISBN  WHERE User_ID= %s""", [friendId])
        row = cursor.fetchall()
        a = cursor.rowcount
        reading_list = []
        for n in range(a):
            cursor.execute(
                """ select  count(*) from review where ISBN=%s""", [row[n][0]])
            col = cursor.fetchall()
            if row[n][4] == None:
                range_of_rating = 0
            else:
                range_of_rating = row[n][4]
            reading_list.append({
                'ISBN': row[n][0],
                'Title': row[n][1],
                'Year_of_Publication': row[n][2],
                'Genre': row[n][3],
                'Rating': row[n][4],
                'Author': row[n][5],
                'Publisher': row[n][6],
                'stars': range(1, range_of_rating+1),
                'no_stars': range(1, 5-range_of_rating+1),
                'votes': col[0][0],
                'image_url': row[n][7]
            })
        data = {
            'Name': name,
            'friendName': friendName,
            'Unpaid_fees': unpaid_fees,
            'list': reading_list
        }
        return render(request, 'library/friend_bookshelf.html', data)
    elif request.session.get('role') != None:
        return render(request, 'authentication/page_not_found.html')
    else:
        return render(request, 'authentication/error.html')


def add_friend(request):
    userId = request.session.get('userId')
    cursor = connection.cursor()
    if request.method == "POST":

        id = request.POST.get('AddFriend')
        cursor.execute(
            """INSERT INTO friend_list (Friend_ID,User_ID,Status) VALUES (%s,%s,'Pending')""", (id, userId))
        messages.success(request, "Friend request sent successfully")

    cursor.execute(
        """ SELECT Friend_ID,User_ID FROM friend_list WHERE User_ID =%s OR Friend_ID=%s""", (userId, userId))
    row = cursor.fetchall()
    a = cursor.rowcount
    FriendIds = []
    if a != 0:
        for n in range(a):
            # if row[n][0] != userId and row[n][1] != userId:
            if row[n][0] not in FriendIds:
                FriendIds.append(row[n][0])

            if row[n][1] not in FriendIds:
                FriendIds.append(row[n][1])
    for id in FriendIds:
        if id == userId:
            FriendIds.remove(userId)

    row = cursor.execute("""SELECT Name,User_ID FROM user""")
    row = cursor.fetchall()
    a = cursor.rowcount

    NonFriendIds = []
    NonFriendNames = []

    for n in range(a):

        if row[n][1] != userId:

            if row[n][1] not in FriendIds:

                NonFriendIds.append(row[n][1])
                NonFriendNames.append(row[n][0])

    nonfriends = []
    for i in range(0, len(NonFriendIds)):
        nonfriends.append({
            'nonfriendId': NonFriendIds[i],
            'nonfriendName': NonFriendNames[i]
        })

    data = {
        'nonfriends': nonfriends
    }

    if request.GET.get('Search_by') == 'Roll No':

        NonFriendIds = request.GET.get('SearchData')

        cursor.execute(
            """SELECT Name FROM user WHERE User_ID = %s""", [NonFriendIds])
        row = cursor.fetchall()
        nonfriends = []
        if cursor.rowcount > 0:
            NonFriendNames = row[0][0]
            cursor.execute(
                """ select * from friend_list where Friend_ID=%s""", [NonFriendIds])

            if cursor.rowcount == 0:

                for i in range(0, 1):
                    nonfriends.append({
                        'nonfriendId': NonFriendIds,
                        'nonfriendName': NonFriendNames
                    })

        data = {
            'nonfriends': nonfriends
        }

    if request.GET.get('Search_by') == 'Name':

        NonFriendNames = request.GET.get('SearchData')

        cursor.execute(
            """SELECT User_ID FROM user WHERE Name = %s""", [NonFriendNames])
        row = cursor.fetchall()
        a = cursor.rowcount
        NonFriendIds = []
        if a != 0:
            for n in range(a):
                cursor.execute("""SELECT User_ID,Friend_ID FROM friend_list WHERE (Friend_ID = %s AND User_Id = %s) OR (Friend_ID = %s AND User_Id = %s) """, [
                    row[n][0], userId, userId, row[n][0]])
                col = cursor.fetchall()
                m = cursor.rowcount
                if cursor.rowcount == 0:
                    NonFriendIds.append(row[n][0])
        nonfriends = []
        if len(NonFriendIds) > 0:
            for i in range(0, len(NonFriendIds)):
                nonfriends.append({
                    'nonfriendId': NonFriendIds[i],
                    'nonfriendName': NonFriendNames
                })

        data = {
            'nonfriends': nonfriends
        }

    return render(request, 'library/friend_add.html', data)
