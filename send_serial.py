import serial
import time
import serial.tools.list_ports

# ports = serial.tools.list_ports.comports()
# for port in ports:  
#     print(f"Found serial device: {port.device}")


# Define the serial port and baud rate
serial_port = "/dev/ttyUSB1"  # Update if different
baud_rate = 9600  # Adjust based on your device

# Open the serial connection
ser = serial.Serial(serial_port, baud_rate, timeout=1)

try:
    while True:
        data_to_send = input("Enter message to send: ")  # Get user input
        ser.write(data_to_send.encode())  # Send data
        print(f"Sent: {data_to_send}")
        time.sleep(1)  # Small delay
        if ser.in_waiting > 0:
            received_data = ser.readline().decode().strip()
            print(f"Received: {received_data}")
            if received_data=="sandhiya":
                print("Correct")
            else:
                print("Incorrect")

except KeyboardInterrupt:
    print("\nClosing serial connection.")
    ser.close()

