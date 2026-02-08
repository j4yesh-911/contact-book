from flask import Blueprint, render_template, redirect, request
from flask_login import login_user, logout_user
from .services import create_user, authenticate_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = authenticate_user(request.form)
        if user:
            login_user(user)
            return redirect("/dashboard")
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        create_user(request.form)
        return redirect("/")
    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect("/")
