import streamlit as st
import pandas as pd
from google import genai
import requests
from datetime import datetime

st.set_page_config(
    page_title="AI Financial Advisor",
    page_icon=" ",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"]{
    font-family: 'Inter', sans-serif;
    background-color: #0e1117;
    color: #ffffff;
}
.chat-message-user {
    background: linear-gradient(135deg, #1a1f2e, #252d3d);
    border: 1px solid #2d3748;
    border-radius: 12px;
    padding: 15px 20px;
    margin: 8px 0;
    margin-left: 20%;
    color: #ffffff;
}
.chat-message-bot {
    background: linear-gradient(135deg, #0d2137, #0a3d2e);
    border: 1px solid #00d4aa;
    border-radius: 12px;
    padding: 15px 20px;
    margin: 8px 0;
    margin-left: 20%;
    color: #ffffff;
}
.chat-label-user {
    font-size: 0.75rem;
    color: #a0aec0;
    margin-bottom: 5px;
    text-align: right;
}
.chat-label-bot{
    font-size: 0.75rem;
    color: #00d4aa;
    margin-bottom: 5px;
}
.metric-card {
    background: linear-gradient(135deg, #1a1f2e, #0252d3d);
    border: 1px solid #2d3748;
    border-radius: 12px;
    padding: 15px;
    text-align: center;
    margin: 5px;
}
.metric-value{
    font-size: 1.5rem;
    font-weight: 700;
    color: #00d4aa;
}
.metric-label {
    font-size: 0.8rem;
    color: #a0aec0;
    margin-top: 3px;
}
.section-header {
    font-size: 1.1rem;
    font-weight: 700;
    color: #00d4aa;
    border-bottom: 2px solid #00d4aa;
    padding bottom: 6px;
    margin: 15px 0 10px 0;
}
.tip-card {
    background: linear-gradient(135deg, #1a2e1a, #1a3a2a);
    border: 1px solid #00d4aa;
    border-radius: 10px;
    padding: 12px 15px;
    margin: 6px 0;
    font-size: 0.9rem;
    color: #e2e8f0;
}
.warn_card {
    background: linear-gradient(135deg, #2e1a1a, #3a1a1a);
    border: 1px solid #ff6b6b;
    border-radius: 10px;
    padding: 12px 15px;
    margin: 6px 0;
    font-size: 0.9rem;
    color: #e2e8f0;
}
</style>
""", unsafe_allow_html=True)

GEMINI_API_KEY = "AIzaSyDOyebFscpwbcbL0Dmm8HW8_sYhI0CtJT0"
client = genai.Client(api_key=GEMINI_API_KEY)

response = client.models.generate_content(
    model="gemini-2.5-flash",
        contents=
    "How should i invest 500,000 Naira in Nigeria?"
)

SYSTEM_PROMPT = """You are Naira Wise, an expert AI Financial Advisor specializing in Nigerian personal finance. You have a deep knowledge of:

1. Nigerian financial products: Piggyvest, Cowrywise,Kuda, Carbon, Fairmoney, Flutterwave, Paystack,Moniepoint
2. Nigerian investment options: NGX stocks, Treasury Bills, Bonds, Fixed Deposits, Real Estate, Agriculture investments
3. CBN policies, interest rates, and monetary policy
4. Nigeria's inflation, exchange rate and economic conditions
5. Personal budgeting and savings strategies for Nigerians
6. Cryptocurrency regulations in Nigeria
7. Tax obligations for Nigerian individuals and businesses
8. Pension and retirement planning in Nigeria (PENCOM, RSA)

Your advice style:
- Always give practical, actionable advice specific to Nigeria
- Use Naira (NGN) for all monetary examples
- Be empathetic to Nigeria's economic challenges
- Explain financial jargon in simple terms
- Always recommend consulting a certified financial advisor for major decisions
- Be conversational, warm and encouraging
- Use Nigerian context and examples where relevant

When asked about investments, always mention:
- Risk level (Low/Medium/High)
- Expected returns in Nigerian Context
- Minimum investment amount in Naira
- Liquidity (how easily can they access their money)

Keep response concise but comprehensive.Use bullet points for clarity."""

def initialize_gemini():
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        return client
    except Exception as e:
        st.error("Gemini error: " + str(e))
        return None
    
def get_ai_response(model, user_message, chat_history):
    try:
        history_text = ""
        for msg in chat_history[-6:]:
            role = "User" if msg["role"] == "user" else "Naira Wise"
            history_text += role + ": " + msg["content"] + "\n"
        full_prompt = (
            SYSTEM_PROMPT
            + "\n\nConversation history:\n"
            + history_text
            + "\nUser: "
            + user_message
            + "\nNaira Wise:"
        )

        response = model.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"
    
def calculate_savings(monthly_savings, months, annual_rate):
    rate = annual_rate / 100 / 12
    if rate == 0:
        return monthly_savings * months
    future_value = monthly_savings * (((1 + rate) ** months - 1) / rate)
    return future_value

def calculate_loan(principal, annual_rate, months):
    rate = annual_rate / 100 / 12
    if rate == 0:
        return principal / months
    payment = principal * (rate * (1 + rate) ** months) / ((1 + rate) ** months - 1)
    return payment

def calculate_inflation_impact(amount, inflation_rate, years):
    return amount / ((1 + inflation_rate / 100) ** years)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "model" not in st.session_state:
    st.session_state.model = initialize_gemini()



st.sidebar.markdown("## Naira Wise")
st.sidebar.markdown("* Your AI Financial Advisor*")
st.sidebar.markdown("---")
st.sidebar.markdown("** Your Profile**")
user_name = st.sidebar.text_input("Your Name", placeholder="e.g. Wisdom")
monthly_income = st.sidebar.number_input(
    "Monthly Income (NGN)", min_value=0, value=150000, step=10000)
financial_goal = st.sidebar.selectbox(
    "Primary Financial Goal",
    ["Save for Emergency Fund",
     "Invest for Passive Income",
     "Pay Off Debt",
     "Save for House",
     "Retirement Planning",
     "Start a Business",
     "Children Education Fund"]
)
st.sidebar.markdown("---")
st.sidebar.markdown("**Quick Questions**")

quick_questions = [
    "How should I start investing in Nigeria?",
    "What is the best savings app in Nigeria?",
    "How do Treasury Bills work in Nigeria?",
    "How can i hedge against Naira devaluation?",
    "What is a good emergency fund size?",
    "How do i invest in NGX stocks?",
    "What are the best fixed deposit rates?",
    "How does Piggyvest Safelock work?"
]


for question in quick_questions:
    if st.sidebar.button(question, key=question, use_container_width=True):
        st.session_state.chat_history.append({
            "role":"user",
            "content": question
        })
        if st.session_state.model:
            response = get_ai_response(
                st.session_state.model,
                question,
                st.session_state.chat_history
            )
            st.session_state.chat_history.append({
                "role":"assistant",
                "content":response
            })

st.sidebar.markdown("---")
if st.sidebar.button("Clear Chat", use_container_width=True):
    st.session_state.chat_history = []


st.sidebar.markdown("---")
st.sidebar.markdown("** Quick Questions**")


greeting = "Hello"
if user_name:
    greeting = "Hello" + (" " + user_name if user_name else "")

st.markdown(
    "<div style='text-align:center; padding: 15px 0'>"
    "<h1 style='color:#00d4aa; font-size:2.2rem; font-weight:700'>"
    " Naira Wise AI"
    "</h1>"
    "<p style='color:#a0aec0; font-size:1rem'>"
    "Your Intelligent Nigerian Financial Advisor"
    "</p></div>",
    unsafe_allow_html=True
)

tab1, tab2, tab3 = st.tabs(
    ["Chat Advisor", "Financial Calculators", "Finance Tips"])

with tab1:
    if not st.session_state.chat_history:
        welcome = (
            greeting + " ! I'm **Naira Wise**, your AI Financial Advisor. "
            "I specialize in Nigerian personal finance.\n\n"
            "I can help you with:\n"
            " Savings and investment strategies\n"
            " Nigerian stock market (NGX)\n"
            " Treasury Bills and Bonds\n"
            " Managing Naira Devalauation\n"
            " Fintech apps(PiggyVest, Cowrywise, Kuda)\n"
            " Real estate investment in Nigeria\n\n"
            "What financial question can i help you with today?"
        )
        st.markdown(
            "<div class='chat-message-bot'>"
            "<div class='chat-label-bot'>Naira Wise</div>"
            + welcome.replace("\n", "<br>")
            + "</div",
            unsafe_allow_html=True
        )
    


    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(
                "<div class='chat-message-user'>"
                "<div class='chat-label-user'>You </div>"
                + message["content"]
                + "</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<div class='chat-message-bot'>"
                "<div class='chat-label-bot'> Naira Wise</div>"
                + message["content"].replace("\n", "<br>")
                + "</div>",
                unsafe_allow_html=True
            )
    st.markdown("")
    col_input, col_btn = st.columns([5, 1])

    with col_input:
        user_input = st.text_input(
            "Ask Naira Wise anything about Nigerian finance...",
            placeholder="e.g. How should i invest 500,000 Naira?",
            key="user_input",
            label_visibility="collapsed"
        )
    
    with col_btn:
        send_btn = st.button("Send ", use_container_width=True)
    
    if send_btn and user_input:
        context = ""
        if monthly_income > 0:
            context = (
                " (Note: The user's monthly income is NGN "
                + str(monthly_income)
                + " and their goal is: "
                + financial_goal
            )
        
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        if st.session_state.model:
            with st.spinner("Naira Wise is thinking..."):
                response = get_ai_response(
                    st.session_state.model,
                    user_input + context,
                    st.session_state.chat_history
                )
            st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response
                })
        st.rerun()

with tab2:
    st.markdown(
        "<p class='section-header'> Nigerian Financial Calculators</p>",
        unsafe_allow_html=True
    )

    calc_type = st.selectbox(
        "Select Calculator",
        ["Savings Goal Calculator",
         "Loan Repayment Calculator",
         "Inflation Impact Calculator",
         "Investment Return Calculator"]
    )

    if calc_type == "Savings Goal Calculator":
            st.markdown("### Savings Goal Calculator")
            col1, col2, col3 = st.columns(3)
            with col1:
                monthly_save = st.number_input(
                    "Monthly Savings (NGN)", min_value=0,
                    value=50000, step=5000)
            with col2:
                save_months = st.slider("Duration (Months)", 1, 120, 12)
            with col3:
                save_rate = st.number_input(
                    "Annual Interest Rate (%)", min_value=0.0,
                    value=12.0, step=0.5)
            
            future_val = calculate_savings(monthly_save, save_months, save_rate)
            total_contributed = monthly_save * save_months
            interest_earned = future_val - total_contributed

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.markdown(
                    "<div class='metric-card'>"
                    "<div class='metric-value'>N" + "{:,.0f}".format(future_val) + "</div>"
                    "<div class='metric-label'>Future Value</div>"
                    "</div>",
                    unsafe_allow_html=True
                )
            with col_b:
                st.markdown(
                    "<div class='metric-card'>"
                    "<div class='metric-value'>N" + "{:,.0f}".format(total_contributed) + "</div>"
                    "<div class='metric-label'>Total Contributed</div>"
                    "</div>",
                    unsafe_allow_html=True
                )
            with col_c:
                st.markdown(
                    "<div class='metric-card'>"
                    "<div class='metric-value'>N" + "{:,.0f}".format(interest_earned) + "</div>"
                    "<div class='metric-label'>Interest Earned</div>"
                    "</div>",
                    unsafe_allow_html=True
                )
            st.markdown("</div>", unsafe_allow_html=True)
        
    elif calc_type == "Loan Repayment Calculator":
            st.markdown(" Loan Repayment Calculator")
            col1, col2, col3 = st.columns(3)
            with col1:
                loan_amount = st.number_input(
                    "Loan Amount (NGN)", min_value=0,
                    value=1000000, step=100000)
            with col2:
                loan_rate = st.number_input(
                    "Annual Interest Rate (%)",
                    value=25.0, step=0.5)
            with col3:
                loan_months = st.slider("Loan Duration (Months)", 1, 60, 12)
            monthly_payment = calculate_loan(loan_amount, loan_rate, loan_months)
            total_payment = monthly_payment * loan_months
            total_interest = total_payment - loan_amount

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.markdown(
                    "<div class='metric-card'>"
                    "<div class='metric-value'>N" + "{:,.0f}".format(monthly_payment) + "</div>"
                    "<div class='metric-label'>Monthly Payment</div>"
                    "</div>",
                    unsafe_allow_html=True
                )
            with col_b:
                st.markdown(
                    "<div class='metric-card'>"
                    "<div class='metric-value'>N" + "{:,.0f}".format(total_payment) + "</div>"
                    "<div class='metric-label'>Total Payment</div>"
                    "</div>",
                    unsafe_allow_html=True
                )
            with col_c:
                st.markdown(
                    "<div class='metric-card'>"
                    "<div class='metric-value'>N" + "{:,.0f}".format(total_interest) + "</div>"
                    "<div class='metric-label'>Total Interest</div>"
                    "</div>",
                    unsafe_allow_html=True
                )
    elif calc_type == "Inflation Impact Calculator":
            st.markdown("### Inflation Impact Calculator")
            col1, col2, col3 = st.columns(3)
            with col1:
                current_amount = st.number_input(
                    "Current Amount (NGN)", min_value=0,
                    value=1000000, step=100000)
            with col2:
                inflation = st.number_input(
                    "Annual Inflation Rate (%)", min_value=0.0,
                    value=33.0, step=0.5)
            with col3:
                years = st.slider("Years", 1, 20, 5)
            
            real_value = calculate_inflation_impact(
                current_amount, inflation, years)
            purchasing_loss = current_amount - real_value
            loss_pct = (purchasing_loss / current_amount) * 100

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.markdown(
                    "<div class='metric-card'>"
                    "<div class='metric-value'>N" + "{:,.0f}".format(real_value) + "</div>"
                    "<div class='metric-label'>ReaL Value in" + str(years) + " Years</div>"
                    "</div>",
                    unsafe_allow_html=True
                )
            with col_b:
                st.markdown(
                    "<div class='metric-card'>"
                    "<div class='metric-value'>N" + "{:,.0f}".format(purchasing_loss) + "</div>"
                    "<div class='metric-label'>Purchasing Power Lost </div>"
                    "</div>",
                    unsafe_allow_html=True
                )
            with col_c:
                st.markdown(
                     "<div class='metric-card'>"
                    "<div class='metric-value'>N" + str(round(loss_pct, 1)) + " pct</div>"
                    "<div class='metric-label'>Value Eroded</div>"
                    "</div>",
                    unsafe_allow_html=True
                )
            warn_msg = (
                "At " + str(inflation) + "pct inflation, your N"
                + "{:,.0f}".format(current_amount)
                + " today will only be worth N"
                + "{:,.0f}".format(round(real_value))
                + " in " + str(years) + " years. Consider investing!"
            )
            st.warning(warn_msg)
            
    elif calc_type == "Investment Return Calculator":
            st.markdown(" ### Investment Return Calculator")
            col1, col2, col3 = st.columns(3)
            with col1:
                invest_amount = st.number_input(
                    "Initial Investment (NGN)", min_value=0,
                    value=500000, step=50000)
            with col2:
                invest_return = st.number_input(
                    "Annual Return (%)", min_value=0.0,
                    value=15.0, step=0.5)
            with col3:
                invest_years = st.slider("Investment Period (Years)", 1, 30, 5)

            future_investment = invest_amount * (
                (1 + invest_return / 100) ** invest_years)
            profit = future_investment - invest_amount
            roi = (profit / invest_amount) * 100

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                 st.markdown(
                    "<div class='metric-card'>"
                    "<div class='metric-value'>N" + "{:,.0f}".format(future_investment) + "</div>"
                    "<div class='metric-label'>Future Value</div>"
                    "</div>",
                    unsafe_allow_html=True
                )
            with col_b:
                st.markdown(
                    "<div class='metric-card'>"
                    "<div class='metric-value'>N" + "{:,.0f}".format(profit) + "</div>"
                    "<div class='metric-label'>Total Profit</div>"
                    "</div>",
                    unsafe_allow_html=True
                )
            with col_c:
                st.markdown(
                     "<div class='metric-card'>"
                    "<div class='metric-value'>N" + str(round(roi, 1)) + " pct</div>"
                    "<div class='metric-label'>Return on Investment</div>"
                    "</div>",
                    unsafe_allow_html=True
                )
            
            with tab3:
                st.markdown(
                    "<p class='section-header'>Nigerian Finance Tips</p>",
                    unsafe_allow_html=True)
                
                col_t1, col_t2 = st.columns(2)

                with col_t1:
                    st.markdown(" ## Savings Tips")
                    tips_savings = [
                        "Follow the 50-30-20 rule: 50% needs, 30% wants, 20% savings",
                        "Use PiggyVest Safelock to avoid touching your savings",
                        "Always keep 3-6 months expenses as emergency fund",
                        "Automate your savings -Pay yourself first every payday",
                        "Save in dollars or USDT to protect against naira devaluation",
                        "Use CowryWise for goal based savings with good interest rates"
                    ]
                    for tip in tips_savings:
                        st.markdown(
                            "<div class='tip-card'> " + tip + "</div>",
                            unsafe_allow_html=True
                        )
                    st.markdoen(" ### Investment Tips")
                    for tip in [
                        "Start with Treasury Bills - low risk, 15-18% annual returns",
                        "Diversify across stocks, bonds and real estate",
                        "Invest in dollar-denominated assets to hedge Naira Risk",
                        "NGX stocks can give 20-30% returns but carry higher risk",
                        "Agriculture investments (Thrive Agric) give 10-15% returns",
                        "Real estate in Lagos and Abuja appreciates 15-20% annually"
                    ]:
                    
                        st.markdown(
                            "<div class='tip-card'> " + tip + "</div>",
                            unsafe_allow_html=True
                        )
                with col_t2:
                    st.markdown(" ### Nigerian Investment Options")
                    investments = [
                        ("Treasury Bills", "Low", "15-18%", "N50,000"),
                        ("Fixed Deposits", "Low", "10-15%", "N100,000"),
                        ("NGX Stocks", "High", "20-30%", "N5,000"),
                        ("Bonds (FGN)", "Low", "14-17%", "N1,000"),
                        ("PiggyVest Flex", "Low", "10-13%", "N100"),
                        ("Cowrywise", "Low", "10-15%", "N1000"),
                        ("Real Estate", "Medium", "15-20%", "N5,000,000"),
                        ("Agriculture", "Medium", "10-15%", "N50,000"),
                    ]
                    st.dataframe(
                        pd.DataFrame(investments,
                                     columns=["Investment", "Risk",
                                              "Annual Return", "Min Amount"]),
                        use_container_width=True,
                        hide_index=True
                    )
                    st.markdown(" ### Warning Signs")
                    for warning in [
                        "Avoid Ponzi schemes - if returns seem too good, they are",
                        "Never invest money you cannot afford to lose in crypto",
                        "Be careful of fake investment platforms on social media",
                        "Always verify CBN-licensed platforms before investing",
                        "High inflation means cash savings lose value quickly"
                    ]:
                        st.markdown(
                            "<div class='warn-card'> " + warning + "</div>",
                            unsafe_allow_html=True)

st.markdown("----")
st.markdown(
    "<div style='text-align:center; color:#a0aec0; padding:10px'>"
    " Naira Wise AI | Built by"
    "<strong style='color:#00d4aa'>Okparaji Wisdom</strong> | "
    "Powered by Google Gemini | "
    "Not a substitute for professional financial advice"
    "</div>",
    unsafe_allow_html=True
)


        
                    





 
            










        
        
        
        




     
