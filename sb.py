from lib import *

## LIST APPNAME ##
#android = android
#ios = ios
#android lite = android_lite
#chrome os = chrome
#iosipad = ios_ipad

##LOGIN QR##
client = Boteater(my_app='ios_ipad', server="sg") ## Change server to jp if use japan vps

##LOGIN TOKEN##
#client = Boteater(my_token="", my_app='ios_ipad', server="sg") ## Change server to jp if use japan vps


## NOTE ##
# Lib dan SC belom 100% jadi, SC berantakan karena buru-buru silahkan rapihin dan edit sesuka hati


temporary = {"autorespond" : [],
             "unsend": {},
             "sider_members":[],
             "chatbot_cmd": "",
             "steal": "",
             "action": "",
             "qr": {}}


help_msg = """- Help
- Selfbot
- Media
- Group
- ChatBot
- Setting
- SaveData
- TokenBot
- About"""

selfbot_msg = """- MyMid
- MyPict
- MyPict
- MyCover
- MyContact
- Changepp
- Changevp
- ChangeCover
- Groupbc
- Friendbc
- Tagpm"""

media_msg = """- ScreenshotWeb
- ShorterLink
- Wallpaperhd
- Danbooru
- GoogleImage
- Joox
- AnimeSearch
- AharacterSearch
- Youtubedl"""

group_msg = """- GName
- GPicture
- GLink
- GCreator
- StealContact
- StealPicture
- StealMid
- StealCover
- StealVideo
- Invitecall
- Tagall"""

chatbot_msg = """- Chatbotmode
- Chatbotmode on
- Chatbotmode off

- Viewstickerid
- Textchatbot add
- Textchatbot del
- Textchatbot list
- Imagechatbot add
- Imagechatbot del
- Imagechatbot list
- Videochatbot add
- Videochatbot del
- Videochatbot list
- Audiochatbot add
- Audiochatbot del
- Audiochatbot list
- Stickerchatbot add
- Stickerchatbot del
- Stickerchatbot list"""

setting_msg = """- Autoadd
- Autoadd on
- Autoadd off
- Autoadd text
- Autojoin
- Autojoin on
- Autojoin off
- Autojoin text
- Autolike
- Autolike on
- Autolike off
- Autolike text
- Autorespond
- Autorespond on
- Autorespond off
- Autorespond text
- Autoread
- Autoread on
- Autoread off
- Autorejectgroup
- Autorejectgroup on
- Autorejectgroup off
- Autoblock
- Autoblock on
- Autoblock of
- Autodirectlink
- Autodirectlink on
- Autodirectlink off
- Detectmention
- Detectmention on
- Detectmention off
- Detectmention text
- Detectsticker
- Detectsticker on
- Detectsticker off
- Detectunsend
- Detectunsend on
- Detectunsend off
- Detectpost
- Detectpost on
- Detectpost off
- Welcomerespond
- Welcomerespond on
- Welcomerespond off
- Welcomerespond text
- Leaverespond
- Leaverespond on
- Leaverespond off
- Leaverespond textg
- Sider
- Sider on
- Sider off
- Sider reset
- Sider text"""

token_msg = """- Login Chrome
- Login IosIpad
- Login AndroidLite
- GetToken"""

about_msg = "Selfbot by Boteater Team"

def my_worker(op):
    if op.type == 5:
        if client.temp_data["autoblock"]["status"] == True:
            client.send_message(op.param1, "BLOCKED!")
            client.contact_block(op.param1)
            print("[ OP ] Autoblock")
        elif client.temp_data["autoadd"]["status"] == True:
            client.send_message(op.param1, client.temp_data["autoadd"]["text"])
            client.contact_add(op.param1)
            print("[ OP ] Autoadd")
            
    elif op.type == 13:
        if client.temp_data["autoreject"]["status"] == True:
            client.group_reject(op.param1)
            print("[ OP ] Autoreject")
        elif client.temp_data["autoleave"]["status"] == True:
            if client.my_mid == op.param3:
                client.group_accept(op.param1)
                client.send_message(op.param1, client.temp_data["autoleave"]["text"])  
                client.group_leave(op.param1)
                print("[ OP ] Autoleave")
        elif client.temp_data["autojoin"]["status"] == True:
            if client.my_mid == op.param3:
                client.group_accept(op.param1)
                client.send_message(op.param1, client.temp_data["autojoin"]["text"])
                print("[ OP ] Autojoin")
                
    elif op.type == 15:
        if client.temp_data["leaverespond"]["status"] == True:
            client.send_message(op.param1, client.temp_data["leaverespond"]["text"] )
            print("[ OP ] Leaverespond")
            
    elif op.type == 17:
        if client.temp_data["welcomerespond"]["status"] == True:
            client.send_message(op.param1, client.temp_data["welcomerespond"]["text"] )
            print("[ OP ] Welcomerespond")
            
    elif op.type in [25, 26]:
        msg = op.message
        text = str(msg.text)
        msg_id = msg.id
        receiver = msg.to
        msg.from_ = msg._from
        sender = msg._from
        cmd = text.lower()
        if msg.toType == 0 and sender != client.my_mid: to = sender
        else: to = receiver
        if msg.contentType == 1:
            if client.temp_data["cover"]["status"] == 1 and sender == client.my_mid:
                try:
                    path = client.download_object(msg_id)
                    client.temp_data["cover"]["pp"] = path
                    client.update_cover()
                    client.temp_data["cover"]["status"] = 0
                    client.send_message(to, "Success...")
                except Exception as e:
                    print(e)
                    client.send_message(to, "Error, please resend your image...")
            if client.temp_data["pp"]["status"] == 1 and sender == client.my_mid:
                try:
                    path = client.download_object(msg_id)
                    client.temp_data["pp"]["pp"] = path
                    client.update_profile_picture()
                    client.temp_data["pp"]["status"] = 0
                    client.send_message(to, "Success...")
                except Exception as e:
                    print(e)
                    client.send_message(to, "Error, please resend your image...")
            if client.temp_data["cvp"]["status"] == 1 and sender == client.my_mid:
                try:
                    path = client.download_object(msg_id)
                    client.temp_data["cvp"]["pp"] = path
                    client.temp_data["cvp"]["status"] = 2
                    client.send_message(to, "Send your video...")
                except Exception as e:
                    print(e)
                    client.send_message(to, "Error, please resend your image...")
        if msg.contentType == 2:
            if client.temp_data["cvp"]["status"] == 2 and sender == client.my_mid:
                try:
                    path = client.download_object(msg_id)
                    client.temp_data["cvp"]["vid"] = path
                    client.update_video_profile()
                    client.temp_data["cvp"]["status"] = 0
                    client.send_message(to, "Success...")
                except Exception as e:
                    print(e)
                    client.send_message(to, "Error, please resend your video...")
        
        if cmd == "help":
            client.send_message(to,help_msg)
        if cmd == "selfbot":
            client.send_message(to,selfbot_msg)
        if cmd == "media":
            client.send_message(to,media_msg)
        if cmd == "group":
            client.send_message(to,group_msg)
        if cmd == "chatbot":
            client.send_message(to,chatbot_msg)
        if cmd == "setting":
            client.send_message(to,setting_msg)
        if cmd == "tokenbot":
            client.send_message(to,token_msg)
        if cmd == "about":
            client.send_message(to,about_msg)

        if cmd == "save data":
            client.save_data()
            client.send_message(to,"Success...")


