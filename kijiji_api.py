from xml.parsers.expat import ExpatError, errors
from httpx_socks import SyncProxyTransport
import httpx
import xmltodict
from singletonmeta import SingletonMeta


class KijijiApiException(Exception):
    """KijijiApi class exception"""


class KijijiApi(metaclass=SingletonMeta):
    """API for interfacing with Kijiji site
    This class is stateless and does not manage user logins on its own.
    Must login first to use methods that require a user ID and token.
    Methods raise KijijiApiException on errors
    """
    def __init__(self, session=None, proxy=None):

        # Base API URL
        self.base_url = 'https://mingle.kijiji.ca/api'

        # Kijiji app version number
        self.app_ver = '17.7.0'

        # Common HTTP header fields
        self.headers = {
            'Accept': 'application/xml',
            'Accept-Language': 'en-CA',
            'User-Agent': f'com.ebay.kijiji.ca {self.app_ver} (LGE Nexus 5; Android 6.0.1; en_US)',
            'X-ECG-VER': '3.6',
        }

        if session:
            if not isinstance(session, httpx.Client):
                raise KijijiApiException("'session' kwarg must be an httpx.Client object")

            self.session = session

            # Append common headers
            self.session.headers = self.headers
        else:
            # Kijiji sometimes takes a bit longer to respond to API requests
            # e.g. for loading conversations
            timeout = httpx.Timeout(30.0, connect=30.0)
            # Added proxy
            if proxy is not None:
                transport = SyncProxyTransport.from_url('socks5://' + proxy.get_username() + ':' + proxy.get_password()
                                                        + '@' + proxy.get_host() + ':' + proxy.get_port())
                self.session = httpx.Client(timeout=timeout, headers=self.headers, transport=transport)
            else:
                self.session = httpx.Client(timeout=timeout, headers=self.headers)

    def login(self, username, password):
        """Login to Kijiji
        :param username: login username
        :param password: login password
        :return: Tuple of user ID and session token
        """
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {
            'username': username,
            'password': password,
            'socialAutoRegistration': 'false',
        }

        r = self.session.post(f'{self.base_url}/users/login', headers=headers, data=payload)
        # print(r.text)
        doc = self._parse_response(r.text)

        if r.status_code == 200:
            try:
                user_id = doc['user:user-logins']['user:user-login']['user:id']
                email = doc['user:user-logins']['user:user-login']['user:email']
                token = doc['user:user-logins']['user:user-login']['user:token']
            except KeyError as e:
                raise KijijiApiException(f"User ID and/or user token not found in response text: {e}")
            return user_id, token
        else:
            raise KijijiApiException(self._error_reason(doc))

    def get_ad(self, user_id, token, ad_id=None):
        """Get existing ad(s)
        If ad_id is left unspecified, query all ads
        :param user_id: user ID number
        :param token: session token
        :param ad_id: ad ID number
        :return: response data dict
        """
        headers = self._headers_with_auth(user_id, token)
        url = f'{self.base_url}/users/{user_id}/ads'
        if ad_id:
            url += f'/{ad_id}'
        else:
            # Query all ads
            url += '?size=50' \
                   '&page=0' \
                   '&_in=id,title,price,ad-type,locations,ad-status,category,pictures,start-date-time,features-active,view-ad-count,user-id,phone,email,rank,ad-address,phone-click-count,map-view-count,ad-source-id,ad-channel-id,contact-methods,attributes,link,description,feature-group-active,end-date-time,extended-info,highest-price'

        r = self.session.get(url, headers=headers)

        doc = self._parse_response(r.text)

        if r.status_code == 200:
            return doc
        else:
            raise KijijiApiException(self._error_reason(doc))

    def get_profile(self, user_id, token):
        """Get profile data
        :param user_id: user ID number
        :param token: session token
        :return: response data dict
        """
        headers = self._headers_with_auth(user_id, token)

        r = self.session.get(f'{self.base_url}/users/{user_id}/profile', headers=headers)

        doc = self._parse_response(r.text)

        if r.status_code == 200:
            return doc
        else:
            raise KijijiApiException(self._error_reason(doc))

    def delete_ad(self, user_id, token, ad_id):
        """Delete ad
        :param user_id: user ID number
        :param token: session token
        :param ad_id: ad ID number
        :return: boolean indicating if deletion was successful
        """
        headers = self._headers_with_auth(user_id, token)

        r = self.session.delete(f'{self.base_url}/users/{user_id}/ads/{ad_id}', headers=headers)

        if r.status_code == 204:
            return True
        else:
            raise KijijiApiException(self._error_reason(self._parse_response(r.text)))

    @staticmethod
    def _headers_with_auth(user_id, token):
        return {'X-ECG-Authorization-User': f'id="{user_id}", token="{token}"'}

    @staticmethod
    def _parse_response(text):
        try:
            doc = xmltodict.parse(text)
        except ExpatError as e:
            raise KijijiApiException(f"Unable to parse text: {errors.messages[e.code]}")
        return doc

    @staticmethod
    def _error_reason(doc):
        messages = []
        try:
            base = doc['api-base-error']

            # Three different possible error types - search through all
            for err_type in ['api-error', 'api-field-error', 'api-debug-error']:
                err_type_plural = err_type + 's'  # Error type name with an appended 's'

                if err_type_plural in base and base[err_type_plural]:
                    if err_type in base[err_type_plural] and base[err_type_plural][err_type]:
                        # Check if there are multiple error messages in the same error type
                        if isinstance(base[err_type_plural][err_type], list):
                            for err in base[err_type_plural][err_type]:
                                messages.append(err_type + ': ' + err['message'])
                        else:
                            messages.append(err_type + ': ' + base[err_type_plural][err_type]['message'])
        except (TypeError, KeyError):
            return 'Unknown API error'
        return messages

    @staticmethod
    def _error_reason_mobile(doc):
        try:
            return doc['message']
        except KeyError:
            return 'Unknown mobile API error'