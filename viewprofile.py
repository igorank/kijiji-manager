import wx
from helper import show_message
from kijiji_api import KijijiApi
from helper import row_builder
from postad import PostAdDialog
from ObjectListView import ObjectListView, ColumnDefn


class AD(object):

    def __init__(self, ad_id, title, category, price, views, start_date, end_date):
        self.ad_id = ad_id
        self.title = title
        self.category = category
        self.price = price
        self.views = views
        self.start_date = start_date
        self.end_date = end_date


def dateConverter(string):
    try:
        x = string.split("T")
        return x[0] + ' ' + x[1][:8]
    except AttributeError:
        return


class ViewDialog(wx.Dialog):

    # def __init__(self, selected_row, title="Profile"):
    def __init__(self, selected_row, config, proxy):
        """Constructor"""
        super().__init__(None, title="%s's profile" % selected_row.email, size=wx.Size(640, 480))
        # super().__init__(None, title=title)
        self.config = config
        self.user_id = selected_row.user_id
        self.email = selected_row.email
        self.token = selected_row.token
        self.k_api = KijijiApi(proxy=proxy)
        self.profile_info = self.k_api.get_profile(self.user_id, self.token)

        # create the sizers
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # create some fonts
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
        font_2 = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL)

        # create some text
        profileid_lbl = wx.StaticText(self, label="User ID :")
        profileid_lbl.SetFont(font)
        self.profileid = wx.StaticText(self, label=self.profile_info['user:user-profile']['user:user-id'])
        self.profileid.SetFont(font_2)
        profileid_sizer = row_builder([profileid_lbl, self.profileid])

        registration_date_lbl = wx.StaticText(self, label="Registration date :")
        registration_date_lbl.SetFont(font)
        self.registration_date = wx.StaticText(self, label=self.profile_info['user:user-profile'][
                                                               'user:user-registration-date'][:10])
        self.registration_date.SetFont(font_2)
        t_var = profileid_lbl.GetSize()[0] + self.profileid.GetSize()[0] + registration_date_lbl.GetSize()[0] + \
                self.registration_date.GetSize()[0]
        spacer = self.GetSize()[0] - t_var
        profileid_sizer.AddSpacer(spacer - int(t_var / 5))  # 60 отступы
        profileid_sizer.Add(registration_date_lbl, 0, wx.ALL, 5)
        profileid_sizer.Add(self.registration_date, 0, wx.ALL, 5)
        main_sizer.Add(profileid_sizer, 0, wx.ALL)

        name_lbl = wx.StaticText(self, label="Name :")
        name_lbl.SetFont(font)
        self.name = wx.StaticText(self, label=self.profile_info['user:user-profile']['user:user-display-name'])
        self.name.SetFont(font_2)
        name_sizer = row_builder([name_lbl, self.name])

        activeads_num_lbl = wx.StaticText(self, label="Active Ads :")
        activeads_num_lbl.SetFont(font)
        self.ads_num = wx.StaticText(self, label=self.profile_info['user:user-profile']['user:user-active-ad-count'])
        self.ads_num.SetFont(font_2)
        name_sizer.AddSpacer(
            (spacer - (name_lbl.GetSize()[0] + self.name.GetSize()[0])) + self.registration_date.GetSize()[
                0])  # 64 отступы
        name_sizer.Add(activeads_num_lbl, 0, wx.ALL, 5)
        name_sizer.Add(self.ads_num, 0, wx.ALL, 5)
        main_sizer.Add(name_sizer, 0, wx.ALL)

        email_lbl = wx.StaticText(self, label="Email :")
        email_lbl.SetFont(font)
        self.email_adr = wx.StaticText(self, label=self.profile_info['user:user-profile']['user:user-email'])
        self.email_adr.SetFont(font_2)
        main_sizer.Add(row_builder([email_lbl, self.email_adr]), 0, wx.ALL)

        self.dataOlv = ObjectListView(self, wx.ID_ANY, sortable=False, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.dataOlv.SetEmptyListMsg("No Ads")

        # if int(self.profile_info['user:user-profile']['user:user-active-ad-count']) > 0:
        #     self.ads = self.k_api.get_ad(self.user_id, self.token)
        self.updateSpreadsheet()
        self.setData()

        post_ad_btn = wx.Button(self, label="Post Ad")
        post_ad_btn.Bind(wx.EVT_BUTTON, self.on_post)
        btn_sizer.Add(post_ad_btn, 0, wx.ALL, 5)

        delete_ad_btn = wx.Button(self, label="Delete Ad")
        delete_ad_btn.Bind(wx.EVT_BUTTON, self.on_delete)
        btn_sizer.Add(delete_ad_btn, 0, wx.ALL, 5)

        main_sizer.Add(self.dataOlv, 1, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(btn_sizer, 0, wx.CENTER)
        self.SetSizer(main_sizer)

    def on_delete(self, event):
        selected_row = self.dataOlv.GetSelectedObject()

        if not selected_row:
            show_message('Please select one advertisement from the list!', 'Error')
            return

        status = self.k_api.delete_ad(self.user_id, self.token, selected_row.ad_id)

        if status:
            show_message("Ad has been removed!", 'Deleted', wx.ICON_INFORMATION)
        else:
            show_message('Something went wrong! Please try again later.', 'Error')

        self.updateSpreadsheet()

    def on_post(self, event):
        with PostAdDialog(self.k_api, self.user_id, self.email, self.token, self.config, self.updateSpreadsheet) as dlg:
            dlg.ShowModal()

        # self.updateSpreadsheet()

    def updateSpreadsheet(self):
        ads = self.k_api.get_ad(self.user_id, self.token)
        print(ads) # TEMP

        data = []
        if 'ad:ad' in ads['ad:ads']:
            if type(ads['ad:ads']['ad:ad']) is list:
                for i in ads['ad:ads']['ad:ad']:
                    try:
                        data.append(AD(i['@id'], i['ad:title'],
                                       i['cat:category']['cat:id-name'],
                                       i['ad:price']['types:amount'],
                                       i['ad:view-ad-count'],
                                       dateConverter(i['ad:start-date-time']),
                                       dateConverter(i['ad:end-date-time'])))
                    except KeyError:
                        data.append(AD(i['@id'], i['ad:title'],
                                       i['cat:category']['cat:id-name'],
                                       " ",
                                       i['ad:view-ad-count'],
                                       dateConverter(i['ad:start-date-time']),
                                       dateConverter(i['ad:end-date-time'])))
            elif type(ads['ad:ads']['ad:ad']) is dict:                  # Если одна реклама
                data.append(AD(ads['ad:ads']['ad:ad']['@id'], ads['ad:ads']['ad:ad']['ad:title'],
                               ads['ad:ads']['ad:ad']['cat:category']['cat:id-name'],
                               ads['ad:ads']['ad:ad']['ad:price']['types:amount'],
                               ads['ad:ads']['ad:ad']['ad:view-ad-count'],
                               dateConverter(ads['ad:ads']['ad:ad']['ad:start-date-time']),
                               dateConverter(ads['ad:ads']['ad:ad']['ad:end-date-time'])))
        self.dataOlv.SetObjects(data)

    def setData(self):
        self.dataOlv.SetColumns([
            ColumnDefn("Ad ID", "left", 70, "ad_id", minimumWidth=70),
            ColumnDefn("Title", "left", 128, "title", minimumWidth=128),
            ColumnDefn("Category", "left", 124, "category", minimumWidth=124),
            ColumnDefn("Price", "left", 50, "price", minimumWidth=50),
            ColumnDefn("Views", "left", 45, "views", minimumWidth=45),
            ColumnDefn("Created", "left", 117, "start_date", minimumWidth=117),
            ColumnDefn("Expires", "left", 117, "end_date", minimumWidth=117),
        ])
