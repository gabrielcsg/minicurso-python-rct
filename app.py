from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecommerce.db"

db = SQLAlchemy(app)

# models

# product
class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120), nullable=False)
  price = db.Column(db.Float, nullable=False)
  description = db.Column(db.Text)


# define routes
  
# add product
@app.route('/api/products/add', methods=['POST'])
def add_product():
  data = request.json
  if ('name' in data and 'price' in data):
    product = Product(
      name=data['name'],
      price=data['price'],
      description=data.get('description', '') # default value
    )
    db.session.add(product)
    db.session.commit()

    return  { "message" : "Product added successfully" }
  
  return jsonify({"message": "Invalid product data"}), 400

# remove product
@app.route('/api/products/delete/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
  product = Product.query.get(product_id)
  if (product):
    db.session.delete(product)
    db.session.commit()
    return  { "message" : "Product deleted successfully" }

  return jsonify({"message": "Product not founded"}), 404

@app.route("/")
def hello_world():
  return "Hello World!"


if __name__ == "__main__":
  app.run(debug=True)
