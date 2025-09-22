import streamlit as st

def display_header():
    
    
def check_first_digit(cpf: str) -> bool:
    """
    Compute and validate the first check digit of a CPF.
    """
    # Sum of the first 9 digits weighted by 10‑i
    total = sum(int(cpf[i]) * (10 - i) for i in range(9))
    remainder = total % 11
    digit01 = 0 if remainder < 2 else 11 - remainder
    return digit01 == int(cpf[9])


def check_second_digit(cpf: str) -> bool:
    """
    Compute and validate the second check digit of a CPF.
    """
    # Sum of the first 10 digits weighted by 11‑i
    total = sum(int(cpf[i]) * (11 - i) for i in range(10))
    remainder = total % 11
    digit02 = 0 if remainder < 2 else 11 - remainder
    return digit02 == int(cpf[10])


def is_valid_cpf(cpf_input: str) -> tuple[bool, str]:
    """
    Remove all non‑digit characters, then validate length,
    repeated sequences, and the two check digits.
    """
    # Keep only digits
    cpf = ''.join(filter(str.isdigit, cpf_input))

    # Must contain exactly 11 digits
    if len(cpf) != 11:
        return False, "❌ CPF must have 11 digits"

    # Reject repeated sequences like 11111111111
    if cpf == cpf[0] * 11:
        return False, "❌ Invalid CPF (repeated sequence!)"

    # Validate each check digit
    if not check_first_digit(cpf):
        return False, "❌ First check digit is invalid!"
    if not check_second_digit(cpf):
        return False, "❌ Second check digit is invalid!"

    return True, "✅ Valid CPF!"


# --------------------------------------------------
# Streamlit UI
# --------------------------------------------------
def main() -> None:
    st.title("🔢 CPF validator")
    
    # Input field for the user to type a CPF
    cpf_input = st.text_input("Enter your CPF:", max_chars=11,)

    # When the button is clicked, validate and show the result
    if st.button("Validate"):
        ok, message = is_valid_cpf(cpf_input)
        if ok:
            st.success(message)
        else:
            st.error(message)


# --------------------------------------------------
# Entry point guard
# --------------------------------------------------
if __name__ == "__main__":
    main()
