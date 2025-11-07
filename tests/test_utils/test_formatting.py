import pytest
from src.mcp_openfoodtox.utils.formatting import normalize_e_number


class TestNormalizeENumber:
    """Test cases for E-number normalization."""

    def test_basic_normalization_with_space(self):
        """Test basic E-number normalization with space."""
        assert normalize_e_number("E 422") == "E 422"
        assert normalize_e_number("e 422") == "E 422"
        assert normalize_e_number("E422") == "E 422"
        assert normalize_e_number("e422") == "E 422"

    def test_strip_roman_numeral_suffixes(self):
        """Test stripping roman numeral suffixes (i, ii, iii)."""
        assert normalize_e_number("E460i") == "E 460"
        assert normalize_e_number("E 460i") == "E 460"
        assert normalize_e_number("E460ii") == "E 460"
        assert normalize_e_number("E 460ii") == "E 460"
        assert normalize_e_number("E500ii") == "E500"
        assert normalize_e_number("E 425 i") == "E 425"
        assert normalize_e_number("E 425 ii") == "E 425"

    def test_strip_roman_numeral_with_parentheses(self):
        """Test stripping roman numerals with parentheses."""
        assert normalize_e_number("E 460(i)") == "E 460"
        assert normalize_e_number("E 460(ii)") == "E 460"
        assert normalize_e_number("E 335(ii)") == "E 335"
        assert normalize_e_number("E 336 (i)") == "E 336"
        assert normalize_e_number("E 340(i)") == "E 340"
        assert normalize_e_number("E 340(ii)") == "E 340"

    def test_strip_letter_suffixes(self):
        """Test stripping letter suffixes (a, b, c)."""
        assert normalize_e_number("E 470a") == "E 470"
        assert normalize_e_number("E 470b") == "E 470"
        assert normalize_e_number("E470a") == "E 470"
        assert normalize_e_number("E470b") == "E 470"

    def test_strip_combined_suffixes(self):
        """Test stripping combined letter and roman numeral suffixes."""
        assert normalize_e_number("E 160a (ii)") == "E 160"
        assert normalize_e_number("E 160b(i)") == "E 160"
        assert normalize_e_number("E 160b(ii)") == "E 160"
        assert normalize_e_number("E160a(ii)") == "E 160"
        assert normalize_e_number("E160b(i)") == "E 160"

    def test_edge_case_e500(self):
        """Test edge case: E500 should not have space."""
        assert normalize_e_number("E500") == "E500"
        assert normalize_e_number("E 500") == "E500"
        assert normalize_e_number("e500") == "E500"
        assert normalize_e_number("e 500") == "E500"
        assert normalize_e_number("E500ii") == "E500"
        assert normalize_e_number("E 500i") == "E500"

    def test_edge_case_e905(self):
        """Test edge case: E905 should not have space."""
        assert normalize_e_number("E905") == "E905"
        assert normalize_e_number("E 905") == "E905"
        assert normalize_e_number("e905") == "E905"
        assert normalize_e_number("e 905") == "E905"

    def test_complex_examples_from_user(self):
        """Test complex examples provided by the user."""
        # All should normalize to base E-number
        assert normalize_e_number("E 160a (ii)") == "E 160"
        assert normalize_e_number("E 160b(i)") == "E 160"
        assert normalize_e_number("E 160b(ii)") == "E 160"
        assert normalize_e_number("E 335(ii)") == "E 335"
        assert normalize_e_number("E 336 (i)") == "E 336"
        assert normalize_e_number("E 340(i)") == "E 340"
        assert normalize_e_number("E 340(ii)") == "E 340"
        assert normalize_e_number("E 425 i") == "E 425"
        assert normalize_e_number("E 425 ii") == "E 425"
        assert normalize_e_number("E 460(i)") == "E 460"
        assert normalize_e_number("E 460(ii)") == "E 460"
        assert normalize_e_number("E 470a") == "E 470"
        assert normalize_e_number("E 470b") == "E 470"
        assert normalize_e_number("E500ii") == "E500"
        assert normalize_e_number("E905") == "E905"

    def test_non_e_number_input(self):
        """Test that non-E-number input is returned unchanged."""
        assert normalize_e_number("aspartame") == "aspartame"
        assert normalize_e_number("vitamin a") == "vitamin a"
        assert normalize_e_number("450") == "450"  # Pure number without E
        assert normalize_e_number("") == ""
        assert normalize_e_number("E") == "E"

    def test_multiple_e_numbers(self):
        """Test behavior with multiple E-numbers (should normalize first one)."""
        # The regex will match the first E-number
        result = normalize_e_number("E 422 and E 951")
        assert result == "E 422"  # Only first match is normalized

    def test_case_insensitivity(self):
        """Test that function is case-insensitive for E/e."""
        assert normalize_e_number("E460") == normalize_e_number("e460")
        assert normalize_e_number("E 500") == normalize_e_number("e 500")
        assert normalize_e_number("E905") == normalize_e_number("e905")

