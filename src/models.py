from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


#relacion uno es a uno

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(100),nullable=False, unique = True)
    password = db.Column(db.String(100), nullable=False)
    profile = db.relationship('Profile',cascade= "all,delete", backref ='user', uselist=False)  #JOIN SQL
    #solo hasta backref el profile va a devolver uno a muchos, si se especifica el uselist = false, devuelve un objeto y lo hace uno a uno.
    contacts = db.relationship('Contact',cascade= "all,delete", backref ='user')  #Aqui no se usa el uselist (Uno es a muchos)
    roles = db.relationship('Role', cascade="all, delete", secondary= "roles_user")

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "email": self.email
        }

    def serialize_with_roles(self):
        return{
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "email": self.email,
            "roles": self.roles()
        }





#por seguridad no devuelvo las contraseñas que no quiero retornar

    def serialize_with_profile(self):
        return{
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "email": self.email,
            "profile": self.profile.serialize(),
            "contacts": self.get_contacts(),
            "roles": self.get_roles()
        }

def get_contacts(self):
    return list(map(lambda contact: contact.serialize(), self.contacts))

def get_roles(self):
    return list(map(lambda contact: role.serialize(), self.roles))



def save(self):
    db.session.add(self)
    db.session.commit()

def update(self):
    db.session.commit()

def delete(self):
    db.session.delete(self)
    db.session.commit()


class Profile(db.Model):
    __tablename__='profiles'
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text, default="")
    twitter = db.Column(db.String(100), default="")
    facebook = db.Column(db.String(100), default="")
    instagram = db.Column(db.String(100), default="")
    linkedin = db.Column(db.String(100), default="")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)


    def serialize(self):
        return{
            "id": self.id,
            "bio": self.bio,
            "twitter": self.twitter,
            "facebook": self.facebook,
            "instagram": self.instagram,
            "linkedin": self.linkedin
        }

    def serialize_with_user(self):
        return{
            "id": self.id,
            "name": self.user.name + " " + self.user.lastname,
            "bio": self.bio,
            "twitter": self.twitter,
            "facebook": self.facebook,
            "instagram": self.instagram,
            "linkedin": self.linkedin
        }       
      
def save(self):
    db.session.add(self)
    db.session.commit()

def update(self):
    db.session.commit()

def delete(self):
    db.session.delete(self)
    db.session.commit()



#relacion uno es a muchos

class Contact(db.Model):
    __tablename__ = "contacts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    work = db.Column(db.String(200), nullable=False)
    phone_home = db.Column(db.String(200), default="")
    email = db.Column(db.String(100), default="")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)


    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "phone_work": self.phone_work,
            "phone_home": self.phone_home,
            "email": self.email
    
        }       
      
def save(self):
    db.session.add(self)
    db.session.commit()

def update(self):
    db.session.commit()

def delete(self):
    db.session.delete(self)
    db.session.commit()



    #OTRO EJEMPLO MUCHO ES A MUCHOS

class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    users = db.relationship('User', cascade="all, delete", secondary= "roles_user")



    def serialize(self):
        return{
            "id": self.id,
            "name": self.name
     
        }    

    def serialize_with_users(self):
        return{
            "id": self.id,
            "name": self.name,
            "users":self.get_users()
     
        }    



    def get_users(self)      :
        return list(map(lambda user: {"id": user.id , "name": user.name}, self.users))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class RoleUser(db.Model):
    __tablename__= 'roles_user'
    role_id  = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key= True)
    #Esta es una clave compuesta por que tiene 2 primary key.

#ondelete va adentro de la Foreign Key.

"""
cuando hago el flask db upgrade me tira este error:
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 7442dbae48ab -> 931657603ab4, empty message
ERROR [flask_migrate] Error: No support for ALTER of constraints in SQLite dialect. Please refer to the batch mode feature which allows for SQLite migrations using a copy-and-move strategy.
"""
