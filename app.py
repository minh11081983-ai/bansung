import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Valorant Bot Aim Range - Streamlit",
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
        color: #ff4655 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar hướng dẫn & cài đặt
with st.sidebar:
    st.title("🎯 VALORANT BOT RANGE")
    st.write("Mô phỏng chế độ tập bắn Bot phòng luyện tập Valorant trên Streamlit!")
    st.markdown("---")
    st.subheader("🎮 Hướng dẫn chơi")
    st.write("1. Nhấn **BẮT ĐẦU** để vào phòng tập.")
    st.write("2. Bắn vào **ĐẦU BOT (HEADSHOT)** để hạ gục ngay lập tức & x2 điểm.")
    st.write("3. Bắn vào **THÂN BOT** cần 2 phát để hạ gục.")
    st.write("4. Súng có hiệu ứng giật (Recoil) & tia lửa nòng súng (Muzzle Flash).")
    st.markdown("---")
    st.info("💡 **Mẹo:** Rèn luyện kỹ năng kê tâm ngang đầu Bot (Crosshair Placement) để tối ưu khả năng Headshot!")

st.title("🎯 Valorant Bot Range (Luyện Lia Súng & Headshot)")

# Mã nguồn HTML5 Canvas Game
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
        box-shadow: 0 0 35px rgba(255, 70, 85, 0.4);
        border-radius: 12px;
        overflow: hidden;
        border: 2px solid #ff4655;
        background: #111827;
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
        background: rgba(15, 23, 42, 0.8);
        padding: 8px 16px;
        border-radius: 8px;
        border: 1px solid rgba(255, 70, 85, 0.4);
    }
    .hud-val {
        color: #ff4655;
        font-size: 22px;
    }
    #menu-overlay {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(15, 23, 42, 0.88);
        backdrop-filter: blur(6px);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
        z-index: 20;
    }
    h1 {
        font-size: 40px;
        margin-bottom: 10px;
        color: #ff4655;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    p {
        color: #94a3b8;
        margin-bottom: 25px;
        font-size: 16px;
    }
    .btn {
        background: linear-gradient(135deg, #ff4655 0%, #dc2626 100%);
        color: white;
        border: none;
        padding: 14px 40px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 30px;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 4px 15px rgba(255, 70, 85, 0.5);
    }
    .btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 70, 85, 0.8);
        background: linear-gradient(135deg, #ff6b78 0%, #ff4655 100%);
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
        color: #ff4655;
        font-weight: bold;
    }
</style>
</head>
<body>

<div id="game-container">
    <div class="hud">
        <div class="hud-item">KILLS: <span id="score" class="hud-val">0</span></div>
        <div class="hud-item">HEADSHOTS: <span id="headshots" class="hud-val">0</span></div>
        <div class="hud-item">TỶ LỆ HS: <span id="hs-percent" class="hud-val">0%</span></div>
        <div class="hud-item">THỜI GIAN: <span id="time" class="hud-val">30</span>s</div>
    </div>

    <div id="menu-overlay">
        <h1 id="menu-title">VALORANT BOT RANGE</h1>
        <p id="menu-subtitle">Tập ngắm headshot bot phòng luyện tập Valorant</p>
        
        <div id="final-stats" class="stats-card" style="display: none;">
            <h3>THỐNG KÊ TRẬN ĐẤU</h3>
            <div class="stats-grid">
                <div class="stat-box">
                    <span class="stat-label">Tổng Kills</span>
                    <span id="final-score" class="stat-number">0</span>
                </div>
                <div class="stat-box">
                    <span class="stat-label">Headshot %</span>
                    <span id="final-hs" class="stat-number">0%</span>
                </div>
                <div class="stat-box">
                    <span class="stat-label">Độ Chính Xác</span>
                    <span id="final-acc" class="stat-number">0%</span>
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

// Web Audio API giả lập tiếng súng Vandal / Phantom
const AudioContext = window.AudioContext || window.webkitAudioContext;
let audioCtx = null;

