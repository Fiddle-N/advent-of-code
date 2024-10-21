from dataclasses import dataclass

@dataclass(frozen=True)
class Vec:
    px: int
    py: int
    pz: int
    vx: int
    vy: int
    vz: int


def main():
    a = Vec(19, 13, 30, -2, 1, -2)
    b = Vec(18, 19, 22, -1, -1, -2)
    
    axm = 1 / a.vx
    axc = -(a.px) / a.vx

    aym = 1 / a.vy
    ayc = -(a.py) / a.vy

    bxm = 1 / b.vx
    bxc = -(b.px) / b.vx

    bym = 1 / b.vy
    byc = -(b.py) / b.vy

    print(axm, axc, aym, ayc, bxm, bxc, bym, byc)

    ac = (ayc - axc) / - aym
    am = (-axm) / - aym

    print(ac, am)

    bc = (byc - bxc) / - bym
    bm = (-bxm) / - bym

    print(bc, bm)

    x = (ac - bc) / (bm - am)

    print(x)

    y = (am * x) + ac

    print(y)

    print((x - a.px) / )


main()

