# from datetime import datetime

# from flask import flash, redirect, render_template, request, url_for

# from package.backend.databases.Inventory.models_inv.product_model import Product
# from package.backend.databases.Inventory.service_inv.category_service import (
#     get_all_categories,
# )
# from package.backend.databases.Inventory.service_inv.supplier_service import (
#     get_all_suppliers,
# )
# from package.backend.db_conn.aws_mysql import get_session  # SQLAlchemy session
# from package.frontend import frontend_bp

# # --- Product CRUD ---


# @frontend_bp.route("/products")
# def list_products():
#     db = next(get_session())
#     products = db.session.query(Product).all()
#     # Optionally eager load category and supplier for display:
#     # products = db.session.query(Product).join(Category).join(Supplier).all()
#     return render_template("product_list.html", products=products)


# @frontend_bp.route("/products/add", methods=["GET", "POST"])
# def add_product():
#     db = next(get_session())
#     categories = get_all_categories()
#     suppliers = get_all_suppliers()

#     if request.method == "POST":
#         try:
#             data = {
#                 "name": request.form.get("name", "").strip(),
#                 "sku": request.form.get("sku", "").strip(),
#                 "category_id": int(request.form.get("category_id")),
#                 "supplier_id": int(request.form.get("supplier_id")),
#                 "cost_price": float(request.form.get("cost_price")),
#                 "selling_price": float(request.form.get("selling_price")),
#                 "quantity_in_stock": int(request.form.get("quantity_in_stock")),
#                 "expiry_date": datetime.strptime(
#                     request.form.get("expiry_date"), "%Y-%m-%d"
#                 )
#                 if request.form.get("expiry_date")
#                 else None,
#                 "description": request.form.get("description", "").strip(),
#                 "status": request.form.get("status", "active").strip(),
#                 "created_at": datetime.utcnow(),
#                 "updated_at": datetime.utcnow(),
#             }
#         except Exception as e:
#             flash(f"Invalid input: {e}", "error")
#             return redirect(url_for("frontend_bp.add_product"))

#         # Basic validation example
#         if not data["name"] or not data["sku"]:
#             flash("Name and SKU are required.", "error")
#             return redirect(url_for("frontend_bp.add_product"))

#         product = Product(**data)
#         db.session.add(product)
#         db.session.commit()
#         flash("Product added successfully.", "success")
#         return redirect(url_for("frontend_bp.list_products"))

#     return render_template(
#         "product_form.html",
#         product=None,
#         categories=categories,
#         suppliers=suppliers,
#         form_action=url_for("frontend_bp.add_product"),
#     )


# @frontend_bp.route("/products/edit/<int:product_id>", methods=["GET", "POST"])
# def edit_product(product_id):
#     db = next(get_session())
#     product = Product.query.get_or_404(product_id)
#     categories = get_all_categories()
#     suppliers = get_all_suppliers()

#     if request.method == "POST":
#         try:
#             product.name = request.form.get("name", "").strip()
#             product.sku = request.form.get("sku", "").strip()
#             product.category_id = int(request.form.get("category_id"))
#             product.supplier_id = int(request.form.get("supplier_id"))
#             product.cost_price = float(request.form.get("cost_price"))
#             product.selling_price = float(request.form.get("selling_price"))
#             product.quantity_in_stock = int(request.form.get("quantity_in_stock"))
#             product.expiry_date = (
#                 datetime.strptime(request.form.get("expiry_date"), "%Y-%m-%d")
#                 if request.form.get("expiry_date")
#                 else None
#             )
#             product.description = request.form.get("description", "").strip()
#             product.status = request.form.get("status", "active").strip()
#             product.updated_at = datetime.utcnow()
#         except Exception as e:
#             flash(f"Invalid input: {e}", "error")
#             return redirect(url_for("frontend_bp.edit_product", product_id=product_id))

#         if not product.name or not product.sku:
#             flash("Name and SKU are required.", "error")
#             return redirect(url_for("frontend_bp.edit_product", product_id=product_id))

#         db.session.commit()
#         flash("Product updated successfully.", "success")
#         return redirect(url_for("frontend_bp.list_products"))

#     return render_template(
#         "product_form.html",
#         product=product,
#         categories=categories,
#         suppliers=suppliers,
#         form_action=url_for("frontend_bp.edit_product", product_id=product_id),
#     )


# @frontend_bp.route("/products/delete/<int:product_id>", methods=["POST"])
# def delete_product(product_id):
#     db = next(get_session())
#     product = Product.query.get_or_404(product_id)
#     db.session.delete(product)
#     db.session.commit()
#     flash("Product deleted successfully.", "success")
#     return redirect(url_for("frontend_bp.list_products"))
