from flask import render_template

def list(payments):
    return render_template('payments/index.html', payments =payments)

def create(form): #sending form for wtforms
    return render_template('payments/create.html', form=form)

def edit(form, payment):
    return render_template('payments/edit.html', form=form, payment=payment)

#optional
def list_active(payments_active):
    return render_template('payments/page.html', payments_active =payments_active)