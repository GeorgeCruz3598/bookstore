from flask import render_template

def list(books):
    return render_template('books/index.html', books =books)

def create(form):
    return render_template('books/create.html', form=form)

def edit(form, book):
    return render_template('books/edit.html', form=form, book=book)

def list_by_active(books):
    return render_template('books/index.html', books =books)

def list_by_category_active(books, category):
    return render_template('books/books_by_category.html', books =books, category=category)