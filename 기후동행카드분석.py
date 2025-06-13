import streamlit as st
import pandas as pd
import plotly.express as px

# --- URL 수정 ---
activated_cards_url = 'https://raw.githubusercontent.com/iissyyii/final/main/activated_cards.xlsx'
age_group_users_url = 'https://raw.githubusercontent.com/iissyyii/final/main/age_group_users.csv'
carmale_url = 'https://raw.githubusercontent.com/iissyyii/final/main/carmale.xlsx'
carfemale_url = 'https://raw.githubusercontent.com/iissyyii/final/main/carfemale.xlsx'

@st.cache_data
def load_data():
    """
    엑셀 파일과 CSV 파일을 GitHub Raw URL에서 직접 불러옵니다.
    """
    try:
        activated_df = pd.read_excel(activated_cards_url)
        age_group_df = pd.read_csv(age_group_users_url)  # CSV 파일을 읽도록 수정
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

    # '24.2월', '24.3월' 등의 컬럼명을 가져와서 x축으로 사용
    try:
        # '구분' 컬럼을 제외하고 월별 데이터 추출
        activated_df_months = activated_df.drop(columns=['Unnamed: 0', '구분'])

        # 월별 데이터의 컬럼명을 '월'로 변환하여 시각화
        fig1 = px.line(activated_df_months.T, 
                       labels={'index': '월', 'value': '활성화 카드 수'},
                       title='월별 활성화된 기후동행카드 수')

        st.plotly_chart(fig1)

    except IndexError:
        st.warning("활성화 카드 데이터(activated_cards.xlsx)에 적절한 월별 데이터가 필요합니다.")
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
        st.warning("연령대별 이용자 데이터(age_group_users.csv)에 '따릉이 포함'과 '따릉이 미포함' 컬럼이 필요합니다.")
        st.write("현재 파일의 컬럼:", age_group_df.columns.tolist())







@st.cache_data
def load_data():
    """
    GitHub에서 남성 및 여성 자차 보유 데이터를 각각 불러옵니다.
    """
    try:
        # 각각의 엑셀 파일 불러오기
        carmale_df = pd.read_excel(carmale_url)
        carfemale_df = pd.read_excel(carfemale_url)
        
        # 성별 컬럼을 추가하여 두 데이터 합치기
        carmale_df['성별'] = '남성'
        carfemale_df['성별'] = '여성'
        
        # 두 데이터프레임을 합침
        combined_df = pd.concat([carmale_df, carfemale_df], ignore_index=True)
        return combined_df
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return None

# 데이터 불러오기
combined_df = load_data()

# 데이터 로딩에 성공한 경우에만 아래 시각화 코드를 실행
if combined_df is not None:
    st.title('연령대별 자차 보유 현황 (성별 합산)')

    # 데이터 구조를 확인
    st.write("데이터 프레임 미리보기:", combined_df.head())

    # 1. 연령대별 자차 보유 현황 시각화
    st.header('연령대별 자차 보유 현황')

    # '연령대'와 '자차 보유' 컬럼이 존재하는지 확인
    if '연령대' in combined_df.columns and '자차 보유' in combined_df.columns:
        # 연령대별 자차 보유 현황 합산
        age_group_df = combined_df.groupby('연령대')['자차 보유'].sum().reset_index()

        # 바 차트 생성
        fig = px.bar(age_group_df, x='연령대', y='자차 보유',
                     labels={'연령대': '연령대', '자차 보유': '자차 보유자 수'},
                     title='연령대별 자차 보유 현황 (성별 합산)')
        st.plotly_chart(fig)
    else:
        st.warning("데이터에 '연령대'와 '자차 보유' 컬럼이 필요합니다.")
        st.write("현재 파일의 컬럼:", combined_df.columns.tolist())

else:
    st.error("데이터를 불러오지 못했습니다. 파일 URL을 확인해 주세요.")
