from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    status = Column(String, nullable=False, default="uploaded")
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    ingredients = relationship("Ingredient", back_populates="document")


class Allergen(Base):
    __tablename__ = "allergens"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)  # e.g. "Milk", "Peanuts", "Gluten"


# Junction table for the many-to-many relationship between ingredients and allergens.
# No model class needed here — this table has no extra data of its own, just the two links.
ingredient_allergens = Table(
    "ingredient_allergens",
    Base.metadata,
    Column("ingredient_id", Integer, ForeignKey("ingredients.id"), primary_key=True),
    Column("allergen_id", Integer, ForeignKey("allergens.id"), primary_key=True),
)


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # e.g. "Cream sauce"
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)

    document = relationship("Document", back_populates="ingredients")
    allergens = relationship("Allergen", secondary=ingredient_allergens)