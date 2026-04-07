
## Giải thích bổ sung (dành cho người viết prompt):
1. Thân thiện & gần gũi: Giữ persona "như một người bạn đi du lịch nhiều" để câu trả lời tự nhiên, ấm áp, không máy móc.
2. Chủ động tool chaining: Đây là yêu cầu cốt lõi của test case. Khi người dùng cung cấp đủ 4 thông tin (điểm khởi hành + điểm đến + số đêm + ngân sách), agent phải tự động gọi chuỗi tool theo thứ tự search_flights → search_hotels → calculate_budget mà không hỏi thêm thông tin ở lượt đầu.
3. Ưu tiên tuyệt đối cho golden rule: Đã đặt rule "Ưu tiên tuyệt đối" ở vị trí cao nhất để khắc phục mâu thuẫn trước đây giữa "hỏi nếu thiếu thông tin" và "phải gọi tool ngay". Rule này ghi đè lên các quy tắc cũ, buộc agent hành động trước khi trò chuyện.
4. Xử lý thông tin thiếu: Cho phép agent tự chọn ngày khởi hành gần nhất hợp lý (hôm nay + 10 ngày) và ước lượng max_price_per_night dựa trên ngân sách, thay vì hỏi ngay. Chỉ hỏi thêm (ngày chính xác, số người, sở thích…) sau khi đã có kết quả tool.
5. Không bịa thông tin & bắt buộc dùng tool: Tất cả giá vé, giá phòng, chi phí đều phải đến từ tool. Không được tự đưa ra bất kỳ con số nào.
6. Cấu trúc suy nghĩ (CoT): Thêm hướng dẫn suy nghĩ nội bộ theo 4 bước rõ ràng trước khi quyết định output, giúp agent nhất quán trong việc nhận diện và thực hiện tool chaining.
7. Response format & constraints: Đảm bảo khi đã có dữ liệu từ tool thì phải trả lời đúng format quy định, đồng thời cấm output text bình thường khi đang ở giai đoạn cần gọi tool.
Mục tiêu tổng thể:
- Agent phải pass được test case Multi-Step Tool Chaining (tự gọi 3 tool khi có đủ điều kiện).
- Vẫn giữ được tính thân thiện, gần gũi như người bạn.
- Tránh tình trạng hỏi thông tin quá sớm hoặc trả lời chung chung.
- Đảm bảo tính chính xác và an toàn (không bịa giá, không cam kết đặt vé).