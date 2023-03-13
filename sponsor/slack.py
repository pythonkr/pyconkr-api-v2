import requests
from constance import config
from requests import RequestException


def send_new_sponsor_notification(id: int, sponsor_name: str):
    block = _get_base_block()
    block.extend(_get_sponsor_sections(id, sponsor_name))

    try:
        response = requests.post(
            url=config.SLACK_SPONSOR_NOTI_WEBHOOK_URL,
            headers={"Content-Type": "application/json"},
            json={"blocks": block},
        )
    except RequestException as e:
        raise RuntimeError("Slack 호출 중 오류 발생")

    if response.status_code != 200:
        raise RuntimeError("Slack에서 오류 응답: {}".format(response.content))


def _get_base_block() -> list:
    # create block var
    block = list()

    # add Title
    block.append(
        {"type": "section", "text": {"type": "mrkdwn", "text": "새로운 알림이 있습니다."}}
    )

    # add title
    block.append(
        {
            "type": "header",
            "text": {"type": "plain_text", "text": "새로운 후원사 신청이 있습니다. :-)"},
        }
    )

    return block


def _get_sponsor_sections(id: int, sponsor_name: str) -> list:
    section_blocks = list()

    # add sponsor section
    section_blocks.append(
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "{}에서 후원사를 신청했습니다.".format(sponsor_name),
            },
        }
    )

    # add hyperlink button
    section_blocks.append(
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "내용 보기", "emoji": True},
                    "value": "click_me",
                    "url": "https://api.pycon.kr/admin/sponsor/sponsor/{}/change/".format(
                        id
                    ),
                }
            ],
        }
    )

    return section_blocks
