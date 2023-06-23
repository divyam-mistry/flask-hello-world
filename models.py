from app import db
from datetime import datetime

class Product(db.Model):
    product_id = db.Column(db.String(50), primary_key=True)
    
    def __repr__(self):
        return '<Product %r>' % self.product_id
    
class Location(db.Model):
    location_id = db.Column(db.String(50), primary_key=True)
    
    def __repr__(self):
        return '<Location %r>' % self.location_id
    
class ProductMovement(db.Model):
    movement_id = db.Column(db.String(50), primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    from_location = db.Column(db.String(50), db.ForeignKey('location.location_id'))
    to_location = db.Column(db.String(50), db.ForeignKey('location.location_id'))
    product_id = db.Column(db.String(50), db.ForeignKey('product.product_id'))
    qty = db.Column(db.Integer)
    
    from_location_rel = db.relationship('Location', foreign_keys=[from_location])
    to_location_rel = db.relationship('Location', foreign_keys=[to_location])
    product_rel = db.relationship('Product', foreign_keys=[product_id])
    
    def __repr__(self):
        return '<ProductMovement %r>' % self.movement_id