from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

# from sqlalchemy.orm import relationship
# from package.databases.Inventory.models_inv.product_model import Product
# from package.databases.Inventory.models_inv.user_model import User
from package.backend.db_conn.aws_mysql import Base


class SalesStock(Base):
    __tablename__ = "sales_stock"

    sale_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.product_id"))
    quantity: Mapped[int] = mapped_column(Integer)
    selling_price: Mapped[float] = mapped_column(Float)
    sale_date: Mapped[str] = mapped_column(String(50))
    sold_by_user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # product: Mapped["Product"] = relationship("Product", back_populates="sales_stocks")
    # sold_by_user: Mapped["User"] = relationship("User", back_populates="sales_stocks")

    def __repr__(self) -> str:
        return f"<SalesStock(id={self.sale_id}, product_id={self.product_id}, quantity={self.quantity})>"
