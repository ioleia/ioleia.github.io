// Capture only local, committed runtime files. QA_OUTPUT must be outside the checkout.
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs=require('node:fs');
const path=require('node:path');
const crypto=require('node:crypto');
const root=path.resolve(__dirname,'..');
const output=process.env.QA_OUTPUT;
if(!output) throw Error('Set QA_OUTPUT to the review evidence directory.');
fs.mkdirSync(output,{recursive:true});
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.BROWSER_PATH?{executablePath:process.env.BROWSER_PATH}:{})});
 try{
  for(const [name,width,height] of [['desktop',1440,900],['tablet',768,1024],['mobile',390,844],['mobile-320',320,740]]){
   const page=await browser.newPage({viewport:{width,height}});
   await page.goto('file://'+path.join(root,'index.html'));
   await page.waitForTimeout(200);
   await page.screenshot({path:path.join(output,name+'.png'),fullPage:true});
   if(name==='desktop'||name==='mobile'){
    for(let moment=2;moment<=3;moment++){
     await page.getByRole('button',{name:new RegExp('Read message '+moment)}).click();
     await page.screenshot({path:path.join(output,`${name}-moment-${moment}.png`),fullPage:true});
    }
   }
   await page.close();
  }
  const reduced=await browser.newPage({viewport:{width:390,height:844},reducedMotion:'reduce'});
  await reduced.goto('file://'+path.join(root,'index.html'));
  await reduced.screenshot({path:path.join(output,'reduced-motion.png'),fullPage:true});
  await reduced.close();
  const master=fs.readFileSync(path.join(root,'docs/brand/ioleia-a2-1-master-monochrome.svg'),'utf8');
  const luminous=fs.readFileSync(path.join(root,'assets/ioleia-a2-1-luminous.svg'),'utf8');
  const comparison=await browser.newPage({viewport:{width:1100,height:610}});
  const uri=s=>'data:image/svg+xml;base64,'+Buffer.from(s).toString('base64');
  await comparison.setContent(`<body style="margin:0;background:#09092b;color:#f8f1e8;font:16px/1.6 system-ui;display:flex;text-align:center;justify-content:space-evenly;padding-top:56px"><figure><img width="400" src="${uri(master.replace('fill="#000000"','fill="#f8f1e8"'))}"><figcaption>Canonical A2.1 · light ink for comparison</figcaption></figure><figure><img width="400" src="${uri(luminous)}"><figcaption>Luminous rendering · same locked path</figcaption></figure></body>`);
  await comparison.screenshot({path:path.join(output,'logo-comparison.png')});
  const geometry=await comparison.evaluate(async({master,luminous})=>{
   const raster=async svg=>{const i=new Image();i.src='data:image/svg+xml;base64,'+btoa(unescape(encodeURIComponent(svg)));await i.decode();const c=document.createElement('canvas');c.width=c.height=700;const x=c.getContext('2d');x.drawImage(i,0,0,700,700);return x.getImageData(0,0,700,700).data};
   const a=await raster(master),b=await raster(luminous);let canonicalPixels=0,pixelsOutsideCanonical=0,missingInteriorPixels=0;
   for(let i=3;i<a.length;i+=4){if(a[i]>0)canonicalPixels++;if(a[i]===0&&b[i]>0)pixelsOutsideCanonical++;if(a[i]>240&&b[i]===0)missingInteriorPixels++;}
   return {renderSize:700,canonicalPixels,pixelsOutsideCanonical,missingInteriorPixels};
  },{master,luminous});
  if(geometry.pixelsOutsideCanonical||geometry.missingInteriorPixels)throw Error('Raster geometry mismatch');
  fs.writeFileSync(path.join(output,'geometry-checks.json'),JSON.stringify(geometry,null,2));
  const runtime=['index.html','styles.css','preview.js','assets/ioleia-a2-1-luminous.svg','assets/reference/approved-light-field-board.png'];
  const hashes=Object.fromEntries(runtime.map(file=>[file,crypto.createHash('sha256').update(fs.readFileSync(path.join(root,file))).digest('hex')]));
  fs.writeFileSync(path.join(output,'captured-runtime-hashes.json'),JSON.stringify(hashes,null,2));
  console.log(JSON.stringify({screenshots:10,geometry,runtimeFiles:runtime.length}));
 }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
