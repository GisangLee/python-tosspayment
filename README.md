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
toss.confirm(payment_key: str, order_id: str, idempotency_key: str, amount: int)
```

## Cancel Payment
```python
toss.cancel(payment_key: str, idempotency_key: str, cancel_data: dict)
```

## Search Payment
```python
toss.search_payment(payment_key: str)
```