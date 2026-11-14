# Báo cáo cá nhân — Day 06

**Trần Văn Quang · 2A202604032 · L3B**

**Xác nhận:** Trần Văn Quang đã đọc trực tiếp, duyệt thủ công các mẫu đánh giá và phê duyệt kết quả trong báo cáo. [Bản ghi phê duyệt](../../results/approval.json)

Cấu hình theo đoạn có filter chapter được chọn trên dev với Evidence Hit@3 đạt 11/15. Sau khi khóa cấu hình, cả 5 câu test đều có evidence đầy đủ ở top-1. Kết quả này áp dụng cho corpus và tập câu hỏi nhỏ của bài.

## Dữ liệu và pipeline

Corpus lấy sáu chương của Python Tutorial 3.13 gồm controlflow, datastructures, modules, inputoutput, errors và classes. Tổng cộng 155.554 ký tự nội dung được chia thành **59 đơn vị nguồn**, mỗi đơn vị từ 1.721 ký tự trở lên. Đây là đơn vị truy vết của HTML, không phải số trang PDF.

Bộ thu thập chỉ lấy phần thân tài liệu, bỏ điều hướng và dấu liên kết ở heading. Nội dung được chuẩn hóa NFC, dấu xuống dòng và khoảng trắng cuối dòng. Mỗi đơn vị gom các đoạn theo thứ tự nguồn đến ít nhất 2.500 ký tự; phần dư dưới 1.500 ký tự được nhập vào đơn vị trước. Không nhân bản nội dung để đủ số lượng. Manifest ghi số ký tự, đoạn đầu/cuối, số thứ tự và SHA-256 từng đơn vị. Bản HTML gốc cũng được lưu để kiểm lại. [Manifest](../../data/manifest.json)

Tài liệu dùng PSF License Version 2; ví dụ code còn được cấp phép theo 0BSD. Bản giấy phép đã được lưu cùng dữ liệu. Thay đổi so với nguồn là trích phần nội dung, chuẩn hóa và chia đơn vị. [Giấy phép](../../data/LICENSE-PYTHON.txt)

Pipeline đọc JSONL → tạo chunk → BGE embedding → Qdrant local → truy xuất top-3 → chấm evidence và xuất trace. Model là **BAAI/bge-small-en-v1.5**, bản quantized ONNX từ Qdrant, revision `aa8f8b060edb00e03bfdd08813a2949946c8ba55`, vector **384 chiều**, chạy bằng CPUExecutionProvider. FastEmbed 0.9.1 dùng trực tiếp văn bản cho query/passages của model này. Tên model, revision và checksum trọng số được giữ để tái lập. [Model](../../artifacts/model.json)

Store là Qdrant client 1.20.0 local persistent, tìm kiếm cosine exact. Model và vector được cache trên máy. Chi phí API là **0 USD**, chưa quy đổi điện, thời gian máy hoặc băng thông tải. Qdrant local dùng bộ lưu trữ riêng của thư viện. Chunk dài nhất của A có 243 token; B/C có 479 token, dưới giới hạn 512 của model nên không bị cắt khi tạo embedding. [Môi trường](../../results/environment.json) · [Kiểm dữ liệu và token](../../results/corpus_validation.json)

Metadata có `document_id`, `source`, `page`, `unit_id`, `chapter`, `version`, `language` và ranh giới ký tự. `page` là số thứ tự đơn vị trong chương. `chapter` được lấy từ trang nguồn và dùng làm filter khi câu hỏi nêu trước phạm vi. Điều kiện lọc được so chính xác với metadata; dữ liệu gold chỉ được đọc ở bước đánh giá. ID chunk có hash nội dung và ranh giới. Upsert giữ ID ổn định, nạp lại không trùng và xóa chunk không còn thuộc snapshot sau khi ghi thành công. [Mã lưu trữ](../../starter/src/store.py)

| Trường | Kiểu dữ liệu | Nguồn giá trị và mục đích |
|---|---|---|
| `document_id`, `source` | Chuỗi | ID chương trong manifest và URL gốc, dùng truy về tài liệu |
| `page` | Số nguyên | Số thứ tự đơn vị nội dung trong chương, bắt đầu từ 1 |
| `unit_id` | Chuỗi | Tên chương ghép số thứ tự, ví dụ `classes-009`, để tra đơn vị trong manifest |
| `chapter` | Chuỗi | Tên chương từ URL nguồn; có sáu giá trị phân biệt để lọc |
| `version` | Chuỗi | `3.13` từ đường dẫn tài liệu; không suy ra số bản vá |
| `language` | Chuỗi | `en`, ngôn ngữ của corpus Python Tutorial đã chọn |
| `start_char`, `end_char` | Số nguyên | Ranh giới trong text đơn vị đã chuẩn hóa, bắt đầu từ 0, gồm đầu và không gồm cuối |

