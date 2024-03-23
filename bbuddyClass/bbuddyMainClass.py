from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path('.') / 'authkey.env'
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    pass


class BuddyClassBlob:

    def __init__(self):

        # Zendesk Agent Base URL -> Used by agents to access tickets on Zendesk
        self.zend_agent_tickets_url = f"https://opendns.zendesk.com/agent/tickets/"
        self.zendesk_ticket_base_url = f"https://opendns.zendesk.com/api/v2/tickets/"

        self.zendesk_api_url = 'https://opendns.zendesk.com/api/v2/views/159080128/tickets.json'
        self.zendesk_org_url = "https://opendns.zendesk.com/api/v2/organizations/"
        self.zendesk_user_url = "https://opendns.zendesk.com/api/v2/users/"

        # WebEx base URL:
        self.webex_base_url = 'https://webexapis.com/v1/'

        # Content type for request headers
        self.contentType = 'application/json'

        # Loading AuthKeys via environment variables:

        self.zendesk_auth_key = os.getenv('zendesk_auth_key')
        self.WebEx_teams_auth_key = os.getenv('WebEx_teams_auth_key')
        self.monday_auth_keys = os.getenv('monday_auth_keys')

        # Tests Bot and space:
        self.tqw_webex_token = os.getenv('tqw_webex_token')
        self.tamqueuewatcher_room_id = os.getenv('tamqueuewatcher_room_id')
        self.Global_TAM_UMB_Queue_watcher = os.getenv('Global_TAM_UMB_Queue_watcher')

        self.zendesk_api_url = 'https://opendns.zendesk.com/api/v2/views/159080128/tickets.json'
        self.zendesk_org_url = "https://opendns.zendesk.com/api/v2/organizations/"
        self.zendesk_user_url = "https://opendns.zendesk.com/api/v2/users/"
        self.zendesk_base_url = "https://opendns.zendesk.com/api/v2/"

        self.zendesk_headers = {
            'Content-Type': self.contentType,
            'Authorization': f'Basic {self.zendesk_auth_key}'
        }

        self.tamBBbot_data = {
            "access_token": "ZmYzOThjZTYtNWVmYi00MjY4LWExYTEtNjQ1MzA5ODNmYTljZjJmNDE5NjMtNDkx_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f",
            "name": "bbbot",
            "address": "Tambbbot@webex.bot"}

        self.tqw_room_id = "Y2lzY29zcGFyazovL3VzL1JPT00vNWMwY2EzZDAtZjI2ZS0xMWVkLTkwYTUtYjdjMTAyNGFjMDZm"
        self.tamBBbot_webHook_data = {
              "id": "Y2lzY29zcGFyazovL3VzL1dFQkhPT0svNDgxYzM1NjMtZjhjMS00ZjQ1LTk2YTgtNTM4YzkyMGMyZTMx",
              "name": "tamBBWebHook",
              "targetUrl": "https://webexapis.com/v1/webhooks/incoming/Y2lzY29zcGFyazovL3VzL1dFQkhPT0svYjEwZTViZDEtMWFlZS00NTQ3LTg5NzEtMzUyNzIyNjhjMzVl",
              "resource": "messages",
              "event": "created",
              "orgId": "Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8xZWI2NWZkZi05NjQzLTQxN2YtOTk3NC1hZDcyY2FlMGUxMGY",
              "createdBy": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS83M2EyZGZmOS1mNmQzLTQ4ODctYjg1Yy0yZDgxYjM1OTdiZTA",
              "appId": "Y2lzY29zcGFyazovL3VzL0FQUExJQ0FUSU9OL0MzMmM4MDc3NDBjNmU3ZGYxMWRhZjE2ZjIyOGRmNjI4YmJjYTQ5YmE1MmZlY2JiMmM3ZDUxNWNiNGEwY2M5MWFh",
              "ownedBy": "creator",
              "status": "active",
              "created": "2024-02-12T07:51:11.297Z"
            }
        # Content type for request headers
        self.contentType = 'application/json'

        # WebEx room ID:
        self.tqw_dev_room = os.getenv('tqw_dev_room')

        # Bot key
        self.UmbrellaBackLogBuddy_key = os.getenv('UmbrellaBackLogBuddy_key')

        # WebEx room api key:
        self.WebEx_teams_auth_key = os.getenv('WebEx_teams_auth_key')

        # Set the header Webex API Endpoint - Production.
        self.webex_headers = {
            'Content-Type': self.contentType,
            'Authorization': f'Bearer {self.WebEx_teams_auth_key}'
        }

        # Set the interval for the API to Zendesk call (in seconds)
        self.polling_interval = 60

        self.EMEA_region = ['GB', 'BE', 'PL', 'ES', 'PT']
        self.US_region = ['CR', 'US', 'CA']
        self.APAC_region = ['AU', 'CN', 'JP']

        self.tams_email_list = ['jalero@cisco.com', 'aparedez@cisco.com', 'anattwoo@cisco.com', 'dforcade@cisco.com',
                                'kporzezr@cisco.com', 'nnwobodo@cisco.com', 'aely@cisco.com', 'arjraina@cisco.com',
                                'ajavaher@cisco.com', 'brparnel@cisco.com', 'ccoral@cisco.com', 'kevhudso@cisco.com',
                                'kvindas@cisco.com', 'mneibert@cisco.com', 'paulth2@cisco.com', 'pwijenay@cisco.com',
                                'tarrashi@cisco.com', 'tingwa2@cisco.com', 'ugandhi@cisco.com', 'wgardeaz@cisco.com',
                                'xiaoshya@cisco.com', 'yusito@cisco.com']
