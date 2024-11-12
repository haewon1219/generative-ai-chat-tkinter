import tkinter as tk
from tkinter import messagebox
import mysql.connector
import importlib

# 데이터베이스 연결 설정
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1024",
    database="e-commerce"
)

# GUI 설정
root = tk.Tk()
root.title("로그인")
root.geometry("300x200")

# ID 입력 필드
label_id = tk.Label(root, text="ID")
label_id.pack(pady=5)
entry_id = tk.Entry(root)
entry_id.pack(pady=5)

# 비밀번호 입력 필드
label_password = tk.Label(root, text="비밀번호")
label_password.pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

# 로그인 버튼
login_button = tk.Button(
    root,
    text="로그인",
    command=lambda: (
        # 사용자 입력값 가져오기
        (user_id := entry_id.get()),
        (user_password := entry_password.get()),

        # 입력값 유효성 검사
        messagebox.showwarning("입력 오류", "ID와 비밀번호를 모두 입력해주세요.")
        if not user_id or not user_password
        else (
            # 데이터베이스에서 사용자 정보 확인
            (cursor := connection.cursor()),
            cursor.execute(
                "SELECT * FROM users WHERE id = %s AND password = %s",
                (user_id, user_password)
            ),
            (result := cursor.fetchone()),

            # 로그인 성공 여부 확인
            (
                messagebox.showinfo("로그인 성공", "로그인에 성공했습니다."),
                root.destroy(),  # 로그인 창 종료
                (my_gpt := importlib.import_module("1111_재미니")).myGpt()  # myGtp 클래스 호출
            )
            if result
            else messagebox.showerror("로그인 실패", "ID 또는 비밀번호가 잘못되었습니다."),

            cursor.close()
        )
    )
)
login_button.pack(pady=20)

# GUI 실행
root.mainloop()

# GUI 종료 후 데이터베이스 연결 해제
connection.close()
print("MySQL 연결이 종료되었습니다.")
