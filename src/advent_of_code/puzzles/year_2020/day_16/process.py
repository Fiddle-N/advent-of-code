import collections
import itertools
import math
import timeit


class TicketTranslation:
    def __init__(self, ticket_data=None):
        self.rules: dict[str, set[int]]
        self.nearby_tickets: list[list[int]]
        self.valid_tickets: list[list[int]]
        ticket_data = ticket_data if ticket_data is not None else self._read_file()
        self._preprocess(ticket_data)

    @staticmethod
    def _read_file():
        with open("input.txt") as f:
            return f.read().strip()

    def _preprocess(self, ticket_data):
        rule_data, your_ticket_data, nearby_ticket_data = ticket_data.split("\n\n")
        self.rules = collections.defaultdict(set)
        for line in rule_data.split("\n"):
            rule_name, raw_rule_range_data = line.split(": ")
            rule_range_data = raw_rule_range_data.split(" or ")
            for rule_range in rule_range_data:
                range_start, range_end = rule_range.split("-")
                rule_range = range(int(range_start), int(range_end) + 1)
                self.rules[rule_name].update(list(rule_range))

        _, your_ticket_fields = your_ticket_data.split("\n")
        self.ticket = [
            int(ticket_field) for ticket_field in your_ticket_fields.split(",")
        ]

        self.nearby_tickets = []
        _, nearby_ticket_fields = nearby_ticket_data.split("\n", 1)
        for ticket_line in nearby_ticket_fields.split("\n"):
            self.nearby_tickets.append(
                [int(ticket_field) for ticket_field in ticket_line.split(",")]
            )

    def invalid_tickets(self):
        self.valid_tickets = []
        valid_ranges = set.union(*self.rules.values())
        invalid_fields = []
        for ticket in self.nearby_tickets:
            invalid_ticket_fields = [
                ticket_field
                for ticket_field in ticket
                if ticket_field not in valid_ranges
            ]
            invalid_ticket = bool(invalid_ticket_fields)
            if invalid_ticket:
                invalid_fields.extend(invalid_ticket_fields)
            else:
                self.valid_tickets.append(ticket)
        return invalid_fields

    def _resolve_order(self, field_order):
        while not all((len(fields) == 1) for fields in field_order):
            unresolved_field_order = field_order
            resolved_fields = set.union(
                *[fields for fields in unresolved_field_order if len(fields) == 1]
            )
            field_order = []
            for fields in unresolved_field_order:
                if len(fields) == 1:
                    field_order.append(fields)
                else:
                    field_order.append(fields - resolved_fields)
        return list(itertools.chain.from_iterable(field_order))

    def determine_fields(self):
        valid_tickets = [self.ticket] + self.valid_tickets
        unresolved_field_order = []
        for fields_by_position in zip(*valid_tickets):
            fields_by_position_set = set(fields_by_position)
            potential_fields = set()
            for rule_name, rule_fields in self.rules.items():
                if not (fields_by_position_set - rule_fields):
                    potential_fields.add(rule_name)
            unresolved_field_order.append(potential_fields)
        return self._resolve_order(unresolved_field_order)


def main():
    ticket_translation = TicketTranslation()
    print(f"Ticket scanning error rate: {sum(ticket_translation.invalid_tickets())}")
    field_order = ticket_translation.determine_fields()
    departure_fields = [
        (field, field_value)
        for field, field_value in zip(field_order, ticket_translation.ticket)
        if field.startswith("departure")
    ]
    print(f"Departure fields: {departure_fields}")
    print(f"Departure field value: {math.prod(value for _, value in departure_fields)}")


if __name__ == "__main__":
    print(f"Completed in {timeit.timeit(main, number=1)} seconds")
