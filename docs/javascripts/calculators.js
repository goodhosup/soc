/* SoC Handbook 계산기 — docs/reference/calculators.md
 * 공식은 tools/soc_numbers.py와 같다. 페이지에 해당 요소가 있을 때만 동작한다.
 *   dram_bw_gbs, llm_tokens_per_s, dyn_power_ratio, energy_ratio,
 *   dies_per_wafer, poisson_yield, npu_peak_tops/gpu_tflops, pixel_rate_gbps, frame_mb,
 *   battery_wh, runtime_h
 */
(function () {
  "use strict";

  var $ = function (id) { return document.getElementById(id); };
  var num = function (id) {
    var v = parseFloat($(id).value);
    return isFinite(v) ? v : NaN;
  };
  var fmt = function (x, d) {
    if (!isFinite(x)) return "—";
    return x.toLocaleString("ko-KR", { minimumFractionDigits: d, maximumFractionDigits: d });
  };
  var set = function (id, text) { var el = $(id); if (el) el.textContent = text; };

  // ---------------------------------------------------------------- soc_numbers.py와 같은 식
  function dramBwGbs(mts, busBits) { return mts * 1e6 * busBits / 8 / 1e9; }
  function llmTokensPerS(bwGbs, paramsB, bits) { return bwGbs / (paramsB * bits / 8); }
  function dynPowerRatio(f0, v0, f1, v1) { return Math.pow(v1 / v0, 2) * (f1 / f0); }
  function energyRatio(f0, v0, f1, v1) { return dynPowerRatio(f0, v0, f1, v1) * (f0 / f1); }
  function diesPerWafer(area, waferMm) {
    var r = waferMm / 2;
    return Math.PI * r * r / area - Math.PI * waferMm / Math.sqrt(2 * area);
  }
  function poissonYield(area, d0) { return Math.exp(-(area / 100) * d0); }
  function peakTops(units, ghz, opsPerUnit, rate) { return units * opsPerUnit * ghz * rate / 1000; }
  function pixelRateGbps(w, h, bits, fps) { return w * h * bits * fps / 1e9; }
  function frameMb(w, h, bits) { return w * h * bits / 8 / 1e6; }
  function batteryWh(mah, v) { return mah * v / 1000; }

  // 입력 id 목록에 input 이벤트를 걸고 한 번 계산한다.
  function bind(ids, fn) {
    for (var i = 0; i < ids.length; i++) {
      if (!$(ids[i])) return; // 요소가 없으면 이 계산기는 건너뜀
    }
    ids.forEach(function (id) {
      $(id).addEventListener("input", fn);
      $(id).addEventListener("change", fn);
    });
    fn();
  }

  function init() {
    // (1) LPDDR 피크 대역폭
    bind(["bw-rate", "bw-bus"], function () {
      var bw = dramBwGbs(num("bw-rate"), num("bw-bus"));
      set("bw-out", fmt(bw, 1));
      set("bw-ch", fmt(num("bw-bus") / 16, 0));
    });
    var preset = $("bw-preset");
    if (preset && $("bw-rate")) {
      preset.addEventListener("change", function () {
        if (preset.value) {
          $("bw-rate").value = preset.value;
          $("bw-rate").dispatchEvent(new Event("input"));
        }
      });
    }

    // (2) LLM 생성 토큰 속도 상한
    bind(["llm-rate", "llm-bus", "llm-params", "llm-bits", "llm-eff"], function () {
      var bw = dramBwGbs(num("llm-rate"), num("llm-bus"));
      var model = num("llm-params") * num("llm-bits") / 8;
      var tps = llmTokensPerS(bw, num("llm-params"), num("llm-bits"));
      set("llm-bw", fmt(bw, 1));
      set("llm-model", fmt(model, 2));
      set("llm-out", fmt(tps, 1));
      set("llm-real", fmt(tps * num("llm-eff") / 100, 1));
    });

    // (3) DVFS 동적 전력과 에너지
    bind(["dv-f0", "dv-v0", "dv-f1", "dv-v1"], function () {
      var f0 = num("dv-f0"), v0 = num("dv-v0"), f1 = num("dv-f1"), v1 = num("dv-v1");
      var p = dynPowerRatio(f0, v0, f1, v1), e = energyRatio(f0, v0, f1, v1);
      set("dv-p", fmt(p, 3));
      set("dv-e", fmt(e, 3));
      set("dv-t", fmt(f0 / f1, 2));
      set("dv-psave", fmt((1 - p) * 100, 1));
      set("dv-esave", fmt((1 - e) * 100, 1));
    });

    // (4) 웨이퍼당 다이 수와 수율
    bind(["dw-area", "dw-wafer", "dw-d0"], function () {
      var a = num("dw-area"), w = num("dw-wafer"), d0 = num("dw-d0");
      var n = diesPerWafer(a, w), y = poissonYield(a, d0);
      set("dw-n", fmt(Math.round(n), 0));
      set("dw-y", fmt(y * 100, 1));
      set("dw-good", fmt(Math.round(n * y), 0));
    });

    // (5) NPU·GPU 피크 연산 성능
    bind(["tp-units", "tp-ghz", "tp-rate", "tp-util", "tp-watt"], function () {
      var peak = peakTops(num("tp-units"), num("tp-ghz"), 2, num("tp-rate"));
      set("tp-out", fmt(peak, 2));
      set("tp-eff", fmt(peak * num("tp-util") / 100, 2));
      set("tp-pw", fmt(peak / num("tp-watt"), 2));
    });

    // (6) 카메라·디스플레이 raw 데이터 속도
    bind(["px-w", "px-h", "px-bits", "px-fps"], function () {
      var w = num("px-w"), h = num("px-h"), b = num("px-bits"), f = num("px-fps");
      set("px-out", fmt(pixelRateGbps(w, h, b, f), 2));
      set("px-mp", fmt(w * h / 1e6, 1));
      set("px-frame", fmt(frameMb(w, h, b), 1));
      set("px-gbs", fmt(pixelRateGbps(w, h, b, f) / 8, 2));
    });
    var pxPreset = $("px-preset");
    if (pxPreset && $("px-w")) {
      pxPreset.addEventListener("change", function () {
        var v = pxPreset.value.split(",");
        if (v.length === 4) {
          ["px-w", "px-h", "px-bits", "px-fps"].forEach(function (id, i) { $(id).value = v[i]; });
          $("px-w").dispatchEvent(new Event("input"));
        }
      });
    }

    // (7) 배터리 사용 시간
    bind(["bat-mah", "bat-v", "bat-w"], function () {
      var wh = batteryWh(num("bat-mah"), num("bat-v"));
      var h = wh / num("bat-w");
      set("bat-wh", fmt(wh, 2));
      set("bat-h", fmt(h, 1));
      set("bat-d", fmt(h / 24, 1));
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
