# Packages
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Modules
from db.postgresql_db import Base


class UsersModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    author_pseudonym: Mapped[str] = mapped_column(unique=True, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    books: Mapped["BooksModel"] = relationship(back_populates="users")
