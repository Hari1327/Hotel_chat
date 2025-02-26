import streamlit as st
from transformers import pipeline

# Load Hugging Face chatbot model
chatbot = pipeline("conversational", model="facebook/blenderbot-400M-distill")

def chatbot_response(user_input):
    response = chatbot(user_input)
    return response["generated_responses"][0]

st.title("🏨 Hotel Chatbot")

# Sidebar options
menu = st.sidebar.radio("Select an option", ["Chat", "Make a Booking", "Cancel a Booking", "Payment Methods", "Hotel Info", "Room Service", "WiFi Details", "Local Recommendations", "Customer Support"])

if menu == "Chat":
    user_input = st.text_input("Ask me anything about the hotel:")
    if user_input:
        response = chatbot_response(user_input)
        st.write(response)

elif menu == "Make a Booking":
    st.subheader("Book a Service")
    service = st.selectbox("Choose a service", ["Room", "Dining", "Spa", "Conference Room"])
    date = st.date_input("Select a date")
    st.button("Confirm Booking", on_click=lambda: st.success(f"{service} booked for {date}"))

elif menu == "Cancel a Booking":
    st.subheader("Cancel a Booking")
    booking_id = st.text_input("Enter your booking ID")
    if st.button("Cancel Booking"):
        st.error(f"Booking {booking_id} has been canceled.")

elif menu == "Payment Methods":
    st.subheader("Available Payment Methods")
    st.write("✅ Credit/Debit Card")
    st.write("✅ PayPal")
    st.write("✅ Google Pay / Apple Pay")
    st.write("✅ Cash at Reception")

elif menu == "Hotel Info":
    st.subheader("Hotel Information")
    st.write("🏨 Check-in: 2:00 PM")
    st.write("🏨 Check-out: 11:00 AM")
    st.write("🏨 Free WiFi available")
    st.write("🏨 Swimming pool, gym, spa")

elif menu == "Room Service":
    st.subheader("Order Room Service")
    food_item = st.text_input("Enter food or service request")
    if st.button("Order Now"):
        st.success(f"Room service request received: {food_item}")

elif menu == "WiFi Details":
    st.subheader("WiFi Information")
    st.write("📶 Network: Hotel_WiFi")
    st.write("🔑 Password: Stay@Hotel123")

elif menu == "Local Recommendations":
    st.subheader("Nearby Attractions")
    st.write("🌆 Famous Restaurant: City Dine")
    st.write("🏛️ Tourist Spot: Grand Museum")
    st.write("🛍️ Shopping Mall: Central Plaza")

elif menu == "Customer Support":
    st.subheader("Customer Support")
    issue = st.text_area("Describe your issue")
    if st.button("Submit Issue"):
        st.warning("Your issue has been reported. Our team will contact you soon.")

st.sidebar.info("For assistance, call +123456789 or email support@hotel.com")
