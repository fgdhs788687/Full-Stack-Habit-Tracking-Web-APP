import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool # StaticPool ensures that every thread shares the same in-memory database
)

# Session Factory for testing purpose:
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# For every test function we will create a fresh database:
@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

# or we can write @pytest.fixture(scope="function") as this is the same as @pytest.fixture here the scope is function by default:
@pytest.fixture
def auth_headers(client):
    payload = {
        "email": "testuser@gmail.com",
        "password": "testuser123",
        "timezone": "Asia/Kolkata"
    }
    response = client.post('/auth/register', json=payload)

    login_response = client.post(
        '/auth/login', data = {'username':'testuser@gmail.com', 'password':'testuser123'}
    )
    token = login_response.json()['access_token']
    return {'Authorization': f'Bearer {token}'}