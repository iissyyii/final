import streamlit as st
import pandas as pd
import plotly.express as px

# --- URL 수정 ---
activated_cards_url = 'https://raw.githubusercontent.com/iissyyii/final/main/activated_cards.xlsx'
age_group_users_url = 'https://raw.githubusercontent.com/iissyyii/final/main/age_group_users1.xlsx'

@st.cache_data
def load_data():
    """
    엑셀 파일을 GitHub Raw URL에서 직접 불러옵니다.
    """
    try:
        activated_df = pd.read_excel(activated_cards_url)
        age_group_df = pd.read_excel(age_group_users_url)
        return activated_df, age_group_df
    except Exception as e:
        # 만약 URL에서 파일을 불러오다 오류가 발생하면, 사용자에게 에러 메시지를 보여줍니다.
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        st.error("GitHub URL이 정확한 Raw 파일 주소인지 다시 한 번 확인해주세요.")
        return None, None

# 데이터 불러오기
activated_df, age_group_df = load_data()

# 데이터 로딩에 성공한 경우에만 아래 시각화 코드를 실행
if activated_df is not None and age_group_df is not None:
    st.title('기후동행카드 시각화')

    # 1. 활성화된 기후동행카드 수 시각화
    st.header('활성화된 기후동행카드 수')

    # 컬럼명이 정확하지 않을 수 있으므로, 첫 번째와 두 번째 컬럼을 사용하도록 설정
    try:
        date_col = activated_df.columns[0]
        count_col = activated_df.columns[1]
        
        fig1 = px.line(activated_df, x=date_col, y=count_col,
                       labels={date_col: '날짜', count_col: '활성화 카드 수'},
                       title='일별 활성화된 기후동행카드 수')
        st.plotly_chart(fig1)

    except IndexError:
        st.warning("활성화 카드 데이터(activated_cards.xlsx)에 최소 2개 이상의 컬럼이 필요합니다.")
    except Exception as e:
        st.error(f"활성화 카드 차트 생성 중 오류: {e}")

    # 2. 연령대별 기후동행카드 이용자 수 시각화
    st.header('연령대별 기후동행카드 이용자 수')

    # '따릉이 포함'과 '따릉이 미포함' 컬럼이 있는지 확인하고 합치기
    if '따릉이 포함' in age_group_df.columns and '따릉이 미포함' in age_group_df.columns:
        # '따릉이 포함'과 '따릉이 미포함' 컬럼을 합쳐 '이용자 수' 컬럼 생성
        age_group_df['이용자 수'] = age_group_df['따릉이 포함'] + age_group_df['따릉이 미포함']
        
        # 새로 만든 '이용자 수' 컬럼을 사용해서 바 차트 생성
        fig2 = px.bar(age_group_df, x='연령대', y='이용자 수', 
                      labels={'연령대': '연령대', '이용자 수': '이용자 수'},
                      title='연령대별 이용자 수')
        st.plotly_chart(fig2)
    else:
        st.warning("연령대별 이용자 데이터(age_group_users.xlsx)에 '따릉이 포함'과 '따릉이 미포함' 컬럼이 필요합니다.")
        st.write("현재 파일의 컬럼:", age_group_df.columns.tolist())
