Backend chính

Yêu cầu: 
        - Đã cài python 3.12.x
        - Cấu trúc thư mục: 
                            PBL6
                                .venv (môi trường)
                                backend (chứa code đã pull về)
Các bước chạy backend:
    - Tạo môi trường: 
        python -m venv .venv

    - Kích hoạt môi trường:
        cd PBL6
        .venv\Scripts\activate

    - Cài đặt các package:
        cd backend
        pip install -r requirements.txt

    - Đổi file config.env.sample thành config.env
    
    - Thêm db.sql vào MySql ()
    
    - Chỉnh các Database Settings trong config.env tương ứng (DB_NAME = tên db vừa thêm)

    - Migrate
        python manage.py migrate
        
    - Chạy server
        cd backend
        py manage.py runserver

    
