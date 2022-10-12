import wx
import xmltodict
from kijiji_api import KijijiApiException
from helper import show_message
from helper import row_builder


class PostAdDialog(wx.Dialog):

    def __init__(self, kijiji_api, user_id, user_token):
        """Constructor"""
        super().__init__(None, title="Post Ad", size=wx.Size(320, 480))

        # payload = {
        #     'ad:ad': {
        #         '@xmlns:ad': 'http://www.ebayclassifiedsgroup.com/schema/ad/v1',
        #         '@xmlns:cat': 'http://www.ebayclassifiedsgroup.com/schema/category/v1',
        #         '@xmlns:loc': 'http://www.ebayclassifiedsgroup.com/schema/location/v1',
        #         '@xmlns:attr': 'http://www.ebayclassifiedsgroup.com/schema/attribute/v1',
        #         '@xmlns:types': 'http://www.ebayclassifiedsgroup.com/schema/types/v1',
        #         '@xmlns:pic': 'http://www.ebayclassifiedsgroup.com/schema/picture/v1',
        #         '@xmlns:vid': 'http://www.ebayclassifiedsgroup.com/schema/video/v1',
        #         '@xmlns:user': 'http://www.ebayclassifiedsgroup.com/schema/user/v1',
        #         '@xmlns:feature': 'http://www.ebayclassifiedsgroup.com/schema/feature/v1',
        #         '@id': '',
        #         'cat:category': {'@id': '14970001'},
        #         'loc:locations': {'loc:location': {'@id': '1700248'}},
        #         'ad:ad-type': {'ad:value': 'OFFERED'},
        #         'ad:title': 'Reminders of Him: A Novel',
        #         'ad:description': 'A troubled young mother yearns for a shot at redemption in this heartbreaking yet hopeful story from #1 New York Times bestselling author Colleen Hoover.',
        #         'ad:price': {'types:price-type': {'types:value': 'SPECIFIED_AMOUNT'}},
        #         'ad:account-id': '1025825002',
        #         'ad:email': 'fzwopyipfslicecgxkcx@inbox.lv',
        #         'ad:poster-contact-email': 'fzwopyipfslicecgxkcx@inbox.lv',
        #         # 'ad:poster-contact-name': None,  # Not sent by Kijiji app
        #         'ad:phone': None,
        #         'ad:ad-address': {
        #             'types:radius': 400,
        #             'types:latitude': '42.5814',
        #             'types:longitude': '-80.39912',
        #             'types:full-address': 'Norfolk County Hwy 59, Port Rowan, ON N0E 1M0',
        #             'types:zip-code': 'N0E 1M0',
        #         },
        #         'ad:visible-on-map': 'true',  # appears to make no difference if set to 'true' or 'false'
        #         'attr:attributes': {'attr:attribute': [{'@localized-label': 'For Sale By', '@type': 'ENUM', '@accessibility-feature': 'false', '@name': 'forsaleby', 'attr:value': {'@localized-label': 'Owner', '#text': 'ownr'}}, {'@localized-label': 'Condition', '@type': 'ENUM', '@accessibility-feature': 'false', '@name': 'condition', 'attr:value': {'@localized-label': 'Used - Like new', '#text': 'usedlikenew'}}]},
        #         'pic:pictures': None,
        #         'vid:videos': None,
        #         'ad:adSlots': None,
        #         'ad:listing-tags': None,
        #     }
        # }
        #
        # # Set price if dollar amount given
        # payload['ad:ad']['ad:price'].update({
        #     'types:amount': '13.37',
        #     'types:currency-iso-code': {'types:value': 'CAD'},  # Assume Canadian dollars
        #     })
        #
        # xml_payload = xmltodict.unparse(payload, short_empty_elements=True)
        #
        # # Submit final payload
        # try:
        #     print(kijiji_api.post_ad(user_id, user_token, xml_payload))
        # except KijijiApiException as exception:
        #     show_message(str(exception), 'Error')

        # Категории
        self.cats = kijiji_api.get_categories(user_id, user_token)
        # print(cats['cat:categories']['cat:category']['cat:category'][0]['cat:category'])
        # print(self.cats['cat:categories']['cat:category']['cat:category'][0]['cat:category'][1])
        main_cats = []
        for i in self.cats['cat:categories']['cat:category']['cat:category']:
            main_cats.append(i['cat:id-name'])
            # print(i['cat:id-name'])
        main_cats.pop()
        # print(type(self.cats))

        # #Локация
        # locs = kijiji_api.get_locations(user_id, user_token)
        # print(locs)

        # create the sizers
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # create some fonts
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
        font_2 = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL)

        title_lbl = wx.StaticText(self, label="Title :")
        title_lbl.SetFont(font)
        title = wx.TextCtrl(self, value="", size=(250, -1))
        main_sizer.Add(row_builder([title_lbl, title]))

        # create some text
        category_lbl = wx.StaticText(self, label="Main Category :")
        category_lbl.SetFont(font)
        self.main_cats_list = wx.Choice(self, wx.ID_ANY, choices=main_cats)
        self.main_cats_list.SetSelection(0)
        self.main_cats_list.Bind(wx.EVT_CHOICE, self.update_subcategories)
        main_sizer.Add(row_builder([category_lbl, self.main_cats_list]))

        subcategories_lbl = wx.StaticText(self, label="Subcategory :")
        subcategories_lbl.SetFont(font)
        self.subcategories_list = wx.ComboBox(self, wx.ID_ANY, style=wx.CB_READONLY,
                                              choices=self.get_subcategories(self.main_cats_list.GetCurrentSelection()))
        self.subcategories_list.SetSelection(0)
        # self.subcategories_list.Bind(wx.EVT_COMBOBOX, self.update_subcategories)
        main_sizer.Add(row_builder([subcategories_lbl, self.subcategories_list]))

        description_lbl = wx.StaticText(self, label="Description :")
        description_lbl.SetFont(font)
        description = wx.TextCtrl(self, value="", size=(250, 150), style=wx.TE_MULTILINE)
        main_sizer.Add(row_builder([description_lbl, description]))

        price_lbl = wx.StaticText(self, label="Price :")
        price_lbl.SetFont(font)
        price = wx.TextCtrl(self, value="", size=(100, -1))
        main_sizer.Add(row_builder([price_lbl, price]))

        post_btn = wx.Button(self, label="Post")
        post_btn.Bind(wx.EVT_BUTTON, self.post)
        btn_sizer.Add(post_btn, 0, wx.ALL, 5)

        main_sizer.Add(btn_sizer, 0, wx.CENTER)
        self.SetSizer(main_sizer)

    def post(self, event):
        print(1)

    def update_subcategories(self, event):
        self.subcategories_list.Clear()
        # print(self.main_cats_list.GetCurrentSelection())
        self.subcategories_list.SetItems(self.get_subcategories(self.main_cats_list.GetCurrentSelection()))
        self.subcategories_list.SetSelection(0)

    def get_subcategories(self, index):
        subcategories = []
        for i in self.cats['cat:categories']['cat:category']['cat:category'][index]['cat:category']:
            subcategories.append(i['cat:id-name'])
            # print(i['cat:id-name'])
        return subcategories
