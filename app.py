from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
db = SQLAlchemy(app)

class Product(db.Model):
    product_id = db.Column(db.String(50), primary_key=True)
    
    def __repr__(self):
        return f"Product(product_id='{self.product_id}'"
    
class Location(db.Model):
    location_id = db.Column(db.String(50), primary_key=True)
    
    def __repr__(self):
        return f"Location(location_id='{self.location_id}'"
    
class ProductMovement(db.Model):
    movement_id = db.Column(db.String(50), primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now)
    from_location = db.Column(db.String(50), db.ForeignKey('location.location_id'))
    to_location = db.Column(db.String(50), db.ForeignKey('location.location_id'))
    product_id = db.Column(db.String(50), db.ForeignKey('product.product_id'))
    qty = db.Column(db.Integer)
    
    from_location_rel = db.relationship('Location', foreign_keys=[from_location])
    to_location_rel = db.relationship('Location', foreign_keys=[to_location])
    product_rel = db.relationship('Product', foreign_keys=[product_id])
    
    def __repr__(self):
        return f"ProductMovement(movement_id='{self.movement_id}', timestamp='{self.timestamp}', " \
               f"from_location='{self.from_location}', to_location='{self.to_location}', " \
               f"product_id='{self.product_id}', qty={self.qty})"

# with app.app_context():
#     db.create_all()

# Product routes
@app.route('/product', methods=['POST', 'GET'])
def insert_product():
    if request.method == 'POST':
        product_id = request.form['product_id']
        product = Product.query.get(product_id)
        if product:
            product.product_id = product_id
        else:
            product = Product(product_id=product_id)
        try:
            db.session.add(product)
            db.session.commit()
            return redirect('/product')
        except:
            return "There was an error inserting the product"
    else:
        products = Product.query.all()
        return render_template('product.html', products=products)

@app.route('/product/update/<string:id>', methods=['POST','GET'])
def update_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.product_id = request.form['product_id']
        
        try:
            db.session.commit()
            return redirect('/product')
        except:
            return "There was an error updating the product."
    else:
        return render_template('updateproduct.html', product=product)

@app.route('/product/delete/<string:id>')
def delete_product(id):
    product_to_delete = Product.query.get_or_404(id)
    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        return redirect('/product')
    except:
        return "There was an error deleting the product."


# Location routes
@app.route('/location', methods=['POST', 'GET'])
def insert_location():
    if request.method == 'POST':
        location_id = request.form['location_id']
        location = Location.query.get(location_id)
        if location:
            location.location_id = location_id
        else:
            location = Location(location_id=location_id)
        try:
            db.session.add(location)
            db.session.commit()
            return redirect('/location')
        except:
            return "There was an error inserting the location."
    else:
        locations = Location.query.all()
        return render_template('location.html', locations=locations)

@app.route('/location/update/<string:id>', methods=['POST','GET'])
def update_location(id):
    location = Location.query.get_or_404(id)
    if request.method == 'POST':
        location.location_id = request.form['location_id']
        
        try:
            db.session.commit()
            return redirect('/location')
        except:
            return "There was an error updating the location."
    else:
        return render_template('updatelocation.html', location=location)

@app.route('/location/delete/<string:id>')
def delete_location(id):
    location_to_delete = Location.query.get_or_404(id)
    try:
        db.session.delete(location_to_delete)
        db.session.commit()
        return redirect('/location')
    except:
        return "There was an error deleting the location."

# Product Movement routes
@app.route('/movement', methods=['POST', 'GET'])
def insert_movement():
    if request.method == 'POST':
        movement_id = request.form['movement_id']
        product_id = request.form['product_id']
        from_location = request.form['from_location']
        to_location = request.form['to_location']
        qty = request.form['qty']
        product_movement_exists = ProductMovement.query.filter_by(movement_id=movement_id).first()
        if product_movement_exists:
            return "This product movement already exists. Please update the existing one."
        if not from_location and not to_location:
            return "Please provide either of the two locations"
        movement = ProductMovement(movement_id=movement_id,product_id=product_id, 
                                   from_location=from_location, to_location=to_location, qty=qty)
        try:
            db.session.add(movement)
            db.session.commit()
            return redirect('/movement')
        except Exception as error:
            return f'There was an error inserting the product movement. {error}'
    else:
        movements = ProductMovement.query.all()
        products = Product.query.all()
        locations = Location.query.all()
        return render_template('movement.html', movements=movements, products=products, locations=locations )


@app.route('/movement/update/<string:id>', methods=['POST','GET'])
def update_movement(id):
    movement = ProductMovement.query.get_or_404(id)
    if request.method == 'POST':
        movement.movement_id = request.form['movement_id']
        movement.product_id = request.form['product_id']
        movement.from_location = request.form['from_location']
        movement.to_location = request.form['to_location']
        movement.qty = request.form['qty']
        movement.timestamp = datetime.now()
        try:
            
            db.session.commit()
            return redirect('/movement')
        except Exception as error:
            return f'There was an error updating the product movement. {error}'
    else:
        products = Product.query.all()
        locations = Location.query.all()
        return render_template('updatemovement.html', movement=movement, products=products, locations=locations )

@app.route('/movement/delete/<string:id>')
def delete_movement(id):
    movement_to_delete = ProductMovement.query.get_or_404(id)
    try:
        db.session.delete(movement_to_delete)
        db.session.commit()
        return redirect('/movement')
    except Exception as error:
        return f'There was an error deleting the product movement. {error}'

# Report route
@app.route('/report')
def generate_report():
    locations = Location.query.all()
    report_data=[]
    total_balance_data=[]
    for location in locations:
        product_balances = {}
        total_balance = 0
        movements = ProductMovement.query.filter((ProductMovement.from_location == location.location_id)
                                                 or (ProductMovement.to_location == location.location_id)).all()
        print(movements)
        for movement in movements:
            if movement.product_id not in product_balances:
                product_balances[movement.product_id]=0
            if movement.from_location == location.location_id:
                product_balances[movement.product_id] -= movement.qty
            if movement.to_location == location.location_id:
                product_balances[movement.product_id] += movement.qty
        for product_id, balance in product_balances.items():
            total_balance += balance
            report_data.append({'product_id': product_id, 'location': location.location_id, 'qty': balance})
        total_balance_data.append({'location': location.location_id, 'qty': total_balance})
    total = 0
    for item in total_balance_data:
        total += item['qty']
    total_balance_data.append({'location': 'Total', 'qty': total})
    return render_template('report.html', report_data=report_data, total_balance_data=total_balance_data)

# Home route
@app.route('/')
def hello():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)