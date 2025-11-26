from flask import Flask, render_template, jsonify, request
from models import db, User, Post  

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  

with app.app_context():
    db.create_all()  


#with app.app_context(): 
#     user1 = User(username="khalid_dev", email="khalid@example.com", password="azerty123")
#      user2 = User(username="sara_writer", email="sara@example.com", password="writer2025")

#    db.session.add(user1)
#    db.session.commit()
#    db.session.add(user2)
#    db.session.commit()
#    user3 = User(
#        username="naima_blog",
#        email="naima@example.com",
#        password="n123456",
#        posts=[
#            Post(title="My first cooking article", body="Today I share my couscous recipe."),
#            Post(title="Travel experience", body="I visited Chefchaouen last summer.")
#        ]
#    )
#    db.session.add(user3)
#    db.session.commit()


@app.route("/")
def index():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)


#@app.route("/posts")
#def show_posts():
#    posts = Post.query.all()
#    return render_template("posts.html", posts=posts)

#@app.route("/users")
#def show_users():
#    users = User.query.all()
#    return render_template("users.html", users=users)


@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    users_list = []
    for user in users:
        users_list.append({
            "id": user.id,
            "username": user.username,
            "email": user.email
        })
    return jsonify(users_list), 200


@app.route("/users", methods=["POST"])
def create_usr():
    data = request.get_json()
    if not data or not all(k in data for k in ("username", "email", "password")):
        return jsonify({"error": "Missing data"}), 400

    if User.query.filter((User.username == data['username']) | (User.email == data['email'])).first():
        return jsonify({"error": "User already exists"}), 409

    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created", "id": new_user.id}), 201


@app.route("/posts", methods=["GET"])
def get_posts():
    posts = Post.query.all()
    posts_list = []
    for post in posts:
        posts_list.append({
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "author": {
                "id": post.author.id,
                "username": post.author.username,
                "email": post.author.email
            }
        })
    return jsonify(posts_list), 200


@app.route("/posts", methods=["POST"])
def create_pot():
    data = request.get_json()
    if not data or not all(k in data for k in ("title", "body", "user_id")):
        return jsonify({"error": "Missing data"}), 400

    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({"error": "User not found"}), 404

    new_post = Post(
        title=data['title'],
        body=data['body'],
        author=user  
    )
    db.session.add(new_post)
    db.session.commit()
    return jsonify({"message": "Post created", "id": new_post.id}), 201  


if __name__ == "__main__":
    app.run(debug=True)
