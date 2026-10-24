"""Offline zero-dependency smoke test. Run: python tests/smoke.py"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import subprocess, sys, re
root=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=set();self.urls=[];self.text=[];self.tags=[];self.main=False
        self.mobile=False;self.menu_button=False;self.title=False;self.viewport=False
    def handle_starttag(self,name,attrs):
        a=dict(attrs);self.tags.append((name,a))
        if a.get('id'):self.ids.add(a['id'])
        if name=='main' and a.get('id')=='main':self.main=True
        if name=='nav' and a.get('id')=='mobile-menu':self.mobile=True
        if name=='button' and a.get('id')=='menu-toggle':self.menu_button=True
        if name=='title':self.title=True
        if name=='meta' and a.get('name')=='viewport':self.viewport=True
        attr={'a':'href','img':'src','script':'src','link':'href'}.get(name)
        if attr and a.get(attr):self.urls.append(a[attr])
    def handle_data(self,data):self.text.append(data)

def parse(file):
    p=Page();p.feed(file.read_text(encoding='utf8'));return p

pages=sorted(root.glob('*.html'))
errors=[];checked=0
if len(pages)!=8:errors.append(f'Expected 8 HTML pages; found {len(pages)}')
for file in pages:
    page=parse(file)
    for property_name in ('main','mobile','menu_button','title','viewport'):
        if not getattr(page,property_name):errors.append(f'{file.name}: missing {property_name}')
    visible=' '.join(page.text)
    if 'Johell' in visible or 'JOHELL' in visible:errors.append(f'{file.name}: old name visibly printed')
    if file.name=='index.html' and not all(x.casefold() in visible.casefold() for x in ('ODUKOYA','JOEL','software developer','websites','web applications')):
        errors.append('index.html: identity or service focus missing')
    normalized=visible.replace('J.O.I .','J.O.I.')
    if re.search(r'(?i)(?<![a-z.])joi(?![a-z.])', normalized):
        errors.append(f'{file.name}: J.O.I. brand punctuation missing')
    unwanted=('Independent Digital Practice','Portfolio / 2026','Drag to Orbit','Change Form','Restore Form',
              'Proof Is in the Work','Make It Real','The Human Behind the Code','Ideas Are Only the Beginning',
              'Build What Matters','Good Work Starts With a Hello')
    if any(term.casefold() in visible.casefold() for term in unwanted):
        errors.append(f'{file.name}: unwanted decorative or generic copy remains')
    if file.name=='contact.html':
        if not all(k in page.ids for k in ('contact-form','name','email','subject','message')):errors.append('contact.html: composer incomplete')
        if 'not a website submission service' not in visible:errors.append('contact.html: explicit email-draft disclosure missing')
        if 'ODUKOYAJOEL@ZOHOMAIL.COM' not in visible or '+234 916 075 1598' not in visible:errors.append('contact.html: verified contact details missing')
    if file.name=='about.html' and 'assets/joel-enhanced.webp' not in page.urls:errors.append('about.html: optimized display portrait missing')
    if file.name=='services.html':
        if visible.count('Request a quote') < 7:errors.append('services.html: service quote actions missing')
        for service in ('Business websites','Full-stack web applications','School websites','Website redesign and improvement','Website updates and maintenance','Deployment and domain setup'):
            if service not in visible:errors.append('services.html: missing '+service)
        if 'mailto:ODUKOYAJOEL@ZOHOMAIL.COM' not in file.read_text(encoding='utf8'):errors.append('services.html: email-based quote workflow missing')
        if any(x in visible for x in ('USD','NGN','Naira')):errors.append('services.html: fixed-currency pricing found')
    for raw in page.urls:
        u=urlparse(raw)
        if u.scheme or raw.startswith('//'):continue
        target=(root/unquote(u.path)).resolve() if u.path else file
        if not target.is_relative_to(root):errors.append(f'{file.name}: unsafe link {raw}')
        elif not target.exists():errors.append(f'{file.name}: missing linked file {raw}')
        elif u.fragment and target.suffix=='.html' and unquote(u.fragment) not in parse(target).ids:
            errors.append(f'{file.name}: broken fragment {raw}')
        checked+=1

required_assets=('assets/caleb-live-capture.webp','assets/caleb-finder-capture.webp','assets/school-live-capture.webp',
                'assets/services-concept.webp','assets/og-portfolio.png')
all_html='\n'.join(f.read_text(encoding='utf8') for f in pages)
for asset in required_assets:
    if asset not in all_html:errors.append('Required new image is not referenced: '+asset)
for logo in ('html5.svg','css3.svg','javascript.svg','typescript.svg','react.svg','nextdotjs.svg',
             'nodedotjs.svg','python.svg','supabase.svg','github.svg','x.svg','instagram.svg','linkedin.svg'):
    if f'assets/logos/{logo}' not in all_html:errors.append('Required logo is not referenced: '+logo)

for js in (root/'js').glob('*.js'):
    proc=subprocess.run(['node','--check',str(js)],capture_output=True,text=True)
    if proc.returncode:errors.append(f'{js.name}: {proc.stderr.strip()}')
for word in ('prefers-reduced-motion','max-width:760px','max-width:390px','.mobile-menu','.about-editorial {'):
    if word not in (root/'styles.css').read_text():errors.append('CSS missing feature: '+word)
print(f'Checked {len(pages)} HTML pages and {checked} local references; checked JS syntax, anchors, navigation, identity and mobile/reduced-motion rules.')
if errors:
    for error in errors:print('FAIL:',error)
    sys.exit(1)
print('PASS: all static smoke tests')
