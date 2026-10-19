'use strict';
const mission = JSON.parse(document.getElementById('mission-data').textContent);
const day = document.getElementById('day');
function updateDay(){
  const index=Number(day.value)-1;
  const a=mission.modern[index], b=mission.legacy[index];
  document.getElementById('dayValue').textContent=String(a.day).padStart(2,'0');
  document.getElementById('hours').textContent=`${a.day*24} hours into the flight`;
  for(const [name,value] of [['modern',a.km],['legacy',b.km]]){
    document.getElementById(name+'Distance').innerHTML=value.toLocaleString('en-US')+' <small>km</small>';
    document.getElementById(name+'Bar').style.width=(a.day/5*100)+'%';
  }
  document.getElementById('comparison').textContent=a.km===b.km?`✓ Exact match on day ${a.day}`:'Outputs differ';
}
day.addEventListener('input',updateDay);
updateDay();
