from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Book
from .forms import BookForm
from .models import Author
from .models import Loan
from .models import UserProfile
from .forms import AuthorForm
from .forms import LoanForm
from .forms import SearchBookForm
from .forms import RegisterUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import logout
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


# Create your views here.
def home (request):
    form = SearchBookForm(request.GET)
    title = request.GET.get('title')
    isbn =  request.GET.get('isbn')
    books = Book.objects.all()
    if title:
       books = books.filter(title__icontains = title)
    if isbn:
       books = books.filter(isbn = isbn)        
    return render(request, 'home.html', {'books':books,'form':form})

@login_required
@permission_required('library.book_admin',raise_exception = True)
def book_all (request):
    books = Book.objects.all()
    return render(request,'book/all.html',{'books': books})
    
@login_required
@permission_required('library.book_admin',raise_exception = True)
def book_update (request, book_id):
    book = get_object_or_404(Book, id = book_id)
    if request.method=='POST':
        received_form = BookForm(request.POST, instance = book)  
        if received_form.is_valid(): 
            received_form.save()
            messages.success(request,'Livro Alterado')
            form = received_form 
    else:
        form = BookForm(instance = book)
    return render(request,'book/update.html',{'form': form}) 

@login_required
@permission_required('library.book_admin',raise_exception = True)    
def book_create (request):
    if request.method=='POST':
        received_form = BookForm(request.POST)  
        if received_form.is_valid(): 
            received_form.save()
            messages.success(request,'Livro Cadastrado')
    form = BookForm()  
    return render(request,'book/create.html',{'form': form}) 

@login_required
@permission_required('library.book_admin',raise_exception = True)
def book_view(request, book_id):
    book = get_object_or_404(Book, id = book_id)     
    return render(request,'book/view.html',{'book': book})     

@login_required
@permission_required('library.book_admin',raise_exception = True)
def book_delete(request, book_id):
    book = get_object_or_404(Book, id = book_id)
    book.delete()
    return render(request, 'book/delete.html')

@login_required    
@permission_required('library.author_admin',raise_exception = True)
def author_all (request):
    authors = Author.objects.all()
    return render(request,'author/all.html',{'authors': authors})

@login_required  
@permission_required('library.author_admin',raise_exception = True)  
def author_update (request, author_id):
    author = get_object_or_404(Author, id = author_id)
    if request.method=='POST':
        received_form = AuthorForm(request.POST, instance = author)  
        if received_form.is_valid(): 
            received_form.save()
            messages.success(request,'Autor Alterado')
            form = received_form 
    else:
        form = AuthorForm(instance = author)
    return render(request,'author/update.html',{'form': form}) 

@login_required    
@permission_required('library.author_admin',raise_exception = True)
def author_create (request):
    if request.method=='POST':
        received_form = AuthorForm(request.POST)  
        if received_form.is_valid(): 
            received_form.save()
            messages.success(request,'Autor Cadastrado')
    form = AuthorForm() 
    return render(request,'author/create.html',{'form': form}) 

@login_required
@permission_required('library.author_admin',raise_exception = True)
def author_view(request, author_id):
    author = get_object_or_404(Author, id = author_id)
    return render(request,'author/view.html',{'author': author})     

@login_required
@permission_required('library.author_admin',raise_exception = True)
def author_delete(request, author_id):
    author = get_object_or_404(Author, id = author_id)
    author.delete()
    return render(request, 'author/delete.html')

def user_create (request):
    form = None
    if request.method == 'POST':
        received_form = RegisterUserForm(request.POST)
        if received_form.is_valid(): 
            user = received_form.save()
            book_admin = received_form.cleaned_data['book_admin']
            if book_admin:
                permission = Permission.objects.get(codename = 'book_admin')
                user.user_permissions.add(permission)
            author_admin = received_form.cleaned_data['author_admin']
            if author_admin:
                permission = Permission.objects.get(codename = 'author_admin')
                user.user_permissions.add(permission)       
            user_profile = UserProfile()
            user_profile.user = user
            user_profile.save()
            messages.success(request,'Usuário Cadastrado')
        else:
            form = received_form
    form = form or RegisterUserForm() 
    return render(request,'user/create.html',{'form': form})     

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Usuário ou Senha Incorretos!')
    return render(request, 'user/login.html')
    
def user_logout(request):
    logout(request);
    return render(request, 'user/logout.html')

@login_required
def loan_do(request, book_id):
    book = get_object_or_404(Book,id = book_id)
    if request.method == 'POST':
        received_form = LoanForm(request.POST)
        if received_form.is_valid():
            requested_count = received_form.cleaned_data['count']
            requested_count = min(book.count,requested_count)
            book.count -= requested_count
            book.save()
            user_profile = request.user.userprofile
            loans = Loan.objects.filter(book__pk = book.id)
            loans = loans.filter(userprofile__pk = user_profile.id)    
            if len(loans) == 0 :
                loan = Loan()
                loan.book = book 
                loan.count = requested_count
                loan.save()
                user_profile.loans.add(loan)
                user_profile.save()
            else:
                loan = loans[0]
                loan.count += requested_count
                loan.save()
            messages.success(request,'%d  Livro(s) Emprestado(s)'%(requested_count))
    form = LoanForm()
    return render(request, 'loan/do.html',{'book':book, 'form':form})

@login_required    
def loan_undo(request, book_id):
    book = get_object_or_404(Book,id = book_id)
    user_profile = request.user.userprofile
    loans = Loan.objects.filter(book__pk = book.id)
    loans = loans.filter(userprofile__pk = user_profile.id)
    if len(loans) == 0 :
        messages.error(request, 'Não há Empréstimos para o Usuário deste Livro')
        loan_count = 0
    else:
        loan = loans[0]
        loan_count = loan.count
        if request.method == 'POST':
            received_form = LoanForm(request.POST)       
            if received_form.is_valid():
                requested_count = received_form.cleaned_data['count']
                requested_count = min(loan.count,requested_count)
                loan_count -= requested_count
                book = loan.book
                if loan_count == 0:
                    loan.delete()
                else:
                    loan.count = loan_count
                    loan.save()
                book.count += requested_count
                book.save()
                messages.success(request,'%d  Livro(s) Devolvido(s)'%(requested_count))
    form = LoanForm()
    return render(request, 'loan/undo.html',{'book':book, 'form':form, 'loan_count':loan_count,})
    
            
