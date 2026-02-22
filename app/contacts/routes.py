from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.exceptions import ContactExistsError, InvalidPhoneError
from .services import (
    add_contact,
    delete_contact,
    list_contacts,
    get_contact,
    update_contact,
    toggle_favorite,
)

contacts_bp = Blueprint("contacts", __name__)
PER_PAGE = 10

@contacts_bp.route("/dashboard")
@login_required
def dashboard():
    search = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)
    favorites_only = request.args.get("favorites", "").lower() == "1"
    pagination = list_contacts(search=search or None, page=page, per_page=PER_PAGE, favorites_only=favorites_only)
    edit_id = request.args.get("edit", type=int)
    edit_contact = get_contact(edit_id) if edit_id else None
    return render_template(
        "dashboard.html",
        contacts=pagination.items,
        pagination=pagination,
        search=search,
        favorites_filter=favorites_only,
        edit_contact=edit_contact,
    )

@contacts_bp.route("/add", methods=["POST"])
@login_required
def add():
    name = (request.form.get("name") or "").strip()
    phone = (request.form.get("phone") or "").strip()
    if not name or not phone:
        flash("Name and phone are required.", "error")
        return redirect(url_for("contacts.dashboard"))
    try:
        add_contact({
            "name": name,
            "phone": phone,
            "email": (request.form.get("email") or "").strip(),
        })
        flash("Contact added.", "success")
    except InvalidPhoneError as e:
        flash(str(e), "error")
    except ContactExistsError as e:
        flash(str(e), "error")
    return redirect(url_for("contacts.dashboard"))

@contacts_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    contact = get_contact(id)
    if not contact:
        return redirect(url_for("contacts.dashboard"))
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        phone = (request.form.get("phone") or "").strip()
        if not name or not phone:
            flash("Name and phone are required.", "error")
            return redirect(url_for("contacts.dashboard", edit=id))
        try:
            update_contact(id, {
                "name": name,
                "phone": phone,
                "email": (request.form.get("email") or "").strip(),
            })
            flash("Contact updated.", "success")
            args = {}
            if request.form.get("q"):
                args["q"] = request.form.get("q")
            if request.form.get("favorites") == "1":
                args["favorites"] = "1"
            if request.form.get("page"):
                args["page"] = request.form.get("page")
            return redirect(url_for("contacts.dashboard", **args))
        except InvalidPhoneError as e:
            flash(str(e), "error")
        except ContactExistsError as e:
            flash(str(e), "error")
        return redirect(url_for("contacts.dashboard", edit=id))
    return redirect(url_for("contacts.dashboard", edit=id))

@contacts_bp.route("/delete/<int:id>")
@login_required
def delete(id):
    delete_contact(id)
    flash("Contact deleted.", "success")
    return redirect(url_for("contacts.dashboard"))

@contacts_bp.route("/favorite/<int:id>")
@login_required
def favorite(id):
    toggle_favorite(id)
    return redirect(request.referrer or url_for("contacts.dashboard"))
