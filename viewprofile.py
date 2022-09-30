import wx
from kijiji_api import KijijiApi
from dialogs import row_builder
from ObjectListView import ObjectListView, ColumnDefn


class ViewDialog(wx.Dialog):

    # def __init__(self, selected_row, title="Profile"):
    def __init__(self, selected_row):
        """Constructor"""
        super().__init__(None, title="%s's profile" % selected_row.email, size=wx.Size(640, 480))
        # super().__init__(None, title=title)

        self.k_api = KijijiApi()
        self.user_id, self.token = self.k_api.login(selected_row.email, selected_row.kijiji_pass)
        self.profile_info = self.k_api.get_profile(self.user_id, self.token)
        print(self.profile_info)
        #self.ads = self.k_api.get_ad(self.user_id, self.token)
        #print(self.ads)

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
        t_var = profileid_lbl.GetSize()[0] + self.profileid.GetSize()[0] + registration_date_lbl.GetSize()[0] + self.registration_date.GetSize()[0]
        spacer = self.GetSize()[0] - t_var
        profileid_sizer.AddSpacer(spacer - int(t_var/5))    # 60 отступы
        profileid_sizer.Add(registration_date_lbl, 0, wx.ALL, 5)
        profileid_sizer.Add(self.registration_date, 0, wx.ALL, 5)
        main_sizer.Add(profileid_sizer, 0, wx.ALL)

        name_lbl = wx.StaticText(self, label="Name :")
        name_lbl.SetFont(font)
        self.name = wx.StaticText(self, label=self.profile_info['user:user-profile']['user:user-display-name'])
        self.name.SetFont(font_2)
        name_sizer = row_builder([name_lbl, self.name])

        activeads_num_lbl = wx.StaticText(self, label="Active ADs :")
        activeads_num_lbl.SetFont(font)
        self.ads_num = wx.StaticText(self, label=self.profile_info['user:user-profile']['user:user-active-ad-count'])
        self.ads_num.SetFont(font_2)
        name_sizer.AddSpacer((spacer - (name_lbl.GetSize()[0] + self.name.GetSize()[0])) + self.registration_date.GetSize()[0])  # 64 отступы
        name_sizer.Add(activeads_num_lbl, 0, wx.ALL, 5)
        name_sizer.Add(self.ads_num, 0, wx.ALL, 5)
        main_sizer.Add(name_sizer, 0, wx.ALL)

        email_lbl = wx.StaticText(self, label="Email :")
        email_lbl.SetFont(font)
        self.email = wx.StaticText(self, label=self.profile_info['user:user-profile']['user:user-email'])
        self.email.SetFont(font_2)
        main_sizer.Add(row_builder([email_lbl, self.email]), 0, wx.ALL)

        self.dataOlv = ObjectListView(self, wx.ID_ANY, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.setData()

        post_ad_btn = wx.Button(self, label="Post Ad")
        post_ad_btn.Bind(wx.EVT_BUTTON, self.on_register)
        btn_sizer.Add(post_ad_btn, 0, wx.ALL, 5)

        delete_ad_btn = wx.Button(self, label="Delete Ad")
        delete_ad_btn.Bind(wx.EVT_BUTTON, self.on_register)
        btn_sizer.Add(delete_ad_btn, 0, wx.ALL, 5)

        main_sizer.Add(self.dataOlv, 1, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(btn_sizer, 0, wx.CENTER)
        self.SetSizer(main_sizer)

    def on_register(self):
        """
        Edit a record in the database
        """
        # author_dict, book_dict = self.get_data()
        # combo_dict = {**author_dict, **book_dict}
        # # controller.edit_record(self.session, self.selected_row.id, combo_dict)
        # show_message("Book Edited Successfully!", "Success",
        #              wx.ICON_INFORMATION)
        self.Close()

    def setData(self):
        self.dataOlv.SetColumns([
            ColumnDefn("Ad ID", "left", -1, "email"),
            ColumnDefn("Title", "left", -1, "kijiji_pass"),
            ColumnDefn("Category", "left", -1, "email_pass"),
            ColumnDefn("Price", "left", -1, "imap_pass"),
            ColumnDefn("Views", "left", -1, "forwarding"),
        ])
