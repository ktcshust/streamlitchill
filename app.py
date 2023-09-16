import streamlit as st
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import defaultdict
import os
import shutil


# Lấy danh sách các stop words tiếng Anh
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))


# Đọc tệp văn bản và tạo tệp mới với định dạng cho trước
def format_text(input_file, output_file, max_line_length):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    formatted_lines = []
    current_line = ""

    for line in lines:
        words = line.strip().split()
        for word in words:
            if len(current_line) + len(word) + 1 <= max_line_length:
                current_line += word + " "
            else:
                formatted_lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            formatted_lines.append(current_line.strip())
            current_line = ""

    with open(output_file, 'w') as f:
        f.write('\n'.join(formatted_lines))


# Tạo bảng chỉ dẫn cho các từ khóa
def create_keyword_index(input_file):
    keyword_index = defaultdict(list)

    with open(input_file, 'r') as f:
        lines = f.readlines()

    for idx, line in enumerate(lines, start=1):
        words = word_tokenize(line.lower())
        for word in words:
            if word.isalpha() and word not in stop_words:
                keyword_index[word].append(idx)

    return keyword_index


def main():
    st.title("Text Formatting and Keyword Indexing")

    uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

    if uploaded_file is not None:
        max_line_length = st.slider("Maximum line length", min_value=10, max_value=100, value=50)

        # Đọc tệp tải lên tạm thời để định dạng và tạo bảng chỉ dẫn
        temp_file_path = "temp_uploaded_file.txt"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.read())

        st.write("Uploaded file saved temporarily.")

        # Định dạng tệp văn bản và tạo bảng chỉ dẫn từ khóa
        formatted_output_path = "formatted_output.txt"
        format_text(temp_file_path, formatted_output_path, max_line_length)
        keyword_index = create_keyword_index(formatted_output_path)

        # Đọc nội dung tệp mới đã định dạng và hiển thị trên Streamlit
        with open(formatted_output_path, "r") as f:
            formatted_text = f.read()
            st.write("Formatted Text:")
            st.text(formatted_text)

        # Hiển thị bảng chỉ dẫn từ khóa
        st.write("Keyword Index:")
        for keyword, lines in keyword_index.items():
            st.write(f"{keyword}: {', '.join(map(str, lines))}")

        

        # Xóa tệp tạm thời sau khi hoàn thành
        os.remove(temp_file_path)


if __name__ == "__main__":
    main()
