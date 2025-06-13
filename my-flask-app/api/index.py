from flask import Flask, request, jsonify
import random

app = Flask(__name__)

def compute_checksum(data):
    total_sum = 0
    if len(data) % 2 != 0:
        data.append(0x00)
    for i in range(0, len(data), 2):
        word = (data[i] << 8) | data[i + 1]
        total_sum += word
        if total_sum > 0xFFFF:
            total_sum = (total_sum & 0xFFFF) + 1
    return ~(total_sum & 0xFFFF) & 0xFFFF

def binary_string_to_bytes(binary):
    bytes_list = []
    for i in range(0, len(binary), 8):
        byte_string = binary[i:i+8]
        if len(byte_string) < 8:
            byte_string = byte_string.ljust(8, '0')
        byte = int(byte_string, 2)
        bytes_list.append(byte)
    return bytes_list

def introduce_errors(data, num_errors):
    for _ in range(num_errors):
        byte_index = random.randint(0, len(data) - 1)
        bit_index = random.randint(0, 7)
        data[byte_index] ^= (1 << bit_index)

def simulate_binary_transmission(binary_input):
    data = binary_string_to_bytes(binary_input)
    checksum = compute_checksum(data)
    data.append((checksum >> 8) & 0xFF)
    data.append(checksum & 0xFF)

    error_bits = 0
    random_chance = random.randint(0, 99)
    if random_chance < 10:
        error_bits = random.randint(1, 3)
        introduce_errors(data, error_bits)
        error_message = f"⚠ Noise simulated: {error_bits} bit error(s) introduced."
    else:
        error_message = "✅ Clean transmission (no errors introduced)."

    receiver_checksum = compute_checksum(data)
    if receiver_checksum == 0x0000:
        result_message = "✅ No error detected. Data is valid."
    else:
        result_message = "❌ Error detected! Data is corrupted."

    return {
        'original_input': binary_input,
        'bytes_data': ' '.join(f"{byte:08b}" for byte in binary_string_to_bytes(binary_input)),
        'sender_checksum': f"0x{checksum:04X}",
        'data_with_checksum': ' '.join(f"{byte:08b}" for byte in data),
        'error_message': error_message,
        'receiver_checksum': f"0x{receiver_checksum:04X}",
        'result_message': result_message
    }

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    binary_input = data.get('binary_input', '')
    if not all(c in '01' for c in binary_input):
        return jsonify({'error': 'Invalid binary input. Only 0s and 1s are allowed.'}), 400
    result = simulate_binary_transmission(binary_input)
    return jsonify(result)

def handler(request):
    with app.test_request_context(path=request.path, method=request.method, json=request.json):
        return app.full_dispatch_request()
