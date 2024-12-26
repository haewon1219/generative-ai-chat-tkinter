import google.generativeai as genai
import tkinter as tk
from tkinter import messagebox, Label, Entry, Button, Text, Scrollbar, END
import mysql.connector
from datetime import datetime

class myGpt:
    def __init__(self):
        # Google Generative AI API 설정
        self.key = 'XYZ'
        genai.configure(api_key=self.key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.chat_session = self.model.start_chat(history=[])  # 히스토리 기능 활성화
        
        # MySQL 데이터베이스 연결 설정
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1024",
            database="e-commerce"
        )
        
        # Tkinter 설정
        self.window = tk.Tk()
        self.window.title("Generative AI Chat")
        self.window.geometry("500x700")

        # GUI 구성
        title = '삼정KPMG / Ver1.0 / 구글 재미니와 연동하는 tkinter'
        logo_label = Label(self.window, text=title, font=("Arial", 15, "bold"), fg="blue")
        logo_label.grid(row=0, column=0, columnspan=4, pady=10)

        # 입력 필드 및 버튼
        Label(self.window, text="입력:").grid(row=1, column=0, sticky="ew")
        self.entry = Entry(self.window, width=50)
        self.entry.grid(row=1, column=1, sticky="ew")
        
        send_button = Button(self.window, text="전송", command=self.send_message)
        send_button.grid(row=1, column=2, sticky="ew")
        
        new_button = Button(self.window, text="New", command=self.reset_chat)
        new_button.grid(row=1, column=3, sticky="ew")

        # 채팅 히스토리 창 및 스크롤바 설정
        self.chat_history = Text(self.window, wrap='word')
        self.chat_history.grid(row=2, column=0, columnspan=4, sticky="nsew")
        
        scrollbar = Scrollbar(self.window, command=self.chat_history.yview)
        scrollbar.grid(row=2, column=4, sticky="ns")
        self.chat_history.config(yscrollcommand=scrollbar.set)

        # 창 크기 조정 설정
        self.window.grid_rowconfigure(2, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(2, weight=1)
        self.window.grid_columnconfigure(3, weight=1)

        self.window.mainloop()

    # 메시지 전송 기능
    def send_message(self):
        user_input = self.entry.get()
        if user_input.strip() == "":
            messagebox.showwarning("입력 오류", "메시지를 입력해주세요.")
            return

        # 사용자 입력과 모델 응답을 채팅 히스토리에 추가
        self.chat_history.insert(END, f"사용자: {user_input}\n")
        response = self.chat_session.send_message(user_input)
        self.chat_history.insert(END, f"모델: {response.text}\n")
        
        # 입력 필드 초기화
        self.entry.delete(0, END)
        self.chat_history.yview(END)

        # MySQL에 대화 기록 저장
        cursor = self.connection.cursor()
        insert_query = """
            INSERT INTO chat_history (id, timestamp, question, response)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, ("사용자ID", datetime.now(), user_input, response.text))
        self.connection.commit()
        cursor.close()

    # 채팅 히스토리 초기화
    def reset_chat(self):
        self.chat_session = self.model.start_chat(history=[])
        self.chat_history.delete(1.0, END)
        self.chat_history.insert(END, "New chat started.\n")