function playSound(type) {
    if (!audioCtx) audioCtx = new AudioContext();
    if (audioCtx.state === 'suspended') audioCtx.resume();

    const now = audioCtx.currentTime;

    if (type === 'vandal') {
        // Tiếng súng nổ mạnh
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(300, now);
        osc.frequency.exponentialRampToValueAtTime(40, now + 0.12);
        gain.gain.setValueAtTime(0.4, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.12);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start(now);
        osc.stop(now + 0.12);
    } else if (type === 'headshot') {
        // Tiếng ting Headshot đặc trưng Valorant
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(1400, now);
        osc.frequency.setValueAtTime(1800, now + 0.05);
        gain.gain.setValueAtTime(0.3, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.18);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start(now);
        osc.stop(now + 0.18);
    }
}

// Biến Game State
let gameState = 'MENU';
let score = 0;
let headshots = 0;
let totalShots = 0;
let hits = 0;
let timeLeft = 30;
let timerInterval = null;

// Biến hiệu ứng súng
let gunRecoilY = 0;
let muzzleFlash = 0;
let mousePos = { x: 450, y: 300 };

let bots = [];
let particles = [];
let floatingTexts = [];

// Khởi tạo Robot Valorant (Vàng Neon)
class ValorantBot {
    constructor() {
        this.x = Math.random() * (canvas.width - 240) + 120;
        this.y = Math.random() * 120 + 200; // Đặt bot ở khoảng sân giữa
        this.scale = 1.1;
        this.hp = 2; // 2 phát thân hoặc 1 phát đầu
        this.maxHp = 2;
        
        // Vùng Headshot & Bodyshot
        this.headRadius = 16;
        this.headYOffset = -55;
        this.bodyWidth = 36;
        this.bodyHeight = 60;
    }

    draw() {
        ctx.save();
        ctx.translate(this.x, this.y);

        // Hiệu ứng viền phát sáng màu vàng (Yellow Glow) chuẩn Valorant
        ctx.shadowColor = '#eab308';
        ctx.shadowBlur = 15;

        // 1. Thân Bot (Armor & Robot body)
        ctx.fillStyle = '#94a3b8';
        ctx.strokeStyle = '#facc15';
        ctx.lineWidth = 2;

        // Vai & Giáp
        ctx.beginPath();
        ctx.roundRect(-this.bodyWidth / 2 - 6, -35, this.bodyWidth + 12, 20, 6);
        ctx.fillStyle = '#475569';
        ctx.fill();
        ctx.stroke();

        // Ngực & Bụng
        ctx.beginPath();
        ctx.roundRect(-this.bodyWidth / 2, -15, this.bodyWidth, this.bodyHeight, 8);
        ctx.fillStyle = '#cbd5e1';
        ctx.fill();
        ctx.stroke();

        // Lõi năng lượng ngực (Triangular Core)
        ctx.beginPath();
        ctx.moveTo(0, -5);
        ctx.lineTo(-8, 10);
        ctx.lineTo(8, 10);
        ctx.closePath();
        ctx.fillStyle = '#38bdf8';
        ctx.shadowColor = '#38bdf8';
        ctx.shadowBlur = 10;
        ctx.fill();

        // Reset shadow cho cổ & đầu
        ctx.shadowColor = '#eab308';
        ctx.shadowBlur = 15;

        // 2. Cổ Bot
        ctx.fillStyle = '#334155';
        ctx.fillRect(-5, -45, 10, 12);

        // 3. Đầu Bot (Robot Head)
        ctx.beginPath();
        ctx.roundRect(-14, this.headYOffset - 12, 28, 28, 6);
        ctx.fillStyle = '#e2e8f0';
        ctx.fill();
        ctx.strokeStyle = '#facc15';
        ctx.lineWidth = 2.5;
        ctx.stroke();

        // Mắt Robot phát sáng (Cyan Eye)
        ctx.beginPath();
        ctx.arc(0, this.headYOffset, 5, 0, Math.PI * 2);
        ctx.fillStyle = '#06b6d4';
        ctx.shadowColor = '#06b6d4';
        ctx.shadowBlur = 12;
        ctx.fill();

        ctx.restore();
    }

