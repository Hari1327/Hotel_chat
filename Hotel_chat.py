import streamlit as st
import requests

# Load API key securely from Streamlit secrets
try:
    HF_API_KEY = st.secrets["HF_API_KEY"]
except KeyError:
    st.error("API key not found. Please add it to secrets.toml")
    st.stop()

# Hugging Face API URL for the Llama model
HF_API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

def chatbot_response(user_input):
    """Sends user input to the Hugging Face API and returns the chatbot's response."""
    payload = {"inputs": user_input}
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad status codes
        result = response.json()
        
        # Extract the generated text from the response
        if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
            return result[0]["generated_text"]
        else:
            return "Error: Unexpected response format."
    except requests.exceptions.RequestException as e:
        return f"Error: API request failed. Details: {e}"

# Streamlit App
st.title("\U0001F3E8 Hotel Chatbot")

# Sidebar options
menu = st.sidebar.radio(
    "Select an option",
    ["Chat", "Make a Booking", "Cancel a Booking", "Payment Methods", "Hotel Info", "Room Service", "WiFi Details", "Local Recommendations", "Customer Support"]
)

if menu == "Chat":
    st.subheader("Chat with the Hotel Bot")
    user_input = st.text_input("Ask me anything about the hotel:")
    if user_input:
        with st.spinner("Generating response..."):
            response = chatbot_response(user_input)
        st.write(response)

elif menu == "Make a Booking":
    st.subheader("Book a Service")
    service = st.selectbox("Choose a service", ["Room", "Dining", "Spa", "Conference Room"])
    date = st.date_input("Select a date")
    if st.button("Confirm Booking"):
        st.success(f"{service} booked for {date}")

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
    st.write("\U0001F3E8 Check-in: 2:00 PM")
    st.write("\U0001F3E8 Check-out: 11:00 AM")
    st.write("\U0001F3E8 Free WiFi available")
    st.write("\U0001F3E8 Swimming pool, gym, spa")

elif menu == "Room Service":
    st.subheader("Order Room Service")
    food_item = st.text_input("Enter food or service request")
    if st.button("Order Now"):
        st.success(f"Room service request received: {food_item}")

elif menu == "WiFi Details":
    st.subheader("WiFi Information")
    st.write("\U0001F4F6 Network: Hotel_WiFi")
    st.write("\U0001F511 Password: Stay@Hotel123")

elif menu == "Local Recommendations":
    st.subheader("Nearby Attractions")
    st.write("\U0001F306 Famous Restaurant: City Dine")
    st.write("\U0001F3DB️ Tourist Spot: Grand Museum")
    st.write("\U0001F6CD️ Shopping Mall: Central Plaza")

elif menu == "Customer Support":
    st.subheader("Customer Support")
    issue = st.text_area("Describe your issue")
    if st.button("Submit Issue"):
        st.warning("Your issue has been reported. Our team will contact you soon.")

# Footer
st.sidebar.info("For assistance, call +123456789 or email support@hotel.com")
