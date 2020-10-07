import json
import sys
import wx
import wx.richtext as rt
import socketio
import datetime

from DH import DH

import sympy
import random
import logging
import os




if not os.path.isdir('log'):
    os.mkdir('log')
filename = datetime.datetime.now()
filename = filename.strftime("%Y%m%d%H%M%S")
filename = 'log\\Client_' + filename + '.log'

logger = logging.getLogger('client_logger')
logger.setLevel(logging.INFO)
fh = logging.FileHandler(filename)
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
logger.addHandler(fh)

sio = socketio.Client(logger=False)
class Messenger(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='CryptoChat Application')
        self.InitUI()
        self.Centre()

        self.makeMenuBar()

        self.CreateStatusBar()
        self.log("Write your usser name and Server Address, then Click to connect...")

        self.Show()

        self.connected = False
        self.sessionOpen = False

        
        self.dh = None
        self.users = {}


    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbUser = wx.BoxSizer(wx.HORIZONTAL)
        self.lblUser = wx.StaticText(panel, label='User Name')
        self.txtUser = wx.TextCtrl(panel)
        hbUser.Add(self.lblUser, flag=wx.RIGHT, border=8)
        hbUser.Add(self.txtUser, proportion=1)
        vbox.Add(hbUser, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        vbox.Add((-1, 5))

        hbServer = wx.BoxSizer(wx.HORIZONTAL)
        self.lblSever = wx.StaticText(panel, label='Server Address')
        self.txtServer = wx.TextCtrl(panel,value='http://localhost:5000')
        self.btnConnect = wx.Button(panel, label='Connect')
        hbServer.Add(self.lblSever, flag=wx.RIGHT, border=8)
        hbServer.Add(self.txtServer, proportion=1)
        hbServer.Add(self.btnConnect, proportion=0.5)
        vbox.Add(hbServer, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        vbox.Add((-1, 10))

        hbUsers = wx.BoxSizer(wx.HORIZONTAL)
        self.lblUsers = wx.StaticText(panel, label='Connected users')
        self.cmbUsers = wx.ComboBox(panel)
        self.btnChatWith = wx.Button(panel, label='Chat...')
        hbUsers.Add(self.lblUsers, flag=wx.RIGHT, border=8)
        hbUsers.Add(self.cmbUsers, proportion=1)
        hbUsers.Add(self.btnChatWith, proportion=0.5)
        vbox.Add(hbUsers, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        vbox.Add((-1, 10))

        hbChat = wx.BoxSizer(wx.HORIZONTAL)
        lblChat = wx.StaticText(panel, label='Chat Box')
        hbChat.Add(lblChat)
        vbox.Add(hbChat, flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add((-1, 10))

        hbChatBx = wx.BoxSizer(wx.HORIZONTAL)
        self.txtChat = rt.RichTextCtrl(panel, style=wx.VSCROLL|wx.HSCROLL|wx.TE_READONLY)
        hbChatBx.Add(self.txtChat, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbChatBx, proportion=1, flag=wx.EXPAND|wx.RIGHT|wx.EXPAND,border=10)

        hbMsg = wx.BoxSizer(wx.HORIZONTAL)
        self.txtMsg = wx.TextCtrl(panel)
        self.btnSendMsg = wx.Button(panel,label='Send')
        hbMsg.Add(self.txtMsg, proportion=1)
        hbMsg.Add(self.btnSendMsg, proportion=0.3)
        vbox.Add(hbMsg, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,border=10)
        vbox.Add((-1, 10))

        panel.SetSizer(vbox)

        self.cmbUsers.Enabled = False
        self.btnChatWith.Enabled = False

        self.btnConnect.Bind(wx.EVT_BUTTON, self.OnConnect)
        self.btnChatWith.Bind(wx.EVT_BUTTON, self.OnChatWith)
        self.btnSendMsg.Bind(wx.EVT_BUTTON,self.OnSendMsg)

        self.initControls()
        

    def log(self,msg):
        self.SetStatusText(msg)
        logger.info(msg)

    def initControls(self):
        self.cmbUsers.Enabled = False
        self.btnChatWith.Enabled = False
        self.txtChat.Enabled = False
        self.txtMsg.Enabled = False
        self.btnSendMsg.Enabled = False

    def makeMenuBar(self):
        fileMenu = wx.Menu()
        exitItem = fileMenu.Append(wx.ID_EXIT)
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)



    def create_public_keys(self):
        self.log(f'Creating public keys...')
        key_1 = sympy.randprime(2**17,2**18)
        key_2 = DH.primRoots(key_1)[0]
        self.log(f'Public Keys created {key_1} - {key_2}')
        return(key_1,key_2)

    
    def create_shared_key(self,key_1,key_2):
        self.log('Creating Shared Key...')
        self.dh = DH(key_2,key_1)
        self.dh.create_shared_key()
        self.log('Shared Key Created!')
        return self.dh.shared_key

    
    def create_full_key(self,shared_key):
        self.log(f'Creating Full key with shared key {shared_key}...')
        self.dh.create_full_key(shared_key)
    
    def next_key(self):
        self.log("Generating new private key...")
        self.dh.next_key()
        self.log('Creating Shared Key...')
        self.log(f'Shared Key Created! {self.dh.private_key} - {self.dh.shared_key}')
        return self.dh.shared_key
     
    def OnConnect(self, event):
        if not self.connected: #Connect to web server
            self.log("Connecting to server...")
            #try:
            self.btnConnect.LabelText = 'Disconnect'
            user = self.txtUser.Value
            server = self.txtServer.Value
            sio.connect(server)
            self.log(f'Connected to server {server} with user {user} session id:{sio.sid}')
            sio.emit('login', {'session':sio.sid,'user':user})
            self.cmbUsers.Clear()
            self.connected = True
            # except:
            # err = sys.exc_info()[0]
            # log(f"System error! {err}")
        else: #Disconnect
            self.log("Disconecting from server...")
            self.btnConnect.LabelText = 'Connect'
            sio.emit('logout', {'session':sio.sid,'user':self.txtUser.Value})
            self.connected = False
            self.log("Disconnected")
            sio.disconnect()
        self.txtUser.Enabled = not self.connected
        self.txtServer.Enabled = not self.connected
        self.initControls()

    def OnChatWith(self,event):
        user = self.cmbUsers.GetStringSelection()
        key_1, key_2 = self.create_public_keys()
        requester_shared_key = self.create_shared_key(key_1,key_2)
        data = {
            'requester':self.txtUser.Value, 
            'requester_sid': sio.sid,
            'requester_shared_key':requester_shared_key,
            'user': user,
            'user_sid':self.users[user],
            'user_shared_key':None,
            'key_1' : key_1,
            'key_2' : key_2}
        self.log(f'Sending chat request to user {user}...')
        sio.emit('chatwith', data)

    

    def OnSendMsg(self,event):
        msg = self.txtMsg.Value
        now = datetime.datetime.now()
        nowStr = now.strftime("%Y-%m-%d %H:%M:%S")
        if len(msg):
            msg = f'{nowStr} \t {self.txtUser.Value}: {self.txtMsg.Value}'
            self.txtChat.BeginTextColour((255, 0, 0))
            self.txtChat.WriteText(msg)
            self.txtChat.EndTextColour()
            self.txtChat.Newline()
            self.log('Encrypting message...')
            enc = self.dh.encrypt(msg)
            user = self.cmbUsers.GetStringSelection()
            s_id = self.users[user]
            data = {
                'requester':self.txtUser.Value, 
                'requester_sid': sio.sid,
                'requester_shared_key':self.dh.shared_key,
                'user': user,
                'user_sid':s_id,
                'user_shared_key':None,
                'enc':enc}
            self.log(f'Sending Encrypted  message...{enc}')
            sio.emit('sendmessage',data)
            self.txtMsg.Clear()
          
    def decryptMessage(self,enc):
        msg = self.dh.decrypt(enc)
        self.log('Decrypting message...')
        self.txtChat.BeginTextColour((0, 150, 100))
        self.txtChat.WriteText(msg)
        self.txtChat.EndTextColour()
        self.txtChat.Newline()
        self.log('Message decrypted!')

    def OnExit(self, event):
            """Close the frame, terminating the application."""
            self.Close(True)

    def OnAbout(self, event):
        """Display an About Dialog"""
        message = '''
            Author: Asahi Cantu Moreno
            Application Description: This project emulates the diffe-hallman encryption mechanism to securely send messages from the web
            from one user to another.
            Created for the assignment of  Network Security and Cryptography for the University of Stavanger
        '''
        wx.MessageBox(message,"About Client Application",wx.OK|wx.ICON_INFORMATION)


  
@sio.event
def connect():
    print("Socket Connected")

@sio.event
def connect_error():
    print("Socket Connection failed!")

@sio.event
def disconnect():
    print("Socket")

@sio.on("users")
def users(data):
    print(f'receiving new users {data}')
    if data:
        for key in data:
            user = data[key]
            if user != frame.txtUser.Value:
                if user not in frame.cmbUsers.Strings:
                    frame.users[user] = key
                    frame.cmbUsers.Append(user)
                    print(f'User {user} connected!')
    if not frame.cmbUsers.IsListEmpty():
        frame.cmbUsers.SetSelection(0)
        frame.cmbUsers.Enabled = True
        frame.btnChatWith.Enabled = True
        frame.SetStatusText('New Users Received')
    else:
        frame.cmbUsers.Enabled = False
        frame.btnChatWith.Enabled = False
        frame.SetStatusText('Waiting for users...')


@sio.on("beginchat")
def beginchat(data):
    requester = data['requester']
    user = data['user']
    key_1= data['key_1']
    key_2 = data['key_2']
    msg  =f'{requester} wants to start chat session with {user}... '  
    frame.log(msg)
    if frame.connected and not frame.sessionOpen:
        result = wx.MessageDialog(frame, msg, caption='Click Yes to Accept',
              style=wx.YES_NO|wx.CENTRE, pos=wx.DefaultPosition).ShowModal()
        if result == wx.ID_YES:
            frame.log('Linking messaging...')
            location = frame.cmbUsers.FindString(requester)
            frame.cmbUsers.SetSelection(location)
            frame.cmbUsers.Enabled = False
            frame.btnChatWith.Enabled = False
            shared_key = frame.create_shared_key(key_1,key_2)
            data['user_shared_key'] = shared_key
            sio.emit('onhandshake',data)

@sio.on('handshake')
def handshake(data):
    requester_sid = data['requester_sid']
    requester_shared_key = data['requester_shared_key']
    user_sid = data['user_sid']
    user_shared_key = data['user_shared_key']
    shared_key = None
    if sio.sid == requester_sid:
        shared_key = user_shared_key 
    elif sio.sid == user_sid:
        shared_key = requester_shared_key
    else:
        frame.log('Invalid handshake, could not establish communication')
    
    if shared_key:
        frame.create_full_key(shared_key)
        frame.btnChatWith.Enabled = False
        frame.txtMsg.Enabled = True
        frame.btnSendMsg.Enabled = True
        frame.txtChat.Enabled = True
        frame.log(f'Full key created! {frame.dh.full_key}, connection established')
        
@sio.on("sendmessage")
def sendmessage(data):
    enc = data['enc']
    print(f'Message received {enc} decryptinc')
    frame.SetStatusText(f'Message received, decrypting...')
    frame.decryptMessage(enc)
    user = frame.cmbUsers.GetStringSelection()
    s_id = frame.users[user]
    data = {
            'requester':frame.txtUser.Value, 
            'requester_sid': sio.sid,
            'requester_shared_key':frame.next_key(),
            'user': user,
            'user_sid':s_id,
            'user_shared_key':None}
    sio.emit('onnextkey',data)


@sio.on("nextkey")
def nextkey(data):
    frame.log('Generating next shared key')
    data['user_shared_key'] = frame.next_key()
    sio.emit('onhandshake',data)



if __name__ == '__main__':
    app = wx.App()
    frame = Messenger()
    frame.SetSize(wx.Size(600,500))
    frame.log('Client Application has started')
    app.MainLoop()
    
    
