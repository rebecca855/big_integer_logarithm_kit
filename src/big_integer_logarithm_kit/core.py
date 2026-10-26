"""Core integer-floor-of-logarithm routine.

The task: given a non-negative Python ``int`` ``n`` and an integer base
``b >= 2``, return the largest integer ``k`` such that ``b ** k <= n``.

We *cannot* just call ``math.log`` on a 5000-digit number — CPython's
``float`` only has 53 bits of precision, so ``math.log(10**600)`` already
overflows to ``inf`` long before you reach cryptographic sizes.  The
``decimal`` module would work but drags in a global context and per-call
configuration.  The approach here is deliberately narrow: use the bit
length of ``n`` to get a *tight* initial guess for ``k``, then correct
with at most two comparisons of ``b ** k`` against ``n``.

The two real edge cases:
  * ``n == 0`` — log is undefined, so we raise (the README documents this).
  * ``n == 1`` — log of 1 in any base is 0, handled before any division.

Integer exponentiation via Python's built-in ``**`` on ``int`` is exact
and reasonably fast; for the sizes this library targets (up to a few
thousand digits) a Newton / Karatsuba-style exponent ladder would add
complexity without measurable benefit, so we keep it simple.
"""


class IntegerLogarithmError(ValueError):
    """Raised when ``floor_log_b`` is asked for something it cannot return.

    Subclassing ``ValueError`` keeps the exception catchable by callers
    that already trap bad-argument ``ValueError``s.
    """


def floor_log_b(n: int, b: int) -> int:
    """Return the largest integer ``k`` with ``b ** k <= n``.

    Requires ``n >= 0`` and integer base ``b >= 2``; otherwise raises
    :class:`IntegerLogarithmError`.  The result is always a non-negative
    Python ``int``.

    Algorithm:
      1. Reject the undefined / impossible cases.
      2. Short-circuit ``n == 1`` -> ``0`` (avoids a division below).
      3. Estimate ``k0`` via ``n.bit_length() / b.bit_length()``. Because
         ``b`` and ``n`` share the same bit-to-log scaling, this estimate
         is never more than 1 away from the true floor.
      4. Correct: while ``b ** k0 > n`` decrement, while
         ``b ** (k0 + 1) <= n`` increment.  Total correction steps ≤ 2.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise IntegerLogarithmError(f"n must be int, got {type(n).__name__}")
    if not isinstance(b, int) or isinstance(b, bool):
        raise IntegerLogarithmError(f"b must be int, got {type(b).__name__}")

    if n < 0:
        raise IntegerLogarithmError("logarithm undefined for negative n")
    if n == 0:
        raise IntegerLogarithmError("logarithm undefined for n == 0")
    if b < 2:
        raise IntegerLogarithmError(f"base must be >= 2, got {b}")

    if n == 1:
        return 0

    # Bit-length ratio gives a tight seed.  Using floor division on the
    # bit lengths (rather than a float division) avoids precision loss
    # when n is enormous — ``n.bit_length()`` is an exact int.
    k = (n.bit_length() - 1) // b.bit_length()

    # If b is a power of two, ``b.bit_length()`` under-counts by one,
    # so ``b ** k`` can be too large.  Fix with at most one decrement.
    while b ** k > n:
        k -= 1

    # Conversely the seed can be one too small when n is just above a
    # power-of-b boundary.  Fix with at most one increment.
    while b ** (k + 1) <= n:
        k += 1

    return k
