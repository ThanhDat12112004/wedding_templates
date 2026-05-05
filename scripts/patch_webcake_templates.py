#!/usr/bin/env python3
"""Batch-patch template_1..10.html: viewport, branding cleanup, names, theme tint."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Ordered: longer phrases first
TEXT_REPLACEMENTS: list[tuple[str, str]] = [
    ("Phạm Mai Hương", "Lê Nguyên Thảo"),
    ("Trần Minh Hoàng", "Dương Thành Đạt"),
    ("Minh Hoàng &amp; Lê Nguyên Thảo ", "Dương Thành Đạt &amp; Lê Nguyên Thảo "),
    ("Minh Hoàng & Lê Nguyên Thảo ", "Dương Thành Đạt & Lê Nguyên Thảo "),
    ("Nguyễn Anh Tú", "Dương Thành Đạt"),
    ("Trần Thị Diệu Nhi", "Lê Nguyên Thảo"),
    ("Anh Tú - Diệu Nhi", "Dương Thành Đạt - Lê Nguyên Thảo"),
    ("Dương Thành Đạt & Mai Hương", "Dương Thành Đạt & Lê Nguyên Thảo"),
    ("Thành Đạt & Mai Hương", "Dương Thành Đạt & Lê Nguyên Thảo"),
    ("Mai Hương", "Lê Nguyên Thảo"),
    ("Minh An", "Lê Nguyên Thảo"),
    ("Phương Thúy", "Lê Nguyên Thảo"),
    ("Trịnh Phương Thúy", "Lê Nguyên Thảo"),
    ("Thanh Thuý", "Lê Nguyên Thảo"),
    ("Anh Tuấn", "Dương Thành Đạt"),
    ("Anh Long", "Dương Thành Đạt"),
    ("Anh Tú", "Dương Thành Đạt"),
    ("Diệu Nhi", "Lê Nguyên Thảo"),
    ("Minh Hoàng ", "Dương Thành Đạt "),
    # Chú rể / cô dâu: TRẦN–MỸ DUYÊN = nhà trai; PHẠM–NGỌC HẠNH = nhà gái
    ("ÔNG TRẦN QUỐC TUẤN\nBÀ LÊ THỊ MỸ DUYÊN ", "ÔNG BÀ NHÀ TRAI\n"),
    ("ÔNG PHẠM GIA LONG\nBÀ NGUYỄN THỊ NGỌC HẠNH ", "ÔNG BÀ NHÀ GÁI\n"),
    # MAPPING / script dùng chuỗi JS "\\n" (backslash + n)
    ("ÔNG TRẦN QUỐC TUẤN\\nBÀ LÊ THỊ MỸ DUYÊN ", "ÔNG BÀ NHÀ TRAI\\n"),
    ("ÔNG PHẠM GIA LONG\\nBÀ NGUYỄN THỊ NGỌC HẠNH ", "ÔNG BÀ NHÀ GÁI\\n"),
    ("ÔNG PHẠM GIA LONG\nBÀ NGUYỄN THỊ NGỌC HẠNH <br>", "ÔNG BÀ NHÀ GÁI <br>"),
    # Ghi chú trong <!-- --> (designer notes)
    ("ÔNG TRẦN QUỐC TUẤN\nBÀ LÊ THỊ MỸ DUYÊN\n", "ÔNG BÀ NHÀ TRAI\n"),
    ("ÔNG PHẠM GIA LONG\nBÀ NGUYỄN THỊ NGỌC HẠNH\n", "ÔNG BÀ NHÀ GÁI\n"),
    ("THAM DỰ LỄ CƯỚI MINH HOÀNG & MAI HƯƠNG ", "THAM DỰ LỄ CƯỚI DƯƠNG THÀNH ĐẠT & LÊ NGUYÊN THẢO "),
    # Sửa nhãn nhà trai/gái bị đảo trong MAPPING (chuỗi \\n như file JS export)
    ('{ id: "w-ig5jcswu", text: "ÔNG BÀ NHÀ GÁI\\n"},', '{ id: "w-ig5jcswu", text: "ÔNG BÀ NHÀ TRAI\\n"},'),
    ('{ id: "w-bv74resi", text: "ÔNG BÀ NHÀ TRAI\\n"},', '{ id: "w-bv74resi", text: "ÔNG BÀ NHÀ GÁI\\n"},'),
    ('{ id: "w-2g81k7ss", text: "ÔNG BÀ NHÀ GÁI\\n"},', '{ id: "w-2g81k7ss", text: "ÔNG BÀ NHÀ TRAI\\n"},'),
    ('{ id: "w-1e424hst", text: "ÔNG BÀ NHÀ TRAI\\n"},', '{ id: "w-1e424hst", text: "ÔNG BÀ NHÀ GÁI\\n"},'),
    ('{ id: "w-38exi7p9", text: "ÔNG BÀ NHÀ GÁI\\n"},', '{ id: "w-38exi7p9", text: "ÔNG BÀ NHÀ TRAI\\n"},'),
    ('{ id: "w-6kdhwvkd", text: "ÔNG BÀ NHÀ TRAI\\n"},', '{ id: "w-6kdhwvkd", text: "ÔNG BÀ NHÀ GÁI\\n"},'),
    ('{ id: "w-vq47tj4t", text: "ÔNG BÀ NHÀ GÁI\\n"},', '{ id: "w-vq47tj4t", text: "ÔNG BÀ NHÀ TRAI\\n"},'),
    ('{ id: "w-fynwgspj", text: "ÔNG BÀ NHÀ TRAI\\n"},', '{ id: "w-fynwgspj", text: "ÔNG BÀ NHÀ GÁI\\n"},'),
    ('{ id: "w-xjdsrgp5", text: "ÔNG BÀ NHÀ GÁI\\n"},', '{ id: "w-xjdsrgp5", text: "ÔNG BÀ NHÀ TRAI\\n"},'),
    ('{ id: "w-k4vnjy9f", text: "ÔNG BÀ NHÀ TRAI\\n"},', '{ id: "w-k4vnjy9f", text: "ÔNG BÀ NHÀ GÁI\\n"},'),
    # Cùng mapping nhưng file gốc dùng newline thật trong chuỗi JS
    ('{ id: "w-ig5jcswu", text: "ÔNG BÀ NHÀ GÁI\n"},', '{ id: "w-ig5jcswu", text: "ÔNG BÀ NHÀ TRAI\n"},'),
    ('{ id: "w-bv74resi", text: "ÔNG BÀ NHÀ TRAI\n"},', '{ id: "w-bv74resi", text: "ÔNG BÀ NHÀ GÁI\n"},'),
    ('{ id: "w-2g81k7ss", text: "ÔNG BÀ NHÀ GÁI\n"},', '{ id: "w-2g81k7ss", text: "ÔNG BÀ NHÀ TRAI\n"},'),
    ('{ id: "w-1e424hst", text: "ÔNG BÀ NHÀ TRAI\n"},', '{ id: "w-1e424hst", text: "ÔNG BÀ NHÀ GÁI\n"},'),
    ('{ id: "w-38exi7p9", text: "ÔNG BÀ NHÀ GÁI\n"},', '{ id: "w-38exi7p9", text: "ÔNG BÀ NHÀ TRAI\n"},'),
    ('{ id: "w-6kdhwvkd", text: "ÔNG BÀ NHÀ TRAI\n"},', '{ id: "w-6kdhwvkd", text: "ÔNG BÀ NHÀ GÁI\n"},'),
    ('{ id: "w-vq47tj4t", text: "ÔNG BÀ NHÀ GÁI\n"},', '{ id: "w-vq47tj4t", text: "ÔNG BÀ NHÀ TRAI\n"},'),
    ('{ id: "w-fynwgspj", text: "ÔNG BÀ NHÀ TRAI\n"},', '{ id: "w-fynwgspj", text: "ÔNG BÀ NHÀ GÁI\n"},'),
    ('{ id: "w-xjdsrgp5", text: "ÔNG BÀ NHÀ GÁI\n"},', '{ id: "w-xjdsrgp5", text: "ÔNG BÀ NHÀ TRAI\n"},'),
    ('{ id: "w-k4vnjy9f", text: "ÔNG BÀ NHÀ TRAI\n"},', '{ id: "w-k4vnjy9f", text: "ÔNG BÀ NHÀ GÁI\n"},'),
    ("BÀ LÊ THỊ MỸ DUYÊN <br><br>", ""),
    ("BÀ LÊ THỊ MỸ DUYÊN <br>", ""),
    ("BÀ NGUYỄN THỊ NGỌC HẠNH <br>", ""),
    ("BÀ NGUYỄN THỊ HẢI <br>", ""),
    ("ÔNG CẤN VĂN AN BÀ NGUYỄN THỊ HẢI", "ÔNG BÀ NHÀ TRAI"),
    ("| THIỆP CƯỚI ONLINE LONG THỊNH", ""),
    ("THIỆP CƯỚI ONLINE LONG THỊNH", ""),
    # STK mẫu nhà cung cấp
    ("MBBANK - NGUYEN TAN DAT<br>8838683860<br>", ""),
    ("MBBANK<br>NGUYEN TAN DAT\n<br>8838683860<br>", ""),
    ("MBBANK<br>NGUYEN TAN DAT<br>8838683860<br>", ""),
    ("<br>8838683860<br>", ""),
]

VIEWPORT_RE = re.compile(
    r'<meta name="viewport" content="width=device-width, initial-scale=1">\s*'
    r'<script async="" src="\./template_\d+_files/app\.js"></script><script type="text/javascript">\s*'
    r'!function\(e,t,i\)\{.*?\}\(window,document,"DISPLAY"\);\s*'
    r'</script><meta name="viewport" content="width=420,[^"]+">',
    re.DOTALL,
)


def viewport_block(n: int) -> str:
    app_js = f"./template_{n}_files/app.js"
    vp = """        <script type="text/javascript">