## Cấu hình và benchmark

| Cấu hình | Tham số chunk | Metadata và truy xuất | Giả thuyết trước thử |
|---|---|---|---|
| A | Fixed 500 ký tự, overlap 50 | Cùng schema, không filter | Cửa sổ ngắn có thể cắt mất phần evidence |
| B | Theo đoạn, tối đa 1.000 ký tự, overlap 0 | Cùng schema, không filter | Ranh giới đoạn giữ ngữ cảnh tốt hơn |
| C | Giống B hoàn toàn | Chỉ bật filter chapter cho câu có ngữ cảnh chương | Giảm kết quả cùng thuật ngữ nhưng khác phạm vi |

A–B chỉ đổi chiến lược chunking. B–C dùng đúng cùng 201 chunk, model và metadata; chỉ khác filter lúc truy xuất. Với câu không yêu cầu filter, C thực hiện truy vấn giống B. [Kế hoạch thí nghiệm](../../benchmark/plan.json)

Benchmark có 20 câu tiếng Anh để phù hợp model và nguồn. q01–q15 thuộc dev, q16–q20 thuộc test. Năm câu test về classes được tách theo chủ đề trước truy xuất. Bốn câu nêu ngữ cảnh chapter là q10, q12, q15 và q18; trong đó q18 thuộc test. Mỗi câu có đáp án, document ID, đơn vị và trích dẫn đã đối chiếu với snapshot. Evidence của q09, q18, q19 được rút về câu đủ hỗ trợ đáp án trong lúc soạn, trước lượt dev đầu tiên. [Câu hỏi và gold](../../benchmark/questions.jsonl)

Ngữ cảnh chapter là input được cung cấp trước trong câu hỏi, không lấy từ gold để dựng filter. Các chương cùng thuộc Python Tutorial, dùng chung cách viết và thuật ngữ; chia theo chủ đề giúp giảm trùng nội dung nhưng chưa tạo được một tập kiểm tra độc lập về nguồn tài liệu.

Tiêu chí chọn được ghi trước khi đọc test, theo thứ tự ưu tiên **dev Evidence Hit@3 → dev Hit@1 → ít chunk hơn → thứ tự ID**. C được chọn trước test. Sau khi đã có test, thay đổi ở mã điều phối chỉ gồm tùy chọn thư mục output và chặn ghi đè để tái lập. Sau đó bổ sung thống kê tài nguyên từ chunk đã lưu, hồ sơ duyệt và kiểm tra đóng gói; không chỉnh retrieval, cấu hình, câu hỏi hay gold. Bản điều phối tại thời điểm test đầu được lưu kèm; lần tái lập dùng cùng cấu hình và tập đã xem, không được xem là holdout mới. [Lựa chọn](../../results/selection.json) · [Ghi nhận tái lập](../../results/runtime_provenance.json)

## Kết quả

Hit@1 là số câu có chunk hạng 1 thuộc gold source/unit và chứa đủ evidence đã khóa. Evidence Hit@3 là số câu có ít nhất một chunk như vậy trong top-3. So khớp chuẩn hóa khoảng trắng. Đây là metric tự động bảo thủ; đoạn đủ ý nhưng khác hoặc thiếu phần dẫn của gold có thể bị tính trượt.

| Strategy | Split | Hit@1 | Evidence Hit@3 | Số chunk | Ingest có cache | Chi phí API |
|---|---|---:|---:|---:|---:|---:|
| A | Dev | 6/15 (40,0%) | 8/15 (53,3%) | 362 | 2,64 giây | 0 USD |
| B | Dev | 7/15 (46,7%) | 10/15 (66,7%) | 201 | 1,71 giây | 0 USD |
| C | Dev | 8/15 (53,3%) | 11/15 (73,3%) | 201 | 1,72 giây | 0 USD |
| A | Test | 3/5 (60,0%) | 4/5 (80,0%) | 362 | Như dòng A ở trên | 0 USD |
| B | Test | 5/5 (100%) | 5/5 (100%) | 201 | Như dòng B ở trên | 0 USD |
| C | Test | 5/5 (100%) | 5/5 (100%) | 201 | Như dòng C ở trên | 0 USD |

Thời gian là một lượt nạp có vector cache, gồm đọc cache và upsert, chưa gồm lượt kiểm nạp lại. Entry point ban đầu vô tình chạy hai lần và ghi đè thời gian nạp đầu bằng thời gian có cache. Lỗi đã được sửa trước test; bảng trên giữ đúng số liệu còn lưu và không dùng nó để kết luận tốc độ tính embedding lần đầu. C tái sử dụng vector B. [Thống kê ingest](../../results/ingestion.json) · [CSV metric](../../results/metrics.csv)

