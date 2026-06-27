// assets/charts.js — ECharts 雷达图 + 平台对比柱状图
(function() {
  var style = getComputedStyle(document.documentElement);
  var accent = style.getPropertyValue('--accent').trim();
  var accent2 = style.getPropertyValue('--accent2').trim();
  var ink = style.getPropertyValue('--ink').trim();
  var muted = style.getPropertyValue('--muted').trim();
  var rule = style.getPropertyValue('--rule').trim();
  var bg2 = style.getPropertyValue('--bg2').trim();
  var red = style.getPropertyValue('--red').trim();
  var green = style.getPropertyValue('--green').trim();
  var orange = style.getPropertyValue('--orange').trim();

  // ===== Radar Chart (Updated) =====
  var radarEl = document.getElementById('chart-radar');
  if (radarEl) {
    var radar = echarts.init(radarEl, null, { renderer: 'svg' });
    radar.setOption({
      animation: false,
      legend: {
        data: ['当前得分（更新）', '满分基准'],
        bottom: 0,
        textStyle: { color: muted, fontSize: 12 },
        itemWidth: 12, itemHeight: 12
      },
      radar: {
        center: ['50%', '48%'],
        radius: '62%',
        indicator: [
          { name: '痛点明确度\n(15)', max: 15 },
          { name: '产品可演示性\n(12)', max: 12 },
          { name: '差异化程度\n(12)', max: 12 },
          { name: '平台匹配度\n(16)', max: 16 },
          { name: '团队可信度\n(13)', max: 13 },
          { name: '供应链就绪\n(13)', max: 13 },
          { name: '定价竞争力\n(10)', max: 10 },
          { name: '社群/预热\n(5)', max: 5 },
          { name: '冷启动路径\n(3)', max: 3 },
          { name: '合规与交付\n(5)', max: 5 },
          { name: '商业可持续\n(3)', max: 3 },
          { name: '情绪价值\n(3)', max: 3 }
        ],
        shape: 'circle',
        splitNumber: 3,
        axisName: { color: muted, fontSize: 10, lineHeight: 14 },
        splitLine: { lineStyle: { color: rule } },
        splitArea: { show: false },
        axisLine: { lineStyle: { color: rule } }
      },
      series: [{
        type: 'radar',
        data: [
          {
            value: [10, 8, 11, 8, 5, 3, 8, 2, 2, 4, 3, 3],
            name: '当前得分',
            areaStyle: { color: accent + '30' },
            lineStyle: { color: accent, width: 2 },
            itemStyle: { color: accent },
            symbol: 'circle', symbolSize: 5
          },
          {
            value: [15, 12, 12, 16, 13, 13, 10, 5, 3, 5, 3, 3],
            name: '满分基准',
            lineStyle: { color: muted, width: 1, type: 'dashed' },
            itemStyle: { color: muted },
            areaStyle: { color: 'transparent' },
            symbol: 'none'
          }
        ],
        tooltip: {
          appendToBody: true,
          backgroundColor: '#1a2038',
          borderColor: rule,
          textStyle: { color: ink, fontSize: 12 }
        }
      }]
    });
    window.addEventListener('resize', function() { radar.resize(); });
  }

  // ===== Platform Bar Chart (Updated) =====
  var platformEl = document.getElementById('chart-platform');
  if (platformEl) {
    var bar = echarts.init(platformEl, null, { renderer: 'svg' });
    bar.setOption({
      animation: false,
      grid: { left: 90, right: 30, top: 20, bottom: 40 },
      xAxis: {
        type: 'value', max: 100,
        axisLine: { lineStyle: { color: rule } },
        axisLabel: { color: muted, fontSize: 11 },
        splitLine: { lineStyle: { color: rule, type: 'dashed' } }
      },
      yAxis: {
        type: 'category',
        data: ['flyingV', 'Kickstarter', '嘖嘖 zeczec', 'Makuake', 'Indiegogo'],
        axisLine: { lineStyle: { color: rule } },
        axisLabel: { color: ink, fontSize: 12 },
        axisTick: { show: false }
      },
      series: [{
        type: 'bar',
        data: [
          { value: 20, itemStyle: { color: red } },
          { value: 35, itemStyle: { color: '#fbbf24' } },
          { value: 45, itemStyle: { color: orange } },
          { value: 50, itemStyle: { color: orange } },
          { value: 55, itemStyle: { color: green } }
        ],
        barWidth: 22,
        label: {
          show: true, position: 'right',
          formatter: '{c}分', color: muted, fontSize: 11
        },
        itemStyle: { borderRadius: [0, 4, 4, 0] }
      }],
      tooltip: {
        appendToBody: true,
        backgroundColor: '#1a2038',
        borderColor: rule,
        textStyle: { color: ink, fontSize: 12 },
        formatter: function(p) { return p.name + ': ' + p.value + '/100'; }
      }
    });
    window.addEventListener('resize', function() { bar.resize(); });
  }
})();
