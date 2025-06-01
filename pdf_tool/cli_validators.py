"""CLI Validators submodule."""

from click import BadParameter


def validate_ranges(ctx, param, value: list[str]) -> list[tuple[int, int]]:  # noqa: ARG001, ANN001
    if value is None:
        return None

    formatted_ranges = []

    for curr_range in value:
        dash_count = curr_range.count("-")

        if dash_count == 1:
            formatted_ranges.append(tuple(map(int, curr_range.split("-"))))

        elif dash_count == 0:
            formatted_ranges.append((int(curr_range), int(curr_range)))

        else:
            raise BadParameter(f'{curr_range}. Ranges should be formatted like this : "1-3 4 5-5 ..."')

    return formatted_ranges


def validate_order(ctx, param, value: list[str]) -> list[int]:  # noqa: ARG001, ANN001
    indexes = []

    for index in value:
        try:
            indexes.append(int(index))
        except ValueError as error:
            raise BadParameter(f"'{index}'. Must be an integer.") from error

    return indexes


if __name__ == "__main__":
    print(validate_ranges(None, None, "1-2 5 3-4"))  # noqa: T201
