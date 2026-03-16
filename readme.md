<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SentinelVote AI — Secure Voting</title>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
:root {
  --ink: #0a0c0f;
  --ink2: #111318;
  --surface: #13161c;
  --surface2: #1a1e27;
  --border: rgba(255,255,255,0.07);
  --border2: rgba(255,255,255,0.12);
  --blue: #2563ff;
  --blue2: #3b82f6;
  --cyan: #06d6d6;
  --gold: #f59e0b;
  --red: #ef4444;
  --green: #22c55e;
  --text: #e8eaf0;
  --muted: #6b7280;
  --muted2: #9ca3af;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  font-family:'DM Sans',sans-serif;
  background:var(--ink);
  color:var(--text);
  overflow-x:hidden;
  cursor:none;
}

/* CURSOR */
.cur-dot,.cur-ring{position:fixed;pointer-events:none;z-index:9999;border-radius:50%;transform:translate(-50%,-50%)}
.cur-dot{width:5px;height:5px;background:var(--cyan);transition:transform .1s}
.cur-ring{width:32px;height:32px;border:1.5px solid rgba(6,214,214,.4);transition:transform .12s,width .2s,height .2s}
body:has(a:hover) .cur-ring,body:has(button:hover) .cur-ring{width:44px;height:44px;border-color:var(--cyan)}

/* NOISE OVERLAY */
body::before{
  content:'';position:fixed;inset:0;z-index:1;pointer-events:none;opacity:.025;
  background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}

/* SCAN LINE */
body::after{
  content:'';position:fixed;top:-100%;left:0;width:100%;height:2px;
  background:linear-gradient(90deg,transparent,rgba(6,214,214,.3),transparent);
  z-index:2;pointer-events:none;
  animation:scan 8s linear infinite;
}
@keyframes scan{to{top:110%}}

/* BG GRID */
.grid-bg{
  position:fixed;inset:0;z-index:0;
  background-image:
    linear-gradient(rgba(37,99,255,.03) 1px,transparent 1px),
    linear-gradient(90deg,rgba(37,99,255,.03) 1px,transparent 1px);
  background-size:48px 48px;
  animation:gridPulse 8s ease infinite;
}
@keyframes gridPulse{0%,100%{opacity:.5}50%{opacity:1}}

