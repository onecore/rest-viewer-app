# -*- encoding: utf8 -*-
from _ast import Str
__author__ = ['CSECSD']
__language__ = ['Python', 'Kivy', 'C']
__version__ = ['0.2']
__developer__ = ['CoreSEC Software Development', 'Geek Talks']
__compat__ = ['cross-platform']
__devel__ = ['Maria Shiela Magistrado',
             'Tony Birol',
             'Jay Paterno',
             'Arel Jao Guina',
             'Kyle Paguio',
             'Mark Anthony Pequeras'
             ]

from License import * # < License is under PSF from GPL (Commercial License)
from time import clock
from kivy.uix.rst import RstDocument
from kivy.app import App
from kivy.utils import platform
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.graphics import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.layout import Layout
from kivy.uix.bubble import Bubble
from kivy.parser import parse_color
from kivy.base import runTouchApp
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput
from kivy.properties import (StringProperty, ObjectProperty,
                             NumericProperty, ListProperty)
from kivy.uix.codeinput import CodeInput
from kivy.uix.popup import Popup
import urllib
import urllib2

# content Size target: 480,800

if platform() == 'android':
    REVMOB_APP_ID = '5106bea78e5bd71500000098'
elif platform() == 'ios':
    REVMOB_APP_ID = '5106be9d0639b41100000052'
else:
    REVMOB_APP_ID = 'unknown platform for RevMob'
Target = [480,800]

Builder.load_string("""

# RST Viewer Python Style Sheety  :)
<rootEngine>:

    Image:
        source: "coreEngine/Images/drawing.png"

        RstDocument:
            id: core
            size_hint: None,None
            source: root.sourceView()
            height: 510
            width: 460
            pos: 10,115

        Button:
            id: sourceView
            background_down: "coreEngine/Images/CoreTex_ViewScript.png"
            background_normal: "coreEngine/Images/CoreTex_ViewScript.png"
            size_hint: None,None
            height: 85
            width: 84
            pos: 370,705
            on_press: root.sourceView()


        Image:
            source: "coreEngine/Images/CoreTex_Background.png"
            size_hint: None,None
            size: 480,58
            pos: 0,637

        Button:
            id: parserView
            background_down: "coreEngine/Images/CoreTex_Build.png"
            background_normal: "coreEngine/Images/CoreTex_Build.png"
            size_hint: None,None
            height: 85
            width: 84
            pos: 279,705
            on_press: root.compileView()


        Button:
            id: questionMarkButton
            background_down: "coreEngine/Images/HelpButton.png"
            background_normal: "coreEngine/Images/HelpButton.png"
            size_hint: None,None
            height: 64
            width: 64
            pos: 235,19
            on_press: root.helpView()


        Button:
            id: Delete
            size_hint: None,None
            background_normal: "coreEngine/Images/CoreTex_Clear.png"
            background_down: "coreEngine/Images/CoreTex_Clear.png"
            size: 90,40
            pos: 185,645
            on_press: root.clear()

        Button:
            id: Load
            background_normal: "coreEngine/Images/CoreTex_Load.png"
            background_down: "coreEngine/Images/CoreTex_Load.png"
            size_hint: None,None
            size: 90,40
            pos: 3,645
            on_press: root.Load()

        Button:
            id: loadFromWeb
            background_normal: "coreEngine/Images/CoreTex_Web.png"
            background_down: "coreEngine/Images/CoreTex_Web.png"
            size_hint: None,None
            size: 90,40
            pos: 94,645
            on_press: root.loadRemotely()

        Button:
            id: createNew
            size_hint: None,None
            size: 58,58
            pos: 285,638
            background_normal: "coreEngine/Images/newfile.png"
            background_down: "coreEngine/Images/newfile.png"
            on_press: root.createNew()

        Button:
            id: WebShare
            size: 48,48
            pos: 336,26
            size_hint: None,None
            background_normal: "coreEngine/Images/websh.png"
            background_down: "coreEngine/Images/websh.png"
            on_press: root.webShareAPI()



        Button:
            id: EmailMe
            size: 64,64
            pos: 394,19

            size_hint: None,None
            background_normal: "coreEngine/Images/email.png"
            background_down: "coreEngine/Images/email.png"
            on_press: root.SendEmail()

        Button:
            id: Tweakle
            size: 64,64
            pos: 130,19
            size_hint: None,None
            background_normal: "coreEngine/Images/tweak.png"
            background_down: "coreEngine/Images/tweak.png"
            on_press: root.TweakView()

        Button:
            id: Settings
            size: 64,64
            pos: 13,19
            size_hint: None,None
            background_normal: "coreEngine/Images/setting.png"
            background_down: "coreEngine/Images/setting.png"
            on_press: root.SettingView()

        # Logo bro
        Image:
            source: "coreEngine/Images/CoreTex_Logo.png"
            pos: -23,713
            size: 196,64
        # Bottom BG

""")

