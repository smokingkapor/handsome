# -*- coding: utf-8 -*-
import requests
import six
from hashlib import md5
from urllib import urlencode


def encode_dict(params):
    return {k:six.u(v).encode('utf-8') if isinstance(v, str) else v.encode('utf-8') if isinstance(v, six.string_types) else v for k, v in six.iteritems(params)}


class Alipay(object):

    GATEWAY_URL = 'https://mapi.alipay.com/gateway.do'

    def __init__(self, pid, key, seller_email):
        self.key = key
        self.pid = pid
        self.default_params = {'_input_charset': 'utf-8',
                               'partner': pid,
                               'seller_email': seller_email,
                               'payment_type': '1'}

    def _generate_sign(self, params):
        src = '&'.join(['%s=%s' % (key, value) for key,
                        value in sorted(params.items())]) + self.key
        return md5(src.encode('utf-8')).hexdigest()

    def _check_params(self, params, names):
        if not all(k in params for k in names):
            raise MissingParameter('missing parameters')
        return

    def _build_url(self, service, **kw):
        params = self.default_params.copy()
        params['service'] = service
        params.update(kw)
        params.update({'sign_type': 'MD5',
                       'sign': self._generate_sign(params)})

        return '%s?%s' % (self.GATEWAY_URL, urlencode(encode_dict(params)))

    def create_direct_pay_by_user_url(self, **kw):
        '''即时到帐'''
        self._check_params(kw, ['out_trade_no', 'subject'])

        if not kw.get('total_fee') and \
           not (kw.get('price') and kw.get('quantity')):
            raise ParameterValueError('total_fee or (price && quantiry)\
             must have one')

        url = self._build_url('create_direct_pay_by_user', **kw)
        return url

    def create_partner_trade_by_buyer_url(self, **kw):
        '''担保交易'''
        names = ['out_trade_no', 'subject', 'logistics_type',
                 'logistics_fee', 'logistics_payment', 'price', 'quantity']
        self._check_params(kw, names)
        url = self._build_url('create_partner_trade_by_buyer', **kw)
        return url

    def trade_create_by_buyer_url(self, **kw):
        '''标准双接口'''
        names = ['out_trade_no', 'subject', 'logistics_type',
                 'logistics_fee', 'logistics_payment', 'price', 'quantity']
        self._check_params(kw, names)

        url = self._build_url('trade_create_by_buyer', **kw)
        return url

    def verify_notify(self, **kw):
        sign = kw.pop('sign')
        kw.pop('sign_type')
        if self._generate_sign(kw) == sign:
            return requests.get("https://mapi.alipay.com/gateway.do?service=notify_verify&partner=%s&notify_id=%s" % (self.pid, kw['notify_id'])).text == 'true'
        else:
            return False


class AlipayException(Exception):
    '''Base Alipay Exception'''


class MissingParameter(AlipayException):
    """Raised when the create payment url process is missing some
    parameters needed to continue"""


class ParameterValueError(AlipayException):
    """Raised when parameter value is incorrect
    """


def includeme(config):
    settings = config.registry.settings
    config.registry['alipay'] = Alipay(
        pid=settings.get('alipay.pid'),
        key=settings.get('alipay.key'),
        seller_email=settings.get('alipay.seller_email'))
