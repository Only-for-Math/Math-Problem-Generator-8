import streamlit as st
import streamlit.components.v1 as components
import random
import json
import urllib.request
import base64
import time

# ==========================================
# [기능] GitHub 방문자 카운터 (API 이용)
# ==========================================
def update_github_visitor_count():
    if st.session_state.get('counted_visit', False):
        return

    try:
        token = st.secrets["GITHUB_TOKEN"]
        repo = st.secrets["GITHUB_REPO"]
        file_path = st.secrets.get("GITHUB_FILE_PATH", "visitor_count.txt")

        url = f"https://api.github.com/repos/{repo}/contents/{file_path}"
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Streamlit-App"
        }

        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            sha = data["sha"]
            content_b64 = data["content"]
            current_str = base64.b64decode(content_b64).decode('utf-8').strip()
            count = int(current_str) if current_str.isdigit() else 0

        new_count = count + 1
        new_content_b64 = base64.b64encode(str(new_count).encode('utf-8')).decode('utf-8')

        update_data = {
            "message": f"Update visitor count to {new_count}",
            "content": new_content_b64,
            "sha": sha
        }

        req_put = urllib.request.Request(
            url, 
            data=json.dumps(update_data).encode('utf-8'), 
            headers=headers, 
            method="PUT"
        )
        with urllib.request.urlopen(req_put) as response:
            pass

        st.session_state['counted_visit'] = True
    except Exception as e:
        pass # 카운터 오류 시 무시

update_github_visitor_count()

# ==========================================
# [중1] 일반 수준 (일차방정식, 식의 값, 비례식, 평균)
# ==========================================
def g1_linear(target):
    a, c = random.sample(range(-5, 6), 2)
    while a == c or a == 0 or c == 0:
        a, c = random.sample(range(-5, 6), 2)
    b = random.randint(-5, 5)
    d = a * target + b - c * target
    
    def fmt(coef, const):
        c_str = f"{coef}x" if abs(coef) != 1 else ("x" if coef == 1 else "-x")
        if const > 0: return f"{c_str}+{const}"
        elif const < 0: return f"{c_str}-{abs(const)}"
        return c_str

    q = f"다음 방정식의 해 $x$를 구하시오.\n\n$${fmt(a, b)}={fmt(c, d)}$$"
    exp = f"이항하여 정리하면:\n\n$${a-c}x={d-b}$$\n\n따라서 $x={target}$"
    return q, exp, str(target)

def g1_expr(target):
    x_val = random.choice([-2, -1, 2, 3])
    a = random.randint(2, 5)
    b = target - a * x_val
    b_str = f"+{b}" if b > 0 else (f"-{abs(b)}" if b < 0 else "")
    
    q = f"$x={x_val}$ 일 때, 다음 식의 값을 구하시오.\n\n$${a}x{b_str}$$"
    exp = f"식에 대입하면:\n\n$${a}\\times({x_val}){b_str}={target}$$"
    return q, exp, str(target)

def g1_prop(target):
    b = random.choice([3, 6, 9])
    c = random.randint(2, 5)
    val = b * c // 3
    a = val - target
    a_str = f"+{a}" if a > 0 else (f"-{abs(a)}" if a < 0 else "")
    
    q = f"다음 비례식을 만족하는 $x$의 값을 구하시오.\n\n$$(x{a_str}):{b}={c}:3$$"
    exp = f"내항의 곱과 외항의 곱은 같으므로:\n\n$$3(x{a_str})={b * c}$$\n\n$$3x{f'+{3*a}' if a>0 else f'-{abs(3*a)}'}={b*c}$$\n\n따라서 $x={target}$"
    return q, exp, str(target)

def g1_stat(target):
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    total = a + b + target
    while total % 3 != 0:
        b += 1
        total = a + b + target
    avg = total // 3
    
    q = f"세 수 ${a}, {b}, x$ 의 평균이 ${avg}$일 때, $x$의 값을 구하시오."
    exp = f"평균을 구하는 식을 세우면:\n\n$$\\frac{{{a}+{b}+x}}{{3}}={avg}$$\n\n$${a+b}+x={avg * 3}$$\n\n따라서 $x={target}$"
    return q, exp, str(target)

