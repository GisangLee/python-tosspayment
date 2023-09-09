# Toss Payment SDK for Python

- python version >= 3.8



# Pip install Link
- https://pypi.org/project/python-tosspayments/



# Use

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
### Confirm Payment
```python
toss_client.confirm(payment_key: str, toss_order_id: str, amount: int, idempotency_key: str = None)
```
* request body
  ```
  {
      "amount":"1000",
      "orderId":"ORDER_ID_THAT_YOU_CREATE",  -> need to create when creating your payment data
      "paymentKey":"PAYMENT_KEY_FROM_FRONT_END",  -> We receive it from the front-end.
  }
  ```

### Cancel Payment
```python
toss_client.cancel(payment_key: str, cancel_data: dict, idempotency_key: str = None)
```
* request body
  ```
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

### Search Payment
```python
toss_client.search_payment(payment_key: str)
```