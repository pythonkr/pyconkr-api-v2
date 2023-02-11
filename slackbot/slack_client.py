import os
from typing import Optional

from slack_sdk import WebClient

def mention_member(members: list):
    text = ""
    for member in members:
        text = f"{text} <@{member}>"
    return text


def mention_group(groups: list):
    text = ""
    for group in groups:
        text = f"{text} <!subteam^{groups}>"
    return text


class SlackClient:
    def __init__(self):
        self.client = WebClient(token=os.environ["SLACK_TOKEN"])

    def send_message(
            self,
            channel: str,
            message: str,
            group_ids: list[str] = [],
            member_ids: list[str] = [],
    ):
        """
        Slack Message를 보내는 메서드 입니다.
        @param channel: 메세지를 전송할 채널 ID를 적어주세요.
        @type channel: str
        @param message: 메세지 내용을 적어주세요.
        @type message: str
        @param group_ids: 멘션하고 싶은 group id를 list에 담아주세요. 필수는 아닙니다.
        @type group_ids: list[str]
        @param member_ids: 멘션하고 싶은 member id를 list에 담아주세요. 필수는 아닙니다.
        @type member_ids: list[str
        """
        self.client.chat_postMessage(
            channel=channel,
            text=f"""
                {mention_group(group_ids)} {mention_member(member_ids)} {message}
                """
        )

if __name__ == "__main__":
    client = SlackClient()
    client.send_message(
        channel="C04NR74D895",
        member_ids=["U04JGSN5FMM"],
        message="Hello world"
    )
