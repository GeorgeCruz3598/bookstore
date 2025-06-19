from flask import render_template

def list(orders):
    return render_template('orders/index.html', orders = orders)

def my_orders(orders):
    return render_template('orders/my_orders.html', orders = orders)

def add_order(form,book):
    return render_template('orders/add_order.html', form=form, book=book)

def edit(form, order, book):
    return render_template('orders/edit.html', form=form, order=order, book=book)

def my_orders_edit(form, order, book):
    return render_template('orders/my_orders_edit.html', form=form, order=order, book=book)
