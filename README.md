# Toss Payment SDK for Python

- python version >= 3.8

# Pip install Link
- https://pypi.org/project/python-tosspayments/

# Library update will be from last commit of that branch

# branch convention
* naming
  * version-<version_number>
    * ex ) version-0.0.7

# Use

## install 
```zsh
pip install python-tosspayments # latest version
pip install python-tosspayments==0.0.5 # specific version
```

## Load Lib
```python
from tosspayments import Tosspayments
```

## Initialize
```python
toss_client = Tosspayments("Your Toss Payment Secret Key")
```

## APIs
Please visit the official [Toss Payments](https://docs.tosspayments.com/reference) website to find the most up-to-date information.
### Common Guidelines for POST APIs
* idempotency_key  
  * An `idempotency_key` can be used for the POST API (at headers).
    * If you want `idempotence`, add idempotency_key. (`not required`)
    * max_length = 300
  * The remaining APIs automatically guarantee idempotence.
  * [reference](https://docs.tosspayments.com/reference/using-api/idempotency-key)
___

### Pay with Card Number
```python
toss_client.pay_with_card_number(data: dict, idempotency_key: str = None)
```
* request body
  ```Json \
  // Korean
  {
    "data": {
      "amount":1000,
      "orderId":"주문 번호",  -> need to create when creating your payment data
      "cardNumber": "카드 번호 (최대 20자)", -> required,
      "cardExpirationYear": "카드 유효 년", -> required
      "cardExpirationMonth": "카드 유효 월", -> required
      "orderName": "주문명 (ex. 생수 외 1건)", -> required
      "customerIdentityNumber": "카드 소유자 정보 (생년월일 6자리(YYMMDD) 혹은 사업자등록번호 10자리)", -> required
      "cardPassword": "카드 비밀번호 앞 두 자리", -> not required
      "cardInstallmentPlan": 2, -> not required // "신용카드 할부 개월 수 ( 2 ~ 12 )"
      "useFreeInstallmentPlan": "카드사 무이자 할부 적용 여부 (default is False)", -> not required
      "taxFreeAmount": 0 -> not required // "결제할 금액 중 면제 금액 (default is 0)"
      "customerEmail": "고객 이메일 주소 (결제 결과 전송용, 최대 100자)", -> not required
      "customerName": "고객 이름 (최대 100자)", -> not required
  
      // 해외 카드 결제의 3DS 인증에 사용합니다. 3DS 인증 결과를 전송해야 되면 필수입니다.
      "vbv": {
          "cavv": "3D Secure session value",
          "xid": "transaction id",
          "eci ": "code value of 3DS authentication"
       }
    },
    "idempotency_key": "idempotency_key"
  }
  ```
  
  ```Json \
  // English
  {
    "data": {
      "amount":1000,
      "orderId":"ORDER_ID_THAT_YOU_CREATE",  -> need to create when creating your payment data
      "cardNumber": "CARD NUMBER", -> max length is 20 required,
      "cardExpirationYear": "CARD EXPIRATION YEAR", -> required
      "cardExpirationMonth": "CARD EXPIRATION MONTH", -> required
      "orderName": "order name", -> ex) 생수 외 1건 required
      "customerIdentityNumber": "CARD OWNER INFO", -> Birthdate(YYMNMDD) OR Business registration 10 digit number required
      "cardPassword": "First two number of password", -> not required
      "cardInstallmentPlan": 2, -> not required // "(2 ~ 12) Number of installment months for the credit card"
      "useFreeInstallmentPlan": "Whether interest-free installment is applied by the card company", -> not required
      "taxFreeAmount": 0, -> not required // "tax Free Amount (default is 0)"
      "customerEmail": "customer email (max length is 100)", -> not required
      "customerName": "customer name (max length is 100)", -> not required
 
      // translates to "Used for 3DS authentication of overseas card payments. It is essential if you need to send the 3DS authentication results.
      "vbv": {
          "cavv": "3D Secure session value",
          "xid": "transaction id",
          "eci ": "code value of 3DS authentication"
       } 
    },
    "idempotency_key": "idempotency_key",
  },
  ```

### Confirm Payment
```python
toss_client.confirm(payment_key: str, toss_order_id: str, amount: int, idempotency_key: str = None)
```
* request body
  ```Json
  {
      "amount":1000,
      "orderId":"ORDER_ID_THAT_YOU_CREATE",  -> need to create when creating your payment data
      "paymentKey":"PAYMENT_KEY_FROM_FRONT_END",  -> We receive it from the front-end.
  }
  ```

### Cancel Payment
```python
toss_client.cancel(payment_key: str, cancel_data: dict, idempotency_key: str = None)
```
* request body
  ```Json
    cancel_data = {
        "cancel_reason": "단순변심",  -> required
        "cancel_amount": 1000,
        "curreny": "KRW",
        "divided_payment": "True",
        "refund_receive_account": {   -> When a user pays with a virtual account, it is mandatory
            "account_number": "1234567",
            "bank": "13",
            "holder_name": "test" 
        },
        "tax_amount": 100,
        "tax_exemption_amount": 0,
        "tax_free_amount": 0,
    }
  ```
  * Because we send our `payment_key` in the headers, we can simply add the required data when posting to the cancel API.
    * `cancel_reason`, `refund_receive_account (case of virtual_account)`
    * If you want to include the remaining data, you are allowed to do so.

### GET Payment by PaymentKey
```python
toss_client.get_payment_by_payment_key(payment_key: str)
```

### GET Payment by Order id
```python
toss_client.get_payment_by_order_id(order_id: str)
```


### GET Transaction
```python
toss_client.get_transaction(start_date: str, end_date: str, starting_after: str = None, limit: int = None)
```
  * start_date
    * It's the date and time information you want to start the query with.
    * The format is yyyy-MM-dd'T'hh:mm:ss in ISO 8601.
  * end_date
    * It's the date and time information you want to end the query with.
    * The format is yyyy-MM-dd'T'hh:mm:ss in ISO 8601.
    * ex) 
      ```python
          start_date = str((now-datetime.timedelta(days=10)).isoformat())
          end_date = str(now.isoformat())
      ```
  * starting_after
    * Used to query records after a specific payment transaction.
  * limit
    * It's the number of records you will receive in a single response.
    * The default value is 100, and the maximum value that can be set is 10,000