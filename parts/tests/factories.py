import factory 

from factory.django import DjangoModelFactory

from parts.models import Part

class PartsFactory(DjangoModelFactory):
    """
    Parts factory
    """ 
    class Meta:
        model = Part

    name = factory.Faker('name')
    sku = factory.Faker('ean')
    description = factory.Faker('catch_phrase')
    weight_ounces = factory.Faker('random_digit')
    is_active = factory.Faker('random_element', elements=(0,1))