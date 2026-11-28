# Trạng thái nguồn phát hành điều hướng TTH — 28/11/2026

## Cập nhật sau rà soát production

Bản 6c85df8 có lỗi sai đối tượng Healthcare còn sót: thẻ chuyên khoa trỏ chung Tim mạch và hồ sơ bác sĩ dùng trang mẫu. Không dùng kết quả 675 assertions của lượt trước để kết luận toàn bộ đích đúng nội dung. Xem FOLLOWUP.md và healthcare-semantic-baseline.json. Bản hiệu chỉnh kế tiếp bổ sung phân giải 45 danh tính đã có trong nguồn, 107 assertions về danh tính/ngữ cảnh và kiểm tra trực tiếp nội dung đích trong trình duyệt. Trạng thái phát hành và nghiệm thu mới nhất nằm trong biên nhận production của gói bàn giao cùng nhánh tth-navigation-handover.

Nguồn tiếp quản và production trước sửa: 9412d7ffaadd886a19deed520a914a05cd70a9b9.
Mốc hero được bảo vệ: 06ab2e950546cc463cef62215ffafbd836619e36.

## Kết quả kiểm chứng

- 675 assertions nghiệp vụ trong trình duyệt: 398 đặt lịch/liên hệ/hồ sơ kiến trúc và 277 chương trình/menu cha; 0 FAIL.
- Kiểm kê toàn bộ các trạng thái trang/ngôn ngữ và tương tác: SUMMARY.json; JSON đầy đủ và ma trận chín trường nằm trong thư mục này.
- 31 assertions độc lập kiểm tra hợp đồng, trường hợp chữ Đ hoa, VI | EN gộp, hotline trước lượt scan, mã đối tượng theo từng thẻ và bảo vệ định danh khi cập nhật dữ liệu.
- 70 script của bản biên dịch đạt kiểm tra cú pháp; 126 trang Healthcare và payload ảnh giữ nguyên ngoài adapter điều hướng.
- Hero desktop đã đối chiếu ảnh: vùng so sánh có sai khác kênh màu bằng 0. Lưu ảnh desktop/mobile/tablet và ảnh đặt lịch theo đối tượng.

## Nguồn và cơ chế tiếp quản

- Group: pages-overrides/catalog/kien-truc-thuong-hieu-final/. navigation.js quản lý hành vi, navigation-build.mjs đăng ký route dịch vụ và mã đối tượng theo thẻ, navigation-registry.json bảo vệ định danh khi cập nhật dữ liệu.
- Healthcare: tth-healthcare-release/. Nguồn website.zip đã duyệt được giữ nguyên; build-navigation.mjs chèn adapter từ navigation.js.
- Không đưa bộ chạy kiểm thử hoặc nhật ký kỹ thuật vào output production.
- Không tạo dự án, domain, hoặc rollback hệ thống.
- Commit hiện hành của thư mục nguồn này là bản được bàn giao; đối chiếu deployment gắn với commit trên Vercel và kiểm tra production trước khi tiếp tục sửa. READY không tự thay thế nghiệm thu nghiệp vụ.

## Các phần cần hiểu đúng

Biểu mẫu/HIS/CRM, hồ sơ minh họa và Zalo/hotline chưa được công bố vẫn giữ đúng trạng thái minh họa/chưa kết nối; không giả lập gửi hoặc xác nhận thành công. Healthcare chưa có bản dịch EN đầy đủ cho toàn bộ nội dung; điều hướng giữ nguyên trang/đối tượng và ghi nhận partial-translation. Xem BUGS.md, NAVIGATION_CONTRACT.md và TAKEOVER.md.
