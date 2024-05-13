# Import necessary libraries
import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt

# Initialize values
measure_limit = 10
messages = []
min_val = None
max_val = None
sum_val = 0

# MQTT settings
broker = "broker.hivemq.com"
port = 1883
topic = "sensor/temperature"

# Callback when a message is received
def on_message(client, userdata, message):
    global min_val, max_val, sum_val
    
    # Decode message
    msg = float(message.payload.decode())
    
    # Append to messages list
    messages.append(msg)
    
    # Update min, max, and sum
    if min_val is None or msg < min_val:
        min_val = msg
    if max_val is None or msg > max_val:
        max_val = msg
    sum_val += msg
    
    # Check if we have received enough messages
    if len(messages) >= measure_limit:
        client.disconnect()

# Setup MQTT client
client = mqtt.Client()
client.on_message = on_message
client.connect(broker, port)

# Subscribe to topic
client.subscribe(topic)

# Start the loop
client.loop_forever()

# Calculate average
avg_val = sum_val / measure_limit

# Print results
print(f"Min: {min_val}")
print(f"Max: {max_val}")
print(f"Avg: {avg_val}")

# Plot graph
plt.plot(messages)
plt.title("Temperature Readings")
plt.xlabel("Message Number")
plt.ylabel("Temperature")
plt.show()