################### SELFBOT ##########################

        if cmd == "tagpm" and sender == client.my_mid:
            if msg.toType != 2:
                for num in range(3):
                    client.send_mention(to, to, "READ ME!")
        if cmd == "mymid":
            me = client.get_contact(sender).mid
            client.send_message(to, me)
        if cmd == "mypict" :
            me = client.get_contact(sender)
            url = client.download_link("http://dl.profile.line-cdn.net/"+me.pictureStatus, ".jpg", True)
            client.post_image(to, url)
            client.send_message(to, url)
        if cmd == "myvideo":
            me = client.get_contact(sender)
            if me.videoProfile != None:
                url = client.download_link("https://obs.line-scdn.net/{}/vp".format(me.pictureStatus), ".mp4", True)
                client.post_image(to, url)
                client.send_message(to, url)
            else:
                client.send_message(to, "Video profile not found...")
        if cmd == "mycover":
            url = client.download_link(client.get_timeline_cover(sender), ".jpg", True)
            client.post_image(to, url)
            client.send_message(to, url)
        if cmd == "mycontact":
            me = client.get_contact(sender).mid
            client.send_contact(to, me)
        if cmd == "changepp" and sender == client.my_mid:
            client.temp_data["pp"]["status"] = 1
            client.send_message(to, "Please send your image...")
        if cmd == "changevp" and sender == client.my_mid:
            client.temp_data["cvp"]["status"] = 1
            client.send_message(to, "Please send your image...")
        if cmd == "changecover" and sender == client.my_mid:
            client.temp_data["cover"]["status"] = 1
            client.send_message(to, "Please send your image...")
        if cmd == "groupbc" and sender == client.my_mid:
            client.temp_data["gbc"]["status"] = 1
            client.send_message(to,"Please send your text...")
        elif client.temp_data["gbc"]["status"] == 1 and sender == client.my_mid:
            if cmd not in ["please send your text...", "abort"]:
                t= threading.Thread(target=client.send_group_bc, args=(to,text,))
                t.daemon = True
                t.start()
                client.temp_data["gbc"]["status"] = 0
        if cmd == "friendbc" and sender == client.my_mid:
            client.temp_data["fbc"]["status"] = 1
            client.send_message(to,"Please send your text...")
        elif client.temp_data["fbc"]["status"] == 1 and sender == client.my_mid:
            if cmd not in ["please send your text...", "abort"]:
                t= threading.Thread(target=client.send_friend_bc, args=(to,text,))
                t.daemon = True
                t.start()
                client.temp_data["fbc"]["status"] = 0


