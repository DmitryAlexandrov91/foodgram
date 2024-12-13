import hashlib


class RecipeURlDecoder:

    def __init__(self):
        self.lib = {}

    def encode(self, long_url):
        """Кодирует длинную ссылку в короткую вида https://ma.rs/X7NYIol."""
        start_link = 'https://ma.rs/'
        hash_link = hashlib.md5(long_url.encode()).hexdigest()
        result_link = start_link + hash_link
        self.lib[result_link] = long_url
        return result_link

    def decode(self, short_url):
        """Декодирует короткую ссылку вида https://ma.rs/X7NYIol в исходную."""
        return self.lib[short_url]