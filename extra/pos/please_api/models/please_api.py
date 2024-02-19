import requests, logging
import json
from requests.exceptions import ConnectionError, HTTPError, Timeout
_logger = logging.getLogger(__name__)

user_demo = 'admincerezas'
clave_demo = 'Camica33235525'

url_session = "https://pleaseco.azurewebsites.net/api/account/login"
url_get_store = "https://pleaseco.azurewebsites.net/clientapi/clientorder/GetStores"
url_create_so = "https://pleaseco.azurewebsites.net/clientapi/clientorder/create"
url_get_tracking = "https://pleaseco.azurewebsites.net/clientapi/clientorder/track?o={}"
url_tracking_state = "https://pleaseco.azurewebsites.net/clientapi/clientorder/GetOrderStatus?o={}"

class PleaseAPI():
	user = False
	password = False

	def __init__(self, user, password):
		self.user = user
		self.password = password

	def set_data_json(self, user=False, password=False):
		data = {
			"userName": user or self.user,
			"password": password or self.password
		}
		html_json = json.dumps(data, indent=4, separators=(',', ': '))
		return html_json

	def get_session(self):
		data = self.set_data_json()
		headers = {
			'Content-Type': 'application/json'
		}
		try:
			r = requests.post(url_session, data=data, headers=headers)
		except (ConnectionError, HTTPError) as e:
			_logger.warning('ConnectionError HTTPError %s' %e)
			return False
		except (ConnectionError, Timeout) as e:
			_logger.warning('ConnectionError  Timeout %s' %e)
			return False
		_logger.info('\n PLEASE CONECTION API status_code: %s' % r.status_code)
		if r.status_code == 200:
			return r.json()
		return False

	def get_stores(self):
		token = self.get_session()
		if not token:
			return False
		headers = {
			"Content-Type": "application/json",
			"Authorization": "Bearer %s" %token.get('token')
		}
		try:
			r = requests.get(url_get_store, headers=headers)
		except (ConnectionError, HTTPError) as e:
			_logger.warning('ConnectionError HTTPError %s' %e)
			return False
		except (ConnectionError, Timeout) as e:
			_logger.warning('ConnectionError  Timeout %s' %e)
			return False
		if r.status_code == 200:
			_logger.info('\n get_stores %s \n' %r.content)
			return r.json()
		return False

	def create_so(self, order, lines):
		token = self.get_session()
		if not token:
			return False
		datas = self.set_data_so(order, lines)
		headers = {
			"Content-Type": "application/json",
			"Authorization": "Bearer %s" %token.get('token')
		}
		data = json.dumps(datas, indent=4, separators=(',', ': '))
		try:
			r = requests.post(url_create_so, data=data, headers=headers)
		except (ConnectionError, HTTPError) as e:
			_logger.warning('ConnectionError HTTPError %s' %e)
			return False
		except (ConnectionError, Timeout) as e:
			_logger.warning('ConnectionError  Timeout %s' %e)
			return False
		_logger.info('\n PLEASE API status_code: %s' %r.status_code)
		if r.status_code == 200:
			return (r.content).decode("utf-8")
		if r.status_code == 400:
			state_track = self.get_tracking_state(order.get('storeOrderNumber'))
			if state_track:
				return (r.content).decode("utf-8")
			else:
				return False
			return (r.content).decode("utf-8")
		return False

	def get_traking_so(self, track_code):
		token = self.get_session()
		if not token:
			return False
		headers = {
			"Content-Type": "application/json",
			"Authorization": "Bearer %s" %token.get('token')
		}

		try:
			r = requests.get(url_get_tracking.format(track_code), headers=headers)
		except (ConnectionError, HTTPError) as e:
			_logger.info('ConnectionError HTTPError %s' %e)
			return False
		except (ConnectionError, Timeout) as e:
			_logger.info('ConnectionError  Timeout %s' %e)
			return False
		if r.status_code == 200:
			_logger.info('\n get_traking_so %s \n' %r.content)
			return r.json()
		return False

	def get_tracking_state(self, track_code):
		token = self.get_session()
		if not token:
			return False
		headers = {
			"Content-Type": "application/json",
			"Authorization": "Bearer %s" %token.get('token')
		}

		try:
			r = requests.get(url_tracking_state.format(track_code), headers=headers)
		except (ConnectionError, HTTPError) as e:
			_logger.info('ConnectionError HTTPError %s' %e)
			return False
		except (ConnectionError, Timeout) as e:
			_logger.info('ConnectionError  Timeout %s' %e)
			return False
		if r.status_code == 200:
			_logger.info('\n get_tracking_state %s \n' %r.content)
			return r.json()
		return False

	def set_data_so(self, order, lines):
		data = {
			"storeOrderNumber": order.get('storeOrderNumber'),
			"totalPrice": order.get("totalPrice"),
			"shippingAddress": order.get("shippingAddress"),
			"city": order.get("city"),
			"customerName": order.get("customerName"),
			"customerPhoneNumber": order.get("customerPhoneNumber"),
			"cashOnDelivery": order.get("cashOnDelivery"),
			"sticker": order.get("sticker", False),
			"ContainerNumber": order.get('ContainerNumber'),
			"storeId": order.get("storeId"), # Esto solo si existe mas de dos tiendas, aun no logro comprender
			}
		if order.get("customerEmail"):
			data.update(
				customerEmail =  order.get("customerEmail")
				)
		if order.get("customerNote"):
			data.update(
				customerNote =  order.get("customerNote")
				)

		detail = []
		for l in lines:
			vals = {
				"name": l.get('name'),
				"quantity": l.get('quantity'),
				"price": l.get('price')
			}
			detail.append(vals)
		data.update(details = detail)
		return data