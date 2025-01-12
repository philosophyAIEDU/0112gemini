import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def main():
    st.title("PDF 문서 분석기 with Gemini")
    
    api_key = st.text_input("Google API 키를 입력하세요:", type="password")
    
    if api_key:
        try:
            genai.configure(api_key=api_key)
            
            uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type=['pdf'])
            
            if uploaded_file is not None:
                text_content = extract_text_from_pdf(uploaded_file)
                
                with st.expander("추출된 텍스트 보기"):
                    st.text(text_content)
                
                user_question = st.text_input("PDF에 대해 질문하세요:")
                
                if user_question:
                    model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-1219')
                    
                    with st.spinner('답변을 생성하고 있습니다...'):
                        response = model.generate_content([
                            f"다음 문서 내용을 바탕으로 질문에 답변해주세요:\n\n"
                            f"문서 내용:\n{text_content}\n\n"
                            f"질문: {user_question}"
                        ])
                        
                        # 응답 처리 방식 수정
                        if response.parts:
                            for part in response.parts:
                                st.write(part.text)
                        else:
                            st.write(response.text)
                        
        except Exception as e:
            st.error("오류가 발생했습니다.")
            st.error(f"오류 내용: {str(e)}")

if __name__ == "__main__":
    main()
