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
  * starting_after
    * Used to query records after a specific payment transaction.
  * limit
    * It's the number of records you will receive in a single response.
    * The default value is 100, and the maximum value that can be set is 10,000