(function(){
  var CW=420,DW=960,BP=768;
  var lastContent=null,lastBucket=null,appliedMobile=false;
  /** Không dùng clientWidth sau meta width=420 (nó ~420 → scale=1 → thiệp lệch/tràn). Lấy độ rộng cửa sổ thật. */
  function readW(){
    var ow=window.outerWidth|0;
    if(ow>=300&&ow<=1100)return ow;
    var iw=window.innerWidth|0;
    if(iw>=300&&iw<=1100)return iw;
    var sw=(window.screen&&window.screen.width)|0;
    if(sw>=300&&sw<=1100)return sw;
    return iw||document.documentElement.clientWidth||CW;
  }
  function applyViewport(){
    var w=readW(),mobile=w<BP,bucket=mobile?"m":"d";
    window.DISPLAY=mobile?"mobile":"desktop";
    if(bucket==="m"&&appliedMobile&&bucket===lastBucket)return;
    var c;
    if(mobile){
      var s=Math.max(0.28,Math.min(2.85,Math.round((w/CW)*100)/100));
      c="width="+CW+", initial-scale="+s+", minimum-scale="+s+", maximum-scale="+s+", user-scalable=no, viewport-fit=cover";
    }else{
      c="width="+DW+", initial-scale=1, minimum-scale=1, maximum-scale=1, user-scalable=no";
    }
    if(c===lastContent){lastBucket=bucket;appliedMobile=(bucket==="m");return;}
    lastContent=c;
    var nodes=document.head.querySelectorAll("meta[name=viewport]");
    for(var i=0;i<nodes.length;i++)nodes[i].remove();
    var m=document.createElement("meta");
    m.name="viewport";
    m.setAttribute("content",c);
    document.head.insertBefore(m,document.head.firstChild);
    lastBucket=bucket;
    appliedMobile=(bucket==="m");
    try{window.scrollTo(0,0);document.documentElement.scrollLeft=0;document.body.scrollLeft=0;}catch(e){}
  }
  function onResize(){
    clearTimeout(window.__wedVp);
    window.__wedVp=setTimeout(function(){
      var b=(readW()<BP)?"m":"d";
      if(b!==lastBucket){lastContent=null;appliedMobile=false;applyViewport();}
    },400);
  }
  applyViewport();
  window.addEventListener("resize",onResize,{passive:true});
  window.addEventListener("orientationchange",function(){
    appliedMobile=false;
    lastContent=null;
    setTimeout(function(){
      applyViewport();
      try{window.scrollTo(0,0);document.documentElement.scrollLeft=0;document.body.scrollLeft=0;}catch(e){}
    },360);
  });
})();
    </script>