################### SETTING MENU ##########################
        if cmd == "autoadd" and sender == client.my_mid:
            if client.temp_data["autoadd"]["status"] == True:
                status = "on"
            if client.temp_data["autoadd"]["status"] == False:
                status = "off"
            client.send_message(to,"Status: {} \nText:\n{}".format(status, client.temp_data["autoadd"]["text"]))
        if cmd == "autoadd on" and sender == client.my_mid:
            client.temp_data["autoadd"]["status"] = True
            client.send_message(to,"Success...")
        if cmd == "autoadd off" and sender == client.my_mid:
            client.temp_data["autoadd"]["status"] = False
            client.send_message(to,"Success...")
        if cmd == "autoadd text" and sender == client.my_mid:
            client.temp_data["autoadd"]["change"] = 1
            client.send_message(to,"Please send your text...")
        elif client.temp_data["autoadd"]["change"] == 1 and sender == client.my_mid:
            if cmd not in ["please send your text...", "abort"]:
                client.temp_data["autoadd"]["text"] = text
                client.temp_data["autoadd"]["change"] = 0
                client.send_message(to,"Success...")

        if cmd == "autojoin" and sender == client.my_mid:
            if client.temp_data["autojoin"]["status"] == True:
                status = "on"
            if client.temp_data["autojoin"]["status"] == False:
                status = "off"
            client.send_message(to,"Status: {} \nText:\n{}".format(status, client.temp_data["autojoin"]["text"]))
        if cmd == "autojoin on" and sender == client.my_mid:
            client.temp_data["autojoin"]["status"] = True
            client.send_message(to,"Success...")
        if cmd == "autojoin off" and sender == client.my_mid:
            client.temp_data["autojoin"]["status"] = False
            client.send_message(to,"Success...")
        if cmd == "autojoin text" and sender == client.my_mid:
            client.temp_data["autojoin"]["change"] = 1
            client.send_message(to,"Please send your text...")
        elif client.temp_data["autojoin"]["change"] == 1 and sender == client.my_mid:
            if cmd not in ["please send your text...", "abort"]:
                client.temp_data["autojoin"]["text"] = text
                client.temp_data["autojoin"]["change"] = 0
                client.send_message(to,"Success...")

        if cmd == "autoleave" and sender == client.my_mid:
            if client.temp_data["autoleave"]["status"] == True:
                status = "on"
            if client.temp_data["autoleave"]["status"] == False:
                status = "off"
            client.send_message(to,"Status: {} \nText:\n{}".format(status, client.temp_data["autoleave"]["text"]))
        if cmd == "autoleave on" and sender == client.my_mid:
            client.temp_data["autoleave"]["status"] = True
            client.send_message(to,"Success...")
        if cmd == "autoleave off" and sender == client.my_mid:
            client.temp_data["autoleave"]["status"] = False
            client.send_message(to,"Success...")
        if cmd == "autoleave text" and sender == client.my_mid:
            client.temp_data["autoleave"]["change"] = 1
            client.send_message(to,"Please send your text...")
        elif client.temp_data["autoleave"]["change"] == 1 and sender == client.my_mid:
            if cmd not in ["please send your text...", "abort"]:
                client.temp_data["autoleave"]["text"] = text
                client.temp_data["autoleave"]["change"] = 0
                client.send_message(to,"Success...")

        if cmd == "autorespond" and sender == client.my_mid:
            if client.temp_data["autorespond"]["status"] == True:
                status = "on"
            if client.temp_data["autorespond"]["status"] == False:
                status = "off"
            client.send_message(to,"Status: {} \nText:\n{}".format(status, client.temp_data["autorespond"]["text"]))
        if cmd == "autorespond on" and sender == client.my_mid:
            client.temp_data["autorespond"]["status"] = True
            client.send_message(to,"Success...")
        if cmd == "autorespond off" and sender == client.my_mid:
            client.temp_data["autorespond"]["status"] = False
            client.send_message(to,"Success...")
        if cmd == "autorespond text" and sender == client.my_mid:
            client.temp_data["autorespond"]["change"] = 1
            client.send_message(to,"Please send your text...")
        elif client.temp_data["autorespond"]["change"] == 1 and sender == client.my_mid:
            if cmd not in ["please send your text...", "abort"]:
                client.temp_data["autorespond"]["text"] = text
                client.temp_data["autorespond"]["change"] = 0
                client.send_message(to,"Success...")
        if client.temp_data["autorespond"]["status"] == True and sender != client.my_mid:
            if msg.toType != 2:
                if sender not in temporary["autorespond"]:
                    client.send_message(to, client.temp_data["autorespond"]["text"])
                    temporary["autorespond"].append(sender)
                    print("[ OP ] AUTORESPOND")

        if cmd == "welcomerespond" and sender == client.my_mid:
            if client.temp_data["welcomerespond"]["status"] == True:
                status = "on"
            if client.temp_data["welcomerespond"]["status"] == False:
                status = "off"
            client.send_message(to,"Status: {} \nText:\n{}".format(status, client.temp_data["welcomerespond"]["text"]))
        if cmd == "welcomerespond on" and sender == client.my_mid:
            client.temp_data["welcomerespond"]["status"] = True
            client.send_message(to,"Success...")
        if cmd == "welcomerespond off" and sender == client.my_mid:
            client.temp_data["welcomerespond"]["status"] = False
            client.send_message(to,"Success...")
        if cmd == "welcomerespond text" and sender == client.my_mid:
            client.temp_data["welcomerespond"]["change"] = 1
            client.send_message(to,"Please send your text...")
        elif client.temp_data["welcomerespond"]["change"] == 1 and sender == client.my_mid:
            if cmd not in ["please send your text...", "abort"]:
                client.temp_data["welcomerespond"]["text"] = text
                client.temp_data["welcomerespond"]["change"] = 0
                client.send_message(to,"Success...")

        if cmd == "leaverespond" and sender == client.my_mid:
            if client.temp_data["leaverespond"]["status"] == True:
                status = "on"
            if client.temp_data["leaverespond"]["status"] == False:
                status = "off"
            client.send_message(to,"Status: {} \nText:\n{}".format(status, client.temp_data["leaverespond"]["text"]))
        if cmd == "leaverespond on" and sender == client.my_mid:
            client.temp_data["leaverespond"]["status"] = True
            client.send_message(to,"Success...")
        if cmd == "leaverespond off" and sender == client.my_mid:
            client.temp_data["leaverespond"]["status"] = False
            client.send_message(to,"Success...")
        if cmd == "leaverespond text" and sender == client.my_mid:
            client.temp_data["leaverespond"]["change"] = 1
            client.send_message(to,"Please send your text...")
        elif client.temp_data["leaverespond"]["change"] == 1 and sender == client.my_mid:
            if cmd not in ["please send your text...", "abort"]:
                client.temp_data["leaverespond"]["text"] = text
                client.temp_data["leaverespond"]["change"] = 0
                client.send_message(to,"Success...")

        if cmd == "detectmention" and sender == client.my_mid:
            if client.temp_data["detectmention"]["status"] == True:
                status = "on"
            if client.temp_data["detectmention"]["status"] == False:
                status = "off"
            client.send_message(to,"Status: {} \nText:\n{}".format(status, client.temp_data["detectmention"]["text"]))
        if cmd == "detectmention on" and sender == client.my_mid:
            client.temp_data["detectmention"]["status"] = True
            client.send_message(to,"Success...")
        if cmd == "detectmention off" and sender == client.my_mid:
            client.temp_data["detectmention"]["status"] = False
            client.send_message(to,"Success...")
        if cmd == "detectmention text" and sender == client.my_mid:
            client.temp_data["detectmention"]["change"] = 1
            client.send_message(to,"Please send your text...")
        elif client.temp_data["detectmention"]["change"] == 1 and sender == client.my_mid:
            if cmd not in ["please send your text...", "abort"]:
                client.temp_data["detectmention"]["text"] = text
                client.temp_data["detectmention"]["change"] = 0
                client.send_message(to,"Success...")
        if client.temp_data["detectmention"]["status"] == True and sender != client.my_mid:
            if msg.contentType == 0:
                mid_list = client.get_mentiones(msg)
                if client.my_mid in mid_list and mid_list != None:
                    client.send_mention(sender, to, client.temp_data["detectmention"]["text"])
                    print("[ OP ] Detectmention")

        if cmd == "autolike" and sender == client.my_mid:
            if client.temp_data["autolike"]["status"] == True:
                status = "on"
            if client.temp_data["autolike"]["status"] == False:
                status = "off"
            client.send_message(to,"Status: {} \nText:\n{}".format(status, client.temp_data["autolike"]["text"]))
        if cmd == "autolike on" and sender == client.my_mid:
            client.temp_data["autolike"]["status"] = True
            client.send_message(to,"Success...")
        if cmd == "autolike off" and sender == client.my_mid:
            client.temp_data["autolike"]["status"] = False
            client.send_message(to,"Success...")
        if cmd == "autolike text" and sender == client.my_mid:
            client.temp_data["autolike"]["change"] = 1
            client.send_message(to,"Please send your text...")
        elif client.temp_data["autolike"]["change"] == 1 and sender == client.my_mid:
            if cmd not in ["please send your text...", "abort"]:
                client.temp_data["autolike"]["text"] = text
                client.temp_data["autolike"]["change"] = 0
                client.send_message(to,"Success...")
        if msg.contentType == 16 and client.temp_data["autolike"]["status"] == True:
            url = msg.contentMetadata["postEndUrl"]
            client.post_timeline_like(url[25:58], url[66:])
            client.post_timeline_comment(url[25:58], url[66:], client.temp_data["autolike"]["text"])
            client.send_message(to,"Success...")
            print("[ OP ] Autolike")

        if cmd == "autorejectgroup" and sender == client.my_mid:
            if client.temp_data["autorejectgroup"]["status"] == True:
                status = "on"
            if client.temp_data["autorejectgroup"]["status"] == False:
                status = "off"
            client.send_message(to,"Status: "+status)
        if cmd == "autorejectgroup on" and sender == client.my_mid:
            client.temp_data["autorejectgroup"]["status"] = True
            client.send_message(to,"Success...")
        if cmd == "autorejectgroup off" and sender == client.my_mid:
            client.temp_data["autorejectgroup"]["status"] = False
            client.send_message(to,"Success...")

        if cmd == "autoread" and sender == client.my_mid:
            if client.temp_data["autoread"]["status"] == True:
                status = "on"
            if client.temp_data["autoread"]["status"] == False:
                status = "off"
            client.send_message(to,"Status: "+status)
        if cmd == "autoread on" and sender == client.my_mid:
            client.temp_data["autoread"]["status"] = True
            client.send_message(to,"Success...")
        if cmd == "autoread off" and sender == client.my_mid:
            client.temp_data["autoread"]["status"] = False
            client.send_message(to,"Success...")
        if client.temp_data["autoread"]["status"] == True and sender != client.my_mid:
            client.send_message_checked(to, msg.id)
                
        if cmd == "autoblock" and sender == client.my_mid:
            if client.temp_data["autoblock"]["status"] == True:
                status = "on"
            if client.temp_data["autoblock"]["status"] == False:
                status = "off"
            client.send_message(to,"Status: "+status)
        if cmd == "autoblock on" and sender == client.my_mid:
            client.temp_data["autoblock"]["status"] = True
            client.send_message(to,"Success...")
        if cmd == "autoblock off" and sender == client.my_mid:
            client.temp_data["autoblock"]["status"] = False
            client.send_message(to,"Success...")

        if cmd == "detectpost" and sender == client.my_mid:
            if client.temp_data["detectpost"]["status"] == True:
                status = "on"
            if client.temp_data["detectpost"]["status"] == False:
                status = "off"
            client.send_message(to,"Status: "+status)
        if cmd == "detectpost on" and sender == client.my_mid:
            client.temp_data["detectpost"]["status"] = True
            client.send_message(to,"Success...")
        if cmd == "detectpost off" and sender == client.my_mid:
            client.temp_data["detectpost"]["status"] = False
            client.send_message(to,"Success...")
        if msg.contentType == 16 and client.temp_data["detectpost"]["status"] == True:
            a= "Creator : " + msg.contentMetadata["serviceName"] + "\n"
            a+= "Url : " + msg.contentMetadata["postEndUrl"] + "\n"
            if "mediaOid" in msg.contentMetadata:
                for media in ast.literal_eval(msg.contentMetadata["previewMedias"]):
                    part_list = media["mediaOid"].split("|")
                    for part in part_list:
                        if "oid=" in part:
                            oid = part
                        if "sid=" in part:
                            sid = part.replace("sid=", "")
                    if media["mediaType"] == "V":
                        link = client.download_link("https://obs-sg.line-apps.com/myhome/"+sid+"/download.nhn?"+oid, ".mp4", True)
                        client.post_video(to, link)
                        a+= "\nLink video :\n" + link
                    if media["mediaType"] == "I":
                        link = client.download_link("https://obs-sg.line-apps.com/myhome/"+sid+"/download.nhn?"+oid, ".jpg", True)
                        client.post_image(to, link)
                        a+= "\nLink image :\n" + link
            client.send_message(to, a)
            print("[ OP ] Detectpost")

        if cmd == "detectsticker" and sender == client.my_mid:
            if client.temp_data["detectsticker"]["status"] == True:
                status = "on"
            if client.temp_data["detectsticker"]["status"] == False:
                status = "off"
            client.send_message(to,"Status: "+status)
        if cmd == "detectsticker on" and sender == client.my_mid:
            client.temp_data["detectsticker"]["status"] = True
            client.send_message(to,"Success...")
        if cmd == "detectsticker off" and sender == client.my_mid:
            client.temp_data["detectsticker"]["status"] = False
            client.send_message(to,"Success...")
        if client.temp_data["detectsticker"]["status"] == True and sender != client.my_mid:
            if msg.contentType == 7:
                stk_id = msg.contentMetadata["STKID"]
                pkg_id = msg.contentMetadata["STKPKGID"]
                ret_= "STICKER ID: {}\n".format(stk_id)
                ret_+= "STICKER LINK: line://shop/detail/{}".format(pkg_id)
                client.send_message(to, ret_)
                print("[ OP ] Detectsticker")

        if cmd == "sider" and sender == client.my_mid:
            if client.temp_data["sider"]["status"] == True:
                status = "on"
            if client.temp_data["sider"]["status"] == False:
                status = "off"
            client.send_message(to,"Status: {} \nText:\n{}".format(status, client.temp_data["sider"]["text"]))
        if cmd == "sider on" and sender == client.my_mid:
            if msg.toType == 2:
                client.temp_data["sider"]["status"] = True
                client.temp_data["sider"]["groups"].append(to)
                client.send_message(to,"Success...")
        if cmd == "sider off" and sender == client.my_mid:
            client.temp_data["sider"]["status"] = False
            client.temp_data["sider"]["groups"] = []
            client.send_message(to,"Success...")
        if cmd == "sider reset" and sender == client.my_mid:
            temporary['sider_members'] = []
            client.send_message(to,"Success...")
        if cmd == "sider text" and sender == client.my_mid:
            client.temp_data["sider"]["change"] = 1
            client.send_message(to,"Please send your text...")
        elif client.temp_data["sider"]["change"] == 1 and sender == client.my_mid:
            if cmd not in ["please send your text...", "abort"]:
                client.temp_data["sider"]["text"] = text
                client.temp_data["sider"]["change"] = 0
                client.send_message(to,"Success...")
    
        if cmd == "detectunsend" and sender == client.my_mid:
            if client.temp_data["detectunsend"]["status"] == True:
                status = "on"
            if client.temp_data["detectunsend"]["status"] == False:
                status = "off"
            client.send_message(to,"Status: "+status)
        if cmd == "detectunsend on" and sender == client.my_mid:
            client.temp_data["detectunsend"]["status"] = True
            client.send_message(to,"Success...")
        if cmd == "detectunsend off" and sender == client.my_mid:
            client.temp_data["detectunsend"]["status"] = False
            client.send_message(to,"Success...")
        if client.temp_data["detectunsend"]["status"] == True and sender != client.my_mid:
            if msg.contentType == 0:
                temporary["unsend"][msg.id] = {"text":msg.text,"type":"text","from":msg._from}
            if msg.contentType == 1:
                path = client.line_obs+'/talk/m/download.nhn?oid='+msg_id
                link = client.download_link(path, ".jpg", True)
                temporary["unsend"][msg.id] = {"type":"img","from":msg._from,"link":link}
            if msg.contentType == 2:
                path = client.line_obs+'/talk/m/download.nhn?oid='+msg_id
                link = client.download_link(path, ".mp4", True)
                temporary["unsend"][msg.id] = {"type":"video","link":link,"from":msg._from}
            if msg.contentType == 3:
                path = client.line_obs+'/talk/m/download.nhn?oid='+msg_id
                link = client.download_link(path, ".mp3", True)
                temporary["unsend"][msg.id] = {"type":"audio","link":link,"from":msg._from}

        if cmd == "autodirectlink" and sender == client.my_mid:
            if client.temp_data["autodirectlink"]["status"] == True:
                status = "on"
            if client.temp_data["autodirectlink"]["status"] == False:
                status = "off"
            client.send_message(to,"Status: "+status)
        if cmd == "autodirectlink on" and sender == client.my_mid:
            client.temp_data["autodirectlink"]["status"] = True
            client.send_message(to,"Success...")
        if cmd == "autodirectlink off" and sender == client.my_mid:
            client.temp_data["autodirectlink"]["status"] = False
            client.send_message(to,"Success...")
        if client.temp_data["autodirectlink"]["status"] == True:
            if msg.contentType == 1:
                path = client.line_obs+'/talk/m/download.nhn?oid='+msg_id
                link = client.download_link(path, ".jpg", True)
                client.send_message(to,link)
            if msg.contentType == 2:
                path = client.line_obs+'/talk/m/download.nhn?oid='+msg_id
                link = client.download_link(path, ".mp4", True)
                client.send_message(to,link)
            if msg.contentType == 3:
                path = client.line_obs+'/talk/m/download.nhn?oid='+msg_id
                link = client.download_link(path, ".mp3", True)
                client.send_message(to,link)


