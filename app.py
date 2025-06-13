import random
import time

# ---------- Phase 2: Checksum Computation ----------
def compute_checksum(data):
    total_sum = 0

    if len(data) % 2 != 0:
        data.append(0x00)  # Padding

    for i in range(0, len(data), 2):
        word = (data[i] << 8) | data[i + 1]
        total_sum += word

        if total_sum > 0xFFFF:
            total_sum = (total_sum & 0xFFFF) + 1  # Wrap around

    return ~(total_sum & 0xFFFF) & 0xFFFF  # One's complement

# ---------- Convert binary string to byte vector ----------
def binary_string_to_bytes(binary):
    bytes_list = []
    for i in range(0, len(binary), 8):
        byte_string = binary[i:i+8]
        if len(byte_string) < 8:
            byte_string = byte_string.ljust(8, '0')  # Padding if last byte is incomplete
        byte = int(byte_string, 2)
        bytes_list.append(byte)
    return bytes_list

# ---------- Error Simulation ----------
def introduce_errors(data, num_errors):
    for _ in range(num_errors):
        byte_index = random.randint(0, len(data) - 1)
        bit_index = random.randint(0, 7)
        data[byte_index] ^= (1 << bit_index)  # Flip random bit

# ---------- Transmission Simulation ----------
def simulate_binary_transmission(binary_input):
    print("\n=== Transmission Simulation Steps ===")

    # Step 1: Show original input
    print("\nStep 1: Original Binary Input")
    print("-----------------------------")
    print(binary_input)

    data = binary_string_to_bytes(binary_input)

    # Step 2: Show the data converted to bytes
    print("\nStep 2: Binary Data Converted to Bytes")
    print("-------------------------------------")
    for byte in data:
        print(f"{byte:08b}", end=" ")
    print()

    checksum = compute_checksum(data)

    # Step 3: Show checksum computation
    print("\nStep 3: Checksum Computation")
    print("---------------------------")
    print(f"Sender Checksum: 0x{checksum:04X}")

    # Step 4: Show data with checksum appended
    print("\nStep 4: Data with Checksum Appended")
    print("----------------------------------")
    data.append((checksum >> 8) & 0xFF)
    data.append(checksum & 0xFF)
    for byte in data:
        print(f"{byte:08b}", end=" ")
    print()

    # Optional: simulate error
    error_bits = 0
    random_chance = random.randint(0, 99)
    if random_chance < 10:
        error_bits = random.randint(1, 3)
        introduce_errors(data, error_bits)
        print(f"\n⚠  Noise simulated: {error_bits} bit error(s) introduced.")
    else:
        print("\n✅ Clean transmission (no errors introduced).")

    # Step 5: Show receiver's verification process
    print("\nStep 5: Receiver's Verification")
    print("------------------------------")
    receiver_checksum = compute_checksum(data)
    print(f"Receiver Computed Checksum: 0x{receiver_checksum:04X}")

    # Step 6: Show verification result
    print("\nStep 6: Verification Result")
    print("--------------------------")
    if receiver_checksum == 0x0000:
        print("✅ Checksum Validation: 0x0000")
        print("✅ No error detected. Data is valid.")
    else:
        print(f"❌ Checksum Validation: 0x{receiver_checksum:04X}")
        print("❌ Error detected! Data is corrupted.")

# ---------- Main Menu ----------
def main():
    random.seed(int(time.time()))
    while True:
        print("\n" + "=" * 50)
        print("🌐 Internet Checksum (Binary Input) Simulator 🌐")
        print("=" * 50)
        print("📜 Submitted to: Rashid Rasheed")
        print("📜 Course: Computer Networks")
        print("📜 Submitted by:")
        print("   - Muhammad Junaid (F2023266884)")
        print("   - Arsal Naveed (F2023266900)")
        print("📜 Section: V4")
        print("=" * 50)
        print("\n📌 Menu Options:")
        print("  1. 🔢 Enter binary data and calculate checksum")
        print("  2. 🚪 Exit")
        print("\n" + "=" * 50)
        choice = input("Choose an option (1 or 2): ")

        if choice == "1":
            binary_input = input("\nEnter binary string (only 0s and 1s, e.g., 0100100001100101):\n")

            if not all(c in '01' for c in binary_input):
                print("❌ Invalid binary input. Only 0s and 1s are allowed.")
                input("Press Enter to continue...")
                continue

            simulate_binary_transmission(binary_input)
            input("\nPress Enter to return to the main menu...")
        elif choice == "2":
            print("\n👋 Thank you for using the Internet Checksum Simulator. Goodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please select a valid option.")
            time.sleep(1)

if _name_ == "_main_":
    main()