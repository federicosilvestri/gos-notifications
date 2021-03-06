from random import randint
from unittest.mock import Mock, patch

import requests
from werkzeug.exceptions import HTTPException

from tests.rao.rao_test import RaoTest


class TestRestaurantManager(RaoTest):

    @classmethod
    def setUpClass(cls):
        super(TestRestaurantManager, cls).setUpClass()
        from gooutsafe.rao.restaurant_manager import RestaurantManager
        cls.restaurant_manager = RestaurantManager
    
    @patch('gooutsafe.rao.restaurant_manager.requests.get')
    def test_get_restaurant_by_op_id_success(self, mock):
        mock.return_value = Mock(status_code=200, 
                            json = lambda:{
                                'restaurant_sheet':{
                                    'restaurant':{
                                        'owner_id':1,
                                        'tables':{},
                                        'availabilities': {},
                                    },
                                },
                            })
        response = self.restaurant_manager.get_owner_id_by_restaurant_id(randint(0, 999))
        assert response == 1

    @patch('gooutsafe.rao.restaurant_manager.requests.get')
    def test_get_restaurant_by_op_id_fail(self, mock):
        mock.return_value = Mock(status_code=400)
        with self.assertRaises(RuntimeError):
            response = self.restaurant_manager.get_owner_id_by_restaurant_id(randint(0, 999))