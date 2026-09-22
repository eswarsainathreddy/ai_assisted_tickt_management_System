import requests
from fastapi import Body, Form, HTTPException
import streamlit as st
import pandas as pd
import time

def init_session():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in=False

def login():
    st.set_page_config(
        page_title="AI Ticket Ops - Authentication",
        page_icon="🎫",
        layout="wide"
    )

    st.markdown("""
    <style>
    /* Clean Dark Auth Theme */
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #172554 100%);
    }

    .auth-header {
        text-align: center;
        margin-top: 15px;
        margin-bottom: 24px;
    }

    .auth-logo {
        font-size: 52px;
        margin-bottom: 4px;
        filter: drop-shadow(0 4px 12px rgba(124, 58, 237, 0.4));
    }

    .auth-title {
        font-size: 32px;
        font-weight: 800;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
        margin-bottom: 6px;
    }

    .auth-subtitle {
        color: #94a3b8;
        font-size: 15px;
    }

    .stButton button {
        background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        height: 48px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        transition: all 0.25s ease !important;
        margin-top: 10px !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.3) !important;
    }

    .stButton button:hover {
        background: linear-gradient(90deg, #4f46e5, #7c3aed) !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.45) !important;
    }

    /* Style tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        justify-content: center;
        margin-bottom: 20px;
    }

    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        font-size: 15px;
        padding: 8px 22px;
        border-radius: 10px;
        color: #94a3b8;
    }

    .stTabs [aria-selected="true"] {
        color: #a78bfa !important;
        border-bottom-color: #a78bfa !important;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.35, 1])

    with col2:
        st.markdown("""
        <div class="auth-header">
            <div class="auth-logo">🎫</div>
            <div class="auth-title">AI Ticket Ops</div>
            <div class="auth-subtitle">Autonomous Incident Resolution & Agent Platform</div>
        </div>
        """, unsafe_allow_html=True)

        tab_login, tab_register = st.tabs(["🔐 Sign In", "✨ Create Account"])

        with tab_login:
            st.markdown("##### Sign in with your credentials")
            with st.form("login_form", clear_on_submit=False):
                login_user = st.text_input(
                    "Username",
                    placeholder="Enter your username (e.g. sai, ramya, or your own)",
                    key="login_user"
                )
                login_pwd = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password",
                    key="login_pwd"
                )

                submit_login = st.form_submit_button("🚀 Sign In", use_container_width=True)

            if submit_login:
                if not login_user.strip() or not login_pwd:
                    st.error("⚠️ Please enter both username and password.")
                else:
                    with st.spinner("Authenticating..."):
                        try:
                            response = requests.post(
                                "http://localhost:8000/auth/login",
                                data={
                                    "username": login_user.strip(),
                                    "password": login_pwd
                                }
                            )

                            if response.status_code == 200:
                                res_data = response.json()
                                st.session_state.logged_in = True
                                st.session_state.token = res_data["access_token"]
                                st.session_state.username = res_data.get("username", login_user.strip())
                                st.session_state.fullname = res_data.get("fullname", "")
                                st.success(f"🎉 Welcome back, {st.session_state.username}! Redirecting...")
                                time.sleep(0.4)
                                st.switch_page("pages/home.py")
                            else:
                                err_msg = response.json().get("detail", "Invalid username or password")
                                st.error(f"❌ {err_msg}")
                        except Exception as e:
                            st.error("❌ Could not connect to backend server. Make sure FastAPI is running on port 8000.")

            with st.expander("💡 Quick Demo Credentials"):
                st.markdown("""
                You can use your newly registered account, or any of these demo accounts:
                - **Username:** `sai` | **Password:** `sai123`
                - **Username:** `ramya` | **Password:** `ramya123`
                - **Username:** `sandy` | **Password:** `sandy123`
                """)

        with tab_register:
            st.markdown("##### Create your personal account")
            with st.form("register_form", clear_on_submit=False):
                reg_name = st.text_input(
                    "Full Name *",
                    placeholder="e.g., Eswar Reddy",
                    key="reg_name"
                )
                reg_username = st.text_input(
                    "Username *",
                    placeholder="Choose a unique username",
                    key="reg_username"
                )
                reg_email = st.text_input(
                    "Email Address *",
                    placeholder="e.g., eswar@example.com",
                    key="reg_email"
                )
                reg_mobile = st.text_input(
                    "Mobile Number (Optional)",
                    placeholder="e.g., 9876543210",
                    key="reg_mobile"
                )

                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    reg_pwd = st.text_input(
                        "Password *",
                        type="password",
                        placeholder="Min 4 characters",
                        key="reg_pwd"
                    )
                with col_p2:
                    reg_pwd_confirm = st.text_input(
                        "Confirm Password *",
                        type="password",
                        placeholder="Re-enter password",
                        key="reg_pwd_confirm"
                    )

                submit_reg = st.form_submit_button("✨ Create Account & Sign In", use_container_width=True)

            if submit_reg:
                if not reg_name.strip() or not reg_username.strip() or not reg_email.strip() or not reg_pwd:
                    st.error("⚠️ Please fill in all required fields marked with *.")
                elif "@" not in reg_email or "." not in reg_email:
                    st.error("⚠️ Please enter a valid email address.")
                elif len(reg_pwd) < 4:
                    st.error("⚠️ Password must be at least 4 characters long.")
                elif reg_pwd != reg_pwd_confirm:
                    st.error("⚠️ Passwords do not match.")
                else:
                    with st.spinner("Registering your account in database..."):
                        try:
                            payload = {
                                "fullname": reg_name.strip(),
                                "username": reg_username.strip(),
                                "email": reg_email.strip(),
                                "password": reg_pwd,
                                "mobile_number": reg_mobile.strip() or None
                            }
                            response = requests.post(
                                "http://localhost:8000/auth/register",
                                json=payload
                            )

                            if response.status_code == 200:
                                res_data = response.json()
                                st.session_state.logged_in = True
                                st.session_state.token = res_data["access_token"]
                                st.session_state.username = res_data["username"]
                                st.session_state.fullname = res_data.get("fullname", reg_name.strip())
                                st.success(f"🎉 Account created successfully! Welcome, {reg_name.strip()}!")
                                time.sleep(0.4)
                                st.switch_page("pages/home.py")
                            else:
                                err_msg = response.json().get("detail", "Registration failed")
                                st.error(f"❌ {err_msg}")
                        except Exception as e:
                            st.error("❌ Could not connect to backend server. Make sure FastAPI is running on port 8000.")


def get_tickets_data(token):

    headers = {
    "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        "http://localhost:8000/tickets",
        headers=headers
    )

    return response.json()

def edit_response(token, ticket_id, final_response, userid, username):

    headers = {
    "Authorization": f"Bearer {token}"
    }
    
   
    response= requests.get(
    "http://localhost:8000/threads/thread",
    params={"ticket_id": ticket_id},
    headers=headers)
    
    thread_=response.json()

    thread_id=thread_["thread_id"]

    response = requests.post(
    "http://localhost:8000/agent/resume",

    json={
        "thread_id": thread_id,
        "final_response": final_response,
        "ticket_id": ticket_id,
        "user_id": userid,
        "username": username,
        "token": token
    },
    headers=headers
    )

    # return response.json()

def get_resolved_ticket_details(row):
    data={
           "ticket_id" : row["ticket_id"],

            "user_id" : row["user_id"],
            "username" : row["username"],

            "category" : row["category"],
            "title_query" : row["title_query"],
            "ticket_description" : row["ticket_description"],

            "status" : row["status"],
            "created_at" : row["created_at"],

            "intent" : row["intent"],

            "priority" : row["priority"],

            "ai_response" : row["ai_response"],
            "ai_confidence" : row["ai_confidence"],
            "retrieved_documents" : row["retrieved_documents"],

            "final_response" : row["final_response"],

            "resolution_state" : row["resolution_state"],

            "resolved_by" : row["resolved_by"]
        }
    df=pd.DataFrame(data.items(), columns=["Key","Value"])
    return df

def create_ticket_api(token, ticket_payload):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(
        "http://localhost:8000/tickets/create",
        json=ticket_payload,
        headers=headers
    )
    if response.status_code != 200:
        raise Exception(response.json().get("detail", "Failed to create ticket"))
    return response.json()

def execute_agent_ticket_api(token, ticket_payload):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(
        "http://localhost:8000/agent/execute",
        json=ticket_payload,
        headers=headers
    )
    if response.status_code != 200:
        raise Exception(response.json().get("detail", "Agent failed to process ticket"))
    return response.json()