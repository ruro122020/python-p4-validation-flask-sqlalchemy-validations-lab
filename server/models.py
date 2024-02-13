from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates("name")
    def validate_name(self, key, name):
      if not name:
        raise ValueError("name must be of type string and more than 1 characters")
      
      author = db.session.query(Author.id).filter_by(name = name).first()
      if author is not None:
         raise ValueError('name must be unique.')
      return name
    
    @validates("phone_number")
    def validate_phone_number(self, key, phone_number):
      int(phone_number)
      if len(phone_number) == 10:
        return phone_number
      else:
        raise ValueError('phone number must be 10 digits long')
      

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates("title")
    def validate_title(self, key, title):
       click_bait_words = ["Won't Believe", "Secret", "Top", "Guess"]
       
       if not any(word in title for word in click_bait_words):
        raise ValueError("title must be of type string and more than 1 character")
       else:
        return title
       
    @validates("content")
    def validate_content(self, key, content):
       if len(content) >= 250:
        return content
       else:
        raise ValueError('content must be at least 250 characters long')
    
    @validates("summary")
    def validate_summary(self, key, summary):
      if len(summary) <= 250:
        return summary
      else:
        raise ValueError("summary must be less than 250 characters long")
      
    @validates("category")
    def validate_category(self, key, category):
      if category == 'Fiction' or category == 'Non-Fiction':
        return category
      else:
        raise ValueError("category must be of fiction or non-fiction")
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
