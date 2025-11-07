import re


def normalize_e_number(query: str) -> str:
    """
    Normalize E-number queries by stripping suffixes and standardizing format.

    - Strips all suffixes (letters a/b/c, roman numerals i/ii/iii with/without parens)
    - Normalizes base to 'E 999' format (uppercase E, space, number)
    - Exception: E500 and E905 are normalized to 'E500' and 'E905' (no space)
    - Also handles edge cases: 'e 500' -> 'E500', 'E 905' -> 'E905'

    Args:
        query: Input string that may contain an E-number

    Returns:
        Normalized E-number string, or original string if no E-number pattern found

    Examples:
        >>> normalize_e_number("E460i")
        'E 460'
        >>> normalize_e_number("E 160a (ii)")
        'E 160'
        >>> normalize_e_number("e500ii")
        'E500'
        >>> normalize_e_number("E 500")
        'E500'
        >>> normalize_e_number("E 905")
        'E905'
        >>> normalize_e_number("e422")
        'E 422'
    """
    # Pattern to match E-numbers: E/e followed by optional space, then capture digits
    # The digits are the base number; everything after is suffix to be stripped
    pattern = r"[Ee]\s*(\d+)"

    match = re.search(pattern, query, re.IGNORECASE)
    if not match:
        return query

    # Extract the base number (first sequence of digits after E/e)
    number_str = match.group(1)
    number = int(number_str)

    # Normalize based on number
    if number == 500:
        return "E500"
    elif number == 905:
        return "E905"
    else:
        return f"E {number}"