######################## GROUP MENU #############################
        if cmd == "gpicture" and msg.toType == 2:
            group = client.group_info(to)
            url = client.download_link("http://dl.profile.line-cdn.net/" + group.pictureStatus, ".jpg", True)
            client.post_image(to, url)
            client.send_message(to, url)
        if cmd == "glink" and msg.toType == 2:
            client.send_message(to,"https://line.me/R/ti/g/"+client.group_ticket(to))
        if cmd == "gcreator" and msg.toType == 2:
            group = client.group_info(to)
            client.send_contact(to,group.creator.mid)
        if cmd == "gname" and msg.toType == 2:
            group = client.group_info(to)
            client.send_message(to,group.name)
        if cmd == "stealcontact" and msg.toType == 2:
            temporary["steal"]= "contact"
            client.send_message(to,"Please mention target...")
        if cmd == "stealpicture" and msg.toType == 2:
            temporary["steal"]= "picture"
            client.send_message(to,"Please mention target...")
        if cmd == "stealmid" and msg.toType == 2:
            temporary["steal"]= "mid"
            client.send_message(to,"Please mention target...")
        if cmd == "stealcover" and msg.toType == 2:
            temporary["steal"]= "cover"
            client.send_message(to,"Please mention target...")
        if cmd == "stealvideo" and msg.toType == 2:
            temporary["steal"]= "video"
            client.send_message(to,"Please mention target...")
        if temporary["steal"] != "" and msg.toType == 2:
            if msg.contentType == 0:
                mid_list = client.get_mentiones(msg)
                for mid in mid_list:
                    if temporary["steal"] == "contact":
                        me = client.get_contact(mid).mid
                        client.send_contact(to, me)
                    if temporary["steal"] == "picture":
                        me = client.get_contact(mid)
                        url = client.download_link("http://dl.profile.line-cdn.net/"+me.pictureStatus, ".jpg", True)
                        client.post_image(to, url)
                        client.send_message(to, url)
                    if temporary["steal"] == "mid":
                        me = client.get_contact(mid).mid
                        client.send_message(to, me)
                    if temporary["steal"] == "cover":
                        url = client.download_link(client.get_timeline_cover(mid), ".jpg", True)
                        client.post_image(to, url)
                        client.send_message(to, url)
                    if temporary["steal"] == "video":
                        me = client.get_contact(mid)
                        if me.videoProfile != None:
                            url = client.download_link("https://obs.line-scdn.net/{}/vp".format(me.pictureStatus), ".mp4", True)
                            client.post_image(to, url)
                            client.send_message(to, url)
                        else:
                            client.send_message(to, "Video profile not found...")
                temporary["steal"]= ""
        if cmd == "invitecall" and msg.toType == 2 and sender == client.my_mid:
            status = client.get_group_call(to).online
            if status != False:
                client.invite_group_call(to)
            else:
                client.send_message(to, "Group call not found...")
        if cmd == "tagall" and msg.toType == 2 and sender == client.my_mid:
            client.tagall_member(to)
            
