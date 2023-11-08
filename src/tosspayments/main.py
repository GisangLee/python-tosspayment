import requests
import base64


class TossPayments(object):
    def __init__(self, secret_key):
        self.__secret_key = secret_key
        self.__base_url = "https://api.tosspayments.com/"
        self.__api_version = "v1"
        self.__payment_api_url = f"{self.__api_version}/payments/"
        self.__brandpay_api_url = f"{self.__api_version}/brandpay/"
        self.__transactions_api_url = f"{self.__api_version}/transactions/"
        self.__create_billing_key_api_url = f"{self.__api_version}/billing/"

    class __HttpError(Exception):
        def __init__(self, code: str, error_type: str, reason=None):
            self.code = code
            self.error_type = error_type
            self.reason = reason

    def __get_response(self, response):
        result = response.json()
        if response.status_code != requests.codes.ok:
            raise self.__HttpError(
                response.status_code,
                result.get("code"),
                result.get("message", ""),
            )
        return result

    @staticmethod
    def __get_headers(self):
        """
        시크릿키를 base64로 인코딩해 Authorization에 대입 (비밀번호를 사용하지 않으므로 시크릿 키 뒤에 콜론 포함)
        """
        return {
            "Authorization": "".join(
                [
                    "Basic ",
                    base64.b64encode(f"{self.__secret_key}:".encode("utf-8")).decode(
                        "utf-8"
                    ),
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

    def confirm(
        self,
        payment_key: str,
        order_id: str,
        amount: int,
        idempotency_key: str = None,
    ):
        """
        Confirm the payment

        Params:

        - payment_key (str) – The payment key.

        - order_id (str) – order id

        - amount (int) – amount

        - idempotency_key – Idempotency key (if needed).
        """
        response = self.__post(
            "".join([self.__base_url, self.__payment_api_url, "confirm"]),
            data={
                "paymentKey": payment_key,
                "orderId": order_id,
                "amount": amount,
            },
            idempotency_key=idempotency_key,
        )

        return self.__get_response(response)

    def cancel(self, payment_key: str, cancel_data: dict, idempotency_key: str = None):
        """
        Cancel the payment

        Params:

        payment_key (str) – The payment key.

        cancel_data – Data for cancellation:
            - cancel_reason (str, required) – Reason for cancellation. Required.
            - cancel_amount (int, optional) – Amount to cancel. 값이 없으면 전액 취소됩니다.
            - currency (str, optional) – Currency type.  PayPal 해외간편결제 부분 취소에는 필수. PayPal에서 사용할 수 있는 통화는 USD.
            - refund_receive_account (dict, optional) – Refund account. 가상계좌 결제에만 필수:
                - account_number (str, required) – Account number. - 없이 숫자만 넣어야 합니다.
                - bank (str, required) – Bank code.
                - holder_name (str, required) – Account holder's name.
            - tax_amount (int, optional) – Tax amount.
            - tax_exemption_amount (int, optional) – Tax exemption amount.
            - tax_free_amount (int, optional) – Tax free amount.

        idempotency_key – Idempotency key (if needed).
        """

        response = self.__post(
            "".join(
                [self.__base_url, self.__payment_api_url, f"{payment_key}/", "cancel"]
            ),
            data=cancel_data,
            idempotency_key=idempotency_key,
        )

        return self.__get_response(response)

    def get_payment_by_payment_key(self, payment_key: str):
        """
        Search Payment by payment key

        Params:

        - payment_key (str) – The payment key.

        """
        response = self.__get(
            "".join([self.__base_url, self.__payment_api_url, f"{payment_key}"]),
            params={"paymentKey": payment_key},
        )

        return self.__get_response(response)

    def get_payment_by_order_id(self, order_id: str):
        """
        Search Payment by order id

        Params:

        - order_id (str) – order_id.

        """
        response = self.__get(
            "".join(
                [self.__base_url, self.__payment_api_url, "orders/", f"{order_id}"]
            ),
            params={"orderId": order_id},
        )

        return self.__get_response(response)

    def get_transaction(
        self,
        start_date: str,
        end_date: str,
        starting_after: str = None,
        limit: int = None,
    ):
        """
        Search Transaction

        Params:

        - start_date (str) - start date

        - end_date (str) - end date

        - starting_after (str) - last cursor value of transaction

        - limit (int) – number of items to search.

        """
        # 파라미터를 추가할 리스트 생성
        potential_params = [
            ("startDate", start_date),
            ("endDate", end_date),
            ("startingAfter", starting_after),
            ("limit", limit),
        ]

        response = self.__get(
            "".join([self.__base_url, self.__transactions_api_url]),
            params={
                key: value for key, value in potential_params if value
            },  # None이 아닌 값만 딕셔너리에 추가
        )

        return self.__get_response(response)

    def pay_with_card_number(self, data: dict, idempotency_key: str = None):
        """
        Pay with card number

        Params:

        data – Data for cancellation:
            - amount (str, required) - Amount.
            - orderId (str, required) - 주문 번호, need to create when creating your payment data.
            - cardNumber (str, required) - 카드 번호 (최대 20자).
            - cardExpirationYear (str, required) - 카드 유효 년.
            - cardExpirationMonth (str, required) - 카드 유효 월.
            - orderName (str, required) - 주문명 (ex. 생수 외 1건).
            - customerIdentityNumber (str, required) - 카드 소유자 정보 (생년월일 6자리(YYMMDD) 혹은 사업자등록번호 10자리).
            - cardPassword (str, optional) - 카드 비밀번호 앞 두 자리.
            - cardInstallmentPlan (int, optional) - 신용카드 할부 개월 수 ( 2 ~ 12 ) 결제 금액이 5만원 이상일 때만 할부가 적용.
            - useFreeInstallmentPlan (bool, optional) - 카드사 무이자 할부 적용 여부 (default is False).
            - taxFreeAmount (int, optional) - 결제할 금액 중 면제 금액 (default is 0).
            - customerEmail (str, optional) - 고객 이메일 주소 (결제 결과 전송용, 최대 100자).
            - customerName (str, optional) - 고객 이름 (최대 100자).
            - vbv (str, optional) - 해외 카드 결제의 3DS 인증에 사용합니다. 3DS 인증 결과를 전송해야 되면 필수입니다:
                - cavv (str, requried) - 3D Secure session value.
                - xid (str, requried) - transaction id.
                - eci  (str, requried) - "code value of 3DS authentication.

        idempotency_key – Idempotency key (if needed).

        """
        response = self.__post(
            "".join([self.__base_url, self.__payment_api_url, "key-in"]),
            data=data,
            idempotency_key=idempotency_key,
        )

        return self.__get_response(response)

    def request_brand_pay_access_token(
        self,
        customer_key: str,
        grant_type: str,
        code: str = None,
        refresh_token: str = None,
        customer_identity: dict = {},
    ):
        """
        Request Brand Pay Access Token

        Params:

        - customer_key (str, required) - 고객 ID.

        - grant_type (str, required) - 요청 타입. AuthorizationCode, RefreshToken 중 하나.

        - code (str, optional) - 약관 동의 API의 응답 또는 리다이렉트 URL의 쿼리 파라미터로 돌아온 code를 넣어줍니다. grantType이 AuthorizationCode이면 필수.

        - refresh_token(str, optional) - Access Token 발급 API로 돌아온 refreshToken을 넣어줍니다. grantType이 RefreshToken이면 필수.

        - customer_identity (dict, optional) - 인증에 필요한 고객 정보:
            - ci (str, optional) - 고객의 연계 정보(CI)
            - mobilePhone (str, optional)- 고객 휴대폰번호
            - name (str, optional) - 고객 이름
            - rrn (str, optional) - 고객의 주민번호 앞 7자리(생년월일+성별코드)

        :returns {
          "accessToken": "accessToken",
          "refreshToken": "refreshToken",
          "tokenType": "bearer",
          "expiresIn": 2592000
        }

        """
        potential_body = [
            ("customerKey", customer_key),
            ("grantType", grant_type),
            ("code", code),
            ("refreshToken", refresh_token),
            ("customerIdentity", customer_identity),
        ]
        response = self.__post(
            "".join(
                [
                    self.__base_url,
                    self.__brandpay_api_url,
                    "authorizations/access-token",
                ]
            ),
            data={key: value for key, value in potential_body if value},
        )

        return self.__get_response(response)

    def confirm_brandpay(
        self,
        payment_key: str,
        amount: int,
        customer_key: str,
        order_id: str,
    ):
        """
        Search Transaction

        Params:

        - payment_key (str, required) - payment key

        - amount (int, required) - amount

        - customer_key (str, required) - 고객 ID입니다. 가맹점에서 직접 생성하고 관리하는 값.

        - order_id (str, required) – order id

        """
        response = self.__post(
            "".join([self.__base_url, self.__brandpay_api_url, "payments/confirm"]),
            data={
                "paymentKey": payment_key,
                "amount": amount,
                "customerKey": customer_key,
                "orderId": order_id,
            },
        )
        return self.__get_response(response)

    def create_billing_key(self, data: dict):
        """
        Create Billing Key

        Params:

        - data (dict) - 빌링키 발급에 필요한 정보:
            - cardNumber (str) - 카드 번호
            - cardExpirationYear (str)- 카드 반료 년
            - cardExpirationMonth (str) - 카드 반료 월
            - cardPassword (str) - 카드 비밀번호 앞 두자리
            - customerIdentityNumber (str) - 생년월일
            - customerKey (str) - 고객 키

        :return
            {
              "mId": "tosspayments",
              "customerKey": "iy1HaBNtNrFYO3N0YNWbZ",
              "authenticatedAt": "2021-01-01T10:01:30+09:00",
              "method": "카드",
              "billingKey": "iy1HaBNtNrFYO3N0YNWbZ",
              "card": {
                "issuerCode": "61",
                "acquirerCode": "31",
                "number": "43301234****123*",
                "cardType": "신용",
                "ownerType": "개인"
              }
            }
        """
        response = self.__post(
            "".join(
                [
                    self.__base_url,
                    self.__create_billing_key_api_url,
                    "authorizations/card",
                ]
            ),
            data=data,
            idempotency_key=None,
        )

        return self.__get_response(response)

    def pay_with_billing_key(self, billing_key: str, data: dict):
        """
        Create Billing Key

        Params:
        - billing_key (str) - 빌링 key

        - data (dict) - 빌링키 발급에 필요한 정보:
            - amount (int) - 금액
            - orderName (str)- 주문 명
            - orderId (str) - 주문 번호
            - customer_key (str) - 고객 키

        :return
        {
          "mId": "tvivarepublica2",
          "lastTransactionKey": "748038ECC457E11C9532BB4A7B7D02E1",
          "paymentKey": "xMljweGQBN5OWRapdA8dPbZN9zYl7X8o1zEqZKLPbmD70vk4",
          "orderId": "b05c8d5b-7414-44af-9bcd-053e5eeec1e1",
          "orderName": "음악 스트리밍 구독",
          "taxExemptionAmount": 0,
          "status": "DONE",
          "requestedAt": "2023-08-08T16:30:01+09:00",
          "approvedAt": "2023-08-08T16:30:01+09:00",
          "useEscrow": false,
          "cultureExpense": false,
          "card": {
            "company": "토스뱅크",
            "issuerCode": "24",
            "acquirerCode": "21",
            "number": "53275010****222*",
            "installmentPlanMonths": 0,
            "isInterestFree": false,
            "interestPayer": null,
            "approveNo": "00000000",
            "useCardPoint": false,
            "cardType": "신용",
            "ownerType": "개인",
            "acquireStatus": "READY",
            "receiptUrl": "https://dashboard.tosspayments.com/receipt/redirection?transactionId=tviva20230808163001X5IR1&ref=PX",
            "amount": 4900
          },
          "virtualAccount": null,
          "transfer": null,
          "mobilePhone": null,
          "giftCertificate": null,
          "cashReceipt": null,
          "cashReceipts": null,
          "discount": null,
          "cancels": null,
          "secret": null,
          "type": "BILLING",
          "easyPay": null,
          "country": "KR",
          "failure": null,
          "isPartialCancelable": true,
          "receipt": {
            "url": "https://dashboard.tosspayments.com/receipt/redirection?transactionId=tviva20230808163001X5IR1&ref=PX"
          },
          "checkout": {
            "url": "https://api.tosspayments.com/v1/payments/xMljweGQBN5OWRapdA8dPbZN9zYl7X8o1zEqZKLPbmD70vk4/checkout"
          },
          "transactionKey": "748038ECC457E11C9532BB4A7B7D02E1",
          "currency": "KRW",
          "totalAmount": 50000,
          "balanceAmount": 50000,
          "suppliedAmount": 45455,
          "vat": 4545,
          "taxFreeAmount": 0,
          "method": "카드",
          "version": "2022-07-27"
        }
        """
        response = self.__post(
            "".join([self.__base_url, self.__create_billing_key_api_url, billing_key]),
            data=data,
            idempotency_key=None,
        )

        return self.__get_response(response)
