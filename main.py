import streamlit as st

# ========== 1. 分类菜单+价格 ==========
menu_categories = {
    "🍽️ 招牌菜": {"蜜汁叉烧饭": 22, "黑椒牛柳意面": 28, "香辣烤鱼": 38, "宫保鸡丁": 25},
    "🍟 小吃": {"薯条": 12, "鸡块": 15, "炸牛奶": 18, "洋葱圈": 10},
    "🥤 饮品": {"可乐": 6, "柠檬水": 8, "珍珠奶茶": 15, "柠檬红茶": 12},
    "🍚 主食": {"卤肉饭": 20, "番茄鸡蛋面": 18, "牛肉炒饭": 26, "炸酱面": 16}
}

# 合并所有菜品
all_dishes = {}
for cat in menu_categories.values():
    all_dishes.update(cat)


# ========== 2. 优惠活动规则 ==========
def calculate_discount(total_price):
    if total_price >= 80:
        discount = 20
    elif total_price >= 50:
        discount = 10
    else:
        discount = 0
    final_price = total_price - discount
    return discount, final_price


# ========== 3. 初始化会话状态 ==========
if "cart" not in st.session_state:
    st.session_state.cart = []
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant",
         "content": "你好！我是智能点餐助手～\n可点击左侧菜单点菜，也可以直接跟我说！\n🎁 优惠：满50减10，满80减20"}
    ]

# ========== 页面配置 ==========
st.set_page_config(page_title="智能点餐-含优惠活动", page_icon="🍽️")
st.title("🍽️ 智能点餐助手 | 含优惠活动")

# 聊天记录展示
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ========== 侧边栏：分类菜单 + 订单 + 优惠 ==========
with st.sidebar:
    st.title("📋 菜单分类")

    # 可交互分类菜单
    for cat_name, dishes in menu_categories.items():
        with st.expander(cat_name, expanded=False):
            for dish, price in dishes.items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"{dish}")
                with col2:
                    st.write(f"¥{price}")
                # 点菜按钮
                if st.button(f"➕ 点这个", key=dish, use_container_width=True):
                    st.session_state.cart.append(dish)
                    st.session_state.messages.append({
                        "role": "user", "content": f"我要一份 {dish}"
                    })
                    st.session_state.messages.append({
                        "role": "assistant", "content": f"✅ 已加：{dish}（¥{price}）"
                    })
                    st.rerun()

    st.divider()

    # 优惠活动说明
    st.info("🎁 优惠活动\n• 满50元 减10元\n• 满80元 减20元")
    st.divider()

    # 订单清单 & 价格&优惠计算
    st.title("🛒 我的订单")
    if not st.session_state.cart:
        st.write("暂无菜品")
    else:
        original_total = 0
        for dish in st.session_state.cart:
            p = all_dishes[dish]
            original_total += p
            st.write(f"• {dish}  ¥{p}")

        # 计算优惠
        discount, final_total = calculate_discount(original_total)
        st.divider()
        st.write(f"💰 原价合计：¥{original_total}")
        st.write(f"🎁 优惠减免：-¥{discount}")
        st.subheader(f"✅ 实付总价：¥{final_total}")

    # 清空订单按钮
    if st.button("🗑️ 清空订单", use_container_width=True):
        st.session_state.cart = []
        st.rerun()

# ========== 对话框输入逻辑 ==========
user_input = st.chat_input("输入菜名、推荐、菜单、下单")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    reply = ""

    # 下单指令
    if "下单" in user_input:
        original = sum([all_dishes[d] for d in st.session_state.cart])
        disc, final = calculate_discount(original)
        reply = f"✅ 订单已确认！\n原价：¥{original}  优惠：减¥{disc}\n实付：¥{final}\n请呼叫店员为您确认订单并结账～"

    # 菜品推荐
    elif "辣" in user_input:
        reply = "推荐辣菜：\n• 香辣烤鱼 ¥38\n• 宫保鸡丁 ¥25"
    elif "清淡" in user_input:
        reply = "推荐清淡：\n• 番茄鸡蛋面 ¥18\n• 柠檬水 ¥8"
    elif "小吃" in user_input:
        reply = "推荐小吃：\n• 薯条 ¥12\n• 鸡块 ¥15"
    elif "推荐" in user_input:
        reply = "今日推荐：蜜汁叉烧饭 + 柠檬红茶，好吃不贵～"

    # 查看菜单
    elif "菜单" in user_input:
        reply = "📋 完整分类菜单已展示在左侧，可直接点击加号点菜哦！"

    # 文字点菜
    else:
        matched = False
        for d in all_dishes:
            if d in user_input:
                st.session_state.cart.append(d)
                reply = f"✅ 已为您加单：{dish}（¥{all_dishes[d]}）"
                matched = True
                break
        if not matched:
            reply = "我没听懂哦～可以点左侧菜单，或说菜名、推荐、下单"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)