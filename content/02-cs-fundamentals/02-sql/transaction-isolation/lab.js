(function(){
/* ---------------- lab: hai transaction song song ---------------- */
const TSCEN = {
  dirty: {
    name: "dirty read",
    steps: [
      {t: 1, op: "BEGIN"},
      {t: 1, op: "UPDATE balance = 0 WHERE id=1", note: "chưa commit"},
      {t: 2, op: "BEGIN"},
      {t: 2, op: "SELECT balance WHERE id=1", read: true},
      {t: 1, op: "ROLLBACK", note: "huỷ thay đổi"}
    ],
    /* T2 đọc thấy gì */
    sees: {RU: "0 — dữ liệu chưa commit", RC: "100", RR: "100", S: "100"},
    bad: {RU: false, RC: false, RR: false, S: false},
    verdict: {
      RU: "PostgreSQL KHÔNG hỗ trợ READ UNCOMMITTED — nó chạy như READ COMMITTED, nên T2 vẫn đọc 100. Dirty read bất khả thi nhờ MVCC.",
      RC: "T2 đọc 100 — chỉ thấy dữ liệu đã commit. Dirty read được chặn.",
      RR: "T2 đọc 100 từ snapshot của nó. An toàn.",
      S: "T2 đọc 100. An toàn."
    }
  },
  nonrep: {
    name: "non-repeatable read",
    steps: [
      {t: 2, op: "BEGIN"},
      {t: 2, op: "SELECT balance WHERE id=1", read: true, first: true},
      {t: 1, op: "UPDATE balance = 50 WHERE id=1; COMMIT"},
      {t: 2, op: "SELECT balance WHERE id=1", read: true},
      {t: 2, op: "COMMIT"}
    ],
    sees: {RU: "lần 1: 100 · lần 2: 50", RC: "lần 1: 100 · lần 2: 50",
           RR: "lần 1: 100 · lần 2: 100", S: "lần 1: 100 · lần 2: 100"},
    bad: {RU: true, RC: true, RR: false, S: false},
    verdict: {
      RU: "Hai lần đọc cùng một dòng cho hai giá trị khác nhau — dị thường xảy ra.",
      RC: "Snapshot được cấp MỚI cho mỗi câu lệnh, nên lần đọc thứ hai thấy giá trị mới. Đây là hành vi mặc định của PostgreSQL.",
      RR: "Một snapshot cho cả transaction → hai lần đọc luôn giống nhau. Được chặn.",
      S: "Được chặn, như REPEATABLE READ."
    }
  },
  phantom: {
    name: "phantom read",
    steps: [
      {t: 2, op: "BEGIN"},
      {t: 2, op: "SELECT COUNT(*) WHERE status='active'", read: true, first: true},
      {t: 1, op: "INSERT (status='active'); COMMIT"},
      {t: 2, op: "SELECT COUNT(*) WHERE status='active'", read: true},
      {t: 2, op: "COMMIT"}
    ],
    sees: {RU: "lần 1: 10 · lần 2: 11", RC: "lần 1: 10 · lần 2: 11",
           RR: "lần 1: 10 · lần 2: 10", S: "lần 1: 10 · lần 2: 10"},
    bad: {RU: true, RC: true, RR: false, S: false},
    verdict: {
      RU: "Dòng mới xuất hiện giữa hai lần đếm — phantom.",
      RC: "Phantom xảy ra, vì mỗi câu lệnh có snapshot riêng.",
      RR: "PostgreSQL chặn cả phantom ở mức này — khác với yêu cầu tối thiểu của chuẩn SQL, vì nó dùng snapshot isolation.",
      S: "Được chặn."
    }
  },
  lost: {
    name: "lost update",
    steps: [
      {t: 1, op: "BEGIN; SELECT stock WHERE id=1", read: true, first: true},
      {t: 2, op: "BEGIN; SELECT stock WHERE id=1", read: true},
      {t: 1, op: "UPDATE stock = 9; COMMIT"},
      {t: 2, op: "UPDATE stock = 9", note: "dựa trên giá trị đã đọc"},
      {t: 2, op: "COMMIT"}
    ],
    sees: {RU: "cả hai đọc 10", RC: "cả hai đọc 10", RR: "cả hai đọc 10", S: "cả hai đọc 10"},
    bad: {RU: true, RC: true, RR: false, S: false},
    verdict: {
      RU: "stock cuối cùng = 9 thay vì 8 — MẤT một lần trừ kho.",
      RC: "stock cuối cùng = 9 thay vì 8 — lost update xảy ra ngay ở mức MẶC ĐỊNH. Chữa bằng UPDATE nguyên tử, FOR UPDATE, hoặc cột version.",
      RR: "T2 bị huỷ với lỗi 40001 serialization_failure. Dữ liệu an toàn, nhưng ứng dụng BẮT BUỘC phải thử lại.",
      S: "T2 bị huỷ với lỗi 40001. Ứng dụng phải thử lại."
    }
  }
};
let TSTEP3 = 0, TTIMER3 = null;

function tRender3(){
  const sc = TSCEN[document.getElementById("tscen").value];
  const lv = document.getElementById("tlevel").value;
  const done = TSTEP3 >= sc.steps.length;

  let h = `<div class="hm"><table style="min-width:480px"><tr>
    <th style="width:40px"></th><th style="color:var(--filled)">T1</th><th style="color:var(--ok)">T2</th></tr>`;
  sc.steps.forEach((s, i) => {
    const active = i === TSTEP3 - 1;
    const shown = i < TSTEP3;
    const cell = v => {
      if(!v) return `<td></td>`;
      const bg = active ? "var(--probe)" : (shown ? "var(--panel)" : "transparent");
      const fg = active ? "#0E141B" : (shown ? "var(--text)" : "var(--rule)");
      return `<td><div class="cell" style="background:${bg};color:${fg};text-align:left;
        font-weight:${active?600:400};padding:6px 9px">${s.op}${s.note ? ` <span style="opacity:.7">— ${s.note}</span>` : ""}</div></td>`;
    };
    h += `<tr><td class="rl">${i+1}</td>${cell(s.t === 1)}${cell(s.t === 2)}</tr>`;
  });
  h += `</table></div>`;
  document.getElementById("tview3").innerHTML = h;

  const isBad = sc.bad[lv];
  const col = isBad ? "var(--tomb)" : "var(--ok)";
  document.getElementById("tverdict").innerHTML = done
    ? `<div class="note" style="border-left-color:${col};margin:0">
         <h4 style="color:${col}">${sc.name} · ${{RU:"READ UNCOMMITTED",RC:"READ COMMITTED",RR:"REPEATABLE READ",S:"SERIALIZABLE"}[lv]}</h4>
         <p style="margin:0 0 6px;font-family:var(--mono);font-size:12.5px">T2 đọc được: ${sc.sees[lv]}</p>
         ${sc.verdict[lv]}</div>`
    : `<p class="legend"><span>bấm "Bước tiếp" để chạy hết rồi xem kết luận</span></p>`;
}
function tStep3(){
  const sc = TSCEN[document.getElementById("tscen").value];
  if(TSTEP3 < sc.steps.length){ TSTEP3++; tRender3(); }
  else tStop3();
}
function tReset3(){ tStop3(); TSTEP3 = 0; tRender3(); }
function tStop3(){ if(TTIMER3){ clearInterval(TTIMER3); TTIMER3 = null;
  document.getElementById("tauto3").textContent = "Tự chạy"; } }

document.getElementById("tstep3").addEventListener("click", tStep3);
document.getElementById("trst3").addEventListener("click", tReset3);
["tscen","tlevel"].forEach(id => document.getElementById(id).addEventListener("change", tReset3));
document.getElementById("tauto3").addEventListener("click", () => {
  if(TTIMER3) return tStop3();
  const sc = TSCEN[document.getElementById("tscen").value];
  if(TSTEP3 >= sc.steps.length) tReset3();
  document.getElementById("tauto3").textContent = "Dừng";
  TTIMER3 = setInterval(tStep3, 900);
});
tReset3();
})();
