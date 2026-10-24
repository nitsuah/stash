"""Builds the free tools site (static, client-side only, no trackers). Stdlib only. python build_site.py -> dist/"""
import html, json, os, pathlib, shutil, zipfile

ROOT = pathlib.Path(__file__).parent
BASE = os.environ.get("TOOLS_BASE", "")  # e.g. /tools when served from nitsuah.io
HOST = os.environ.get("TOOLS_HOST", "")
DIST = ROOT / ("dist-nitsuah" if BASE else "dist")


def href_index():
    return BASE if BASE else "index.html"


def href_page(slug):
    return f"{BASE}/{slug}" if BASE else f"{slug}.html"


def href_css():
    return f"{BASE}/style.css" if BASE else "style.css"


def canonical(slug):
    return f'<link rel="canonical" href="{(HOST + BASE + "/" + slug).rstrip("/")}">' if BASE else ""
shutil.rmtree(DIST, ignore_errors=True)
DIST.mkdir()

CSS = """:root{--bg:#fff;--fg:#1a1a1a;--muted:#4a4a4a;--accent:#0b5cad;--soft:#f2f5f9;--line:#c8d0da}*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:18px/1.6 system-ui,Segoe UI,sans-serif}a{color:var(--accent)}
a:focus,button:focus,input:focus,select:focus,textarea:focus{outline:3px solid #ffbf47;outline-offset:2px}
.skip{position:absolute;left:-999px}.skip:focus{left:1rem;top:1rem;background:#fff;padding:.5rem;z-index:9}
header,main,footer{max-width:46rem;margin:auto;padding:1rem 1.25rem}header{display:flex;flex-wrap:wrap;gap:.5rem 1.5rem;align-items:baseline;border-bottom:1px solid var(--line)}
nav a{margin-right:1rem}label{display:block;margin:.9rem 0 .2rem;font-weight:600}input,select,textarea{font:inherit;padding:.45rem;width:100%;border:1px solid #6b7785;border-radius:6px;background:#fff;color:var(--fg)}
input[type=color]{padding:.1rem;height:2.6rem}output,.result{display:block;margin:1.2rem 0;padding:1rem;background:var(--soft);border-radius:8px;font-size:1.2rem}
.btn{display:inline-block;background:var(--accent);color:#fff;border:0;padding:.6rem 1.1rem;border-radius:6px;font:inherit;font-weight:600;cursor:pointer}
.muted{color:var(--muted)}.grid{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(14rem,1fr));padding:0;list-style:none}.card{border:1px solid var(--line);border-radius:8px;padding:1rem}
fieldset{border:1px solid var(--line);border-radius:8px;margin:1rem 0}ul.plain{list-style:none;padding:0}label.inline{display:flex;gap:.5rem;font-weight:400;align-items:flex-start}label.inline input{width:1.2rem;height:1.2rem;margin-top:.35rem}
#preview{border:1px solid var(--line);border-radius:8px;padding:1rem;margin:1rem 0}#preview table{width:100%;border-collapse:collapse}#preview th,#preview td{border:1px solid #888;padding:.4rem;text-align:left}
@media print{body.pp *{visibility:hidden}body.pp #preview,body.pp #preview *{visibility:visible}body.pp #preview{position:absolute;left:0;top:0;width:100%;border:0}}
.preview{padding:1rem;border:1px solid var(--line);border-radius:8px;margin:1rem 0}textarea{min-height:14rem;font-family:ui-monospace,Consolas,monospace;font-size:.9rem}"""

TOOLS = []  # (slug, title, description)


def page(slug, title, desc, h1, intro, tool, script, notes):
    TOOLS.append((slug, title, desc))
    body = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} | Nitsuah Labs free tools</title><meta name="description" content="{html.escape(desc)}">{canonical(slug)}<link rel="stylesheet" href="{href_css()}"></head><body>
<a class="skip" href="#main">Skip to content</a><header><strong>Nitsuah Labs tools</strong><nav aria-label="Main"><a href="{href_index()}">All tools</a></nav></header>
<main id="main"><h1>{html.escape(h1)}</h1><p>{intro}</p>{tool}<h2>About this tool</h2>{notes}</main>
<footer><p class="muted">Free, runs in your browser, nothing is uploaded or tracked. <a href="{href_index()}">More free tools</a>.</p></footer><script>{script}</script></body></html>"""
    (DIST / f"{slug}.html").write_text(body, encoding="utf-8")


NUM = "const $=i=>parseFloat(document.getElementById(i).value)||0;const out=document.getElementById('out');document.querySelectorAll('input').forEach(e=>e.addEventListener('input',run));"


def field(i, label, v):
    return f'<label for="{i}">{label}</label><input id="{i}" type="number" step="any" value="{v}">'


# --- contrast checker ---
page("contrast-checker", "WCAG color contrast checker", "Check text and background color contrast against WCAG 2.2 AA and AAA. Free, runs in your browser.",
     "WCAG color contrast checker", "Pick a text color and a background color to see the contrast ratio and whether it passes WCAG AA and AAA.",
     """<label for="fg">Text color</label><input id="fg" type="color" value="#767676"><label for="bg">Background color</label><input id="bg" type="color" value="#ffffff">
<div class="preview" id="prev">Sample text: The quick brown fox jumps over the lazy dog.</div><output id="out" aria-live="polite"></output>""",
     """function lum(h){const c=[1,3,5].map(i=>parseInt(h.slice(i,i+2),16)/255).map(v=>v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4));return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]}
