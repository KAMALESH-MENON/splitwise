import phonenumbers

# Test cases
test_numbers = [
    "+14155552671",  # Valid US number
    "4155552671",    # US number without country code
    "+919876543210", # Valid Indian number
    "9876543210",    # Indian number without country code
    "abcd1234",      # Invalid
    "+1-800-ABC-123" # Invalid
]

for num in test_numbers:
    try:
        print(f"Testing: {num}")
        parsed = phonenumbers.parse(num, "US")  # Change "US" if needed
        print(f"Parsed: {parsed}")

        is_valid = phonenumbers.is_valid_number(parsed)
        formatted = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164) if is_valid else "Invalid"

        print(f"Valid: {is_valid}")
        print(f"Formatted: {formatted}\n")

    except phonenumbers.NumberParseException as e:
        print(f"Error parsing '{num}': {e}\n")
