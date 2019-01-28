from django.core.management.base import BaseCommand
from django_seed import Seed
seeder = Seed.seeder()
import random
from ...models import *

class Command(BaseCommand):

  # Examples of custom word lists you can instruct Django_Seed to use
  adjectives = [
  "Absorbing", "Adorable", "Adventurous", "Appealing",
  "Artistic", "Athletic", "Attractive", "Bold"]

  things = [
  "Alarm clock", "Armoire", "Backpack", "Bedding", "Bedspread", "Blankets", "Blinds", "Bookcase", "Books", "Broom", "Brush", "Bucket", "Calendar", "Candles", "Carpet", "Chair", "Chairs", "China", "Clock", "Coffee table", "Comb", "Comforter", "Computer"]

  departments = [
    "Human Resources", "Research & Development", "Sales", "Management",
    "Ecommerce", "Marketing", "Finance", "Accounting", "Sanitation", "IT", "Training"]

  # this is where the magic happens
  def handle(self, *args, **options):
    
    # add departments
    # TODO - currently department names can duplicate, fix this so they only occur once
    seeder.add_entity(Department, 6, {
      'budget': lambda x: random.randint(10000, 2500000),
      'name': lambda x: seeder.faker.word(ext_word_list=["Human Resources", "Research & Development", "Sales", "Management",
    "Ecommerce", "Marketing", "Finance", "Accounting", "Sanitation", "IT", "Training"])
    })

    # add employees
    seeder.add_entity(Employee, 15, {
      'isSupervisor': lambda x: random.randint(0, 1)
    })

    # add computers
    # we can toy with the purchase/decomm dates 
    seeder.add_entity(Computer, 20, {
      'purchaseDate': lambda x: seeder.faker.date_time_between(start_date='-10y', end_date='now'),
      'decommissionDate': lambda x: seeder.faker.date_time_between(start_date='-5y', end_date='now'),
      'manufacturer': lambda x: seeder.faker.word(ext_word_list=["Dell", "Lenovo", "HP", "Apple", "Gateway", "Compaq", "Micron"]),
      'model': lambda x: seeder.faker.word(ext_word_list=["Slow", "Fast", "Chunk", "Boat Anchor", "Speedy", "Nimble"])
    })

    seeder.execute()