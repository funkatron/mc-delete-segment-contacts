import os
import logging

from dotenv import load_dotenv
import requests

load_dotenv()

MC_API_KEY = os.getenv("MC_API_KEY")
MC_LIST_ID = os.getenv("MC_LIST_ID")
MC_SEGMENT_ID = os.getenv("MC_SEGMENT_ID")
MC_API_URL = "https://{}.api.mailchimp.com/3.0/".format(os.getenv("MC_DC"))

MC_PAGING_COUNT = 100

logging.basicConfig(level=logging.INFO)


class MCUnsubber:

    def __init__(self, api_key):
        self.api_key = api_key
        self.session = self.make_request_session(self.api_key)

    def get_url(self, path: str):
        return "{}{}".format(MC_API_URL, path)

    def make_request_session(self, api_key: str):
        s = requests.Session()
        s.headers = {'authorization': 'apikey {}'.format(api_key)}
        return s

    def get_all_segment_members(self, list_id: str, segment_id: str):
        logging.info("Getting all members of segment {} of list {}...".format(MC_SEGMENT_ID, MC_LIST_ID))
        offset = 0
        members = []
        while True:
            logging.debug("Getting members {} to {}".format(offset, (offset + MC_PAGING_COUNT - 1)))
            new_members = self.get_segment_members(list_id, segment_id, offset, MC_PAGING_COUNT)
            if len(new_members) < 1:
                break
            members = members + new_members
            offset += MC_PAGING_COUNT
        logging.info("Done")
        return members

    def get_segment_members(self, list_id: str, segment_id: str, offset: int = 0, count: int = 100):
        segment_members: list = []
        params = {'count': count, 'offset': offset, 'fields': 'members.id'}
        url = self.get_url("lists/{}/segments/{}/members".format(list_id, segment_id))
        resp = self.session.get(url, params=params)
        resp_json = resp.json()
        if resp_json:
            segment_members = resp_json.get('members', [])
        return segment_members

    def delete_list_member(self, list_id: str, member_id: list):
        """
        DELETE lists/c9367a4faf/members/ab1f9522d1ef5a6a5e3accd955c27211
        """
        logging.debug('Deleting member {} from list {}'.format(member_id, list_id))
        url = self.get_url("lists/{}/members/{}".format(list_id, member_id))
        resp = self.session.delete(url)
        if not resp.ok:
            logging.warning("Problem deleting member {}. Raising HTTP Error".format(member_id))
            resp.raise_for_status()


if __name__ == '__main__':
    mcunsubber = MCUnsubber(MC_API_KEY)
    segment_members = mcunsubber.get_all_segment_members(MC_LIST_ID, MC_SEGMENT_ID)
    logging.info("Got {} members for segment {} of list {}".format(len(segment_members), MC_SEGMENT_ID, MC_LIST_ID))
    logging.info('Deleting {} members...'.format(len(segment_members)))
    for member in segment_members:
        if member.get('id'):
            mcunsubber.delete_list_member(MC_LIST_ID, member.get('id'))
    logging.info('Done')
