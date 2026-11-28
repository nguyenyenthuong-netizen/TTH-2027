# Nhật ký lỗi và xử lý

| Mã | Trạng thái | Nguyên nhân | Hiệu chỉnh và bằng chứng |
|---|---|---|---|
| NAV-14 | Đã sửa trong nguồn kế tiếp 6c85df8 | Thẻ chuyên khoa dùng chung href Tim mạch; kiểm kê tồn tại đích không phát hiện sai nội dung | Đăng ký 21 chuyên khoa từ h1 của trang đã duyệt; phân giải theo danh tính/alias, giữ cơ sở; chưa có hồ sơ thì báo chưa kết nối |
| NAV-15 | Đã sửa trong nguồn kế tiếp 6c85df8 | Capture trung tâm chạy trước bộ chọn hồ sơ bác sĩ cũ; href gốc có thể che query item được runtime bổ sung | Phân giải 24 bác sĩ theo tên đã có; giữ item của gói/dịch vụ/bài viết. Không chọn hồ sơ khác cho thẻ chưa công bố danh tính |
| NAV-01 | Đã sửa | Nút hotline Group bị bắt bởi handler mở liên hệ | Chuẩn hóa tel:19002675; browser xác nhận href của thanh cố định |
| NAV-02 | Đã sửa | request(n) suy diễn hành vi theo trang, bỏ ý định hợp tác trên nhãn nút | Intent hợp tác độc lập với field; thử các trang topic và đối tác |
| NAV-03 | Đã sửa | Contact intent và booking preferences chỉ lưu trong bộ nhớ | URL mang context công khai; reload/back/forward khôi phục đúng đối tượng |
| NAV-04 | Đã sửa | Window listener menu cha chạy trước listener điều hướng ở document | Adapter xử lý capture trước; click tên menu cha và menu mobile đạt |
| NAV-05 | Đã sửa | Metadata dịch vụ tam-DV-04 tồn tại nhưng không có template và TITLE route | Đăng ký tự động dịch vụ từ NORMALIZED vào template/TITLE; đúng Hà Tĩnh / RHM / dịch vụ 3, không gán bác sĩ thẩm mỹ sang RHM |
| NAV-06 | Đã sửa | CTA đặt lịch của Healthcare bỏ query từ hồ sơ hoặc microsite | Adapter giữ doctor/branch/specialty/source/subject; không sửa payload nội dung và ảnh |
| NAV-07 | Đã sửa | Fragment không có đích và chức năng chưa kết nối có thể trông như liên kết đang hoạt động | Healthcare phân biệt unavailable; bỏ href giả, nêu chưa kết nối. Zalo không bịa OA |
| NAV-08 | Đã sửa | Gọi tel/mail trong iframe sandbox có thể bị giữ trong frame | Bridge giới hạn tel/mailto từ chính frame; giữ nguyên sandbox |
| NAV-13 | Đã sửa | Nút gộp VI \| EN bị xem là liên kết trang chủ EN | Nhận diện toggle thực tế theo nhãn/aria-label; giữ query, cơ sở và đối tượng khi đổi hai chiều |
| NAV-12 | Đã sửa | Anchor của hồ sơ kiến trúc bị xử lý như điểm cuộn | Giữ bộ chuyển view gốc; 21 lượt hồ sơ kiến trúc đạt |
| NAV-11 | Đã sửa | Default href hotline có thể còn là contact trước lượt scan DOM | Gán tel đồng bộ tại capture click; unit test xác nhận href và chỉ thực thi một lần |
| NAV-10 | Đã sửa | Nhận diện chữ Đ hoa và nhãn đặt lịch EN không đầy đủ ở Healthcare | Chuẩn hóa đ/Đ và nhãn Book appointment; 10 assertions độc lập; kiểm tra trực tiếp hồ sơ bác sĩ → TTH Vinh / Ngoại tổng quát |
| NAV-09 | Đã sửa | Lựa chọn chuyên khoa từ trang chuyên môn không truyền vào booking | Context chuyên khoa và cơ chế áp lại khi người dùng chọn cơ sở phù hợp |

## Các phát hiện trong kiểm thử, chưa từng phát hành

- Bộ quét đầu cập nhật History quá nhanh: 262 cảnh báo URL quota. Tách kiểm tra cấu trúc khỏi History; kiểm thử lịch sử ở tốc độ tương tác thực tế.
- Bộ chạy tìm CTA theo data attribute trước khi requestAnimationFrame kịp gắn metadata: cảnh báo giả. Chuyển sang phân giải hợp đồng trực tiếp trên phần tử DOM.
- Preview tự tải lại khi thay gói kiểm thử làm hủy lượt chạy. Đóng băng gói trong mỗi lượt nghiệm thu; không tính lượt bị hủy là PASS.
- Healthcare go(TienIch_Hotline) chủ ý mở modal, không phải trang. Tách modal khỏi lượt quét trang, nghiệm thu popup riêng.
- Gói Healthcare cần escape ký tự `<`/`>` khi nhúng JSON trang HTML. Đã thêm gate bắt buộc; không có bản lỗi đóng gói nào được deploy.
- Rà toàn bộ đối tượng ban đầu: 377 assertions, 2 FAIL cùng tam/med-service-3 (VN/EN). Đã sửa NAV-05 và chạy lại toàn bộ.

## Dữ liệu/chức năng chưa kết nối thực tế

- Đặt lịch, đăng ký chương trình, hồ sơ bác sĩ và dữ liệu minh họa chưa trở thành nghiệp vụ HIS/CRM thật.
- Specialty/elder chưa có hotline/OA chính thức trong cấu hình; không gán số dùng chung thay thế.
- Healthcare chưa có bản dịch EN đầy đủ cho toàn bộ nội dung; điều hướng giữ trang/đối tượng và đánh dấu partial-translation. Đây là phần nội dung cần bổ sung, không được báo là đã hoàn tất dịch thuật.

## Ghi nhận ngoài phạm vi điều hướng

- Ở khung tablet 768 px, nhãn ảnh minh họa của hero có thể nằm thấp, gần phần hành trình. Giữ nguyên thiết kế đã duyệt, ghi nhận bằng ảnh tablet-group.jpg; không tự thiết kế lại.
