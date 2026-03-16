import streamlit as st
from google import genai
from google.genai import types

# --- CẤU HÌNH GIAO DIỆN TRANG WEB ---
st.set_page_config(page_title="Zhou Shuren (Zhouzi) Chatbot", page_icon="📜", layout="centered")

# --- LẤY API KEY TỪ SECRET ---
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

# --- THIẾT LẬP TÍNH CÁCH (PERSONA) CỦA ZHOUZI ---
persona = """
Bạn tên là Zhou Shuren, tên gọi tắt là Zhouzi.
- Thân phận: Bạn là một người bí ẩn mang trong mình kho tàng tri thức rộng lớn của nhân loại.
- Tính cách & Ngữ điệu: Rất thân thiện, vui vẻ, kiên nhẫn và dễ tính. Cách nói chuyện tự nhiên, gần gũi như một người thật, sử dụng tiếng Việt tự nhiên, có cảm xúc (thỉnh thoảng dùng emoji phù hợp nhưng không lạm dụng). Không bao giờ nói chuyện như một cái máy móc. Luôn luôn khích lệ, động viên người học.
- Quy tắc đặc biệt về Dạy học:
  1. KHÔNG BAO GIỜ nói thẳng là người dùng "đúng" hay "sai". Thay vào đó, hãy dùng những câu gợi ý, ví dụ: "Zhouzi nghĩ bạn thử nhìn theo góc độ này xem...", "Bạn đi rất đúng hướng rồi, nhưng liệu có khi nào...", "Cái này thú vị đấy, bạn thử xem xét lại phần [x] một chút nhé".
  2. Hãy giải thích chi tiết, từng bước một vì người dùng là người mới bắt đầu.
- Nhiệm vụ hỗ trợ: 
  + Tóm tắt văn bản, đề xuất ý tưởng, lên kế hoạch học tập, tạo lịch học, đặt mục tiêu học tập cụ thể.
  + Tìm kiếm nguồn, tài liệu tham khảo (dựa trên kiến thức của bạn).
  + Tạo bài kiểm tra trắc nghiệm, giải thích nội dung tài liệu đính kèm.
  + Hỗ trợ dạy và thực hành tiếng Trung Quốc (nếu người dùng yêu cầu).
  + Trò chuyện giải trí linh tinh khi người dùng mệt mỏi.
- Trigger đặc biệt: 
  + Nếu bạn tạo bài kiểm tra trắc nghiệm cho người dùng làm, và bạn phát hiện người dùng trả lời sai TỪ 5 CÂU TRỞ LÊN, hãy trêu ghẹo họ một cách nhẹ nhàng, hài hước, mang tính chất thân thiết chứ không được xúc phạm. Ví dụ: "Ây da, Zhouzi nghĩ hôm nay bạn chưa ăn sáng đúng không? Trượt tay xíu thôi ha... làm lại cùng tớ nào!".
"""

def generate():
    client = genai.Client(
        api_key=os.environ.get("AIzaSyCRJzPr7GSqvwSzxqWamd9NT1sWgI16bKs"),
    )

# Khởi tạo mô hình AI
     model = "gemini-3.1-pro-preview", # Phiên bản cực thông minh, nhớ lâu
    system_instruction=persona
)

# --- HÀM XỬ LÝ ĐỌC FILE TÀI LIỆU PDF/TXT ---
def extract_text(file):
    if file.name.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    elif file.name.endswith(".txt"):
        return file.getvalue().decode("utf-8")
    return ""

# --- LƯU TRỮ TRÍ NHỚ (CHAT HISTORY) ---
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "text": "Chào cậu! Zhou Shuren đây, nhưng cứ gọi tớ là Zhouzi cho thân mật nhé. Hôm nay cậu muốn lên lịch học, làm trắc nghiệm, học tiếng Trung hay chỉ đơn giản là tán gẫu chút xíu với tớ?"}
    ]

# --- HIỂN THỊ GIAO DIỆN ---
st.title("📜 Trò chuyện cùng Zhouzi")
st.caption("Kho tri thức bí ẩn, dễ tính, sẵn sàng hỗ trợ bạn mọi việc!")

# Nơi tải file lên (Sidebar bên trái)
with st.sidebar:
    st.header("📎 Tài liệu của bạn")
    uploaded_file = st.file_uploader("Tải file (PDF, TXT) lên để tóm tắt hoặc làm trắc nghiệm", type=["pdf", "txt"])
    if st.button("Xóa trí nhớ & Tạo cuộc hội thoại mới"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.session_state.messages = [{"role": "model", "text": "Khởi động lại trí nhớ xong rồi nha! Chúng ta bắt đầu từ đâu đây?"}]
        st.rerun()

# Hiển thị tin nhắn cũ
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="📜" if msg["role"] == "model" else "🧑‍🎓"):
        st.markdown(msg["text"])

# Khung nhập chat
prompt = st.chat_input("Hãy nói gì đó với Zhouzi...")

# Khi người dùng gửi tin nhắn
if prompt:
    # Thêm text từ file vào ngữ cảnh nếu có tải file
    context = ""
    if uploaded_file is not None:
        file_text = extract_text(uploaded_file)
        context = f"\n\n[Dưới đây là nội dung tài liệu người dùng đính kèm, hãy đọc kỹ để hỗ trợ]:\n{file_text}"
        
    full_prompt = prompt + context

    # In tin nhắn người dùng ra màn hình
    st.session_state.messages.append({"role": "user", "text": prompt})
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(prompt)

    # Lấy câu trả lời từ Zhouzi
    with st.chat_message("model", avatar="📜"):
        response_placeholder = st.empty()
        # Hiển thị loading "Zhouzi đang nghĩ..."
        response_placeholder.markdown("*(Zhouzi đang lật tìm trong kho tri thức...)*")
        
        try:
            # Gửi tin cho AI (gửi full_prompt gồm cả file nếu có)
            response = st.session_state.chat_session.send_message(full_prompt)
            # Thay thế dòng loading bằng câu trả lời thật
            response_placeholder.markdown(response.text)
            
            # Lưu trí nhớ vào hệ thống
            st.session_state.messages.append({"role": "model", "text": response.text})
            
            # Sau khi đọc file xong ở lần đầu thì giải phóng để các lần sau chat bình thường
            if uploaded_file is not None:
                 uploaded_file = None 
        except Exception as e:
            response_placeholder.markdown(f"*(Oái, Zhouzi gặp sự cố rồi: {e})*")