### Độ dài chunk và lượng token

| Cấu hình | Ký tự min / median / P90 / max | Ký tự trung bình | Tổng ký tự | Token min / median / P90 / max | Tổng token |
|---|---|---:|---:|---|---:|
| A | 60 / 500 / 500 / 500 | 471,56 | 170.704 | 20 / 122 / 178 / 243 | 46.123 |
| B | 23 / 837 / 985 / 999 | 772,51 | 155.275 | 15 / 200 / 293 / 479 | 41.347 |
| C | 23 / 837 / 985 / 999 | 772,51 | 155.275 | 15 / 200 / 293 / 479 | 41.347 |

Token được đếm riêng cho từng chunk bằng tokenizer của đúng revision model, gồm special token, tắt padding và truncation. Không chunk nào vượt 512 token. Tổng token là lượng nội dung của mỗi cấu hình, có tính lặp do overlap và special token của từng chunk; không phải số token trả phí hoặc số token thực sự được tính lại ở lượt có cache. B/C có một số chunk ngắn ở ranh giới đoạn, vì vậy số lượng chunk ít hơn vẫn cần đi kèm kiểm tra coherence. Thống kê này được tính từ các chunk đã lưu sau thử nghiệm, không dùng để chỉnh cấu hình hay benchmark. [Thống kê đầy đủ](../../results/chunk_statistics.json)

### Năm khía cạnh đánh giá

| Cấu hình | Coherence /2, 10 mẫu | Metadata đúng và đủ, test top-3 | Đúng phạm vi filter dev | Đúng phạm vi filter test | Grounding 0/1/2 và trung bình |
|---|---:|---:|---:|---:|---|
| A | 1,00 | 15/15 | 2/3 | 0/1 | 0 / 0 / 5, trung bình 2,00 |
| B | 1,80 | 15/15 | 2/3 | 1/1 | 0 / 0 / 5, trung bình 2,00 |
| C | 1,80 | 15/15 | 3/3 | 1/1 | 0 / 0 / 5, trung bình 2,00 |

Coherence được chấm trên 10 vị trí nguồn cho mỗi cấu hình, tổng 30 mẫu. Grounding được chấm trên cùng 5 câu test cho mỗi cấu hình, tổng 15 trường hợp. Mỗi nhãn có điểm 0–2 và lý do; phần grounding kèm đoạn nguồn hỗ trợ. Điểm grounding đánh giá đủ bằng chứng trong top-3 để trả lời, không đánh giá câu trả lời của một chatbot. Phương pháp chấm được ghi ở cuối báo cáo. [Coherence](../../results/coherence_audit.jsonl) · [Grounding](../../results/grounding_audit.jsonl)

Lượt rà thứ hai giữ nguyên toàn bộ điểm, bổ sung đoạn nguồn hỗ trợ cho 15 nhãn grounding và đối chiếu lại 45 bản ghi metadata. [Kết quả rà nhãn](../../results/audit_review.json)

[Bảng chấm từng mẫu](../../results/review_sheet.md) tập hợp điểm, lý do, nội dung chunk và bằng chứng của toàn bộ 90 bản ghi để đối chiếu với hồ sơ gốc.

Mười vị trí coherence được chốt trước truy xuất, lấy đều theo thứ tự document ID và page. A chọn chunk bao phủ có offset đầu nhỏ nhất nếu hai chunk chồng nhau. B và C có cùng mẫu chunk. A thường dừng giữa từ, câu hoặc code. B giữ đoạn tốt hơn, nhưng s04 và s06 vẫn kết thúc bằng câu dẫn thiếu ví dụ tiếp theo nên chỉ đạt 1. [Vị trí mẫu](../../benchmark/coherence_positions.json)

Metadata được kiểm bằng script trên 5 câu test × 3 hạng × 3 cấu hình, tổng 45 bản ghi, rồi được tác giả đọc lại và xác nhận thủ công. Kiểm URL, unit, chapter/version/language và text đúng đoạn ký tự trong snapshot. C có 3/3 câu dev và 1/1 câu test tuân thủ ngữ cảnh lọc. A/B không bật filter, nên vẫn có kết quả ngoài phạm vi dù mọi trường metadata được ghi đúng. Số câu filter rất ít, chưa đủ để kết luận rộng. [Metadata audit](../../results/metadata_audit.jsonl) · [Tổng hợp](../../results/quality_summary.json)

## Phân tích và kết luận

