# Tiếp quản chính xác

1. Đọc STATUS.md, FOLLOWUP.md, healthcare-semantic-summary.json và biên nhận production mới nhất trên nhánh tth-navigation-handover. Lượt rà soát sau 6c85df8 đã phát hiện lỗi đúng route nhưng sai đối tượng mà kiểm kê trước bỏ sót. Không suy diễn READY hoặc số đích tồn tại là đạt nghiệp vụ.
2. Repo duy nhất: nguyenyenthuong-netizen/TTH-2027. Không tạo dự án/domain mới. Dự án Group: tth-website-danh-muc; Healthcare: tth-healthcare-website.
3. Mốc trước sửa: 9412d7ffaadd886a19deed520a914a05cd70a9b9. Hero được bảo vệ từ 06ab2e950546cc463cef62215ffafbd836619e36. Luôn fetch nguồn mới nhất trước sửa; không reset về các mốc này.
4. Nguồn Group: pages-overrides/catalog/kien-truc-thuong-hieu-final/. build.mjs giải mã base có checksum, navigation-build.mjs đăng ký route dịch vụ từ dữ liệu, navigation.js xử lý hợp đồng trung tâm.
5. Nguồn Healthcare: tth-healthcare-release/. website.zip là nguồn đã duyệt; build-navigation.mjs chèn adapter, không sửa ZIP gốc. vercel.json gọi Node build-navigation.mjs.
6. Chạy kiểm tra:

```
node scripts/tth_navigation_contract_test.mjs
node scripts/tth_healthcare_navigation_test.mjs
node scripts/tth_healthcare_semantic_test.mjs
node pages-overrides/catalog/kien-truc-thuong-hieu-final/build.mjs /tmp/tth-catalog
node tth-healthcare-release/build-navigation.mjs /tmp/tth-healthcare
python scripts/tth_navigation_build_gate.py /tmp/tth-catalog/index.html /tmp/tth-healthcare/index.html
```

7. Chuẩn bị QA ở thư mục riêng, tuyệt đối không đưa qa-after.html/scenarios.html/healthcare-qa.html/responsive.html vào output production:

```
python scripts/tth_navigation_prepare_catalog_qa.py /tmp/tth-catalog/index.html /path/to/preview/dist
python scripts/tth_navigation_prepare_qa.py /path/to/preview/dist /tmp/tth-healthcare/index.html
```

8. Dùng browser click Run complete route audit, Run navigation scenarios và Run Healthcare audit. Không thay file preview trong lúc chạy. Lưu JSON từ script#qa-results, script#scenario-results, script#hc-results. Kiểm thử modal hotline riêng vì route này chủ ý mở modal.
9. So sánh ảnh hero cùng viewport. Bằng chứng vùng hero desktop trước/sau phải giữ nguyên; toàn bộ styles/images của Healthcare được gate kiểm tra byte-identical.
10. Chỉ push main/đưa production sau khi lỗi nghiêm trọng đã được xử lý. Push không force; kiểm tra source remote mới nhất ngay trước push. Sau READY phải kiểm lại production và context/reload/language/back.
11. Duy trì một bộ hồ sơ mới nhất; thay báo cáo và gói ZIP của cùng hồ sơ. Không tạo hàng loạt bản trùng lặp.
