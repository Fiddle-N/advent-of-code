def mass_to_fuel(mass):
    return (mass // 3) - 2


def total_fuel(initial_fuel):
    total_fuel = initial_fuel
    input_fuel = initial_fuel
    while True:
        extra_fuel = mass_to_fuel(input_fuel)
        if extra_fuel <= 0:
            extra_fuel = 0
        total_fuel += extra_fuel
        if not extra_fuel:
            return total_fuel
        else:
            input_fuel = extra_fuel


def main():
    with open("input.txt") as f:
        masses = [int(mass) for mass in f]
    initial_fuels = [mass_to_fuel(mass) for mass in masses]
    print(f"initial fuel = {sum(initial_fuels)}")
    print(f"total fuel = {sum(total_fuel(fuel) for fuel in initial_fuels)}")


if __name__ == "__main__":
    main()