**A–B.** Evidence Hit@3 dev tăng 8/15 → 10/15 và test tăng 4/5 → 5/5. Số chunk giảm từ 362 xuống 201, khoảng 44,5%. Coherence tăng 1,00 → 1,80 theo cách chấm đã mô tả. A chứa 170.704 ký tự qua các chunk vì overlap; B/C chứa 155.275 ký tự, không tính khoảng trắng bị bỏ ở ranh giới. Đổi lấy ít vector hơn là chunk dài hơn, có thể chứa nhiều ý hoặc thêm nhiễu.

**B–C.** Filter giúp q12 lấy được bằng chứng từ inputoutput thay vì các đoạn xử lý exception ở errors. Hit@3 dev tăng 10/15 → 11/15. Trên test, B và C đều 5/5 nên chưa có bằng chứng về mức tăng retrieval ở tập này. Filter hữu ích khi phạm vi được người dùng nêu đúng; phạm vi sai có thể loại mất evidence.

### Ví dụ lỗi

| Câu và cấu hình | Hiện tượng quan sát | Nguồn và bài học |
|---|---|---|
| q12, B | Top-3 đều ở chương errors dù hỏi việc đóng file trong inputoutput. C dùng ngữ cảnh chapter và lấy được evidence. | python313-inputoutput, unit 5. Filter sửa sai phạm vi giữa hai chương cùng nhắc exception. |
| q04, C | Top-3 ở các unit 9 và 11 nhưng thiếu gold tại unit 10. | python313-controlflow, unit 10. Filter cùng chương không sửa được thứ hạng bên trong chương. |
| q17, A | Metric exact quote tính trượt vì chunk mất câu mở đầu của gold; hạng 1 vẫn giữ câu giải thích tìm method trong chuỗi base class. | python313-classes, unit 9. Grounding được rà riêng là đủ ý. Đây là giới hạn của gold/so khớp tự động, không sửa gold sau khi xem test. |

[Trace và phân tích lỗi](../../results/failure_analysis.json)

Chọn **C** cho corpus này vì thắng theo quy tắc dev đã khóa, giữ đầy đủ metadata và có thể dùng ngữ cảnh chương sẵn có. Với câu không có ngữ cảnh đó, C trở về cách truy xuất của B. Có thể mở rộng bằng cách sửa gold tối thiểu, thêm câu hỏi khó và điều kiện, hoặc thử reranker trên một vòng thí nghiệm mới với test mới.

### Kiểm tra tái lập và giới hạn

- 60 lượt truy xuất gốc, mỗi lượt giữ đủ ba chunk, score, source, page, filter và nhãn hit.
- Nạp lại cùng snapshot giữ số point; xóa chunk cũ khi snapshot giảm; từ chối vector sai chiều; đóng rồi mở lại store vẫn đọc được.
- Rà ranh giới source và phủ toàn bộ ký tự có nội dung cho cả ba cách chia. B và C có cùng chunk, metadata.
- Lần tái lập cho cùng top-3, text, metadata, nhãn và metric. Chênh điểm cosine lớn nhất khoảng 7,01 × 10⁻⁸ do lưu vector float32, dưới ngưỡng kiểm 10⁻⁶.
- Trong setup có hai lỗi bảo vệ hash và nhận diện tên chapter, được sửa trước retrieval. Traceback được giữ trong log. [Log lỗi](../../results/error.log)
- Bộ test năm câu chỉ đại diện một phần classes. So khớp full quote có thể quá chặt; nhãn định tính phụ thuộc cách diễn giải tiêu chí và chưa được kiểm tra độ đồng thuận giữa những người chấm. Chưa chạy thử trên tài liệu tiếng Việt, PDF scan hay workload lớn.

[Kiểm tra kỹ thuật](../../results/verification.json)

## Công cụ và cách kiểm tra theo yêu cầu lab

Dùng ChatGPT/Codex để hỗ trợ hiện thực, viết câu hỏi từ nguồn và rà audit. Các metric định lượng được tính từ trace chạy bằng model và Qdrant thật. Phần chấm định tính ban đầu dùng ChatGPT/Codex đọc từng mẫu theo thang 0–2 của GUIDE, đối chiếu chunk với nguồn rồi ghi điểm và lý do. Lượt rà thứ hai kiểm lại nhãn và bổ sung trích dẫn cho từng trường hợp grounding. Sau đó, Trần Văn Quang trực tiếp đọc và duyệt thủ công 30 mẫu coherence, 15 trường hợp grounding và 45 bản ghi metadata, giữ nguyên các nhãn và kết quả. Bản ghi phê duyệt lưu xác nhận này; thông tin tạo nhãn ban đầu được giữ để truy vết. Đây là lượt tự rà của tác giả nên có thể có thiên lệch, chưa có người chấm độc lập. Metadata và số liệu cũng được đối chiếu bằng script. Lệnh tái lập nằm trong [README](../../README.md).
