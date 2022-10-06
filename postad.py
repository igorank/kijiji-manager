import wx
import xmltodict
from helper import show_message
from helper import row_builder


class PostAdDialog(wx.Dialog):

    def __init__(self, kijiji_api, user_id, user_token):
        """Constructor"""
        super().__init__(None, title="Post Ad", size=wx.Size(480, 480))

        payload = {
            'ad:ad': {
                '@xmlns:ad': 'http://www.ebayclassifiedsgroup.com/schema/ad/v1',
                '@xmlns:cat': 'http://www.ebayclassifiedsgroup.com/schema/category/v1',
                '@xmlns:loc': 'http://www.ebayclassifiedsgroup.com/schema/location/v1',
                '@xmlns:attr': 'http://www.ebayclassifiedsgroup.com/schema/attribute/v1',
                '@xmlns:types': 'http://www.ebayclassifiedsgroup.com/schema/types/v1',
                '@xmlns:pic': 'http://www.ebayclassifiedsgroup.com/schema/picture/v1',
                '@xmlns:vid': 'http://www.ebayclassifiedsgroup.com/schema/video/v1',
                '@xmlns:user': 'http://www.ebayclassifiedsgroup.com/schema/user/v1',
                '@xmlns:feature': 'http://www.ebayclassifiedsgroup.com/schema/feature/v1',
                '@id': '',
                'cat:category': {'@id': '14970001'},
                'loc:locations': {'loc:location': {'@id': '1700286'}},
                'ad:ad-type': {'ad:value': 'OFFERED'},
                'ad:title': 'Atomic Habits',
                'ad:description': 'The #1 New York Times bestseller. Over 4 million copies sold!\r\nUsed. No rips.',
                'ad:price': {'types:price-type': {'types:value': 'SPECIFIED_AMOUNT'}},
                'ad:account-id': '1025801083',
                'ad:email': 'gvsdfdknapbxrtkucgvm@inbox.lv',
                'ad:poster-contact-email': 'gvsdfdknapbxrtkucgvm@inbox.lv',
                # 'ad:poster-contact-name': None,  # Not sent by Kijiji app
                'ad:phone': None,
                'ad:ad-address': {
                    'types:radius': 400,
                    'types:latitude': '49.24542',
                    'types:longitude': '-122.97849',
                    'types:full-address': 'Fitzgerald Ave, Burnaby, BC V5G 3R8',
                    'types:zip-code': 'V5G 3R8',
                },
                'ad:visible-on-map': 'true',  # appears to make no difference if set to 'true' or 'false'
                'attr:attributes': [{'@localized-label': 'For Sale By', '@type': 'ENUM', '@accessibility-feature': 'false', '@name': 'forsaleby', 'attr:value': {'@localized-label': 'Owner', '#text': 'ownr'}}, {'@localized-label': 'Condition', '@type': 'ENUM', '@accessibility-feature': 'false', '@name': 'condition', 'attr:value': {'@localized-label': 'Used - Good', '#text': 'usedgood'}}],
                'pic:pictures': None,
                'vid:videos': None,
                'ad:adSlots': None,
                'ad:listing-tags': None,
            }
        }

        payload['ad:ad']['ad:price'].update({
            'types:amount': '7.00',
            'types:currency-iso-code': {'types:value': 'CAD'},  # Assume Canadian dollars
        })

        xml_payload = xmltodict.unparse(payload, short_empty_elements=True)

        # Submit final payload
        print(kijiji_api.post_ad(user_id, user_token, xml_payload))

        # create the sizers
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # create some fonts
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
        font_2 = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL)

        # create some text
        profileid_lbl = wx.StaticText(self, label="User ID :")
        profileid_lbl.SetFont(font)
        self.profileid = wx.StaticText(self, label="")
        self.profileid.SetFont(font_2)
        profileid_sizer = row_builder([profileid_lbl, self.profileid])

        main_sizer.Add(btn_sizer, 0, wx.CENTER)
        self.SetSizer(main_sizer)