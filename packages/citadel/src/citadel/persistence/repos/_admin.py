from sqlalchemy import func, select
from sqlalchemy.orm import Session

from citadel.auth.passwords import hash_password
from citadel.exceptions import AdminError
from citadel.schema.auth import RegisterRequest

from ..models import Spartan


class AdminRepo:
    def __init__(self, session: Session) -> None:
        self.session = session

    def fetch_spartan(self, username: str) -> Spartan | None:
        return self.session.scalar(select(Spartan).where(Spartan.username == username))

    def create_spartan(self, request: RegisterRequest) -> Spartan:
        existing_mail = self.session.scalar(
            select(Spartan).where(Spartan.email == request.email)
        )
        existing_username = self.session.scalar(
            select(Spartan).where(Spartan.username == request.username)
        )
        if existing_mail is not None:
            raise AdminError(f"{existing_mail} already exists")
        if existing_username is not None:
            raise AdminError(f"{existing_username} already exists")
        spartan = Spartan(
            username=request.username,
            email=request.email,
            hashed_password=hash_password(request.password),
        )
        self.session.add(spartan)
        return spartan

    def count(self) -> int:
        stmt = select(func.count()).select_from(Spartan)
        return self.session.scalar(stmt) or 0
