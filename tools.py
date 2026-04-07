from langchain_core.tools import tool
import logging

# Logger sẽ được config từ agent.py
logger = logging.getLogger("TravelBuddy-Tools")
# MOCK DATA – Dữ liệu giả lập hệ thống du lịch
# Lưu ý: Giá cả có logic (VD: cuối tuần đắt hơn, hạng cao hơn đắt hơn)
# Sinh viên cần đọc hiểu data để debug test cases.
# =================================================================

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 4.6},
    ],
}

@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy chuyến bay, trả về thông báo không có chuyến.
    """
    # Log chi tiết
    logger.info(f"    [search_flights] được gọi")
    logger.info(f"    - Khởi hành: {origin}")
    logger.info(f"    - Đích đến: {destination}")
    
    for i in FLIGHTS_DB.keys():
        if i[0].lower() == origin.lower() and i[1].lower() == destination.lower():
            flights = FLIGHTS_DB[i]
            logger.info(f"    -  Tìm thấy {len(flights)} chuyến bay")
            result = f"Các chuyến bay từ {origin} đến {destination}:\n"
            for idx, f in enumerate(flights, 1):
                result += f"- {f['airline']}: {f['departure']} - {f['arrival']}, {f['class']}, {f['price']:,} VNĐ\n"
                logger.debug(f"      Chuyến {idx}: {f['airline']} ({f['price']:,} VNĐ)")
            logger.info(f"    - Kết quả: Trả về danh sách {len(flights)} chuyến bay")
            return result

    logger.warning(f"    -  Không tìm thấy chuyến bay từ {origin} đến {destination}")
    return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."


@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn
    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    logger.info(f"   [search_hotels] được gọi")
    logger.info(f"    - Thành phố: {city}")
    logger.info(f"    - Giá tối đa: {max_price_per_night:,} VNĐ/đêm")
    
    for i in HOTELS_DB.keys():
        if i.lower() == city.lower():
            hotels = HOTELS_DB[i]
            filtered_hotels = [h for h in hotels if h["price_per_night"] <= max_price_per_night]
            if not filtered_hotels:
                logger.warning(f"    - Không tìm thấy khách sạn ở {city} với giá tối đa {max_price_per_night:,} VNĐ")
                return f"Không tìm thấy khách sạn nào ở {city} với giá tối đa {max_price_per_night:,} VNĐ mỗi đêm."
            logger.info(f"    - Tìm thấy {len(filtered_hotels)} khách sạn (từ {len(hotels)} tổng)")
            result = f"Các khách sạn ở {city} với giá tối đa {max_price_per_night:,} VNĐ mỗi đêm:\n"
            for idx, h in enumerate(filtered_hotels, 1):
                result += f"- {h['name']}: {h['stars']} sao, {h['area']}, rating {h['rating']}, {h['price_per_night']:,} VNĐ/đêm\n"
                logger.debug(f"      [{idx}] {h['name']} - {h['price_per_night']:,} VNĐ")
            logger.info(f"    - Kết quả: Trả về danh sách {len(filtered_hotels)} khách sạn")
            return result

    logger.error(f"    - ❌ Thành phố {city} không có trong database")
    return f"Không tìm thấy khách sạn nào ở {city}."

@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy, 
      định dạng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')
    Trả về bảng chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    logger.info(f"   [calculate_budget] được gọi")
    logger.info(f"    - Ngân sách tổng: {total_budget:,} VNĐ")
    logger.info(f"    - Chuỗi chi phí: {expenses}")
    
    dict_expenses = {}
    try:
        for item in expenses.split(","):
            name, cost = item.split(":")
            dict_expenses[name.strip()] = int(cost.strip())
        logger.info(f"    -  Parse chi phí thành công ({len(dict_expenses)} khoản)")
    except ValueError as e:
        logger.error(f"    -  Lỗi parse chi phí: {e}")
        return "Lỗi: Định dạng chi phí không hợp lệ. Vui lòng kiểm tra lại."

    total_expenses = sum(dict_expenses.values())
    remaining_budget = total_budget - total_expenses

    # Log chi tiết từng khoản chi
    for name, cost in dict_expenses.items():
        logger.debug(f"      - {name}: {cost:,} VNĐ")

    # Format bảng chi tiết
    result = "Bảng chi phí:\n"
    for name, cost in dict_expenses.items():
        result += f"- {name}: {cost:,} VNĐ\n"
    result += "---\n"
    result += f"Tổng chi: {total_expenses:,} VNĐ\n"
    result += f"Ngân sách: {total_budget:,} VNĐ\n"
    result += f"Còn lại: {remaining_budget:,} VNĐ\n"

    if remaining_budget < 0:
        logger.warning(f"    -  Vượt ngân sách {-remaining_budget:,} VNĐ!")
        result += f"Vượt ngân sách {-remaining_budget:,} VNĐ! Cần điều chỉnh."
    else:
        logger.info(f"    -  Ngân sách còn lại: {remaining_budget:,} VNĐ")

    logger.info(f"    - Kết quả: Tổng chi {total_expenses:,} VNĐ, còn {remaining_budget:,} VNĐ")
    return result
@tool
def get_today() -> str:
    """
    Trả về ngày tháng hiện tại theo định dạng 'dd/mm/yyyy'.
    Công cụ này có thể hữu ích nếu agent cần đưa ra gợi ý dựa trên ngày tháng (VD: cuối tuần, lễ tết).
    """
    from datetime import datetime
    today = datetime.now().strftime("%d/%m/%Y")
    logger.info(f"   [get_today] được gọi - Trả về ngày hiện tại: {today}")
    return today