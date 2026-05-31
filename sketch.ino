#include <WiFi.h>
#include <string.h>
#include "mbedtls/sha256.h"
#include "mbedtls/aes.h"

const char* ssid = "Wokwi-GUEST";
const char* password = "";

// ===== 全域 =====
static uint8_t serverPublicKey[32];
static uint8_t signature[32];
static uint8_t verify_buf[32];
static uint8_t sharedSecret[32];

static uint8_t encryptedData[32];
static uint8_t decryptedData[32];

// 模擬 private key（固定）
static uint8_t fake_sk[32] = "SERVER_PRIVATE_KEY_123456";

// ===== Server: 產生身份 + 簽章 =====
void server_generate_identity() {
  for (int i = 0; i < 32; i++) {
    serverPublicKey[i] = random(0, 256);
  }

  // signature = H(pk || sk)
  mbedtls_sha256(serverPublicKey, 32, signature, 0);
  mbedtls_sha256_context ctx;
  mbedtls_sha256_init(&ctx);
  mbedtls_sha256_starts(&ctx, 0);

  mbedtls_sha256_update(&ctx, serverPublicKey, 32);
  mbedtls_sha256_update(&ctx, fake_sk, 32);

  mbedtls_sha256_finish(&ctx, signature);
  mbedtls_sha256_free(&ctx);
}

// ===== Client: 驗證（模擬 Dilithium）=====
bool verify_server() {
  mbedtls_sha256(serverPublicKey, 32, verify_buf, 0);
  mbedtls_sha256_context ctx;
  mbedtls_sha256_init(&ctx);
  mbedtls_sha256_starts(&ctx, 0);

  mbedtls_sha256_update(&ctx, serverPublicKey, 32);
  mbedtls_sha256_update(&ctx, fake_sk, 32);

  mbedtls_sha256_finish(&ctx, verify_buf);
  mbedtls_sha256_free(&ctx);

  return memcmp(verify_buf, signature, 32) == 0;
}

// ===== 模擬 Saber KEM =====
void saber_key_exchange() {
  uint8_t ct[32];

  // 模擬 ciphertext
  for (int i = 0; i < 32; i++) {
    ct[i] = random(0, 256);
  }

  // sharedSecret = H(ct)
  mbedtls_sha256(ct, 32, sharedSecret, 0);
}

// ===== AES 加密 =====
void encrypt_data(uint8_t *input) {
  mbedtls_aes_context aes;
  mbedtls_aes_init(&aes);

  mbedtls_aes_setkey_enc(&aes, sharedSecret, 256);
  mbedtls_aes_crypt_ecb(&aes, MBEDTLS_AES_ENCRYPT, input, encryptedData);

  mbedtls_aes_free(&aes);
}

// ===== AES 解密 =====
void decrypt_data() {
  mbedtls_aes_context aes;
  mbedtls_aes_init(&aes);

  mbedtls_aes_setkey_dec(&aes, sharedSecret, 256);
  mbedtls_aes_crypt_ecb(&aes, MBEDTLS_AES_DECRYPT, encryptedData, decryptedData);

  mbedtls_aes_free(&aes);
}

// ===== print hex =====
void print_hex(uint8_t *data, int len) {
  for (int i = 0; i < len; i++) {
    Serial.printf("%02X", data[i]);
  }
  Serial.println();
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  randomSeed(esp_random());

  // ===== WiFi =====
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(200);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");

  // ===== Step 1: Server Identity =====
  Serial.println("Server generating identity...");
  server_generate_identity();

  // ===== Step 2: 驗證 =====
  Serial.println("Verifying Server (Simulated Dilithium)...");
  if (verify_server()) {
    Serial.println("✔ AUTH SUCCESS");
  } else {
    Serial.println("✖ AUTH FAIL");
    return;
  }

  // ===== Step 3: Saber =====
  Serial.println("Running Simulated Saber KEM...");
  saber_key_exchange();

  Serial.println("Shared Secret:");
  print_hex(sharedSecret, 32);

  // ===== Step 4: 加密 =====
  uint8_t message[32] = {0};
  strcpy((char*)message, "Post-Quantum IoT");

  Serial.println("Original:");
  Serial.println((char*)message);

  encrypt_data(message);

  Serial.println("Encrypted:");
  print_hex(encryptedData, 16); // AES block size = 16 bytes

  decrypt_data();

  Serial.println("Decrypted:");
  print_hex(decryptedData, 16);
}

void loop() {}