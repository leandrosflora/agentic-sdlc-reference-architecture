const money=n=>new Intl.NumberFormat("pt-BR",{style:"currency",currency:"USD",minimumFractionDigits:3}).format(n);
const escapeHtml=s=>String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
async function load(){
  const response=await fetch("dashboard-data.json");
  if(!response.ok) throw new Error("dashboard data unavailable");
  const d=await response.json();
  document.querySelector("#change-title").textContent=d.change_id+" · "+d.project_id;
  document.querySelector("#change-meta").textContent=d.change_set_id+" · risco "+d.risk+" · atualizado "+new Date(d.updated_at).toLocaleString("pt-BR");
  document.querySelector("#status").textContent=d.status;
  const completed=d.events.filter(e=>e.status==="completed").length;
  const progress=Math.round(completed/d.events.length*100);
  document.querySelector("#progress-label").textContent=completed+"/"+d.events.length+" etapas";
  document.querySelector("#progress-bar").style.width=progress+"%";
  const metrics=[["Progresso",progress+"%"],["Custo total",money(d.cost.total_usd)],["Evidências",d.evidence_bundle.length],["Repositórios",d.repositories.length]];
  document.querySelector("#metrics").innerHTML=metrics.map(x=>'<article class="metric"><span>'+escapeHtml(x[0])+'</span><strong>'+escapeHtml(x[1])+'</strong></article>').join("");
  document.querySelector("#workflow").innerHTML=d.events.map(e=>'<li><span class="step-icon">✓</span><div><div class="step-name">'+escapeHtml(e.step)+'</div><div class="step-agent">'+escapeHtml(e.actor)+' · '+escapeHtml(e.status)+'</div></div><span class="step-cost">'+money(e.cost_usd)+'</span></li>').join("");
  document.querySelector("#repositories").innerHTML=d.repositories.map(r=>'<div class="repo"><div><strong>'+escapeHtml(r.component)+'</strong><br><small>'+escapeHtml(r.repository)+'</small></div><span class="status">'+escapeHtml(r.status)+'</span></div>').join("");
  const max=Math.max(...d.events.map(e=>e.cost_usd),.001);
  document.querySelector("#costs").innerHTML=d.events.filter(e=>e.cost_usd>0).map(e=>'<div class="cost-row"><span>'+escapeHtml(e.step)+'</span><span class="bar"><i style="width:'+(e.cost_usd/max*100)+'%"></i></span><b>'+money(e.cost_usd)+'</b></div>').join("");
  document.querySelector("#evidence-count").textContent=d.evidence_bundle.length+" artefatos";
  document.querySelector("#evidence").innerHTML=d.evidence_bundle.map(e=>'<tr><td>'+escapeHtml(e.step)+'</td><td>'+escapeHtml(e.uri)+'</td><td><code>'+escapeHtml(e.sha256.slice(0,16))+'…</code></td></tr>').join("");
}
load().catch(err=>{document.querySelector("#change-title").textContent="Dashboard indisponível";document.querySelector("#change-meta").textContent=err.message;});
