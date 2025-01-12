import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import os

def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def main():
    st.title("PDF 문서 분석기 with Gemini")
    
    # API 키 입력
    api_key = st.text_input("Google API 키를 입력하세요:", type="password")
    
    if api_key:
        genai.configure(api_key=api_key)
        
        # PDF 파일 업로드
        uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type=['pdf'])
        
        if uploaded_file is not None:
            # PDF에서 텍스트 추출
            text_content = extract_text_from_pdf(uploaded_file)
            
            # 사용자 질문 입력
            user_question = st.text_input("PDF에 대해 질문하세요:")
            
            if user_question:
                try:
                    # Gemini 모델 설정
                    model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-1219')
                    
                    # 프롬프트 생성
                    prompt = f"""
                    다음 문서 내용을 바탕으로 질문에 답변해주세요:
                    
                    문서 내용:
                    {text_content}
                    
                    질문: {user_question}
                    """
                    
                    # 응답 생성
                    response = model.generate_content(prompt)
                    
                    # 결과 표시
                    st.write("답변:")
                    st.write(response.text)
                    
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()