class rootEngine(FloatLayout):


#    def mp(self,mn):
#        # {
#        def __init__(**kwargs):
#            super(mp,self).__init__(self)
#            
#        def lambida(object):
#            lambda mn, mn * mn // .2 ## get power
#            
#        def squary(object):
#            lambda mn: mn ** mn / 2
        # } 
        
# just some dictionaries below        

    def __init__(self,**kwargs):
        """
        Main Engine
        """
        super(rootEngine,self).__init__(**kwargs)
        self.rstView(name="coreEngine/Rst/index.rst")
        self.Config = None
        self.savedSource = "" # None Immutable
        self.current = "" # None Immutable
        _savedInts = open("coreEngine/Rst/saved.ctex","r")
        self.saved = 0
        self.savedMake = 0
        self.iterSaved = 0
        self.toMakeSaved = None
        self.coreTexMimes = {
            "index":"coreEngine/Rst/index.rst",
            "code":"coreEngine/Rst/code.rst",
            "help":"coreEngine/Rst/help.rst",
            "new":"coreEngine/Rst/new.rst",
            "web":"coreEngine/Rst/web.rst",
            "cache":"coreEngine/Rst/cache.rst",
            "saved":"coreEngine/Rst/saved.ctex",
            "cleared":"coreEngine/Rst/cleared.rst",
            } # .rst = ReST File ,  .ctex = CoreTEX File


    def getLatestSaved(self):
        _openFile = open(self.coreTexMimes["saved"],"r") # .ctex is the Mimetype for the CoreTEX File
        _contents = _openFile.read()
        _openFile.close()
        #if _openFile.close():
        eval_isDangerous = eval(_contents)
        for Ints in eval_isDangerous:
            Latest =  int(max(eval_isDangerous)) # Latest Enumeration
            Iterable = list(eval_isDangerous) # List / Array
            break
        self.saved = Latest
        self.iterSaved = Iterable 


    def reloadCode(self):
        """
        reload Compiler
        """
        self.rstView(name=str(self.current))


    def loadRemotely(self):
        """
        Load Remotely (web)
        """
        toDownload = ""
        main = Popup(title="Load .RST Document Remotely",
                     size_hint=(.9,.4))
        layer = FloatLayout()
        cancelBtn = Button(text="Cancel",
                           size_hint=(.4,.12),
                           pos_hint={"x":.10,"y":0.04}) # 100% - hint (divide if needed)
        openBtn = Button(text="Load",
                           size_hint=(.4,.12),
                           pos_hint={"x":.50,"y":0.04})                         
        desc = "Make sure to load a raw RST Source"
        descWid = Label(text=str(desc),size_hint=(.4,.4),
                                pos_hint={"x":0.30,
                                "y":0.50})
        url_box = TextInput(text="http://",
                            size_hint=(.8,0.15),
                            pos_hint={"x":0.10,"y":0.24},
                            multiline = False)


        def closePop(object):
            
            """
            Close Popups
            INNER FUNC
            """
            main.dismiss()
            
        
        def LabelError(object):
            """
            Exception Message
            INNER FUNC
            """
            main.title="Please Recheck the URL"
        
        
        def web_Get(object):
            """
            get rst source via Web
            INNER FUNC
            """
            _string_url = str(url_box.text)
            
            def check_Rst(filer):
                from pygments.lexers.text import RstLexer #

                file_to_check = str(filer)
                return RstLexer.analyse_text(file_to_check)
                
            try:
                webEmu = urllib.urlopen(_string_url)
                response = webEmu.read()
                #if "http://" not in _string_url:
                #    print "error"
                #    return False
                #elif "https://" not in _string_url:
                #    print "error"
                #    return False
                    #_fixed_url = "https://{web}".format(web=_string_url) #SSL Protocol
                #else:
                #    _fixed_url = "{web}".format(web=_string_url) # clean yet with error i guess.

            except Exception:
                main.title = "Error, Please recheck the Url! or your Connection"
                url_box.text="http://"
                return False
            
            main.title = "Source has been Loaded to Editor Successfully"
            web_cache_file = open("coreEngine/Rst/web.rst","w")
            web_cache_file.write(str(response))
            web_cache_file.close()      
            if len(str(response)) <= 3:
                main.title="File from Web has Unsufficient bytes"
                
            else:
                self.current = self.coreTexMimes["web"]
                
                try:
                    self.rstView(name="coreEngine/Rst/web.rst")
                    #self.ids.core.source = "coreEngine/Rst/web.rst"
                except:
                    main.title = "File Not Loaded: Parsing Returns Error"
            main.dismiss()
                    
        cancelBtn.bind(on_release=closePop)                 
        openBtn.bind(on_press=web_Get)  
                              
        layer.add_widget(url_box)
        layer.add_widget(cancelBtn)
        layer.add_widget(openBtn)
        layer.add_widget(descWid)
        main.add_widget(layer)
        main.open()

    def Loader_NoErr(self, ctexSaved,fixedPath):
        import os
        with open(ctexSaved) as f:
            Source_read = f.read()
        self.current = self.coreTexMimes["saved"]
        self.rstView(name=str(fixedPath))


    def Load(self):
        """
        Load from the Disk
        Button > Load()
        """
        from functools import partial
        from kivy.uix import filechooser
        from kivy.uix.filechooser import FileChooserListView, FileChooserIconView
        main = ModalView(size_hint=(.8,.8)) # everything on this Modal is 80%
        BL = BoxLayout(portrait="vertical")
        
        FLV = FileChooserListView(path="coreEngine/Saved",)
        
        

        def cTexloader(instance):
            Selected = FLV.selection
            Selected_Attr = Selected
            LStoString = str(Selected_Attr[0])
            self.Loader_NoErr(ctexSaved=LStoString,fixedPath=LStoString)
            
            
            


        

        Load_Btn = Button(text="Load this File")
        Load_Btn.bind(on_press=cTexloader)
        main.add_widget(BL)
        BL.add_widget(FLV) 
        BL.add_widget(Load_Btn)       

        main.open()


    def createNew(self):
        """
        Create New File [Button]
        """
        try:
            savedLists = open("coreEngine/Rst/saved.ctex","r") # Saved Pattern file ....
            lastSaved = savedLists.read()
            size_val = eval(str(lastSaved))
            to_create = len(size_val)
            cache_Files = {"file":"{name}.rst".format(name=int(to_create) + 1),
                         "number":str(int(to_create) + 1)}
            self.ids.core.source="coreEngine/Rst/new.rst"
        except:
            self.ids.core.text="Error Occured processing New File!"
        finally:
            self.currentCache_file = cache_Files["file"]
            self.currentCache_int = cache_Files["number"]
            savedLists.close()
            self.current = "new.rst"

    def clear(self):
        from coreEngine.Libraries import createlib
        """
        Clear Editor func
        """
        if len(self.ids.core.text) > 1:
            self.current = self.coreTexMimes["cleared"]
            self.ids.core.source = "coreEngine/Rst/cleared.rst"
        else:
            pass
        


    def webShareAPI(self):
        """
        using pastebin-API to send and save on web!
        """
        pass
    

    def SendEmail(self):
        """
        send the source to any Email func
        """
        self.getLatestSaved()


    def helpView(self):
        """
        Show Help/Guides modal (show when help button pressed)
        """
        widgets = FloatLayout(size_hint=(None,None),
                         size=(300,300),
                         background_color=parse_color("#FF9933"),)
        sizer = NumericProperty(30)
        main = ModalView(title_color=parse_color("#FF9933"),
                     title_size=(25),
                     seperator_height=("9dp"),
                     separator_color=parse_color("#FF9933"),
                     #background_color=parse_color("#FF9933"),
                     size_hint=(None,None),
                     size=(400,620),
                     content = Image(source="coreEngine/Images/about.png"),
                             )
        

        
        white_bar = Image(source="coreEngine/Images/whitebar.png",
                          pos=(123,123),
                          size=(400,400))
        
        logo = Image(source="coreEngine/Images/about.png")
        
        main.add_widget(logo, 1)
        main.open()

    
    
    
