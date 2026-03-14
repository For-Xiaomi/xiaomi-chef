import streamlit as st
from datetime import datetime
import random

# --- 1. 页面基础配置 ---
st.set_page_config(page_title="小米的智能全能私厨", page_icon="👩‍🍳", layout="wide")

# --- 2. 高级感 CSS 美化 ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(180deg, #FEFCF6 0%, #FDF2F4 100%); }
    .recipe-card { 
        background: white; 
        padding: 20px; 
        border-radius: 15px; 
        border-left: 6px solid #FADADD; 
        margin-bottom: 15px; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    .recipe-card:hover { transform: translateY(-2px); }
    .section-title { color: #7A6D6D; font-size: 1.6em; font-weight: bold; margin-bottom: 15px; padding-top: 10px; }
    .stButton>button { 
        width: 100%; 
        border-radius: 25px; 
        height: 3.5em; 
        background: linear-gradient(90deg, #FADADD 0%, #BDB5D0 100%); 
        color: white !important; 
        border: none; 
        font-weight: bold; 
        font-size: 1.1em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 海量扩容数据库 ---
INGREDIENT_DB = {
    "鸡蛋": ["🍳 西红柿炒蛋(国民菜)", "🍳 虾仁蒸蛋(鲜嫩)", "🍳 韭菜炒蛋", "🍳 温泉蛋拌饭", "🍳 秋葵厚蛋烧", "🍳 糖醋荷包蛋", "🍳 葱花滑蛋"],
    "鸡肉": ["🍗 可乐鸡翅(零失败)", "🍗 奥尔良煎鸡腿排", "🍗 宫保鸡丁(少油版)", "🍗 手撕柠檬鸡", "🍗 椰子鸡汤面", "🍗 咖喱鸡块", "🍗 秘汁焖鸡翅"],
    "牛肉": ["🥩 洋葱炒肥牛", "🥩 番茄牛腩汤", "🥩 黑椒杏鲍菇牛肉粒", "🥩 杭椒炒牛柳", "🥩 肥牛寿喜烧", "🥩 土豆片炒牛肉", "🥩 滑蛋牛肉"],
    "虾/鱼": ["🍤 蒜蓉粉丝蒸虾", "🍤 白灼基围虾", "🍤 咸蛋黄大虾", "🍤 西兰花炒虾仁", "🐟 清蒸鲈鱼", "🐟 番茄鱼片汤", "🐟 柠檬煎龙利鱼"],
    "土豆": ["🥔 醋溜土豆丝", "🥔 酱汁土豆丁", "🥔 奶香土豆泥", "🥔 孜然土豆片", "🥔 咖喱土豆", "🥔 红烧土豆块"],
    "西葫芦": ["🥒 蒜蓉西葫芦", "🥒 西葫芦鸡蛋饼", "🥒 虾仁炒西葫芦", "🥒 蚝油西葫芦", "🥒 酱爆西葫芦"],
    "胡萝卜": ["🥕 胡萝卜炒蛋", "🥕 糖醋胡萝卜丝", "🥕 羊肉炖胡萝卜", "🥕 凉拌胡萝卜丝", "🥕 胡萝卜炒肉丝"],
    "白菜/娃娃菜": ["🥬 醋溜白菜", "🥬 上汤娃娃菜", "🥬 粉丝娃娃菜", "🥬 暖心白菜豆腐汤", "🥬 白菜粉丝炖冻豆腐"],
    "西兰花/花菜": ["🥦 蒜蓉西兰花", "🥦 耗油炙烤花菜", "🥦 西兰花炒蛋", "🥦 凉拌西兰花", "🥦 西兰花炒虾仁"],
    "菌菇/木耳": ["🍄 耗油杏鲍菇", "🍄 蒜香金针菇", "🍄 菌菇蛋花汤", "🍄 凉拌木耳腐竹", "🍄 椒盐平菇"],
    "豆腐": ["🍲 蛤蜊豆腐汤", "🍲 咸蛋黄豆腐", "🍲 小葱拌豆腐", "🍲 家常红烧豆腐", "🍲 煎豆腐蘸酱"],
    "茄子/黄瓜": ["🍆 蒜蓉蒸茄子", "🍆 鱼香茄子", "🥒 拍黄瓜", "🥒 黄瓜炒蛋", "🥒 黄瓜肉片"],
    "主食": ["🍜 番茄鸡蛋面", "🍜 鸡丝凉面", "🍚 黄金蛋炒饭", "🥟 鲜虾水饺", "🍝 培根意面(无猪肉用牛培根)"]
}

SPECIAL_MENUS = {
    "口味": {
        "清淡": ["白灼基围虾", "清蒸鲈鱼", "上汤娃娃菜", "冬瓜豆腐汤", "清炖土豆丁", "清炒上海青"],
        "鲜香": ["蟹黄豆腐", "蒜蓉粉丝蒸虾", "黑椒牛柳", "咖喱鸡块", "照烧鸡腿排", "蚝油生菜"],
        "麻辣": ["麻婆豆腐", "酸辣土豆丝", "辣味口水鸡", "尖椒炒肥牛", "辣子鸡丁"],
        "凉拌菜": ["拍黄瓜", "凉拌西兰花", "柠檬手撕鸡", "糖醋胡萝卜丝", "凉拌黑木耳", "凉拌皮蛋"]
    },
    "营养需求": {
        "减脂": ["清蒸龙利鱼", "白灼西兰花", "水煮鸡胸肉沙拉", "全麦荞麦面", "香煎虾仁", "紫薯燕麦"],
        "养胃": ["小米南瓜粥", "山药炖鸡汤", "暖心豆腐汤", "烂糊白菜面", "蒸水蛋", "热汤挂面"],
        "滋补": ["红枣当归鸡汤", "银耳莲子羹", "核桃奶香燕麦", "红糖姜茶", "桂圆枸杞茶"]
    },
    "餐时": {
        "早餐": ["全麦面包夹蛋", "燕麦牛奶粥", "西葫芦鸡蛋饼", "蒸山药紫薯", "牛奶玉米片"],
        "午餐": ["洋葱肥牛饭", "宫保鸡丁+糙米饭", "土豆牛肉盖饭", "清炒时蔬+鱼排", "红烧肉感素菜"],
        "晚餐": ["番茄豆腐汤", "清汤挂面", "凉拌蔬菜拼盘", "清蒸娃娃菜", "皮蛋瘦肉粥(无猪肉版)"]
    }
}

# --- 4. 纪念日计算 ---
target_date = datetime.strptime("2025-08-08", "%Y-%m-%d")
days_count = abs((datetime.now() - target_date).days)

st.title("👩‍🍳 小米的智能全能私厨")
st.markdown(f"💖 **守护小米的第 {days_count} 天 · 每一顿饭都要认真对待**")

# --- 5. 核心功能标签页 ---
tab1, tab2, tab3 = st.tabs(["🛒 冰箱寻宝", "🌈 灵感口味", "🍱 场景/营养"])

with tab1:
    user_input = st.text_input("✨ 冰箱里有什么？(空格隔开食材)：", placeholder="胡萝卜 鸡蛋 肥牛...", key="ing_input")
    
    if user_input:
        # 有输入时的精准匹配逻辑
        inputs = list(set(user_input.split())) 
        st.markdown('<div class="section-title">🍴 智能配餐灵感</div>', unsafe_allow_html=True)
        for ing in inputs:
            matched = [k for k in INGREDIENT_DB.keys() if ing in k or k in ing]
            if matched:
                key = matched[0]
                sample_num = min(len(INGREDIENT_DB[key]), 2)
                dishes = random.sample(INGREDIENT_DB[key], sample_num)
                st.markdown(f'<div class="recipe-card" style="border-left-color:#BDB5D0"><b>【{ing}】的美味建议：</b><br>{" · ".join(dishes)}</div>', unsafe_allow_html=True)
            else:
                st.info(f"🔍 还没收录【{ing}】，但推荐【蒜蓉清炒】或【鸡蛋同炒】绝不出错！")
    else:
        # 无输入时的“场景化”刷新逻辑
        st.markdown('<div class="section-title">🌟 灵感盲盒 · 治愈你的纠结</div>', unsafe_allow_html=True)
        
        # 刷新按钮：点击会导致页面重新运行，从而触发 random.choice
        if st.button("🔄 换一批方案", use_container_width=True) or 'last_dishes' not in st.session_state:
            # 方案 A: 荤素正餐 (逻辑去重)
            cat_main = random.choice(["鸡肉", "牛肉", "虾/鱼"])
            cat_veg = random.choice(["白菜/娃娃菜", "西兰花/花菜", "西葫芦", "茄子/黄瓜", "土豆"])
            plan_a = f"正式餐：{random.choice(INGREDIENT_DB[cat_main])} + {random.choice(INGREDIENT_DB[cat_veg])}"
            
            # 方案 B: 简易/轻食
            plan_b = f"轻盈餐：{random.choice(INGREDIENT_DB['鸡蛋'] + INGREDIENT_DB['豆腐'] + INGREDIENT_DB['菌菇/木耳'])}"
            
            # 方案 C: 懒人/深夜食堂 (手动设置的精品列表)
            lazy_options = [
                "🍜 番茄鸡蛋面 (暖胃神器)", "🍚 黄金蛋炒饭 (冰箱清道夫)", "🥟 汤饺/煎饺 (无需思考)", 
                "🍞 鸡蛋三明治 (5分钟出炉)", "🍜 鸡丝凉面 (爽口解腻)", "🍲 暖心豆腐汤面 (治愈疲惫)",
                "🍝 懒人意面 (简单有格调)", "🍲 肥牛小火锅 (一人份的快乐)"
            ]
            plan_c = f"懒人专区：{random.choice(lazy_options)}"
            
            st.session_state.last_dishes = [plan_a, plan_b, plan_c]
            st.toast("主厨已重新备菜！👩‍🍳")

        # 展示三个不重复场景的卡片
        col1, col2, col3 = st.columns(3)
        d = st.session_state.last_dishes
        with col1:
            st.markdown(f'<div class="recipe-card" style="border-left-color:#FADADD"><b>🍱 方案 A (有滋有味)</b><br>{d[0]}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="recipe-card" style="border-left-color:#BDB5D0"><b>🥗 方案 B (轻盈小食)</b><br>{d[1]}</div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="recipe-card" style="border-left-color:#A8DADC"><b>🌙 方案 C (懒人/深夜)</b><br>{d[2]}</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-title">😋 按口味点菜</div>', unsafe_allow_html=True)
    taste = st.selectbox("今天想吃什么味道？", ["点我选择", "清淡", "鲜香", "麻辣", "凉拌菜"])
    if taste != "点我选择":
        for dish in SPECIAL_MENUS["口味"][taste]:
            st.write(f"✨ {dish}")

with tab3:
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown('<div class="section-title">🕒 什么时候吃？</div>', unsafe_allow_html=True)
        meal_time = st.radio("场景：", ["早餐", "午餐", "晚餐"], horizontal=True)
        if st.button(f"生成{meal_time}灵感"):
            items = random.sample(SPECIAL_MENUS["餐时"][meal_time], 2)
            st.success(f"建议试试：{items[0]} 或 {items[1]}")
    with col_r:
        st.markdown('<div class="section-title">🏥 营养/特殊需求</div>', unsafe_allow_html=True)
        need = st.selectbox("现在的身体状态：", ["减脂", "养胃", "滋补"])
        if st.button("查看建议菜单"):
            st.info(f"为您准备的【{need}】方案：\n\n" + "\n\n".join([f"· {x}" for x in SPECIAL_MENUS["营养需求"][need]]))

# --- 6. 底部情感彩蛋 ---
st.markdown("---")
if st.button("🌸 小米累了/不想思考了"):
    st.snow()
    options = [
        "点个外卖，咱今天不洗碗！🍕", 
        "喝杯热牛奶，早点休息吧，我也想你了。🥛", 
        "吃个简单的番茄鸡蛋面，其实也很有营养。🍜",
        "别硬撑啦，休息也是今天的重要任务！💤"
    ]
    st.error(random.choice(options))
    st.caption("记得哦，你的快乐比做饭重要一百倍 ❤️")