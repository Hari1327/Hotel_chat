import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load the DeepSeek model and tokenizer
try:
    model_name = "deepseek-ai/DeepSeek-R1"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)
    print("DeepSeek model and tokenizer loaded successfully! ✅")
except Exception as e:
    st.error(f"Error loading the DeepSeek model: {e}")
    st.stop()

def chatbot_response(user_input):
    """Generates a response using the DeepSeek model."""
    try:
        # Tokenize the input
        inputs = tokenizer(user_input, return_tensors="pt")

        # Generate a response
        outputs = model.generate(
            **inputs,
            max_length=100,  # Adjust max_length as needed
            num_return_sequences=1,  # Generate one response
            no_repeat_ngram_size=2,  # Avoid repeating phrases
            top_p=0.9,  # Nucleus sampling
            temperature=0.7,  # Control randomness
        )

        # Decode the generated text
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
    except Exception as e:
        return f"Error generating response: {e}"

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
