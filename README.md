# Day 06 — Data Ingestion Engineering

Pipeline truy xuất Python Tutorial 3.13 bằng BGE chạy CPU và Qdrant local. Corpus gồm **59 đơn vị nội dung** từ sáu chương, mỗi đơn vị tối thiểu 1.721 ký tự. Cấu hình C được chọn bằng 15 câu dev, sau đó đánh giá trên 5 câu test đã tách theo chủ đề classes.

| Cấu hình | Chunk | Filter | Dev Hit@1 | Dev Evidence Hit@3 | Test Hit@1 | Test Evidence Hit@3 |
|---|---|---|---:|---:|---:|---:|
| A | 500 ký tự, overlap 50 | Không | 6/15 | 8/15 | 3/5 | 4/5 |
| B | Theo đoạn, tối đa 1.000 ký tự | Không | 7/15 | 10/15 | 5/5 | 5/5 |
| C | Giống B | Chapter nếu câu hỏi nêu trước | 8/15 | 11/15 | 5/5 | 5/5 |

## Cài và chạy trên Windows

Cần Python 3.13 và mạng cho lần tải thư viện, model đầu tiên. Chạy từ thư mục gốc repo.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.lock
$env:PYTHONUTF8 = "1"
$env:HF_HUB_DISABLE_SYMLINKS_WARNING = "1"
cd starter
..\.venv\Scripts\python.exe -m src.run --output-dir results/reproduced
cd ..
.\.venv\Scripts\python.exe starter/scripts/verify_results.py
.\.venv\Scripts\python.exe starter/scripts/measure_chunks.py
```

Chọn một tên output mới ở mỗi lần chạy. Pipeline bảo vệ kết quả test đã lưu. Đường dẫn output được tính từ gốc repo dù lệnh chạy ở `starter/`. Qdrant lưu trên đĩa trong thư mục output, không cần Docker hoặc API key. Lệnh `verify_results.py` đối chiếu bộ kết quả gốc kèm repo.

Giữ file `.gitattributes` khi clone để Git bảo toàn byte của mã nguồn và dữ liệu đã khóa, tránh lệch checksum do đổi LF/CRLF. Lệnh `measure_chunks.py` dùng tokenizer đã tải ở bước chạy pipeline để đo lại các chunk gốc kèm repo.

Corpus và benchmark đã kèm bản snapshot để tái lập. Chỉ dùng các lệnh sau trong một checkout chưa có `data/pages.jsonl` hoặc chưa có benchmark nếu cần chuẩn bị lại dữ liệu. Trang web có thể thay đổi, vì vậy dùng bản kèm repo để đối chiếu đúng lần đo.

```powershell
.\.venv\Scripts\python.exe starter/scripts/prepare_corpus.py
.\.venv\Scripts\python.exe starter/scripts/prepare_benchmark.py
```

## Các đầu ra cần xem

- [Báo cáo cá nhân](report/individual/2A202604032_TranVanQuang.md) có phương pháp, năm khía cạnh, lỗi và giới hạn.
- [Đối chiếu rubric](report/rubric_check.md) dẫn bằng chứng cho từng tiêu chí của thang 100 điểm.
- [Manifest](data/manifest.json) ghi nguồn, quyền, ngày lấy, ranh giới đơn vị và SHA-256. [Giấy phép Python](data/LICENSE-PYTHON.txt) được giữ cùng corpus.
- [Benchmark](benchmark/questions.jsonl) gồm 20 câu với evidence. [Kế hoạch khóa trước thử nghiệm](benchmark/plan.json) ghi split, cấu hình và cách chọn.
- [Nhật ký thí nghiệm](artifacts/experiment_log.csv), [model và checksum](artifacts/model.json), [môi trường chạy](results/environment.json).
- [Dev traces](results/traces_dev.jsonl), [test traces](results/traces_test.jsonl), [bảng metric](results/metrics.csv), [lựa chọn trước test](results/selection.json).
- [Coherence](results/coherence_audit.jsonl), [grounding](results/grounding_audit.jsonl), [metadata audit](results/metadata_audit.jsonl) và [tổng hợp chất lượng](results/quality_summary.json).
- [Bảng chấm dễ đọc](results/review_sheet.md) tập hợp điểm, lý do, chunk và bằng chứng của toàn bộ 90 bản ghi.
- [Xác nhận phê duyệt kết quả của Trần Văn Quang](results/approval.json).
- [Kiểm tra kỹ thuật](results/verification.json), [đóng gói Git](results/packaging_verification.json), [ví dụ lỗi](results/failure_analysis.json) và [ghi nhận tái lập](results/runtime_provenance.json).
- [Phân bố độ dài chunk và tổng token](results/chunk_statistics.json), tính bằng tokenizer của model đã khóa.

## Phạm vi kiểm tra

Đã chạy 60 lượt truy xuất và kiểm top-3, metric, filter, nạp lại không trùng, xóa chunk cũ và mở lại dữ liệu đã lưu. Đã rà 30 mẫu coherence, 15 trường hợp grounding và đối chiếu 45 bản ghi metadata với snapshot. Nhãn, lý do và đoạn nguồn hỗ trợ được lưu trong các file audit; phương pháp chấm và giới hạn được ghi trong [báo cáo](report/individual/2A202604032_TranVanQuang.md#công-cụ-và-cách-kiểm-tra-theo-yêu-cầu-lab).

Trần Văn Quang đã trực tiếp đọc và duyệt thủ công toàn bộ 90 bản ghi, xác nhận giữ nguyên các nhãn và kết quả. Thông tin người duyệt được lưu trong các file audit và [bản ghi phê duyệt](results/approval.json).

Chi phí API là 0 USD. Thời gian ingest trong bảng kết quả là lượt có cache, không đại diện chi phí tính embedding lần đầu. Test chỉ có năm câu thuộc chương classes, nên kết quả 5/5 không đủ để kết luận cho toàn bộ tài liệu Python.

## Tài liệu đề bài

[GUIDE](GUIDE.md) · [BENCHMARK](BENCHMARK.md) · [RUBRIC](RUBRIC.md) · [RULES](RULES.md) · [SUBMISSION](SUBMISSION.md)