const fg=document.getElementById('fg'),bg=document.getElementById('bg'),prev=document.getElementById('prev'),out=document.getElementById('out');
function run(){const a=lum(fg.value),b=lum(bg.value),r=(Math.max(a,b)+0.05)/(Math.min(a,b)+0.05);prev.style.color=fg.value;prev.style.background=bg.value;
const p=(t,ok)=>t+': '+(ok?'pass':'FAIL');out.textContent='Contrast '+r.toFixed(2)+':1. '+[p('AA normal text (4.5:1)',r>=4.5),p('AA large text (3:1)',r>=3),p('AAA normal (7:1)',r>=7),p('UI components (3:1)',r>=3)].join(' | ')}
fg.addEventListener('input',run);bg.addEventListener('input',run);run();""",
     "<p>WCAG 2.2 level AA asks for a 4.5:1 contrast ratio for normal text and 3:1 for large text (18pt, or 14pt bold) and for user interface components and graphics. Level AAA asks for 7:1 for normal text. The ratio is computed from the relative luminance of the two colors. Text over images or gradients needs a manual check. The default grey on white is a classic near miss: #767676 is the lightest grey that passes AA on white.</p>")

# --- hourly rate ---
page("freelance-hourly-rate-calculator", "Freelance hourly rate calculator", "Work out the minimum hourly rate you need from your income goal, expenses, billable hours and working weeks.",
     "Freelance hourly rate calculator", "Enter your yearly income goal and costs to see the minimum hourly rate that gets you there.",
     field("income", "Target yearly income ($)", 80000) + field("expenses", "Yearly business expenses ($)", 12000) + field("hours", "Billable hours per week", 25) + field("weeks", "Working weeks per year", 46) + '<output id="out" aria-live="polite"></output>',
     NUM + "function run(){const r=($('income')+$('expenses'))/Math.max(1,$('hours')*$('weeks'));out.textContent='Minimum hourly rate: $'+r.toFixed(2)}run();",
     "<p>Rate = (income goal + expenses) / (billable hours per week x working weeks). Billable hours are fewer than hours worked: admin, sales and learning are unpaid, so most freelancers bill 20 to 30 hours a week. This is before taxes; add your own tax set-aside to the income goal. It is a starting point, not financial advice.</p>")

# --- quote ---
page("project-quote-calculator", "Project quote calculator with risk buffer", "Build a fixed-price project quote from estimated hours, hourly rate, risk buffer and fixed costs.",
     "Project quote calculator", "Turn an hours estimate into a fixed price that includes a buffer for the unknowns.",
     field("hours", "Estimated hours", 40) + field("rate", "Hourly rate ($)", 75) + field("buffer", "Risk buffer (%)", 20) + field("costs", "Fixed costs ($)", 0) + '<output id="out" aria-live="polite"></output>',
     NUM + "function run(){const q=$('hours')*$('rate')*(1+$('buffer')/100)+$('costs');out.textContent='Quote: $'+q.toFixed(2)}run();",
     "<p>Quote = hours x rate x (1 + buffer) + fixed costs. Estimates are usually optimistic, so a 15 to 30 percent buffer is common for work with unknowns. Put the scope and what is out of scope in writing next to any fixed price.</p>")

# --- margin ---
page("margin-markup-calculator", "Margin and markup calculator", "Calculate profit margin and markup from cost and price.",
     "Margin and markup calculator", "Enter what something costs and what you charge to see both margin and markup.",
     field("cost", "Cost ($)", 60) + field("price", "Price ($)", 100) + '<output id="out" aria-live="polite"></output>',
     NUM + "function run(){const m=$('price')?($('price')-$('cost'))/$('price')*100:0,k=$('cost')?($('price')-$('cost'))/$('cost')*100:0;out.textContent='Margin: '+m.toFixed(1)+'%  |  Markup: '+k.toFixed(1)+'%'}run();",
     "<p>Margin is profit as a share of the price; markup is profit as a share of the cost. A 50 percent markup is a 33.3 percent margin, a common source of pricing mistakes.</p>")

# --- late fee ---
page("late-fee-calculator", "Late payment fee calculator", "Calculate a simple late fee and total due for an overdue invoice.",
     "Late payment fee calculator", "See what a monthly late fee adds to an overdue invoice.",
     field("amount", "Invoice amount ($)", 1000) + field("rate", "Monthly late fee (%)", 1.5) + field("months", "Months late", 2) + '<output id="out" aria-live="polite"></output>',
     NUM + "function run(){const f=$('amount')*($('rate')/100)*$('months');out.textContent='Late fee: $'+f.toFixed(2)+'  |  Total due: $'+($('amount')+f).toFixed(2)}run();",
     "<p>This is a simple, non-compounding fee. Late fees must be in your contract or invoice terms in advance, and legal limits vary by place, so check local rules before charging them. Not legal advice.</p>")

# --- JSON-LD ---
page("local-business-json-ld-generator", "Local business JSON-LD generator", "Generate schema.org LocalBusiness structured data (JSON-LD) from a simple form. Free and private.",
     "Local business JSON-LD generator", "Fill in your business details and copy the structured data into your site's head.",
     """<label for="type">Type</label><select id="type"><option>LocalBusiness</option><option>Restaurant</option><option>CafeOrCoffeeShop</option><option>Store</option><option>ProfessionalService</option></select>
<label for="name">Business name</label><input id="name" type="text" value="Corner Cafe"><label for="url">Website URL</label><input id="url" type="url" value="https://example.com">
<label for="tel">Phone</label><input id="tel" type="tel" value="Phone not provided"><label for="street">Street</label><input id="street" type="text" value="123 Main Street">
<label for="city">City</label><input id="city" type="text" value="Your Town"><label for="state">State</label><input id="state" type="text" value="VA"><label for="zip">ZIP</label><input id="zip" type="text" value="20000">
<label for="o1">Weekday hours: opens</label><input id="o1" type="time" value="07:00"><label for="c1">Weekday hours: closes</label><input id="c1" type="time" value="16:00">
<label for="o2">Weekend hours: opens</label><input id="o2" type="time" value="08:00"><label for="c2">Weekend hours: closes</label><input id="c2" type="time" value="14:00">
<label for="result">JSON-LD to paste in your page head</label><textarea id="result" readonly></textarea><button class="btn" id="copy" type="button">Copy</button><span id="done" role="status" class="muted"></span>""",
     """const g=i=>document.getElementById(i).value;