    checkHit(mx, my) {
        // Kiểm tra Headshot
        const headX = this.x;
        const headY = this.y + this.headYOffset;
        const distHead = Math.hypot(mx - headX, my - headY);

        if (distHead <= this.headRadius) {
            return 'HEAD';
        }

        // Kiểm tra Bodyshot
        const left = this.x - this.bodyWidth / 2 - 5;
        const right = this.x + this.bodyWidth / 2 + 5;
        const top = this.y - 35;
        const bottom = this.y + this.bodyHeight;

        if (mx >= left && mx <= right && my >= top && my <= bottom) {
            return 'BODY';
        }

        return 'MISS';
    }
}

class Particle {
    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.color = color;
        this.radius = Math.random() * 3 + 2;
        this.vx = (Math.random() - 0.5) * 7;
        this.vy = (Math.random() - 0.5) * 7;
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
        this.vy = -1.8;
    }

    update() {
        this.y += this.vy;
        this.alpha -= 0.03;
    }

    draw() {
        ctx.save();
        ctx.globalAlpha = this.alpha;
        ctx.font = '900 20px Segoe UI';
        ctx.fillStyle = this.color;
        ctx.fillText(this.text, this.x - 20, this.y);
        ctx.restore();
    }
}

function spawnBot() {
    while (bots.length < 3) {
        bots.push(new ValorantBot());
    }
}

function updateHUD() {
    document.getElementById('score').innerText = score;
    document.getElementById('headshots').innerText = headshots;
    const hsPerc = score > 0 ? Math.round((headshots / score) * 100) : 0;
    document.getElementById('hs-percent').innerText = hsPerc + '%';
    document.getElementById('time').innerText = timeLeft;
}

function startGame() {
    score = 0;
    headshots = 0;
    totalShots = 0;
    hits = 0;
    timeLeft = 30;
    bots = [];
    particles = [];
    floatingTexts = [];
    gameState = 'PLAYING';

    document.getElementById('menu-overlay').style.display = 'none';
    updateHUD();
    spawnBot();

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
    document.getElementById('menu-subtitle').innerText = 'Hoàn thành lượt tập luyện bắn Bot.';
    document.getElementById('start-btn').innerText = 'BẮT ĐẦU LẠI';

    const hsPerc = score > 0 ? Math.round((headshots / score) * 100) : 0;
    const acc = totalShots > 0 ? Math.round((hits / totalShots) * 100) : 0;

    document.getElementById('final-score').innerText = score;
    document.getElementById('final-hs').innerText = hsPerc + '%';
    document.getElementById('final-acc').innerText = acc + '%';
    document.getElementById('final-stats').style.display = 'block';
}

// Xử lý di chuyển chuột
canvas.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    mousePos.x = e.clientX - rect.left;
    mousePos.y = e.clientY - rect.top;
});

// Xử lý Bắn súng
canvas.addEventListener('mousedown', (e) => {
    if (gameState !== 'PLAYING') return;

    totalShots++;
    gunRecoilY = 18; // Hiệu ứng giật súng
    muzzleFlash = 4; // Bật lửa nòng súng
    playSound('vandal');

    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;

    let hitAny = false;

    for (let i = bots.length - 1; i >= 0; i--) {
        const bot = bots[i];
        const hitType = bot.checkHit(mx, my);

        if (hitType === 'HEAD') {
            hitAny = true;
            hits++;
            score++;
            headshots++;
            playSound('headshot');

            // Tạo hiệu ứng Headshot nổ hạt vàng & đỏ
            for (let p = 0; p < 16; p++) {
                particles.push(new Particle(mx, my, '#facc15'));
                particles.push(new Particle(mx, my, '#ef4444'));
            }
            floatingTexts.push(new FloatingText('HEADSHOT! 160', mx, my, '#facc15'));

            bots.splice(i, 1);
            spawnBot();
            break;

        } else if (hitType === 'BODY') {
            hitAny = true;
            hits++;
            bot.hp--;

            for (let p = 0; p < 8; p++) {
                particles.push(new Particle(mx, my, '#cbd5e1'));
            }

            if (bot.hp <= 0) {
                score++;
                floatingTexts.push(new FloatingText('KILL 40', mx, my, '#38bdf8'));
                bots.splice(i, 1);
                spawnBot();
            } else {
                floatingTexts.push(new FloatingText('40', mx, my, '#ffffff'));
            }
            break;
        }
    }

    if (!hitAny) {
        // Bắn trượt ra ngoài
        for (let p = 0; p < 4; p++) {
            particles.push(new Particle(mx, my, '#64748b'));
        }
    }

    updateHUD();
});

