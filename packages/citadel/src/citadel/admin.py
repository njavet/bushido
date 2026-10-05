from getpass import getpass

from sqlalchemy import select

from citadel.auth.passwords import hash_password
from citadel.conf import get_db_url
from citadel.persistence import SessionFactory
from citadel.persistence.models import Spartan


def create_user() -> None:
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    password = getpass("Password: ")
    db_url = get_db_url()
    sf = SessionFactory(db_url=db_url)

    with sf.session() as session:
        existing = session.scalar(select(Spartan).where(Spartan.email == email))

        if existing:
            raise RuntimeError("User already exists")

        spartan = Spartan(
            name=name,
            email=email,
            hashed_password=hash_password(password),
            is_active=True,
            is_admin=True,
        )

        session.add(spartan)
        session.commit()
        session.refresh(spartan)

        print(f"Created Spartan id={spartan.id}")