function run(){const d={"@context":"https://schema.org","@type":g('type'),name:g('name'),url:g('url'),telephone:g('tel'),
address:{"@type":"PostalAddress",streetAddress:g('street'),addressLocality:g('city'),addressRegion:g('state'),postalCode:g('zip'),addressCountry:"US"},
openingHoursSpecification:[{"@type":"OpeningHoursSpecification",dayOfWeek:["Monday","Tuesday","Wednesday","Thursday","Friday"],opens:g('o1'),closes:g('c1')},
{"@type":"OpeningHoursSpecification",dayOfWeek:["Saturday","Sunday"],opens:g('o2'),closes:g('c2')}]};
document.getElementById('result').value='<script type="application/ld+json">\\n'+JSON.stringify(d,null,2)+'\\n<\\/script>'}
document.querySelectorAll('input,select').forEach(e=>e.addEventListener('input',run));run();
document.getElementById('copy').addEventListener('click',function(){const t=document.getElementById('result');t.select();try{navigator.clipboard.writeText(t.value);document.getElementById('done').textContent=' Copied.'}catch(e){document.getElementById('done').textContent=' Select the text and copy it.'}});""",
     "<p>Structured data helps search engines understand your business details such as name, address, phone and opening hours. Paste the output in the head of your page, then test it with a validator such as the Schema.org validator or Google's Rich Results Test. It does not guarantee rankings. US country code is assumed; edit it in the output if needed.</p>")

# --- SRT shifter ---
page("srt-subtitle-shifter", "SRT subtitle time shifter", "Shift SRT subtitle timings earlier or later by a number of seconds. Runs in your browser; the file never leaves your computer.",
     "SRT subtitle time shifter", "Fix subtitles that are out of sync by shifting every timestamp. Your file stays on your computer.",
     """<label for="file">SRT file</label><input id="file" type="file" accept=".srt,text/plain"><label for="secs">Shift (seconds, negative = earlier)</label><input id="secs" type="number" step="0.1" value="2.5">
<button class="btn" id="go" type="button">Shift and download</button><output id="out" aria-live="polite">Choose a file to begin.</output>""",
     """const T=/(\\d{2}):(\\d{2}):(\\d{2}),(\\d{3})/g;
function sh(m,h,mi,s,ms,k){let v=((+h*60+ +mi)*60+ +s)*1000+ +ms+k;v=Math.max(0,Math.round(v));const p=(n,l)=>String(n).padStart(l,'0');return p(Math.floor(v/3600000),2)+':'+p(Math.floor(v/60000)%60,2)+':'+p(Math.floor(v/1000)%60,2)+','+p(v%1000,3)}
document.getElementById('go').addEventListener('click',function(){const f=document.getElementById('file').files[0],out=document.getElementById('out');if(!f){out.textContent='Please choose an SRT file first.';return}
const k=(parseFloat(document.getElementById('secs').value)||0)*1000;f.text().then(function(t){const r=t.replace(T,function(m,h,mi,s,ms){return sh(m,h,mi,s,ms,k)});
const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([r],{type:'text/plain'}));a.download=f.name.replace(/\\.srt$/i,'')+'-shifted.srt';a.click();out.textContent='Done. Downloaded '+a.download+'.'})});""",
     "<p>SubRip (.srt) files store each subtitle with a start and end time. If a video was re-edited or the subtitles came from a different cut, every cue can be a fixed number of seconds off. This tool adds or subtracts that offset from all timestamps. Times never go below zero.</p>")

# --- invoice generator ---
rows = "".join(
    f'<fieldset><legend>Line item {i}</legend><label for="d{i}">Description</label><input id="d{i}" type="text" value="{d}">'
    f'<label for="q{i}">Quantity</label><input id="q{i}" type="number" step="any" value="{q}"><label for="r{i}">Rate ($)</label><input id="r{i}" type="number" step="any" value="{r}"></fieldset>'
    for i, (d, q, r) in enumerate([("Website design", 1, 1200), ("Hosting setup", 2, 75), ("", 0, 0), ("", 0, 0), ("", 0, 0)], 1))
page("invoice-generator", "Free invoice generator (print or save as PDF)", "Make a clean invoice in your browser and print it or save it as a PDF. No sign-up, nothing uploaded.",
     "Free invoice generator", "Fill in the details, check the preview, then print or save as PDF from your browser. Nothing is uploaded.",
     """<div class="noprint"><label for="from">Your name and address</label><textarea id="from" rows="3">Your Name
123 Main Street
Your Town, ST 00000</textarea><label for="to">Bill to</label><textarea id="to" rows="3">Client Name
456 Client Road
Client Town, ST 00000</textarea>
<label for="num">Invoice number</label><input id="num" type="text" value="1001"><label for="date">Invoice date</label><input id="date" type="date" value="2026-01-15"><label for="due">Due date</label><input id="due" type="date" value="2026-02-14">
""" + rows + """<label for="tax">Tax (%)</label><input id="tax" type="number" step="any" value="0"><label for="notes">Notes or payment details</label><textarea id="notes" rows="3">Payment due within 30 days. Thank you.</textarea>
<button class="btn" id="print" type="button">Print or save as PDF</button></div><section id="preview" aria-label="Invoice preview" aria-live="polite"></section>""",
     """document.body.className='pp';const g=i=>document.getElementById(i).value;const money=n=>'$'+n.toFixed(2);
