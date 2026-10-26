# big_integer_logarithm_kit

Returns the integer floor of the base-`b` logarithm of an arbitrarily large integer, using bit-length scaling and correction.

```python
from big_integer_logarithm_kit import floor_log_b

print(floor_log_b(10 ** 1000, 10))   # 1000
print(floor_log_b(10 ** 1000 - 1, 10))  # 999
print(floor_log_b(2 ** 5000, 2))     # 5000
```

## Why this exists

`math.log` fails on big integers because it converts to a 64-bit `float` first: `math.log(10**400)` is already `inf`. The `decimal` module can do it but needs global context configuration and is overkill when you only want the floor. This library computes the floor directly from `n.bit_length()`, then corrects with at most two exact `b ** k` comparisons. No floats, no external context, no third-party packages.

## Edge cases

`n == 0` raises `IntegerLogarithmError` (logarithm is undefined there). `n == 1` returns `0` for every base. Bases below `2` are rejected. `bool` arguments are rejected even though `bool` subclasses `int`, because `floor_log_b(8, True)` returning `8` would be a silent footgun.

## Exports

- `floor_log_b(n: int, b: int) -> int` — floor of log base `b` of `n`.
- `IntegerLogarithmError` — subclass of `ValueError`, raised on bad input.
