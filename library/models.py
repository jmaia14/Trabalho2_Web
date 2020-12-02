from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class Author (models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        permissions = [('author_admin','Administrar Autores')]
    
    def __str__(self):
        return self.name

class Book (models.Model):
    title = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20)
    year = models.IntegerField()
    edition = models.IntegerField()
    pages = models.IntegerField()
    count = models.IntegerField()
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    
    class Meta:
        permissions = [('book_admin','Administrar Livros')]
    
    def __str__(self):
        return self.title
   
class Loan (models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    count = models.IntegerField()
        
       
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='userprofile')
    loans = models.ManyToManyField(Loan, blank=True)
    
    def __str__(self):
        return str(self.user)

    
       
