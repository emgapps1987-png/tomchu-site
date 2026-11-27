(function(){
var CARE=__CARE__,WA="__WA__",EP="__EP__",K='tt-care';
var HEAD=['היום הראשון – שומרים על הכיסוי','שומרים על ניקיון','מגרד? זה סימן שהוא מחלים 💙','כמעט שם – בלי שמש ובלי מים עומדים'];
function tasks(i){return i<=14?[['שטיפה + משחה – בוקר','מים פושרים, סבון עדין, ייבוש בטפיחות'],['שטיפה + משחה – צהריים','שכבה דקה בלבד'],['שטיפה + משחה – ערב','ולא לגרד 😉']]:[['קרם לחות בלי בישום','פעם–פעמיים ביום'],['בלי שמש ישירה, ים, בריכה או ג׳קוזי','מקלחת רגילה – כן']]}
function phase(i){return i<=0?0:i<=3?1:i<=14?2:i<=29?3:4}
var ESC={'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'};
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return ESC[c]})}
function wa(t){return WA+'?text='+encodeURIComponent(t)}
function load(){try{var j=JSON.parse(localStorage.getItem(K)||'null');return j&&/^\d{4}-\d\d-\d\d$/.test(j.start)?j:null}catch(e){return null}}
function save(j){try{if(j)localStorage.setItem(K,JSON.stringify(j));else localStorage.removeItem(K)}catch(e){}}
function iso(d){var z=new Date(d.getTime()-d.getTimezoneOffset()*6e4);return z.toISOString().slice(0,10)}
function fmt(s){var p=s.split('-');return p[2]+'/'+p[1]+'/'+p[0]}
var today=iso(new Date()),root=document.getElementById('hj');
var FEEL={good:'מעולה! ממשיכים ככה 💙',itch:'גירוד וקילוף הם חלק טבעי מההחלמה. לא מגרדים ולא מקלפים – אפשר לטפוח קלות ולמרוח שכבה דקה של משחה.'};
function odd(){return '<div class="hj-alert"><p><strong>מתי לפנות לרופא/ה:</strong> '+esc(CARE.warning)+'</p></div><a class="btn btn-ghost" href="'+wa('היי תום, משהו בקעקוע נראה לי לא רגיל. מצרפ/ת תמונה:')+'" target="_blank" rel="noopener">לשלוח תמונה לתום בוואטסאפ</a>'}
function start(){
 var y=iso(new Date(Date.now()-864e5));
 return '<div class="hj-card hj-start"><h2>יומן החלמה אישי</h2><p class="muted">ספרו לנו מתי עשיתם את הקעקוע, ונלווה אתכם יום־יום עד שהעור מחלים.</p>'+
 '<label for="hj-date">מתי עשיתם את הקעקוע?</label><div class="hj-chips"><button type="button" data-d="'+today+'" aria-pressed="true">היום</button><button type="button" data-d="'+y+'" aria-pressed="false">אתמול</button></div>'+
 '<input type="date" id="hj-date" value="'+today+'" max="'+today+'"><button type="button" class="btn btn-iri" id="hj-go">להתחיל את היומן</button><p class="hj-priv">🔒 נשמר רק במכשיר שלך.</p></div>'}
