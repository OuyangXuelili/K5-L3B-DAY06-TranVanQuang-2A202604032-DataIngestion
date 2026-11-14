# Pipeline local — BGE và Qdrant

Các hàm trong `src/` đã được hiện thực. Xem [README ở gốc repo](../README.md) để cài môi trường và chạy.

```powershell
cd starter
..\.venv\Scripts\python.exe -m src.run --output-dir results/another-run
```

Các stage là `ingest`, `dev`, `test` và mặc định `all`. Khi tách stage, dùng cùng `--output-dir`. Cấu hình được khóa vào `selection.json` sau dev. Stage test kiểm fingerprint của benchmark, corpus và mã pipeline trước khi truy xuất.

- `ingestion.py` đọc PDF hoặc JSONL, chuẩn hóa Unicode và kiểm đơn vị nguồn.
- `chunking.py` giữ nguồn, trang, ranh giới ký tự và ID theo nội dung.
- `embeddings.py` dùng BGE quantized ONNX revision cố định, cache theo nội dung.
- `store.py` dùng Qdrant local lưu bền vững. Chỉ xóa chunk cũ sau khi upsert snapshot mới thành công.
- `evaluation.py` chấm full evidence trong một chunk và chấp nhận danh sách gold thay thế nếu benchmark khai báo.
- `run.py` lưu index, trace, metric, lựa chọn dev và mẫu audit.

Các file Docker, SQL, `scripts/check_setup.py` và `.env.example` là phương án PostgreSQL gốc để tham khảo. Bài này dùng Qdrant, nên các lệnh chạy ở trên không cần PostgreSQL. Nếu muốn dùng riêng tiện ích kiểm PostgreSQL, cài thêm `psycopg[binary]` và `python-dotenv`.
