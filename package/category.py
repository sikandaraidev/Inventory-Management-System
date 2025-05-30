# from flask import Blueprint, flash, redirect, render_template, request, url_for

# from package.backend.databases.Inventory.models_inv.category_model import Category
# from package.backend.db_conn.aws_mysql import get_session  # SQLAlchemy session

# category_bp = Blueprint("category_bp", __name__, url_prefix="/categories")


# @category_bp.route("/")
# def list_categories():
#     categories = Category.query.all()
#     return render_template("category_list.html", categories=categories)


# @category_bp.route("/add", methods=["GET", "POST"])
# def add_category():
#     db = next(get_session())
#     if request.method == "POST":
#         name = request.form.get("name")
#         description = request.form.get("description")

#         if not name:
#             flash("Name is required", "error")
#             return redirect(url_for("category_bp.add_category"))

#         new_cat = Category(name=name, description=description)
#         db.session.add(new_cat)
#         db.session.commit()
#         flash("Category added successfully", "success")
#         return redirect(url_for("category_bp.list_categories"))

#     return render_template(
#         "category_form.html",
#         category=None,
#         form_action=url_for("category_bp.add_category"),
#     )


# @category_bp.route("/edit/<int:category_id>", methods=["GET", "POST"])
# def edit_category(category_id):
#     db = next(get_session())
#     category = Category.query.get_or_404(category_id)

#     if request.method == "POST":
#         name = request.form.get("name")
#         description = request.form.get("description")

#         if not name:
#             flash("Name is required", "error")
#             return redirect(
#                 url_for("category_bp.edit_category", category_id=category_id)
#             )

#         category.name = name
#         category.description = description
#         db.session.commit()
#         flash("Category updated successfully", "success")
#         return redirect(url_for("category_bp.list_categories"))

#     return render_template(
#         "category_form.html",
#         category=category,
#         form_action=url_for("category_bp.edit_category", category_id=category_id),
#     )


# @category_bp.route("/delete/<int:category_id>", methods=["POST"])
# def delete_category(category_id):
#     db = next(get_session())
#     category = Category.query.get_or_404(category_id)
#     db.session.delete(category)
#     db.session.commit()
#     flash("Category deleted successfully", "success")
#     return redirect(url_for("category_bp.list_categories"))
