import phonenumbers
from faker.providers.phone_number.uk_UA import Provider


class CustomPhoneProvider(Provider):
    def phone_number(self):
        """ Creation of our own phone_number provider """
        while True:
            phone_number = self.numerify(self.random_element(self.formats))
            parsed_number = phonenumbers.parse(phone_number, 'UA')
            if phonenumbers.is_valid_number(parsed_number):
                return phonenumbers.format_number(
                    parsed_number,
                    phonenumbers.PhoneNumberFormat.E164
                )
