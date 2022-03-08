from django.core.cache import cache


PRODUCT_OPTION_KEY = "product_option_pk_"


def get_and_incr_view_count_product_option(pk):
    """
    Возвращает счетчик просмотров ProductOption по pk модели,
    предварительно инкрементировав.
    """
    product_option_key = f"{PRODUCT_OPTION_KEY}{pk}"
    cache.get_or_set(product_option_key, 0)
    return cache.incr(product_option_key)


def get_view_count_product_option(pk):
    """
    Возвращает счетчик просмотров ProductOption по pk модели.
    """
    product_option_key = f"{PRODUCT_OPTION_KEY}{pk}"
    return cache.get_or_set(product_option_key, 0)


def get_all_view_count_product_option():
    """
    Возвращает dict со всеми имеющимися ключями и значениями.
    """
    product_option_key_all = f"{PRODUCT_OPTION_KEY}*"
    return cache.get_many(cache.keys(product_option_key_all))


def get_view_count_product_option_from_list(product_option_pks: list):
    """
    Возвращает dict со счетчиком просмотров для каждого pk из product_option_pks.
    """
    product_option_keys = [f"{PRODUCT_OPTION_KEY}{pk}" for pk in product_option_pks]
    return cache.get_many(product_option_keys)

