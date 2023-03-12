import openai
from io import BytesIO
import streamlit as st
st.set_page_config(page_title="xiaohaiteng",page_icon=":shark:" ,layout="wide")


import streamlit as st



keys=['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',
'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',
'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',
'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',
'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',
'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',
'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',
'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',
'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',
'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',
'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']


models = {
        "gpt-3.5-turbo": "gpt-3.5-turbo",
        "gpt-3.5-turbo-0301": "gpt-3.5-turbo-0301",
    }
# 添加菜单

def generate_response(prompt, model, index):
    openai.api_key = index
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ])

    message = response['choices'][0]['message']['content']
    # message = response.choices[0].text.strip()
    return message


def get_state():
    return {"chat_history": []}


def save_chat_history(chat_history):
    data = "\n".join(chat_history)
    b = BytesIO(data.encode())
    return st.download_button(label="Download chat history", data=b, file_name="chat_history.txt",
                              mime="text/plain")



menu = ["主页", "旁白"]
choice = st.sidebar.selectbox("主页", menu)












if "state" not in st.session_state:
    st.session_state.state = get_state()

if choice == "主页":
    if "state" not in st.session_state:
        st.session_state.state = get_state()

    col1, col2,col3= st.container(),st.container(),st.container()
    st.title("")

    with col2:
        st.header("对话")
        message = st.text_area(":shark:", height=100, value="", key="input")
        coll1,coll2,coll3=st.columns(3)
        with coll1:
            if st.button("发送",use_container_width=True):
                chat_history = st.session_state.state["chat_history"]
                # 清除重复聊天记录
                chat_history.append("You: " + message) if "You: " + message not in chat_history else chat_history.append(
                    "You: " + "")
                index = len(chat_history) % len(keys)  # 使用取模操作来循环使用API key
                if "model" not in st.session_state:
                        st.session_state.model =models[0]
                response = generate_response("\n".join(chat_history), models[st.session_state.model],keys[index])
                chat_history.append("ChatGPT: " + response)
                st.session_state.state["chat_history"] = chat_history

        with coll2:
            if st.button("保存聊天记录",use_container_width=True):
                st.write(save_chat_history(st.session_state.state["chat_history"]), unsafe_allow_html=True)
        with coll3:
            if st.button("重开一个对话",use_container_width=True):
                st.session_state.state = get_state()

        keys=[]
        with st.expander("配置项"):
            model = st.selectbox("选择模型", list(models.keys()),key="model")





                # 添加博客链接
            st.markdown("""
                <div style="text-align:center;">
        <a class="link" href="https://yang1he.gitee.io" target="_blank">作者链接</a>
    </div>
                """, unsafe_allow_html=True)
    with col1:
        st.header("聊天记录")
        for msg in st.session_state.state["chat_history"]:
            st.markdown("---")
            st.write(msg)
    # 计数功能
    with col3:
        chat_count = sum(1 for item in st.session_state.state["chat_history"] if isinstance(item, str)
                     or (isinstance(item, dict)
                         and any(isinstance(value, str)
                                 for value in item.values())))
        str_count=len(str(st.session_state.state["chat_history"]))
        col1, col2 = st.columns(2)
        col1.metric("交流总字数", str_count-2,"")
        col2.metric("对话数", chat_count,"")

elif choice == "旁白":
    st.write("小海豚的专属chatgpt")
    st.empty()