function run(){const pv=document.getElementById('preview');pv.textContent='';
const el=(t,x,p)=>{const e=document.createElement(t);if(x!==undefined)e.textContent=x;(p||pv).appendChild(e);return e};
el('h2','Invoice '+g('num'));el('p','Date: '+g('date')+'   Due: '+g('due'));
const f=el('p','From:\\n'+g('from'));f.style.whiteSpace='pre-line';const t=el('p','Bill to:\\n'+g('to'));t.style.whiteSpace='pre-line';
const tb=el('table');const hr=el('tr',undefined,el('thead',undefined,tb));['Description','Qty','Rate','Amount'].forEach(h=>el('th',h,hr));
const body=el('tbody',undefined,tb);let sub=0;
for(let i=1;i<=5;i++){const d=g('d'+i),q=parseFloat(g('q'+i))||0,r=parseFloat(g('r'+i))||0;if(!d&&!q&&!r)continue;const a=q*r;sub+=a;
const tr=el('tr',undefined,body);el('td',d,tr);el('td',String(q),tr);el('td',money(r),tr);el('td',money(a),tr);}
const tax=sub*((parseFloat(g('tax'))||0)/100);
[['Subtotal',sub],['Tax',tax],['Total due',sub+tax]].forEach(function(x){const tr=el('tr',undefined,body);const c=el('th',x[0],tr);c.colSpan=3;el('td',money(x[1]),tr);});
const n=el('p',g('notes'));n.style.whiteSpace='pre-line';}
document.querySelectorAll('input,textarea').forEach(e=>e.addEventListener('input',run));run();
document.getElementById('print').addEventListener('click',function(){window.print();});""",
     "<p>Fill in your details and up to five line items; the preview updates as you type and totals are calculated for you. Use your browser's print dialog and choose Save as PDF to keep a copy. Nothing leaves your device. Check tax and invoicing rules where you work; this is a formatting aid, not legal or tax advice.</p>")

# --- accessibility checklist ---
GROUPS = {
    "Perceivable": [("1.1.1", "Every meaningful image has a text alternative; decorative images are hidden from assistive tech"), ("1.2.2", "Prerecorded video has captions"), ("1.3.1", "Headings, lists, tables and form labels use real HTML structure"), ("1.4.3", "Text contrast is at least 4.5:1 (3:1 for large text)"), ("1.4.4", "Text can be zoomed to 200% without losing content"), ("1.4.10", "Content reflows at 320px wide without horizontal scrolling"), ("1.4.11", "Buttons, inputs and focus indicators have 3:1 contrast")],
    "Operable": [("2.1.1", "Everything works with a keyboard alone"), ("2.1.2", "Keyboard focus is never trapped"), ("2.4.1", "A skip link lets keyboard users bypass the navigation"), ("2.4.3", "Focus order follows the visual order"), ("2.4.4", "Link text makes sense out of context"), ("2.4.7", "Keyboard focus is clearly visible"), ("2.4.11", "Focused items are not hidden behind sticky headers (WCAG 2.2)"), ("2.5.8", "Click targets are at least 24 by 24 CSS pixels (WCAG 2.2)")],
    "Understandable": [("3.1.1", "The page language is set (html lang)"), ("3.2.3", "Navigation is consistent across pages"), ("3.3.1", "Form errors are identified in text"), ("3.3.2", "Inputs have visible labels and instructions"), ("3.3.7", "Do not ask users to re-enter information you already have (WCAG 2.2)"), ("3.3.8", "Login does not rely on solving a puzzle or memorizing (WCAG 2.2)")],
    "Robust": [("4.1.2", "Custom controls expose name, role and state"), ("4.1.3", "Status messages are announced without moving focus")],
}
chk = "".join(f"<h2>{g}</h2><ul class='plain'>" + "".join(f"<li><label class='inline'><input type='checkbox' data-k='{c}'> <strong>{c}</strong> {t}</label></li>" for c, t in items) + "</ul>" for g, items in GROUPS.items())
page("accessibility-checklist", "Website accessibility checklist (WCAG 2.2 AA)", "A plain-language WCAG 2.2 AA checklist for designers and developers. Ticks are saved in your browser.",
     "Website accessibility checklist (WCAG 2.2 AA)", "A working checklist in plain language. Ticks are saved in this browser only.",
     chk, """document.querySelectorAll('input[type=checkbox]').forEach(function(c){try{c.checked=localStorage.getItem('a11y-'+c.dataset.k)==='1'}catch(e){}c.addEventListener('change',function(){try{localStorage.setItem('a11y-'+c.dataset.k,c.checked?'1':'0')}catch(e){}})})""",
     "<p>The numbers are WCAG success criteria. Automated tools catch only part of these issues, so also test with a keyboard and a screen reader. This is a working aid, not a conformance audit or legal advice.</p>")

# --- word counter ---
page("word-counter", "Word and character counter with reading time", "Count words, characters, sentences and estimate reading time as you type. Runs in your browser; nothing is uploaded.",
     "Word and character counter", "Paste or type text to count words, characters, sentences and paragraphs, with an estimated reading time.",
     '<label for="t">Your text</label><textarea id="t" rows="10">Paste your text here.</textarea><output id="out" aria-live="polite"></output>',
     """const t=document.getElementById('t'),out=document.getElementById('out');
function run(){const s=t.value,w=(s.trim().match(/\\S+/g)||[]).length,c=s.length,cn=s.replace(/\\s/g,'').length,se=(s.match(/[^.!?]+[.!?]+(\\s|$)/g)||[]).length,p=s.split(/\\n\\s*\\n/).filter(x=>x.trim()).length,m=w/238;
out.textContent=w+' words | '+c+' characters ('+cn+' without spaces) | '+se+' sentences | '+p+' paragraphs | reading time '+(m<1?'under 1 minute':Math.round(m)+' minutes')}
t.addEventListener('input',run);run();""",
     "<p>Words are runs of non-space characters. Reading time assumes about 238 words per minute, a commonly cited average for silent reading of non-fiction; speaking time is closer to 130 words per minute. Sentence counts are approximate because abbreviations also end with periods.</p>")

# --- aspect ratio ---
page("aspect-ratio-calculator", "Aspect ratio and resolution calculator", "Find the aspect ratio of a width and height, or scale a resolution to a new width while keeping the ratio.",
     "Aspect ratio and resolution calculator", "Enter a resolution to see its aspect ratio, then enter a new width to get the matching height.",
     field("w", "Width (px)", 1920) + field("h", "Height (px)", 1080) + field("nw", "New width (px)", 1280) + '<output id="out" aria-live="polite"></output>',
     NUM + "function gcd(a,b){return b?gcd(b,a%b):a}function run(){const w=$('w'),h=$('h'),nw=$('nw');if(!w||!h){out.textContent='Enter a width and height.';return}const d=gcd(Math.round(w),Math.round(h));out.textContent='Aspect ratio '+(Math.round(w)/d)+':'+(Math.round(h)/d)+' ('+(w/h).toFixed(3)+'). At width '+nw+' the height is '+Math.round(nw*h/w)+' px.'}run();",
     "<p>The ratio is width divided by height, reduced with the greatest common divisor. Common ratios: 16:9 for video and most screens, 9:16 for vertical video, 1:1 for square posts, 4:3 for older displays and 4:5 for portrait social posts. Many video encoders need even dimensions; round to the nearest even number if needed.</p>")

# --- color converter ---
page("color-converter", "HEX, RGB and HSL color converter", "Convert a color between HEX, RGB and HSL and see a preview.",
     "HEX, RGB and HSL color converter", "Pick a color or type a HEX value to get RGB and HSL.",
     '<label for="c">Color</label><input id="c" type="color" value="#0b5cad"><label for="hx">HEX</label><input id="hx" type="text" value="#0b5cad"><div class="preview" id="prev">Preview</div><output id="out" aria-live="polite"></output>',
     """const c=document.getElementById('c'),hx=document.getElementById('hx'),prev=document.getElementById('prev'),out=document.getElementById('out');