# ==========================================
# [중2] 심화 수준 (계수 복잡화, 두 점 지나는 직선 등)
# ==========================================
def g2_sys(target):
    x = random.randint(-4, 4)
    y = target - x
    a = 3*x - 4*y
    b = 5*x + 2*y
    
    q = f"다음 연립방정식의 해를 $x, y$라 할 때, $x+y$ 의 값을 구하시오.\n\n$$\\begin{{cases}}3x-4y={a}\\\\5x+2y={b}\\end{{cases}}$$"
    exp = f"두 번째 식에 2를 곱하여 첫 번째 식과 더하면 $13x = {a + 2*b}$ 이므로 $x={x}$ 입니다.\n\n$x$를 대입하여 풀면 $y={y}$ 가 나옵니다.\n\n따라서 $x+y={target}$"
    return q, exp, str(target)

def g2_func(target):
    slope = random.choice([-3, -2, 2, 3])
    x1 = random.randint(-3, 3)
    y1 = slope * x1 + target 
    x2 = x1 + random.choice([1, 2])
    y2 = slope * x2 + target
    
    q = f"두 점 $({x1}, {y1})$, $({x2}, {y2})$를 지나는 직선의 $y$절편을 구하시오."
    exp = f"직선의 기울기는 $a = \\frac{{{y2}-({y1})}}{{{x2}-({x1})}} = {slope}$ 입니다.\n\n함수식을 $y={slope}x+b$ 로 두고 점 $({x1}, {y1})$을 대입하면:\n\n$${y1}={slope}\\times({x1})+b$$\n\n따라서 $y$절편은 $b={target}$"
    return q, exp, str(target)

def g2_exp(target):
    a = random.randint(3, 6)
    b = random.randint(2, 5)
    c = 2*a + 3*b - target
    
    q = f"다음 등식을 만족하는 $x$의 값을 구하시오.\n\n$$(4^{{{a}}}\\times 8^{{{b}}})\\div 2^{{{c}}}=2^x$$"
    exp = f"밑을 $2$로 통일하면 $4 = 2^2, 8 = 2^3$ 이므로:\n\n$$(2^{{{2*a}}}\\times 2^{{{3*b}}})\\div 2^{{{c}}}=2^x$$\n\n지수법칙에 의해 지수끼리 계산하면:\n\n$$x={2*a}+{3*b}-{c}={target}$$"
    return q, exp, str(target)

def g2_ineq(target):
    a = random.randint(1, 3)
    b = random.randint(1, 3)
    upper_bound = target + 1
    c = upper_bound - 3*a - 2*b
    
    q = f"다음 부등식을 만족하는 가장 큰 정수 $x$의 값을 구하시오.\n\n$$\\frac{{x-{a}}}{{2}} - \\frac{{x+{b}}}{{3}} < \\frac{{{c}}}{{6}}$$"
    exp = f"양변에 분모의 최소공배수인 $6$을 곱하면:\n\n$$3(x-{a}) - 2(x+{b}) < {c}$$\n\n$$3x - {3*a} - 2x - {2*b} < {c}$$\n\n$$x - {3*a+2*b} < {c}$$\n\n$$x < {upper_bound}$$\n\n이 범위를 만족하는 가장 큰 정수는 ${target}$입니다."
    return q, exp, str(target)

# ==========================================
# [중3] 난이도 하향 조정 (기본 계산 위주)
# ==========================================
def g3_trigo(target):
    a = target - 2
    a_str = f"+{a}" if a > 0 else (f"-{abs(a)}" if a < 0 else "")
    
    q = f"다음 식의 값을 구하시오.\n\n$$\\tan 45^\\circ + 2\\sin 30^\\circ {a_str}$$"
    exp = f"각 삼각비의 값을 대입하면 $\\tan 45^\\circ=1$, $\\sin 30^\\circ=\\frac{{1}}{{2}}$ 이므로:\n\n$$1 + 2 \\times \\frac{{1}}{{2}} {a_str}$$\n\n$$= 1 + 1 {a_str} = 2 {a_str} = {target}$$"
    return q, exp, str(target)

