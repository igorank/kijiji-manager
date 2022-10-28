import wx
import helper
import configparser
from proxy import Proxy
from viewprofile import ViewDialog
from registerdialog import RegisterDialog
from ObjectListView import ObjectListView, ColumnDefn
from gsheet import GSheet


class Account(object):

    def __init__(self, user_id, email, kijiji_pass, email_pass, imap_pass, forwarding, token):
        self.user_id = user_id
        self.email = email
        self.kijiji_pass = kijiji_pass
        self.email_pass = email_pass
        self.imap_pass = imap_pass
        self.forwarding = forwarding
        self.token = token


class MainPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.proxy = Proxy(username=self.config['PROXY']['USERNAME'], password=self.config['PROXY']['PASSWORD'],
                           host=self.config['PROXY']['HOST'], port=self.config['PROXY']['PORT'],
                           url=self.config['PROXY']['URL'])

        gsheets = GSheet(self.config['GOOGLE_SHEETS']['KEY'], self.config['GOOGLE_SHEETS']['KEYFILE_NAME'])
        self.main_sheet = gsheets.get_main_worksheet(int(self.config['GOOGLE_SHEETS']['GID']))
        list_of_hashes = self.main_sheet.get_all_records()
        self.data = []
        for i in list_of_hashes:
            self.data.append(Account(i['User ID'], i['Email'], i['Kijiji password'], i['Email Password'], i['IMAP password'],
                                     i['Forwarding to'], i['Token']))

        self.dataOlv = ObjectListView(self, wx.ID_ANY, sortable=False, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.dataOlv.SetEmptyListMsg("No Profiles")
        self.setData()
        # Allow the cell values to be edited when double/single-clicked
        # self.dataOlv.cellEditMode = ObjectListView.CELLEDIT_SINGLECLICK
        # self.dataOlv.cellEditMode = ObjectListView.CELLEDIT_DOUBLECLICK

        registerBtn = wx.Button(self, wx.ID_ANY, "Register")
        registerBtn.Bind(wx.EVT_BUTTON, self.registerControl)
        btn_sizer.Add(registerBtn, 0, wx.ALL, 5)

        deleteBtn = wx.Button(self, wx.ID_ANY, "Delete")
        deleteBtn.Bind(wx.EVT_BUTTON, self.deleteControl)
        btn_sizer.Add(deleteBtn, 0, wx.ALL, 5)

        updateBtn = wx.Button(self, wx.ID_ANY, "Update")
        updateBtn.Bind(wx.EVT_BUTTON, self.updateControl)
        btn_sizer.Add(updateBtn, 0, wx.ALL, 5)

        ViewBtn = wx.Button(self, wx.ID_ANY, "View Profile")
        ViewBtn.Bind(wx.EVT_BUTTON, self.view_record)
        btn_sizer.Add(ViewBtn, 0, wx.ALL, 5)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.dataOlv, 1, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(btn_sizer, 0, wx.CENTER)
        self.SetSizer(mainSizer)

    def registerControl(self, event):
        with RegisterDialog(self.config, self.proxy, self.main_sheet) as dlg:
            dlg.ShowModal()
            self.updateSpreadsheet()

    def deleteControl(self, event):
        selected_row = self.dataOlv.GetSelectedObject()
        if not selected_row:
            helper.show_message('Please select one profile from the list!', 'Error')
            return

        cell = self.main_sheet.find(selected_row.email)
        self.main_sheet.delete_row(cell.row)

        # Update
        self.updateSpreadsheet()

        helper.show_message("Profile has been deleted!", 'Deleted', wx.ICON_INFORMATION)

    def view_record(self, event):
        selected_row = self.dataOlv.GetSelectedObject()
        if not selected_row:
            helper.show_message('Please select one profile from the list!', 'Error')
            return

        try:
            with ViewDialog(selected_row, self.config, self.proxy) as dlg:
                dlg.ShowModal()
        except Exception as e:
            helper.show_message(str(e), 'Error')

    def updateControl(self, event):
        self.updateSpreadsheet()
        helper.show_message("The table has been updated!", 'Updated', wx.ICON_INFORMATION)

    def updateSpreadsheet(self):
        list_of_hashes = self.main_sheet.get_all_records()

        self.data = []
        for i in list_of_hashes:
            self.data.append(
                Account(i['User ID'], i['Email'], i['Kijiji password'], i['Email Password'], i['IMAP password'],
                        i['Forwarding to'], i['Token']))

        self.dataOlv.SetObjects(self.data)

    def setData(self):
        self.dataOlv.SetColumns([
            ColumnDefn("User ID", "left", 70, "user_id", minimumWidth=70),
            ColumnDefn("Email", "left", 213, "email", minimumWidth=213),
            ColumnDefn("Kijiji password", "left", 89, "kijiji_pass", minimumWidth=89),
            ColumnDefn("Email Password", "left", 116, "email_pass", minimumWidth=116),
            ColumnDefn("IMAP password", "left", 88, "imap_pass", minimumWidth=88),
            ColumnDefn("Forwarding to", "left", 211, "forwarding", minimumWidth=211),
            ColumnDefn("Token", "left", 1783, "token", minimumWidth=1783)
        ])

        self.dataOlv.SetObjects(self.data)
