import streamlit as st
import pandas as pd
import plotly.express as px

# 깃허브 raw 링크 (본인 깃허브 주소로 변경하세요)
activated_cards_url = 'https://github.com/user/repo/raw/main/activated_cards.xlsx'
age_group_users_url = 'https://github.com/user/repo/raw/main/age_group_users.xlsx'

@st.cache_data
def load_data():
    activated_df = pd.read_excel(activated_cards_url)
    age_group_df = pd.read_excel(age_group_users_url)
    return activated_df, age_group_df

activated_df, age_group_df = load_data()

st.title('기후동행카드 시각화')

# 1. 활성화된 기후동행카드 수 시각화
st.header('활성화된 기후동행카드 수')

# 활성화 카드 데이터가 예를 들어, 날짜별 카드 수라고 가정
# 컬럼명 확인 후 필요에 따라 수정하세요
fig1 = px.line(activated_df, x=activated_df.columns[0], y=activated_df.columns[1],
               labels={activated_df.columns[0]:'날짜', activated_df.columns[1]:'활성화 카드 수'},
               title='활성화된 기후동행카드 수 추이')
st.plotly_chart(fig1)

# 2. 연령대별 기후동행카드 이용자 수 시각화
st.header('연령대별 기후동행카드 이용자 수')

# 연령대별 데이터가 예를 들어 '연령대', '이용자 수' 컬럼이 있다고 가정
fig2 = px.bar(age_group_df, x='연령대', y='이용자 수', 
              labels={'연령대':'연령대', '이용자 수':'이용자 수'},
              title='연령대별 이용자 수')
st.plotly_chart(fig2)

