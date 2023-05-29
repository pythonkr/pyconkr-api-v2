import requests
import constance


class PortOneClient:
    # TODO: 상황에 맞는 Error로 변경하기: 지금은 모두 ValueError
    def __init__(self):
        self.url = "https://api.iamport.kr"

    # TODO: 잘 말아서 Singleton 패턴으로 만들기
    def get_access_token(self) -> str:
        endpoint = self.url + "/users/getToken"

        if constance.config["imp_key"] is None or constance.config["imp_secret"] is None:
            raise ValueError("Access Token 발급 실패: imp_key 또는 imp_secret을 찾을 수 없습니다.")

        request_dto = {
            "imp_key": constance.config["IMP_KEY"],
            "imp_secret": constance.config["IMP_SECRET"]
        }

        response = requests.post(
            endpoint,
            request_dto
        )

        if not response.ok:
            raise ValueError("Access Token 발급에 실패했습니다.")

        return response.json().get("access_token")

    def find_payment_info(self, payment_key: str):
        endpoint = self.url + "/payments/{}"

        if payment_key is None or payment_key == "":
            raise ValueError("payment_key (merchant_uid)는 필수값입니다.")

        request_header = {
            "Authorization": self.get_access_token()
        }

        response = requests.get(endpoint.format(payment_key), headers=request_header)

        if not response.ok:
            raise ValueError("결제 정보 조회에 실패했습니다.")

        return response.json()

    def req_cancel_payment(self, payment_key: str, price: int, reason: str = ""):
        endpoint = self.url + "/payments/cancel"

        if payment_key is None or payment_key == "":
            raise ValueError("payment_key (merchant_uid)는 필수값입니다.")

        if price is None or price == 0:
            raise ValueError("금액은 필수값입니다.")

        request_header = {
            "Authorization": self.get_access_token()
        }

        request_dto = {
            "merchant_uid": payment_key,
            "amount": price,
            "checksum": price   # 지금은 전액환불하는 케이스만 존재함 -> 환불요청금액과 결제 건의 환불가능금액은 동일해야함
        }

        if reason is not None and reason != "":
            request_dto["reason"] = reason

        response = requests.post(
            endpoint,
            request_dto,
            headers=request_header
        )

        if not response.ok:
            raise ValueError("Portone에서 비정상 응답: {}".format(payment_key))

        response_data = response.json()

        if response_data.get("code") is None or response_data.get("code") != 0:
            raise ValueError("환불 처리 실패: {}".format(payment_key))

        return True
