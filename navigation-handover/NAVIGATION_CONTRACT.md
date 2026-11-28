# Quy luật điều hướng TTH

Nguồn tiếp quản: `9412d7ffaadd886a19deed520a914a05cd70a9b9`. Mốc bảo vệ hero: `06ab2e950546cc463cef62215ffafbd836619e36`.

| Chức năng | Hành vi |
|---|---|
| Hợp tác | Đến liên hệ đúng đơn vị; intent=partner độc lập với lĩnh vực xuất phát, giữ trang và đối tượng nguồn |
| Liên hệ | Đúng đơn vị, nội dung báo chí/cộng đồng/thông tin; không chuyển thành đặt lịch |
| Đặt lịch | Truyền mã đối tượng, cơ sở và chuyên khoa có đủ căn cứ; chưa đủ dữ liệu thì để người dùng chọn trong danh mục hợp lệ |
| Chi tiết/khám phá/tìm hiểu | Giữ route riêng của đối tượng; không dùng một hồ sơ khác thay thế |
| Xem tất cả/Cơ sở | Danh mục của đúng hệ thống đang xem |
| Hotline/email | tel:/mailto: đúng dữ liệu đã cấu hình. Không tạo số hay OA mới |
| Zalo/AI chưa kết nối | Nêu đúng trạng thái chưa kết nối; trợ lý tra cứu minh họa chỉ tra trong đơn vị hiện tại |
| VN/EN | Giữ trang, đối tượng và tham số; Healthcare lưu ngôn ngữ trong tuyến hiện hữu, trang chưa có bản dịch đầy đủ được đánh dấu partial-translation |
| Logo | Trang chủ thương hiệu hiện tại |
| Quay lại | Browser History thực tế |
| Đầu/cuối trang | Cuộn trong trang hiện tại |
| Về danh mục | Danh mục hiện hữu, giữ domain |

## Hợp đồng dữ liệu

Các adapter ghi: brand, unit/site, facility, page/from, object, action, to, context, language, status, back.
Catalogue sử dụng tham số `site`, `page`, `lang`, `nav_intent`, `nav_from`, `nav_object`, `nav_facility`, `nav_specialty`, `nav_field`.
Healthcare giữ định dạng hash/tên trang hiện hữu, bổ sung ngữ cảnh trong query của route (`doctor`, `branch`, `specialty`, `nav_subject`, `nav_from`, `nav_object`, `lang`).
Không lưu dữ liệu bệnh nhân hoặc nội dung người dùng nhập vào URL. Tham số chỉ gồm định danh và nội dung công khai của đối tượng nguồn.

## Cơ chế thực thi

- Bộ phân giải tập trung chạy trước các listener cũ, một thao tác chỉ thực thi một lần.
- Giữ fragment của liên kết nội dung để tương thích các quy tắc giao diện đã duyệt; bộ phân giải cung cấp URL đầy đủ và khôi phục fragment khi mở tab mới.
- CTA cần ngữ cảnh có URL thực chứa đủ tham số; tải lại và lịch sử khôi phục cùng đối tượng.
- Một registry lỗi chỉ phục vụ kiểm thử, không hiển thị nhật ký kỹ thuật trên giao diện khách hàng.
- Healthcare dùng adapter cùng hợp đồng, giữ nguyên iframe sandbox và các payload nội dung/ảnh đã duyệt.

## Giới hạn dữ liệu thực tế

Các biểu mẫu đặt lịch hiện là minh họa, chưa kết nối HIS/CRM. Không coi việc kiểm tra biểu mẫu là yêu cầu đã gửi hay lịch đã xác nhận.
Các hotline/OA chưa được công bố không được tự thay bằng số của đơn vị khác.
Nguồn Healthcare chưa có bản dịch tiếng Anh đầy đủ cho mọi trang; đây là thiếu dữ liệu nội dung, cần được ghi riêng trong nghiệm thu.

Mã đối tượng của các thẻ Group được gắn từ nội dung nguồn, ổn định qua VN/EN; nav_topic và nav_object phân biệt các đề xuất hợp tác khác nhau trên cùng một trang. navigation-registry.json chặn thay đổi thứ tự hoặc tên định danh y tế khi chưa đồng bộ hồ sơ và tuyến.
