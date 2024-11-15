from app import db

place_amenity = db.Table('place_amenity',
                         db.Column('place_id', db.String(36), db.ForeignKey(
                             'place.id'), primary_key=True),
                         db.Column('amenity_id', db.String(36), db.ForeignKey(
                             'amenity.id'), primary_key=True)
                         )
