import streamlit as st

st.title("🔎 Validador de CPF")
cpf_input = st.text_input("Digite o CPF:")

if st.button("Validar"):
    cpf = ''.join(filter(str.isdigit, cpf_input))

    if len(cpf) != 11:
        st.error("❌ CPF must have 11 digits")
    elif cpf == cpf[0] * 11:
        st.error("❌ Invalid CPF (repeated sequence!)")
    else:
        try:
            sum_variable = sum(int(cpf[i]) * (10 - i) for i in range(9))
            remainder = sum_variable % 11
            if remainder < 2:
                digit01 = 0
            else:
                digit01 = 11 - remainder

            if digit01 != int(cpf[9]):
                st.error("❌ First check digit is invalid!")
            else:
                sum_variable = sum(int(cpf[i]) * (11 - i) for i in range(10))
                remainder = sum_variable % 11
                if remainder < 2:
                    digit02 = 0
                else:
                    digit02 = 11 - remainder

                if digit02 != int(cpf[10]):
                    st.error("❌ Second check digit is invalid!")
                else:
                    st.success("✅ CPF válido!")

        except IndexError:
            st.error("❌ Error processing CPF - invalid format")
