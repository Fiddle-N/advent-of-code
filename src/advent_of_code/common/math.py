import operator
from dataclasses import dataclass
from enum import Enum
from math import gcd, prod


class Operator(Enum):
    EQ = "=="
    NE = "!="
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="


OP_FNS = {
    Operator.EQ: operator.eq,
    Operator.NE: operator.ne,
    Operator.LT: operator.lt,
    Operator.LE: operator.le,
    Operator.GT: operator.gt,
    Operator.GE: operator.ge,
}


@dataclass(frozen=True)
class ModInt:
    val: int
    mod: int


def crt(mod_ints: list[ModInt]) -> ModInt:
    """
    Given a series of congruences in the form

    x ≡ A mod m
    x ≡ B mod n
    x ≡ C mod o
    etc

    then assuming that m, n, o etc are all coprime
    (they only share 1 as their common divisor)

    find
    x ≡ D mod p

    that would satisfy them all input congruences.
    """
    moduli = [mod_int.mod for mod_int in mod_ints]
    if gcd(*moduli) != 1:
        raise ValueError("Mod Ints are not coprime")
    total_modulus = prod(moduli)
    val = 0
    for mod_int in mod_ints:
        partial_product = total_modulus // mod_int.mod
        mod_inv = pow(partial_product, -1, mod_int.mod)
        val += mod_int.val * partial_product * mod_inv
    return ModInt(val % total_modulus, total_modulus)
