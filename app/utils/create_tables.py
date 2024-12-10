from app import create_app
from sqlalchemy.orm import Session
from app.models.model import Base
from app.models.model import Employee  

app = create_app()

def create_employee():
  with app.app_context():
    session: Session = app.session

    new_employee = Employee(
        name="Anderson", 
        email="anderson@email.com", 
        password="1234", 
        isAdmin=True
    )

    session.add(new_employee)
    session.commit()

with app.app_context():
  Base.metadata.create_all(bind=app.session.get_bind())
  create_employee()