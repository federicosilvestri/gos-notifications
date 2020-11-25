import os
import requests


class RestaurantManager(object):
    """
    This class represent the Resource Access Object.
    """
    RESTAURANT_URL = 'http://%s:%s' % (
        os.getenv('RESTAURANTS_MS_HOST', None),
        os.getenv('RESTAURANTS_MS_PORT', None)
    )

    """Timeout for HTTP request"""
    TIMEOUT_SECONDS = 20

    @classmethod
    def get_owner_id_by_restaurant_id(cls, restaurant_id: int) -> str:
        try:
            response = requests.get(url='%s/restaurant/%s' % (cls.RESTAURANT_URL, restaurant_id),
                                    timeout=cls.TIMEOUT_SECONDS)
            if response.status_code != 200:
                raise RuntimeError('The restaurant does not exist!')

            json_response = response.json()
            return json_response['restaurant_sheet']['owner_id']
        except(requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            raise RuntimeError('Cannot connect to restaurant ms. Check the microservice')