/* TOP DEMO BANNER */
.demo-banner{
  position:relative;z-index:10;
  background:linear-gradient(90deg,#0d1b3e,#111827,#0d1b3e);
  border-bottom:1px solid rgba(37,99,255,.3);
  padding:10px 24px;
  display:flex;align-items:center;justify-content:center;gap:16px;
  overflow:hidden;
}
.demo-banner::before{
  content:'';position:absolute;inset:0;
  background:linear-gradient(90deg,transparent,rgba(37,99,255,.08),transparent);
  animation:shimmer 3s ease infinite;
}
@keyframes shimmer{0%{transform:translateX(-100%)}100%{transform:translateX(100%)}}
.demo-badge{
  font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:600;
  letter-spacing:.15em;text-transform:uppercase;
  background:rgba(37,99,255,.2);border:1px solid rgba(37,99,255,.4);
  color:var(--blue2);padding:3px 10px;border-radius:2px;
  animation:badgePulse 2s ease infinite;
}
@keyframes badgePulse{0%,100%{box-shadow:0 0 0 0 rgba(37,99,255,.4)}50%{box-shadow:0 0 0 6px rgba(37,99,255,0)}}
.demo-text{font-size:13px;color:var(--muted2);letter-spacing:.01em}
.demo-link{
  display:inline-flex;align-items:center;gap:6px;
  background:linear-gradient(135deg,#1d4ed8,#2563ff);
  color:#fff;text-decoration:none;
  font-size:12px;font-weight:500;letter-spacing:.03em;
  padding:6px 16px;border-radius:3px;
  border:1px solid rgba(59,130,246,.4);
  transition:all .2s;
  position:relative;overflow:hidden;
}
.demo-link:hover{transform:translateY(-1px);box-shadow:0 8px 24px rgba(37,99,255,.4)}
.demo-link svg{width:12px;height:12px}

/* NAV */
nav{
  position:sticky;top:0;z-index:100;
  display:flex;align-items:center;justify-content:space-between;
  padding:16px 48px;
  background:rgba(10,12,15,.85);
  backdrop-filter:blur(24px);
  border-bottom:1px solid var(--border);
}
.nav-logo{
  display:flex;align-items:center;gap:10px;
  font-family:'Bebas Neue',sans-serif;font-size:22px;letter-spacing:.06em;
  color:var(--text);text-decoration:none;
}
.logo-shield{
  width:28px;height:28px;
  background:linear-gradient(135deg,var(--blue),var(--cyan));
  clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);
  display:flex;align-items:center;justify-content:center;
  font-size:13px;color:#fff;
  animation:shieldPulse 4s ease infinite;
}
@keyframes shieldPulse{0%,100%{filter:brightness(1)}50%{filter:brightness(1.3)}}
.nav-links{display:flex;gap:4px}
.nav-link{
  padding:6px 14px;border-radius:3px;font-size:13px;color:var(--muted2);
  text-decoration:none;transition:all .2s;
  font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.05em;
}
.nav-link:hover{color:var(--text);background:rgba(255,255,255,.05)}
.nav-cta{
  background:rgba(37,99,255,.15);border:1px solid rgba(37,99,255,.3);
  color:var(--blue2);padding:7px 18px;border-radius:3px;
  font-size:12px;font-weight:500;text-decoration:none;letter-spacing:.04em;
  transition:all .2s;font-family:'JetBrains Mono',monospace;
}
.nav-cta:hover{background:rgba(37,99,255,.3);box-shadow:0 0 20px rgba(37,99,255,.3)}

/* HERO */
.hero{
  position:relative;z-index:5;
  min-height:90vh;display:flex;align-items:center;justify-content:center;
  padding:80px 48px;text-align:center;
  overflow:hidden;
}
.hero-orbs{position:absolute;inset:0;pointer-events:none}
.orb{
  position:absolute;border-radius:50%;filter:blur(80px);opacity:.15;
  animation:orbFloat linear infinite;
}
.orb1{width:600px;height:600px;background:var(--blue);top:-200px;left:-200px;animation-duration:20s}
.orb2{width:400px;height:400px;background:var(--cyan);bottom:-100px;right:-100px;animation-duration:15s}
.orb3{width:300px;height:300px;background:#7c3aed;top:50%;left:50%;animation-duration:18s}
@keyframes orbFloat{0%{transform:translate(0,0) scale(1)}33%{transform:translate(30px,-20px) scale(1.05)}66%{transform:translate(-20px,30px) scale(.95)}100%{transform:translate(0,0) scale(1)}}

.hero-tag{
  display:inline-flex;align-items:center;gap:8px;
  padding:5px 16px;border-radius:2px;
  border:1px solid rgba(6,214,214,.3);background:rgba(6,214,214,.05);
  font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.12em;
  color:var(--cyan);text-transform:uppercase;
  margin-bottom:28px;
  animation:fadeSlideUp .8s ease both;
}
.hero-tag-dot{width:6px;height:6px;background:var(--cyan);border-radius:50%;animation:tagPulse 1.5s ease infinite}
@keyframes tagPulse{0%,100%{opacity:1;box-shadow:0 0 0 0 rgba(6,214,214,.5)}50%{opacity:.7;box-shadow:0 0 0 8px rgba(6,214,214,0)}}

.hero-title{
  font-family:'Bebas Neue',sans-serif;
  font-size:clamp(64px,10vw,128px);
  line-height:.92;letter-spacing:.02em;
  margin-bottom:8px;
  animation:fadeSlideUp .8s ease .1s both;
}
.hero-title span{
  display:block;
  background:linear-gradient(135deg,#fff 30%,var(--blue2));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
}
.hero-title .accent{
  background:linear-gradient(135deg,var(--cyan),var(--blue2));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  font-size:clamp(48px,7vw,96px);
}
.hero-sub{
  font-size:17px;line-height:1.7;color:var(--muted2);
  max-width:560px;margin:0 auto 40px;font-weight:300;
  animation:fadeSlideUp .8s ease .2s both;
}
.hero-sub strong{color:var(--text);font-weight:500}

.hero-actions{
  display:flex;gap:14px;justify-content:center;flex-wrap:wrap;
  animation:fadeSlideUp .8s ease .3s both;
  margin-bottom:64px;
}
.btn-primary{
  display:inline-flex;align-items:center;gap:8px;
  background:linear-gradient(135deg,#1d4ed8,var(--blue));
  color:#fff;text-decoration:none;padding:14px 28px;border-radius:3px;
  font-size:14px;font-weight:500;letter-spacing:.03em;border:none;cursor:pointer;
  box-shadow:0 8px 32px rgba(37,99,255,.3),inset 0 1px 0 rgba(255,255,255,.1);
  transition:all .3s;position:relative;overflow:hidden;
}
.btn-primary::after{
  content:'';position:absolute;inset:0;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.1),transparent);
  transform:skewX(-20deg) translateX(-200%);
  transition:transform .4s;
}
.btn-primary:hover::after{transform:skewX(-20deg) translateX(200%)}
.btn-primary:hover{transform:translateY(-2px);box-shadow:0 16px 48px rgba(37,99,255,.5)}
.btn-secondary{
  display:inline-flex;align-items:center;gap:8px;
  background:transparent;color:var(--text);
  border:1px solid var(--border2);
  padding:13px 24px;border-radius:3px;
  font-size:14px;font-weight:400;letter-spacing:.02em;text-decoration:none;
  transition:all .2s;
}
.btn-secondary:hover{background:rgba(255,255,255,.05);border-color:rgba(255,255,255,.2)}

/* STATS STRIP */
.hero-stats{
  display:flex;gap:0;justify-content:center;
  border:1px solid var(--border);border-radius:4px;
  background:var(--surface);overflow:hidden;
  max-width:560px;margin:0 auto;
  animation:fadeSlideUp .8s ease .4s both;
}
.stat{padding:18px 32px;text-align:center;flex:1;position:relative}
.stat+.stat::before{content:'';position:absolute;left:0;top:20%;height:60%;width:1px;background:var(--border)}
.stat-num{font-family:'Bebas Neue',sans-serif;font-size:28px;letter-spacing:.04em;color:var(--blue2);line-height:1}
.stat-label{font-size:11px;color:var(--muted);letter-spacing:.08em;text-transform:uppercase;margin-top:4px;font-family:'JetBrains Mono',monospace}

@keyframes fadeSlideUp{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:translateY(0)}}

/* SECTION */
section{position:relative;z-index:5;padding:80px 48px;max-width:1200px;margin:0 auto}
.section-tag{
  font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.18em;
  text-transform:uppercase;color:var(--blue2);margin-bottom:12px;
  display:flex;align-items:center;gap:8px;
}
.section-tag::before{content:'//';color:var(--muted);margin-right:2px}
.section-h{
  font-family:'Bebas Neue',sans-serif;font-size:clamp(36px,5vw,56px);
  letter-spacing:.04em;margin-bottom:16px;line-height:1;
}
.section-p{font-size:15px;color:var(--muted2);line-height:1.8;max-width:600px;font-weight:300}

/* LAYERS */
.layers{margin-top:48px;display:flex;flex-direction:column;gap:0}
.layer{
  display:grid;grid-template-columns:48px 1fr;gap:0;
  align-items:stretch;
  opacity:0;transform:translateX(-20px);
  transition:all .5s ease;
}
.layer.visible{opacity:1;transform:translateX(0)}
.layer-line{display:flex;flex-direction:column;align-items:center}
.layer-num{
  width:40px;height:40px;border-radius:3px;
  display:flex;align-items:center;justify-content:center;
  font-family:'Bebas Neue',sans-serif;font-size:20px;
  flex-shrink:0;
}
.layer-vert{flex:1;width:1px;background:var(--border);margin:4px auto}
.layer-body{
  padding:0 0 32px 20px;
}
.layer-title{font-size:16px;font-weight:500;margin-bottom:6px;padding-top:10px}
.layer-desc{font-size:13px;color:var(--muted2);line-height:1.7;font-weight:300}
.layer-tech{
  display:inline-flex;align-items:center;gap:6px;margin-top:10px;
  font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.1em;
  padding:3px 10px;border-radius:2px;text-transform:uppercase;
}

/* TECH STACK */
.tech-grid{
  display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:1px;
  background:var(--border);border:1px solid var(--border);border-radius:4px;
  overflow:hidden;margin-top:48px;
}
.tech-cell{
  background:var(--ink2);padding:24px;
  transition:background .2s;
  opacity:0;transform:translateY(16px);
  transition:all .4s ease;
}
.tech-cell.visible{opacity:1;transform:translateY(0)}
.tech-cell:hover{background:var(--surface)}
.tech-cat{font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin-bottom:14px}
.tech-item{font-size:13px;color:var(--muted2);margin-bottom:6px;display:flex;align-items:center;gap:8px;font-weight:300}
.tech-dot{width:4px;height:4px;border-radius:50%;background:var(--blue2);flex-shrink:0}

/* ARCH */
.arch-diagram{
  margin-top:48px;
  border:1px solid var(--border);border-radius:4px;
  background:var(--surface);overflow:hidden;
  opacity:0;transform:translateY(20px);transition:all .6s ease;
}
.arch-diagram.visible{opacity:1;transform:translateY(0)}
.arch-layer{
  padding:20px 28px;border-bottom:1px solid var(--border);
  display:grid;grid-template-columns:120px 1fr;gap:20px;align-items:center;
}
.arch-layer:last-child{border-bottom:none}
.arch-label{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.12em;text-transform:uppercase}
.arch-content{display:flex;gap:8px;flex-wrap:wrap}
.arch-chip{
  padding:4px 12px;border-radius:2px;font-size:11px;font-family:'JetBrains Mono',monospace;
  letter-spacing:.05em;border:1px solid;
}

/* TEAM */
.team-grid{
  display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px;margin-top:48px;
}
.team-card{
  background:var(--surface);border:1px solid var(--border);border-radius:4px;
  padding:24px;transition:all .3s;
  opacity:0;transform:translateY(16px);transition:all .4s ease;
}
.team-card.visible{opacity:1;transform:translateY(0)}
.team-card:hover{border-color:rgba(37,99,255,.3);background:var(--surface2);transform:translateY(-4px) !important}
.team-avatar{
  width:48px;height:48px;border-radius:3px;
  display:flex;align-items:center;justify-content:center;
  font-family:'Bebas Neue',sans-serif;font-size:20px;
  margin-bottom:14px;
}
.team-name{font-size:15px;font-weight:500;margin-bottom:3px}
.team-role{font-size:12px;color:var(--muted);font-family:'JetBrains Mono',monospace;letter-spacing:.05em}
.team-link{
  display:inline-flex;align-items:center;gap:5px;margin-top:12px;
  font-size:11px;color:var(--blue2);text-decoration:none;
  font-family:'JetBrains Mono',monospace;letter-spacing:.05em;
  transition:color .2s;
}
.team-link:hover{color:var(--cyan)}

/* FLOW */
.flow{
  margin-top:48px;display:flex;flex-direction:column;gap:0;
  position:relative;
}
.flow::before{
  content:'';position:absolute;left:20px;top:0;bottom:0;width:1px;
  background:linear-gradient(180deg,var(--blue) 0%,var(--cyan) 50%,transparent 100%);
}
.flow-step{
  display:grid;grid-template-columns:40px 1fr;gap:16px;padding-bottom:28px;
  opacity:0;transform:translateX(-12px);transition:all .4s ease;
}
.flow-step.visible{opacity:1;transform:translateX(0)}
.flow-circle{
  width:40px;height:40px;border-radius:50%;
  background:var(--ink);border:2px solid var(--blue);
  display:flex;align-items:center;justify-content:center;
  font-family:'Bebas Neue',sans-serif;font-size:16px;color:var(--blue2);
  flex-shrink:0;z-index:1;
}
.flow-content{padding-top:8px}
.flow-title{font-size:14px;font-weight:500;margin-bottom:4px}
.flow-desc{font-size:12px;color:var(--muted2);line-height:1.6;font-weight:300}

/* FOOTER */
footer{
  position:relative;z-index:5;
  border-top:1px solid var(--border);
  padding:40px 48px;
  display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:20px;
}
.footer-logo{
  font-family:'Bebas Neue',sans-serif;font-size:18px;letter-spacing:.06em;
  color:var(--muted);
}
.footer-quote{
  font-size:12px;font-style:italic;color:var(--muted);text-align:center;
  font-weight:300;letter-spacing:.02em;max-width:320px;
}
.footer-badges{display:flex;gap:8px;flex-wrap:wrap}
.badge{
  font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.12em;
  text-transform:uppercase;padding:4px 10px;border-radius:2px;
  border:1px solid var(--border2);color:var(--muted);
}

/* DIVIDER */
.divider{
  position:relative;z-index:5;
  height:1px;background:linear-gradient(90deg,transparent,var(--border),transparent);
  margin:0 48px;
}

/* SCROLLBAR */
::-webkit-scrollbar{width:3px}
::-webkit-scrollbar-track{background:var(--ink)}
::-webkit-scrollbar-thumb{background:var(--blue);border-radius:2px}

/* RESPONSIVE */
@media(max-width:768px){
  nav{padding:14px 20px}
  .hero{padding:60px 24px}
  section{padding:60px 24px}
  .hero-stats{flex-direction:column}
  .stat+.stat::before{top:0;left:20%;width:60%;height:1px}
  footer{padding:32px 24px}
}
</style>
</head>
<body>
<div class="cur-dot" id="cd"></div>
<div class="cur-ring" id="cr"></div>
<div class="grid-bg"></div>

<!-- DEMO BANNER -->
<div class="demo-banner">
  <span class="demo-badge">Live Demo</span>
  <span class="demo-text">See SentinelVote AI in action — full system running</span>
  <a href="https://drive.google.com/file/d/1Y-2H1yvLYgqMUU-CQWmSPDcPJX9LZdVR/view?usp=sharing" target="_blank" class="demo-link">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg>
    Watch Demo
  </a>
</div>

<!-- NAV -->
<nav>
  <a href="#" class="nav-logo">
    <div class="logo-shield">⬡</div>
    SentinelVote
  </a>
  <div class="nav-links">
    <a href="#security" class="nav-link">Security</a>
    <a href="#architecture" class="nav-link">Architecture</a>
    <a href="#flow" class="nav-link">Flow</a>
    <a href="#stack" class="nav-link">Stack</a>
    <a href="#team" class="nav-link">Team</a>
  </div>
  <a href="https://github.com/RuchikaaVerma/SentinelVote-AI" target="_blank" class="nav-cta">GitHub →</a>
</nav>

<!-- HERO -->
<div class="hero">
  <div class="hero-orbs">
    <div class="orb orb1"></div>
    <div class="orb orb2"></div>
    <div class="orb orb3"></div>
  </div>
  <div>
    <div class="hero-tag"><div class="hero-tag-dot"></div>AI-Secured Voting Platform · v2.0</div>
    <div class="hero-title">
      <span>Sentinel</span>
      <span class="accent">Vote AI</span>
    </div>
    <p class="hero-sub">
      <strong>What if digital elections could be more secure than physical ones?</strong><br>
      Multi-layer biometric authentication, behavioral AI fraud detection, and blockchain audit trails — all in one system.
    </p>
    <div class="hero-actions">
      <a href="https://drive.google.com/file/d/1Y-2H1yvLYgqMUU-CQWmSPDcPJX9LZdVR/view?usp=sharing" target="_blank" class="btn-primary">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg>
        Watch Demo
      </a>
      <a href="https://github.com/RuchikaaVerma/SentinelVote-AI" target="_blank" class="btn-secondary">
        View on GitHub ↗
      </a>
    </div>
    <div class="hero-stats">
      <div class="stat">
        <div class="stat-num" data-target="5">0</div>
        <div class="stat-label">Security Layers</div>
      </div>
      <div class="stat">
        <div class="stat-num" data-target="128">0</div>
        <div class="stat-label">Face Dimensions</div>
      </div>
      <div class="stat">
        <div class="stat-num" data-target="256">0</div>
        <div class="stat-label">SHA Bits</div>
      </div>
    </div>
  </div>
</div>

<div class="divider"></div>

<!-- SECURITY LAYERS -->
<section id="security">
  <div class="section-tag">Security Architecture</div>
  <div class="section-h">Five Layers.<br>Zero Compromise.</div>
  <p class="section-p">Every vote passes through five independent verification systems before being recorded. Each layer catches what the previous one might miss.</p>

  <div class="layers" id="layersList">
    <div class="layer" data-delay="0">
      <div class="layer-line">
        <div class="layer-num" style="background:rgba(239,68,68,.1);color:#ef4444;border:1px solid rgba(239,68,68,.2)">5</div>
        <div class="layer-vert"></div>
      </div>
      <div class="layer-body">
        <div class="layer-title">Blockchain Audit Trail</div>
        <div class="layer-desc">Every vote generates a SHA-256 cryptographic hash chained to the previous block. Immutable, tamper-proof, publicly verifiable. Even admin access cannot alter recorded votes.</div>
        <span class="layer-tech" style="background:rgba(239,68,68,.08);color:#ef4444;border-color:rgba(239,68,68,.2)">SHA-256 · Cryptographic Hashing</span>
      </div>
    </div>
    <div class="layer" data-delay="100">
      <div class="layer-line">
        <div class="layer-num" style="background:rgba(245,158,11,.1);color:#f59e0b;border:1px solid rgba(245,158,11,.2)">4</div>
        <div class="layer-vert"></div>
      </div>
      <div class="layer-body">
        <div class="layer-title">Vote Lock — Double Vote Prevention</div>
        <div class="layer-desc">Database-level constraint enforced alongside session-state verification. Once a vote is cast for an election, the record is locked. No workarounds, no re-submission.</div>
        <span class="layer-tech" style="background:rgba(245,158,11,.08);color:#f59e0b;border-color:rgba(245,158,11,.2)">MongoDB · Session Guard</span>
      </div>
    </div>
    <div class="layer" data-delay="200">
      <div class="layer-line">
        <div class="layer-num" style="background:rgba(37,99,255,.1);color:var(--blue2);border:1px solid rgba(37,99,255,.2)">3</div>
        <div class="layer-vert"></div>
      </div>
      <div class="layer-body">
        <div class="layer-title">Behavioral AI — Anomaly Detection</div>
        <div class="layer-desc">Isolation Forest ML model tracks keystroke dynamics, mouse trajectory, login timing, and device fingerprints. Risk score 0–1. Threshold at 0.3 triggers automatic block before voting begins.</div>
        <span class="layer-tech" style="background:rgba(37,99,255,.08);color:var(--blue2);border-color:rgba(37,99,255,.2)">Isolation Forest · sklearn</span>
      </div>
    </div>
    <div class="layer" data-delay="300">
      <div class="layer-line">
        <div class="layer-num" style="background:rgba(6,214,214,.1);color:var(--cyan);border:1px solid rgba(6,214,214,.2)">2</div>
        <div class="layer-vert"></div>
      </div>
      <div class="layer-body">
        <div class="layer-title">Face Recognition — Biometric Verification</div>
        <div class="layer-desc">dlib extracts 128-dimensional face encodings at registration. Login requires real-time webcam comparison. Euclidean distance tolerance of 0.6. Impersonation with stolen credentials fails here.</div>
        <span class="layer-tech" style="background:rgba(6,214,214,.08);color:var(--cyan);border-color:rgba(6,214,214,.2)">dlib · face_recognition · 128-D vector</span>
      </div>
    </div>
    <div class="layer" data-delay="400">
      <div class="layer-line">
        <div class="layer-num" style="background:rgba(34,197,94,.1);color:var(--green);border:1px solid rgba(34,197,94,.2)">1</div>
        <div class="layer-vert" style="opacity:0"></div>
      </div>
      <div class="layer-body">
        <div class="layer-title">Password Authentication</div>
        <div class="layer-desc">bcrypt hashing at cost factor 12. Enforces uppercase, lowercase, digit, and special character requirements. Protects against rainbow table and brute-force attacks as the first gate.</div>
        <span class="layer-tech" style="background:rgba(34,197,94,.08);color:var(--green);border-color:rgba(34,197,94,.2)">bcrypt · Cost Factor 12</span>
      </div>
    </div>
  </div>
</section>

<div class="divider"></div>

<!-- ARCHITECTURE -->
<section id="architecture">
  <div class="section-tag">System Design</div>
  <div class="section-h">Architecture</div>
  <p class="section-p">Three-tier system: browser UI talks to Flask backend which orchestrates AI/ML modules and persists to MongoDB.</p>

  <div class="arch-diagram" id="archDiagram">
    <div class="arch-layer">
      <div class="arch-label" style="color:#7c3aed">Frontend</div>
      <div class="arch-content">
        <span class="arch-chip" style="color:#a78bfa;border-color:rgba(124,58,237,.3);background:rgba(124,58,237,.08)">HTML5 / CSS3</span>
        <span class="arch-chip" style="color:#a78bfa;border-color:rgba(124,58,237,.3);background:rgba(124,58,237,.08)">TailwindCSS</span>
        <span class="arch-chip" style="color:#a78bfa;border-color:rgba(124,58,237,.3);background:rgba(124,58,237,.08)">Chart.js</span>
        <span class="arch-chip" style="color:#a78bfa;border-color:rgba(124,58,237,.3);background:rgba(124,58,237,.08)">Webcam API</span>
        <span class="arch-chip" style="color:#a78bfa;border-color:rgba(124,58,237,.3);background:rgba(124,58,237,.08)">behavior.js</span>
      </div>
    </div>
    <div class="arch-layer">
      <div class="arch-label" style="color:var(--blue2)">Flask Backend</div>
      <div class="arch-content">
        <span class="arch-chip" style="color:var(--blue2);border-color:rgba(37,99,255,.3);background:rgba(37,99,255,.08)">/register</span>
        <span class="arch-chip" style="color:var(--blue2);border-color:rgba(37,99,255,.3);background:rgba(37,99,255,.08)">/login</span>
        <span class="arch-chip" style="color:var(--blue2);border-color:rgba(37,99,255,.3);background:rgba(37,99,255,.08)">/cast-vote</span>
        <span class="arch-chip" style="color:var(--blue2);border-color:rgba(37,99,255,.3);background:rgba(37,99,255,.08)">/dashboard</span>
        <span class="arch-chip" style="color:var(--blue2);border-color:rgba(37,99,255,.3);background:rgba(37,99,255,.08)">/results</span>
      </div>
    </div>
    <div class="arch-layer">
      <div class="arch-label" style="color:var(--cyan)">AI / ML</div>
      <div class="arch-content">
        <span class="arch-chip" style="color:var(--cyan);border-color:rgba(6,214,214,.3);background:rgba(6,214,214,.08)">face_auth.py</span>
        <span class="arch-chip" style="color:var(--cyan);border-color:rgba(6,214,214,.3);background:rgba(6,214,214,.08)">behavior_model.py</span>
        <span class="arch-chip" style="color:var(--cyan);border-color:rgba(6,214,214,.3);background:rgba(6,214,214,.08)">IsolationForest</span>
        <span class="arch-chip" style="color:var(--cyan);border-color:rgba(6,214,214,.3);background:rgba(6,214,214,.08)">dlib 128-D</span>
      </div>
    </div>
    <div class="arch-layer">
      <div class="arch-label" style="color:#ef4444">Security</div>
      <div class="arch-content">
        <span class="arch-chip" style="color:#ef4444;border-color:rgba(239,68,68,.3);background:rgba(239,68,68,.08)">Blockchain audit</span>
        <span class="arch-chip" style="color:#ef4444;border-color:rgba(239,68,68,.3);background:rgba(239,68,68,.08)">SHA-256</span>
        <span class="arch-chip" style="color:#ef4444;border-color:rgba(239,68,68,.3);background:rgba(239,68,68,.08)">bcrypt</span>
        <span class="arch-chip" style="color:#ef4444;border-color:rgba(239,68,68,.3);background:rgba(239,68,68,.08)">CORS</span>
      </div>
    </div>
    <div class="arch-layer" style="border-bottom:none">
      <div class="arch-label" style="color:var(--green)">MongoDB</div>
      <div class="arch-content">
        <span class="arch-chip" style="color:var(--green);border-color:rgba(34,197,94,.3);background:rgba(34,197,94,.08)">users</span>
        <span class="arch-chip" style="color:var(--green);border-color:rgba(34,197,94,.3);background:rgba(34,197,94,.08)">votes</span>
        <span class="arch-chip" style="color:var(--green);border-color:rgba(34,197,94,.3);background:rgba(34,197,94,.08)">audit_chain</span>
        <span class="arch-chip" style="color:var(--green);border-color:rgba(34,197,94,.3);background:rgba(34,197,94,.08)">sessions</span>
      </div>
    </div>
  </div>
</section>

<div class="divider"></div>

<!-- USER FLOW -->
<section id="flow">
  <div class="section-tag">User Journey</div>
  <div class="section-h">Registration to<br>Confirmed Vote</div>
  <p class="section-p">Every voter passes through the same pipeline. No step can be skipped. No shortcut bypasses the chain.</p>

  <div class="flow" id="flowList">
    <div class="flow-step" data-delay="0"><div class="flow-circle">1</div><div class="flow-content"><div class="flow-title">Register with face capture</div><div class="flow-desc">Fill form → webcam captures face → dlib extracts 128-D encoding → stored in MongoDB with bcrypt password</div></div></div>
    <div class="flow-step" data-delay="80"><div class="flow-circle">2</div><div class="flow-content"><div class="flow-title">Login: password check</div><div class="flow-desc">bcrypt comparison. Wrong password → immediate block. Correct → proceed to Layer 2</div></div></div>
    <div class="flow-step" data-delay="160"><div class="flow-circle">3</div><div class="flow-content"><div class="flow-title">Real-time face verification</div><div class="flow-desc">Webcam frame compared against stored encoding. Distance > 0.6 → access denied. Confidence score returned</div></div></div>
    <div class="flow-step" data-delay="240"><div class="flow-circle">4</div><div class="flow-content"><div class="flow-title">Behavioral AI scoring</div><div class="flow-desc">Isolation Forest evaluates keystroke timing, mouse patterns, login velocity. Risk score computed. Score > 0.3 → blocked</div></div></div>
    <div class="flow-step" data-delay="320"><div class="flow-circle">5</div><div class="flow-content"><div class="flow-title">Vote casting</div><div class="flow-desc">Candidate selection → double-vote check → vote stored → SHA-256 hash generated → blockchain block appended</div></div></div>
    <div class="flow-step" data-delay="400"><div class="flow-circle">6</div><div class="flow-content"><div class="flow-title">Confirmation + live results</div><div class="flow-desc">Vote confirmation with block hash shown. Results dashboard updates in real-time. Blockchain integrity verified</div></div></div>
  </div>
</section>

<div class="divider"></div>

<!-- TECH STACK -->
<section id="stack">
  <div class="section-tag">Tech Stack</div>
  <div class="section-h">Built With</div>
  <div class="tech-grid" id="techGrid">
    <div class="tech-cell" data-delay="0">
      <div class="tech-cat">Backend</div>
      <div class="tech-item"><div class="tech-dot"></div>Python 3.11+</div>
      <div class="tech-item"><div class="tech-dot"></div>Flask 2.3.0</div>
      <div class="tech-item"><div class="tech-dot"></div>PyMongo 4.5.0</div>
      <div class="tech-item"><div class="tech-dot"></div>bcrypt 4.0.1</div>
    </div>
    <div class="tech-cell" data-delay="80">
      <div class="tech-cat" style="color:#06d6d6">AI / ML</div>
      <div class="tech-item"><div class="tech-dot" style="background:var(--cyan)"></div>dlib 19.24.0</div>
      <div class="tech-item"><div class="tech-dot" style="background:var(--cyan)"></div>face_recognition 1.3.0</div>
      <div class="tech-item"><div class="tech-dot" style="background:var(--cyan)"></div>scikit-learn 1.3.0</div>
      <div class="tech-item"><div class="tech-dot" style="background:var(--cyan)"></div>NumPy 1.24.0</div>
    </div>
    <div class="tech-cell" data-delay="160">
      <div class="tech-cat" style="color:#a78bfa">Frontend</div>
      <div class="tech-item"><div class="tech-dot" style="background:#a78bfa"></div>HTML5 / CSS3 / JS</div>
      <div class="tech-item"><div class="tech-dot" style="background:#a78bfa"></div>TailwindCSS 3.3.0</div>
      <div class="tech-item"><div class="tech-dot" style="background:#a78bfa"></div>Chart.js 4.4.0</div>
      <div class="tech-item"><div class="tech-dot" style="background:#a78bfa"></div>Webcam API</div>
    </div>
    <div class="tech-cell" data-delay="240">
      <div class="tech-cat" style="color:#ef4444">Security</div>
      <div class="tech-item"><div class="tech-dot" style="background:#ef4444"></div>SHA-256 hashing</div>
      <div class="tech-item"><div class="tech-dot" style="background:#ef4444"></div>Blockchain audit</div>
      <div class="tech-item"><div class="tech-dot" style="background:#ef4444"></div>Flask Sessions</div>
      <div class="tech-item"><div class="tech-dot" style="background:#ef4444"></div>CORS protection</div>
    </div>
    <div class="tech-cell" data-delay="320">
      <div class="tech-cat" style="color:var(--green)">Database</div>
      <div class="tech-item"><div class="tech-dot" style="background:var(--green)"></div>MongoDB 6.0</div>
      <div class="tech-item"><div class="tech-dot" style="background:var(--green)"></div>MongoDB Atlas</div>
      <div class="tech-item"><div class="tech-dot" style="background:var(--green)"></div>Compass GUI</div>
      <div class="tech-item"><div class="tech-dot" style="background:var(--green)"></div>GridFS (encodings)</div>
    </div>
    <div class="tech-cell" data-delay="400">
      <div class="tech-cat" style="color:#f59e0b">DevOps</div>
      <div class="tech-item"><div class="tech-dot" style="background:#f59e0b"></div>Docker + Compose</div>
      <div class="tech-item"><div class="tech-dot" style="background:#f59e0b"></div>Railway deploy</div>
      <div class="tech-item"><div class="tech-dot" style="background:#f59e0b"></div>Git / GitHub</div>
      <div class="tech-item"><div class="tech-dot" style="background:#f59e0b"></div>Postman testing</div>
    </div>
  </div>
</section>

<div class="divider"></div>

<!-- TEAM -->
<section id="team">
  <div class="section-tag">Team</div>
  <div class="section-h">SentinelVote<br>AI Team</div>
  <div class="team-grid" id="teamGrid">
    <div class="team-card" data-delay="0">
      <div class="team-avatar" style="background:rgba(37,99,255,.15);color:var(--blue2)">RV</div>
      <div class="team-name">Ruchika Verma</div>
      <div class="team-role">Full Stack · AI/ML</div>
      <a href="https://www.linkedin.com/in/ruchika-verma-888bb6309" target="_blank" class="team-link">LinkedIn ↗</a>
    </div>
    <div class="team-card" data-delay="100">
      <div class="team-avatar" style="background:rgba(6,214,214,.15);color:var(--cyan)">DS</div>
      <div class="team-name">Divyanshi Singh</div>
      <div class="team-role">Backend Engineer</div>
      <a href="https://linkedin.com/in/member2" target="_blank" class="team-link">LinkedIn ↗</a>
    </div>
    <div class="team-card" data-delay="200">
      <div class="team-avatar" style="background:rgba(124,58,237,.15);color:#a78bfa">AA</div>
      <div class="team-name">Archana Agahari</div>
      <div class="team-role">Frontend · UI/UX</div>
      <a href="https://linkedin.com/in/member3" target="_blank" class="team-link">LinkedIn ↗</a>
    </div>
    <div class="team-card" data-delay="300">
      <div class="team-avatar" style="background:rgba(239,68,68,.15);color:#ef4444">R</div>
      <div class="team-name">Rashmi</div>
      <div class="team-role">Security Engineer</div>
      <a href="https://linkedin.com/in/member4" target="_blank" class="team-link">LinkedIn ↗</a>
    </div>
  </div>
</section>

<!-- FOOTER -->
<footer>
  <div class="footer-logo">SentinelVote AI</div>
  <div class="footer-quote">"Security is not optional in democracy. It's fundamental."</div>
  <div class="footer-badges">
    <span class="badge">MIT License</span>
    <span class="badge">Python 3.11+</span>
    <span class="badge">Flask 2.3</span>
    <span class="badge">MongoDB 6.0</span>
  </div>
</footer>

<script>
// Cursor
const cd = document.getElementById('cd'), cr = document.getElementById('cr');
let rx=0,ry=0,mx=0,my=0;
document.addEventListener('mousemove',e=>{mx=e.clientX;my=e.clientY});
(function cur(){
  rx+=(mx-rx)*.13;ry+=(my-ry)*.13;
  cd.style.cssText=`left:${mx}px;top:${my}px`;
  cr.style.cssText=`left:${rx}px;top:${ry}px`;
  requestAnimationFrame(cur);
})();

// Counter animation
function animateCount(el, target, duration=1200) {
  let start=0, startTime=null;
  const step = ts => {
    if(!startTime) startTime=ts;
    const prog = Math.min((ts-startTime)/duration,1);
    const ease = 1-Math.pow(1-prog,3);
    el.textContent = Math.round(ease*target);
    if(prog<1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

// Intersection observer for scroll reveals
const obs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if(e.isIntersecting) {
      const el = e.target;
      const delay = parseInt(el.dataset.delay || 0);
      setTimeout(() => el.classList.add('visible'), delay);
      obs.unobserve(el);
    }
  });
}, {threshold: 0.1});

// Observe all animated elements
document.querySelectorAll('.layer,.tech-cell,.team-card,.flow-step,.arch-diagram').forEach(el => obs.observe(el));

// Stats counters
const statsObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if(e.isIntersecting) {
      document.querySelectorAll('[data-target]').forEach(el => {
        animateCount(el, parseInt(el.dataset.target));
      });
      statsObs.disconnect();
    }
  });
}, {threshold: 0.5});
const statsEl = document.querySelector('.hero-stats');
if(statsEl) statsObs.observe(statsEl);

// Animate stats on load too (they're above the fold)
setTimeout(() => {
  document.querySelectorAll('[data-target]').forEach(el => {
    animateCount(el, parseInt(el.dataset.target));
  });
}, 600);
</script>
</body>
</html>
