// Run with PLAYWRIGHT_MODULE set to the installed Playwright package path.
// Optional BROWSER_PATH selects a local Chrome; no web service is involved.
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const output = process.env.QA_OUTPUT || '/private/tmp/ioleia-scene-qa';
fs.mkdirSync(output, {recursive:true});
const url = 'file://' + path.join(root, 'index.html');
const report = {checks:[], layouts:[], externalRequests:[], consoleErrors:[], pageErrors:[]};
function check(name, condition) {assert.ok(condition, name); report.checks.push(name);}
(async () => {
  const browser = await chromium.launch({headless:true, ...(process.env.BROWSER_PATH ? {executablePath:process.env.BROWSER_PATH} : {})});
  try {
    const context = await browser.newContext();
    context.on('request', req => {if (/^https?:/.test(req.url())) report.externalRequests.push(req.url());});
    context.on('page', page => {
      page.on('console', msg => {if(msg.type()==='error') report.consoleErrors.push(msg.text());});
      page.on('pageerror', err => report.pageErrors.push(err.message));
    });
    const page = await context.newPage();
    await page.setViewportSize({width:1440,height:900});
    await page.clock.install();
    await page.goto(url);
    check('One email-only form and one signup CTA', await page.locator('form').count()===1 && await page.locator('input').count()===1 && await page.getByRole('button',{name:'Join early access',exact:true}).count()===1);
    const active = () => page.locator('.moment.is-current').getAttribute('aria-labelledby');
    const stopped = () => page.evaluate(() => document.body.classList.contains('motion-paused') && document.getAnimations().every(a=>a.playState!=='running'));
    const position = () => page.locator('.signup-form').boundingBox();
    const firstPosition = await position();
    check('Initial Moment 1', await active()==='moment-one');
    await page.clock.runFor(16000);
    await page.waitForTimeout(600);
    const opacity = await page.locator('.moment').evaluateAll(nodes=>nodes.map(n=>Number(getComputedStyle(n).opacity)));
    check('A real 1.2-second opacity crossfade', opacity[0]>0 && opacity[0]<1 && opacity[1]>0 && opacity[1]<1);
    await page.waitForTimeout(700);
    check('Moment 2 after its dwell', await active()==='moment-two');
    check('Signup stays in the same position through crossfade', JSON.stringify(await position())===JSON.stringify(firstPosition));
    await page.clock.runFor(20000);
    await page.waitForTimeout(1300);
    check('Moment 3 follows Moment 2', await active()==='moment-three');
    await page.clock.runFor(14000);
    await page.waitForTimeout(1300);
    check('Sequence loops to Moment 1', await active()==='moment-one');
    await page.locator('#email').focus();
    check('Email focus freezes field and messages', await stopped());
    const focused = await active();
    await page.clock.runFor(40000);
    check('No rotation during focus', await active()===focused);
    await page.locator('#email').fill('reader@example.com');
    await page.locator('#email').blur();
    await page.clock.runFor(40000);
    check('Typing keeps motion paused after blur', await stopped() && await active()===focused);
    await page.getByRole('button',{name:'Resume motion',exact:true}).click();
    check('Explicit resume restarts motion', !(await stopped()));
    await page.getByRole('button',{name:'Pause motion',exact:true}).click();
    check('Pause Motion freezes both systems', await stopped());
    await page.locator('#email').fill('not-an-email');
    await page.getByRole('button',{name:'Join early access',exact:true}).click();
    check('Native invalid email check and input focus', await page.locator('#email').evaluate(e=>e.validity.typeMismatch && e===document.activeElement));
    await page.locator('#email').fill('');
    await page.getByRole('button',{name:'Join early access',exact:true}).click();
    check('Native required email check', await page.locator('#email').evaluate(e=>e.validity.valueMissing));
    await page.locator('#email').fill('reader@example.com');
    await page.locator('#email').press('Enter');
    check('Enter submits a truthful preview confirmation', (await page.locator('.form-status').textContent()).includes('Nothing was sent or saved'));
    check('Preview clears email and focuses status', await page.locator('#email').inputValue()==='' && await page.locator('.form-status').evaluate(e=>e===document.activeElement));
    check('Submission stays paused', await stopped());
    check('No cookies created', (await context.cookies()).length===0);
    await page.reload();
    await page.keyboard.press('Tab');
    check('Keyboard reaches skip link', await page.locator('.skip-link').evaluate(e=>e===document.activeElement));
    await page.keyboard.press('Enter');
    check('Skip link focuses main', await page.locator('main').evaluate(e=>e===document.activeElement));
    await page.getByRole('button',{name:/Read message 2/}).focus();
    await page.keyboard.press('Enter');
    check('Keyboard message selection works and pauses', await active()==='moment-two' && await stopped());
    check('Visible keyboard focus ring', await page.getByRole('button',{name:/Read message 2/}).evaluate(e=>getComputedStyle(e).outlineStyle==='solid'));
    await page.emulateMedia({reducedMotion:'reduce'});
    await page.waitForFunction(()=>document.querySelector('.moment.is-current').getAttribute('aria-labelledby')==='moment-one' && document.getAnimations().length===0);
    check('Reduced motion returns to Moment 1 with zero animation', await active()==='moment-one' && (await page.evaluate(()=>document.getAnimations().length))===0);
    await page.clock.runFor(90000);
    check('Reduced motion never rotates automatically', await active()==='moment-one');
    await page.getByRole('button',{name:/Read message 3/}).click();
    check('Reduced motion offers nonanimated access to other copy', await active()==='moment-three' && (await page.evaluate(()=>document.getAnimations().length))===0);
    await page.emulateMedia({reducedMotion:'no-preference'});
    await page.waitForFunction(()=>!matchMedia('(prefers-reduced-motion: reduce)').matches);
    await page.reload();
    // Exercise the visibility handler deterministically, including a fade in progress.
    await page.clock.runFor(16000);
    await page.waitForTimeout(600);
    await page.evaluate(()=>{Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'));});
    check('Hidden document freezes field and in-progress fade', await stopped());
    const frozenOpacity=await page.locator('.moment').evaluateAll(ns=>ns.map(n=>getComputedStyle(n).opacity));
    await page.clock.runFor(30000);
    check('Hidden fade does not advance', JSON.stringify(frozenOpacity)===JSON.stringify(await page.locator('.moment').evaluateAll(ns=>ns.map(n=>getComputedStyle(n).opacity))));
    await page.evaluate(()=>{delete document.hidden;document.dispatchEvent(new Event('visibilitychange'));});
    await page.waitForTimeout(1300);
    check('Visible page resumes the paused fade', !(await stopped()));

    for (const [width,height] of [[1440,900],[1440,768],[768,1024],[390,844],[390,667],[320,740],[320,568]]) {
      await page.setViewportSize({width,height});
      await page.reload();
      const layout={width,height,moments:[]};
      for(let i=0;i<3;i++) {
        await page.getByRole('button',{name:new RegExp('Read message '+(i+1))}).click();
        const data=await page.evaluate(()=>{
          const box=s=>document.querySelector(s).getBoundingClientRect().toJSON();
          return {scrollWidth:document.documentElement.scrollWidth,scrollHeight:document.documentElement.scrollHeight,orb:box('.orb-art'),text:box('.messages'),signup:box('.signup-form'),input:box('#email'),button:box('#preview-submit')};
        });
        check(`${width}×${height} message ${i+1}: no overflow or overlap`,data.scrollWidth<=width && data.orb.bottom<=data.text.top && data.text.bottom<=data.signup.top && data.input.width>=200 && data.button.height>=44);
        if(width===1440 || height>=740) check(`${width}×${height} signup controls within screen`,data.button.bottom<=height);
        layout.moments.push(data);
      }
      check(`${width}×${height}: stable signup across all messages`,layout.moments.every(m=>m.signup.y===layout.moments[0].signup.y));
      report.layouts.push(layout);
    }
    const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});
    const fallback=await nojs.newPage();
    await fallback.goto(url);
    check('No-JS fallback shows all approved moments', await fallback.locator('.moment:visible').count()===3);
    check('No-JS fallback disables the form',await fallback.locator('#preview-submit').isDisabled() && await fallback.locator('#email').isDisabled());
    check('No-JS fallback states that signup is off',await fallback.locator('noscript').isVisible());
    check('No-JS fallback has no horizontal overflow',await fallback.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
    await fallback.screenshot({path:path.join(output,'no-javascript.png'),fullPage:true});
    await nojs.close();
    check('No external network requests',report.externalRequests.length===0);
    check('No console or page errors',report.consoleErrors.length===0 && report.pageErrors.length===0);
    fs.writeFileSync(path.join(output,'browser-checks.json'),JSON.stringify(report,null,2));
    console.log(JSON.stringify({passed:report.checks.length,layouts:report.layouts.length,externalRequests:report.externalRequests,errors:report.consoleErrors.concat(report.pageErrors)}));
  } finally {await browser.close();}
})().catch(err=>{console.error(err);process.exitCode=1;});