function conv(h){h=h.replace('#','');if(h.length===3)h=h.split('').map(x=>x+x).join('');if(!/^[0-9a-f]{6}$/i.test(h))return null;const r=parseInt(h.slice(0,2),16),g=parseInt(h.slice(2,4),16),b=parseInt(h.slice(4,6),16),R=r/255,G=g/255,B=b/255,mx=Math.max(R,G,B),mn=Math.min(R,G,B),l=(mx+mn)/2,d=mx-mn;
let s=0,hu=0;if(d){s=d/(1-Math.abs(2*l-1));hu=mx===R?((G-B)/d)%6:mx===G?(B-R)/d+2:(R-G)/d+4;hu=Math.round(hu*60);if(hu<0)hu+=360}return{r,g,b,h:hu,s:Math.round(s*100),l:Math.round(l*100),hex:'#'+h.toLowerCase()}}
function show(v){const o=conv(v);if(!o){out.textContent='Enter a valid HEX value such as #0b5cad.';return}prev.style.background=o.hex;prev.style.color=(o.r*0.299+o.g*0.587+o.b*0.114)>150?'#000':'#fff';out.textContent=o.hex+' | rgb('+o.r+', '+o.g+', '+o.b+') | hsl('+o.h+', '+o.s+'%, '+o.l+'%)';return o}
c.addEventListener('input',function(){hx.value=c.value;show(c.value)});hx.addEventListener('input',function(){const o=show(hx.value);if(o)c.value=o.hex});show(hx.value);""",
     "<p>HEX is the red, green and blue channels in base 16. RGB lists them as 0 to 255. HSL describes hue (0 to 360 degrees), saturation and lightness. Values are rounded to whole numbers, so a round trip can differ by one step.</p>")

# --- case converter ---
page("text-case-converter", "Text case converter", "Convert text to upper case, lower case, title case, sentence case, camelCase, snake_case or kebab-case.",
     "Text case converter", "Type or paste text and choose a case.",
     '<label for="t">Your text</label><textarea id="t" rows="5">Hello world from the case converter</textarea><label for="m">Convert to</label><select id="m"><option value="upper">UPPER CASE</option><option value="lower">lower case</option><option value="title">Title Case</option><option value="sentence">Sentence case</option><option value="camel">camelCase</option><option value="snake">snake_case</option><option value="kebab">kebab-case</option></select><label for="o">Result</label><textarea id="o" rows="5" readonly></textarea>',
     """const t=document.getElementById('t'),m=document.getElementById('m'),o=document.getElementById('o');
const words=s=>s.toLowerCase().match(/[a-z0-9]+/g)||[];
function run(){const s=t.value,w=words(s),k=m.value;o.value=k==='upper'?s.toUpperCase():k==='lower'?s.toLowerCase():k==='title'?s.toLowerCase().replace(/(^|\\s)(\\S)/g,(x,a,b)=>a+b.toUpperCase()):k==='sentence'?s.toLowerCase().replace(/(^\\s*|[.!?]\\s+)(\\S)/g,(x,a,b)=>a+b.toUpperCase()):k==='camel'?w.map((x,i)=>i?x[0].toUpperCase()+x.slice(1):x).join(''):k==='snake'?w.join('_'):w.join('-')}
t.addEventListener('input',run);m.addEventListener('change',run);run();""",
     "<p>Camel, snake and kebab case split on anything that is not a letter or number, so punctuation is dropped. Title case here capitalizes every word and does not apply style-guide rules for small words.</p>")

# --- UTM builder ---
page("utm-link-builder", "UTM link builder", "Build a campaign URL with UTM parameters for source, medium, campaign, term and content.",
     "UTM link builder", "Add campaign tracking parameters to a link so your analytics can tell where visits came from.",
     '<label for="u">Website URL</label><input id="u" type="url" value="https://example.com/page"><label for="s">Source (utm_source)</label><input id="s" type="text" value="newsletter"><label for="m">Medium (utm_medium)</label><input id="m" type="text" value="email"><label for="c">Campaign (utm_campaign)</label><input id="c" type="text" value="spring_launch"><label for="te">Term (optional)</label><input id="te" type="text"><label for="co">Content (optional)</label><input id="co" type="text"><label for="o">Tagged URL</label><textarea id="o" rows="3" readonly></textarea>',
     """const g=i=>document.getElementById(i).value.trim();
function run(){let u;try{u=new URL(g('u'))}catch(e){document.getElementById('o').value='Enter a full URL starting with https://';return}
[['utm_source','s'],['utm_medium','m'],['utm_campaign','c'],['utm_term','te'],['utm_content','co']].forEach(function(p){const v=g(p[1]);if(v)u.searchParams.set(p[0],v);else u.searchParams.delete(p[0])});document.getElementById('o').value=u.toString()}
document.querySelectorAll('input').forEach(e=>e.addEventListener('input',run));run();""",
     "<p>UTM parameters are plain query-string tags that analytics tools read. Keep names consistent and lower case so reports do not split into near-duplicates, and never put personal data in them because URLs get logged and shared.</p>")

# --- password generator ---
page("password-generator", "Random password generator", "Generate strong random passwords in your browser using the Web Crypto API. Nothing is sent anywhere.",
     "Random password generator", "Choose a length and character types. Passwords are generated on your device and never sent or stored.",
     field("len", "Length", 20) + '<label class="inline"><input id="lo" type="checkbox" checked> Lower case</label><label class="inline"><input id="up" type="checkbox" checked> Upper case</label><label class="inline"><input id="di" type="checkbox" checked> Digits</label><label class="inline"><input id="sy" type="checkbox" checked> Symbols</label><button class="btn" id="gen" type="button">Generate</button><output id="out" aria-live="polite"></output>',
     """const out=document.getElementById('out');
