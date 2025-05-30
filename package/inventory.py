import os
from datetime import datetime, timedelta, timezone

# from app.models import Activity
from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_jwt_extended import jwt_required
from sqlalchemy.orm import joinedload  # ensure this is imported
from werkzeug.utils import secure_filename

from package.backend.auth_jwt.decorator_jwt import role_required
from package.backend.databases.form.form import ProductForm
from package.backend.databases.Inventory.models_inv.category_model import Category
from package.backend.databases.Inventory.models_inv.product_model import Product
from package.backend.databases.Inventory.models_inv.supplier_model import Supplier
from package.backend.db_conn.aws_mysql import get_session

inventory_bp = Blueprint("inventory", __name__)


# Home page
@jwt_required()
@role_required(["admin", "staff"])
@inventory_bp.route("/products")
def products():
    return render_template("inventory.html")


@inventory_bp.route("/")
@jwt_required()
@role_required(["admin", "staff"])
def home():
    db = next(get_session())  # get a session instance

    products = db.query(Product).all()
    low_stock_count = db.query(Product).filter(Product.quantity_in_stock < 10).count()
    soon_date = datetime.now(timezone.utc) + timedelta(days=30)
    expiring_soon_count = (
        db.query(Product).filter(Product.expiry_date <= soon_date).count()
    )
    out_of_stock_count = (
        db.query(Product).filter(Product.quantity_in_stock == 0).count()
    )
    recent_products = (
        db.query(Product).order_by(Product.created_at.desc()).limit(5).all()
    )

    # You can close session manually if you want here:
    db.close()

    return render_template(
        "home.html",
        products=products,
        low_stock_count=low_stock_count,
        expiring_soon_count=expiring_soon_count,
        out_of_stock_count=out_of_stock_count,
        recent_products=recent_products,
    )


@inventory_bp.route("/products/add", methods=["GET", "POST"])
@jwt_required()
@role_required("admin")
def add_product():
    db = next(get_session())  # This is your SQLAlchemy session
    form = ProductForm()

    # Correct usage of session
    form.category_id.choices = [
        (c.category_id, c.name) for c in db.query(Category).order_by(Category.name)
    ]
    form.supplier_id.choices = [
        (s.supplier_id, s.name) for s in db.query(Supplier).order_by(Supplier.name)
    ]

    if form.validate_on_submit():
        try:
            product = Product(
                name=form.name.data,
                sku=form.sku.data,
                category_id=form.category_id.data,
                supplier_id=form.supplier_id.data,
                cost_price=form.cost_price.data,
                selling_price=form.selling_price.data,
                quantity_in_stock=form.quantity_in_stock.data,
                expiry_date=form.expiry_date.data,
                description=form.description.data,
                status=form.status.data,
            )

            if form.image.data:
                filename = secure_filename(form.image.data.filename)
                filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                form.image.data.save(filepath)
                product.image_url = url_for("static", filename=f"uploads/{filename}")

            db.add(product)
            db.commit()

            flash("Product added successfully", "success")
            return redirect(url_for("inventory.products"))

        except Exception as e:
            db.rollback()
            flash(f"Error adding product: {str(e)}", "error")

    return render_template("product_form.html", form=form)


@inventory_bp.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
@role_required("admin")
def edit_product(product_id):
    db = next(get_session())

    # Correct way to get the product or return 404 manually
    product = db.query(Product).get(product_id)
    if not product:
        abort(404)

    form = ProductForm(obj=product)

    # Populate dropdowns
    form.category_id.choices = [
        (c.category_id, c.name) for c in db.query(Category).order_by(Category.name)
    ]
    form.supplier_id.choices = [
        (s.supplier_id, s.name) for s in db.query(Supplier).order_by(Supplier.name)
    ]

    if form.validate_on_submit():
        try:
            product.name = form.name.data
            product.sku = form.sku.data
            product.category_id = form.category_id.data
            product.supplier_id = form.supplier_id.data
            product.cost_price = form.cost_price.data
            product.selling_price = form.selling_price.data
            product.quantity_in_stock = form.quantity_in_stock.data
            product.expiry_date = form.expiry_date.data
            product.description = form.description.data
            product.status = form.status.data

            # Handle file upload
            if form.image.data:
                if product.image_url:
                    try:
                        os.remove(
                            os.path.join(
                                current_app.config["UPLOAD_FOLDER"],
                                product.image_url.split("/")[-1],
                            )
                        )
                    except OSError:
                        pass

                filename = secure_filename(form.image.data.filename)
                filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
                form.image.data.save(filepath)
                product.image_url = url_for("static", filename=f"uploads/{filename}")

            db.commit()
            flash("Product updated successfully", "success")
            return redirect(url_for("inventory.products"))

        except Exception as e:
            db.rollback()
            flash(f"Error updating product: {str(e)}", "error")

    return render_template("product_form.html", form=form, product=product)


@inventory_bp.route("/categories", methods=["GET", "POST"])
@role_required(["admin", "staff"])
def categories():
    db = next(get_session())
    if request.method == "POST":
        # Handle AJAX request for adding/editing category
        if request.is_json:
            data = request.get_json()

            try:
                if "category_id" in data:  # Edit existing
                    category = db.query(Category).get(data["category_id"])

                    if not category:
                        return jsonify({"error": "Category not found"}), 404

                    category.name = data["name"]
                    category.description = data.get("description", "")
                else:  # Add new
                    category = Category(
                        name=data["name"], description=data.get("description", "")
                    )
                    db.session.add(category)

                db.session.commit()
                return jsonify({"success": True}), 200

            except Exception as e:
                db.session.rollback()
                return jsonify({"error": str(e)}), 500

    categories = db.query(Category).options(joinedload(Category.products)).all()
    return render_template("categories.html", categories=categories)


@inventory_bp.route("/reporting")
@role_required(["admin", "staff"])
def reporting():
    db = next(get_session())

    # Correct query syntax using plain SQLAlchemy session
    low_stock_items = (
        db.query(Product)
        .filter(Product.quantity_in_stock < 10)
        .options(joinedload(Product.category))
        .all()
    )

    return render_template("reporting.html", low_stock_items=low_stock_items)
