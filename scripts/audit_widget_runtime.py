"""Reproduce widget blank states using the public library and mocked API responses.

No account credentials, live timings, or signed-in portal access are used.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
import json,hashlib,requests
r=Path(__file__).resolve().parents[1];out=r/'tmp/widget-investigation';out.mkdir(parents=True,exist_ok=True)
response=requests.get('https://widgets.masjidal.com/timetable/v0/widget.js',timeout=40);response.raise_for_status();(out/'widget.js').write_bytes(response.content)
script=response.content.decode('utf-8');results=[]
cases=[('prayer-premium',{'type':'prayer','premium':True}),('prayer-basic',{'type':'prayer','premium':False}),('announcements-premium',{'type':'announcement','premium':True}),('announcements-basic',{'type':'announcement','premium':False}),('settings-403',{'type':'prayer','status':403}),('settings-500',{'type':'prayer','status':500}),('settings-missing',{'type':'prayer','missing_settings':True}),('wrong-type-plural',{'type':'announcements','premium':True}),('missing-key',{'type':'prayer','missing_key':True}),('late-attributes',{'type':'prayer','late':True}),('settings-blocked',{'type':'prayer','abort':True}),('announcement-api-fails',{'type':'announcement','premium':True,'ann_fails':True}),('timings-api-fails',{'type':'prayer','premium':True,'timings_fails':True}),('timings-empty',{'type':'prayer','premium':True,'empty_timings':True})]
with sync_playwright() as p:
 for engine in ['chromium','firefox']:
  b=getattr(p,engine).launch()
  for name,case in cases:
   page=b.new_page();requests=[];errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   def route_handler(route):
    u=urlparse(route.request.url)
    if u.hostname=='widget-test.example':
     attrs='' if case.get('late') else ' widget-id="test-widget" type="'+case['type']+'"'+('' if case.get('missing_key') else ' api-key="msj_pk_TEST_NOT_A_REAL_KEY"')
     html='<html><head><script src="https://widgets.masjidal.com/timetable/v0/widget.js" defer></script></head><body><masjidal-widget'+attrs+'></masjidal-widget></body></html>'
     route.fulfill(status=200,content_type='text/html; charset=utf-8',body=html)
    elif u.hostname=='widgets.masjidal.com':route.fulfill(status=200,content_type='text/javascript; charset=utf-8',body=script)
    elif u.hostname=='api.masjidal.com':
     requests.append(u.path)
     if u.path=='/widgets':
      if case.get('abort'):route.abort('failed');return
      payload={'data':{}} if case.get('missing_settings') else {'data':{'settings':{'isPremium':case.get('premium',True),'theme':'light','layout':'table','annLayout':'stacked','header':'masjid'}}}
      status=case.get('status',200)
     elif u.path=='/timings':payload={'data':{'masjid':'Test Masjid','timezone':'America/Toronto','timings':([] if case.get('empty_timings') else [{'date':'Monday, Nov 2, 2026','salah':{'fajr':'06:00 AM','sunrise':'07:00 AM','dhuhr':'12:30 PM','asr':'03:00 PM','maghrib':'05:30 PM','isha':'07:00 PM'},'iqamah':{'fajr':'06:30 AM','dhuhr':'01:00 PM','asr':'03:30 PM','maghrib':'05:35 PM','isha':'07:30 PM'}}])}};status=500 if case.get('timings_fails') else 200
     elif u.path=='/announcements':payload={'data':{'announcements':[{'title':'Test notice','message':'Test message','type':'important'}]}};status=500 if case.get('ann_fails') else 200
     else:raise AssertionError(u.path)
     route.fulfill(status=status,content_type='application/json',headers={'Access-Control-Allow-Origin':'*'},body=json.dumps(payload))
    else:route.abort()
   page.route('**/*',route_handler);page.goto('https://widget-test.example/');page.wait_for_function('customElements.get("masjidal-widget")!==undefined');page.wait_for_timeout(250)
   if case.get('late'):
    page.evaluate('''()=>{let w=document.querySelector('masjidal-widget');w.setAttribute('widget-id','test-widget');w.setAttribute('type','prayer');w.setAttribute('api-key','msj_pk_TEST_NOT_A_REAL_KEY')}''');page.wait_for_timeout(150)
   facts=page.evaluate('''()=>{let w=document.querySelector('masjidal-widget'),s=w.shadowRoot;return {upgraded:!!s,rendered:!!s?.querySelector('.prayer-widget-root,.ann-widget-root'),visibleText:s?.querySelector('div')?.innerText?.slice(0,250)||'',height:w.getBoundingClientRect().height}}''');row={'engine':engine,'case':name,**facts,'requests':requests,'errors':errors};results.append(row);expected=name in ['prayer-premium','prayer-basic','announcements-premium','announcement-api-fails'];assert facts['rendered']==expected,(name,facts);print(engine,name,"rendered" if facts["rendered"] else "blank",flush=True);page.close()
  b.close()
(out/'reproduction-results.json').write_text(json.dumps({'script_sha256':hashlib.sha256(script.encode()).hexdigest(),'mocked_api':True,'results':results},indent=2))

print("Passed",len(results),"public-library/mock-API browser cases. Results:",out/"reproduction-results.json")