function journal(j){
 var i=Math.round((Date.parse(today)-Date.parse(j.start))/864e5),ph=phase(i);
 if(ph===4)return '<div class="hj-card hj-done"><span class="big">🏅</span><h2>הקעקוע החלים!</h2><p class="muted">30 יום של שמירה – כל הכבוד. מעכשיו רק קרם הגנה (SPF 50) בשמש, והוא יישאר חד לשנים.</p><a class="btn btn-iri" href="'+wa('היי תום, הקעקוע החלים! הנה תמונה של התוצאה 🙂')+'" target="_blank" rel="noopener">לשלוח לתום תמונה של התוצאה</a><button type="button" class="btn btn-ghost" id="hj-reset">לסיים את היומן</button></div>';
 var T=tasks(i),done=(j.done&&j.done[today])||[],feel=(j.feel&&j.feel[today])||'',pct=Math.min(100,Math.round((i+1)/30*100)),st=CARE.steps[ph];
 var h='<div class="hj-top"><div class="hj-ring" style="--p:'+pct+'%" role="img" aria-label="יום '+(i+1)+' מתוך 30"><div><b>'+(i+1)+'</b><span>מתוך 30</span></div></div><div><span class="hj-kick">יום '+(i+1)+' · '+esc(st.title)+'</span><h2>'+HEAD[ph]+'</h2></div></div>';
 h+='<div class="hj-card"><span class="hj-kick">מה צפוי היום</span><p>'+esc(st.text)+'</p></div>';
 h+='<div class="hj-card"><div class="hj-th"><strong>המשימות של היום</strong><span id="hj-count">'+done.length+' מתוך '+T.length+'</span></div>'+T.map(function(t,k){return '<button type="button" class="hj-task" data-t="'+k+'" aria-pressed="'+(done.indexOf(k)>-1)+'"><span class="ck" aria-hidden="true"></span><span><strong>'+t[0]+'</strong><small>'+t[1]+'</small></span></button>'}).join('')+'</div>';
 h+='<div class="hj-card"><strong>איך הקעקוע מרגיש היום?</strong><div class="hj-feel">'+[['good','😊','מעולה'],['itch','😐','מגרד'],['odd','😟','משהו מוזר']].map(function(f){return '<button type="button" data-f="'+f[0]+'" aria-pressed="'+(feel===f[0])+'"><span aria-hidden="true">'+f[1]+'</span>'+f[2]+'</button>'}).join('')+'</div><div id="hj-fo">'+(feel==='odd'?odd():FEEL[feel]?'<p class="muted">'+FEEL[feel]+'</p>':'')+'</div></div>';
 h+='<div class="hj-card"><strong>הדרך שלך</strong>'+CARE.steps.map(function(s,k){return '<div class="hj-step'+(k<ph?' past':k===ph?' here':'')+'"><span class="dot" aria-hidden="true">'+(k<ph?'✓':'')+'</span><span><span class="when">'+esc(s.when)+(k===ph?' · את/ה כאן':'')+'</span><span class="t">'+esc(s.title)+'</span></span></div>'}).join('')+'</div>';
 if(i<=29)h+='<div class="hj-card"><strong>'+(MOBILE?'תזכורות ביומן של הטלפון':'תזכורות ב־Google Calendar')+'</strong><p class="muted">'+(i<=14?'מוסיפים ליומן (Apple / Google) תזכורות לשטיפה ומשחה – בוקר, צהריים וערב עד סוף השבועיים הראשונים, ותזכורת ליום שבו הקעקוע מחלים.':'מוסיפים ליומן (Apple / Google) תזכורת ליום שבו הקעקוע מחלים.')+'</p><div id="hj-calbox">'+calButtons(j.start,i)+'</div></div>';
 h+='<p class="hj-foot">התחלתם ב־'+fmt(j.start)+' · <button type="button" class="hj-link" id="hj-reset">איפוס היומן</button></p>';
 return h}

function icsFile(start){
 var day=864e5,s0=Date.parse(start+'T12:00:00Z'),td=Date.parse(today+'T12:00:00Z');
 function ymd(t){return new Date(t).toISOString().slice(0,10).replace(/-/g,'')}
 var n=new Date(),p=function(x){return(x<10?'0':'')+x},stamp=n.getUTCFullYear()+p(n.getUTCMonth()+1)+p(n.getUTCDate())+'T'+p(n.getUTCHours())+p(n.getUTCMinutes())+p(n.getUTCSeconds())+'Z';
 function e(x){return String(x).replace(/\\/g,'\\\\').replace(/,/g,'\\,').replace(/;/g,'\;').replace(/\n/g,'\\n')}
 var out=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//Tomchu Tattoo//Care//HE','CALSCALE:GREGORIAN','METHOD:PUBLISH','X-WR-CALNAME:Tomchu Tattoo – החלמה'];
 function ev(uid,t,hh,title,desc,count){out.push('BEGIN:VEVENT','UID:'+uid+'-'+start+'@tomchutattoo','DTSTAMP:'+stamp,'DTSTART:'+ymd(t)+'T'+hh+'0000','DURATION:PT10M');if(count>1)out.push('RRULE:FREQ=DAILY;COUNT='+count);out.push('SUMMARY:'+e(title),'DESCRIPTION:'+e(desc),'BEGIN:VALARM','ACTION:DISPLAY','DESCRIPTION:'+e(title),'TRIGGER:PT0M','END:VALARM','END:VEVENT')}
 var first=Math.max(s0,td),left=15-Math.round((first-s0)/day);
 if(left>0){ev('wash-am',first,'09','קעקוע: שטיפה + משחה 🫧 (בוקר)','מים פושרים, סבון עדין, ייבוש בטפיחות ושכבה דקה של משחה.',left);ev('wash-noon',first,'14','קעקוע: שטיפה + משחה 🫧 (צהריים)','שכבה דקה של משחה, וזהו.',left);ev('wash-pm',first,'20','קעקוע: שטיפה + משחה 🫧 (ערב)','מים פושרים, ייבוש בטפיחות ומשחה. ולא לגרד 😉',left)}
 if(s0+15*day>=td)ev('two-weeks',s0+15*day,'10','שבועיים לקעקוע ✨','מהיום אפשר לעבור לקרם לחות. עוד שבועיים בלי שמש ובריכה.',1);
 if(s0+30*day>=td)ev('healed',s0+30*day,'10','הקעקוע החלים! 🏅','מעכשיו רק קרם הגנה SPF 50 בשמש. מוזמנים לשלוח לתום תמונה של התוצאה.',1);
 out.push('END:VCALENDAR');return out.join('\r\n')}

