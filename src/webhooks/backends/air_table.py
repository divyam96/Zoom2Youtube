from airtable import Airtable

from webhooks.backends.base import WebHookBase
from settings import AIR_TABLE_API_KEY, AIR_TABLE_BASE_KEY, AIR_TABLE_TABLE_NAME, AIR_TABLE_TABLE_COLUMNS


class AirTableClient(WebHookBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_key = AIR_TABLE_BASE_KEY
        self.table = AIR_TABLE_TABLE_NAME
        self.columns = AIR_TABLE_TABLE_COLUMNS
        self.token = AIR_TABLE_API_KEY

    def send(self, event_name: str, **kwargs):
        data = self.get_data_for_event(event_name, **kwargs)
        airtable = Airtable(AIR_TABLE_BASE_KEY, AIR_TABLE_TABLE_NAME, api_key=AIR_TABLE_API_KEY)
        airtable.insert(data)

    def new_video(self, **kwargs):
        name = self.payload['result']['name']
        link = self.payload['result']['link']
        data = {self.columns[0]: name, self.columns[1]: link}
        return data
