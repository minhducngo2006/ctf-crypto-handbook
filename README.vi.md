# CTF Crypto Handbook — Hướng dẫn tiếng Việt

Đây là cẩm nang thực chiến dành cho **Crypto CTF trong phạm vi được cho phép**. Repo sử dụng quy trình dựa trên bằng chứng:

```text
artifact → phương trình chính xác → giả thuyết kiểm chứng được → solver tối thiểu → bằng chứng độc lập
```

## Cách sử dụng

1. Giữ nguyên file challenge gốc; đọc source hoặc transcript trước.
2. Làm theo [quy trình evidence-first](docs/00-evidence-first-workflow.md).
3. Chuẩn hóa encoding và mô hình toán bằng [Math & Encoding](docs/01-math-and-encoding.md).
4. Chọn đúng nhóm kỹ thuật trong bảng dưới.
5. Sao chép [`templates/solve.py`](templates/solve.py) hoặc [`templates/solve.sage`](templates/solve.sage).
6. Ghi FACT, INFERENCE, HYPOTHESIS và kết quả test vào [`templates/solve_log.md`](templates/solve_log.md).
7. Chỉ kết luận đã solve sau khi mọi phép kiểm chứng phù hợp đều thành công.

## Chọn hướng phân tích

| Dấu hiệu | Kiểm tra đầu tiên | Tài liệu |
|---|---|---|
| Cipher cổ điển, alphabet lạ, Base encoding | Giữ nguyên alphabet/byte; thử phép biến đổi trực tiếp | [Classical, XOR & Stream](docs/02-classical-xor-stream.md) |
| XOR, keystream, recurrence tuyến tính | Căn chỉnh byte; khai thác known plaintext hoặc quan hệ đại số | [Classical, XOR & Stream](docs/02-classical-xor-stream.md) |
| Block 16 byte, IV/nonce/tag | Xác định mode và cách serialize trước | [Block Cipher](docs/03-block-ciphers.md) |
| `n`, `e`, `c`, PEM, nhiều modulus | Kiểm tra range, GCD giữa modulus được cung cấp, exact root | [RSA](docs/04-rsa.md) |
| Curve point, `(r,s)`, nonce/commitment | Xác thực group và kiểm tra nonce/transcript reuse có bằng chứng | [ECC & Signature](docs/05-ecc-signatures.md) |
| Hash, MAC, CRC, checksum | Dựng lại message framing và domain separation | [Hash, MAC & PRNG](docs/06-hash-mac-prng.md) |
| Chuỗi output giả ngẫu nhiên | Viết đúng recurrence; tái tạo toàn bộ output đã quan sát | [Hash, MAC & PRNG](docs/06-hash-mac-prng.md) |
| Modular equation có sai số nhỏ, proof verifier | Xác định bounds/dimensions hoặc constraint thực sự được kiểm tra | [Lattice, LWE & ZKP](docs/07-lattices-lwe-zkp.md) |

## Checklist bắt buộc

- Parser tái tạo đúng public input từng byte.
- Giá trị suy ra thỏa mọi phương trình, giới hạn và điều kiện ban đầu.
- Có phép nghịch đảo, sample giữ lại, implementation thứ hai hoặc verifier xác nhận.
- Plaintext/flag đúng encoding và format mà đề bài mô tả.
- Không dùng “thấy chữ đọc được” làm bằng chứng duy nhất.

## Nguyên tắc an toàn

- Chỉ sử dụng trong CTF, lab hoặc hệ thống được cấp quyền rõ ràng.
- Không mở rộng sang host, endpoint, account hoặc service ngoài scope.
- Không commit token, cookie, credential, private key hoặc dữ liệu không liên quan.
- Không chạy file/package lạ chỉ vì nó có đuôi `.py`, `.sage` hoặc `.sh`.
- Ưu tiên mô hình toán và test xác định; tránh brute force, wordlist và attack-all.

Phần kỹ thuật sử dụng tiếng Anh để giữ nguyên thuật ngữ phổ biến trong tài liệu và công cụ CTF. Quay lại [README chính](README.md).
