# units.py

from decimal import Decimal


class UnitConverter:
    def __init__(self):
        # Define conversion factors
        self.gram_to_ounce = 0.03527396
        self.gram_to_ounce_troy = 0.0321507
        self.gram_to_kilogram = 0.001

    def convert(self, value, from_unit, to_unit):
        conversion_factor = self.get_conversion_factor(from_unit, to_unit)
        if conversion_factor is not None:
            return round(Decimal(value) * Decimal(conversion_factor),4)
        else:
            raise ValueError(f"Conversion from {from_unit} to {to_unit} is not supported.")

    def get_conversion_factor(self, from_unit, to_unit):
        conversion_factors = {
            ('gram', 'ounce'): self.gram_to_ounce,
            ('gram', 'ounce_troy'): self.gram_to_ounce_troy,
            ('gram', 'kilogram'): self.gram_to_kilogram
        }
        return conversion_factors.get((from_unit, to_unit), None)
