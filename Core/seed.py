from .models import Localidad
from faker import Faker

faker = Faker()

def seed_db():
    for  n in range(0,n):
        Localidad.objects.create(
            CodigoPosta = n,
            NombreLocalidad = faker.name()
        )