######################## CHATBOT MODE #############################
        

        if cmd == "chatbotmode" and sender == client.my_mid:
            if client.temp_data["chatbotmode"]["status"] == True:
                status = "on"
            if client.temp_data["chatbotmode"]["status"] == False:
                status = "off"
            client.send_message(to,"Status: "+status)
        if cmd == "chatbotmode on" and sender == client.my_mid:
            client.temp_data["chatbotmode"]["status"] = True
            client.send_message(to,"Success...")
        if cmd == "chatbotmode off" and sender == client.my_mid:
            client.temp_data["chatbotmode"]["status"] = False
            client.send_message(to,"Success...")
            
        if cmd == "textchatbot add" and sender == client.my_mid:
            client.temp_data["chatbotmode"]["change"] = 10
            client.send_message(to,"Please send your command text...")
        elif client.temp_data["chatbotmode"]["change"] == 10  and sender == client.my_mid:
            if cmd not in ["please send your command text...", "abort"]:
                client.temp_data["chatbotmode"]["data"]["text"][cmd]= ""
                client.temp_data["chatbotmode"]["change"] = 20
                temporary["chatbot_cmd"] = cmd
                client.send_message(receiver,"Please send your reply text...")
        elif client.temp_data["chatbotmode"]["change"] == 20  and sender == client.my_mid:
            if cmd not in ["please send your reply text...", "abort"]:
                client.temp_data["chatbotmode"]["data"]["text"][temporary["chatbot_cmd"]]= cmd
                client.temp_data["chatbotmode"]["change"] = 0
                client.send_message(to,"Success...")
        if cmd == "textchatbot del" and sender == client.my_mid:
            client.temp_data["chatbotmode"]["change"] = 30
            client.send_message(to,"Please send your command text...")
        elif client.temp_data["chatbotmode"]["change"] == 30  and sender == client.my_mid:
            if cmd not in ["please send your command text...", "abort"]:
                if cmd in client.temp_data["chatbotmode"]["data"]["text"]:
                    del client.temp_data["chatbotmode"]["data"]["text"][cmd]
                    client.temp_data["chatbotmode"]["change"] = 0
                    client.send_message(to,"Success...")
                else:
                    client.temp_data["chatbotmode"]["change"] = 0
                    client.send_message(to,"Command not found...")
        if cmd == "textchatbot list" and sender == client.my_mid:
            if client.temp_data["chatbotmode"]["data"]["text"] != {}:
                data = "\n"
                for command in client.temp_data["chatbotmode"]["data"]["text"]:
                    data+= "\n- " + command
                client.send_message(to,data.replace("\n\n", ""))

        if cmd == "imagechatbot add" and sender == client.my_mid:
            client.temp_data["chatbotmode"]["change"] = 11
            client.send_message(to,"Please send your command text...")
        elif client.temp_data["chatbotmode"]["change"] == 11  and sender == client.my_mid:
            if cmd not in ["please send your command text...", "abort"]:
                client.temp_data["chatbotmode"]["data"]["img"][cmd]= ""
                client.temp_data["chatbotmode"]["change"] = 21
                temporary["chatbot_cmd"] = cmd
                client.send_message(receiver,"Please send your reply image...")
        elif client.temp_data["chatbotmode"]["change"] == 21  and sender == client.my_mid:
            if cmd not in ["please send your reply image...", "abort"]:
                if msg.contentType == 1:
                    path = client.line_obs+'/talk/m/download.nhn?oid='+msg_id
                    client.send_message(to,"Please wait...")
                    link = client.download_link_gdrive(path, ".jpg", True)
                    client.temp_data["chatbotmode"]["data"]["img"][temporary["chatbot_cmd"]]= link
                    client.temp_data["chatbotmode"]["change"] = 0
                    client.send_message(to,"Success...")
        if cmd == "imagechatbot del" and sender == client.my_mid:
            client.temp_data["chatbotmode"]["change"] = 31
            client.send_message(to,"Please send your command text...")
        elif client.temp_data["chatbotmode"]["change"] == 31  and sender == client.my_mid:
            if cmd not in ["please send your command text...", "abort"]:
                if cmd in client.temp_data["chatbotmode"]["data"]["img"]:
                    del client.temp_data["chatbotmode"]["data"]["img"][cmd]
                    client.temp_data["chatbotmode"]["change"] = 0
                    client.send_message(to,"Success...")
                else:
                    client.temp_data["chatbotmode"]["change"] = 0
                    client.send_message(to,"Command not found...")
        if cmd == "imagechatbot list" and sender == client.my_mid:
            if client.temp_data["chatbotmode"]["data"]["img"] != {}:
                data = "\n"
                for command in client.temp_data["chatbotmode"]["data"]["img"]:
                    data+= "\n- " + command
                client.send_message(to,data.replace("\n\n", ""))

        if cmd == "videochatbot add" and sender == client.my_mid:
            client.temp_data["chatbotmode"]["change"] = 12
            client.send_message(to,"Please send your command text...")
        elif client.temp_data["chatbotmode"]["change"] == 12  and sender == client.my_mid:
            if cmd not in ["please send your command text...", "abort"]:
                client.temp_data["chatbotmode"]["data"]["video"][cmd]= ""
                client.temp_data["chatbotmode"]["change"] = 22
                temporary["chatbot_cmd"] = cmd
                client.send_message(receiver,"Please send your reply video...")
        elif client.temp_data["chatbotmode"]["change"] == 22  and sender == client.my_mid:
            if cmd not in ["please send your reply video...", "abort"]:
                if msg.contentType == 2:
                    client.send_message(to,"Please wait...")
                    path = client.line_obs+'/talk/m/download.nhn?oid='+msg_id
                    link = client.download_link_gdrive(path, ".mp4", True)
                    client.temp_data["chatbotmode"]["data"]["video"][temporary["chatbot_cmd"]]= link
                    client.temp_data["chatbotmode"]["change"] = 0
                    client.send_message(to,"Success...")
        if cmd == "videochatbot del" and sender == client.my_mid:
            client.temp_data["chatbotmode"]["change"] = 32
            client.send_message(to,"Please send your command text...")
        elif client.temp_data["chatbotmode"]["change"] == 32  and sender == client.my_mid:
            if cmd not in ["please send your command text...", "abort"]:
                if cmd in client.temp_data["chatbotmode"]["data"]["video"]:
                    del client.temp_data["chatbotmode"]["data"]["video"][cmd]
                    client.temp_data["chatbotmode"]["change"] = 0
                    client.send_message(to,"Success...")
                else:
                    client.temp_data["chatbotmode"]["change"] = 0
                    client.send_message(to,"Command not found...")
        if cmd == "videochatbot list" and sender == client.my_mid:
            if client.temp_data["chatbotmode"]["data"]["video"] != {}:
                data = "\n"
                for command in client.temp_data["chatbotmode"]["data"]["video"]:
                    data+= "\n- " + command
                client.send_message(to,data.replace("\n\n", ""))

        if cmd == "audiochatbot add" and sender == client.my_mid:
            client.temp_data["chatbotmode"]["change"] = 13
            client.send_message(to,"Please send your command text...")
        elif client.temp_data["chatbotmode"]["change"] == 13  and sender == client.my_mid:
            if cmd not in ["please send your command text...", "abort"]:
                client.temp_data["chatbotmode"]["data"]["audio"][cmd]= ""
                client.temp_data["chatbotmode"]["change"] = 23
                temporary["chatbot_cmd"] = cmd
                client.send_message(receiver,"Please send your reply audio...")
        elif client.temp_data["chatbotmode"]["change"] == 23  and sender == client.my_mid:
            if cmd not in ["please send your reply audio...", "abort"]:
                if msg.contentType == 3:
                    client.send_message(to,"Please wait...")
                    path = client.line_obs+'/talk/m/download.nhn?oid='+msg_id
                    link = client.download_link_gdrive(path, ".mp3", True)
                    client.temp_data["chatbotmode"]["data"]["audio"][temporary["chatbot_cmd"]]= link
                    client.temp_data["chatbotmode"]["change"] = 0
                    client.send_message(to,"Success...")
        if cmd == "audiochatbot del" and sender == client.my_mid:
            client.temp_data["chatbotmode"]["change"] = 33
            client.send_message(to,"Please send your command text...")
        elif client.temp_data["chatbotmode"]["change"] == 33  and sender == client.my_mid:
            if cmd not in ["please send your command text...", "abort"]:
                if cmd in client.temp_data["chatbotmode"]["data"]["audio"]:
                    del client.temp_data["chatbotmode"]["data"]["audio"][cmd]
                    client.temp_data["chatbotmode"]["change"] = 0
                    client.send_message(to,"Success...")
                else:
                    client.temp_data["chatbotmode"]["change"] = 0
                    client.send_message(to,"Command not found...")
        if cmd == "audiochatbot list" and sender == client.my_mid:
            if client.temp_data["chatbotmode"]["data"]["audio"] != {}:
                data = "\n"
                for command in client.temp_data["chatbotmode"]["data"]["audio"]:
                    data+= "\n- " + command
                client.send_message(to,data.replace("\n\n", ""))

        if cmd == "stickerchatbot add" and sender == client.my_mid:
            client.temp_data["chatbotmode"]["change"] = 14
            client.send_message(to,"Please send your command text...")
        elif client.temp_data["chatbotmode"]["change"] == 14  and sender == client.my_mid:
            if cmd not in ["please send your command text...", "abort"]:
                client.temp_data["chatbotmode"]["data"]["sticker"][cmd]= ""
                client.temp_data["chatbotmode"]["change"] = 24
                temporary["chatbot_cmd"] = cmd
                client.send_message(receiver,"Please send your sticker id...")
        elif client.temp_data["chatbotmode"]["change"] == 24  and sender == client.my_mid:
            if cmd not in ["please send your sticker id...", "abort"]:
                link = client.gen_sticker_link(cmd)
                if link != None:
                    client.temp_data["chatbotmode"]["data"]["sticker"][temporary["chatbot_cmd"]]= link
                    client.temp_data["chatbotmode"]["change"] = 0
                    client.send_message(to,"Success...")
                else:
                    client.temp_data["chatbotmode"]["change"] = 0
                    client.send_message(to,"Wrong sticker id...")
        if cmd == "stickerchatbot del" and sender == client.my_mid:
            client.temp_data["chatbotmode"]["change"] = 34
            client.send_message(to,"Please send your command text...")
        elif client.temp_data["chatbotmode"]["change"] == 34  and sender == client.my_mid:
            if cmd not in ["please send your command text...", "abort"]:
                if cmd in client.temp_data["chatbotmode"]["data"]["sticker"]:
                    del client.temp_data["chatbotmode"]["data"]["sticker"][cmd]
                    client.temp_data["chatbotmode"]["change"] = 0
                    client.send_message(to,"Success...")
                else:
                    client.temp_data["chatbotmode"]["change"] = 0
                    client.send_message(to,"Command not found...")
        if cmd == "stickerchatbot list" and sender == client.my_mid:
            if client.temp_data["chatbotmode"]["data"]["sticker"] != {}:
                data = "\n"
                for command in client.temp_data["chatbotmode"]["data"]["sticker"]:
                    data+= "\n- " + command
                client.send_message(to,data.replace("\n\n", ""))

        if cmd == "viewstickerid" and sender == client.my_mid:
            client.temp_data["chatbotmode"]["change"] = 15
            client.send_message(to,"Please send your sticker link...")
        elif client.temp_data["chatbotmode"]["change"] == 15  and sender == client.my_mid:
            if cmd not in ["please send your sticker link....", "abort"]:
                if "https://line.me/S/sticker/" in text:
                    for link in text.split("\n"):
                        if "https://line.me/S/sticker/" in link:
                            if "?" in link:
                                sticker_id = link.split("?")[0].split("/")[-1]
                            else:
                                sticker_id = link.split("/")[-1]
                    sticker_list= client.get_sticker_info(sticker_id).productDetail.productProperty.stickerProperty.stickerIds
                    print(sticker_list)
                    for sticker in sticker_list:
                        client.post_sticker(to,client.gen_sticker_link(sticker))
                        client.send_message(to,"Sticker ID: "+str(sticker))
                    client.temp_data["chatbotmode"]["change"] = 0
                
        if client.temp_data["chatbotmode"]["status"] == True:
            if cmd in client.temp_data["chatbotmode"]["data"]["text"]:
                client.send_message(to,client.temp_data["chatbotmode"]["data"]["text"][cmd])
            if cmd in client.temp_data["chatbotmode"]["data"]["img"]:
                client.post_image(to,client.temp_data["chatbotmode"]["data"]["img"][cmd])
            if cmd in client.temp_data["chatbotmode"]["data"]["video"]:
                client.post_video(to,client.temp_data["chatbotmode"]["data"]["video"][cmd])
            if cmd in client.temp_data["chatbotmode"]["data"]["audio"]:
                client.post_audio(to,client.temp_data["chatbotmode"]["data"]["audio"][cmd])
            if cmd in client.temp_data["chatbotmode"]["data"]["sticker"]:
                client.post_sticker(to,client.temp_data["chatbotmode"]["data"]["sticker"][cmd])

