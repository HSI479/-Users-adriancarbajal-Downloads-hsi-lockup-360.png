// 4:19 Podcast medallion — a vector RECREATION of the brand logo for rendering when the
// original PNGs ("419 Podcast Logo.png" / "419 Poscast Logo Shiney.png" in iCloud) are not
// on this machine. Pass --logo <path-to-png> to render.mjs to use the real artwork instead.
window.LOGO_SVG = `
<svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="4:19 Podcast">
  <defs>
    <radialGradient id="face" cx="50%" cy="38%" r="70%">
      <stop offset="0" stop-color="#2C2A24"/>
      <stop offset="1" stop-color="#15140F"/>
    </radialGradient>
    <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#EAD39A"/>
      <stop offset=".45" stop-color="#D8B45A"/>
      <stop offset="1" stop-color="#8A6817"/>
    </linearGradient>
    <clipPath id="inner"><circle cx="500" cy="500" r="392"/></clipPath>
  </defs>
  <!-- medallion rings -->
  <circle cx="500" cy="500" r="472" fill="none" stroke="url(#gold)" stroke-width="22"/>
  <circle cx="500" cy="500" r="436" fill="url(#face)" stroke="url(#gold)" stroke-width="6"/>
  <circle cx="500" cy="500" r="408" fill="none" stroke="#D8B45A" stroke-width="2" opacity=".55"/>
  <!-- cast net (Matthew 4:19: "I will make you fishers of men") -->
  <g clip-path="url(#inner)" fill="none" stroke="#D8B45A" stroke-width="2.2" opacity=".42">
    <path d="M60 560 Q500 740 940 560"/><path d="M60 620 Q500 800 940 620"/><path d="M60 680 Q500 860 940 680"/>
    <path d="M60 740 Q500 920 940 740"/><path d="M60 800 Q500 980 940 800"/>
    <path d="M110 500 Q180 760 340 940"/><path d="M230 500 Q290 760 430 980"/><path d="M360 520 Q400 780 470 1000"/>
    <path d="M890 500 Q820 760 660 940"/><path d="M770 500 Q710 760 570 980"/><path d="M640 520 Q600 780 530 1000"/>
  </g>
  <!-- microphone -->
  <g transform="translate(500 290)">
    <rect x="-58" y="-150" width="116" height="200" rx="58" fill="#1C1B18" stroke="url(#gold)" stroke-width="10"/>
    <g stroke="#D8B45A" stroke-width="4" opacity=".9">
      <line x1="-40" y1="-110" x2="40" y2="-110"/><line x1="-50" y1="-80" x2="50" y2="-80"/>
      <line x1="-54" y1="-50" x2="54" y2="-50"/><line x1="-54" y1="-20" x2="54" y2="-20"/><line x1="-46" y1="10" x2="46" y2="10"/>
    </g>
    <path d="M-100 -20 v40 a100 100 0 0 0 200 0 v-40" fill="none" stroke="url(#gold)" stroke-width="10" stroke-linecap="round"/>
    <line x1="0" y1="120" x2="0" y2="160" stroke="url(#gold)" stroke-width="10" stroke-linecap="round"/>
  </g>
  <!-- 4:19 -->
  <text x="500" y="640" text-anchor="middle" font-family="Rokkitt, Georgia, serif" font-weight="800" font-size="248" fill="url(#gold)" letter-spacing="-4">4:19</text>
  <!-- PODCAST -->
  <text x="500" y="722" text-anchor="middle" font-family="Archivo, Arial, sans-serif" font-weight="700" font-size="58" fill="#EAD39A" letter-spacing="22">PODCAST</text>
  <!-- Sharpening shield -->
  <g transform="translate(500 820)">
    <path d="M-42 -40 h84 v44 q0 40 -42 58 q-42 -18 -42 -58 z" fill="#1C1B18" stroke="url(#gold)" stroke-width="6"/>
    <path d="M-20 26 L22 -22" stroke="#D8B45A" stroke-width="7" stroke-linecap="round"/>
    <path d="M-20 26 L-6 22 L-16 12 z" fill="#D8B45A"/>
  </g>
</svg>`;

// Renders the logo into an element: uses window.LOGO_SRC (real PNG) when set, else the SVG above.
window.mountLogo = function (el) {
  if (window.LOGO_SRC) { el.innerHTML = '<img src="' + window.LOGO_SRC + '" alt="4:19 Podcast" style="width:100%;height:100%;object-fit:contain;display:block">'; }
  else { el.innerHTML = window.LOGO_SVG; }
};
