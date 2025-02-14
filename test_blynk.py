import BlynkLib
import time

BLYNK_AUTH = "6GgI9K5dzYI2qdwagMSBVyLKvF3suEvv"

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH, server="blynk.cloud", port=80)

# Correct way to handle virtual pin writes in BlynkLib v0.2.0
@blynk.VIRTUAL_WRITE(1)  # This registers a handler for V1
def v1_read_handler(value):
    received_text = value[0]  # Extract the string
    print(f"Received from Blynk: {received_text}")
    blynk.virtual_write(0, f"Pi received: {received_text}")  # Send acknowledgment to V0

def send_data():
    try:
        while True:
            blynk.run()  # Keep connection alive
            blynk.virtual_write(0, "HelloFrom raspberry")  # Send data to V0
            print("Data sent to Blynk!")
            time.sleep(5)
            # for i in range(100):
            #     blynk.virtual_write(0,i)  # Send data to V0
            #     print("Data sent to Blynk!")
            #     time.sleep(1)
    except KeyboardInterrupt:
        print("\nKeyboard Interrupt detected! Exiting gracefully...")
    finally:
        print("Closing connection to Blynk.")
# Start the function
blynk.start()
