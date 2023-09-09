# Toss Payment SDK for Python

- python version >= 3.8



# Pip install Link
- https://pypi.org/project/python-tosspayments/



# Use

## Load Lib
```python
from tosspayments import Tosspayments
```

## initialize
```python
toss = Tosspayments("Your Toss Payment Secret Key")
```

## Confirm Payment
```python
toss.confirm(payment_key: str, toss_order_id: str, amount: int, idempotency_key: str = None)
```
* idempotency_key 
  * If you want `idempotence`, add idempotency_key. (`not required`)
  * An `idempotency_key` is required for the POST API. The remaining APIs automatically guarantee idempotence. 

## Cancel Payment
```python
toss.cancel(payment_key: str, cancel_data: dict, idempotency_key: str = None)
```
* idempotency_key 
  * If you want `idempotence`, add idempotency_key. (`not required`)
  * An `idempotency_key` is required for the POST API. The remaining APIs automatically guarantee idempotence. 


## Search Payment
```python
toss.search_payment(payment_key: str)
```