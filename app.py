import streamlit as st

# Initialize session state for the calculator
if 'calc_display' not in st.session_state:
    st.session_state.calc_display = ""
if 'show_result' not in st.session_state:
    st.session_state.show_result = False
if 'last_result' not in st.session_state:
    st.session_state.last_result = ""

def update_input(value):
    if st.session_state.show_result:
        st.session_state.calc_display = str(value)
        st.session_state.show_result = False
    else:
        value = value.replace('＊', '*').replace('−', '-').replace('＋', '+').replace('÷', '/')
        if value in ['+', '-', '*', '/', '^2']:
            if st.session_state.calc_display and st.session_state.calc_display[-1] in ['+', '-', '*', '/', '^2']:
                st.session_state.calc_display = st.session_state.calc_display[:-1] + value
            else:
                st.session_state.calc_display += str(value)
        else:
            st.session_state.calc_display += str(value)

def reset_display():
    st.session_state.calc_display = ""
    st.session_state.show_result = False

def delete_last_character():
    st.session_state.calc_display = st.session_state.calc_display[:-1]

def use_last_result():
    if st.session_state.last_result:
        if st.session_state.calc_display == "":
            st.session_state.calc_display = st.session_state.last_result
        elif st.session_state.calc_display[-1] in ['+', '-', '*', '/']:
            st.session_state.calc_display += st.session_state.last_result
        else:
            st.session_state.calc_display += " * " + st.session_state.last_result

def evaluate_expression():
    try:
        expression = st.session_state.calc_display
        # Replace ^2 with **2 for squaring
        while '^2' in expression:
            # Find the position of the last occurrence of ^2
            pos = expression.rfind('^2')
            # Find the position of the number or expression preceding ^2
            start_pos = pos - 1
            while start_pos > 0 and expression[start_pos].isdigit() or expression[start_pos] in '.':
                start_pos -= 1
            start_pos += 1
            # Extract the number or expression before ^2
            before_power = expression[start_pos:pos]
            # Replace the last occurrence of ^2 with **2
            expression = expression[:start_pos] + f"({before_power})**2" + expression[pos + 2:]
        
        # Evaluate the expression
        if st.session_state.calc_display:
            result = str(eval(expression))
            st.session_state.last_result = result
            st.session_state.calc_display = result
    except Exception as e:
        st.session_state.calc_display = "INF"
        st.session_state.last_result = ""  # Clear last result on error

def main():
    # Sidebar content
    st.sidebar.image("cinnamon_bootcamp.jpg", caption="Cinnamon Bootcamp", use_column_width=True)  # Adjust file name and caption as needed
    st.sidebar.write("""
        **Calculator Instructions:**

        - **AC**: Clear all input
        - **DEL**: Delete the last character
        - **Ans**: Use the last result in the current expression
        - **^2**: Square the preceding number
        - **=**: Evaluate the expression
    """)

    # Title of the app
    st.title("Simple Calculator")

    # Display for input and result
    current_display = st.text_input("Output", value=st.session_state.calc_display, key="calc_display", disabled=True)

    # CSS to style buttons uniformly
    st.markdown("""
        <style>
        .custom-button {
            background-color: #e8e8e8;
            border: none;
            border-radius: 8px;
            color: black;
            padding: 0;
            text-align: center;
            text-decoration: none;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;   
            cursor: pointer;
            width: 100%;
            height: 60px;
            box-sizing: border-box; 
        }
        .custom-button:hover {
            background-color: #c0c0c0;
        }
        .stButton>button {
            width: 100%;
            height: 100%;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        .stButton>button:focus {
            outline: none;
        }
        </style>
    """, unsafe_allow_html=True)

    # Layout for calculator buttons
    button_layout = [
        ['7', '8', '9', 'DEL', 'AC'],
        ['4', '5', '6', '＊', '÷'],
        ['1', '2', '3', '＋', '−'],
        ['0', '.', 'Ans', '^2', '=']
    ]

    # Display the buttons
    for row in button_layout:
        columns = st.columns(len(row))  # Create columns for each button
        for idx, button in enumerate(row):
            with columns[idx]:
                if button == 'AC':
                    st.button(button, on_click=reset_display, key=button, help="Clear display", use_container_width=True)
                elif button == 'DEL':
                    st.button(button, on_click=delete_last_character, key=button, help="Delete last character", use_container_width=True)
                elif button == 'Ans':
                    st.button(button, on_click=use_last_result, key=button, help="Use last result", use_container_width=True)
                elif button == '=':
                    st.button(button, on_click=evaluate_expression, key='equals', help="Calculate the result", use_container_width=True)
                elif button == '^2':
                    st.button(button, on_click=update_input, args=('^2',), key=button, use_container_width=True)
                else:
                    st.button(button, on_click=update_input, args=(button,), key=button, use_container_width=True)

if __name__ == "__main__":
    main()