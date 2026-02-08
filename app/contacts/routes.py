from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from .services import add_contact, delete_contact, list_contacts

contacts_bp = Blueprint("contacts", __name__)

@contacts_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", contacts=list_contacts())

@contacts_bp.route("/add", methods=["POST"])
@login_required
def add():
    add_contact(request.form)
    return redirect("/dashboard")

@contacts_bp.route("/delete/<int:id>")
@login_required
def delete(id):
    delete_contact(id)
    return redirect("/dashboard")