def g3_quad_func(target):
    p = random.choice([2, -2, 3, -3])
    b = 2 * p
    c = - (p**2) + target
    b_str = f"+{b}x" if b > 0 else (f"-{abs(b)}x" if b < 0 else "")
    c_str = f"+{c}" if c > 0 else (f"-{abs(c)}" if c < 0 else "")
    
    q = f"이차함수 $y=-x^2 {b_str} {c_str}$ 의 최댓값을 구하시오."
    exp = f"이차함수 식을 완전제곱꼴로 변형하면:\n\n$$y=-(x^2 - {2*p}x) {c_str}$$\n\n$$y=-(x - {p})^2 + {p**2} {c_str}$$\n\n$$y=-(x - {p})^2 + {target}$$\n\n$x^2$의 계수가 음수이므로, 이 함수는 $x={p}$ 일 때 최댓값 ${target}$을 가집니다."
    return q, exp, str(target)

def g3_sqrt(target):
    offset = target - 1
    off_str = f"+{offset}" if offset > 0 else (f"-{abs(offset)}" if offset < 0 else "")
    
    q = f"다음 식을 간단히 하여 값을 구하시오. (단, $2 < \\sqrt{{5}} < 3$)\n\n$$\\sqrt{{(3 - \\sqrt{{5}})^2}} + \\sqrt{{(2 - \\sqrt{{5}})^2}} {off_str}$$"
    exp = f"$\\sqrt{{5}} < 3$ 이므로 $3 - \\sqrt{{5}} > 0$ 입니다.\n\n$\\sqrt{{5}} > 2$ 이므로 $2 - \\sqrt{{5}} < 0$ 입니다.\n\n따라서 근호 안의 부호에 따라 식을 정리하면:\n\n$$(3 - \\sqrt{{5}}) - (2 - \\sqrt{{5}}) {off_str} = 3 - \\sqrt{{5}} - 2 + \\sqrt{{5}} {off_str} = 1 {off_str} = {target}$$"
    return q, exp, str(target)

def g3_advanced(target):
    b = random.randint(2, 4)
    a = b**2 - 1 
    c = target + 1
    c_str = f"+{c}" if c > 0 else (f"-{abs(c)}" if c < 0 else "")
    
    q = f"$$x = {b} + \\sqrt{{{a}}}$$ 일 때, 다음 식의 값을 구하시오.\n\n$$x^2 - {2*b}x {c_str}$$"
    exp = f"식 $x = {b} + \\sqrt{{{a}}}$ 에서 ${b}$를 이항하면:\n\n$$x - {b} = \\sqrt{{{a}}}$$\n\n양변을 제곱하면:\n\n$$(x - {b})^2 = {a}$$\n\n$$x^2 - {2*b}x + {b**2} = {a} \\implies x^2 - {2*b}x = {a} - {b**2} = -1$$\n\n주어진 식에 대입하면 $-1 {c_str} = {target}$"
    return q, exp, str(target)

def generate_problems(grade):
    if grade == 1:
        funcs = [g1_linear, g1_expr, g1_prop, g1_stat]
        title = "[ 중학교 1학년 수학 ]"
    elif grade == 2:
        funcs = [g2_sys, g2_func, g2_exp, g2_ineq]
        title = "[ 중학교 2학년 수학 (심화) ]"
    else:
        funcs = [g3_trigo, g3_quad_func, g3_sqrt, g3_advanced]
        title = "[ 중학교 3학년 수학 ]"
        
    target = 15
    selected_func = random.choice(funcs)
    return title, [selected_func(target)]

# ==========================================
# Streamlit 메인 로직 및 GUI 구성
# ==========================================
st.set_page_config(page_title="공룡시대 문제 1", layout="centered")

if 'step' not in st.session_state:
    st.session_state.step = 'select' 
    st.session_state.problems = []
    st.session_state.title = ""
    st.session_state.is_dev_mode = False
    st.session_state.start_time = 0.0

# --- 화면 1: 학년 선택 ---
if st.session_state.step == 'select':
    st.markdown("## 공룡시대 문제 1")
    st.write("문제를 풀 학년을 선택하세요. (제한 시간 1분!)")
    
    col1, col2, col3 = st.columns(3)
    if col1.button("중1 문제 시작", use_container_width=True):
        st.session_state.title, st.session_state.problems = generate_problems(1)
        st.session_state.start_time = time.time()
        st.session_state.step = 'solve'
        st.rerun()
    if col2.button("중2 문제 시작", use_container_width=True):
        st.session_state.title, st.session_state.problems = generate_problems(2)
        st.session_state.start_time = time.time()
        st.session_state.step = 'solve'
        st.rerun()
    if col3.button("중3 문제 시작", use_container_width=True):
        st.session_state.title, st.session_state.problems = generate_problems(3)
        st.session_state.start_time = time.time()
        st.session_state.step = 'solve'
        st.rerun()

    st.write("")
    st.write("")
    st.write("")
    st.session_state.is_dev_mode = st.checkbox("개발자 옵션 (정답 및 풀이 확인 기능 켜기)", value=st.session_state.is_dev_mode)

