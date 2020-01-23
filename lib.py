from thrift.transport.THttpClient import THttpClient
from thrift.protocol.TCompactProtocol import TCompactProtocol
from boteater_lib import BoteaterService
from boteater_lib.ttypes import *
import json, re, ast, traceback, datetime, threading, copy, os, base64, requests, tempfile, time, shutil, urllib, string, random
from random import randint


class Boteater():
    def __init__(self, my_app, my_token=None, server=None):
        if server == "japan":
            self.line_server = "https://ga2.line.naver.jp" #Japan
        elif server == "sg":
            self.line_server = "https://ga2s.line.naver.jp" #Indo/Singapure
        else:
            self.line_server = "https://gd2.line.naver.jp" #Japan
        self.line_obs = "https://obs-sg.line-apps.com"
        self.boteater_api = "https://api.boteater.us"
        self.liff_url = "https://api.line.me/message/v3/share"
        self.sticker_link= "https://stickershop.line-scdn.net/stickershop/v1/sticker/{}/iPhone/sticker@2x.png"
        self.sticker_link_animation= "https://stickershop.line-scdn.net/stickershop/v1/sticker/{}/iPhone/sticker_animation@2x.png"
        self.data_headers = self.read_json("headers.json")
        if my_app in self.data_headers:
            self.headers = self.data_headers[my_app]
            if my_token != None:
                self.headers["X-Line-Access"] = my_token
            else:
                del self.headers["X-Line-Access"]
                self.headers["X-Line-Access"] = self.qr_login(self.headers)
        else:
            raise Exception('APP not found!!!')

        ### CONNECT TO POOL ###
        transport = THttpClient(self.line_server + '/P4')
        transport.setCustomHeaders(self.headers)
        transport.open()
        protocol = TCompactProtocol(transport)
        self.pool = BoteaterService.Client(protocol)
        
        ### CONNECT TO TALK ###
        transport = THttpClient(self.line_server + '/api/v4/TalkService.do')
        transport.setCustomHeaders(self.headers)
        transport.open()
        protocol = TCompactProtocol(transport)
        self.talk = BoteaterService.Client(protocol)

        ### CONNECT TO CHANNEL ###
        transport = THttpClient(self.line_server + '/CH4')
        transport.setCustomHeaders(self.headers)
        transport.open()
        protocol = TCompactProtocol(transport)
        self.channel = BoteaterService.Client(protocol)

        ### CONNECT TO CALL ###
        transport = THttpClient(self.line_server + '/V4')
        transport.setCustomHeaders(self.headers)
        transport.open()
        protocol = TCompactProtocol(transport)
        self.call = BoteaterService.Client(protocol)

        ### CONNECT TO SHOP ###
        transport = THttpClient(self.line_server + '/TSHOP4')
        transport.setCustomHeaders(self.headers)
        transport.open()
        protocol = TCompactProtocol(transport)
        self.shop = BoteaterService.Client(protocol)

        ### CONNECT TO LIFF ###
        transport = THttpClient(self.line_server + '/LIFF1')
        transport.setCustomHeaders(self.headers)
        transport.open()
        protocol = TCompactProtocol(transport)
        self.liff = BoteaterService.Client(protocol)

        self.profile_data = self.talk.getProfile()
        self.my_mid = self.profile_data.mid
        self.last_op = self.pool.getLastOpRevision()
        self.issue_liff_view()
        self.tl_channel = self.issue_channel_token('1341209950').channelAccessToken
        self.tl_headers = copy.deepcopy(self.headers)
        self.tl_headers["X-Line-ChannelToken"] = self.tl_channel
        self.tl_headers["X-Line-Mid"] = self.my_mid
        self.tl_headers["X-Line-AcceptLanguage"] = 'en'
        self.tl_headers["X-Requested-With"] = 'jp.naver.line.android.LineApplication'
        self.tl_headers["Content-Type"] = 'application/json'
        
        self.my_OBStoken = self.gen_obs_token()
        print("[ Login ] Display Name: " + self.profile_data.displayName)
        self.temp_data = self.read_json("tmp.json")

    def qr_login(self, headers):
        sys_name = "BE-Team"
        transport = THttpClient(self.line_server + '/api/v4/TalkService.do')
        transport.setCustomHeaders(headers)
        protocol = TCompactProtocol(transport)
        talk = BoteaterService.Client(protocol)
        qr_code = talk.getAuthQrcode(True, sys_name, True)
        transport.close()
        print(qr_code.callbackUrl)
        headers["X-Line-Access"] = qr_code.verifier
        transport = THttpClient(self.line_server + '/api/v4p/rs')
        transport.setCustomHeaders(headers)
        protocol = TCompactProtocol(transport)
        auth = BoteaterService.Client(protocol)
        get_access = json.loads(requests.get(self.line_server + '/Q', headers=headers).text)
        login_request = LoginRequestStruct()
        login_request.type = 1
        login_request.identityProvider = 1
        login_request.keepLoggedIn = True
        login_request.accessLocation = "8.8.8.8"
        login_request.systemName = sys_name
        login_request.verifier = get_access['result']['verifier']
        login_request.e2eeVersion = 0
        result = auth.loginZ(login_request)
        transport.close()
        return result.authToken

    def read_json(self, filename):
        with open(filename) as f:
            try:
                data = json.loads(f)
            except:
                data = json.load(f)
            f.close()
        return data

    def write_json(self, filename, data):
        with open(filename, "w") as f:
            json.dump(data,f,indent=4,sort_keys=True)
            f.close()
        return
    
    def save_data(self):
        write_json("tmp.json", self.temp_data)

    def download_link(self, url, ext, headers=False):
        data = {"url": url,
                "ext": ext}
        if headers == False:
            r = requests.post(self.boteater_api + "/local_drive", data=data)
            return json.loads(r.text)["result"]
        if headers == True:
            r = requests.post(self.boteater_api + "/local_drive", data=data, headers=self.headers)
            return json.loads(r.text)["result"]

    def download_link_gdrive(self, url, ext, headers=False):
        data = {"url": url,
                "ext": ext}
        if headers == False:
            r = requests.post(self.boteater_api + "/google_drive", data=data)
            return json.loads(r.text)["result"]
        if headers == True:
            r = requests.post(self.boteater_api + "/google_drive", data=data, headers=self.headers)
            return json.loads(r.text)["result"]

    def download_object(self, messageId):
        path = self.gen_tmp_file()
        r = requests.get(self.line_obs+"/talk/m/download.nhn?oid="+messageId, headers=self.headers, stream=True)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
                f.close()
            return path
        else:
            raise Exception('[ Error ] Download object')

    def issue_channel_token(self, channel_id):
        return self.channel.issueChannelToken(channel_id)

    def issue_liff_view(self):
        data = {
            'on': [
                'P',
                'CM'
                ],
            'off': []
            }
        headers = copy.deepcopy(self.headers)
        headers["Content-Type"] = "application/json"
        headers["X-Line-ChannelId"] = "1586794970"
        requests.post('https://access.line.me/dialog/api/permissions', json=data, headers=headers)
        return

    def get_timeline_user(self, mid):
        return json.loads(requests.get(self.line_server+"/mh/api/v1/userpopup/getDetail.json?userMid="+mid, headers=self.tl_headers).text)

    def get_timeline_cover(self, mid):
        home = self.get_timeline_user(mid)
        return self.line_obs+'/myhome/c/download.nhn?userid='+mid+'&oid='+home['result']['objectId']

    def get_timeline_url(self, Hid):
        link = self.line_server+"/mh/api/v51/web/getUrl.json?homeId="+Hid
        return json.loads(requests.get(link, headers=self.tl_headers).text)["result"]["homeWebUrl"]

    def get_timeline_post(self, Hid):
        link = self.line_server+"/mh/api/v51/post/list.json?postLimit=999&commentLimit=999&likeLimit=999&homeId="+Hid
        return json.loads(requests.get(link, headers=self.tl_headers).text)

    def get_mentiones(self, msg):
        if 'MENTION' in msg.contentMetadata.keys()!= None:
            mention = ast.literal_eval(msg.contentMetadata['MENTION'])
            mentionees = mention['MENTIONEES']
            mid_list = []
            for mention in mentionees:
                if mention["M"] not in mid_list:
                    mid_list.append(mention["M"])
            return mid_list
        else:
            return None
        
    def get_contact(self, mid):
        return self.talk.getContact(mid)

    def get_joined_group(self):
        return self.talk.getGroupIdsJoined()

    def get_group_call(self, gmid):
        return self.call.getGroupCall(gmid)

    def get_all_contact(self):
        return self.talk.getAllContactIds()

    def get_sticker_info(self, Sid):
        data = GetProductRequestStruct()
        data.productType = 1
        data.productId = Sid
        data.carrierCode = "510012"
        data.saveBrowsingHistory = False
        return self.shop.getProductV2(request=data)

    def gen_obs_token(self):
        return self.talk.acquireEncryptedAccessToken(1)

    def gen_tmp_file(self):
        name, path = 'tmpfile-%s-%i.bin' % (int(time.time()), randint(0, 9)), tempfile.gettempdir()
        return os.path.join(path, name)

    def gen_obs_param(self, params):
        return base64.b64encode(json.dumps(params).encode('utf-8'))

    def gen_object_id(self):
        random.seed = (os.urandom(1024))
        return ''.join(random.choice("abcdef1234567890") for i in range(32))

    def gen_random(self, count):
        random.seed = (os.urandom(1024))
        return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(count))

    def gen_sticker_link(self, Sid):
        patern = copy.deepcopy(self.sticker_link_animation)
        link = patern.format(Sid)
        r = requests.get(link)
        if r.status_code == 200:
            return link
        patern = copy.deepcopy(self.sticker_link)
        link = patern.format(Sid)
        r = requests.get(link)
        if r.status_code == 200:
            return link
        return None

    def contact_block(self, mid):
        return self.talk.blockContact(0, mid)

    def contact_add(self, mid):
        return self.talk.findAndAddContactsByMid(0, mid, 0, '')

    def group_info(self, gmid):
        return self.talk.getGroupWithoutMembers(gmid)

    def group_info_full(self, gmid):
        return self.talk.getGroup(gmid)

    def group_ticket(self, gmid):
        return self.talk.reissueGroupTicket(gmid)
    
    def group_kick(gmid, list_target):
        return self.talk.kickoutFromGroup(0, gmid, list_target)

    def group_create(gname, list_target):
        return self.talk.createGroupV2(0, gname, list_target)

    def group_cancel(gmid, list_target):
        return self.talk.cancelGroupInvitation(0, gmid, list_target)

    def group_reject(gmid):
        return self.talk.rejectGroupInvitation(0, gmid)

    def group_accept(gmid):
        return self.talk.acceptGroupInvitation(0, gmid)

    def group_leave(gmid):
        return self.talk.leaveGroup(0, gmid)

    def send_friend_bc(self, to, text):
        friends = self.get_all_contact()
        num= 0
        for friend in friends:
            try:
                self.send_message(friend, "{}".format(str(text)))
                num+=1
                time.sleep(0.3)
            except:
                pass
        return self.send_message(to,"Success broadcast {} friends".format(num))

    def send_group_bc(self, to, text):
        groups = self.get_joined_group()
        num= 0
        for group in groups:
            try:
                self.send_message(group, "{}".format(str(text)))
                num+=1
                time.sleep(0.3)
            except:
                pass
        return self.send_message(to,"Success {} groups".format(num))

    def send_message(self, to, text, contentMetadata={}, contentType=0):
        msg = MessageStruct()
        msg.to, msg._from = to, self.my_mid
        msg.text = text
        msg.contentType, msg.contentMetadata = contentType, contentMetadata
        return self.talk.sendMessage(0, msg)

    def send_mention(self, mid, to, text):
        mentiones = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@x  {}'.format(text)
        return self.send_message(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+mentiones+']}'}, contentType=0)

    def send_message_checked(self, to, msg_id):
        return self.talk.sendChatChecked(0, to, msg_id)

    def send_contact(self, to, mid):
        return self.send_message(to, '', {'mid': mid}, 13)

    def send_free_sticker(self, mid, Sid):
        info = self.get_STinfo(sticker_id)
        locale = LocaleStruct()
        locale.language = "EN"
        locale.country = "ID"
        price = info.productDetail.price
        data = PurchaseOrderStruct()
        data.shopId = "stickershop"
        data.productId = sticker_id
        data.recipientMid = mid
        data.price = price
        data.enableLinePointAutoExchange= True
        data.locale = locale
        data.presentAttributes = {}
        return self.shop.placePurchaseOrderForFreeProduct(data)

    def send_paid_sticker(self, mid, Sid):
        info = self.get_STinfo(sticker_id)
        locale = LocaleStruct()
        locale.language = "EN"
        locale.country = "ID"
        price = info.productDetail.price
        data = PurchaseOrderStruct()
        data.shopId = "stickershop"
        data.productId = sticker_id
        data.recipientMid = mid
        data.price = price
        data.enableLinePointAutoExchange= True
        data.locale = locale
        data.presentAttributes = {}
        return self.shop.placePurchaseOrderWithLineCoin(data)

    def tagall_member(self, gmid):
        arr = []
        num = 0
        ret = ""
        group = self.group_info_full(gmid)
        members = [mem.mid for mem in group.members]
        for i in members:
            arrData = {'S':str(len(ret)), 'E':str(len(ret) + len("@x\n") - 1), 'M':i}
            arr.append(arrData)
            ret+= "@x\n"
            num+=1
            if num == 20:
                self.send_message(gmid, ret, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
                num=1
                arr= []
                ret = ""
        return self.send_message(gmid, ret, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)


    def invite_group_call(self, gmid, count=3):
        group = self.group_info_full(gmid)
        members = [mem.mid for mem in group.members]
        for num in range(count):
            self.call.inviteIntoGroupCall(gmid, members, 1)
        return

    def post_sticker(self, to, url):
        data = {
            "type": "template",
            "altText": "Boteater Team",
            "template": {
                "type": "image_carousel",
                "columns": [
                    {
                        "imageUrl": url,
                        "size": "full",
                        "action": {
                            "type": "uri",
                            "uri" : "https://boteater.us/"
                            }
                        }
                    ]
                }
            }
        liff_struct = LiffViewRequestStruct(
            liffId="1586794970-VKzbNLP7",
            context=LiffContextStruct(chat=ChatContextStruct(to)),
            lang="en_ID"
            )
        bearer = self.liff.issueLiffView(liff_struct).accessToken
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; SM-N950N Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36 (Mobile; afma-sdk-a-v12529005.12451000.1)',
                   'Content-Type': 'application/json',
                   'Authorization': 'Bearer {}'.format(bearer)}
        result = requests.post(self.liff_url, json={"messages":[data]}, headers=headers)
        if result.status_code != 200:
            raise Exception("[ Error ] Fail post sticker")
        return


    def post_video(self, to, url):
        data = {
            "type": "video",
            "originalContentUrl": url,
            "previewImageUrl": "https://boteater.us/logo.jpg"
            }
        liff_struct = LiffViewRequestStruct(
            liffId="1586794970-VKzbNLP7",
            context=LiffContextStruct(chat=ChatContextStruct(to)),
            lang="en_ID"
            )
        bearer = self.liff.issueLiffView(liff_struct).accessToken
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; SM-N950N Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36 (Mobile; afma-sdk-a-v12529005.12451000.1)',
                   'Content-Type': 'application/json',
                   'Authorization': 'Bearer {}'.format(bearer)}
        result = requests.post(self.liff_url, json={"messages":[data]}, headers=headers)
        if result.status_code != 200:
            raise Exception("[ Error ] Fail post video")
        return


    def post_image(self, to, url):
        data = {
            "type": "image",
            "originalContentUrl": url,
            "previewImageUrl": url
            }
        liff_struct = LiffViewRequestStruct(
            liffId="1586794970-VKzbNLP7",
            context=LiffContextStruct(chat=ChatContextStruct(to)),
            lang="en_ID"
            )
        bearer = self.liff.issueLiffView(liff_struct).accessToken
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; SM-N950N Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36 (Mobile; afma-sdk-a-v12529005.12451000.1)',
                   'Content-Type': 'application/json',
                   'Authorization': 'Bearer {}'.format(bearer)}
        result = requests.post(self.liff_url, json={"messages":[data]}, headers=headers)
        if result.status_code != 200:
            raise Exception("[ Error ] Fail post image")
        return

    def post_audio(self, to, url):
        data = {
            "type": "audio",
            "originalContentUrl": url,
            "duration": 1000
            }
        liff_struct = LiffViewRequestStruct(
            liffId="1586794970-VKzbNLP7",
            context=LiffContextStruct(chat=ChatContextStruct(to)),
            lang="en_ID"
            )
        bearer = self.liff.issueLiffView(liff_struct).accessToken
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; SM-N950N Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36 (Mobile; afma-sdk-a-v12529005.12451000.1)',
                   'Content-Type': 'application/json',
                   'Authorization': 'Bearer {}'.format(bearer)}
        result = requests.post(self.liff_url, json={"messages":[data]}, headers=headers)
        if result.status_code != 200:
            raise Exception("[ Error ] Fail post audio")
        return

    def post_flex(self, to, data):
        liff_struct = LiffViewRequestStruct(
            liffId="1586794970-VKzbNLP7",
            context=LiffContextStruct(chat=ChatContextStruct(to)),
            lang="en_ID"
            )
        bearer = self.liff.issueLiffView(liff_struct).accessToken
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; SM-N950N Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36 (Mobile; afma-sdk-a-v12529005.12451000.1)',
                   'Content-Type': 'application/json',
                   'Authorization': 'Bearer {}'.format(bearer)}
        result = requests.post(self.liff_url, json={"messages":[data]}, headers=headers)
        if result.status_code != 200:
            raise Exception("[ Error ] Fail post flex")
        return

    def post_timeline_like(self, Aid, Cid):
        data = {'contentId': Cid,
                'actorId': Aid,
                'likeType': random.choice([1001,1002,1003,1004,1005,1006])
                }
        link = self.line_server+'/mh/api/v51/like/create.json?homeId='+Aid
        return json.loads(requests.post(link, headers=self.tl_headers, data=json.dumps(data)).text)

    def post_timeline_comment(self, Aid, Cid, text):
        data = {'contentId': Cid,
                'actorId': Aid,
                'commentText': text,
                'contentsList': [],
                'recallInfos': []
                }
        link = self.line_server+'/mh/api/v51/comment/create.json?homeId='+Aid
        return json.loads(requests.post(link, headers=self.tl_headers, data=json.dumps(data)).text)

    def update_group(self, Ginfo):
        return self.talk.updateGroup(0, Ginfo)

    def update_profile_picture(self):
        headers = copy.deepcopy(self.headers)
        headers["X-Line-Access"] = self.my_OBStoken
        headers["content-type"] = "image/png"
        obs= self.gen_obs_param({"name":"profile.jpg", "type":"image", "ver":"2.0"})
        headers["x-obs-params"] = obs
        result = requests.post(self.line_obs + "/r/talk/p/" + self.my_mid, headers=headers, data=open(self.temp_data["pp"]["pp"], 'rb'))
        if result.status_code != 201:
            raise Exception("[ Error ] Fail change profile picture")
        return

    def update_video_profile(self):
        headers = copy.deepcopy(self.headers)
        headers["X-Line-Access"] = self.my_OBStoken
        headers["content-type"] = "video/mp4"
        obs= self.gen_obs_param({"name": self.temp_data["cvp"]["vid"], "type":"video", "ver":"2.0", "cat":"vp.mp4"})
        headers["x-obs-params"] = obs
        result = requests.post(self.line_obs + "/r/talk/vp/" + self.my_mid, headers=headers, data=open(self.temp_data["cvp"]["vid"], 'rb'))
        if result.status_code != 201:
            raise Exception("Fail change vp")
        headers = copy.deepcopy(self.headers)
        headers["X-Line-Access"] = self.my_OBStoken
        headers["content-type"] = "image/png"
        obs= self.gen_obs_param({"name":"profile.jpg", "type":"image", "ver":"2.0", "cat":"vp.mp4"})
        headers["x-obs-params"] = obs
        result = requests.post(self.line_obs + "/r/talk/p/" + self.my_mid, headers=headers, data=open(self.temp_data["cvp"]["pp"], 'rb'))
        if result.status_code != 201:
            raise Exception("[ Error ] Fail change video profile")
        return

    def update_cover(self):
        oid = self.gen_object_id()
        headers = copy.deepcopy(self.tl_headers)
        headers["X-Line-PostShare"] = "false"
        headers["X-Line-StoryShare"] = "false"
        headers["x-line-signup-region"] = "ID"
        headers["content-type"] = "image/png"
        obs= self.gen_obs_param({"name": self.temp_data["cover"]["pp"], "oid": oid, "type": "image", "userid": self.my_mid, "ver":"2.0"})
        headers["x-obs-params"] = obs
        result = requests.post(self.line_obs + "/r/myhome/c/" + oid, headers=headers, data=open(self.temp_data["cover"]["pp"], 'rb'))
        if result.status_code != 201:
            raise Exception("[ Error ] Fail change cover")
        return


    ### MEDIA ####

    def screenshot_web(self, to, link):
        self.send_message(to,"Please wait....")
        result = json.loads(requests.get(self.boteater_api+"/ss?url="+link).text)
        if result["status"] != 200:
            raise Exception("[ Error ] Error api")
        else:
            self.post_image(to,result["result"])
            return self.send_message(to,result["result"])

    def shorter_link(self, to, link):
        result = json.loads(requests.get(self.boteater_api+"/shorter?url="+link).text)
        if result["status"] != 200:
            raise Exception("[ Error ] Error api")
        else:
            return self.send_message(to,result["result"])

    def wallpaper_hd(self, to, search):
        self.send_message(to,"Please wait....")
        result = json.loads(requests.get(self.boteater_api+"/alphacoders?search="+search).text)
        if result["status"] != 200:
            raise Exception("[ Error ] Error api")
        else:
            flex_data = {
                "type": "flex",
                "altText": "Boteater Team",
                "contents": {
                    "type": "carousel",
                    "contents": []
                    }
                }
            for num in range(10):
                content_data =  {
                    "type": "bubble",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "Boteater Team",
                                "size": "xl",
                                "color": "#000000",
                                "weight": "bold",
                                "decoration": "underline",
                                "align": "center"
                                }
                            ]
                        },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "image",
                                "url": result["result"][num]["url"],
                                "size": "full",
                                "aspectMode": "cover"
                                },
                            {
                                "type": "text",
                                "text": result["result"][num]["name"],
                                "color": "#000000",
                                "wrap": True
                                },
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "Download Link",
                                    "uri": "line://app/1586794970-VKzbNLP7?act=msg&text="+result["result"][num]["url"]
                                    },
                                "margin": "xxl",
                                "height": "sm",
                                "style": "primary"
                                }
                            ]
                        },
                    "styles": {
                        "header": {
                            "backgroundColor": "#01A9DB"
                            },
                        "body": {
                            "backgroundColor": "#81F7F3"
                            }
                        }
                    }
                flex_data["contents"]["contents"].append(content_data) 
            return self.post_flex(to,flex_data)

    def danbooru(self, to, page=1):
        self.send_message(to,"Please wait....")
        result = json.loads(requests.get(self.boteater_api+"/danbooru?page="+page).text)
        if result["status"] != 200:
            raise Exception("[ Error ] Error api")
        else:
            flex_data = {
                "type": "flex",
                "altText": "Boteater Team",
                "contents": {
                    "type": "carousel",
                    "contents": []
                    }
                }
            for num in range(10):
                content_data =  {
                    "type": "bubble",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "Boteater Team",
                                "size": "xl",
                                "color": "#000000",
                                "weight": "bold",
                                "decoration": "underline",
                                "align": "center"
                                }
                            ]
                        },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "image",
                                "url": result["result"][num]["url-local"],
                                "size": "full",
                                "aspectMode": "cover"
                                },
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "Download Link",
                                    "uri": "line://app/1586794970-VKzbNLP7?act=msg&text="+result["result"][num]["url-local"]
                                    },
                                "margin": "xxl",
                                "height": "sm",
                                "style": "primary"
                                }
                            ]
                        },
                    "styles": {
                        "header": {
                            "backgroundColor": "#01A9DB"
                            },
                        "body": {
                            "backgroundColor": "#81F7F3"
                            }
                        }
                    }
                flex_data["contents"]["contents"].append(content_data) 
            return self.post_flex(to,flex_data)

    def google_image(self, to, search):
        result = json.loads(requests.get(self.boteater_api+"/googleimg?search="+search).text)
        if result["status"] != 200:
            raise Exception("[ Error ] Error api")
        else:
            flex_data = {
                "type": "flex",
                "altText": "Boteater Team",
                "contents": {
                    "type": "carousel",
                    "contents": []
                    }
                }
            for num in range(10):
                content_data =  {
                    "type": "bubble",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "Boteater Team",
                                "size": "xl",
                                "color": "#000000",
                                "weight": "bold",
                                "decoration": "underline",
                                "align": "center"
                                }
                            ]
                        },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "image",
                                "url": result["result"][num],
                                "size": "full",
                                "aspectMode": "cover"
                                },
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "Download Link",
                                    "uri": "line://app/1586794970-VKzbNLP7?act=msg&text="+result["result"][num]
                                    },
                                "margin": "xxl",
                                "height": "sm",
                                "style": "primary"
                                }
                            ]
                        },
                    "styles": {
                        "header": {
                            "backgroundColor": "#01A9DB"
                            },
                        "body": {
                            "backgroundColor": "#81F7F3"
                            }
                        }
                    }
                flex_data["contents"]["contents"].append(content_data) 
            return self.post_flex(to,flex_data)

    def joox(self, to, search):
        self.send_message(to,"Please wait....")
        result = json.loads(requests.get(self.boteater_api+"/joox?search="+search).text)
        if result["status"] != 200:
            raise Exception("[ Error ] Error api")
        else:
            flex_data = {
                "type": "flex",
                "altText": "Boteater Team",
                "contents": {
                    "type": "carousel",
                    "contents": []
                    }
                }
            for num in range(5):
                content_data =  {
                    "type": "bubble",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "Boteater Team",
                                "size": "xl",
                                "color": "#000000",
                                "weight": "bold",
                                "decoration": "underline",
                                "align": "center"
                                }
                            ]
                        },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "image",
                                "url": result["result"][num]["image"],
                                "size": "full",
                                "aspectMode": "cover"
                                },
                            {
                                "type": "text",
                                "text": result["result"][num]["artist"]+" - "+result["result"][num]["title"],
                                "color": "#000000",
                                "wrap": True
                                },
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "Download Link",
                                    "uri": "line://app/1586794970-VKzbNLP7?act=msg&text="+result["result"][num]["stream-url"]
                                    },
                                "margin": "xxl",
                                "height": "sm",
                                "style": "primary"
                                },
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "Send Audio",
                                    "uri": "line://app/1586794970-VKzbNLP7?act=audio&url="+result["result"][num]["stream-url"]
                                    },
                                "margin": "sm",
                                "height": "sm",
                                "style": "primary"
                                }
                            ]
                        },
                    "styles": {
                        "header": {
                            "backgroundColor": "#01A9DB"
                            },
                        "body": {
                            "backgroundColor": "#81F7F3"
                            }
                        }
                    }
                flex_data["contents"]["contents"].append(content_data) 
            return self.post_flex(to,flex_data)

    def mal_anime(self, to, search):
        self.send_message(to,"Please wait....")
        result = json.loads(requests.get(self.boteater_api+"/mal/anime?search="+search).text)
        if result["status"] != 200:
            raise Exception("[ Error ] Error api")
        else:
            flex_data = {
                "type": "flex",
                "altText": "Boteater Team",
                "contents": {
                    "type": "carousel",
                    "contents": []
                    }
                }
            for num in range(len(result["result"])):
                content_data =  {
                    "type": "bubble",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "Boteater Team",
                                "size": "xl",
                                "color": "#000000",
                                "weight": "bold",
                                "decoration": "underline",
                                "align": "center"
                                }
                            ]
                        },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "image",
                                "url": result["result"][num]["image"],
                                "size": "full",
                                "aspectMode": "cover"
                                },
                            {
                                "type": "text",
                                "text": result["result"][num]["info"],
                                "color": "#000000",
                                "wrap": True
                                },
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "Original Link",
                                    "uri": result["result"][num]["url-ori"]
                                    },
                                "margin": "xxl",
                                "height": "sm",
                                "style": "primary"
                                }
                            ]
                        },
                    "styles": {
                        "header": {
                            "backgroundColor": "#01A9DB"
                            },
                        "body": {
                            "backgroundColor": "#81F7F3"
                            }
                        }
                    }
                flex_data["contents"]["contents"].append(content_data)
            return self.post_flex(to,flex_data)

    def mal_character(self, to, search):
        self.send_message(to,"Please wait....")
        result = json.loads(requests.get(self.boteater_api+"/mal/char?search="+search).text)
        if result["status"] != 200:
            raise Exception("[ Error ] Error api")
        else:
            flex_data = {
                "type": "flex",
                "altText": "Boteater Team",
                "contents": {
                    "type": "carousel",
                    "contents": []
                    }
                }
            for num in range(len(result["result"])):
                content_data =  {
                    "type": "bubble",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "Boteater Team",
                                "size": "xl",
                                "color": "#000000",
                                "weight": "bold",
                                "decoration": "underline",
                                "align": "center"
                                }
                            ]
                        },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "image",
                                "url": result["result"][num]["image"],
                                "size": "full",
                                "aspectMode": "cover"
                                },
                            {
                                "type": "text",
                                "text": result["result"][num]["info"],
                                "color": "#000000",
                                "wrap": True
                                },
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "Original Link",
                                    "uri": result["result"][num]["url-ori"]
                                    },
                                "margin": "xxl",
                                "height": "sm",
                                "style": "primary"
                                }
                            ]
                        },
                    "styles": {
                        "header": {
                            "backgroundColor": "#01A9DB"
                            },
                        "body": {
                            "backgroundColor": "#81F7F3"
                            }
                        }
                    }
                flex_data["contents"]["contents"].append(content_data)
            return self.post_flex(to,flex_data)

    def yt_dl_local(self, to, search=None, link=None):
        self.send_message(to,"Please wait....")
        if search != None:
            result = json.loads(requests.get(self.boteater_api+"/ytdl-local?search="+search).text)
        elif link != None:
            result = json.loads(requests.get(self.boteater_api+"/ytdl-local?url="+link).text)
        if result["status"] != 200:
            raise Exception("[ Error ] Error api")
        else:
            flex_data = {
                "type": "flex",
                "altText": "Boteater Team",
                "contents": {
                  "type": "carousel",
                  "contents": [
                    {
                      "type": "bubble",
                      "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                          {
                            "type": "text",
                            "text": "Boteater Team",
                            "size": "xl",
                            "color": "#000000",
                            "weight": "bold",
                            "decoration": "underline",
                            "align": "center"
                          }
                        ]
                      },
                      "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                          {
                            "type": "image",
                            "url": result["result"]["thumbnail"],
                            "size": "full",
                            "aspectMode": "cover"
                          },
                          {
                            "type": "button",
                            "action": {
                              "type": "uri",
                              "label": "Download Video",
                              "uri": "line://app/1586794970-VKzbNLP7?act=msg&text="+result["result"]["video_url"]
                            },
                            "margin": "xxl",
                            "height": "sm",
                            "style": "primary"
                          },
                          {
                            "type": "button",
                            "action": {
                              "type": "uri",
                              "label": "Send Video",
                              "uri": "line://app/1586794970-VKzbNLP7?act=video&url="+result["result"]["video_url"]
                            },
                            "margin": "sm",
                            "height": "sm",
                            "style": "primary"
                          },
                          {
                            "type": "button",
                            "action": {
                              "type": "uri",
                              "label": "Download Audio",
                              "uri": "line://app/1586794970-VKzbNLP7?act=msg&text="+result["result"]["audio_url"]
                            },
                            "margin": "xxl",
                            "height": "sm",
                            "style": "primary"
                          },
                          {
                            "type": "button",
                            "action": {
                              "type": "uri",
                              "label": "Send Audio",
                              "uri": "line://app/1586794970-VKzbNLP7?act=audio&url="+result["result"]["audio_url"]
                            },
                            "margin": "sm",
                            "height": "sm",
                            "style": "primary"
                          },
                          {
                            "type": "button",
                            "action": {
                              "type": "uri",
                              "label": "Original Link",
                              "uri": result["result"]["webpage_url"]
                            },
                            "margin": "xxl",
                            "height": "sm",
                            "style": "primary"
                          }
                        ]
                      },
                      "styles": {
                        "header": {
                          "backgroundColor": "#01A9DB"
                        },
                        "body": {
                          "backgroundColor": "#81F7F3"
                        }
                      }
                    }
                  ]
                }
                }
            return self.post_flex(to,flex_data)

