import wx
import os
import xmltodict
import configparser
from random import choices
from helper import show_message
from helper import row_builder
from picture import Picture
from kijiji_api import KijijiApiException


# Добавить фильтр только для png jpg...
def get_random_photos(path, num=1):          # 2 - коли
    files = os.listdir(path)
    files = [f for f in files if os.path.isfile(path + '/' + f)]  # Filtering only the files.
    photo_names = choices(files, k=num)
    # photo_path = path + "\\" + photo_name
    return photo_names


class PostAdDialog(wx.Dialog):

    def __init__(self, kijiji_api, user_id, email, user_token, updateSpreadsheet):
        """Constructor"""
        super().__init__(None, title="Post Ad", size=wx.Size(480, 530)) # Size(480, 640)
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.updateSpreadsheet = updateSpreadsheet
        self.kijiji_api = kijiji_api
        self.user_id = user_id
        self.email = email
        self.user_token = user_token
        self.locations = self.kijiji_api.get_locations(self.user_id, self.user_token)
        sub_locations = self.get_sub_locations()
        # Категории
        self.cats = kijiji_api.get_categories(user_id, user_token)
        # print(self.cats) #TEMP
        # print(cats['cat:categories']['cat:category']['cat:category'][0]['cat:category'])
        # print(self.cats['cat:categories']['cat:category']['cat:category'][0]['cat:category'][1])
        main_cats = []
        for i in self.cats['cat:categories']['cat:category']['cat:category']:
            main_cats.append(i['cat:id-name'])
            # print(i['cat:id-name'])
        main_cats.pop()
        # print(type(self.cats))

        # #Локация TEMP
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
        self.title = wx.TextCtrl(self, value=self.config['DEFAULT_AD']['TITLE'], size=(420, -1))
        self.title.SetMaxLength(64)
        main_sizer.Add(row_builder([title_lbl, self.title]))

        # create some text
        category_lbl = wx.StaticText(self, label="Main Category :")
        category_lbl.SetFont(font)
        self.main_cats_list = wx.Choice(self, wx.ID_ANY, choices=main_cats)
        # self.main_cats_list.SetSelection(0)
        self.main_cats_list.SetSelection(main_cats.index(self.config['DEFAULT_AD']['MAIN_CATEGORY']))
        self.main_cats_list.Bind(wx.EVT_CHOICE, self.update_subcategories)
        # self.main_cats_list.Bind(wx.EVT_CHOICE, self.update_categories)
        main_sizer.Add(row_builder([category_lbl, self.main_cats_list]))

        subcategories_lbl = wx.StaticText(self, label="Subcategory :")
        subcategories_lbl.SetFont(font)
        self.subcategories_list = wx.ComboBox(self, wx.ID_ANY, style=wx.CB_READONLY,
                                              choices=self.get_subcategories(self.main_cats_list.GetCurrentSelection()))
        # self.subcategories_list.SetSelection(0)
        self.subcategories_list.SetSelection(self.get_subcategories(self.main_cats_list.GetCurrentSelection()).index(self.config['DEFAULT_AD']['SUBCATEGORY']))
        self.subcategories_list.Bind(wx.EVT_COMBOBOX, self.update_categories)
        main_sizer.Add(row_builder([subcategories_lbl, self.subcategories_list]))

        categories_lbl = wx.StaticText(self, label="Category :")
        categories_lbl.SetFont(font)
        self.categories_list = wx.ComboBox(self, wx.ID_ANY, size=(200, -1), style=wx.CB_READONLY,
                                           choices=self.get_categories(self.main_cats_list.GetCurrentSelection(),
                                                                       self.subcategories_list.GetCurrentSelection()))
        if self.categories_list.GetCount() < 1:
            self.categories_list.Disable()
        else:
            self.categories_list.Enable()
            # self.categories_list.SetSelection(0)
            self.categories_list.SetSelection(self.get_categories(self.main_cats_list.GetCurrentSelection(),
                                                                  self.subcategories_list.GetCurrentSelection()).index(self.config['DEFAULT_AD']['CATEGORY']))
        # self.main_cats_list.Bind(wx.EVT_CHOICE, self.update_categories)
        # self.main_cats_list.Bind(wx.EVT_COMBOBOX, self.update_categories)
        # self.subcategories_list.Bind(wx.EVT_COMBOBOX, self.update_subcategories)
        main_sizer.Add(row_builder([categories_lbl, self.categories_list]))

        description_lbl = wx.StaticText(self, label="Description :")
        description_lbl.SetFont(font)
        self.description = wx.TextCtrl(self, value=self.config['DEFAULT_AD']['DESCRIPTION'], size=(400, 150), style=wx.TE_MULTILINE)
        main_sizer.Add(row_builder([description_lbl, self.description]))

        photo_folder_lbl = wx.StaticText(self, label="Folder with Images :")
        photo_folder_lbl.SetFont(font)
        self.photo_folder = wx.DirPickerCtrl(self, id=wx.ID_ANY, path=self.config['DEFAULT_AD']['IMAGES_FOLDER'],
                                             message="Choose pictures directory", style=wx.DIRP_DEFAULT_STYLE,
                                             size=(400, -1))
        main_sizer.Add(row_builder([photo_folder_lbl, self.photo_folder]))

        locations_lbl = wx.StaticText(self, label="Location :")
        locations_lbl.SetFont(font)
        self.locations_list = wx.ComboBox(self, wx.ID_ANY, size=(400, -1), style=wx.CB_READONLY,
                                          choices=self.locs_to_strings(sub_locations))
        # self.locations_list.SetSelection(0)
        self.locations_list.SetSelection(self.locs_to_strings(sub_locations).index(self.config['DEFAULT_AD']['LOCATION']))
        main_sizer.Add(row_builder([locations_lbl, self.locations_list]))

        fulladdress_lbl = wx.StaticText(self, label="Full Address :")
        fulladdress_lbl.SetFont(font)
        self.fulladdress = wx.TextCtrl(self, value=self.config['DEFAULT_AD']['FULL_ADDRESS'], size=(400, -1))
        main_sizer.Add(row_builder([fulladdress_lbl, self.fulladdress]))

        zip_code_lbl = wx.StaticText(self, label="Zip-Code :")
        zip_code_lbl.SetFont(font)
        self.zip_code = wx.TextCtrl(self, value=self.config['DEFAULT_AD']['POSTAL_CODE'], size=(100, -1))
        main_sizer.Add(row_builder([zip_code_lbl, self.zip_code]))

        price_lbl = wx.StaticText(self, label="Price :")
        price_lbl.SetFont(font)
        self.price = wx.TextCtrl(self, value=self.config['DEFAULT_AD']['PRICE'], size=(80, -1))
        main_sizer.Add(row_builder([price_lbl, self.price]))

        post_btn = wx.Button(self, label="Post")
        post_btn.Bind(wx.EVT_BUTTON, self.post)
        btn_sizer.Add(post_btn, 0, wx.ALL, 5)

        main_sizer.Add(btn_sizer, 0, wx.CENTER)
        self.SetSizer(main_sizer)

    def post(self, event):

        photos_name_list = get_random_photos(self.photo_folder.GetPath(), int(self.config['DEFAULT_AD']['IMAGES_NUM'])) # второй аргумент - количество картинок
        photos_list = []
        for i in photos_name_list:
            photos_list.append(Picture(i, self.photo_folder.GetPath()))

        zip_code = self.zip_code.GetValue()
        location = self.kijiji_api.geo_location(zip_code)

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
                'loc:locations': {'loc:location': {'@id': self.get_location_id()}},
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
                    'types:latitude': str(location.latitude),
                    'types:longitude': str(location.longitude),
                    'types:full-address': self.fulladdress.GetValue(), # 'Norfolk County Hwy 59, Port Rowan, ON N0E 1M0'
                    'types:zip-code': zip_code,
                },
                'ad:visible-on-map': 'true',  # appears to make no difference if set to 'true' or 'false'
                'attr:attributes': None, # TEMP
                # 'attr:attributes': {'attr:attribute': [
                #     {'@localized-label': 'For Sale By', '@type': 'ENUM', '@accessibility-feature': 'false',
                #      '@name': 'forsaleby', 'attr:value': {'@localized-label': 'Owner', '#text': 'ownr'}},
                #     {'@localized-label': 'Condition', '@type': 'ENUM', '@accessibility-feature': 'false',
                #      '@name': 'condition',
                #      'attr:value': {'@localized-label': 'Used - Like new', '#text': 'usedlikenew'}}]},
                'pic:pictures': self.create_picture_payload(photos_list),
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

        print(payload)
        print("\n")

        xml_payload = xmltodict.unparse(payload, short_empty_elements=True)

        print(xml_payload)

        # Submit final payload
        try:
            ad_id = self.kijiji_api.post_ad(self.user_id, self.user_token, xml_payload)
            show_message(f"Ad #{str(ad_id)} has been posted!", 'Posted', wx.ICON_INFORMATION)
            self.Close()
            self.updateSpreadsheet()
        # except KijijiApiException as exception:
        except Exception as exception:
            show_message(str(exception), 'Error')

    def get_category_id(self):
        if self.categories_list.IsEnabled():
            id_name = self.categories_list.GetString(self.categories_list.GetCurrentSelection())
            res = None
            for i in \
            self.cats['cat:categories']['cat:category']['cat:category'][self.main_cats_list.GetCurrentSelection()][
                'cat:category'][self.subcategories_list.GetCurrentSelection()]['cat:category']:
                if i['cat:id-name'] == id_name:
                    res = i
                    break
            return res['@id']
        else:
            id_name = self.subcategories_list.GetString(self.subcategories_list.GetCurrentSelection())
            res = None
            for i in \
            self.cats['cat:categories']['cat:category']['cat:category'][self.main_cats_list.GetCurrentSelection()][
                'cat:category']:
                if i['cat:id-name'] == id_name:
                    res = i
                    break
            return res['@id']

    def get_location_id(self):
        id_name = self.locations_list.GetString(self.locations_list.GetCurrentSelection())
        locs = id_name.split(',')
        count = id_name.count(',')
        res = None
        # if count >= 2:
        for i in self.locations['loc:locations']['loc:location']['loc:location']:
            if i['loc:localized-name'] == locs[0]:
                for j in i['loc:location']:
                    if j['loc:localized-name'] == locs[1][1:]:
                        if count >= 2:
                            for k in j['loc:location']:
                                if k['loc:localized-name'] == locs[2][1:]:
                                    res = k
                                    break
                        else:
                            res = j
                            break
        return res['@id']

    def update_subcategories(self, event):
        if self.main_cats_list.GetCurrentSelection() == 4:
            self.price.Disable()        # Выключаем поле Price, если выбрана категория Services
        else:
            self.price.Enable()

        self.subcategories_list.Clear()
        # print(self.main_cats_list.GetCurrentSelection())
        self.subcategories_list.SetItems(self.get_subcategories(self.main_cats_list.GetCurrentSelection()))
        self.subcategories_list.SetSelection(0)

        self.update_categories(event)

    def update_categories(self, event):
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
            for i in self.cats['cat:categories']['cat:category']['cat:category'][index]['cat:category'][index2][
                'cat:category']:
                categories.append(i['cat:id-name'])
            return categories
        else:
            return []

    def get_subcategories(self, index):
        subcategories = []
        # subcategories = [{}]
        for i in self.cats['cat:categories']['cat:category']['cat:category'][index]['cat:category']:
            # subcategories.append({'id': i['@id'], 'name': i['cat:id-name']})
            subcategories.append(i['cat:id-name'])
        # print(subcategories)
        return subcategories

    def get_main_locations(self) -> list:
        locs = []
        for i in self.locations['loc:locations']['loc:location']['loc:location']:
            locs.append(i['loc:localized-name'])
        return locs

    def locs_to_strings(self, sub_locs) -> list:
        list_of_strings = []
        for key, value in sub_locs.items():
            for i, j in enumerate(value):
                if type(j) is dict:
                    for key2, value2 in j.items():
                        for b in value2:
                            # if len(b) > 1:
                            list_of_strings.append(str(key) + ", " + key2 + ", " + b)
                        # print(key2)
                        # print(value2)
                    # list_of_strings.append(str(key) + ", " + j[])
                elif type(j) is str:
                    list_of_strings.append(str(key) + ", " + j)

        return list_of_strings

    def get_sub_locations(self) -> dict:
        states = self.get_main_locations()
        locs = {}
        for i in states:
            locs[i] = []
        keys = list(locs)
        # print(locs)
        for i in range(len(keys)):
            for index, j in enumerate(
                    self.locations['loc:locations']['loc:location']['loc:location'][i]['loc:location']):
                if type(j) is dict:
                    if 'loc:location' not in j:
                        locs[keys[int(i)]].append(j['loc:localized-name'])
                    else:
                        sub_locs = {}
                        sub_locs[j['loc:localized-name']] = []
                        for index2, k in enumerate(j['loc:location']):
                            if type(k) is dict:
                                # print(k['loc:localized-name']) # class str
                                sub_locs[j['loc:localized-name']].append(k['loc:localized-name'])
                            # else:
                            #     print(k)  # TEMP
                            #     print(self.locations['loc:locations']['loc:location']['loc:location'][i]['loc:location'][index])  # TEMP
                            #     sub_locs[j['loc:localized-name']].append(self.locations['loc:locations']['loc:location']['loc:location'][i]['loc:location'][index]['loc:location']['loc:localized-name'])
                            #     print(type(self.locations['loc:locations']['loc:location']['loc:location'][i]['loc:location'][index]['loc:location']['loc:localized-name']))
                            # print(sub_locs)
                        locs[keys[int(i)]].append(sub_locs)
                        # sub_locs[j['loc:localized-name']].append(
                        #     self.locations['loc:locations']['loc:location']['loc:location'][i]['loc:location'][index][
                        #         'loc:location']['loc:localized-name'])
                        # print(self.locations['loc:locations']['loc:location']['loc:location'][i]['loc:location'][index]['loc:location'])
                        # print(sub_locs)
            # locs[keys[int(i)]].append(self.locations['loc:locations']['loc:location']['loc:location'][i]['loc:localized-name']) # Баг, который повторяет штаты

        locs['Territories'][0]['Nunavut'] = ['Iqaluit']
        locs['Territories'][1]['Northwest Territories'] = ['Yellowknife']
        locs['Territories'][2]['Yukon'] = ['Whitehorse']

        island_dict = {'Prince Edward Island': ['Charlottetown', 'Summerside']}
        locs['Prince Edward Island'].append(island_dict)

        return locs

    def create_picture_payload(self, data):
        """Build picture payload dict from file* fields."""
        payload = {'pic:picture': []}

        # Mapping of image size names to size in px
        image_sizes = {
            'extraLarge': 800,
            'large': 500,
            'normal': 400,
            'thumbnail': 64,
        }

        for value in data:
            link = self.kijiji_api.upload_image(self.user_id, self.user_token, value)

            # Add a separate link for each image size
            links = []
            for size_name, size_px in image_sizes.items():
                links.append({
                    '@rel': size_name,
                    '@href': f'{link}?rule=kijijica-{size_px}-jpg',
                })

            payload['pic:picture'].append({'pic:link': links})

        return payload if len(payload['pic:picture']) else {}
