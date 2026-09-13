import asyncio
from backend.db.session import AsyncSessionLocal
from backend.models import User, Session, Message, Transcript, Chunk

async def seed_database():
    print("Seeding database with test records...")
    async with AsyncSessionLocal() as session:
        # Create a test user
        user = User(email="test@example.com", hashed_password="dummy_password", is_active=True)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        print(f"Added user: {user.email} (ID: {user.id})")

        # Create a test session
        chat_session = Session(user_id=user.id, title="Test Session")
        session.add(chat_session)
        await session.commit()
        await session.refresh(chat_session)
        print(f"Added session: {chat_session.title} (ID: {chat_session.id})")

        # Create a test message
        message = Message(session_id=chat_session.id, role="user", content="Hello, LennyLens!")
        session.add(message)
        await session.commit()
        print(f"Added message: {message.content}")

        # Create a test transcript
        transcript = Transcript(video_id="test_video_123", title="Test Podcast")
        session.add(transcript)
        await session.commit()
        await session.refresh(transcript)
        print(f"Added transcript: {transcript.title} (ID: {transcript.id})")

        # Create a test chunk with dummy embedding
        # pgvector takes lists/arrays of floats
        chunk = Chunk(
            transcript_id=transcript.id,
            start_time=0.0,
            end_time=10.0,
            text="This is a test transcript chunk.",
            embedding=[0.1] * 384
        )
        session.add(chunk)
        await session.commit()
        print(f"Added chunk to transcript {transcript.title}")

    print("Database seeding completed successfully!")

if __name__ == "__main__":
    asyncio.run(seed_database())
