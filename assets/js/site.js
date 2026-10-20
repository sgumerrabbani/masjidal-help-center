const rootURL=new URL('../..',document.currentScript.src);
function local(path){return new URL(path,rootURL).href;}
function esc(s){return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function topicURL(t){return local(t.items?.length?'category/index.html?topic='+encodeURIComponent(t.slug):'article/index.html?topic='+encodeURIComponent(t.slug));}
function topicCard(t){return `<a class="topic-card" href="${topicURL(t)}">${t.image?`<div class="topic-image"><img src="${local(t.image)}" alt="${esc(t.title)}" loading="lazy"></div>`:''}<div class="topic-body"><h3>${esc(t.title)}</h3><p>${esc(t.desc||'')}</p><span class="topic-arrow">${t.items?.length?'Browse guides':'Read guide'} <span aria-hidden="true">→</span></span></div></a>`;}
function header(){return `<a class="skip-link" href="#main">Skip to content</a><header class="site-header"><div class="container nav"><a class="brand" href="${local('index.html')}" aria-label="Masjidal Help Center"><img class="brand-logo" src="${local(helpData.logo)}" alt="Masjidal"></a><button class="mobile-menu" id="mobileMenu" aria-expanded="false" aria-controls="navigation">Menu ☰</button><div class="navigation" id="navigation"><nav class="nav-links" aria-label="Main navigation"><a class="nav-link" href="https://mymasjidal.ca/pages/features">Features for Masjid</a><details class="dropdown"><summary class="dropdown-toggle">Products <span aria-hidden="true">⌄</span></summary><div class="dropdown-menu">${Object.entries(productLinks).map(([key,links])=>`<div class="dropdown-col"><h4>${key==='consumers'?'For your home':'For your masjid'}</h4>${links.map(([n,u])=>`<a href="${u}">${esc(n)}</a>`).join('')}</div>`).join('')}</div></details><a class="nav-link" href="https://mymasjidal.ca/pages/faq">FAQs</a><a class="nav-link" href="mailto:info@masjidal.com">Contact us</a></nav><div class="nav-actions"><a class="nav-btn" href="https://portal.masjidal.com">Log in</a><a class="nav-btn primary" href="https://portal.masjidal.com">Sign up</a></div></div></div></header>`;}
function footer(){return `<footer class="site-footer"><div class="container footer-inner"><div><a class="brand" href="${local('index.html')}"><img class="brand-logo" src="${local(helpData.logo)}" alt="Masjidal"></a><p>Islamic tech for masjids, homes, and everyone in between.</p><small>© ${new Date().getFullYear()} Masjidal</small></div><div class="footer-links"><a href="${local('index.html')}">Help topics</a><a href="mailto:masjidsupport@masjidal.com">Contact support</a><a href="https://mymasjidal.ca/policies/privacy-policy">Privacy policy</a></div></div></footer>`;}
function support(){return `<div class="cta-band"><div><strong>Still need help?</strong><p>Get in touch with the Masjidal support team.</p></div><a class="cta-btn" href="mailto:masjidsupport@masjidal.com">Contact support <span aria-hidden="true">↗</span></a></div>`;}
function searchBox(value=''){return `<form class="search-wrap" action="${local('category/index.html')}"><span class="search-icon" aria-hidden="true">⌕</span><input class="search-input" name="q" type="search" value="${esc(value)}" placeholder="Search setup, prayer times, announcements…" aria-label="Search all help articles"><button class="search-submit" type="submit" aria-label="Search">→</button></form>`;}
function shell(content){document.body.innerHTML=header()+content+footer()+emailOptions();bindEmailOptions();document.getElementById('mobileMenu').onclick=e=>{const open=e.currentTarget.getAttribute('aria-expanded')!=='true';e.currentTarget.setAttribute('aria-expanded',open);document.getElementById('navigation').classList.toggle('open',open);};document.addEventListener('keydown',e=>{if(e.key==='Escape'){document.querySelector('.dropdown').open=false;document.getElementById('navigation').classList.remove('open');document.getElementById('mobileMenu').setAttribute('aria-expanded','false');}});}

function emailOptions(){
  return `<dialog class="email-dialog" id="emailOptions" aria-labelledby="emailTitle"><div class="email-dialog-head"><h2 id="emailTitle">Send us an email</h2><button type="button" class="email-close" aria-label="Close email options">&times;</button></div><p>Choose your email service, or copy the address.</p><input id="emailAddress" aria-label="Email address" readonly><div class="email-services"><a data-email-launch id="emailApp">Open email app</a><a id="emailGmail" target="_blank" rel="noopener noreferrer">Gmail &nearr;</a><a id="emailOutlook" target="_blank" rel="noopener noreferrer">Outlook &nearr;</a><button type="button" id="emailCopy">Copy email address</button></div><p class="email-hint">If your email app does not open, choose Gmail or Outlook, or paste the address into your email service.</p><p id="emailStatus" role="status" aria-live="polite"></p></dialog>`;
}
function bindEmailOptions(){
  const dialog=document.getElementById('emailOptions');
  const address=document.getElementById('emailAddress');
  const status=document.getElementById('emailStatus');
  document.querySelectorAll('a[href^="mailto:"]').forEach(link=>{
    if(link.hasAttribute('data-email-launch'))return;
    link.addEventListener('click',event=>{
      if(event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;
      event.preventDefault();
      const href=link.getAttribute('href');
      const [recipient,query='']=href.slice(7).split('?');
      address.value=decodeURIComponent(recipient);
      const parameters=new URLSearchParams(query);
      document.getElementById('emailApp').href=href;
      const gmail=new URL('https://mail.google.com/mail/');
      gmail.search=new URLSearchParams({view:'cm',fs:'1',to:address.value,su:parameters.get('subject')||'',body:parameters.get('body')||''});
      document.getElementById('emailGmail').href=gmail.href;
      const outlook=new URL('https://outlook.live.com/mail/0/deeplink/compose');
      outlook.search=new URLSearchParams({to:address.value,subject:parameters.get('subject')||'',body:parameters.get('body')||''});
      document.getElementById('emailOutlook').href=outlook.href;
      status.textContent='';
      dialog.showModal();
    });
  });
  dialog.querySelector('.email-close').onclick=()=>dialog.close();
  dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close();});
  document.getElementById('emailCopy').onclick=async()=>{
    try{await navigator.clipboard.writeText(address.value);status.textContent='Email address copied.';}
    catch{address.focus();address.select();status.textContent='Select and copy this address into your email service.';}
  };
}