var MOBILE=(window.matchMedia&&matchMedia('(pointer:coarse)').matches)||/Android|iP(hone|ad|od)/.test(navigator.userAgent);
function gcal(title,details,ymd,hh,count){var d=ymd+'T'+hh+'0000',e=ymd+'T'+hh+'1000';return 'https://calendar.google.com/calendar/render?action=TEMPLATE&text='+encodeURIComponent(title)+'&details='+encodeURIComponent(details)+'&dates='+d+'/'+e+'&ctz=Asia/Jerusalem'+(count>1?'&recur='+encodeURIComponent('RRULE:FREQ=DAILY;COUNT='+count):'')}
function calButtons(start,i){
 if(MOBILE)return '<a class="btn btn-iri" id="hj-ics" href="#">הוספת כל התזכורות ליומן 📅</a><p class="hj-priv">באייפון לוחצים "הוסף הכול". באנדרואיד פותחים עם אפליקציית היומן.</p>';
 var day=864e5,s0=Date.parse(start+'T12:00:00Z'),td=Date.parse(today+'T12:00:00Z'),first=Math.max(s0,td),left=15-Math.round((first-s0)/day);
 function ymd(t){return new Date(t).toISOString().slice(0,10).replace(/-/g,'')}
 var L=[];
 if(left>0){L.push(['☀️ בוקר · 9:00',gcal('קעקוע: שטיפה + משחה 🫧 (בוקר)','מים פושרים, סבון עדין, ייבוש בטפיחות ושכבה דקה של משחה.',ymd(first),'09',left)]);
  L.push(['🌤️ צהריים · 14:00',gcal('קעקוע: שטיפה + משחה 🫧 (צהריים)','שכבה דקה של משחה, וזהו.',ymd(first),'14',left)]);
  L.push(['🌙 ערב · 20:00',gcal('קעקוע: שטיפה + משחה 🫧 (ערב)','מים פושרים, ייבוש בטפיחות ומשחה. ולא לגרד 😉',ymd(first),'20',left)])}
 if(s0+30*day>=td)L.push(['🏅 היום שהקעקוע מחלים',gcal('הקעקוע החלים! 🏅','מעכשיו רק קרם הגנה SPF 50 בשמש. מוזמנים לשלוח לתום תמונה של התוצאה.',ymd(s0+30*day),'10',1)]);
 return '<div class="hj-gcal">'+L.map(function(x){return '<a class="hj-gbtn" href="'+x[1]+'" target="_blank" rel="noopener"><span>'+x[0]+'</span><b>הוספה ›</b></a>'}).join('')+'</div><p class="hj-priv">כל לחיצה פותחת את Google Calendar עם התזכורת מוכנה, ורק לוחצים "שמירה". <a href="#" id="hj-ics" class="hj-link">יומן אחר? הורדת קובץ</a></p>'}
function render(){var j=load();root.innerHTML=j?journal(j):start();bind(j)}
function bind(j){
 var q=function(s){return root.querySelectorAll(s)};
 if(!j){var inp=document.getElementById('hj-date');q('.hj-chips button').forEach(function(b){b.onclick=function(){inp.value=b.dataset.d;q('.hj-chips button').forEach(function(x){x.setAttribute('aria-pressed',String(x===b))})}});
  inp.onchange=function(){q('.hj-chips button').forEach(function(x){x.setAttribute('aria-pressed',String(x.dataset.d===inp.value))})};
  document.getElementById('hj-go').onclick=function(){var v=inp.value;if(!v||v>today)return;save({start:v});render();window.scrollTo({top:root.offsetTop-90})};return}
 q('.hj-task').forEach(function(b){b.onclick=function(){var c=load();if(!c)return;var k=+b.dataset.t,set=(c.done&&c.done[today])||[],x=set.indexOf(k);if(x>-1)set.splice(x,1);else set.push(k);c.done={};c.done[today]=set;save(c);b.setAttribute('aria-pressed',String(x<0));document.getElementById('hj-count').textContent=set.length+' מתוך '+q('.hj-task').length}});
 q('.hj-feel button').forEach(function(b){b.onclick=function(){var c=load();if(!c)return;var v=b.dataset.f;c.feel={};c.feel[today]=v;save(c);q('.hj-feel button').forEach(function(x){x.setAttribute('aria-pressed',String(x===b))});document.getElementById('hj-fo').innerHTML=v==='odd'?odd():'<p class="muted">'+FEEL[v]+'</p>'}});
 var ic=document.getElementById('hj-ics');if(ic)ic.onclick=function(ev){ev.preventDefault();var a=document.createElement('a');a.href=URL.createObjectURL(new Blob([icsFile(j.start)],{type:'text/calendar;charset=utf-8'}));a.download='tomchu-tattoo-care.ics';document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(a.href);a.remove()},2000)};
 var r=document.getElementById('hj-reset');if(r)r.onclick=function(){if(r.dataset.sure!=='1'){r.dataset.sure='1';r.textContent='בטוח? לחיצה נוספת מוחקת את היומן';return}save(null);render()};
}
render();
})();
