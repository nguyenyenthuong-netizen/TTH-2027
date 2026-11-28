# Rà soát bổ sung sau phát hành 6c85df8

## Kết luận và giới hạn của lượt trước

Lượt kiểm kê trước xác nhận đích tồn tại nhưng bỏ sót trường hợp đúng đường dẫn, sai đối tượng trên Healthcare. Đã tái hiện trực tiếp: từ Main.html, thẻ Sản phụ khoa mở h1 Tim mạch. 675 assertions của lượt trước vẫn là bằng chứng của các kịch bản cụ thể đã chạy, không phải bằng chứng đủ để kết luận mọi liên kết đúng nghiệp vụ. Không dùng READY thay cho nghiệm thu.

## Nguyên nhân và thay đổi

- Lớp capture trung tâm chưa phân giải href mẫu ChuyenKhoa_TimMach.html theo tên thẻ; đồng thời chặn bộ phân giải bác sĩ của mã cũ. Build nay đọc 45 danh tính từ chính các trang chi tiết đã duyệt: 21 chuyên khoa và 24 bác sĩ. Không bổ sung hồ sơ hoặc nội dung y khoa giả.
- Alias Mắt/mổ Phaco, Thận nhân tạo, Chấn thương chỉnh hình, Tiêu hóa, Thần kinh và Phục hồi chức năng được giữ đúng nhóm chuyên môn đã có. Phân biệt các tên dài/ngắn trùng một phần; không đẩy Lão khoa hay bác sĩ chưa công bố sang một đối tượng khác.
- Giữ query item do runtime gắn cho gói khám, dịch vụ, bài viết; không dùng href gốc chung để ghi đè đối tượng đã xác định.
- Giữ cơ sở khi vào chuyên khoa rồi chuyển EN và đặt lịch. Menu cha giữ href cần thiết cho bộ dựng dropdown; chỉ cập nhật native href ở liên kết cần sửa danh tính, đặt lịch hoặc ngôn ngữ.
- Không sửa ZIP gốc, nội dung trang, style, ảnh hoặc Group hero. Gate kiểm tra 126 trang và payload ảnh byte-identical sau khi bỏ script adapter.

## Kiểm thử tái sử dụng

`node scripts/tth_healthcare_semantic_test.mjs`: 107 assertions về 45 danh tính ở VI/EN, alias, thẻ có text node liền nhau, hồ sơ chưa công bố, query item và cơ sở. Bộ này đã được đưa vào workflow cùng 31 assertions hợp đồng trước đó.

Kiểm thử trình duyệt đối chiếu thẻ với h1 thực tế: Sản phụ khoa, Mắt, Thận – Tiết niệu, Hồi sức cấp cứu; bốn bác sĩ trang chủ; Thai sản trọn gói; Hà Tĩnh → Sản phụ khoa → EN → đặt lịch. Kết quả và ma trận chín trường được lưu trong gói bàn giao mới nhất. Quét cấu trúc 230 trạng thái Healthcare được chạy lại trên bản build sửa cuối.

## Điều kiện vận hành còn thiếu

Biểu mẫu, HIS/CRM, Zalo OA hoặc AI chưa có kết nối thật vẫn ghi đúng trạng thái minh họa/chưa kết nối. Điều hướng EN giữ ngữ cảnh; bản dịch nội dung Healthcare còn thiếu. Không tự tạo kết quả gửi thành công, tài khoản OA, hotline, hồ sơ bác sĩ hoặc xác nhận lịch khám. Tích hợp vận hành thật cần đầu mối tiếp nhận, API và quyền truy cập tương ứng; đây không phải dữ liệu có thể suy ra từ website tĩnh.

Đọc biên nhận production và bằng chứng mới nhất trên nhánh tth-navigation-handover trước khi tiếp quản; luôn đối chiếu HEAD main và Vercel, không reset về 6c85df8.
