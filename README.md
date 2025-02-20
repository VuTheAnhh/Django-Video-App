# django-video-app

Dự án **django-video-app** là một ứng dụng Django được thiết kế để phục vụ việc truyền tải video đào tạo và video quảng bá của công ty **VENESA** trong nội bộ. Ứng dụng này giúp lưu trữ dữ liệu video tập trung và cung cấp các tính năng mã hóa, phát trực tuyến video. Ứng dụng sử dụng **FFmpeg** để tạo tệp HLS (HTTP Live Streaming), tính toán thời lượng video và tạo hình thu nhỏ cho video.

## Tính Năng

- **Mã hóa video**: Sử dụng FFmpeg để mã hóa video thành định dạng HLS, giúp video tương thích với nhiều thiết bị và trình duyệt.
- **Tính toán thời lượng video**: Tự động tính toán thời gian phát của video đã tải lên.
- **Tạo hình thu nhỏ**: Tạo hình thu nhỏ (thumbnail) cho video để cung cấp bản xem trước.
- **Phân quyền theo nhóm**: Tạo nhóm và phân quyền video cho người dùng. Người dùng chỉ có thể xem những video thuộc nhóm mà họ được phân quyền.
- **Có thể mở rộng**: Dự án dễ dàng mở rộng để thêm các tính năng liên quan đến video hoặc tùy chỉnh theo yêu cầu.

## Hướng Dẫn Cài Đặt

### Cài Đặt FFmpeg

Để sử dụng ứng dụng, bạn cần cài đặt **FFmpeg**. Tại [đây](https://www.ffmpeg.org/download.html).

### Các Bước Cài Đặt Dự Án

1. **Tải Dự Án Từ GitHub**

   Clone dự án về máy tính

2. **Tạo Môi Trường Ảo**

   Tạo môi trường ảo Python:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate

3. **Cài đặt các gọi phụ thuộc**

   ```bash
   pip install -r requirements.txt

4. **Áp Dụng Migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate

5. **Tạo Superuser**

   ```bash
   python manage.py createsuperuser

6. **Chạy dự án**

   ```bash
   python manage.py runserver


  
   
