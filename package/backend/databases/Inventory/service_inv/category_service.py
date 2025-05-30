from package.backend.databases.Inventory.models_inv.category_model import Category
from package.backend.db_conn.aws_mysql import get_session


def get_all_categories():
    return Category.query.order_by(Category.name).all()


def get_category(category_id):
    return Category.query.get_or_404(category_id)


def create_category(data):
    db = next(get_session())
    cat = Category(**data)
    db.session.add(cat)
    db.session.commit()
    return cat


def update_category(category, data):
    db = next(get_session())
    for key, value in data.items():
        setattr(category, key, value)
    db.session.commit()
    return category


def delete_category(category):
    db = next(get_session())
    db.session.delete(category)
    db.session.commit()