######################## MEDIA #############################

        if cmd == "screenshotweb":
            temporary["action"] = "ssweb"
            client.send_message(to,"Please send your link...")

        elif cmd == "shorterlink":
            temporary["action"] = "shorter"
            client.send_message(to,"Please send your link...")

        elif cmd == "wallpaperhd":
            temporary["action"] = "wallp"
            client.send_message(to,"Please send your search query...")

        elif cmd == "danbooru":
            temporary["action"] = "danb"
            client.send_message(to,"Please send your page number...")

        elif cmd == "googleimage":
            temporary["action"] = "google"
            client.send_message(to,"Please send your search query...")

        elif cmd == "joox":
            temporary["action"] = "joox"
            client.send_message(to,"Please send your search query...")

        elif cmd == "animesearch":
            temporary["action"] = "malanime"
            client.send_message(to,"Please send your search query...")

        elif cmd == "charactersearch":
            temporary["action"] = "malchar"
            client.send_message(to,"Please send your search query...")

        elif cmd == "youtubedl":
            temporary["action"] = "ytdl"
            client.send_message(to,"Please send your search query...")
            
        elif temporary["action"] != "":
            if text not in ["Please send your search query...", "Please send your page number...", "Please send your link..."]:
                if temporary["action"] == "ssweb":
                    try:
                        client.screenshot_web(to,text)
                        temporary["action"] = ""
                    except Exception as e:
                        client.send_message(to,"Error...")
                        temporary["action"] = ""
                        print(e)
                if temporary["action"] == "shorter":
                    try:
                        client.shorter_link(to,text)
                        temporary["action"] = ""
                    except Exception as e:
                        client.send_message(to,"Error...")
                        temporary["action"] = ""
                        print(e)
                if temporary["action"] == "wallp":
                    try:
                        client.wallpaper_hd(to,text)
                        temporary["action"] = ""
                    except Exception as e:
                        client.send_message(to,"Error...")
                        temporary["action"] = ""
                        print(e)
                if temporary["action"] == "danb":
                    try:
                        client.danbooru(to,text)
                        temporary["action"] = ""
                    except Exception as e:
                        client.send_message(to,"Error...")
                        temporary["action"] = ""
                        print(e)
                if temporary["action"] == "google":
                    try:
                        client.google_image(to,text)
                        temporary["action"] = ""
                    except Exception as e:
                        client.send_message(to,"Error...")
                        temporary["action"] = ""
                        print(e)
                if temporary["action"] == "joox":
                    try:
                        client.joox(to,text)
                        temporary["action"] = ""
                    except Exception as e:
                        client.send_message(to,"Error...")
                        temporary["action"] = ""
                        print(e)
                if temporary["action"] == "malanime":
                    try:
                        client.mal_anime(to,text)
                        temporary["action"] = ""
                    except Exception as e:
                        client.send_message(to,"Error...")
                        temporary["action"] = ""
                        print(e)
                if temporary["action"] == "malchar":
                    try:
                        client.mal_character(to,text)
                        temporary["action"] = ""
                    except Exception as e:
                        client.send_message(to,"Error...")
                        temporary["action"] = ""
                        print(e)
                if temporary["action"] == "ytdl":
                    try:
                        client.yt_dl_local(to,search=text)
                        temporary["action"] = ""
                    except Exception as e:
                        client.send_message(to,"Error...")
                        temporary["action"] = ""
                        print(e)

