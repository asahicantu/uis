import wx
class ConnectDialog(wx.Dialog):

    def __init__(self, *args, **kw):
        super(ConnectDialog, self).__init__(*args, **kw)



        self.SetSize((400, 200))
        self.SetTitle("Change Color Depth")

        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        sb = wx.StaticBox(pnl, label='Connection Settings')
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)

        txtConnect      = self.CreateInputBoxFor(pnl,sbs,"User Name:","Alice")
        txtServer       = self.CreateInputBoxFor(pnl,sbs,"Server:","127.0.0.1")


        pnl.SetSizer(sbs)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Close')
        hbox2.Add(okButton)
        hbox2.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(pnl, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hbox2, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.SetSizer(vbox)

        okButton.Bind(wx.EVT_BUTTON, self.OnClose)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)


    def CreateInputBoxFor(self,panel,boxSizer,label,value):
        ctrl = wx.TextCtrl(panel,value = value)
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(wx.StaticText(panel,label=label))
        box.Add(ctrl, flag=wx.LEFT, border=5)
        boxSizer.Add(box)
        return ctrl

    def OnClose(self, e):

        self.Destroy()
