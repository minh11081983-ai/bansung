import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Aim Trainer Pro - Streamlit",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Thêm CSS tùy chỉnh cho giao diện Streamlit
st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    h1, h2, h3 {
        color: #38bdf8 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar hướng dẫn & cài đặt
with st.sidebar:
    st.title("🎯 Aim Trainer Pro")
    st.write("Game luyện tập phản xạ và kỹ năng lia súng (Flick Shot / Tracking) trên Streamlit!")
    st.markdown("---")
    st.subheader("🎮 Hướng dẫn chơi")
    st.write("1. Nhấn nút **BẮT ĐẦU** ở màn hình game.")
    st.write("2. Bắn vào các **Mục tiêu đỏ** nhanh và chính xác nhất có thể.")
    st.write("3. Duy trì **Combo** để nhân đôi/nhân ba điểm số.")
    st.write("4. Game kết thúc khi hết 30 giây.")
    st.markdown("---")
    st.info("💡 **Mẹo:** Bắn trúng tâm mục tiêu lớn để tích điểm nhanh hơn, không bắn trượt ra ngoài để tránh bị tụt phần trăm độ chính xác!")

st.title("🎯 Game Luyện Tập Lia Súng (Aim Trainer)")

# Mã nguồn HTML5 + Canvas + JS nhúng trực tiếp vào Streamlit
game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
    * {
        box-sizing: border-box;
        user-select: none;
        margin: 0;
        padding: 0;
    }
    body {
        background-color: #0b0f19;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        overflow: hidden;
    }
    #game-container {
        position: relative;
        width: 900px;
        height: 600px;
        box-shadow: 0 0 30px rgba(56, 189, 248, 0.3);
        border-radius: 12px;
        overflow: hidden;
        border: 2px solid #1e293b;
        background: radial-gradient(circle at center, #1e293b 0%, #0f172a 100%);
    }
    canvas {
        display: block;
        cursor: crosshair;
    }
    .hud {
        position: absolute;
        top: 15px;
        left: 20px;
        right: 20px;
        display: flex;
        justify-content: space-between;
        pointer-events: none;
        font-size: 18px;
        font-weight: bold;
        color: #f8fafc;
        text-shadow: 0 2px 4px rgba(0,0,0,0.8);
        z-index: 10;
    }
    .hud-item {
        background: rgba(15, 23, 42, 0.7);
        padding: 8px 16px;
        border-radius: 8px;
        border: 1px solid rgba(56, 189, 248, 0.2);
    }
    .hud-val {
        color: #38bdf8;
        font-size: 22px;
    }
    #menu-overlay {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(5px);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
        z-index: 20;
    }
    h1 {
        font-size: 42px;
        margin-bottom: 10px;
        color: #38bdf8;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    p {
        color: #94a3b8;
        margin-bottom: 25px;
        font-size: 16px;
    }
    .btn {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        color: white;
        border: none;
        padding: 14px 40px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 30px;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4);
    }
    .btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(2, 132, 199, 0.6);
        background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%);
    }
    .btn:active {
        transform: translateY(1px);
    }
    .stats-card {
        background: rgba(30, 41, 59, 0.8);
        padding: 20px 40px;
        border-radius: 12px;
        margin-bottom: 25px;
        border: 1px solid #334155;
        text-align: center;
    }
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        margin-top: 10px;
    }
    .stat-box {
        display: flex;
        flex-direction: column;
    }
    .stat-label {
        font-size: 14px;
        color: #94a3b8;
    }
    .stat-number {
        font-size: 26px;
        color: #f43f5e;
        font-weight: bold;
    }
</style>
</head>
<body>

