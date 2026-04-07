import logging
from datetime import datetime

# --- CẤU HÌNH LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test_results.log", encoding="utf-8"), # Ghi vào file
        logging.StreamHandler() # Vẫn hiển thị ra console để tiện theo dõi
    ]
)
logger = logging.getLogger("TravelBuddy")

# ---TEST CASES ---
test_cases = [
    {
        "id": "Test 1",
        "name": "Direct Answer",
        "desc": "Agent chào hỏi, hỏi thêm về sở thích/ngân sách/thời gian. Không gọi tool nào.",
        "input": "Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu."
    },
    {
        "id": "Test 2",
        "name": "Single Tool Call",
        "desc": "Gọi search_flights('Hà Nội', 'Đà Nẵng'), liệt kê 4 chuyến bay.",
        "input": "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng"
    },
    {
        "id": "Test 3",
        "name": "Multi-Step Tool Chaining",
        "desc": "Agent tự chuỗi nhiều bước: 1. search_flights -> 2. search_hotels -> 3. calculate_budget. Tổng hợp thành gợi ý với bảng chi phí.",
        "input": "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!"
    },
    {
        "id": "Test 4",
        "name": "Missing Info",
        "desc": "Agent hỏi lại: thành phố nào? bao nhiêu đêm? ngân sách bao nhiêu? Không gọi tool vội.",
        "input": "Tôi muốn đặt khách sạn"
    },
    {
        "id": "Test 5",
        "name": "Guardrail",
        "desc": "Từ chối lịch sự, nói rằng chỉ hỗ trợ về du lịch.",
        "input": "Giải giúp tôi bài tập lập trình Python về linked list"
    }
]
def run_automated_tests(graph_instance):
    logger.info("="*80)
    logger.info(f"{'BẮT ĐẦU KIỂM THỬ HỆ THỐNG TRAVELBUDDY':^80}")
    logger.info("="*80)

    for case in test_cases:
        logger.info(f"▶️ [{case['id']}] {case['name']}")
        logger.info(f"   Mô tả kỳ vọng: {case['desc']}")
        logger.info(f"   User Input   : {case['input']}")
        
        try:
            # Thực thi graph
            result = graph_instance.invoke({"messages": [("human", case['input'])]})
            
            # Lấy phản hồi cuối cùng
            final_response = result["messages"][-1].content
            
            logger.info(f"   ✅ KẾT QUẢ: {final_response}")
        except Exception as e:
            logger.error(f"   ❌ LỖI KHI THỰC THI: {str(e)}")
            
        logger.info("-" * 80)

    logger.info("KIỂM THỬ HOÀN TẤT. Vui lòng kiểm tra file 'test_results.log'.")