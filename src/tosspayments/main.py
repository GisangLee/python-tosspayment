import requests
import base64


class TossPayments(object):
    def __init__(self, secret_key):
        # self.__secret_key = settings.TOSS_PAYMENT_SECRET
        self.__base_url = "https://api.tosspayments.com/"
        self.__secret_key = secret_key
        self.__api_url = "v1/payments/"

    class HttpError(Exception):
        def __init__(self, code: str, error_type: str, reason=None):
            self.code = code
            self.error_type = error_type
            self.reason = reason

    @staticmethod
    def __get_response(response):
        result = response.json()
        if response.status_code != requests.codes.ok:
            raise TossPayments.HttpError(response.status_code, result.get("code"), result.get("message", ""))
        return result.get("response")

    @staticmethod
    def __get_headers(self):
        """
        시크릿키를 base64로 인코딩해 Authorization에 대입 (비밀번호를 사용하지 않으므로 시크릿 키 뒤에 콜론 포함)
        """
        return {
            "Authorization": "".join(
                [
                    "Basic ",
                    base64.b64encode(f"{self.__secret_key}:".encode("utf-8")).decode("utf-8"),
                ]
            ),
            "Content-Type": "application/json",
        }

    @staticmethod
    def __create_session():
        requests_session = requests.Session()
        requests_adapters = requests.adapters.HTTPAdapter(max_retries=3)
        requests_session.mount("https://", requests_adapters)
        return requests_session

    def __get(self, url: str, params: dict):
        response = self.__create_session().get(
            url,
            headers=self.__get_headers(self),
            params=params,
        )

        return response

    def __post(self, url: str, idempotency_key: str, data: dict):
        headers = self.__get_headers(self)
        new_headers = {
            **headers,
            "Idempotency-Key": idempotency_key,
        }

        response = self.__create_session().post(
            url,
            headers=new_headers,
            json=data,
        )

        return response

    def confirm(self, payment_key: str, toss_order_id: str, idempotency_key: str, amount: int):
        response = self.__post(
            "".join([self.__base_url, self.__api_url, "confirm"]),
            idempotency_key,
            data={
                "paymentKey": payment_key,
                "orderId": toss_order_id,
                "amount": amount,
            },
        )

        if response.status_code == 200:
            return response.json()
        else:
            return self.get_response(response)

    def cancel(self, payment_key: str, idempotency_key: str, cancel_data: dict):
        # refund_receive_account는 가상계좌 결제 건에서만 활용
        refund_receive_account = cancel_data.get("refund_receive_account", {})

        if refund_receive_account:
            data = {
                "cancelReason": cancel_data["cancel_reason"],
                "refundReceiveAccount": {
                    "accountNumber": refund_receive_account.get("account_number"),
                    "bank": refund_receive_account.get("bank"),
                    "holderName": refund_receive_account.get("holder_name"),
                },
            }
        else:
            data = {"cancelReason": cancel_data["cancel_reason"]}

        response = self.__post(
            "".join([self.__base_url, self.__api_url, f"{payment_key}/", "cancel"]),
            idempotency_key,
            data=data,
        )

        if response.status_code == 200:
            return response.json()
        else:
            return self.__get_response(response)

    def search_payment(self, payment_key: str):
        response = self.__get(
            "".join([self.__base_url, self.__api_url, f"{payment_key}"]),
            params={"paymentKey": payment_key},
        )

        if response.status_code == 200:
            return response.json()
        else:
            return self.__get_response(response)