function rnd(n){const a=new Uint32Array(1),lim=Math.floor(4294967296/n)*n;let x;do{crypto.getRandomValues(a);x=a[0]}while(x>=lim);return x%n}
function run(){const L=Math.min(128,Math.max(8,parseInt(document.getElementById('len').value)||20)),sets=[];
if(document.getElementById('lo').checked)sets.push('abcdefghijklmnopqrstuvwxyz');if(document.getElementById('up').checked)sets.push('ABCDEFGHIJKLMNOPQRSTUVWXYZ');if(document.getElementById('di').checked)sets.push('0123456789');if(document.getElementById('sy').checked)sets.push('!@#$%^&*()-_=+[]{};:,.?');
if(!sets.length){out.textContent='Pick at least one character type.';return}
const all=sets.join('');const pw=sets.map(s=>s[rnd(s.length)]);while(pw.length<L)pw.push(all[rnd(all.length)]);for(let i=pw.length-1;i>0;i--){const j=rnd(i+1);[pw[i],pw[j]]=[pw[j],pw[i]]}out.textContent=pw.join('')}
document.getElementById('gen').addEventListener('click',run);run();""",
     "<p>Characters are chosen with the browser's cryptographic random number generator (crypto.getRandomValues) using rejection sampling to avoid bias, and at least one character from each selected type is included. Use a password manager to store the result. A longer password is stronger than a more complicated short one.</p>")

# --- heading outline checker ---
page("heading-outline-checker", "HTML heading outline checker", "Paste HTML to see its heading outline and catch skipped levels, a missing h1 or multiple h1s. Runs in your browser.",
     "HTML heading outline checker", "Paste a page's HTML to see its heading structure and find accessibility problems such as skipped heading levels.",
     '<label for="h">HTML</label><textarea id="h" rows="10">&lt;h1&gt;Title&lt;/h1&gt;&lt;h2&gt;Section&lt;/h2&gt;&lt;h4&gt;Skipped a level&lt;/h4&gt;</textarea><output id="out" aria-live="polite"></output>',
     """const h=document.getElementById('h'),out=document.getElementById('out');
