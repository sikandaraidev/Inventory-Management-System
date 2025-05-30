from package.backend.databases.Inventory.models_inv.supplier_model import Supplier
from package.backend.db_conn.aws_mysql import get_session


def get_all_suppliers():
    return Supplier.query.order_by(Supplier.name).all()


def get_supplier(supplier_id):
    return Supplier.query.get_or_404(supplier_id)


def create_supplier(data):
    db = next(get_session())
    sup = Supplier(**data)
    db.session.add(sup)
    db.session.commit()
    return sup


def update_supplier(supplier, data):
    db = next(get_session())
    for key, value in data.items():
        setattr(supplier, key, value)
    db.session.commit()
    return supplier


def delete_supplier(supplier):
    db = next(get_session())
    db.session.delete(supplier)
    db.session.commit()
