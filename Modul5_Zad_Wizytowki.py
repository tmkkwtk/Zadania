class BaseContact:
    def __init__(self, first_name, last_name, phone, email):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email

    def contact(self):
        text = f"Wybieram numer {self.phone} i dzwonię do {self.first_name} {self.last_name}"
        return text

    @property
    def label_length(self):
        return len(self.first_name) + len(self.last_name) + 1


class BusinessContact(BaseContact):
    def __init__(self, occupancy, company, work_phone, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.occupancy = occupancy
        self.company = company
        self.work_phone = work_phone

    def contact(self):
        return f"Wybieram numer {self.work_phone} i dzwonię do {self.first_name} {self.last_name}"


def create_contacts(type, quantity):
    from faker import Faker

    fake = Faker("pl_PL")
    cards = []
    for i in range(quantity):

        data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "phone": fake.phone_number(),
            "email": fake.email(),
        }

        if type == "business":
            data["occupancy"] = fake.job()
            data["company"] = fake.company()
            data["work_phone"] = fake.phone_number()

            cards.append(BusinessContact(**data))
        else:
            cards.append(BaseContact(**data))

    for card in cards:
        text = ""
        for key, value in vars(card).items():
            text += key + ": " + value + " "
        print(text)
        print(card.contact())
        print(card.label_length)


create_contacts("base", 5)
