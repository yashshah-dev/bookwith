from src.config.app_config import TEST_USER_ID
from src.config.db import SessionLocal
from src.infrastructure.postgres.user.user_dto import UserDTO

# Note: Execute table creation only on first run (not needed if tables already exist)
# Base.metadata.create_all(bind=engine)


def seed_data():
    session = SessionLocal()
    try:
        # Example seed data creation
        seed_items = [UserDTO(id=TEST_USER_ID, username="testuser", email="example@example.com")]

        # Add multiple seed data at once
        session.add_all(seed_items)
        session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    seed_data()