##  FUNCTION




 

    def rstView(self,name=""):
        """
        Return Code into Parser
        """
        self.ids.core.source = name  #simple as dat.  
    
    
    
##  FUNCTION




        

    def TweakView(self):
        """
        Tweak Settings / Color etc.
        """
        pass
    
    
    
    
##  FUNCTION




    def SettingView(self):
        """
        Settings View / Options whatsoever
        """
        self.closeChecker()



    def compileView(self):
        """
        once the source has been sent from compiler, it will show the parsed version of the source
        """
        try: 
            self.ids.core.source = self.current
        except Exception:
            print "error"


    def sourceView(self):
        """
        lemme show your the source!
        """
        
        def subFunction_Divisor(object):
            lambda xy: xy ** xy // 3  # get the Power and return Divided in Floor Division

        self.main = ModalView(size_hint=(None,None),
                         size=(420,750))

        self.modalMain = FloatLayout()
        self.saveButton = Button(text="Save",size_hint=(None,None),size=(100,40),pos=(320,30))
        self.cancelButton = Button(text="Cancel",size_hint=(None,None),size=(100,40),pos=(60,30))
        self.head = Label(text="CoreTEX Source",size_hint=(None,None),pos=(60,700))
        self.box = CodeInput(size_hint=(None,None),size=(390,650),pos=(45,77),use_bubble=True)#editor in modal view#
        self.box.text = str(self.ids.core.text)


        def cancelAll(instance):
            """
            self.main close trigger
            """
            self.main.dismiss()
            

        def saveAll(instance):
            """
            Load Cache.rst (Cache File from the coreEngine)
            everything will be saved as Cache... (Editable on Options)
            """
            cur = self.ids.core.source
            if "index.rst" in str(cur):
                self.main.dismiss() #dont ever let the editor edit this file :P
                return False

            if "new" in self.current:
                self.getLatestSaved() # Run to get Eval code
                # load file 
                _file = open(self.coreTexMimes["saved"],"rw+")
                _read = _file.read()
                # load file
                curCache = int(self.saved)
                cache_value = lambda ctex: ctex + 1;
                cache_final = cache_value(curCache)
                return False
            
            box_strings = str(self.box.text)
            current = self.current # add this on the Current working file
            cache_file_open = open("coreEngine/Rst/cache.rst","w")
            cache_file_writeNow = cache_file_open.write(box_strings)
            cache_file_open.close()
                
            if cache_file_open.closed:
                pass # Do everything here
            
            else:
                cancelAll()
                
                
        # lambda gbox: 
        self.saveButton.bind(on_press=saveAll)
        self.cancelButton.bind(on_press=cancelAll)
        self.modalMain.add_widget(self.box)
        self.modalMain.add_widget(self.head)
        self.modalMain.add_widget(self.cancelButton)
        self.modalMain.add_widget(self.saveButton)
        self.main.add_widget(self.modalMain)
        #main.add_widget(cancelButton)
        self.main.open()


    def AnimateStart(self):
        """
        Animator :) Useless.
        """
        from kivy.animation import Animation

        LOL = Animation(x=50, size=(200, 200), t='in_quad')
        LOL.start(self.ids.startme), self.rstView()


    def closeChecker(self): # call me when needed :3
        """
        Func to do
        If file is Opened, make it close,
        Else file is Closed, do Nothing.
        """
        # constants hack hahaha
        check_1,check_2,check_3,check_4,check_5,check_6,check_7 = 1,1,1,1,1,1,1
        if bool(check_1):
            try:
                file_1 = open(self.coreTexMimes["index"],"r")
            except IOError:
                check_1 = 0
        if bool(check_2):
            try:
                file_2 = open(self.coreTexMimes["code"],"r")
            except IOError:
                check_2 = 0
        if bool(check_3):
            try:
                file_3 = open(self.coreTexMimes["help"],"r")
            except IOError:
                check_3 = 0
        if bool(check_4):
            try:
                file_4 = open(self.coreTexMimes["new"],"r")
            except IOError:
                check_4 = 0        
        if bool(check_5):
            try:
                file_5 = open(self.coreTexMimes["web"],"r")
            except IOError:
                check_5 = 0
        if bool(check_6):
            try:
                file_6 = open(self.coreTexMimes["cache"],"r")
            except IOError:
                check_6 = 0
        if bool(check_7):
            try:
                file_7 = open(self.coreTexMimes["saved"],"r")
            except IOError:
                check_7 = 0
        check_1,check_2,check_3,check_4,check_5,check_6,check_7 = 1,1,1,1,1,1,1


                
if __name__ == "__main__":
    runTouchApp(rootEngine()) # Run CoreTex Loops.
