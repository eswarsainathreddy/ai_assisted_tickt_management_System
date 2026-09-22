import streamlit as st
import time
from datetime import datetime
from src.ui_utils import create_ticket_api, execute_agent_ticket_api

# 🔒 PROTECT PAGE
if not st.session_state.get("logged_in"):
    st.switch_page("pages/home.py")

st.set_page_config(page_title="Create Ticket", page_icon="➕", layout="wide")

# Custom Styles matching AI Ticket Ops Theme
st.markdown("""
<style>
    section[data-testid="stSidebar"] {
        background: #111827;
    }

    .create-card {
        background: linear-gradient(145deg, #111827, #172033);
        border: 1px solid rgba(255,255,255,0.08);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.35);
        margin-bottom: 25px;
    }

    .stButton button {
        background: linear-gradient(90deg, #6C63FF, #8E7CFF);
        color: white;
        border: none;
        border-radius: 10px;
        height: 48px;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .stButton button:hover {
        background: linear-gradient(90deg, #5A52E0, #7A6BFF);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(108,99,255,0.4);
    }

    .success-card {
        background: rgba(34, 197, 94, 0.12);
        border: 1px solid #22c55e;
        border-radius: 14px;
        padding: 20px;
        margin-top: 20px;
        color: #f1f5f9;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    user_display = st.session_state.get("fullname") or st.session_state.get("username", "User")
    st.markdown(f"👤 **Signed in:** `{user_display}`")
    st.divider()
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

st.title("➕ Create New Ticket")
st.markdown("Submit a new customer incident or query directly to the database.")

username = st.session_state.get("username", "sai")
token = st.session_state.get("token", "")

with st.container():
    with st.form("create_ticket_form", clear_on_submit=False):
        st.subheader("📋 Ticket Information")

        title_query = st.text_input(
            "Ticket Title / Query *",
            placeholder="e.g., Charged twice for monthly subscription",
            help="Brief summary of the issue or customer query"
        )

        ticket_description = st.text_area(
            "Detailed Description",
            placeholder="e.g., Customer noticed two debit charges of $29 on their statement for renewal.",
            height=120,
            help="Full explanation of the customer inquiry or problem"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            category = st.selectbox(
                "Category",
                ["Billing", "Refund", "Technical", "Order", "Login", "General"],
                index=0
            )

        with col2:
            priority = st.selectbox(
                "Priority",
                ["Low", "Medium", "High"],
                index=1
            )

        with col3:
            status = st.selectbox(
                "Initial Status",
                ["AI Processing", "Human Review", "Manual Handling", "Resolved"],
                index=0
            )

        st.markdown("---")

        process_mode = st.radio(
            "Creation Mode:",
            [
                "⚡ Direct Database Insert (Instant - saves directly to PostgreSQL)",
                "🤖 Run AI Agent Pipeline (AI classifies, searches knowledge base & drafts response)"
            ],
            index=0
        )

        submit_btn = st.form_submit_button("🚀 Submit Ticket to Database", use_container_width=True)

if submit_btn:
    if not title_query.strip():
        st.error("⚠️ Please provide a Ticket Title / Query.")
    else:
        with st.spinner("Adding ticket to database..."):
            try:
                if "Run AI Agent" in process_mode:
                    # Run through agent pipeline
                    ticket_id = f"TCK{int(time.time()) % 1000000:04d}"
                    payload = {
                        "ticket_id": ticket_id,
                        "user_id": "USR001",
                        "username": username,
                        "title_query": title_query.strip(),
                        "ticket_description": ticket_description.strip() or title_query.strip(),
                        "token": token
                    }
                    try:
                        result = execute_agent_ticket_api(token, payload)
                        st.success(f"🎉 Ticket **{ticket_id}** processed by AI and added to database successfully!")
                    except Exception as agent_err:
                        st.warning(f"AI Agent encountered an issue ({agent_err}). Falling back to direct database insertion...")
                        direct_payload = {
                            "username": username,
                            "category": category,
                            "title_query": title_query.strip(),
                            "ticket_description": ticket_description.strip() or title_query.strip(),
                            "priority": priority,
                            "status": status
                        }
                        result = create_ticket_api(token, direct_payload)
                        st.success(f"🎉 Ticket **{result.get('ticket_id')}** added to database successfully!")
                else:
                    # Direct database insertion
                    direct_payload = {
                        "username": username,
                        "category": category,
                        "title_query": title_query.strip(),
                        "ticket_description": ticket_description.strip() or title_query.strip(),
                        "priority": priority,
                        "status": status
                    }
                    result = create_ticket_api(token, direct_payload)
                    st.success(f"🎉 Ticket **{result.get('ticket_id')}** created and saved to database successfully!")

                # Confirmation Box
                st.markdown(f"""
                <div class="success-card">
                    <h4>✅ Ticket Stored in PostgreSQL Database</h4>
                    <p><strong>Ticket ID:</strong> {result.get('ticket_id', 'TCK')}</p>
                    <p><strong>Category:</strong> {category} | <strong>Priority:</strong> {priority} | <strong>Status:</strong> {status}</p>
                    <p><strong>Query:</strong> {title_query}</p>
                </div>
                """, unsafe_allow_html=True)

                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("🎫 View in All Tickets", use_container_width=True):
                        st.switch_page("pages/view_tickets.py")
                with col_b:
                    if st.button("🏡 Return to Dashboard", use_container_width=True):
                        st.switch_page("pages/home.py")

            except Exception as e:
                st.error(f"❌ Failed to add ticket: {str(e)}")
