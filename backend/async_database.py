from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

'''Creating an async engine for the database'''
engine = create_async_engine('postgresql+asyncpg://postgres:uriel999@localhost/shifttest')

'''Creating an async session with the engine'''
local_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False,
                                   autocommit=False)


async def get_database() -> AsyncSession:
    '''Generates an async session for the database'''
    async with local_session() as session:
        yield session