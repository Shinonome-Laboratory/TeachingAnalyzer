import React, { useState } from 'react';
import { Layout, Typography, Divider, theme, Tabs, Card, Empty, Button, Select, ConfigProvider } from 'antd';
import { RobotOutlined, DownloadOutlined, GlobalOutlined } from '@ant-design/icons';
import { useTranslation } from 'react-i18next';
import enUS from 'antd/locale/en_US';
import zhCN from 'antd/locale/zh_CN';
import jaJP from 'antd/locale/ja_JP';

import VideoUploader from './components/VideoUploader';
import ScatterChart from './components/ScatterChart';
import VideoPlayer from './components/VideoPlayer';
import EngineConfig from './components/EngineConfig';

const { Header, Sider, Content } = Layout;
const { Title, Text } = Typography;

// [ZH] 语言代码到 Ant Design 语言包的映射
// [JA] 言語コードから Ant Design ロケールパッケージへのマッピング
// [EN] Map language codes to Ant Design locale packages
const antdLocaleMap = { en: enUS, zh: zhCN, ja: jaJP };

const App = () => {
  const { token: { colorBgContainer, borderRadiusLG } } = theme.useToken();
  const { t, i18n } = useTranslation();

  // [ZH] 全局状态：分析结果、逐字稿、视频 URL、当前播放时间
  // [JA] グローバル状態：分析結果・文字起こし・動画 URL・現在の再生時刻
  // [EN] Global state: analysis result, transcript, video URL, current playback time
  const [analysisData, setAnalysisData] = useState(null);
  const [transcription, setTranscription] = useState('');
  const [videoUrl, setVideoUrl] = useState(null);
  const [currentTime, setCurrentTime] = useState(0);

  // [ZH] 引擎配置状态（模型选择与温度参数）
  // [JA] エンジン設定状態（モデル選択と temperature パラメータ）
  // [EN] Engine config state (model selection and temperature parameter)
  const [engineConfig, setEngineConfig] = useState({
    whisperModel: 'base',
    ollamaModel: 'llama3.1:8b', // [ZH] 改为本地已部署的模型名 | [JA] ローカルにデプロイ済みのモデル名に変更 | [EN] Change to a model deployed locally
    temperature: 0.3,
  });

  // [ZH] 上传成功后的回调：将后端返回的数据同步到全局状态
  // [JA] アップロード成功時のコールバック：バックエンドの返却データをグローバル状態に反映する
  // [EN] Callback on upload success: sync backend response data into global state
  const handleUploadSuccess = (data, localUrl) => {
    setVideoUrl(localUrl);
    setAnalysisData(data.analysis);
    setTranscription(data.transcription);
  };

  // [ZH] 将分析数据导出为 CSV 文件并触发浏览器下载
  // [JA] 分析データを CSV ファイルにエクスポートし、ブラウザのダウンロードをトリガーする
  // [EN] Export analysis data as a CSV file and trigger a browser download
  const handleDownloadCSV = () => {
    if (!analysisData || analysisData.length === 0) return;

    let csvContent = 'Times,Teaching Action,Detail Description\n';
    analysisData.forEach(item => {
      const time   = item.time;
      const tag    = `"${(item.tag    || '').replace(/"/g, '""')}"`;
      const detail = `"${(item.detail || '').replace(/"/g, '""')}"`;
      csvContent += `${time},${tag},${detail}\n`;
    });

    // [ZH] 添加 UTF-8 BOM，解决 Windows Excel 打开时的中文乱码
    // [JA] UTF-8 BOM を付与し、Windows Excel での文字化けを防ぐ
    // [EN] Prepend UTF-8 BOM to fix garbled characters when opened in Windows Excel
    const blob = new Blob(['﻿' + csvContent], { type: 'text/csv;charset=utf-8;' });
    const url  = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href     = url;
    link.download = 'Teaching Behavior Sequence.csv';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    // [ZH] 根据当前语言动态切换 Ant Design 组件语言包（日期选择器、表格分页等）
    // [JA] 現在の言語に応じて Ant Design コンポーネントのロケールを動的に切り替える
    // [EN] Dynamically switch the Ant Design component locale based on the current language
    <ConfigProvider locale={antdLocaleMap[i18n.language] ?? enUS}>
      <Layout style={{ minHeight: '100vh' }}>

        {/* [ZH] 侧边栏：标题 + 引擎配置 | [JA] サイドバー：タイトル＋エンジン設定 | [EN] Sidebar: title + engine config */}
        <Sider width={320} theme="light" style={{ padding: '20px', borderRight: '1px solid #f0f0f0' }}>
          <Title level={4}><RobotOutlined style={{ marginRight: 8 }} />{t('sidebar_title')}</Title>
          <Divider />
          <EngineConfig config={engineConfig} setConfig={setEngineConfig} />
        </Sider>

        <Layout>
          {/* [ZH] 顶部导航：左侧标题，右侧语言切换器 | [JA] ヘッダー：左タイトル、右言語切替 | [EN] Header: title on left, language switcher on right */}
          <Header style={{
            padding: '0 24px',
            background: colorBgContainer,
            borderBottom: '1px solid #f0f0f0',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            height: 'auto',
            lineHeight: 'normal',
            paddingTop: '10px',
            paddingBottom: '10px',
          }}>
            <div>
              <Title level={3} style={{ margin: 0 }}>{t('app_title')}</Title>
              <Text type="secondary">{t('app_subtitle')}</Text>
            </div>

            {/* [ZH] 语言切换器（右上角） | [JA] 言語切替器（右上） | [EN] Language switcher (top-right) */}
            <Select
              value={i18n.language}
              onChange={(lng) => i18n.changeLanguage(lng)}
              style={{ width: 130 }}
              suffixIcon={<GlobalOutlined />}
              options={[
                { value: 'en', label: '🇺🇸 English' },
                { value: 'zh', label: '🇨🇳 中文' },
                { value: 'ja', label: '🇯🇵 日本語' },
              ]}
            />
          </Header>

          <Content style={{ margin: '24px 16px', padding: 24, background: colorBgContainer, borderRadius: borderRadiusLG }}>

            {/* [ZH] 上传区 | [JA] アップロードエリア | [EN] Upload area */}
            <div style={{ marginBottom: '32px' }}>
              <VideoUploader onAllDataReady={handleUploadSuccess} engineConfig={engineConfig} />
            </div>

            {/* [ZH] 交互区：视频播放器 + 散点图 | [JA] インタラクションエリア：動画＋散布図 | [EN] Interaction: video player + scatter chart */}
            <div style={{ display: 'flex', gap: '24px', marginBottom: '24px' }}>
              <div style={{ flex: 1 }}>
                <VideoPlayer videoUrl={videoUrl} currentTime={currentTime} />
              </div>
              <div style={{ flex: 1 }}>
                <ScatterChart data={analysisData} onPointClick={setCurrentTime} />
              </div>
            </div>

            {/* [ZH] 详情区：逐字稿 + AI 报告 | [JA] 詳細：文字起こし＋AI レポート | [EN] Detail: transcript + AI report */}
            <Card size="small" title={t('results_title')}>
              {transcription ? (
                <Tabs defaultActiveKey="1" items={[
                  {
                    key: '1',
                    label: t('tab_transcription'),
                    children: (
                      <div style={{
                        maxHeight: '400px', overflowY: 'auto', padding: '15px',
                        background: '#f9f9f9', borderRadius: '4px',
                        whiteSpace: 'pre-wrap', fontFamily: 'monospace',
                        lineHeight: '1.8', color: '#333', border: '1px solid #eee',
                      }}>
                        {transcription}
                      </div>
                    ),
                  },
                  {
                    key: '2',
                    label: t('tab_analysis'),
                    children: (
                      <div style={{ padding: '10px' }}>
                        {/* [ZH] 标签左对齐，下载按钮右对齐 | [JA] タグ左、ダウンロード右 | [EN] Tag left, download button right */}
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                          <Text strong>{t('behavior_tags')}</Text>
                          <Button type="primary" icon={<DownloadOutlined />} onClick={handleDownloadCSV} size="small">
                            {t('btn_download_csv')}
                          </Button>
                        </div>
                        <ul>
                          {analysisData?.map((item, index) => (
                            <li key={index}>[{item.time}s] {item.tag}: {item.detail}</li>
                          ))}
                        </ul>
                      </div>
                    ),
                  },
                ]} />
              ) : (
                <Empty description={t('empty_waiting')} />
              )}
            </Card>

          </Content>
        </Layout>
      </Layout>
    </ConfigProvider>
  );
};

export default App;