// Vẽ khẩu súng FPS ở góc dưới
function drawGun() {
    ctx.save();

    // Giảm độ giật súng từ từ
    if (gunRecoilY > 0) gunRecoilY -= 2;

    const gunX = canvas.width - 220;
    const gunY = canvas.height - 120 + gunRecoilY;

    // 1. Tia lửa nòng súng (Muzzle Flash)
    if (muzzleFlash > 0) {
        muzzleFlash--;
        ctx.beginPath();
        ctx.arc(gunX - 110, gunY - 45, 22, 0, Math.PI * 2);
        ctx.fillStyle = '#fef08a';
        ctx.shadowColor = '#f59e0b';
        ctx.shadowBlur = 20;
        ctx.fill();
    }

    // 2. Thân súng Vandal (Góc nhìn thứ nhất)
    ctx.shadowColor = 'transparent';
    
    // Nòng súng
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(gunX - 110, gunY - 48, 120, 10);

    // Thân súng chính
    ctx.beginPath();
    ctx.moveTo(gunX - 30, gunY - 55);
    ctx.lineTo(gunX + 120, gunY - 20);
    ctx.lineTo(gunX + 120, gunY + 80);
    ctx.lineTo(gunX - 10, gunY + 60);
    ctx.lineTo(gunX - 30, gunY - 10);
    ctx.closePath();
    ctx.fillStyle = '#0f172a';
    ctx.fill();
    ctx.strokeStyle = '#ff4655';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Ốp tay súng & đường viền đỏ góc cạnh
    ctx.fillStyle = '#ff4655';
    ctx.fillRect(gunX - 10, gunY - 45, 50, 6);

    ctx.restore();
}

// Vẽ bối cảnh Phòng tập (Valorant Range Background)
function drawBackground() {
    // Tường nhà kho & sàn tập
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 0, canvas.width, 360);

    // Đường chỉ tường kim loại
    ctx.strokeStyle = '#334155';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(0, 360);
    ctx.lineTo(canvas.width, 360);
    ctx.stroke();

    // Sàn nhà
    let gradient = ctx.createLinearGradient(0, 360, 0, canvas.height);
    gradient.addColorStop(0, '#0f172a');
    gradient.addColorStop(1, '#020617');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 360, canvas.width, canvas.height - 360);

    // Vạch kẻ vôi sân tập
    ctx.strokeStyle = 'rgba(250, 204, 21, 0.2)';
    ctx.lineWidth = 2;
    ctx.strokeRect(100, 220, 700, 130);
}

// Vòng lặp Render (Game Loop)
function gameLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    drawBackground();

    if (gameState === 'PLAYING') {
        // Draw Bots
        bots.forEach(b => b.draw());

        // Update & Draw Particles
        for (let i = particles.length - 1; i >= 0; i--) {
            particles[i].update();
            particles[i].draw();
            if (particles[i].alpha <= 0) particles.splice(i, 1);
        }

        // Update & Draw Floating Text
        for (let i = floatingTexts.length - 1; i >= 0; i--) {
            floatingTexts[i].update();
            floatingTexts[i].draw();
            if (floatingTexts[i].alpha <= 0) floatingTexts.splice(i, 1);
        }
    }

    // Vẽ khẩu súng FPS người chơi
    drawGun();

    requestAnimationFrame(gameLoop);
}

gameLoop();
</script>
</body>
</html>
"""

# Nhúng HTML/JS Game vào Streamlit
components.html(game_html, height=650)
