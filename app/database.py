from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import settings

connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    user_id = Column(String(100), unique=True, nullable=False, index=True)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    goal = Column(String(100), nullable=False)
    intensity = Column(String(50), nullable=False)
    original_plan = Column(Text)
    updated_plan = Column(Text)
    nutrition_tip = Column(Text)
    feedback = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def create_tables(): Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
def get_user(db, user_id): return db.query(User).filter(User.user_id == user_id).first()
def get_all_users(db): return db.query(User).order_by(User.created_at.desc()).all()
def create_user(db, username, user_id, age, weight, goal, intensity):
    user = User(username=username,user_id=user_id,age=age,weight=weight,goal=goal,intensity=intensity)
    db.add(user); db.commit(); db.refresh(user); return user
def save_generated_plan(db, user_id, workout_plan, nutrition_tip):
    user=get_user(db,user_id)
    if not user: return None
    user.original_plan=workout_plan; user.nutrition_tip=nutrition_tip; db.commit(); db.refresh(user); return user
def save_updated_plan(db,user_id,updated_plan,feedback):
    user=get_user(db,user_id)
    if not user: return None
    user.updated_plan=updated_plan; user.feedback=feedback; db.commit(); db.refresh(user); return user
def delete_user(db,user_id):
    user=get_user(db,user_id)
    if not user: return False
    db.delete(user); db.commit(); return True
