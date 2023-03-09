import openai
from io import BytesIO
import streamlit as st
st.set_page_config(page_title="Your App", layout="wide")


import streamlit as st


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



menu = ["主页", "开发历史"]
choice = st.sidebar.selectbox("主页", menu)










def main():
    if "state" not in st.session_state:
        st.session_state.state = get_state()

    if choice == "主页":
        if "state" not in st.session_state:
            st.session_state.state = get_state()

        col1, col2,col3= st.container(),st.container(),st.container()
        st.title("")

        with col2:
            st.header("对话")
            keys=[]
            message = st.text_area("You", height=100, value="", key="input")
            with st.expander("配置项"):
                model = st.selectbox("选择模型", list(models.keys()))
                st.write("输入你的openai-key,并回车")
                api_key1,api_key2,api_key3 = st.text_input("api-key1"),st.text_input("api-key2"),st.text_input("api-key3")
                keys = [key for key in [api_key1, api_key2, api_key3] if key] # 如果存在就加进去
                st.write(keys)



            coll1,coll2,coll3=st.columns(3)
            with coll1:
                if st.button("发送",use_container_width=True):
                    chat_history = st.session_state.state["chat_history"]
                    # 清除重复聊天记录
                    chat_history.append("You: " + message) if "You: " + message not in chat_history else chat_history.append(
                        "You: " + "")
                    index = len(chat_history) % len(keys)  # 使用取模操作来循环使用API key

                    response = generate_response("\n".join(chat_history), models[model], keys[index])
                    chat_history.append("ChatGPT: " + response)
                    st.session_state.state["chat_history"] = chat_history

            with coll2:
                if st.button("保存聊天记录",use_container_width=True):
                    st.write(save_chat_history(st.session_state.state["chat_history"]), unsafe_allow_html=True)
            with coll3:
                if st.button("重开一个对话",use_container_width=True):
                    st.session_state.state = get_state()
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
        with col3:
            chat_count = sum(1 for item in st.session_state.state["chat_history"] if isinstance(item, str)
                         or (isinstance(item, dict)
                             and any(isinstance(value, str)
                                     for value in item.values())))
            str_count=len(str(st.session_state.state["chat_history"]))
            col1, col2 = st.columns(2)
            col1.metric("交流总字数", str_count-2,"")
            col2.metric("对话数", chat_count,"")


    elif choice == "开发历史":
        st.title("2023年3月3：开始开发 ChatGPT Web")
        st.write("[2022年3月4：ChatGPT web v0.1.0 版本发布](https://gitee.com/yang1he/chatgpt-web-app)")
        st.write("[2022年3月5：ChatGPT web v0.2 版本发布](https://gitee.com/yang1he/chatgpt-web2-app)")
        st.write("[2022年3月6：ChatGPT web v0.3.0 版本发布](https://gitee.com/yang1he/chatgpt-web3-app)")
        st.write("[2022年3月6：ChatGPT web 需多key版](https://gitee.com/yang1he/chatgpt-web3-app)")
        st.empty()


if __name__ == "__main__":
    main()  # 调用主函数开始Streamlit应用
