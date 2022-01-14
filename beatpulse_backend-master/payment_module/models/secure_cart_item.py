class SecureCartItem:
    
    def __init__(self, beat_id: int, license_id: int, license_price: float, license_discounted_price: float, db_id: int):
        self.beat_id = beat_id
        self.license_id = license_id
        self.license_price = license_price
        self.license_discounted_price = license_discounted_price
        self.db_id = db_id
