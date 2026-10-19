import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Valorant Champions Range - Full Auto",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #f8fafc; }
    .stApp { max-width: 1200px; margin: 0 auto; }
    h1, h2, h3 { color: #eab308 !important; font-family: 'Segoe UI', sans-serif; }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🏆 CHAMPIONS VANDAL RANGE")
    st.write("Phiên bản cập nhật hình ảnh súng chuẩn HD và chế độ xả đạn tự động (Full Auto Spray)!")
    st.markdown("---")
    st.subheader("🎮 Hướng dẫn")
    st.write("1. **Giữ chuột trái (Hold Mouse)**: Sấy đạn liên tục (Full-Auto) giống hệt súng Vandal thật.")
    st.write("2. Kê tâm ngắm vào **ĐẦU BOT (Headshot)** để tiêu diệt ngay lập tức!")
    st.write("3. Hình ảnh skin **Champions Vandal (Đen - Vàng Kim)** HD cực kỳ sắc nét.")

st.title("🏆 Valorant Range - Champions Vandal (Full Auto Spray)")

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
    * { box-sizing: border-box; user-select: none; margin: 0; padding: 0; }
    body {
        background-color: #090d16;
        font-family: 'Segoe UI', sans-serif;
        display: flex; justify-content: center; align-items: center;
        height: 100vh; overflow: hidden;
    }
    #game-container {
        position: relative; width: 900px; height: 600px;
        box-shadow: 0 0 35px rgba(234, 179, 8, 0.35);
        border-radius: 12px; overflow: hidden;
        border: 2px solid #eab308; background: #0f172a;
    }
    canvas { display: block; cursor: crosshair; }
    .hud {
        position: absolute; top: 15px; left: 20px; right: 20px;
        display: flex; justify-content: space-between;
        pointer-events: none; font-size: 18px; font-weight: bold;
        color: #f8fafc; text-shadow: 0 2px 4px rgba(0,0,0,0.8); z-index: 10;
    }
    .hud-item {
        background: rgba(15, 23, 42, 0.85); padding: 8px 16px;
        border-radius: 8px; border: 1px solid rgba(234, 179, 8, 0.5);
    }
    .hud-val { color: #eab308; font-size: 22px; }
    #menu-overlay {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(15, 23, 42, 0.9); backdrop-filter: blur(6px);
        display: flex; flex-direction: column; justify-content: center;
        align-items: center; color: white; z-index: 20;
    }
    h1 { font-size: 38px; margin-bottom: 10px; color: #eab308; text-transform: uppercase; letter-spacing: 2px; }
    p { color: #94a3b8; margin-bottom: 25px; font-size: 16px; }
    .btn {
        background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%);
        color: #0f172a; border: none; padding: 14px 40px; font-size: 20px;
        font-weight: bold; border-radius: 30px; cursor: pointer;
        box-shadow: 0 4px 15px rgba(234, 179, 8, 0.4);
    }
    .btn:hover { background: linear-gradient(135deg, #fde047 0%, #eab308 100%); transform: translateY(-2px); }
    .stats-card {
        background: rgba(30, 41, 59, 0.8); padding: 20px 40px;
        border-radius: 12px; margin-bottom: 25px; border: 1px solid #334155; text-align: center;
    }
    .stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 10px; }
    .stat-number { font-size: 26px; color: #eab308; font-weight: bold; }
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
        <h1 id="menu-title">CHAMPIONS VANDAL RANGE</h1>
        <p id="menu-subtitle">Giữ chuột để sấy đạn liên tục với súng Champions Vandal HD</p>
        
        <div id="final-stats" class="stats-card" style="display: none;">
            <h3>KẾT QUẢ TẬP LUYỆN</h3>
            <div class="stats-grid">
                <div><span style="font-size:14px;color:#94a3b8;">Tổng Kills</span><br><span id="final-score" class="stat-number">0</span></div>
                <div><span style="font-size:14px;color:#94a3b8;">Headshot %</span><br><span id="final-hs" class="stat-number">0%</span></div>
                <div><span style="font-size:14px;color:#94a3b8;">Độ Chính Xác</span><br><span id="final-acc" class="stat-number">0%</span></div>
            </div>
        </div>

        <button id="start-btn" class="btn" onclick="startGame()">BẮT ĐẦU VÀO SÂN</button>
    </div>

    <canvas id="gameCanvas" width="900" height="600"></canvas>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Tải hình ảnh súng Champions Vandal chuẩn
const gunImg = new Image();
gunImg.src = 'https://images.contentstack.io/v3/assets/bltb6540380da7ba7e0/blt1cb3eefcfdd624bf/6110f06a1953ce3575916327/Champions_Vandal.png';

const AudioContext = window.AudioContext || window.webkitAudioContext;
let audioCtx = null;

function playSound(type) {
    if (!audioCtx) audioCtx = new AudioContext();
    if (audioCtx.state === 'suspended') audioCtx.resume();

    const now = audioCtx.currentTime;

    if (type === 'vandal') {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(290, now);
        osc.frequency.exponentialRampToValueAtTime(35, now + 0.09);
        gain.gain.setValueAtTime(0.3, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.09);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(now); osc.stop(now + 0.09);
    } else if (type === 'champions_headshot') {
        [1046.5, 1318.5, 1567.98].forEach((freq, idx) => {
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(freq, now + idx * 0.03);
            gain.gain.setValueAtTime(0.25, now + idx * 0.03);
            gain.gain.linearRampToValueAtTime(0.001, now + 0.35 + idx * 0.03);
            osc.connect(gain); gain.connect(audioCtx.destination);
            osc.start(now + idx * 0.03); osc.stop(now + 0.35 + idx * 0.03);
        });
    }
}

let gameState = 'MENU';
let score = 0, headshots = 0, totalShots = 0, hits = 0, timeLeft = 30;
let timerInterval = null;
let gunRecoilY = 0, muzzleFlash = 0;

// Xử lý giữ chuột sấy đạn (Full Auto)
let isMouseDown = false;
let lastShotTime = 0;
const fireRateMs = 100; // Tốc độ bắn (~10 viên/giây)
let currentMousePos = { x: 450, y: 300 };

let bots = [], particles = [], floatingTexts = [];

class ValorantBot {
    constructor() {
        this.x = Math.random() * (canvas.width - 260) + 130;
        this.y = Math.random() * 100 + 220;
        this.hp = 2;
        this.headRadius = 15;
        this.headYOffset = -50;
        this.bodyWidth = 34;
        this.bodyHeight = 58;
    }

    draw() {
        ctx.save();
        ctx.translate(this.x, this.y);

        ctx.shadowColor = '#facc15';
        ctx.shadowBlur = 12;

        // Thân Robot
        ctx.fillStyle = '#475569';
        ctx.beginPath();
        ctx.roundRect(-this.bodyWidth/2, -15, this.bodyWidth, this.bodyHeight, 6);
        ctx.fill();
        ctx.strokeStyle = '#facc15';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Đầu Robot
        ctx.beginPath();
        ctx.roundRect(-13, this.headYOffset - 12, 26, 26, 6);
        ctx.fillStyle = '#cbd5e1';
        ctx.fill();
        ctx.stroke();

        // Mắt phát sáng
        ctx.beginPath();
        ctx.arc(0, this.headYOffset, 4, 0, Math.PI * 2);
        ctx.fillStyle = '#06b6d4';
        ctx.shadowColor = '#06b6d4';
        ctx.shadowBlur = 10;
        ctx.fill();

        ctx.restore();
    }

    checkHit(mx, my) {
        const headX = this.x;
        const headY = this.y + this.headYOffset;
        if (Math.hypot(mx - headX, my - headY) <= this.headRadius) return 'HEAD';

        const left = this.x - this.bodyWidth / 2 - 4;
        const right = this.x + this.bodyWidth / 2 + 4;
        const top = this.y - 30;
        const bottom = this.y + this.bodyHeight;
        if (mx >= left && mx <= right && my >= top && my <= bottom) return 'BODY';

        return 'MISS';
    }
}

class Particle {
    constructor(x, y, color) {
        this.x = x; this.y = y; this.color = color;
        this.radius = Math.random() * 3 + 2;
        this.vx = (Math.random() - 0.5) * 8;
        this.vy = (Math.random() - 0.5) * 8;
        this.alpha = 1;
    }
    update() { this.x += this.vx; this.y += this.vy; this.alpha -= 0.04; }
    draw() {
        ctx.save(); ctx.globalAlpha = this.alpha;
        ctx.beginPath(); ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = this.color; ctx.fill(); ctx.restore();
    }
}

class FloatingText {
    constructor(text, x, y, color) {
        this.text = text; this.x = x; this.y = y; this.color = color;
        this.alpha = 1; this.vy = -1.8;
    }
    update() { this.y += this.vy; this.alpha -= 0.03; }
    draw() {
        ctx.save(); ctx.globalAlpha = this.alpha;
        ctx.font = '900 20px Segoe UI'; ctx.fillStyle = this.color;
        ctx.fillText(this.text, this.x - 25, this.y); ctx.restore();
    }
}

function spawnBot() {
    while (bots.length < 3) bots.push(new ValorantBot());
}

function updateHUD() {
    document.getElementById('score').innerText = score;
    document.getElementById('headshots').innerText = headshots;
    const hsPerc = score > 0 ? Math.round((headshots / score) * 100) : 0;
    document.getElementById('hs-percent').innerText = hsPerc + '%';
    document.getElementById('time').innerText = timeLeft;
}

function startGame() {
    score = 0; headshots = 0; totalShots = 0; hits = 0; timeLeft = 30;
    bots = []; particles = []; floatingTexts = []; gameState = 'PLAYING';
    document.getElementById('menu-overlay').style.display = 'none';
    updateHUD(); spawnBot();

    clearInterval(timerInterval);
    timerInterval = setInterval(() => {
        timeLeft--; updateHUD();
        if (timeLeft <= 0) endGame();
    }, 1000);
}

function endGame() {
    gameState = 'END'; isMouseDown = false;
    clearInterval(timerInterval);
    document.getElementById('menu-overlay').style.display = 'flex';
    document.getElementById('menu-title').innerText = 'HOÀN THÀNH!';
    document.getElementById('start-btn').innerText = 'CHƠI LẠI';

    const hsPerc = score > 0 ? Math.round((headshots / score) * 100) : 0;
    const acc = totalShots > 0 ? Math.round((hits / totalShots) * 100) : 0;

    document.getElementById('final-score').innerText = score;
    document.getElementById('final-hs').innerText = hsPerc + '%';
    document.getElementById('final-acc').innerText = acc + '%';
    document.getElementById('final-stats').style.display = 'block';
}

function shoot(mx, my) {
    totalShots++;
    gunRecoilY = 14;
    muzzleFlash = 3;
    playSound('vandal');

    let hitAny = false;

    for (let i = bots.length - 1; i >= 0; i--) {
        const bot = bots[i];
        const hitType = bot.checkHit(mx, my);

        if (hitType === 'HEAD') {
            hitAny = true; hits++; score++; headshots++;
            playSound('champions_headshot');

            for (let p = 0; p < 18; p++) {
                particles.push(new Particle(mx, my, '#facc15'));
                particles.push(new Particle(mx, my, '#ffffff'));
            }
            floatingTexts.push(new FloatingText('HEADSHOT!', mx, my, '#facc15'));

            bots.splice(i, 1); spawnBot(); break;
        } else if (hitType === 'BODY') {
            hitAny = true; hits++; bot.hp--;
            for (let p = 0; p < 8; p++) particles.push(new Particle(mx, my, '#cbd5e1'));

            if (bot.hp <= 0) {
                score++;
                floatingTexts.push(new FloatingText('KILL 40', mx, my, '#38bdf8'));
                bots.splice(i, 1); spawnBot();
            }
            break;
        }
    }

    updateHUD();
}

// Xử lý giữ chuột trái để sấy đạn (Auto Spray)
canvas.addEventListener('mousedown', (e) => {
    if (gameState !== 'PLAYING') return;
    isMouseDown = true;
    const rect = canvas.getBoundingClientRect();
    currentMousePos.x = e.clientX - rect.left;
    currentMousePos.y = e.clientY - rect.top;
    
    shoot(currentMousePos.x, currentMousePos.y);
    lastShotTime = Date.now();
});

window.addEventListener('mouseup', () => { isMouseDown = false; });

canvas.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    currentMousePos.x = e.clientX - rect.left;
    currentMousePos.y = e.clientY - rect.top;
});

// Vẽ hình ảnh súng Champions Vandal HD
function drawChampionsVandal() {
    ctx.save();
    if (gunRecoilY > 0) gunRecoilY -= 2;

    const gunWidth = 420;
    const gunHeight = 180;
    const gunX = canvas.width - 380;
    const gunY = canvas.height - 180 + gunRecoilY;

    // 1. Muzzle Flash (Tia lửa nòng súng)
    if (muzzleFlash > 0) {
        muzzleFlash--;
        ctx.beginPath();
        ctx.arc(gunX + 30, gunY + 35, 26, 0, Math.PI * 2);
        ctx.fillStyle = '#fef08a';
        ctx.shadowColor = '#eab308'; ctx.shadowBlur = 30;
        ctx.fill();
    }

    ctx.shadowColor = 'transparent';

    // 2. Vẽ hình ảnh thật của súng Champions Vandal
    if (gunImg.complete) {
        ctx.drawImage(gunImg, gunX, gunY, gunWidth, gunHeight);
    }

    ctx.restore();
}

// Bối cảnh bản đồ Ascent
function drawAscentMap() {
    ctx.fillStyle = '#9a3412';
    ctx.fillRect(0, 0, canvas.width, 380);

    ctx.fillStyle = '#f43f5e';
    ctx.beginPath();
    ctx.moveTo(150, 0); ctx.lineTo(750, 0);
    ctx.lineTo(700, 70); ctx.lineTo(200, 70);
    ctx.closePath(); ctx.fill();

    ctx.fillStyle = '#cbd5e1';
    ctx.beginPath();
    ctx.arc(450, 260, 80, Math.PI, 0);
    ctx.rect(370, 260, 160, 120);
    ctx.fill();

    ctx.fillStyle = '#1e293b';
    ctx.fillRect(382, 260, 136, 120);

    ctx.fillStyle = '#e2e8f0';
    ctx.fillRect(80, 60, 60, 320);
    ctx.fillRect(760, 60, 60, 320);

    let grad = ctx.createLinearGradient(0, 380, 0, canvas.height);
    grad.addColorStop(0, '#475569');
    grad.addColorStop(1, '#0f172a');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 380, canvas.width, canvas.height - 380);
}

function gameLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    drawAscentMap();

    if (gameState === 'PLAYING') {
        // Xử lý sấy đạn liên tục khi giữ chuột
        if (isMouseDown && Date.now() - lastShotTime >= fireRateMs) {
            shoot(currentMousePos.x, currentMousePos.y);
            lastShotTime = Date.now();
        }

        bots.forEach(b => b.draw());

        for (let i = particles.length - 1; i >= 0; i--) {
            particles[i].update(); particles[i].draw();
            if (particles[i].alpha <= 0) particles.splice(i, 1);
        }

        for (let i = floatingTexts.length - 1; i >= 0; i--) {
            floatingTexts[i].update(); floatingTexts[i].draw();
            if (floatingTexts[i].alpha <= 0) floatingTexts.splice(i, 1);
        }
    }

    drawChampionsVandal();

    requestAnimationFrame(gameLoop);
}

gameLoop();
</script>
</body>
</html>
"""

components.html(game_html, height=650)
