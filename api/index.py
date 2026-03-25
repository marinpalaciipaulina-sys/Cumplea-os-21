from flask import Flask, jsonify, render_template_string
import os
from pathlib import Path

app = Flask(__name__)

# Mensajes románticos para las velas
LOVE_MESSAGES = [
    "Eres mi lugar seguro",
    "Gracias por existir en mi vida",
    "Contigo todo es más bonito",
    "Eres mi sueño hecho realidad",
    "Cada día a tu lado es un regalo",
    "Me haces mejor persona",
    "Tu sonrisa es mi sol",
    "Eres mi historia de amor favorita",
    "Mi corazón late por ti",
    "Para siempre empezó cuando te conocí 💖"
]

# Contenido HTML como string (para Vercel)
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Una Experiencia Para Ti</title>
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    
    <script type="importmap">
    {
        "imports": {
            "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
            "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
        }
    }
    </script>
    
    <style>
        :root {
            --bg-deep: #0a0608;
            --bg-warm: #1a0f12;
            --accent-gold: #d4a574;
            --accent-rose: #c97b84;
            --accent-cream: #f5e6d3;
            --text-light: #faf3ef;
            --text-muted: #a89080;
            --glow-warm: rgba(212, 165, 116, 0.4);
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Cormorant Garamond', serif;
            background: var(--bg-deep);
            color: var(--text-light);
            overflow: hidden;
            width: 100vw;
            height: 100vh;
        }
        
        #canvas-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
        }
        
        #particles-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 2;
            pointer-events: none;
        }
        
        .ui-layer {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 10;
            pointer-events: none;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        
        .cinematic-bar {
            position: fixed;
            left: 0;
            width: 100%;
            height: 8vh;
            background: var(--bg-deep);
            z-index: 100;
        }
        
        .cinematic-bar.top { top: 0; }
        .cinematic-bar.bottom { bottom: 0; }
        
        .scene {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            opacity: 0;
            pointer-events: none;
            z-index: 20;
        }
        
        .scene.active {
            pointer-events: auto;
        }
        
        .intro-text {
            font-family: 'Playfair Display', serif;
            font-size: clamp(1.5rem, 4vw, 2.5rem);
            font-weight: 400;
            font-style: italic;
            color: var(--text-light);
            text-align: center;
            opacity: 0;
            text-shadow: 0 0 40px var(--glow-warm);
            letter-spacing: 0.1em;
            line-height: 1.8;
        }
        
        .intro-text span {
            display: block;
        }
        
        .birthday-message {
            font-family: 'Playfair Display', serif;
            font-size: clamp(2rem, 6vw, 4.5rem);
            font-weight: 700;
            text-align: center;
            background: linear-gradient(135deg, var(--accent-gold), var(--accent-rose), var(--accent-cream));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            filter: drop-shadow(0 0 30px var(--glow-warm));
            opacity: 0;
        }
        
        .continue-btn {
            margin-top: 3rem;
            padding: 1rem 3rem;
            font-family: 'Cormorant Garamond', serif;
            font-size: 1.2rem;
            font-weight: 600;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: var(--accent-gold);
            background: transparent;
            border: 1px solid var(--accent-gold);
            cursor: pointer;
            opacity: 0;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            pointer-events: auto;
        }
        
        .continue-btn:hover {
            background: var(--accent-gold);
            color: var(--bg-deep);
            box-shadow: 0 0 40px var(--glow-warm);
            transform: scale(1.05);
        }
        
        #cake-scene {
            pointer-events: none;
        }
        
        .game-ui {
            position: fixed;
            bottom: 12vh;
            left: 50%;
            transform: translateX(-50%);
            text-align: center;
            z-index: 50;
            opacity: 0;
        }
        
        .instruction {
            font-size: clamp(1rem, 2vw, 1.4rem);
            color: var(--text-muted);
            margin-bottom: 1rem;
            font-style: italic;
        }
        
        .progress-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
        }
        
        .progress-text {
            font-size: 1.2rem;
            color: var(--accent-gold);
            font-weight: 600;
        }
        
        .progress-dots {
            display: flex;
            gap: 0.5rem;
        }
        
        .progress-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: var(--bg-warm);
            border: 1px solid var(--accent-gold);
            transition: all 0.5s ease;
        }
        
        .progress-dot.lit {
            background: var(--accent-gold);
            box-shadow: 0 0 15px var(--accent-gold);
        }
        
        .message-popup {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            padding: 2rem 3rem;
            background: linear-gradient(135deg, rgba(26, 15, 18, 0.95), rgba(10, 6, 8, 0.98));
            border: 1px solid var(--accent-gold);
            border-radius: 2px;
            z-index: 100;
            opacity: 0;
            pointer-events: none;
        }
        
        .message-popup p {
            font-family: 'Playfair Display', serif;
            font-size: clamp(1.3rem, 3vw, 2rem);
            font-style: italic;
            color: var(--text-light);
            text-align: center;
        }
        
        .final-message {
            text-align: center;
            opacity: 0;
        }
        
        .final-message h1 {
            font-family: 'Playfair Display', serif;
            font-size: clamp(2rem, 5vw, 4rem);
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-gold), var(--accent-cream), var(--accent-rose));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 2rem;
            line-height: 1.3;
        }
        
        .final-message p {
            font-size: clamp(1.2rem, 2.5vw, 1.8rem);
            color: var(--text-muted);
            font-style: italic;
            max-width: 600px;
        }
        
        #confetti-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 15;
            pointer-events: none;
        }
        
        #loading-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: var(--bg-deep);
            z-index: 1000;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        
        .loader {
            width: 60px;
            height: 60px;
            border: 2px solid var(--bg-warm);
            border-top-color: var(--accent-gold);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        .loading-text {
            margin-top: 2rem;
            font-size: 1rem;
            color: var(--text-muted);
            letter-spacing: 0.3em;
            text-transform: uppercase;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .vignette {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 5;
            background: radial-gradient(ellipse at center, transparent 40%, rgba(10, 6, 8, 0.8) 100%);
        }
        
        .glow-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 6;
            background: radial-gradient(circle at 50% 60%, rgba(212, 165, 116, 0.1) 0%, transparent 50%);
            opacity: 0;
            transition: opacity 1s ease;
        }
        
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                transition-duration: 0.01ms !important;
            }
        }
    </style>
