# TravelBuddy - AI Travel Planning Assistant

🤖 Một trợ lý du lịch thông minh sử dụng AI để lập kế hoạch chuyến du lịch tối ưu theo ngân sách của bạn.

## 📋 Mô Tả Dự Án

**TravelBuddy** là một agent AI được xây dựng trên nền tảng **LangGraph** và **LangChain**, hỗ trợ người dùng lập kế hoạch du lịch tại Việt Nam một cách thông minh. Agent này có khả năng:

- 💰 Tìm kiếm chuyến bay giữa các thành phố
- 🏨 Tìm kiếm khách sạn phù hợp với ngân sách
- 📊 Tính toán và tối ưu hóa chi phí chuyến đi
- 💬 Tương tác tự nhiên bằng tiếng Việt

Agent được thiết kế để **tự động chuỗi các công cụ** (tool chaining) khi nhận được đủ thông tin từ người dùng (điểm khởi hành, điểm đến, số đêm, ngân sách).

## 🎯 Tính Năng Chính

### 1. **Search Flights** ✈️
   - Tìm kiếm chuyến bay giữa 2 thành phố
   - Hiển thị hãng hàng không, giờ cất/hạ cánh, giá vé
   - Hỗ trợ các hạng vé: Economy, Business

### 2. **Search Hotels** 🏨
   - Tìm kiếm khách sạn tại thành phố đích
   - Lọc theo mức giá và số sao
   - Hiển thị khu vực, đánh giá

### 3. **Calculate Budget** 💸
   - Tính toán tổng chi phí chuyến đi
   - Phân bổ ngân sách theo từng hạng mục
   - Đưa ra tư vấn tối ưu hóa chi phí

## 🚀 Cách Sử Dụng

### Cài Đặt

1. **Clone hoặc tải dự án**
   ```bash
   cd 2A202600443_Lab4
   ```

2. **Tạo virtual environment (tùy chọn)**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Cài đặt dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Cấu hình biến môi trường**
   
   Tạo file `.env` trong thư mục gốc dự án:
   ```env
   OLLAMA_BASE_URL=https://kelkoo-her-murphy-rank.trycloudflare.com/v1
   MODEL_NAME=llama3.1:8b
   OLLAMA_API_KEY=your_api_key_here
   ```

### Chạy Agent

```bash
python agent.py
```

### Chạy Test Tự Động

```bash
python test_auto.py
```

### Kiểm Tra Kết Nối API

```bash
python test_api.py
```

## 📁 Cấu Trúc Dự Án

```
.
├── agent.py                 # Main agent logic - LangGraph workflow
├── tools.py                 # Các công cụ: search_flights, search_hotels, calculate_budget
├── system_prompt.txt        # System prompt hướng dẫn hành vi của agent
├── test_auto.py             # Test cases tự động
├── test_api.py              # Test kết nối API OLLAMA
├── requirements.txt         # Dependencies
└── README.md                # File này
```

## 🔧 Dependencies

- **langchain** - Framework xây dựng LLM applications
- **langchain-openai** - OpenAI API client
- **langgraph** - Framework xây dựng agentic workflows
- **python-dotenv** - Quản lý biến môi trường
- **openai** - OpenAI API library

Xem file `requirements.txt` để chi tiết phiên bản.

## 📌 Các Thành Phố Được Hỗ Trợ

### Routes (Tuyến bay)
- Hà Nội → Đà Nẵng
- Hà Nội → Phú Quốc
- Hà Nội → Hồ Chí Minh
- Hồ Chí Minh → Đà Nẵng
- Hồ Chí Minh → Phú Quốc

### Địa Điểm Ở
- **Đà Nẵng** - Bãi biển, miền Trung
- **Phú Quốc** - Hòn đảo, du lịch biển
- **Hồ Chí Minh** - Thành phố lớn

## 💡 Ví Dụ Sử Dụng

### Ví dụ 1: Hỏi Thông Thường
```
User: "Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu."
Agent: [Hỏi thêm về sở thích, ngân sách, thời gian - Không gọi tool]
```

