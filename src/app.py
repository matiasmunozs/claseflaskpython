from flask import Flask, render_template, jsonify,request
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, User, Profile




app = Flask(__name__)
app.url_map.slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

db.init_app(app) 
Migrate(app, db) 
CORS(app)

# db init: inicializa mi estructura para mis migraciones.
# db migrate se encarga de crea las estructuras, en este caso los query para guardar en la base de datos.
# db upgrade se encarga de llevar estas migraciones hacia la base de datos. --> es de decir se encarga de convertir esas migraciones en comandos SQL para generar esas tablas dentro de mi base de datos


#importante: instale la extension de SQLITE para poder ver la base de datos en el visual studio.
#tambien instale MySQL (la version de Weijan Chen )


@app.route("/")
def main():
    return render_template('index.html')

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize()serialize_with_profile, users))

    return jsonify(users), 200

@app.route('/api/users', methods=['POST'])
def post_users():

    name =request.json.get('name')
    lastname =request.json.get('lastname')
    email =request.json.get('email')
    password =request.json.get('password')

    bio =request.json.get('bio', "")
    twitter =request.json.get('twitter', "")
    facebook =request.json.get('facebook', "")
    instagram =request.json.get('instagram', "")
    linkedin =request.json.get('linkedin', "")



    if not email: return jsonify({"Status":False, "msg":"Email is required"}), 400

    user = User.query.filter_by(email=email).first()
    if user: return jsonify({"Status":False, "msg": "Email already in use"}), 400

    """
    user = User()
    user.name = name
    user.lastname = lastname
    user.email = email
    user.password = password
    user.save()

    profile = Profile()
    profile.bio = bio
    profile.twitter = twitter
    profile.facebook = facebook
    profile.instagram = instagram
    profile.linkedin = linkedin
    profile.user_id = user.id
    profile.save()
    """

    user = User()
    user.name = name
    user.lastname = lastname
    user.email = email
    user.password = password

    profile = Profile()
    profile.bio = bio
    profile.twitter = twitter
    profile.facebook = facebook
    profile.instagram = instagram
    profile.linkedin = linkedin
    user.profile = profile

    user.save()

    return jsonify(user.serialize_with_profile()), 201


@app.route('/api/users/<int:id>', methods=['PUT'])
def put_users(id):

    name =request.json.get('name')
    lastname =request.json.get('lastname')
    email =request.json.get('email')
    password =request.json.get('password')

    user = User.query.get(id)
    user.name = name
    user.lastname = lastname
    user.email = email
    user.password = password
    user.update()

    return jsonify(user.serialize()), 200




@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_users(id):

    user = User.query.get(id)

    if not user: return jsonify({"Status": False, "msg":"User does not exist"}), 404

    user.delete()

    return jsonify({"Status": True, "msg":"User deleted"}), 200








if __name__== '__main__':
    app.run()