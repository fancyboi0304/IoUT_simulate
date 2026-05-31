import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# =====================================
# 1. 原始共享金鑰（由 Saber KEM 產生）
# =====================================
shared_secret = b"this_is_shared_secret_32bytes!!"

# =====================================
# 2. 由 shared secret 產生 AES Key
# =====================================
# 使用 SHA-256 後取前 16 bytes 作為 AES-128 金鑰
aes_key = hashlib.sha256(shared_secret).digest()[:16]

# =====================================
# 3. 使用者輸入密文、Hash、IV
# =====================================
print("===== 密文完整性驗證與解密系統 =====")

ciphertext_hex = input("請輸入密文（Hex 格式）: ")
received_hash = input("請輸入接收到的 SHA-256 Hash 值: ")
iv_input = input("請輸入 IV（16字元，例如 1234567890abcdef）: ")

try:
    ciphertext = bytes.fromhex(ciphertext_hex)
    iv = iv_input.encode("utf-8")

    if len(iv) != 16:
        print("錯誤：IV 必須剛好為 16 bytes")
        exit()

except Exception as e:
    print("輸入格式錯誤：", str(e))
    exit()

# =====================================
# 4. 重新計算 Hash 驗證完整性
# =====================================
calculated_hash = hashlib.sha256(ciphertext).hexdigest()

print("\n===== Hash Verification =====")
print("接收到的 Hash值 :", received_hash)
print("重新計算的 Hash :", calculated_hash)

if calculated_hash == received_hash:
    print("\n完整性驗證成功，開始進行解密...\n")

    try:
        # =====================================
        # 5. AES 解密
        # =====================================
        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)

        print("===== 解密成功 =====")
        print("原始資料：")
        print(decrypted_data.decode("utf-8"))

    except Exception as e:
        print("解密失敗：", str(e))

else:
    print("\n===== 驗證失敗 =====")
    print("密文可能遭到竄改，停止解密。")