<div id="game-container">
    <div class="hud">
        <div class="hud-item">ĐIỂM: <span id="score" class="hud-val">0</span></div>
        <div class="hud-item">COMBO: <span id="combo" class="hud-val">x1</span></div>
        <div class="hud-item">ĐỘ CHÍNH XÁC: <span id="accuracy" class="hud-val">100%</span></div>
        <div class="hud-item">THỜI GIAN: <span id="time" class="hud-val">30</span>s</div>
    </div>

    <div id="menu-overlay">
        <h1 id="menu-title">AIM TRAINER PRO</h1>
        <p id="menu-subtitle">Rèn luyện khả năng phản xạ & lia súng góc nhìn chuẩn Esports</p>
        
        <div id="final-stats" class="stats-card" style="display: none;">
            <h3>KẾT QUẢ TRẬN ĐẤU</h3>
            <div class="stats-grid">
                <div class="stat-box">
                    <span class="stat-label">Tổng Điểm</span>
                    <span id="final-score" class="stat-number">0</span>
                </div>
                <div class="stat-box">
                    <span class="stat-label">Chính Xác</span>
                    <span id="final-acc" class="stat-number">0%</span>
                </div>
                <div class="stat-box">
                    <span class="stat-label">Trúng / Bắn</span>
                    <span id="final-shots" class="stat-number">0/0</span>
                </div>
            </div>
        </div>

        <button id="start-btn" class="btn" onclick="startGame()">BẮT ĐẦU CHƠI</button>
    </div>

    <canvas id="gameCanvas" width="900" height="600"></canvas>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Web Audio API để phát tiếng súng và tiếng trúng bia không lag
const AudioContext = window.AudioContext || window.webkitAudioContext;
let audioCtx = null;

function playSound(type) {
    if (!audioCtx) audioCtx = new AudioContext();
    if (audioCtx.state === 'suspended') audioCtx.resume();

    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.connect(gain);
    gain.connect(audioCtx.destination);

    const now = audioCtx.currentTime;

    if (type === 'hit') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(800, now);
        osc.frequency.exponentialRampToValueAtTime(400, now + 0.08);
        gain.gain.setValueAtTime(0.3, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.08);
        osc.start(now);
        osc.stop(now + 0.08);
    } else if (type === 'miss') {
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(150, now);
        osc.frequency.linearRampToValueAtTime(60, now + 0.1);
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.1);
        osc.start(now);
        osc.stop(now + 0.1);
    }
}

// Biến trạng thái Game
let gameState = 'MENU'; // MENU, PLAYING, END
let score = 0;
let combo = 0;
let totalShots = 0;
let hits = 0;
let timeLeft = 30;
let timerInterval = null;

// Đối tượng & Particles
let targets = [];
let particles = [];
let floatingTexts = [];

class Target {
    constructor() {
        this.radius = Math.random() * 12 + 18; // Kích thước từ 18-30px
        this.x = Math.random() * (canvas.width - this.radius * 4) + this.radius * 2;
        this.y = Math.random() * (canvas.height - this.radius * 4 - 80) + this.radius * 2 + 60;
        this.spawnTime = Date.now();
        this.maxLife = 2000; // Mục tiêu tự biến mất sau 2 giây
        this.scale = 0;
    }

    draw() {
        // Hiệu ứng phóng to khi xuất hiện
        if (this.scale < 1) {
            this.scale += 0.1;
        }

        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.scale(this.scale, this.scale);

        // Vòng ngoài
        ctx.beginPath();
        ctx.arc(0, 0, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = '#f43f5e';
        ctx.fill();
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Vòng trong
        ctx.beginPath();
        ctx.arc(0, 0, this.radius * 0.6, 0, Math.PI * 2);
        ctx.fillStyle = '#ffffff';
        ctx.fill();

        // Tâm đỏ
        ctx.beginPath();
        ctx.arc(0, 0, this.radius * 0.3, 0, Math.PI * 2);
        ctx.fillStyle = '#f43f5e';
        ctx.fill();

        ctx.restore();
    }
}

class Particle {
    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.color = color;
        this.radius = Math.random() * 3 + 2;
        this.vx = (Math.random() - 0.5) * 8;
        this.vy = (Math.random() - 0.5) * 8;
        this.alpha = 1;
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;
        this.alpha -= 0.04;
    }

    draw() {
        ctx.save();
        ctx.globalAlpha = this.alpha;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
        ctx.restore();
    }
}

class FloatingText {
    constructor(text, x, y, color) {
        this.text = text;
        this.x = x;
        this.y = y;
        this.color = color;
        this.alpha = 1;
        this.vy = -2;
    }

    update() {
        this.y += this.vy;
        this.alpha -= 0.03;
    }

    draw() {
        ctx.save();
        ctx.globalAlpha = this.alpha;
        ctx.font = 'bold 20px Segoe UI';
        ctx.fillStyle = this.color;
        ctx.fillText(this.text, this.x - 15, this.y);
        ctx.restore();
    }
}

function spawnTargets(count = 3) {
    while (targets.length < count) {
        targets.push(new Target());
    }
}