### Ví dụ 2: Tìm Chuyến Bay (Single Tool)
```
User: "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng"
Agent: [Gọi search_flights] → Liệt kê 4 chuyến bay
```

### Ví dụ 3: Lập Kế Hoạch Hoàn Chỉnh (Tool Chaining)
```
User: "Tôi muốn đi Đà Nẵng từ Hà Nội, ở 3 đêm, ngân sách 10 triệu đồng"
Agent: 
  1. search_flights(Hà Nội → Đà Nẵng)
  2. search_hotels(Đà Nẵng, max_price ≈ 2 triệu/đêm)
  3. calculate_budget → Trả về kế hoạch chi tiết
```

## 🧪 Testing

### Test Cases Bao Gồm:

1. **Test 1** - Direct Answer (Hỏi thêm, không gọi tool)
2. **Test 2** - Single Tool Call (Tìm chuyến bay)
3. **Test 3+** - Multi-tool chaining scenarios

Chạy test:
```bash
python test_auto.py
```

Kết quả test được lưu vào:
- **Console** - Hiển thị trực tiếp
- **travel_buddy_debug.log** - Lưu chi tiết vào file log

## 🔐 Biến Môi Trường

| Biến | Mô Tả | Giá Trị Mặc Định |
|------|-------|-------------------|
| `OLLAMA_BASE_URL` | Endpoint của OLLAMA/LLM server | `https://kelkoo-her-murphy-rank.trycloudflare.com/v1` |
| `MODEL_NAME` | Tên model LLM | `llama3.1:8b` |
| `OLLAMA_API_KEY` | API key cho LLM | Bắt buộc |

## 📊 Data Mô Phỏng

Dự án sử dụng dữ liệu mock (giả lập) để kiểm thử:

- ✈️ **Hãng hàng không**: Vietnam Airlines, VietJet Air, Bamboo Airways
- 🏨 **Loại khách sạn**: 5 sao tới 2 sao (homestay, hostel)
- 💰 **Giá cả**: Thực tế, có logic (cuối tuần đắt hơn, hạng cao hơn đắt hơn)

**Lưu ý:** Sinh viên cần đọc hiểu data trong `tools.py` để debug test cases.

## ⚙️ Cách Hoạt Động

### Workflow (LangGraph)

```
[User Input] → [Agent Node] → [LLM + Tools] → [Tool Execution] → [Response]
                     ↓
              [System Prompt]
```

1. **System Prompt Loading**: Đọc `system_prompt.txt` để hướng dẫn agent
2. **LLM Binding**: Gắn tools vào LLM model
3. **Agent Reasoning**: Agent quyết định gọi tool nào dựa trên input
4. **Tool Chaining**: Tự động chuỗi các tool nếu cần
5. **Response Generation**: Trả lời cho user bằng tiếng Việt

### Rules (Quy Tắc Chính)

- 🎯 **Golden Rule**: Nếu user cung cấp đủ 4 thông tin (origin, destination, nights, budget) → **BẮT BUỘC gọi tool chain ngay**
- 🇻🇳 Trả lời bằng tiếng Việt
- 💬 Tự nhiên như một người bạn du lịch, không robot
- 📋 Chỉ hỏi thêm sau khi nhận kết quả tool

## 🐛 Troubleshooting

### 1. Lỗi kết nối OLLAMA
```
Error: Failed to connect to OLLAMA_BASE_URL
→ Kiểm tra biến OLLAMA_BASE_URL có đúng không
→ Kiểm tra OLLAMA server đang chạy
```

### 2. Lỗi API Key
```
Error: Invalid API key
→ Tạo file .env với OLLAMA_API_KEY đúng
```

### 3. Tool không được gọi
```
→ Kiểm tra system prompt có instruction rõ ràng không
→ Kiểm tra model có support tool use không
```

## 👨‍💻 Thông Tin Tác Giả

**Sinh viên**: 2A202600443  
**Khóa học**: AI in Action - Day 4  
**Thời gian**: April 2026

## 📚 Tài Liệu Tham Khảo

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

## 📝 License

MIT License - Tự do sử dụng cho mục đích học tập và phát triển.

---

**Cập nhật lần cuối**: April 7, 2026
