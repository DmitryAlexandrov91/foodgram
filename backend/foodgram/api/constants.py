import os
from django.conf import settings


MIN_COOKING_TIME = 1
MIN_INGREDIENT_QUANITY = 1
MAX_LENGTH_NAME = 150
MAX_LENGTH_EMAIL = 254
CSV_FOLDER_PATH = os.path.join(settings.BASE_DIR, 'media\\shopping_carts')