function updateHUD() {
    document.getElementById('score').innerText = score;
    document.getElementById('combo').innerText = 'x' + Math.max(1, combo);
    const acc = totalShots > 0 ? Math.round((hits / totalShots) * 100) : 100;
    document.getElementById('accuracy').innerText = acc + '%';
    document.getElementById('time').innerText = timeLeft;
}

function startGame() {
    score = 0;
    combo = 0;
    totalShots = 0;
    hits = 0;
    timeLeft = 30;
    targets = [];
    particles = [];
    floatingTexts = [];
    gameState = 'PLAYING';

    document.getElementById('menu-overlay').style.display = 'none';
    updateHUD();

    spawnTargets(4);

    clearInterval(timerInterval);
    timerInterval = setInterval(() => {
        timeLeft--;
        updateHUD();
        if (timeLeft <= 0) {
            endGame();
        }
    }, 1000);
}

function endGame() {
    gameState = 'END';
    clearInterval(timerInterval);

    document.getElementById('menu-overlay').style.display = 'flex';
    document.getElementById('menu-title').innerText = 'KẾT THÚC!';
    document.getElementById('menu-subtitle').innerText = 'Bạn đã hoàn thành lượt tập luyện.';
    document.getElementById('start-btn').innerText = 'CHƠI LẠI';

    const acc = totalShots > 0 ? Math.round((hits / totalShots) * 100) : 0;
    document.getElementById('final-score').innerText = score;
    document.getElementById('final-acc').innerText = acc + '%';
    document.getElementById('final-shots').innerText = hits + '/' + totalShots;
    document.getElementById('final-stats').style.display = 'block';
}

// Xử lý bắn (Mouse Click)
canvas.addEventListener('mousedown', (e) => {
    if (gameState !== 'PLAYING') return;

    const rect = canvas.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;

    totalShots++;
    let hitAny = false;

    for (let i = targets.length - 1; i >= 0; i--) {
        const t = targets[i];
        const dist = Math.hypot(mouseX - t.x, mouseY - t.y);

        if (dist <= t.radius) {
            hitAny = true;
            hits++;
            combo++;

            // Điểm tính theo tốc độ và nhân combo
            const addedScore = 100 * Math.max(1, combo);
            score += addedScore;

            playSound('hit');

            // Tạo hiệu ứng nổ vỡ hạt
            for (let p = 0; p < 12; p++) {
                particles.push(new Particle(t.x, t.y, '#f43f5e'));
            }

            // Text nổi điểm số
            floatingTexts.push(new FloatingText('+' + addedScore, t.x, t.y, '#38bdf8'));

            // Xóa bia cũ & tạo bia mới
            targets.splice(i, 1);
            spawnTargets(4);
            break;
        }
    }

    if (!hitAny) {
        combo = 0;
        playSound('miss');
        floatingTexts.push(new FloatingText('MISS', mouseX, mouseY, '#ef4444'));
    }

    updateHUD();
});

// Vòng lặp Render (Game Loop)
function gameLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Bật lưới tọa độ trang trí cho background
    ctx.strokeStyle = 'rgba(51, 65, 85, 0.2)';
    ctx.lineWidth = 1;
    for (let x = 0; x < canvas.width; x += 40) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
    }
    for (let y = 0; y < canvas.height; y += 40) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
    }

    if (gameState === 'PLAYING') {
        // Kiểm tra thời gian tồn tại bia
        const now = Date.now();
        for (let i = targets.length - 1; i >= 0; i--) {
            if (now - targets[i].spawnTime > targets[i].maxLife) {
                targets.splice(i, 1);
                combo = 0; // Hết giờ tự biến mất thì gãy combo
                updateHUD();
            }
        }
        spawnTargets(4);

        // Vẽ targets
        targets.forEach(t => t.draw());

        // Update và vẽ Hạt hiệu ứng
        for (let i = particles.length - 1; i >= 0; i--) {
            particles[i].update();
            particles[i].draw();
            if (particles[i].alpha <= 0) particles.splice(i, 1);
        }

        // Update và vẽ Text nổi
        for (let i = floatingTexts.length - 1; i >= 0; i--) {
            floatingTexts[i].update();
            floatingTexts[i].draw();
            if (floatingTexts[i].alpha <= 0) floatingTexts.splice(i, 1);
        }
    }

    requestAnimationFrame(gameLoop);
}

gameLoop();
</script>
</body>
</html>
"""

# Nhúng HTML/JS Game vào giao diện Streamlit với chiều cao 650px
components.html(game_html, height=650)
