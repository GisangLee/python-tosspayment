import requests
import base64


class TossPayments(object):
    def __init__(self, secret_key):
        # self.__secret_key = settings.TOSS_PAYMENT_SECRET
        self.__base_url = "https://api.tosspayments.com/"
        self.__secret_key = secret_key
        self.api_version = "v1"
        self.__payment_api_url = f"{self.api_version}/payments/"
        self.__transactions_api_url = f"{self.api_version}/transactions/"

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

    def __post(self, url: str, data: dict, idempotency_key: str = None):
        headers = self.__get_headers(self)

        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key

        response = self.__create_session().post(
            url,
            headers=headers,
            json=data,
        )

        return response

    def confirm(self, payment_key: str, order_id: str, amount: int, idempotency_key: str = None):
        response = self.__post(
            "".join([self.__base_url, self.__payment_api_url, "confirm"]),
            data={
                "paymentKey": payment_key,
                "orderId": order_id,
                "amount": amount,
            },
            idempotency_key=idempotency_key,
        )

        if response.status_code == 200:
            return response.json()
        else:
            return self.__get_response(response)

    def cancel(self, payment_key: str, cancel_data: dict, idempotency_key: str = None):
        # virtual_account refund info
        refund_receive_account = cancel_data.get("refund_receive_account", {})

        data = {"cancelReason": cancel_data["cancel_reason"]}

        if refund_receive_account:
            data["refundReceiveAccount"] = {
                "accountNumber":
                    refund_receive_account.get("account_number"),
                "bank": refund_receive_account.get("bank"),
                "holderName": refund_receive_account.get("holder_name"),
            }

        response = self.__post(
            "".join([self.__base_url, self.__payment_api_url, f"{payment_key}/", "cancel"]),
            data=data,
            idempotency_key=idempotency_key,
        )

        if response.status_code == 200:
            return response.json()
        else:
            return self.__get_response(response)

    def get_payment_by_payment_key(self, payment_key: str):
        response = self.__get(
            "".join([self.__base_url, self.__payment_api_url, f"{payment_key}"]),
            params={"paymentKey": payment_key},
        )

        if response.status_code == 200:
            return response.json()
        else:
            return self.__get_response(response)

    def get_payment_by_order_id(self, order_id: str):
        response = self.__get(
            "".join([self.__base_url, self.__payment_api_url, "orders/", f"{order_id}"]),
            params={"orderId": order_id},
        )

        if response.status_code == 200:
            return response.json()
        else:
            return self.__get_response(response)

    def get_transaction(self, start_date: str, end_date: str, starting_after: str = None, limit: int = None):
        # 파라미터를 추가할 리스트 생성
        potential_params = [
            ("startDate", start_date),
            ("endDate", end_date),
            ("startingAfter", starting_after),
            ("limit", limit)
        ]

        response = self.__get(
            "".join([self.__base_url, self.__transactions_api_url]),
            params={key: value for key, value in potential_params if value},  # None이 아닌 값만 딕셔너리에 추가
        )

        if response.status_code == 200:
            return response.json()
        else:
            return self.__get_response(response)