# --- 화면 2: 문제 풀이 (타이머 + 단일 문제 출력) ---
elif st.session_state.step == 'solve':
    current_q, current_exp, current_ans = st.session_state.problems[0]
    
    # 남은 시간 계산
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(60 - elapsed, 0)
    
    # 카운트다운 타이머 UI (HTML/JS 주입)
    timer_html = f"""
    <div id="timer_box" style="font-family: sans-serif; font-size: 20px; font-weight: bold; color: {'#ff4b4b' if remaining <= 10 else '#1f1f1f'}; text-align: center; padding: 12px; background-color: {'#ffe6e6' if remaining <= 10 else '#f0f2f6'}; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
        ⏳ 남은 시간: <span id="time">{remaining}</span>초
    </div>
    <script>
        var timeLeft = {remaining};
        var timerElement = document.getElementById('time');
        var timerBox = document.getElementById('timer_box');
        
        var timerId = setInterval(function() {{
            timeLeft--;
            if (timeLeft <= 0) {{
                clearInterval(timerId);
                timerBox.innerHTML = "⏰ 시간 초과! (그래도 정답을 입력해 보세요)";
                timerBox.style.color = '#ff4b4b';
                timerBox.style.backgroundColor = '#ffe6e6';
            }} else {{
                timerElement.innerHTML = timeLeft;
                if (timeLeft <= 10) {{
                    timerBox.style.color = '#ff4b4b';
                    timerBox.style.backgroundColor = '#ffe6e6';
                }}
            }}
        }}, 1000);
    </script>
    """
    components.html(timer_html, height=75)
    
    st.subheader(st.session_state.title)
    st.markdown("---")
    st.markdown(current_q)
    st.write("")
    
    user_answer = st.text_input("정답을 입력하세요 (숫자만 입력):", key="user_answer")
    st.markdown("---")
    
    if st.session_state.is_dev_mode:
        is_expanded = bool(st.session_state.get("pw_single", ""))
        with st.expander("🔒 정답 및 풀이 확인 (암호 입력)", expanded=is_expanded):
            pw = st.text_input("암호를 입력하세요", type="password", key="pw_single")
            if pw == "0805":
                st.success("암호가 확인되었습니다.")
                st.markdown(f"▶ **정답:** {current_ans}")
                st.markdown(f"▶ **풀이:**\n{current_exp}")
            elif pw != "":
                st.error("암호가 올바르지 않습니다.")
            
    st.write("")
    col1, col2, col3 = st.columns([8, 2, 2])
    with col3:
        if st.button("완료 ❯", type="primary", use_container_width=True):
            # 제출 시점의 실제 소요 시간 기록
            final_elapsed = time.time() - st.session_state.start_time
            
            if user_answer.strip() == current_ans:
                if "pw_single" in st.session_state:
                    del st.session_state["pw_single"]
                st.session_state.elapsed_time = final_elapsed
                st.session_state.step = 'end'
                st.rerun()
            else:
                if final_elapsed > 60:
                    st.error("시간이 초과되었습니다! 게다가 오답이네요. 다시 집중해서 풀어보세요! ⏰")
                else:
                    st.error("오답입니다. 다시 풀어보세요!")

# --- 화면 3: 완료 화면 ---
elif st.session_state.step == 'end':
    current_ans = st.session_state.problems[0][2]
    elapsed = st.session_state.get('elapsed_time', 0)
    
    st.markdown("## 정답을 기억하세요")
    st.markdown(f"### **정답: {current_ans}**") 
    
    # 시간에 따른 피드백 텍스트만 남김
    if elapsed <= 60:
        st.success(f"{int(elapsed)}초 만에 정답을 맞췄습니다!")
    else:
        st.warning(f"정답을 맞췄지만 1분을 초과했어요({int(elapsed)}초).")
    
    st.markdown("---")
