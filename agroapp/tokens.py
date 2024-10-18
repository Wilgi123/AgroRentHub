from django.contrib.auth.tokens import PasswordResetTokenGenerator


class FarmerTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.email)

class SupplierTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.email)

class DeliveryBoyTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.email)

farmer_token_generator = FarmerTokenGenerator()
supplier_token_generator = SupplierTokenGenerator()
deliveryboy_token_generator = DeliveryBoyTokenGenerator()
