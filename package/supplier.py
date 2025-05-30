# from flask import Blueprint, flash, redirect, render_template, request, url_for

# from package.backend.databases.Inventory.models_inv.supplier_model import Supplier
# from package.backend.db_conn.aws_mysql import get_session  # SQLAlchemy session

# supplier_bp = Blueprint("supplier_bp", __name__, url_prefix="/suppliers")


# @supplier_bp.route("/")
# def list_suppliers():
#     suppliers = Supplier.query.all()
#     return render_template("supplier_list.html", suppliers=suppliers)


# @supplier_bp.route("/add", methods=["GET", "POST"])
# def add_supplier():
#     if request.method == "POST":
#         db = next(get_session())
#         name = request.form.get("name")
#         contact_name = request.form.get("contact_name")
#         email = request.form.get("email")
#         phone = request.form.get("phone")
#         address = request.form.get("address")

#         if not name:
#             flash("Supplier name is required", "error")
#             return redirect(url_for("supplier_bp.add_supplier"))

#         new_supplier = Supplier(
#             name=name,
#             contact_name=contact_name,
#             email=email,
#             phone=phone,
#             address=address,
#         )
#         db.session.add(new_supplier)
#         db.session.commit()
#         flash("Supplier added successfully", "success")
#         return redirect(url_for("supplier_bp.list_suppliers"))

#     return render_template(
#         "supplier_form.html",
#         supplier=None,
#         form_action=url_for("supplier_bp.add_supplier"),
#     )


# @supplier_bp.route("/edit/<int:supplier_id>", methods=["GET", "POST"])
# def edit_supplier(supplier_id):
#     supplier = Supplier.query.get_or_404(supplier_id)

#     if request.method == "POST":
#         db = next(get_session())
#         name = request.form.get("name")
#         contact_name = request.form.get("contact_name")
#         email = request.form.get("email")
#         phone = request.form.get("phone")
#         address = request.form.get("address")

#         if not name:
#             flash("Supplier name is required", "error")
#             return redirect(
#                 url_for("supplier_bp.edit_supplier", supplier_id=supplier_id)
#             )

#         supplier.name = name
#         supplier.contact_name = contact_name
#         supplier.email = email
#         supplier.phone = phone
#         supplier.address = address

#         db.session.commit()
#         flash("Supplier updated successfully", "success")
#         return redirect(url_for("supplier_bp.list_suppliers"))

#     return render_template(
#         "supplier_form.html",
#         supplier=supplier,
#         form_action=url_for("supplier_bp.edit_supplier", supplier_id=supplier_id),
#     )


# @supplier_bp.route("/delete/<int:supplier_id>", methods=["POST"])
# def delete_supplier(supplier_id):
#     db = next(get_session())
#     supplier = Supplier.query.get_or_404(supplier_id)

#     db.session.delete(supplier)
#     db.session.commit()
#     flash("Supplier deleted successfully", "success")
#     return redirect(url_for("supplier_bp.list_suppliers"))
