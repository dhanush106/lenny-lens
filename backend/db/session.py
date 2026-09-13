from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from backend.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

# Keep a descriptive factory name for application code and scripts.  The
# previous name was imported throughout the project but was never defined,
# which prevented the API from importing at all.
async_session_maker = AsyncSessionLocal

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