######################## TOKENBOT #############################

        if cmd.startswith("login "):
            header = cmd.split(" ")[1]
            if header in ["chrome", "androidlite", "iosipad"]:
                if header == "androidlite":
                    header = "android_lite"
                if header == "iosipad":
                    header = "ios_ipad"
                result = json.loads(requests.get(client.boteater_api+"/qr?header="+header).text)
                temporary["qr"][sender] = result["result"]["callback"]
                client.send_message(to,"- QRLink: \n"+result["result"]["qr_link"]+"\n\n- Login IP: \n"+result["result"]["login_ip"])

        elif cmd == "gettoken":
            if sender in temporary["qr"]:
                result = json.loads(requests.get(temporary["qr"][sender]).text)
                if result["status"] == 200:
                    client.send_message(to,result["result"])

    if op.type == 55:
        if client.temp_data["sider"]["status"] == True:
            if op.param1 in client.temp_data["sider"]["groups"]:
                if op.param2 not in temporary['sider_members']:
                    client.send_mention(op.param2, op.param1, client.temp_data["sider"]["text"])
                    temporary['sider_members'].append(op.param2)
                    
    if op.type == 65:
        if client.temp_data["detectunsend"]["status"] == True:
            msg_id = op.param2
            to = op.param1
            if msg_id in temporary["unsend"]:
                client.send_mention(temporary["unsend"][msg_id]["from"], to, "Unsend detected...")
                if temporary["unsend"][msg_id]["type"] == "text":
                    client.send_message(to,temporary["unsend"][msg_id]["text"])
                elif temporary["unsend"][msg_id]["type"] == "video":
                    client.post_video(to,temporary["unsend"][msg_id]["link"])
                    client.send_message(to,temporary["unsend"][msg_id]["link"])
                elif temporary["unsend"][msg_id]["type"] == "img":
                    client.post_image(to,temporary["unsend"][msg_id]["link"])
                    client.send_message(to,temporary["unsend"][msg_id]["text"])
                elif temporary["unsend"][msg_id]["type"] == "audio":
                    client.post_audio(to,temporary["unsend"][msg_id]["link"])
                    client.send_message(to,temporary["unsend"][msg_id]["text"])
                print("[ OP ] Detectunsend")
def run():
    while True:
        try:
            ops = client.pool.fetchOps(client.last_op, 5, client.last_op, client.last_op)
            for op in ops:
                if op.revision > client.last_op:
                    client.last_op = max(op.revision, client.last_op)
                    my_worker(op)
                    ## Jangan threading disini :) ##
                    ## Don't threading in here :) ##
        except Exception as e:
            print(e)

if __name__ == "__main__":
    run()
