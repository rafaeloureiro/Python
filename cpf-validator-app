import streamlit as st

def check_first_digit(text):
    sum_variable = sum(int(text[i]) * (10 - i) for i in range(9))
    remainder = sum_variable % 11
    if remainder < 2:
        digit01 = 0
    else:
        digit01 = 11 - remainder
    return digit01 == int(cpf[9])

def check_second_digit(text):
    sum_variable = sum(int(text[i]) * (11 - i) for i in range(10))
    remainder = sum_variable % 11
    if remainder < 2:
        digit02 = 0
    else:
        digit02 = 11 - remainder
    return digit02 == int(cpf[10])

def is_valid_cpf(text):
    # Get all digits
    cpf = ''.join(filter(str.isdigit, cpf_input))

    # Check input text
    if len(cpf) != 11:
        return False, "❌ CPF must have 11 digits"
    elif cpf == cpf[0] * 11:
        return False, "❌ Invalid CPF (repeated sequence!)"

    is_ok = check_first_digit(text)
    if not is_ok:
        return False, "❌ First check digit is invalid!"
    
    is_ok = check_second_digit(text)
    if not is_ok:
        return False, "❌ Second check digit is invalid!"
    return True, "✅ CPF válido!"

def main():
    st.title("CPF Validator")
    cpf_input = st.text_input("Please write you CPF number:")

    if st.button("Validate"):
        is_ok, response = is_valid_cpf(cpf_input)
        if is_ok:
            st.success(response)
        else:
            st.error(response)

main()
