from requests import Request, Session
import datetime
import time
import hmac, hashlib
# import json
# import math
# BASE_URL = 
ORDER_API = '/api/v1/redirect/orders'

class Order(object):
    # BASE_URL = 'http://sandbox.lan:9000/'

    def __init__(self, base_url, token=None, provider='Ksher', mid=None, timeout=10):
        self.token = token
        self.provider = provider
        self.mid = mid
        self.BASE_URL = base_url
        self.timeout = timeout

    def create(self,data):
        urlStr = self.BASE_URL+ORDER_API       
        return self._request('POST', urlStr,data=data)

    def query(self, order_id, params={}):
        urlStr = self.BASE_URL+ORDER_API+'/{}'.format(order_id)        
        return self._request('GET', urlStr,data=params)

    def refund(self, order_id, params={}):
        urlStr = self.BASE_URL+ORDER_API+'/{}'.format(order_id)
        return self._request('PUT', urlStr,data=params)

    def cancle(self, order_id):
        urlStr = self.BASE_URL+ORDER_API+'/{}'.format(order_id)        
        return self._request('DELETE', urlStr)

    def _request(self, method, url, data = {}):
        headers =  { "Content-Type": "application/json" }
        method = method.upper()
        if self.mid:
            data['mid'] = self.mid

        data['timestamp'] = str(self._make_timestamp())
        data['provider'] = self.provider
        data['signature'] = self._make_sign(ORDER_API,data)
        req = Request(method, url, headers=headers, json=data)
        prepped = req.prepare()
        s = Session()
        resp = s.send(prepped, timeout=self.timeout)
        s.close()
        return resp

    def generate_order_id(self, orderName='OrderAt'):
        curTime = datetime.datetime.now()
        timeStr = curTime.strftime('%Y%m%dT%H%M%S')
        orderName ='{}{}'.format(orderName, timeStr)
        return orderName

    def _make_timestamp(self):
        return int(time.time())

    # def _check_sign(self, sign):
        
    def _make_sign(self, url, data):
        # make sure it's is not include a signature value
        data.pop('signature', None)
        dataStr = ORDER_API + ''.join(sorted([f'{key}{value}' for key, value in data.items()]))
        dig = hmac.new(self.token.encode(), msg=dataStr.encode(), digestmod=hashlib.sha256).hexdigest()
        return dig

    
        
