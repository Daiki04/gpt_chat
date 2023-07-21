import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)
from langchain.callbacks import get_openai_callback

def init_page():
    st.set_page_config(page_title="My ChatGPT", page_icon=":smiley:") # ページタイトルとアイコンの設定

    st.header("My ChatGPT :speech_balloon:") # ヘッダーの設定

    st.sidebar.title("Options") # サイドバーの設定

def select_model():
    # モデルの設定（サイドバー）
    model = st.sidebar.radio("Choose a model", ("GPT-3.5", "GPT-4"))


    if model == "GPT-3.5":
        model_name = "gpt-3.5-turbo-0613"
    elif model == "GPT-4":
        model_name = "gpt-4"

    # temperatureの設定（サイドバー）
    temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=2.0, value=0.0, step=0.1)

    return ChatOpenAI(temperature=temperature, model_name=model_name)

def init_messages():
    # チャットクリア(サイドバー)
    clear_button = st.sidebar.button("Clear Conversation", key="clear")

    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
        ]
        st.session_state.costs = []

def get_answer(llm, messages):
    with get_openai_callback() as cb:
        answer = llm(messages)
    return answer.content, cb.total_cost

def main():
    init_page() # ページの初期化

    llm = select_model() # モデルの選択

    init_messages() # メッセージの初期化

    # 入力監視
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
        ] # システムメッセージを追加

    if user_input := st.chat_input("聞きたいことを入力してね！"):
        st.session_state.messages.append(HumanMessage(content=user_input)) # 人間の質問を追加
        with st.spinner("ChatGPTが考え中..."):
            # AIの返答を取得
            answer, cost = get_answer(llm, st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=answer)) # AIの返答を追加
        st.session_state.costs.append(cost) # Costを追加

    # メッセージを表示
    messages = st.session_state.get("messages", []) # メッセージを取得
    for message in messages:
        if isinstance(message, AIMessage): # messageの型がAIMessageの場合
            with st.chat_message("assistant"):
                st.markdown(message.content) # ChatGPTの返答を表示
        elif isinstance(message, HumanMessage): # messageの型がHumanMessageの場合
            with st.chat_message("user"):
                st.markdown(message.content) # 人間の質問を表示
        else:
            st.write(f"System message: {message.content}") # システムメッセージを表示

    # Costを表示（サイドバー）
    costs = st.session_state.get("costs", [])
    st.sidebar.markdown("## Costs")
    st.sidebar.markdown(f"**Total cost: ${sum(costs):.5f}**")
    for cost in costs:
        st.sidebar.markdown(f"- ${cost:.5f}")
            

if __name__ == "__main__":
    main()