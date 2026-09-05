(function(){

  var M64 = (1n<<64n)-1n;
  function seq(hash, size, n){
    var mask = BigInt(size-1), h = BigInt(hash) & M64;
    var perturb = h, i = h & mask, out=[{k:0,p:h,i:i}];
    for(var k=1;k<n;k++){ perturb >>= 5n; i = (i*5n + perturb + 1n) & mask; out.push({k:k,p:perturb,i:i}); }
    return out;
  }
  function rail(size, marks, cls){
    var h='';
    for(var s=0;s<size;s++){
      var m = marks[s];
      h += '<div class="slot'+(m===undefined?'':' '+cls)+'"><i>'+s+'</i><u>'+(m===undefined?'·':m)+'</u></div>';
    }
    return h;
  }
  function parseH(v){
    v=(v||'').trim();
    try{ return BigInt(v); }catch(e){ return null; }
  }

  // 05 — probe stepper
  var hIn=document.getElementById('ph'), sIn=document.getElementById('ps'),
      pr=document.getElementById('prail'), ps=document.getElementById('psteps');
  function run(){
    var h=parseH(hIn.value); if(h===null){ ps.innerHTML='<div><span>hash không đọc được</span></div>'; return; }
    var size=parseInt(sIn.value,10), n=Math.min(6,size), r=seq(h,size,n), marks={}, rows='';
    r.forEach(function(st){ var idx=Number(st.i); if(marks[idx]===undefined) marks[idx]=st.k; });
    rows += '<div><span>bước</span><span>slot được thăm</span></div>';
    r.forEach(function(st){ rows += '<div><span>'+st.k+'</span><span>'+st.i+'</span></div>'; });
    pr.style.gridTemplateColumns = 'repeat('+Math.min(16,size)+',minmax(0,1fr))';
    pr.innerHTML = rail(size, marks, 'p');
    ps.innerHTML = rows;
  }
  if(hIn){
    document.getElementById('pgo').addEventListener('click', run);
    hIn.addEventListener('keydown', function(e){ if(e.key==='Enter') run(); });
    sIn.addEventListener('change', run);
    document.getElementById('prnd').addEventListener('click', function(){
      var v=0n; for(var i=0;i<8;i++){ v=(v<<8n)|BigInt(Math.floor(Math.random()*256)); }
      hIn.value='0x'+v.toString(16); run();
    });
    run();
  }

  // 06 — tombstone
  var tb=document.getElementById('tomb');
  if(tb){
    tb.innerHTML =
      '<p class="legend" style="margin:16px 0 4px"><span>A, B, C cùng probe sequence 3 → 5 → 6. Xoá B:</span></p>'
      + '<div class="rail">'
      + '<div class="slot"><i>0</i><u>·</u></div><div class="slot"><i>1</i><u>·</u></div><div class="slot"><i>2</i><u>·</u></div>'
      + '<div class="slot f"><i>3</i><u>A</u></div><div class="slot"><i>4</i><u>·</u></div>'
      + '<div class="slot t"><i>5</i><u>−2</u></div><div class="slot f"><i>6</i><u>C</u></div><div class="slot"><i>7</i><u>·</u></div>'
      + '</div>'
      + '<p class="legend"><span><b style="background:var(--tomb)"></b>DUMMY: không có dữ liệu, nhưng probe vẫn phải đi tiếp qua nó để tới được C ở slot 6.</span></p>'
      + '<p class="legend" style="margin-top:14px"><span>Nếu slot 5 bị ghi EMPTY thay vì DUMMY:</span></p>'
      + '<div class="rail">'
      + '<div class="slot"><i>0</i><u>·</u></div><div class="slot"><i>1</i><u>·</u></div><div class="slot"><i>2</i><u>·</u></div>'
      + '<div class="slot f"><i>3</i><u>A</u></div><div class="slot"><i>4</i><u>·</u></div>'
      + '<div class="slot"><i>5</i><u>·</u></div><div class="slot f"><i>6</i><u>C</u></div><div class="slot"><i>7</i><u>·</u></div>'
      + '</div>'
      + '<p class="legend"><span>tìm C → dừng ở slot 5 vì gặp EMPTY → <b style="background:none;color:var(--tomb);width:auto;height:auto;display:inline;font-weight:600">KeyError, dù C vẫn nằm trong bảng</b></span></p>';
  }
})();
