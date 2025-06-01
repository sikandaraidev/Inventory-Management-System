from flask import (
    Blueprint,
    # abort,
    flash,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_jwt_extended import get_jwt_identity, jwt_required

from package.backend.auth_jwt.decorator_jwt import role_required
from package.backend.databases.Inventory.models_inv.category_model import Category
from package.backend.databases.Inventory.models_inv.product_model import Product
from package.backend.databases.Inventory.models_inv.supplier_model import Supplier
from package.backend.databases.Inventory.models_inv.user_model import User

# from package.backend.databases.product_log.schema_prod_log.prod_meta_schema import (
#     ProductMetadataSchema,
# )
from package.backend.databases.product_log.service_prod_log import prod_meta_service
from package.backend.db_conn.aws_mysql import get_session


def serialize_mongo_doc(doc):
    data = doc.to_mongo().to_dict()
    data["_id"] = str(data["_id"])  # convert ObjectId to str
    return data


frontend_bp = Blueprint(
    "frontend",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static",
)

# ---------- Auth Views ----------


@frontend_bp.route("/signup")
def signup():
    return render_template("signup.html")


@frontend_bp.route("/login")
def login():
    return render_template("login.html")


@frontend_bp.route("/dashboard")
@jwt_required()
@role_required(["admin", "staff"])
def dashboard():
    db = next(get_session())

    # You get current user id from JWT
    from flask_jwt_extended import get_jwt_identity

    user_id = get_jwt_identity()
    user = db.query(User).get(user_id)

    if not user:
        return redirect(url_for("frontend.login"))

    # username = {"role": db.query(User)}
    # role = {"username": db.query(User)}

    stats = {
        "products": db.query(Product).count(),
        "categories": db.query(Category).count(),
        "suppliers": db.query(Supplier).count(),
    }

    return render_template("dashboard.html", user=user, stats=stats)


@frontend_bp.route("/auth/logout", methods=["POST"])
@jwt_required()
@role_required(["admin", "staff"])
def logout():
    resp = make_response(redirect(url_for("frontend.login")))
    resp.delete_cookie("access_token_cookie")
    resp.delete_cookie("refresh_token_cookie")
    return resp


# ---------- Product Views ----------


@frontend_bp.route("/products")
@jwt_required()
@role_required(["admin", "staff"])
def list_products():
    db = next(get_session())
    products = db.query(Product).all()

    # Get user role from JWT
    user_id = get_jwt_identity()
    user = db.query(User).get(user_id)

    # # For each product, fetch metadata and attach
    # products_with_meta = []
    # for p in products:
    #     meta = ProductMetadataModel.objects(product_id=p.id).first()
    #     products_with_meta.append({"product": p, "metadata": meta})

    return render_template(
        "product_list.html",
        products=products,
        user_role=user.role,  # 👈 this is essential
        # products_meta=products_with_meta,
    )


@frontend_bp.route("/products/add", methods=["GET", "POST"])
@jwt_required()
@role_required("admin")
def add_product():
    db = next(get_session())
    categories = db.query(Category).all()
    suppliers = db.query(Supplier).all()

    if request.method == "POST":
        # Read form data
        name = request.form["name"]
        sku = request.form["sku"]
        category_id = request.form["category_id"]
        supplier_id = request.form["supplier_id"]
        cost_price = request.form["cost_price"]
        selling_price = request.form["selling_price"]
        quantity_in_stock = request.form["quantity_in_stock"]
        expiry_date = request.form["expiry_date"]
        description = request.form["description"]
        status = request.form["status"]

        # Create and save new product
        new_product = Product(
            name=name,
            sku=sku,
            category_id=category_id,
            supplier_id=supplier_id,
            cost_price=cost_price,
            selling_price=selling_price,
            quantity_in_stock=quantity_in_stock,
            expiry_date=expiry_date,
            description=description,
            status=status,
        )
        db.add(new_product)
        db.commit()
        flash("Product added successfully", "success")
        return redirect(url_for("frontend.list_products"))

    return render_template(
        "product_form.html",
        product=None,
        categories=categories,
        suppliers=suppliers,
        form_action=url_for("frontend.add_product"),
    )


@frontend_bp.route("/products/edit/<int:product_id>", methods=["GET", "POST"])
@jwt_required()
@role_required("admin")
def edit_product(product_id):
    db = next(get_session())
    product = db.query(Product).get(product_id)
    if not product:
        flash("Product not found", "error")
        return redirect(url_for("frontend.list_products"))

    categories = db.query(Category).all()
    suppliers = db.query(Supplier).all()

    if request.method == "POST":
        # Update product fields from form
        product.name = request.form["name"]
        product.sku = request.form["sku"]
        product.category_id = request.form["category_id"]
        product.supplier_id = request.form["supplier_id"]
        product.cost_price = request.form["cost_price"]
        product.selling_price = request.form["selling_price"]
        product.quantity_in_stock = request.form["quantity_in_stock"]
        product.expiry_date = request.form["expiry_date"]
        product.description = request.form["description"]
        product.status = request.form["status"]

        db.commit()
        flash("Product updated successfully", "success")
        return redirect(url_for("frontend.list_products"))

    return render_template(
        "product_form.html",
        product=product,
        categories=categories,
        suppliers=suppliers,
        form_action=url_for("frontend.edit_product", product_id=product_id),
    )


@frontend_bp.route("/products/delete/<int:product_id>", methods=["POST"])
@jwt_required()
@role_required("admin")
def delete_product(product_id):
    db = next(get_session())
    product = db.query(Product).get(product_id)
    db.delete(product)
    db.commit()
    flash("Product deleted successfully.", "success")
    return redirect(url_for("frontend.list_products"))


# ---------- Category Views ----------


@frontend_bp.route("/categories")
@jwt_required()
@role_required(["admin", "staff"])
def list_categories():
    db = next(get_session())
    categories = db.query(Category).all()
    # print(list(categories))
    return render_template("category_list.html", categories=categories)


@frontend_bp.route("/categories/add", methods=["GET", "POST"])
@jwt_required()
@role_required("admin")
def add_category():
    db = next(get_session())
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")

        if not name:
            flash("Name is required", "error")
            return redirect(url_for("frontend.add_category"))

        category = Category(name=name, description=description)
        db.add(category)
        db.commit()
        flash("Category added successfully", "success")
        return redirect(url_for("frontend.list_categories"))

    return render_template(
        "category_form.html",
        category=None,
        form_action=url_for("frontend.add_category"),
    )


@frontend_bp.route("/categories/edit/<int:category_id>", methods=["GET", "POST"])
@jwt_required()
@role_required("admin")
def edit_category(category_id):
    db = next(get_session())
    category = db.query(Category).get(category_id)

    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")

        if not name:
            flash("Name is required", "error")
            return redirect(url_for("frontend.edit_category", category_id=category_id))

        category.name = name
        category.description = description
        db.commit()
        flash("Category updated successfully", "success")
        return redirect(url_for("frontend.list_categories"))

    return render_template(
        "category_form.html",
        category=category,
        form_action=url_for("frontend.edit_category", category_id=category_id),
    )


@frontend_bp.route("/categories/delete/<int:category_id>", methods=["POST"])
@jwt_required()
@role_required("admin")
def delete_category(category_id):
    db = next(get_session())
    category = db.query(Category).get(category_id)
    db.delete(category)
    db.commit()
    flash("Category deleted successfully", "success")
    return redirect(url_for("frontend.list_categories"))


# ---------- Supplier Views ----------


@frontend_bp.route("/suppliers")
@jwt_required()
@role_required(["admin", "staff"])
def list_suppliers():
    db = next(get_session())
    suppliers = db.query(Supplier).all()
    return render_template("supplier_list.html", suppliers=suppliers)


@frontend_bp.route("/suppliers/add", methods=["GET", "POST"])
@jwt_required()
@role_required("admin")
def add_supplier():
    db = next(get_session())
    if request.method == "POST":
        name = request.form.get("name")
        contact_name = request.form.get("contact_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")

        if not name:
            flash("Supplier name is required", "error")
            return redirect(url_for("frontend.add_supplier"))

        supplier = Supplier(
            name=name,
            contact_name=contact_name,
            email=email,
            phone=phone,
            address=address,
        )
        db.add(supplier)
        db.commit()
        flash("Supplier added successfully", "success")
        return redirect(url_for("frontend.list_suppliers"))

    return render_template(
        "supplier_form.html",
        supplier=None,
        form_action=url_for("frontend.add_supplier"),
    )


@frontend_bp.route("/suppliers/edit/<int:supplier_id>", methods=["GET", "POST"])
@jwt_required()
@role_required("admin")
def edit_supplier(supplier_id):
    db = next(get_session())
    supplier = db.query(Supplier).get(supplier_id)

    if request.method == "POST":
        supplier.name = request.form.get("name")
        supplier.contact_name = request.form.get("contact_name")
        supplier.email = request.form.get("email")
        supplier.phone = request.form.get("phone")
        supplier.address = request.form.get("address")

        if not supplier.name:
            flash("Supplier name is required", "error")
            return redirect(url_for("frontend.edit_supplier", supplier_id=supplier_id))

        db.commit()
        flash("Supplier updated successfully", "success")
        return redirect(url_for("frontend.list_suppliers"))

    return render_template(
        "supplier_form.html",
        supplier=supplier,
        form_action=url_for("frontend.edit_supplier", supplier_id=supplier_id),
    )


@frontend_bp.route("/suppliers/delete/<int:supplier_id>", methods=["POST"])
@jwt_required()
@role_required("admin")
def delete_supplier(supplier_id):
    db = next(get_session())
    supplier = db.query(Supplier).get(supplier_id)
    db.delete(supplier)
    db.commit()
    flash("Supplier deleted successfully", "success")
    return redirect(url_for("frontend.list_suppliers"))


# Product Page render for Product Metadara
@frontend_bp.route("/product-meta/<int:product_id>")
@role_required(["admin", "staff"])
def render_product_meta_page(product_id):
    """
    Renders the HTML page for managing product metadata.
    """
    product = prod_meta_service.get_product_metadata(product_id)
    db = next(get_session())
    product = db.query(Product).filter_by(product_id=product_id).first()
    if not product:
        return "Product not found", 404

    # Resolve related fields manually
    category_name = None
    supplier_name = None

    if product.category_id:
        category = db.query(Category).filter_by(category_id=product.category_id).first()
        category_name = category.name if category else None

    if product.supplier_id:
        supplier = db.query(Supplier).filter_by(supplier_id=product.supplier_id).first()
        supplier_name = supplier.name if supplier else None

    return render_template(
        "new_product_meta.html",
        product=product,
        category_name=category_name,
        supplier_name=supplier_name,
        product_id=product.product_id,
    )


# Product Metadata CRUD route
@frontend_bp.route("/api/meta/<int:product_id>", methods=["GET"])
@role_required(["admin", "staff"])
def get_product_metadata(product_id):
    meta = prod_meta_service.get_product_metadata(product_id)
    if meta:
        return jsonify(serialize_mongo_doc(meta)), 200
    return jsonify({"message": "No metadata found"}), 404


@frontend_bp.route("/api/meta/<int:product_id>", methods=["POST"])
@role_required(["admin"])
def create_product_metadata(product_id):
    product = prod_meta_service.get_product_metadata(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    try:
        new_meta = prod_meta_service.create_product_metadata(product)
        return jsonify(serialize_mongo_doc(new_meta)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@frontend_bp.route("/api/meta/<int:product_id>", methods=["PUT"])
@role_required(["admin"])
def update_product_metadata(product_id):
    updates = request.get_json()
    try:
        updated_meta = prod_meta_service.update_product_metadata(product_id, updates)
        if not updated_meta:
            return jsonify({"message": "Metadata not found"}), 404
        return jsonify(serialize_mongo_doc(updated_meta)), 200
        # return jsonify(updated_meta.to_mongo()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@frontend_bp.route("/api/meta/<int:product_id>", methods=["DELETE"])
@role_required(["admin"])
def delete_product_metadata(product_id):
    deleted = prod_meta_service.delete_product_metadata(product_id)
    if deleted:
        return jsonify({"message": "Metadata deleted"}), 200
    return jsonify({"message": "Metadata not found"}), 404
