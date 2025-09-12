from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Enum, Numeric,
    UniqueConstraint, func
)
from sqlalchemy.orm import relationship
from .db import Base
import enum

class Unit(Base):
    __tablename__ = "units"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    short = Column(String(16), nullable=False)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    sku = Column(String(64))
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False)
    unit = relationship("Unit")

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)

class Stock(Base):
    __tablename__ = "stock"
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    location_id = Column(Integer, ForeignKey("locations.id"), primary_key=True)
    qty = Column(Numeric(12, 3), nullable=False, default=0)
    product = relationship("Product")
    location = relationship("Location")
    __table_args__ = (UniqueConstraint('product_id','location_id', name='uq_stock_prod_loc'),)

class DocType(enum.Enum):
    in_ = "in"
    out = "out"
    invent = "invent"

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    type = Column(Enum(DocType, name="doc_type"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String(64))

class DocItem(Base):
    __tablename__ = "doc_items"
    id = Column(Integer, primary_key=True)
    doc_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    qty = Column(Numeric(12,3), nullable=False)
    document = relationship("Document")
    product = relationship("Product")
    location = relationship("Location")
