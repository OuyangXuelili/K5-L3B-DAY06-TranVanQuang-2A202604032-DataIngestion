# Đối chiếu rubric — Day 06

**Trần Văn Quang · 2A202604032 · L3B**

Bảng này dẫn bằng chứng cho từng tiêu chí trong [RUBRIC](../RUBRIC.md). Cột điểm ghi mức tối đa của đề, chưa phải điểm được giảng viên chấm.

| Tiêu chí | Điểm tối đa | Bằng chứng trong bài |
|---|---:|---|
| Corpus hợp lệ và quyền xử lý | 8 | [Manifest](../data/manifest.json): 59 đơn vị HTML, mỗi đơn vị ít nhất 1.721 ký tự theo quy tắc của GUIDE; sáu nguồn có snapshot và [giấy phép](../data/LICENSE-PYTHON.txt) |
| Đọc, chuẩn hóa, ghi lỗi và truy vết | 12 | [Ingestion](../starter/src/ingestion.py), [bộ chuẩn bị corpus](../starter/scripts/prepare_corpus.py), [kiểm corpus](../results/corpus_validation.json), [log lỗi](../results/error.log); chunk có ID nguồn, đơn vị và offset |
| Ba cấu hình chạy được và ghi tham số | 8 | [Kế hoạch A/B/C](../benchmark/plan.json), [experiment log](../artifacts/experiment_log.csv), [trace dev](../results/traces_dev.jsonl) và [test](../results/traces_test.jsonl) |
| So sánh có kiểm soát | 6 | A–B đổi chunking; B–C giữ đúng cùng chunk và chỉ đổi filter; [kiểm tra](../results/verification.json) xác nhận B/C giống dữ liệu |
| Model thật, vector store và nạp lại | 6 | [Model, revision và checksum](../artifacts/model.json); [Qdrant local](../starter/src/store.py) có tìm kiếm cosine, lưu bền vững và metadata filter; [kiểm tra](../results/verification.json) xác nhận nạp không trùng, xóa chunk cũ, mở lại store |
| Benchmark, evidence, filter và dev/test | 10 | [20 câu hỏi](../benchmark/questions.jsonl), 15 dev/5 test; bốn câu filter, một câu thuộc test; evidence đối chiếu nguồn; [kế hoạch khóa trước thử nghiệm](../benchmark/plan.json) và [lựa chọn trước test](../results/selection.json) |
| Trace và Hit@1/Hit@3 đủ ba cấu hình | 10 | 60 lượt truy xuất, mỗi lượt top-3; [metric dev](../results/metrics_dev.json), [metric test](../results/metrics_test.json) và [CSV](../results/metrics.csv); phép tính được kiểm lại từ trace |
| Retrieval accuracy | 5 | [Báo cáo](individual/2A202604032_TranVanQuang.md) ghi tử/mẫu và định nghĩa so khớp; [phân tích lỗi](../results/failure_analysis.json) nêu cả trường hợp exact quote bỏ sót bằng chứng đủ ý |
| Coherence có nhãn | 5 | [30 nhãn](../results/coherence_audit.jsonl), cùng [10 vị trí](../benchmark/coherence_positions.json) cho ba cấu hình, có điểm 0–2, lý do và trung bình; tác giả đã xác nhận đọc trực tiếp |
| Metadata đủ, đúng và hữu dụng | 5 | [45 bản ghi](../results/metadata_audit.jsonl) được kiểm nguồn và tác giả duyệt; [tổng hợp](../results/quality_summary.json) ghi riêng tỷ lệ tuân thủ filter dev/test; báo cáo giải thích ích lợi và giới hạn |
| Grounding thủ công | 5 | [15 nhãn grounding](../results/grounding_audit.jsonl), năm câu test mỗi cấu hình, thang 0–2, lý do, trích dẫn và phân bố điểm; [xác nhận duyệt thủ công của tác giả](../results/approval.json) |
| Tác động chiến lược và đánh đổi | 5 | [Báo cáo](individual/2A202604032_TranVanQuang.md) so A–B, B–C và giải thích q12, q04, q17; [thống kê chunk/token](../results/chunk_statistics.json), ingest có cache, chi phí, hạn chế và tiêu chí chọn C |
| Tái lập, model, chi phí và artifacts | 8 | [README](../README.md) có lệnh setup/run/verify; [requirements.lock](../requirements.lock), [model](../artifacts/model.json), [môi trường](../results/environment.json), [ghi nhận tái lập](../results/runtime_provenance.json); [.gitattributes](../.gitattributes) và [kiểm tra đóng gói](../results/packaging_verification.json) bảo toàn byte các đầu vào có checksum |
| Kết luận, ví dụ lỗi, giới hạn và trình bày | 7 | [Báo cáo cá nhân](individual/2A202604032_TranVanQuang.md) có ba ví dụ lỗi, lựa chọn theo dev, điều kiện dùng filter, giới hạn test/nhãn/thời gian; [bảng chấm](../results/review_sheet.md) trình bày từng mẫu |
| **Tổng thang điểm** | **100** | **Có bằng chứng cho cả năm nhóm tiêu chí.** |

Các giới hạn cần giữ khi giải thích bài: test chỉ có năm câu thuộc classes; các chương vẫn chung một nguồn Python Tutorial; thời gian ingest còn lưu là lượt có cache; grounding đánh giá evidence thay vì độ chính xác câu trả lời chatbot; lượt duyệt của tác giả chưa phải chấm độc lập. Các giới hạn này đã được nêu trong báo cáo, không sửa gold hoặc thay kết quả để làm đẹp điểm.

Hybrid retrieval là phần tùy chọn trong GUIDE. Bài không cần bổ sung hybrid để đáp ứng các tiêu chí bắt buộc. Việc công bố repo và nộp link theo kênh của lớp vẫn là bước riêng sau khi chốt nội dung.
