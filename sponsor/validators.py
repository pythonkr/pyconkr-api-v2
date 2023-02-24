from collections import OrderedDict

from sponsor.models import Sponsor


class SponsorValidater:
    def assert_create(self, sponsor: OrderedDict):
        target = [self.check_remain_slot(sponsor)]

    def check_remain_slot(self, sponsor: OrderedDict):
        target_level = sponsor.get("level")

        if target_level.limit <= len(
            Sponsor.objects.filter(level=target_level, accepted=True)
        ):
            raise RuntimeError("ERROR: 남은 슬롯 없음")
