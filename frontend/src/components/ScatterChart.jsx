import React, { useMemo } from 'react';
import ReactECharts from 'echarts-for-react';
import { Empty, Card } from 'antd';
import { useTranslation } from 'react-i18next';

const ScatterChart = ({ data, onPointClick }) => {
  const { t, i18n } = useTranslation();

  // [ZH] useMemo 必须在所有条件渲染之前调用，以遵守 React Hooks 规则
  // [JA] React Hooks のルールに従い、すべての条件付きレンダリングより前に useMemo を呼び出す
  // [EN] useMemo must be called before any conditional return to comply with React Hooks rules
  //
  // [ZH] i18n.language 加入依赖数组，确保切换语言后图表文本同步更新
  // [JA] i18n.language を依存配列に追加し、言語切替後にグラフテキストが同期更新されるようにする
  // [EN] Include i18n.language in deps so chart text re-renders when the language changes
  const option = useMemo(() => {
    if (!data || data.length === 0) return {};

    const uniqueTags  = Array.from(new Set(data.map(item => item.tag)));
    const echartsData = data.map(item => [item.time, uniqueTags.indexOf(item.tag), item.detail]);

    return {
      tooltip: {
        trigger: 'item',
        formatter: (params) => {
          const time   = params.value[0];
          const tag    = uniqueTags[params.value[1]];
          const detail = params.value[2];
          return `<strong>${tag}</strong><br/>${t('chart_tooltip_time')}: ${time} ${t('chart_tooltip_seconds')}<br/>${t('chart_tooltip_detail')}: ${detail}`;
        },
      },
      grid:     { left: '3%', right: '7%', bottom: '10%', containLabel: true },
      dataZoom: [{ type: 'slider', xAxisIndex: [0], bottom: 0 }],
      xAxis: {
        name: t('chart_x_axis'),
        type: 'value',
        splitLine: { show: false },
      },
      yAxis: {
        name: t('chart_y_axis'),
        type: 'category',
        data: uniqueTags,
        splitLine: { show: true, lineStyle: { type: 'dashed', color: '#e8e8e8' } },
      },
      series: [{
        name: t('chart_series'),
        type: 'scatter',
        symbolSize: 16,
        data: echartsData,
        itemStyle: { color: '#1890ff', opacity: 0.8, shadowBlur: 10, shadowColor: 'rgba(24, 144, 255, 0.5)' },
      }],
    };
  }, [data, i18n.language, t]);

  // [ZH] 所有 Hooks 调用完毕后再做条件渲染判断
  // [JA] すべての Hooks 呼び出し後に条件付きレンダリングを行う
  // [EN] Perform the conditional render check only after all Hooks have been called
  if (!data || data.length === 0) {
    return (
      <Card style={{ height: '450px', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <Empty description={t('chart_empty')} />
      </Card>
    );
  }

  const onEvents = {
    click: (params) => {
      if (onPointClick && params.value !== undefined) {
        onPointClick(params.value[0]);
      }
    },
  };

  return (
    <Card title={t('chart_title')} size="small">
      <ReactECharts option={option} onEvents={onEvents} style={{ height: '400px', width: '100%' }} />
    </Card>
  );
};

export default ScatterChart;