function txt(s){return s.replace(/<[^>]*>/g,'').replace(/&nbsp;/g,' ').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').replace(/&amp;/g,'&').replace(/\\s+/g,' ').trim();}
function run(){const hs=[],re=/<h([1-6])\\b[^>]*>([\\s\\S]*?)<\\/h\\1\\s*>/gi;let m;while((m=re.exec(h.value))){hs.push({l:+m[1],t:txt(m[2])});}out.textContent='';
if(!hs.length){out.textContent='No headings found.';return}
const ul=document.createElement('ul');let prev=0,issues=[],h1=0;
hs.forEach(function(e){const l=e.l;if(l===1)h1++;const li=document.createElement('li');li.style.marginLeft=((l-1)*1.2)+'rem';li.textContent='h'+l+': '+(e.t||'(empty)');
if(prev&&l>prev+1){li.textContent+='  <- skips from h'+prev+' to h'+l;issues.push('Skipped level before "'+e.t+'"')}
if(!e.t)issues.push('Empty h'+l);ul.appendChild(li);prev=l});
if(h1===0)issues.push('No h1 found');if(h1>1)issues.push('More than one h1 ('+h1+')');
out.appendChild(ul);const p=document.createElement('p');p.textContent=issues.length?'Issues: '+issues.join('; '):'No heading problems found.';out.appendChild(p);}
h.addEventListener('input',run);run();""",
     "<p>Screen reader users navigate by headings, so levels should not skip (for example h2 straight to h4), and a page normally has one h1. Pasted HTML is read with simple pattern matching in your browser and never sent anywhere, so unusual markup (headings split across templates or generated by scripts) can be missed. This checks heading structure only, not whether headings are well written.</p>")

# --- link text checker ---
page("link-text-checker", "Vague link text checker", "Paste HTML to find links with vague or empty text like click here or read more, which fail accessibility guidance.",
     "Vague link text checker", "Paste HTML to find links whose text does not say where they go.",
     '<label for="h">HTML</label><textarea id="h" rows="10">&lt;a href="/a"&gt;Click here&lt;/a&gt; &lt;a href="/b"&gt;Pricing plans&lt;/a&gt; &lt;a href="/c"&gt;&lt;img src="x.png"&gt;&lt;/a&gt;</textarea><output id="out" aria-live="polite"></output>',
     """const h=document.getElementById('h'),out=document.getElementById('out');const BAD=['click here','here','read more','more','learn more','link','this','this link','click','details','continue'];
function txt(s){return s.replace(/<[^>]*>/g,'').replace(/&nbsp;/g,' ').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').replace(/&amp;/g,'&').replace(/\\s+/g,' ').trim();}
function run(){const as=[],re=/<a\\b([^>]*)>([\\s\\S]*?)<\\/a\\s*>/gi;let m;while((m=re.exec(h.value))){const at=m[1],hr=at.match(/href\\s*=\\s*["']([^"']*)["']/i);if(hr)as.push({href:hr[1],aria:(at.match(/aria-label\\s*=\\s*["']([^"']*)["']/i)||[])[1],inner:m[2],raw:m[0]});}out.textContent='';const bad=[];
as.forEach(function(a){let label=(a.aria||txt(a.inner)).trim();if(!label){label=[...a.inner.matchAll(/<img\\b[^>]*\\balt\\s*=\\s*["']([^"']*)["']/gi)].map(x=>x[1]).join(' ').trim();}label=label.toLowerCase();
if(!label)bad.push('Empty link text: '+a.raw.slice(0,80));else if(BAD.indexOf(label.replace(/[.!:]+$/,''))>-1)bad.push('Vague text "'+label+'" -> '+a.href);});
const p=document.createElement('p');p.textContent=as.length+' link(s) checked. '+(bad.length?bad.length+' problem(s):':'No vague or empty link text found.');out.appendChild(p);
if(bad.length){const ul=document.createElement('ul');bad.forEach(b=>{const li=document.createElement('li');li.textContent=b;ul.appendChild(li);});out.appendChild(ul);}}
h.addEventListener('input',run);run();""",
     "<p>WCAG asks that the purpose of a link can be understood from its text (success criterion 2.4.4). Screen readers can list all links on a page, where \"click here\" is meaningless. This checks the text, aria-label and image alt text of links using simple pattern matching against a short list of vague phrases, so it will miss other vague wording and unusual markup. Nothing is uploaded.</p>")

# --- time zone converter ---
ZONES = ["UTC", "America/New_York", "America/Chicago", "America/Denver", "America/Los_Angeles", "America/Sao_Paulo", "Europe/London", "Europe/Paris", "Europe/Berlin", "Africa/Johannesburg", "Asia/Dubai", "Asia/Kolkata", "Asia/Singapore", "Asia/Tokyo", "Australia/Sydney", "Pacific/Auckland"]
zopts = "".join(f"<option>{z}</option>" for z in ZONES)
page("time-zone-converter", "Time zone converter", "Convert a date and time between time zones, including daylight saving changes.",
     "Time zone converter", "Pick a date and time and the zones to convert between.",
     f'<label for="dt">Date and time</label><input id="dt" type="datetime-local" value="2026-01-15T09:00"><label for="from">From</label><select id="from">{zopts}</select><label for="to">To</label><select id="to">{zopts}</select><output id="out" aria-live="polite"></output>',
     """const dt=document.getElementById('dt'),from=document.getElementById('from'),to=document.getElementById('to'),out=document.getElementById('out');from.value='America/New_York';to.value='Europe/London';
function off(ms,z){const p=new Intl.DateTimeFormat('en-US',{timeZone:z,timeZoneName:'longOffset'}).formatToParts(new Date(ms)).find(x=>x.type==='timeZoneName').value,m=p.match(/GMT([+-])(\\d{2}):(\\d{2})/);return m?(m[1]==='-'?-1:1)*(+m[2]*60+ +m[3])*60000:0}
function run(){if(!dt.value){out.textContent='Pick a date and time.';return}const m=dt.value.match(/(\\d+)-(\\d+)-(\\d+)T(\\d+):(\\d+)/),g=Date.UTC(+m[1],m[2]-1,+m[3],+m[4],+m[5]);let u=g-off(g,from.value);u=g-off(u,from.value);
const f=new Intl.DateTimeFormat('en-GB',{timeZone:to.value,dateStyle:'full',timeStyle:'short'}).format(new Date(u));out.textContent=dt.value.replace('T',' ')+' in '+from.value+' = '+f+' in '+to.value}
[dt,from,to].forEach(e=>e.addEventListener('input',run));run();""",
     "<p>The entered time is read as local time in the From zone, then shown in the To zone using your browser's built-in time zone database, so daylight saving changes are handled for the date you choose. A shortlist of common zones is included. Times in the gap or overlap of a daylight saving change are ambiguous and may resolve either way.</p>")

# --- salary / hourly ---
page("hourly-to-salary-calculator", "Hourly to salary calculator", "Convert an hourly rate to a yearly salary and back, using your hours per week and weeks per year.",
     "Hourly to salary calculator", "Convert between an hourly rate and a yearly amount.",
     field("hr", "Hourly rate ($)", 50) + field("hrs", "Hours per week", 40) + field("wk", "Weeks per year", 52) + field("yr", "Or yearly amount ($)", 0) + '<output id="out" aria-live="polite"></output>',
     NUM + "function run(){const hr=$('hr'),hrs=$('hrs'),wk=$('wk'),yr=$('yr');if(yr>0&&hrs*wk>0){out.textContent='Yearly '+yr.toFixed(2)+' = hourly $'+(yr/(hrs*wk)).toFixed(2)+' ('+hrs+' h/week, '+wk+' weeks)'}else{out.textContent='Hourly $'+hr.toFixed(2)+' = yearly $'+(hr*hrs*wk).toFixed(2)+' = monthly $'+(hr*hrs*wk/12).toFixed(2)}}run();",
     "<p>Yearly = hourly x hours per week x weeks per year. Enter a yearly amount to convert the other way; leave it at 0 to convert from hourly. Gross figures only, before tax and unpaid time off. For freelancers, see the hourly rate calculator, which accounts for expenses and non-billable time.</p>")

# --- percentage ---
page("percentage-calculator", "Percentage calculator", "Calculate X percent of a number, what percent one number is of another, and percentage change.",
     "Percentage calculator", "Three common percentage questions in one place.",
     field("a", "A", 20) + field("b", "B", 150) + '<output id="out" aria-live="polite"></output>',
     NUM + "function run(){const a=$('a'),b=$('b');out.textContent=a+'% of '+b+' = '+(a/100*b).toFixed(4).replace(/\\.?0+$/,'')+'  |  '+a+' is '+(b?(a/b*100).toFixed(2):'n/a')+'% of '+b+'  |  change from '+a+' to '+b+' = '+(a?((b-a)/Math.abs(a)*100).toFixed(2)+'%':'n/a')}run();",
     "<p>Enter two numbers, A and B. The result shows A percent of B, A as a percentage of B, and the percentage change from A to B (positive for an increase). Division by zero shows n/a.</p>")

# --- json formatter ---
page("json-formatter", "JSON formatter and validator", "Format, indent and validate JSON in your browser. Nothing is uploaded.",
     "JSON formatter and validator", "Paste JSON to validate it and get a cleanly indented version.",
     '<label for="i">JSON</label><textarea id="i" rows="8">{"name":"Ada","skills":["math","code"],"active":true}</textarea><label for="o">Formatted</label><textarea id="o" rows="8" readonly></textarea><output id="out" aria-live="polite"></output>',
     """const i=document.getElementById('i'),o=document.getElementById('o'),out=document.getElementById('out');
function run(){try{const v=JSON.parse(i.value);o.value=JSON.stringify(v,null,2);out.textContent='Valid JSON.'}catch(e){o.value='';out.textContent='Invalid JSON: '+e.message}}
i.addEventListener('input',run);run();""",
     "<p>The input is parsed with the browser's JSON parser and re-printed with two-space indentation; the error message comes from the browser and usually points at the position of the problem. JSON does not allow comments, trailing commas or single quotes. Nothing is sent anywhere.</p>")

# --- base64 ---
page("base64-encoder-decoder", "Base64 encoder and decoder", "Encode text to Base64 or decode Base64 back to text, with UTF-8 support, in your browser.",
     "Base64 encoder and decoder", "Convert text to Base64 and back. UTF-8 characters are handled correctly.",
     '<label for="i">Input</label><textarea id="i" rows="5">Hello, wörld!</textarea><label for="m">Action</label><select id="m"><option value="enc">Encode to Base64</option><option value="dec">Decode from Base64</option></select><label for="o">Result</label><textarea id="o" rows="5" readonly></textarea><output id="out" aria-live="polite"></output>',
     """const i=document.getElementById('i'),m=document.getElementById('m'),o=document.getElementById('o'),out=document.getElementById('out');
function run(){out.textContent='';try{if(m.value==='enc'){const b=new TextEncoder().encode(i.value);let s='';b.forEach(x=>s+=String.fromCharCode(x));o.value=btoa(s)}else{const s=atob(i.value.trim()),b=Uint8Array.from(s,c=>c.charCodeAt(0));o.value=new TextDecoder('utf-8',{fatal:true}).decode(b)}}catch(e){o.value='';out.textContent='Could not convert: input is not valid for this action.'}}
i.addEventListener('input',run);m.addEventListener('change',run);run();""",
     "<p>Base64 represents bytes using 64 printable characters. Text is converted to UTF-8 bytes first, so accented letters and emoji round-trip correctly. Base64 is an encoding, not encryption: anyone can decode it.</p>")

# --- url encoder ---
page("url-encoder-decoder", "URL encoder and decoder", "Percent-encode or decode text for use in URLs and query strings.",
     "URL encoder and decoder", "Encode text for safe use in a URL, or decode a percent-encoded string.",
     '<label for="i">Input</label><textarea id="i" rows="4">name=Ada Lovelace&city=Zürich</textarea><label for="m">Action</label><select id="m"><option value="enc">Encode</option><option value="dec">Decode</option></select><label for="o">Result</label><textarea id="o" rows="4" readonly></textarea><output id="out" aria-live="polite"></output>',
     """const i=document.getElementById('i'),m=document.getElementById('m'),o=document.getElementById('o'),out=document.getElementById('out');
function run(){out.textContent='';try{o.value=m.value==='enc'?encodeURIComponent(i.value):decodeURIComponent(i.value)}catch(e){o.value='';out.textContent='Could not decode: the input has an invalid percent sequence.'}}
i.addEventListener('input',run);m.addEventListener('change',run);run();""",
     "<p>Encoding uses encodeURIComponent, which escapes reserved characters such as spaces, ampersands, equals signs and slashes, so encode individual values rather than a whole URL. Decoding uses decodeURIComponent.</p>")

# --- timestamp ---
page("unix-timestamp-converter", "Unix timestamp converter", "Convert a Unix timestamp (seconds or milliseconds) to a readable date and back.",
     "Unix timestamp converter", "Convert between Unix time and a readable date.",
     field("ts", "Unix timestamp (seconds or milliseconds)", 1760000000) + '<label for="iso">Or an ISO date</label><input id="iso" type="text" value="2026-01-15T09:00:00Z"><output id="out" aria-live="polite"></output>',
     """const ts=document.getElementById('ts'),iso=document.getElementById('iso'),out=document.getElementById('out');
function run(){const lines=[];const n=parseFloat(ts.value);if(!isNaN(n)){const ms=Math.abs(n)>1e11?n:n*1000,d=new Date(ms);lines.push(isNaN(d)?'Timestamp out of range':'Timestamp '+n+' = '+d.toISOString()+' (UTC)')}
const d2=new Date(iso.value);lines.push(isNaN(d2)?'Enter an ISO date like 2026-01-15T09:00:00Z':iso.value+' = '+Math.floor(d2.getTime()/1000)+' seconds ('+d2.getTime()+' ms)');out.textContent=lines.join('  |  ')}
ts.addEventListener('input',run);iso.addEventListener('input',run);run();""",
     "<p>Unix time counts seconds since 1 January 1970 UTC. Values above about 100 billion are treated as milliseconds. Dates are shown in UTC to avoid ambiguity; include a Z or an offset in ISO dates, otherwise the browser uses your local time zone.</p>")

# --- regex tester ---
page("regex-tester", "Regex tester", "Test a JavaScript regular expression against sample text and see every match. Runs in your browser.",
     "Regex tester", "Try a regular expression on sample text and see each match with its position.",
     '<label for="p">Pattern</label><input id="p" type="text" value="\\b[a-z]+@[a-z]+\\.com\\b"><label for="f">Flags (for example g, i, m)</label><input id="f" type="text" value="gi"><label for="t">Text</label><textarea id="t" rows="6">Contact ann@example.com or bob@example.com for details.</textarea><output id="out" aria-live="polite"></output>',
     """const p=document.getElementById('p'),f=document.getElementById('f'),t=document.getElementById('t'),out=document.getElementById('out');
function run(){out.textContent='';let re;try{re=new RegExp(p.value,f.value.replace(/[^dgimsuvy]/g,''))}catch(e){out.textContent='Invalid pattern: '+e.message;return}
const ms=[];if(re.global){let m,n=0;while((m=re.exec(t.value))&&n<1000){ms.push(m);if(m[0]==='')re.lastIndex++;n++}}else{const m=re.exec(t.value);if(m)ms.push(m)}
const hd=document.createElement('p');hd.textContent=ms.length+' match(es)'+(re.global?'':' (add the g flag for all matches)');out.appendChild(hd);const ul=document.createElement('ul');
ms.slice(0,200).forEach(function(m){const li=document.createElement('li');li.textContent='"'+m[0]+'" at index '+m.index+(m.length>1?' groups: '+m.slice(1).map(x=>x===undefined?'-':x).join(', '):'');ul.appendChild(li)});out.appendChild(ul)}
[p,f,t].forEach(e=>e.addEventListener('input',run));run();""",
     "<p>Patterns use JavaScript regular expression syntax, which differs from other languages in places such as lookbehind support and named groups. Matching stops at 1000 matches. Very complex patterns on long text can be slow because the browser runs them on this page.</p>")

# --- index ---
cards = "".join(f'<li class="card"><h2><a href="{href_page(s)}">{html.escape(t)}</a></h2><p>{html.escape(d)}</p></li>' for s, t, d in TOOLS)
(DIST / "index.html").write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Free tools for freelancers, developers and small sites | Nitsuah Labs</title><meta name="description" content="Free browser tools: WCAG contrast checker, freelance rate and quote calculators, JSON-LD generator, SRT subtitle shifter. No sign-up, nothing uploaded.">{canonical("")}<link rel="stylesheet" href="{href_css()}"></head><body>
<a class="skip" href="#main">Skip to content</a><header><strong>Nitsuah Labs tools</strong></header><main id="main"><h1>Free tools that run in your browser</h1>
<p>Small, useful tools for freelancers, developers and small business sites. No sign-up, no tracking, nothing is uploaded.</p><ul class="grid">{cards}</ul></main>
<footer><p class="muted">Built by Nitsuah Labs.{"" if BASE else ' Source packs and offline scripts: <a href="https://nitsua5.gumroad.com">nitsua5.gumroad.com</a>.'}</p></footer></body></html>""", encoding="utf-8")
(DIST / "style.css").write_text(CSS, encoding="utf-8")
(DIST / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
(DIST / "404.html").write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found</title><link rel="stylesheet" href="{href_css()}"></head><body><main id="main"><h1>Page not found</h1><p><a href="{href_index()}">See all free tools</a></p></main></body></html>', encoding="utf-8")
if not BASE:
    with zipfile.ZipFile(ROOT / "tools-site.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(DIST.iterdir()):
            z.write(p, p.name)
print(len(TOOLS), "tool pages + index;", "base=" + (BASE or "(standalone)"))