</head>
<body>
    <div id="loading-screen">
        <div class="loader"></div>
        <p class="loading-text">Preparando tu experiencia...</p>
    </div>
    
    <div class="cinematic-bar top"></div>
    <div class="cinematic-bar bottom"></div>
    
    <div class="vignette"></div>
    <div class="glow-overlay" id="glow-overlay"></div>
    
    <div id="canvas-container"></div>
    
    <canvas id="particles-canvas"></canvas>
    <canvas id="confetti-canvas"></canvas>
    
    <div id="intro-scene" class="scene">
        <div class="intro-text">
            <span>Esta no es solo una pagina...</span>
            <span>Es algo que hice para ti...</span>
        </div>
    </div>
    
    <div id="welcome-scene" class="scene">
        <h1 class="birthday-message">Feliz cumpleanos, mi amor</h1>
        <button class="continue-btn" id="start-btn">Comenzar</button>
    </div>
    
    <div id="cake-scene" class="scene">
        <div class="game-ui" id="game-ui">
            <p class="instruction">Acerca tu cursor a cada llama y haz clic para apagarla</p>
            <div class="progress-container">
                <span class="progress-text">Velas apagadas: </span>
                <div class="progress-dots" id="progress-dots"></div>
                <span class="progress-text" id="progress-count">0/10</span>
            </div>
        </div>
    </div>
    
    <div class="message-popup" id="message-popup">
        <p id="message-text"></p>
    </div>
    
    <div id="final-scene" class="scene">
        <div class="final-message">
            <h1>Feliz cumpleanos, mi amor.<br>Este pequeno mundo lo hice solo para ti.</h1>
            <p>Con todo mi amor, siempre.</p>
        </div>
    </div>
    
    <script type="module">
        import * as THREE from 'three';
        
        const CONFIG = {
            candles: 10,
            messages: [
                "Eres mi lugar seguro",
                "Gracias por existir en mi vida",
                "Contigo todo es mas bonito",
                "Eres mi sueno hecho realidad",
                "Cada dia a tu lado es un regalo",
                "Me haces mejor persona",
                "Tu sonrisa es mi sol",
                "Eres mi historia de amor favorita",
                "Mi corazon late por ti",
                "Para siempre empezo cuando te conoci"
            ]
        };
        
        const state = {
            currentScene: 'loading',
            candlesExtinguished: [],
            mousePos: new THREE.Vector2(),
            raycaster: new THREE.Raycaster()
        };
        
        let scene, camera, renderer;
        let candles = [], flames = [], flameLights = [];
        let dustParticles;
        
        const clock = new THREE.Clock();
        
        function initThreeJS() {
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x0a0608);
            scene.fog = new THREE.FogExp2(0x0a0608, 0.05);
            
            camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.set(0, 4, 8);
            camera.lookAt(0, 1, 0);
            
            renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            renderer.shadowMap.enabled = true;
            renderer.shadowMap.type = THREE.PCFSoftShadowMap;
            renderer.toneMapping = THREE.ACESFilmicToneMapping;
            renderer.toneMappingExposure = 1.2;
            
            document.getElementById('canvas-container').appendChild(renderer.domElement);
            
            setupLights();
            createCake();
            createCandles();
            createDustParticles();
            animate();
        }
        
        function setupLights() {
            const ambient = new THREE.AmbientLight(0x1a0f12, 0.5);
            scene.add(ambient);
            
            const mainLight = new THREE.DirectionalLight(0xffd4a3, 0.8);
            mainLight.position.set(5, 10, 5);
            mainLight.castShadow = true;
            mainLight.shadow.mapSize.width = 2048;
            mainLight.shadow.mapSize.height = 2048;
            scene.add(mainLight);
            
            const fillLight = new THREE.PointLight(0xc97b84, 0.4, 20);
            fillLight.position.set(-5, 3, -5);
            scene.add(fillLight);
        }
        
        function createCake() {
            const cakeGroup = new THREE.Group();
            
            const frostingMaterial = new THREE.MeshStandardMaterial({
                color: 0xf5e6d3,
                roughness: 0.3,
                metalness: 0.1
            });
            
            const baseGeometry = new THREE.CylinderGeometry(1.8, 2, 0.8, 64);
            const baseMaterial = new THREE.MeshStandardMaterial({
                color: 0x8b5a3c,
                roughness: 0.6,
                metalness: 0.1
            });
            const baseLayer = new THREE.Mesh(baseGeometry, baseMaterial);
            baseLayer.position.y = 0.4;
            baseLayer.castShadow = true;
            baseLayer.receiveShadow = true;
            cakeGroup.add(baseLayer);
            
            const midGeometry = new THREE.CylinderGeometry(1.4, 1.6, 0.7, 64);
            const midLayer = new THREE.Mesh(midGeometry, baseMaterial);
            midLayer.position.y = 1.15;
            midLayer.castShadow = true;
            cakeGroup.add(midLayer);
            
            const topGeometry = new THREE.CylinderGeometry(1, 1.2, 0.6, 64);
            const topLayer = new THREE.Mesh(topGeometry, baseMaterial);
            topLayer.position.y = 1.8;
            topLayer.castShadow = true;
            cakeGroup.add(topLayer);
            
            const topFrostingGeometry = new THREE.CylinderGeometry(1.05, 1.05, 0.1, 64);
            const topFrosting = new THREE.Mesh(topFrostingGeometry, frostingMaterial);
            topFrosting.position.y = 2.15;
            cakeGroup.add(topFrosting);
            
            const plateGeometry = new THREE.CylinderGeometry(2.5, 2.5, 0.1, 64);
            const plateMaterial = new THREE.MeshStandardMaterial({
                color: 0xe8ddd0,
                roughness: 0.2,
                metalness: 0.3
            });
            const plate = new THREE.Mesh(plateGeometry, plateMaterial);
            plate.position.y = -0.05;
            cakeGroup.add(plate);
            
            scene.add(cakeGroup);
        }
        
        function createCandles() {
            const radius = 0.7;
            
            for (let i = 0; i < CONFIG.candles; i++) {
                const angle = (i / CONFIG.candles) * Math.PI * 2;
                const x = Math.cos(angle) * radius;
                const z = Math.sin(angle) * radius;
                createCandle(x, z, i);
            }
        }
        
        function createCandle(x, z, index) {
            const candleGroup = new THREE.Group();
            
            const stickGeometry = new THREE.CylinderGeometry(0.04, 0.05, 0.4, 16);
            const stickMaterial = new THREE.MeshStandardMaterial({
                color: 0xfaf3ef,
                roughness: 0.5
            });
            const stick = new THREE.Mesh(stickGeometry, stickMaterial);
            stick.position.y = 2.35;
            candleGroup.add(stick);
            
            const flameGeometry = new THREE.ConeGeometry(0.025, 0.08, 8);
            const flameMaterial = new THREE.MeshStandardMaterial({
                color: 0xffcc66,
                emissive: 0xff9933,
                emissiveIntensity: 2,
                transparent: true,
                opacity: 0.9
            });
            const flame = new THREE.Mesh(flameGeometry, flameMaterial);
            flame.position.y = 2.7;
            flame.userData = { isFlame: true, index: index, lit: true, originalY: 2.7 };
            candleGroup.add(flame);
            flames.push(flame);
            
            const glowGeometry = new THREE.SphereGeometry(0.08, 16, 16);
            const glowMaterial = new THREE.MeshBasicMaterial({
                color: 0xff9944,
                transparent: true,
                opacity: 0.3
            });
            const glow = new THREE.Mesh(glowGeometry, glowMaterial);
            glow.position.y = 2.7;
            flame.userData.glow = glow;
            candleGroup.add(glow);
            
            const candleLight = new THREE.PointLight(0xff9944, 0.3, 2, 2);
            candleLight.position.y = 2.75;
            candleGroup.add(candleLight);
            flameLights.push(candleLight);
            
            candleGroup.position.set(x, 0, z);
            candles.push(candleGroup);
            scene.add(candleGroup);
        }
        
        function createDustParticles() {
            const particleCount = 300;
            const positions = new Float32Array(particleCount * 3);
            const colors = new Float32Array(particleCount * 3);
            
            for (let i = 0; i < particleCount; i++) {
                positions[i * 3] = (Math.random() - 0.5) * 20;
                positions[i * 3 + 1] = Math.random() * 10;
                positions[i * 3 + 2] = (Math.random() - 0.5) * 20;
                
                colors[i * 3] = 0.83;
                colors[i * 3 + 1] = 0.65;
                colors[i * 3 + 2] = 0.46;
            }
            
            const geometry = new THREE.BufferGeometry();
            geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
            
            const material = new THREE.PointsMaterial({
                size: 0.05,
                vertexColors: true,
                transparent: true,
                opacity: 0.6,
                blending: THREE.AdditiveBlending
            });
            
            dustParticles = new THREE.Points(geometry, material);
            scene.add(dustParticles);
        }
        
        function animate() {
            requestAnimationFrame(animate);
            
            const time = clock.getElapsedTime();
            
            if (dustParticles) {
                dustParticles.rotation.y = time * 0.02;
            }
            
            flames.forEach((flame, index) => {
                if (flame.userData.lit) {
                    const flicker = Math.sin(time * 10 + index) * 0.02;
                    flame.scale.y = 1 + flicker;
                    flame.position.y = flame.userData.originalY + Math.sin(time * 8 + index) * 0.01;
                    
                    if (flame.userData.glow) {
                        flame.userData.glow.material.opacity = 0.25 + flicker * 2;
                    }
                    
                    if (flameLights[index]) {
                        flameLights[index].intensity = 0.3 + flicker * 2;
                    }
                }
            });
            
            renderer.render(scene, camera);
        }
        
        const particlesCanvas = document.getElementById('particles-canvas');
        const pCtx = particlesCanvas.getContext('2d');
        let particlesArray = [];
        
        function initParticlesCanvas() {
            particlesCanvas.width = window.innerWidth;
            particlesCanvas.height = window.innerHeight;
            
            for (let i = 0; i < 80; i++) {
                particlesArray.push({
                    x: Math.random() * particlesCanvas.width,
                    y: Math.random() * particlesCanvas.height,
                    size: Math.random() * 3 + 1,
                    speedX: (Math.random() - 0.5) * 0.5,
                    speedY: (Math.random() - 0.5) * 0.5,
                    opacity: Math.random() * 0.5 + 0.2
                });
            }
        }
        
        function animateParticles() {
            pCtx.clearRect(0, 0, particlesCanvas.width, particlesCanvas.height);
            
            particlesArray.forEach(p => {
                p.x += p.speedX;
                p.y += p.speedY;
                
                if (p.x < 0) p.x = particlesCanvas.width;
                if (p.x > particlesCanvas.width) p.x = 0;
                if (p.y < 0) p.y = particlesCanvas.height;
                if (p.y > particlesCanvas.height) p.y = 0;
                
                pCtx.beginPath();
                pCtx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                pCtx.fillStyle = `rgba(212, 165, 116, ${p.opacity})`;
                pCtx.fill();
            });
            
            requestAnimationFrame(animateParticles);
        }
        
        const confettiCanvas = document.getElementById('confetti-canvas');
        const cCtx = confettiCanvas.getContext('2d');
        let confettiArray = [];
        let confettiActive = false;
        
        function initConfettiCanvas() {
            confettiCanvas.width = window.innerWidth;
            confettiCanvas.height = window.innerHeight;
        }
        
        function createHeartConfetti(intensity = 50) {
            for (let i = 0; i < intensity; i++) {
                confettiArray.push({
                    x: Math.random() * confettiCanvas.width,
                    y: -20 - Math.random() * 100,
                    size: Math.random() * 15 + 8,
                    speedY: Math.random() * 3 + 2,
                    speedX: (Math.random() - 0.5) * 2,
                    rotation: Math.random() * Math.PI * 2,
                    rotationSpeed: (Math.random() - 0.5) * 0.1,
                    opacity: Math.random() * 0.5 + 0.5,
                    hue: Math.random() > 0.5 ? 350 : 35,
                    wobble: Math.random() * Math.PI * 2
                });
            }
            confettiActive = true;
        }
        
        function drawHeart(ctx, x, y, size, rotation, hue, opacity) {
            ctx.save();
            ctx.translate(x, y);
            ctx.rotate(rotation);
            ctx.scale(size / 20, size / 20);
            
            ctx.beginPath();
            ctx.moveTo(0, -5);
            ctx.bezierCurveTo(-10, -15, -20, 0, 0, 15);
            ctx.bezierCurveTo(20, 0, 10, -15, 0, -5);
            ctx.closePath();
            
            ctx.fillStyle = `hsla(${hue}, 70%, 65%, ${opacity})`;
            ctx.fill();
            
            ctx.shadowColor = `hsla(${hue}, 70%, 65%, 0.5)`;
            ctx.shadowBlur = 10;
            ctx.fill();
            
            ctx.restore();
        }
        
        function animateConfetti() {
            if (!confettiActive) {
                requestAnimationFrame(animateConfetti);
                return;
            }
            
            cCtx.clearRect(0, 0, confettiCanvas.width, confettiCanvas.height);
            
            confettiArray = confettiArray.filter(c => c.y < confettiCanvas.height + 50);
            
            confettiArray.forEach(c => {
                c.y += c.speedY;
                c.x += c.speedX + Math.sin(c.wobble) * 0.5;
                c.wobble += 0.05;
                c.rotation += c.rotationSpeed;
                
                drawHeart(cCtx, c.x, c.y, c.size, c.rotation, c.hue, c.opacity);
            });
            
            requestAnimationFrame(animateConfetti);
        }
        
        const scenes = {
            intro: document.getElementById('intro-scene'),
            welcome: document.getElementById('welcome-scene'),
            cake: document.getElementById('cake-scene'),
            final: document.getElementById('final-scene')
        };
        
        function showScene(sceneName) {
            Object.values(scenes).forEach(s => {
                s.classList.remove('active');
                s.style.opacity = '0';
            });
            
            state.currentScene = sceneName;
            
            setTimeout(() => {
                scenes[sceneName].classList.add('active');
            }, 100);
        }
        
        function playIntroScene() {
            showScene('intro');
            
            const introText = document.querySelector('.intro-text');
            
            gsap.timeline()
                .to(scenes.intro, { opacity: 1, duration: 0.5 })
                .to(introText, { opacity: 1, duration: 2, ease: 'power2.out' })
                .to(introText.querySelectorAll('span')[0], { opacity: 1, duration: 2, ease: 'power2.out' }, '-=1.5')
                .to(introText.querySelectorAll('span')[1], { opacity: 1, duration: 2, ease: 'power2.out', delay: 1 })
                .to({}, { duration: 2 })
                .to(introText, { opacity: 0, duration: 1.5, onComplete: playWelcomeScene });
            
            gsap.to(camera.position, { z: 6, duration: 8, ease: 'power1.inOut' });
        }
        
        function playWelcomeScene() {
            showScene('welcome');
            createHeartConfetti(100);
            
            gsap.timeline()
                .to(scenes.welcome, { opacity: 1, duration: 0.5 })
                .to('.birthday-message', { opacity: 1, duration: 1.5, ease: 'power2.out' })
                .to('.continue-btn', { opacity: 1, duration: 1, ease: 'power2.out' }, '-=0.5');
            
            gsap.to('#glow-overlay', { opacity: 1, duration: 2 });
        }
        
        function playCakeScene() {
            showScene('cake');
            
            gsap.to(camera.position, { x: 0, y: 3, z: 5, duration: 2, ease: 'power2.inOut' });
            
            gsap.timeline()
                .to(scenes.cake, { opacity: 1, duration: 0.5 })
                .to('#game-ui', { opacity: 1, duration: 1, ease: 'power2.out', delay: 1 });
            
            const dotsContainer = document.getElementById('progress-dots');
            dotsContainer.innerHTML = '';
            for (let i = 0; i < CONFIG.candles; i++) {
                const dot = document.createElement('div');
                dot.className = 'progress-dot lit';
                dotsContainer.appendChild(dot);
            }
            
            setupInteraction();
        }
        
        function setupInteraction() {
            renderer.domElement.addEventListener('mousemove', onMouseMove);
            renderer.domElement.addEventListener('click', onMouseClick);
        }
        
        function onMouseMove(event) {
            state.mousePos.x = (event.clientX / window.innerWidth) * 2 - 1;
            state.mousePos.y = -(event.clientY / window.innerHeight) * 2 + 1;
            
            if (state.currentScene !== 'cake') return;
            
            state.raycaster.setFromCamera(state.mousePos, camera);
            const intersects = state.raycaster.intersectObjects(flames, true);
            
            flames.forEach(flame => {
                if (flame.userData.lit) {
                    gsap.to(flame.scale, { x: 1, y: 1, duration: 0.3 });
                    if (flame.userData.glow) {
                        gsap.to(flame.userData.glow.material, { opacity: 0.3, duration: 0.3 });
                    }
                }
            });
            
            if (intersects.length > 0) {
                const flame = intersects[0].object;
                if (flame.userData.lit) {
                    gsap.to(flame.scale, { x: 1.2, y: 1.3, duration: 0.2 });
                    if (flame.userData.glow) {
                        gsap.to(flame.userData.glow.material, { opacity: 0.6, duration: 0.2 });
                    }
                    renderer.domElement.style.cursor = 'pointer';
                }
            } else {
                renderer.domElement.style.cursor = 'default';
            }
        }
        
        function onMouseClick(event) {
            if (state.currentScene !== 'cake') return;
            
            state.raycaster.setFromCamera(state.mousePos, camera);
            const intersects = state.raycaster.intersectObjects(flames, true);
            
            if (intersects.length > 0) {
                const flame = intersects[0].object;
                if (flame.userData.lit) {
                    extinguishCandle(flame);
                }
            }
        }
        
        function extinguishCandle(flame) {
            const index = flame.userData.index;
            flame.userData.lit = false;
            state.candlesExtinguished.push(index);
            
            updateProgress();
            
            gsap.timeline()
                .to(flame.scale, { x: 0.1, y: 0.1, duration: 0.3, ease: 'power2.in' })
                .to(flame.material, { opacity: 0, duration: 0.3 }, '-=0.3')
                .to(flame.userData.glow.material, { opacity: 0, duration: 0.3 }, '-=0.3');
            
            gsap.to(flameLights[index], { intensity: 0, duration: 0.5 });
            
            showMessage(index);
            
            if (state.candlesExtinguished.length >= CONFIG.candles) {
                setTimeout(playFinalScene, 2500);
            }
        }
        
        function updateProgress() {
            const count = state.candlesExtinguished.length;
            document.getElementById('progress-count').textContent = `${count}/${CONFIG.candles}`;
            
            const dots = document.querySelectorAll('.progress-dot');
            dots.forEach((dot, i) => {
                if (i < count) {
                    dot.classList.remove('lit');
                }
            });
        }
        
        function showMessage(index) {
            const popup = document.getElementById('message-popup');
            const text = document.getElementById('message-text');
            
            text.textContent = CONFIG.messages[index];
            
            gsap.timeline()
                .to(popup, { opacity: 1, duration: 0.5, pointerEvents: 'auto' })
                .to(popup, { opacity: 0, duration: 0.5, delay: 2, pointerEvents: 'none' });
        }
        
        function playFinalScene() {
            showScene('final');
            createHeartConfetti(200);
            
            gsap.to(camera.position, { x: 0, y: 5, z: 10, duration: 3, ease: 'power2.inOut' });
            gsap.to('#game-ui', { opacity: 0, duration: 1 });
            
            gsap.timeline()
                .to(scenes.final, { opacity: 1, duration: 0.5 })
                .to('.final-message', { opacity: 1, duration: 2, ease: 'power2.out' })
                .from('.final-message h1', { y: 30, opacity: 0, duration: 1.5, ease: 'power2.out' }, '-=1.5')
                .from('.final-message p', { y: 20, opacity: 0, duration: 1, ease: 'power2.out' }, '-=0.5');
            
            gsap.to('#glow-overlay', { opacity: 0.5, duration: 2 });
        }
        
        function init() {
            initThreeJS();
            initParticlesCanvas();
            initConfettiCanvas();
            
            animateParticles();
            animateConfetti();
            
            document.getElementById('start-btn').addEventListener('click', () => {
                gsap.to('.continue-btn', { opacity: 0, duration: 0.3 });
                gsap.to('.birthday-message', { opacity: 0, duration: 0.5 });
                setTimeout(playCakeScene, 500);
            });
            
            setTimeout(() => {
                gsap.to('#loading-screen', {
                    opacity: 0,
                    duration: 1,
                    onComplete: () => {
                        document.getElementById('loading-screen').style.display = 'none';
                        playIntroScene();
                    }
                });
            }, 1500);
        }
        
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
            
            particlesCanvas.width = window.innerWidth;
            particlesCanvas.height = window.innerHeight;
            confettiCanvas.width = window.innerWidth;
            confettiCanvas.height = window.innerHeight;
        });
        
        init();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Sirve la página principal con la experiencia de cumpleaños"""
    return render_template_string(HTML_CONTENT)

@app.route('/api/message/<int:candle>')
def get_message(candle):
    """Retorna un mensaje romántico para cada vela apagada"""
    if 0 <= candle < len(LOVE_MESSAGES):
        return jsonify({
            'message': LOVE_MESSAGES[candle],
            'candle': candle
        })
    return jsonify({'message': 'Te amo 💕', 'candle': candle})

@app.route('/api/messages')
def get_all_messages():
    """Retorna todos los mensajes románticos"""
    return jsonify(LOVE_MESSAGES)

# Handler para Vercel
def handler(request):
    return app(request.environ, lambda status, headers: None)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)