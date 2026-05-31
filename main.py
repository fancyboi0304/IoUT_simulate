# ============================================
# Raspberry Pi Pico (MicroPython / Wokwi 可執行版)
#
# 功能：
# 1. 使用者自行輸入要傳送的訊息
# 2. XOR 加密（模擬 AES）
# 3. Hash 雜湊（模擬 SHA-256）
# 4. Packet 打包
# 5. 顯示完整傳輸流程
# ============================================

import time

XOR_KEY = 0x5A


# ============================================
# XOR 加密（模擬 AES）
# ============================================

def xor_encrypt(text, key):
    encrypted = []

    for ch in text:
        encrypted.append(chr(ord(ch) ^ key))

    return "".join(encrypted)


# ============================================
# HEX 顯示（方便展示）
# ============================================

def to_hex(text):
    hex_result = []

    for ch in text:
        hex_result.append("{:02X}".format(ord(ch)))

    return " ".join(hex_result)


# ============================================
# Hash（DJB2，模擬 SHA-256）
# ============================================

def calculate_hash(data):
    h = 5381

    for ch in data:
        h = ((h << 5) + h) + ord(ch)

    # 模擬 32-bit
    h = h & 0xFFFFFFFF

    return h


# ============================================
# 顯示完整封包流程
# ============================================

def process_message(user_message):
    # Step 1：原始訊息
    plaintext = user_message

    # Step 2：加密
    encrypted_data = xor_encrypt(plaintext, XOR_KEY)

    # Step 3：Hash
    hash_value = calculate_hash(encrypted_data)

    # ========================================
    # 格式化輸出（專題展示版）
    # ========================================

    print("\n==================================================")
    print("         SECURE MESSAGE TRANSMISSION")
    print("   Encryption + Hash + Packet Transmission Demo")
    print("==================================================")

    print("[ MODULE ] Raspberry Pi Pico Sender Node")
    print("[ STATUS ] ACTIVE")
    print("--------------------------------------------------")

    print("[ 1. ORIGINAL MESSAGE ]")
    print("PLAINTEXT : {}".format(plaintext))

    print("--------------------------------------------------")

    print("--------------------------------------------------")
    print("[ 2. ENCRYPTION LAYER (XOR) ]")
    print("CIPHER TEXT : {}".format(encrypted_data))
    print("CIPHER TEXT (HEX): {}".format(to_hex(encrypted_data)))
    print("--------------------------------------------------")

    print("[ 3. INTEGRITY CHECK (HASH) ]")
    print("HASH VALUE  : {}".format(hash_value))

    print("--------------------------------------------------")

    print("[ 4. PACKET STRUCTURE ]")
    print("FORMAT:")
    print("  [CIPHERTEXT] + [HASH]")
    print("PACKET DATA : {} | {}".format(
        encrypted_data,
        hash_value
    ))

    print("==================================================")
    print("MESSAGE ENCRYPTION COMPLETE")
    print("==================================================\n")


# ============================================
# Main Program
# ============================================

print("System Booting...")
time.sleep(2)
print("System Ready.\n")

while True:
    print("請輸入你要傳送的訊息：")

    try:
        user_input = input(">>> ")

        if user_input.strip() == "":
            print("訊息不能為空，請重新輸入。\n")
            continue

        process_message(user_input)

    except KeyboardInterrupt:
        print("\nSystem Stopped.")
        break

    except Exception as e:
        print("發生錯誤：", e)

    time.sleep(1)