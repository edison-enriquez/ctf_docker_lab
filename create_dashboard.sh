#!/bin/bash
cat > /workspaces/ctf_docker_lab/templates/index.html << 'EOF'
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🐳 Docker CTF Lab - Hacker Terminal</title>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;400;500;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --bg-primary: #0a0e27;
            --bg-secondary: #111827;
            --bg-tertiary: #1a1f3a;
            --accent-green: #00ff41;
            --accent-cyan: #00d9ff;
            --accent-purple: #9d4edd;
            --accent-red: #ff006e;
            --text-primary: #e0e0e0;
            --text-secondary: #a0a0a0;
            --border-color: #00ff4144;
        }

        body {
            font-family: 'Fira Code', 'Share Tech Mono', monospace;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
        }

        #matrix-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            opacity: 0.1;
            pointer-events: none;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 1;
        }

        header {
            background: var(--bg-secondary);
            border: 2px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
            position: relative;
            overflow: hidden;
        }

        header::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--accent-green), transparent);
            animation: scan 3s linear infinite;
        }

        @keyframes scan {
            0% { left: -100%; }
            100% { left: 100%; }
        }

        .terminal-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }

        .terminal-dots {
            display: flex;
            gap: 8px;
        }

        .dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            animation: pulse 2s ease-in-out infinite;
        }

        .dot.red { background: var(--accent-red); }
        .dot.yellow { background: #ffd60a; }
        .dot.green { background: var(--accent-green); }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        h1 {
            color: var(--accent-green);
            font-size: 2em;
            text-shadow: 0 0 10px var(--accent-green);
            font-weight: 700;
            letter-spacing: 2px;
        }

        .subtitle {
            color: var(--accent-cyan);
            font-size: 0.9em;
            margin-top: 5px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }

        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: var(--accent-green);
        }

        .stat-card:hover {
            border-color: var(--accent-green);
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.4);
            transform: translateY(-5px);
        }

        .stat-icon {
            font-size: 2.5em;
            margin-bottom: 10px;
            filter: drop-shadow(0 0 10px var(--accent-green));
        }

        .stat-value {
            font-size: 2.5em;
            font-weight: 700;
            color: var(--accent-green);
            text-shadow: 0 0 10px var(--accent-green);
            font-family: 'Share Tech Mono', monospace;
        }

        .stat-label {
            color: var(--text-secondary);
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .progress-bar-container {
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            height: 30px;
            overflow: hidden;
            margin: 15px 0;
            position: relative;
        }

        .progress-bar {
            background: linear-gradient(90deg, var(--accent-green), var(--accent-cyan));
            height: 100%;
            transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--bg-primary);
            font-weight: bold;
            position: relative;
            overflow: hidden;
        }

        .progress-bar::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            bottom: 0;
            right: 0;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            animation: shimmer 2s infinite;
        }

        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }

        .submit-section {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 0 15px rgba(0, 255, 65, 0.2);
        }

        .submit-section h2 {
            color: var(--accent-cyan);
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 3px;
            font-size: 1.2em;
        }

        .form-group {
            display: flex;
            gap: 10px;
        }

        input[type="text"] {
            flex: 1;
            padding: 15px;
            background: var(--bg-tertiary);
            border: 2px solid var(--border-color);
            border-radius: 6px;
            color: var(--accent-green);
            font-family: 'Fira Code', monospace;
            font-size: 0.95em;
            transition: all 0.3s ease;
        }

        input[type="text"]:focus {
            outline: none;
            border-color: var(--accent-cyan);
            box-shadow: 0 0 15px rgba(0, 217, 255, 0.3);
            background: var(--bg-primary);
        }

        input[type="text"]::placeholder {
            color: var(--text-secondary);
            opacity: 0.5;
        }

        button {
            background: linear-gradient(135deg, var(--accent-green), var(--accent-cyan));
            color: var(--bg-primary);
            border: none;
            padding: 15px 35px;
            border-radius: 6px;
            font-size: 1em;
            font-weight: 700;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-family: 'Fira Code', monospace;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        button::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }

        button:hover::before {
            width: 300px;
            height: 300px;
        }

        button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 20px var(--accent-green);
        }

        button:active {
            transform: scale(0.98);
        }

        .challenges-section {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 30px;
            margin-bottom: 30px;
        }

        .challenges-section h2 {
            color: var(--accent-purple);
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 3px;
            font-size: 1.3em;
        }

        .filter-buttons {
            display: flex;
            gap: 10px;
            margin-bottom: 25px;
            flex-wrap: wrap;
        }

        .filter-btn {
            padding: 10px 20px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Fira Code', monospace;
            font-size: 0.85em;
        }

        .filter-btn:hover {
            border-color: var(--accent-green);
            color: var(--accent-green);
        }

        .filter-btn.active {
            background: var(--accent-green);
            color: var(--bg-primary);
            border-color: var(--accent-green);
            box-shadow: 0 0 15px var(--accent-green);
        }

        .challenges-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
            gap: 20px;
        }

        .challenge-card {
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .challenge-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, var(--accent-green), var(--accent-cyan));
        }

        .challenge-card:hover {
            border-color: var(--accent-cyan);
            box-shadow: 0 0 20px rgba(0, 217, 255, 0.3);
            transform: translateY(-5px);
        }

        .challenge-card.completed {
            border-color: var(--accent-green);
            background: rgba(0, 255, 65, 0.05);
        }

        .challenge-card.completed::before {
            background: var(--accent-green);
        }

        .challenge-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 15px;
        }

        .challenge-title {
            font-size: 1.1em;
            font-weight: 700;
            color: var(--accent-cyan);
            margin-bottom: 8px;
        }

        .challenge-card.completed .challenge-title {
            color: var(--accent-green);
        }

        .challenge-badge {
            background: var(--accent-purple);
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 700;
            white-space: nowrap;
        }

        .challenge-card.completed .challenge-badge {
            background: var(--accent-green);
            color: var(--bg-primary);
        }

        .challenge-description {
            color: var(--text-secondary);
            margin-bottom: 15px;
            line-height: 1.6;
            font-size: 0.9em;
        }

        .challenge-meta {
            display: flex;
            gap: 15px;
            font-size: 0.85em;
            color: var(--text-secondary);
            margin-bottom: 12px;
            flex-wrap: wrap;
        }

        .challenge-flag {
            background: var(--bg-secondary);
            border: 1px solid var(--accent-cyan);
            border-radius: 6px;
            padding: 12px;
            margin-top: 12px;
            font-family: 'Share Tech Mono', monospace;
            font-size: 0.85em;
            color: var(--accent-cyan);
            word-break: break-all;
            position: relative;
        }

        .challenge-flag::before {
            content: '> ';
            color: var(--accent-green);
        }

        .hint-button {
            background: var(--accent-purple);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85em;
            margin-top: 12px;
            font-family: 'Fira Code', monospace;
            transition: all 0.3s ease;
        }

        .hint-button:hover {
            background: var(--accent-cyan);
            box-shadow: 0 0 15px var(--accent-cyan);
        }

        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 20px 25px;
            border-radius: 8px;
            color: white;
            font-weight: bold;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
            z-index: 1000;
            animation: slideIn 0.3s ease;
            max-width: 450px;
            border: 2px solid;
            font-family: 'Fira Code', monospace;
        }

        @keyframes slideIn {
            from {
                transform: translateX(500px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        .notification.success {
            background: rgba(0, 255, 65, 0.2);
            border-color: var(--accent-green);
            color: var(--accent-green);
        }

        .notification.error {
            background: rgba(255, 0, 110, 0.2);
            border-color: var(--accent-red);
            color: var(--accent-red);
        }

        .notification.warning {
            background: rgba(255, 214, 10, 0.2);
            border-color: #ffd60a;
            color: #ffd60a;
        }

        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(10, 14, 39, 0.95);
            backdrop-filter: blur(5px);
        }

        .modal-content {
            background: var(--bg-secondary);
            margin: 10% auto;
            padding: 30px;
            border: 2px solid var(--border-color);
            border-radius: 12px;
            max-width: 650px;
            box-shadow: 0 0 40px rgba(0, 255, 65, 0.4);
            position: relative;
        }

        .close {
            position: absolute;
            right: 20px;
            top: 15px;
            font-size: 32px;
            font-weight: bold;
            cursor: pointer;
            color: var(--accent-red);
            transition: all 0.3s ease;
        }

        .close:hover {
            color: var(--accent-green);
            transform: rotate(90deg);
        }

        footer {
            text-align: center;
            color: var(--text-secondary);
            margin-top: 40px;
            padding: 30px;
            border-top: 1px solid var(--border-color);
        }

        footer p {
            margin: 5px 0;
            font-size: 0.9em;
        }

        .dificultad-principiante { color: var(--accent-green); }
        .dificultad-intermedio { color: #ffd60a; }
        .dificultad-avanzado { color: #ff9500; }
        .dificultad-experto { color: var(--accent-red); }

        @media (max-width: 768px) {
            .challenges-grid {
                grid-template-columns: 1fr;
            }
            
            h1 {
                font-size: 1.5em;
            }
            
            .form-group {
                flex-direction: column;
            }

            button {
                width: 100%;
            }
        }

        body::after {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: repeating-linear-gradient(
                0deg,
                rgba(0, 0, 0, 0.15),
                rgba(0, 0, 0, 0.15) 1px,
                transparent 1px,
                transparent 2px
            );
            pointer-events: none;
            z-index: 999;
        }
    </style>
</head>
<body>
    <canvas id="matrix-bg"></canvas>
    
    <div class="container">
        <header>
            <div class="terminal-header">
                <div class="terminal-dots">
                    <span class="dot red"></span>
                    <span class="dot yellow"></span>
                    <span class="dot green"></span>
                </div>
                <span style="color: var(--text-secondary); font-size: 0.9em;">root@docker-ctf-lab:~$</span>
            </div>
            <h1>🐳 DOCKER CTF LAB</h1>
            <p class="subtitle">[ CAPTURE THE FLAG - DOCKER HACKING CHALLENGE ]</p>
            <p class="subtitle" id="studentInfo" style="margin-top: 10px;">[ CONNECTING... ]</p>
        </header>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">🎯</div>
                <div class="stat-value" id="completedCount">0</div>
                <div class="stat-label">CHALLENGES PWNED</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🏆</div>
                <div class="stat-value" id="totalPoints">0</div>
                <div class="stat-label">POINTS EARNED</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">📊</div>
                <div class="stat-value" id="progressPercent">0%</div>
                <div class="stat-label">PROGRESS</div>
                <div class="progress-bar-container">
                    <div class="progress-bar" id="progressBar">0%</div>
                </div>
            </div>
        </div>

        <div class="submit-section">
            <h2>[ SUBMIT FLAG ]</h2>
            <form id="submitForm" class="form-group">
                <input 
                    type="text" 
                    id="flagInput" 
                    placeholder="FLAG{xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}" 
                    autocomplete="off"
                    required
                >
                <button type="submit">EXECUTE</button>
            </form>
            <p class="subtitle" style="margin-top: 12px;">
                > UUID-based flags | Unique per user | Validated in real-time
            </p>
        </div>

        <div class="challenges-section">
            <h2>[ AVAILABLE CHALLENGES ]</h2>
            
            <div class="filter-buttons">
                <button class="filter-btn active" data-filter="all">[*] ALL</button>
                <button class="filter-btn" data-filter="Principiante">[~] NEWBIE</button>
                <button class="filter-btn" data-filter="Intermedio">[+] INTERMEDIATE</button>
                <button class="filter-btn" data-filter="Avanzado">[!] ADVANCED</button>
                <button class="filter-btn" data-filter="Experto">[#] EXPERT</button>
                <button class="filter-btn" data-filter="completed">[✓] PWNED</button>
                <button class="filter-btn" data-filter="pending">[X] PENDING</button>
            </div>

            <div class="challenges-grid" id="challengesGrid">
            </div>
        </div>

        <footer>
            <p>[ DOCKER CTF LAB v2.0 | HACKING SIMULATION ENVIRONMENT ]</p>
            <p>[ UUID-BASED FLAGS | MQTT MONITORING | REAL-TIME VALIDATION ]</p>
            <p style="margin-top: 15px; color: var(--accent-green);">
                > STAY CURIOUS | HACK RESPONSIBLY | LEARN DOCKER
            </p>
        </footer>
    </div>

    <div id="hintModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal()">&times;</span>
            <h2 id="modalTitle" style="color: var(--accent-cyan); margin-bottom: 20px;">[ HINT ]</h2>
            <p id="modalContent" style="color: var(--text-primary); line-height: 1.8;"></p>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('matrix-bg');
        const ctx = canvas.getContext('2d');

        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()';
        const fontSize = 14;
        const columns = canvas.width / fontSize;

        const drops = [];
        for (let i = 0; i < columns; i++) {
            drops[i] = 1;
        }

        function drawMatrix() {
            ctx.fillStyle = 'rgba(10, 14, 39, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = '#00ff41';
            ctx.font = fontSize + 'px monospace';

            for (let i = 0; i < drops.length; i++) {
                const text = letters[Math.floor(Math.random() * letters.length)];
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);

                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            }
        }

        setInterval(drawMatrix, 35);

        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });

        let allChallenges = [];
        let currentFilter = 'all';

        async function loadProgress() {
            try {
                const response = await fetch('/api/progress');
                const data = await response.json();
                
                document.getElementById('studentInfo').textContent = 
                    \`[ USER: \${data.documento || 'ANONYMOUS'} | STATUS: ONLINE ]\`;
                
                document.getElementById('completedCount').textContent = 
                    \`\${data.completados.length}/\${data.total_retos}\`;
                
                document.getElementById('totalPoints').textContent = 
                    \`\${data.puntos}/\${data.total_puntos}\`;
                
                const progress = (data.completados.length / data.total_retos * 100).toFixed(1);
                document.getElementById('progressPercent').textContent = \`\${progress}%\`;
                document.getElementById('progressBar').style.width = \`\${progress}%\`;
                document.getElementById('progressBar').textContent = \`\${progress}%\`;
                
            } catch (error) {
                console.error('Error:', error);
                showNotification('[ ERROR ] Failed to load progress', 'error');
            }
        }

        async function loadChallenges() {
            try {
                const response = await fetch('/api/challenges');
                allChallenges = await response.json();
                renderChallenges();
            } catch (error) {
                console.error('Error:', error);
                showNotification('[ ERROR ] Failed to load challenges', 'error');
            }
        }

        function renderChallenges() {
            const grid = document.getElementById('challengesGrid');
            grid.innerHTML = '';
            
            const filteredChallenges = allChallenges.filter(challenge => {
                if (currentFilter === 'all') return true;
                if (currentFilter === 'completed') return challenge.completado;
                if (currentFilter === 'pending') return !challenge.completado;
                return challenge.dificultad === currentFilter;
            });

            filteredChallenges.forEach(challenge => {
                const card = document.createElement('div');
                card.className = \`challenge-card \${challenge.completado ? 'completed' : ''}\`;
                
                const dificultadClass = \`dificultad-\${challenge.dificultad.toLowerCase()}\`;
                const statusIcon = challenge.completado ? '✓' : 'X';
                
                const flagHtml = !challenge.completado ? 
                    \`<div class="challenge-flag">\${challenge.flag}</div>\` : 
                    \`<div style="color: var(--accent-green); margin-top: 12px; font-size: 0.9em;">
                        [✓] PWNED AT \${new Date(challenge.fecha_completado).toLocaleString('es-ES')}
                     </div>\`;
                
                card.innerHTML = \`
                    <div class="challenge-header">
                        <div>
                            <div class="challenge-title">[\${statusIcon}] \${challenge.nombre}</div>
                            <div class="challenge-meta">
                                <span class="\${dificultadClass}">⚡ \${challenge.dificultad.toUpperCase()}</span>
                                <span style="color: var(--accent-cyan);">🏆 \${challenge.puntos} PTS</span>
                                <span style="color: var(--text-secondary);">📁 \${challenge.categoria}</span>
                            </div>
                        </div>
                        <span class="challenge-badge">#\${challenge.id.toString().padStart(2, '0')}</span>
                    </div>
                    <div class="challenge-description">\${challenge.descripcion}</div>
                    \${flagHtml}
                    \${!challenge.completado ? \`<button class="hint-button" onclick="showHint(\${challenge.id})">💡 SHOW HINT</button>\` : ''}
                \`;
                
                grid.appendChild(card);
            });
        }

        async function showHint(retoId) {
            try {
                const response = await fetch(\`/api/hint/\${retoId}\`);
                const data = await response.json();
                
                if (data.success) {
                    document.getElementById('modalTitle').textContent = \`[ HINT - \${data.nombre} ]\`;
                    document.getElementById('modalContent').textContent = '> ' + data.pista;
                    document.getElementById('hintModal').style.display = 'block';
                }
            } catch (error) {
                console.error('Error:', error);
            }
        }

        function closeModal() {
            document.getElementById('hintModal').style.display = 'none';
        }

        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                currentFilter = this.dataset.filter;
                renderChallenges();
            });
        });

        document.getElementById('submitForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const flagInput = document.getElementById('flagInput');
            const flag = flagInput.value.trim();

            if (!flag) {
                showNotification('[ WARNING ] Please enter a flag', 'warning');
                return;
            }

            try {
                const response = await fetch('/api/submit', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ flag })
                });

                const result = await response.json();

                if (result.success) {
                    showNotification(\`[ SUCCESS ] \${result.message}\`, 'success');
                    flagInput.value = '';
                    
                    await loadProgress();
                    await loadChallenges();

                    if (result.all_completed) {
                        setTimeout(() => {
                            showCongratulations();
                        }, 1500);
                    }
                } else {
                    showNotification(\`[ DENIED ] \${result.message}\`, 'error');
                }
            } catch (error) {
                console.error('Error:', error);
                showNotification('[ ERROR ] Failed to submit flag', 'error');
            }
        });

        function showNotification(message, type = 'success') {
            const notification = document.createElement('div');
            notification.className = \`notification \${type}\`;
            notification.textContent = message;
            document.body.appendChild(notification);

            setTimeout(() => {
                notification.remove();
            }, 5000);
        }

        function showCongratulations() {
            document.getElementById('modalTitle').textContent = '[ SYSTEM PWNED ]';
            document.getElementById('modalContent').innerHTML = \`
                <div style="text-align: center;">
                    <h2 style="color: var(--accent-green); font-size: 2em; margin: 20px 0;">
                        �� CONGRATULATIONS! 🏆
                    </h2>
                    <p style="font-size: 1.2em; margin: 20px 0; color: var(--accent-cyan);">
                        YOU HAVE SUCCESSFULLY COMPLETED ALL CHALLENGES!
                    </p>
                    <p style="color: var(--text-primary); margin-top: 20px;">
                        > You are now a Docker Master!<br>
                        > All systems compromised.<br>
                        > Welcome to the elite.
                    </p>
                </div>
            \`;
            document.getElementById('hintModal').style.display = 'block';
        }

        document.getElementById('hintModal').addEventListener('click', function(e) {
            if (e.target === this) {
                closeModal();
            }
        });

        loadProgress();
        loadChallenges();

        setInterval(() => {
            loadProgress();
        }, 30000);
    </script>
</body>
</html>
EOF
