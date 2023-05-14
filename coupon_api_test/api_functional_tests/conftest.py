import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine
from starlette.testclient import TestClient

from coupon_api.app.coupon_router import coupon_router
from coupon_api.app.main import app
from coupon_api.initialization.database import get_session


@pytest.fixture(name="session")
def session_fixture():
    """In memory empty sqlite session for testing"""
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="fast_api_client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    app.include_router(coupon_router)

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
