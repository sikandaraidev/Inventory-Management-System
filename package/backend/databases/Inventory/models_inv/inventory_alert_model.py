from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from package.backend.db_conn.aws_mysql import Base


class InventoryAlert(Base):
    __tablename__ = "inventory_alert"

    alert_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.product_id"))
    alert_type: Mapped[str] = mapped_column(String(50))
    alert_message: Mapped[str] = mapped_column(Text)
    alert_date: Mapped[str] = mapped_column(String(50))
    resolved: Mapped[str] = mapped_column(String(10), default="No")

    def __repr__(self) -> str:
        return f"<InventoryAlert(id={self.alert_id}, product_id={self.product_id}, type={self.alert_type})>"