"""
    return vp + f'    <script async="" src="{app_js}"></script>'


STYLE_MARKER = 'id="wedding-client-v2"'
EXTRA_MARKER = 'id="wedding-extra-hide"'

STYLE_CSS = """<style id="wedding-client-v2">
/* Ẩn liên hệ / MXH / branding nhà cung cấp */
a[href*="ewedinvite.site/info"],
a[href*="www.ewedinvite.site/info"],
a[title*="ewedinvite.site/info"] {
  display: none !important;
  visibility: hidden !important;
  pointer-events: none !important;
  width: 0 !important;
  height: 0 !important;
  overflow: hidden !important;
}
.login-popup-wrapper,
#login-popup { display: none !important; }

html { overflow-x: hidden; }
body { overflow-x: hidden; }

/* Tông mới (khác bản gốc): nền + filter nhẹ theo từng file */
body {
  background: linear-gradient(165deg, var(--wed-bg-a,#f3f6fb) 0%, var(--wed-bg-b,#fdf8f5) 48%, var(--wed-bg-c,#eef5f2) 100%) !important;
}
.pageview {
  filter: hue-rotate(var(--wed-hue, 12deg)) saturate(1.07) contrast(1.03);
}

/* Viewport khóa zoom; tránh Safari đổi cỡ chữ tự ý */
html,body{
  -webkit-text-size-adjust:100%;
  text-size-adjust:100%;
}
/* Căn thiệp giữa màn hình khi meta co theo CW=420 */
@media screen and (max-width:767px){
  body{
    display:flex;
    flex-direction:column;
    align-items:center;
  }
  .pageview{
    margin-left:auto !important;
    margin-right:auto !important;
    position:relative;
  }
}
</style>
"""

EXTRA_CSS = """<style id="wedding-extra-hide">
/* Tracking pixel nhà cung cấp */
img[src*="page_view.gif"] {
  display: none !important;
  visibility: hidden !important;
  width: 0 !important;
  height: 0 !important;
  opacity: 0 !important;
  pointer-events: none !important;
}
</style>
"""


STRIP_SCRIPT_RE = re.compile(r"<script\s+id=[\"']wedding-strip-branding[\"'][^>]*>.*?</script>", re.DOTALL)

SCRIPT_CLEANUP = """<script id="wedding-strip-branding">
(function(){
  function hideEwLinks(){
    document.querySelectorAll('a[href*="ewedinvite.site/info"]').forEach(function(a){
      var p=a.closest('.com-rectangle')||a.closest('.com-button')||a.parentElement;
      if(p){ p.style.setProperty('display','none','important'); }
      a.style.setProperty('display','none','important');
    });
  }
  function stripLongThinh(){
    document.querySelectorAll('h1,h2,h3,h4,p,div.text-block').forEach(function(el){
      var t=(el.textContent||'').trim();
      if(/LONG\\s*THỊNH|THIỆP\\s+CƯỚI\\s+ONLINE\\s+LONG/i.test(t)){
        var sec=el.closest('.com-section');
        if(sec){ sec.style.setProperty('display','none','important'); }
        else { el.style.setProperty('display','none','important'); }
      }
    });
  }
  function hideTrackingImgs(){
    document.querySelectorAll('img[src*="page_view.gif"]').forEach(function(img){
      img.style.setProperty('display','none','important');
    });
  }
  /** Ẩn logo/icon MXH nhỏ (background pancake CDN đặc trưng) */
  function hideSupplierLogoTiles(){
    document.querySelectorAll('.rectangle-css,.image-background').forEach(function(el){
      var st=(el.getAttribute('style')||'')+(el.style&&el.style.cssText||'');
      if(/36\\/b3\\/ec\\/ae|be\\/ad\\/61\\/25\\/69ccff|08\\/3f\\/7a\\/e9\\/be9a053a|980-h:980-l:7525/i.test(st)){
        var node=el.closest('.com-rectangle,.com-image-block,.p-absolute')||el;
        node.style.setProperty('display','none','important');
      }
    });
  }
  /** Ẩn khối STK / MBBANK còn sót trong DOM */
  function hideBankLines(){
    document.querySelectorAll('h1,h2,h3,h4,p').forEach(function(el){
      var t=(el.textContent||'');
      if(/MBBANK|NGUYEN TAN DAT|8838683860/i.test(t)){
        var block=el.closest('.com-text-block')||el;
        block.style.setProperty('display','none','important');
      }
    });
  }
  function run(){
    hideEwLinks();
    stripLongThinh();
    hideTrackingImgs();
    hideSupplierLogoTiles();
    hideBankLines();
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',run);
  else run();
  try{
    var mo=new MutationObserver(function(){ run(); });
    mo.observe(document.documentElement,{subtree:true,childList:true});
  }catch(e){}
})();
</script>
"""


def theme_vars(n: int) -> str:
    hue = (n * 11) % 72 - 20
    a, b, c = [
        ("#f0f4ff", "#fff9f5", "#e8f5f1"),
        ("#fdf5ff", "#fffbf7", "#eaf4fb"),
        ("#f5fff8", "#fefcf8", "#eef2ff"),
        ("#fff5f5", "#f8fff9", "#f0edff"),
        ("#f5f8ff", "#fffaf3", "#ecf8f3"),
        ("#fdf8ff", "#f7fffb", "#eef6ff"),
        ("#fff8f4", "#f4fff9", "#ebefff"),
        ("#f4fff7", "#fff9fb", "#eef4fa"),
        ("#faf5ff", "#fafff8", "#eaf7f4"),
        ("#fff6f3", "#f6fbff", "#edf8ee"),
    ][(n - 1) % 10]
    return f'<style id="wedding-theme-vars">:root{{--wed-hue:{hue}deg;--wed-bg-a:{a};--wed-bg-b:{b};--wed-bg-c:{c};}}</style>'


def patch_file(path: Path, n: int) -> None:
    text = path.read_text(encoding="utf-8")
    orig = text

    # Viewport
    if VIEWPORT_RE.search(text):
        text = VIEWPORT_RE.sub(viewport_block(n), text, count=1)

    # Names
    for old, new in TEXT_REPLACEMENTS:
        text = text.replace(old, new)

    # Extra CSS (tracking img) once — sau khối wedding-client-v2
    if EXTRA_MARKER not in text and STYLE_MARKER in text:
        v = text.find('id="wedding-client-v2"')
        if v != -1:
            cend = text.find("</style>", v)
            if cend != -1:
                cend += len("</style>")
                text = text[:cend] + "\n" + EXTRA_CSS + text[cend:]

    # Luôn thay script strip bằng bản mới nhất (callable để tránh re.escape trong JS regex \\s)
    _strip_js = SCRIPT_CLEANUP.strip()
    if STRIP_SCRIPT_RE.search(text):
        text = STRIP_SCRIPT_RE.sub(lambda _m: _strip_js, text, count=1)

    # Theme vars + overlay styles once
    if STYLE_MARKER not in text:
        inject = theme_vars(n) + "\n" + STYLE_CSS
        # After charset line inside head
        m = re.search(r"(<head><meta http-equiv=\"Content-Type\"[^>]+>)", text)
        if m:
            text = text.replace(m.group(1), m.group(1) + "\n" + inject, 1)
        else:
            text = inject + text

    # Cleanup script before </html> (nếu chưa có)
    if not STRIP_SCRIPT_RE.search(text) and 'id="wedding-strip-branding"' not in text:
        text = text.replace("</html>", SCRIPT_CLEANUP + "\n</html>", 1)

    if text != orig:
        path.write_text(text, encoding="utf-8")
        print(f"updated {path.name}")
    else:
        print(f"skip {path.name} (no changes)")


def main() -> None:
    for i in range(1, 11):
        p = ROOT / f"template_{i}.html"
        if not p.exists():
            print(f"missing {p}")
            continue
        patch_file(p, i)


if __name__ == "__main__":
    main()
