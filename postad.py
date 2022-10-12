import wx
import xmltodict
from kijiji_api import KijijiApiException
from helper import show_message
from helper import row_builder


class PostAdDialog(wx.Dialog):

    def __init__(self, kijiji_api, user_id, email, user_token):
        """Constructor"""
        super().__init__(None, title="Post Ad", size=wx.Size(320, 480))
        self.kijiji_api = kijiji_api
        self.user_id = user_id
        self.email = email
        self.user_token = user_token

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
        self.title = wx.TextCtrl(self, value="", size=(250, -1))
        main_sizer.Add(row_builder([title_lbl, self.title]))

        # create some text
        category_lbl = wx.StaticText(self, label="Main Category :")
        category_lbl.SetFont(font)
        self.main_cats_list = wx.Choice(self, wx.ID_ANY, choices=main_cats)
        self.main_cats_list.SetSelection(0)
        self.main_cats_list.Bind(wx.EVT_CHOICE, self.update_subcategories)
        # self.main_cats_list.Bind(wx.EVT_CHOICE, self.update_categories)
        main_sizer.Add(row_builder([category_lbl, self.main_cats_list]))

        subcategories_lbl = wx.StaticText(self, label="Subcategory :")
        subcategories_lbl.SetFont(font)
        self.subcategories_list = wx.ComboBox(self, wx.ID_ANY, style=wx.CB_READONLY,
                                              choices=self.get_subcategories(self.main_cats_list.GetCurrentSelection()))
        self.subcategories_list.SetSelection(0)
        self.subcategories_list.Bind(wx.EVT_COMBOBOX, self.update_categories)
        main_sizer.Add(row_builder([subcategories_lbl, self.subcategories_list]))

        categories_lbl = wx.StaticText(self, label="Category :")
        categories_lbl.SetFont(font)
        self.categories_list = wx.ComboBox(self, wx.ID_ANY, size=(200, -1),  style=wx.CB_READONLY,
                                              choices=self.get_categories(self.main_cats_list.GetCurrentSelection(),
                                                                          self.subcategories_list.GetCurrentSelection()))
        if self.categories_list.GetCount() < 1:
            self.categories_list.Disable()
        else:
            self.categories_list.Enable()
            self.categories_list.SetSelection(0)
        # self.main_cats_list.Bind(wx.EVT_CHOICE, self.update_categories)
        # self.main_cats_list.Bind(wx.EVT_COMBOBOX, self.update_categories)
        # self.subcategories_list.Bind(wx.EVT_COMBOBOX, self.update_subcategories)
        main_sizer.Add(row_builder([categories_lbl, self.categories_list]))

        description_lbl = wx.StaticText(self, label="Description :")
        description_lbl.SetFont(font)
        self.description = wx.TextCtrl(self, value="", size=(250, 150), style=wx.TE_MULTILINE)
        main_sizer.Add(row_builder([description_lbl, self.description]))

        fulladdress_lbl = wx.StaticText(self, label="Full Address :")
        fulladdress_lbl.SetFont(font)
        self.fulladdress = wx.TextCtrl(self, value="", size=(200, -1))
        main_sizer.Add(row_builder([fulladdress_lbl, self.fulladdress]))

        zip_code_lbl = wx.StaticText(self, label="Zip-code :")
        zip_code_lbl.SetFont(font)
        self.zip_code = wx.TextCtrl(self, value="", size=(100, -1))
        main_sizer.Add(row_builder([zip_code_lbl, self.zip_code]))

        price_lbl = wx.StaticText(self, label="Price :")
        price_lbl.SetFont(font)
        self.price = wx.TextCtrl(self, value="", size=(80, -1))
        main_sizer.Add(row_builder([price_lbl, self.price]))

        post_btn = wx.Button(self, label="Post")
        post_btn.Bind(wx.EVT_BUTTON, self.post)
        btn_sizer.Add(post_btn, 0, wx.ALL, 5)

        main_sizer.Add(btn_sizer, 0, wx.CENTER)
        self.SetSizer(main_sizer)

    def post(self, event):

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
                'cat:category': {'@id': self.get_category_id()},
                'loc:locations': {'loc:location': {'@id': '1700248'}},
                'ad:ad-type': {'ad:value': 'OFFERED'},
                'ad:title': self.title.GetValue(),
                'ad:description': self.description.GetValue(),
                'ad:price': {'types:price-type': {'types:value': 'SPECIFIED_AMOUNT'}},
                'ad:account-id': self.user_id,
                'ad:email': self.email,
                'ad:poster-contact-email': self.email,
                # 'ad:poster-contact-name': None,  # Not sent by Kijiji app
                'ad:phone': None,
                'ad:ad-address': {
                    'types:radius': 400,
                    'types:latitude': '42.5814',
                    'types:longitude': '-80.39912',
                    'types:full-address': 'Norfolk County Hwy 59, Port Rowan, ON N0E 1M0',
                    'types:zip-code': 'N0E 1M0',
                },
                'ad:visible-on-map': 'true',  # appears to make no difference if set to 'true' or 'false'
                'attr:attributes': {'attr:attribute': [{'@localized-label': 'For Sale By', '@type': 'ENUM', '@accessibility-feature': 'false', '@name': 'forsaleby', 'attr:value': {'@localized-label': 'Owner', '#text': 'ownr'}}, {'@localized-label': 'Condition', '@type': 'ENUM', '@accessibility-feature': 'false', '@name': 'condition', 'attr:value': {'@localized-label': 'Used - Like new', '#text': 'usedlikenew'}}]},
                'pic:pictures': None,
                'vid:videos': None,
                'ad:adSlots': None,
                'ad:listing-tags': None,
            }
        }

        # Set price if dollar amount given
        payload['ad:ad']['ad:price'].update({
            'types:amount': self.price.GetValue(),
            'types:currency-iso-code': {'types:value': 'CAD'},  # Assume Canadian dollars
            })

        xml_payload = xmltodict.unparse(payload, short_empty_elements=True)

        # Submit final payload
        try:
            print(self.kijiji_api.post_ad(self.user_id, self.user_token, xml_payload))
        except KijijiApiException as exception:
            show_message(str(exception), 'Error')

    def get_category_id(self):
        if self.categories_list.IsEnabled():
            id_name = self.categories_list.GetString(self.categories_list.GetCurrentSelection())
            res = None
            for i in self.cats['cat:categories']['cat:category']['cat:category'][self.main_cats_list.GetCurrentSelection()]['cat:category'][self.subcategories_list.GetCurrentSelection()]['cat:category']:
                if i['cat:id-name'] == id_name:
                    res = i
                    break
            return res['@id']
        else:
            id_name = self.subcategories_list.GetString(self.subcategories_list.GetCurrentSelection())
            res = None
            for i in self.cats['cat:categories']['cat:category']['cat:category'][self.main_cats_list.GetCurrentSelection()]['cat:category']:
                if i['cat:id-name'] == id_name:
                    res = i
                    break
            return res['@id']

    def update_subcategories(self, event):
        print(1)
        self.subcategories_list.Clear()
        # print(self.main_cats_list.GetCurrentSelection())
        self.subcategories_list.SetItems(self.get_subcategories(self.main_cats_list.GetCurrentSelection()))
        self.subcategories_list.SetSelection(0)

        self.update_categories(event)

    def update_categories(self, event):
        print(2)
        self.categories_list.Clear()
        # print(self.main_cats_list.GetCurrentSelection())
        self.categories_list.SetItems(self.get_categories(self.main_cats_list.GetCurrentSelection(),
                                                          self.subcategories_list.GetCurrentSelection()))
        if self.categories_list.GetCount() < 1:
            self.categories_list.Disable()
        else:
            self.categories_list.Enable()
            self.categories_list.SetSelection(0)

    def get_categories(self, index, index2):
        # print(self.cats['cat:categories']['cat:category']['cat:category'][index]['cat:category'][index2])
        if 'cat:category' in self.cats['cat:categories']['cat:category']['cat:category'][index]['cat:category'][index2]:
            categories = []
            for i in self.cats['cat:categories']['cat:category']['cat:category'][index]['cat:category'][index2]['cat:category']:
                categories.append(i['cat:id-name'])
            return categories
        else:
            return []

    def get_subcategories(self, index):
        subcategories = []
        #subcategories = [{}]
        for i in self.cats['cat:categories']['cat:category']['cat:category'][index]['cat:category']:
            #subcategories.append({'id': i['@id'], 'name': i['cat:id-name']})
            subcategories.append(i['cat:id-name'])
        #print(subcategories)
        return subcategories
