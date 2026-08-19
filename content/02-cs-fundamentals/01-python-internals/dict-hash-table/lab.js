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
    try{ return v.toLowerCase().indexOf('0x')===0 ? BigInt(v) : BigInt(v); }catch(e){ return null; }
  }

  // 06 — mask
  var rm=document.getElementById('rail-mask');
  if(rm){ rm.innerHTML = rail(8, {0:'×4'}, 'f'); }

  // 10 — probe stepper
  var hIn=document.getElementById('ph'), sIn=document.getElementById('ps'),
      pr=document.getElementById('prail'), ps=document.getElementById('psteps');
  function run(){
    var h=parseH(hIn.value); if(h===null){ ps.innerHTML='<div><span>hash không đọc được</span></div>'; return; }
    var size=parseInt(sIn.value,10), n=Math.min(10,size), r=seq(h,size,n), marks={}, rows='';
    r.forEach(function(st){ var idx=Number(st.i); if(marks[idx]===undefined) marks[idx]=st.k; });
    rows += '<div><span>bước</span><span>perturb</span><span>index</span></div>';
    r.forEach(function(st){
      rows += '<div><span>'+st.k+'</span><span>0x'+st.p.toString(16)+'</span><span>'+st.i+'</span></div>';
    });
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

  // 10 — ba key cùng ô đầu
  var pd=document.getElementById('pdiv');
  if(pd){
    var out='';
    [0x0A3,0x2A3,0x4A3].forEach(function(h){
      var r=seq(h,32,6), marks={};
      r.forEach(function(st){ var ix=Number(st.i); if(marks[ix]===undefined) marks[ix]=st.k; });
      out += '<p class="legend" style="margin:16px 0 4px"><span>hash = 0x'+h.toString(16).toUpperCase()
          +' &nbsp;→&nbsp; ô: '+r.map(function(s){return s.i;}).join(' → ')+'</span></p>'
          + '<div class="rail" style="grid-template-columns:repeat(16,minmax(0,1fr))">'+rail(32,marks,'p')+'</div>';
    });
    pd.innerHTML = out;
  }

  // 11 — clustering: linear vs python
  var cl=document.getElementById('clust');
  if(cl){
    function sim(hashes,size,mode){
      var slots=new Array(size).fill(undefined), mask=BigInt(size-1), total=0, mx=0;
      hashes.forEach(function(h,idx){
        var bh=BigInt(h), perturb=bh, i=bh&mask, p=1;
        while(slots[Number(i)]!==undefined){
          p++;
          if(mode==='lin'){ i=(i+1n)&mask; } else { perturb>>=5n; i=(i*5n+perturb+1n)&mask; }
        }
        slots[Number(i)]=idx; total+=p; if(p>mx) mx=p;
      });
      return {slots:slots,total:total,mx:mx};
    }
    var hs=[]; for(var k=0;k<21;k++) hs.push(3+32*k);
    var html='';
    [['lin','Linear probing — i + 1'],['py','Pseudo-random probing — Python']].forEach(function(m){
      var r=sim(hs,32,m[0]), marks={};
      r.slots.forEach(function(v,ix){ if(v!==undefined) marks[ix]=v; });
      html += '<div class="lab" style="margin:14px 0">'
        + '<div style="font-family:var(--display);font-weight:700;font-size:14px;margin-bottom:8px">'+m[1]+'</div>'
        + '<div class="rail" style="grid-template-columns:repeat(16,minmax(0,1fr))">'+rail(32,marks,m[0]==='lin'?'p':'f')+'</div>'
        + '<div class="stat"><u>tổng probe <b>'+r.total+'</b></u><u>trung bình <b>'+(r.total/21).toFixed(1)+'</b></u><u>tệ nhất <b>'+r.mx+' probe</b></u></div>'
        + '</div>';
    });
    cl.innerHTML = html
      + '<p class="legend"><span>21 key có cùng 5 bit thấp (hash = 3 + 32k) chèn vào bảng 32 ô — số trong ô là thứ tự chèn.</span></p>'
      + '<p style="font-size:14.4px;color:var(--muted);margin-top:10px">Linear probing dồn cả 21 key thành một dải liền kề: key cuối phải dò 21 ô. Pseudo-random probing rải chúng ra khắp bảng, tệ nhất chỉ 3 lần dò. Đây là trường hợp xấu dựng riêng cho linear probing — nhưng "nhiều key cùng bit thấp" là chuyện rất thường gặp với key số tăng dần hay có bước nhảy cố định.</p>';
  }

  // 14 — tombstone
  var tb=document.getElementById('tomb');
  if(tb){
    tb.innerHTML =
      '<p class="legend" style="margin:16px 0 4px"><span>A, B, C cùng probe sequence 3 → 5 → 6. Xoá B:</span></p>'
      + '<div class="rail">'
      + '<div class="slot"><i>0</i><u>·</u></div><div class="slot"><i>1</i><u>·</u></div><div class="slot"><i>2</i><u>·</u></div>'
      + '<div class="slot f"><i>3</i><u>A</u></div><div class="slot"><i>4</i><u>·</u></div>'
      + '<div class="slot t"><i>5</i><u>−2</u></div><div class="slot f"><i>6</i><u>C</u></div><div class="slot"><i>7</i><u>·</u></div>'
      + '</div>'
      + '<p class="legend"><span><b style="background:var(--tomb)"></b>DUMMY: không có dữ liệu, nhưng probe vẫn phải đi tiếp qua nó để tới được C ở ô 6.</span></p>'
      + '<p class="legend" style="margin-top:14px"><span>Nếu ô 5 bị ghi EMPTY thay vì DUMMY:</span></p>'
      + '<div class="rail">'
      + '<div class="slot"><i>0</i><u>·</u></div><div class="slot"><i>1</i><u>·</u></div><div class="slot"><i>2</i><u>·</u></div>'
      + '<div class="slot f"><i>3</i><u>A</u></div><div class="slot"><i>4</i><u>·</u></div>'
      + '<div class="slot"><i>5</i><u>·</u></div><div class="slot f"><i>6</i><u>C</u></div><div class="slot"><i>7</i><u>·</u></div>'
      + '</div>'
      + '<p class="legend"><span>tìm C → dừng ở ô 5 vì gặp EMPTY → <b style="background:none;color:var(--tomb);width:auto;height:auto;display:inline;font-weight:600">KeyError, dù C vẫn nằm trong bảng</b></span></p>';
  }
})();
