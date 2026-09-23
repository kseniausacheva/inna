const {chromium}=require("playwright");const fs=require("fs");
(async()=>{const b=await chromium.launch();const pg=await b.newPage();
const jobs=[["katalog.html","katalog-programm.pdf"],["kair-opisanie.html","kair-opisanie.pdf"],["giza-partner-brief-en.html","giza-partner-brief-en.pdf"],["giza-team-brief-ru.html","giza-team-brief-ru.pdf"],["giza-mehanika-ru.html","giza-mehanika-ru.pdf"],["giza-runbook-en.html","giza-runbook-en.pdf"],["giza-runbook-ar.html","giza-runbook-ar.pdf"],["giza-komplekt-pechati.html","giza-komplekt-pechati.pdf"],["giza-shema-finala.html","giza-shema-finala.pdf"]];
for(const f of fs.readdirSync("programmy").filter(x=>x.endsWith(".html"))) jobs.push(["programmy/"+f,"programmy/"+f.replace(".html",".pdf")]);
for(const [src,out] of jobs){
  await pg.goto("file://"+process.cwd()+"/"+src,{waitUntil:"networkidle"});
  await pg.evaluate(()=>document.fonts.ready);
  await pg.pdf({path:out,format:"A4",printBackground:true,preferCSSPageSize:true});
}
await b.close();console.log("готово:",jobs.length);})().catch(e=>{console.error(e);process.exit(1)})
