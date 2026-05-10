import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

// [ZH] 内联定义三语翻译资源，避免额外的网络请求
// [JA] 三言語の翻訳リソースをインラインで定義し、追加のネットワークリクエストを不要にする
// [EN] Define trilingual translation resources inline to avoid extra network requests
const resources = {
  en: {
    translation: {
      // App shell
      app_title:    'Teaching Behavior Analysis System',
      app_subtitle: 'Self-supervised teaching behavior mining based on local LLMs',
      sidebar_title: 'Settings Panel',
      lang_switch:  'Language',

      // Analysis results section
      results_title:     'Analysis Results',
      tab_transcription: 'Transcription',
      tab_analysis:      'AI Deep Analysis',
      behavior_tags:     'Teaching Behavior Tags:',
      btn_download_csv:  'Download CSV',
      empty_waiting:     'Waiting for analysis...',

      // VideoUploader
      upload_spinning:     'Separating audio, recognizing speech, and running LLM analysis. This may take several minutes, please wait...',
      upload_drag_text:    'Click or drag the teaching video here for automatic analysis',
      upload_hint:         'Supports .mp4, .mov, .avi and other common formats. Speech recognition (Whisper) and action sequence extraction (Ollama) run automatically.',
      upload_success:      '{{name}} analysis complete!',
      upload_error_type:   'Only video files are accepted!',
      upload_error_size:   'Video must be smaller than 500 MB!',
      upload_error_failed: 'Analysis failed',
      upload_error_detail: 'Upload or analysis failed. Please check the backend service log.',

      // EngineConfig
      engine_title:        'Engine Management',
      engine_stt_label:    'Speech Recognition Model (Whisper)',
      engine_tiny:         'Tiny — Fastest, lower precision',
      engine_base:         'Base — Default balance',
      engine_small:        'Small — Higher precision, more memory',
      engine_medium:       'Medium — High precision',
      engine_llm_label:    'Large Language Model (Ollama)',
      engine_temp_label:   'Creativity (Temperature)',
      engine_temp_strict:  'Strict',
      engine_temp_balanced:'Balanced',
      engine_temp_creative:'Creative',
      engine_tip:          'Higher temperature makes analysis more creative; lower temperature keeps it more consistent.',

      // VideoPlayer
      player_empty: 'No video yet. Please upload one first.',
      player_title: 'Teaching Video',

      // ScatterChart
      chart_empty:           'No analysis data yet. Please upload a video first.',
      chart_title:           'Action Sequence Timeline (Click points to jump to video)',
      chart_x_axis:          'Time (seconds)',
      chart_y_axis:          'Teaching Behavior',
      chart_series:          'Teaching Actions',
      chart_tooltip_time:    'Time',
      chart_tooltip_detail:  'Detail',
      chart_tooltip_seconds: 'seconds',
    },
  },

  zh: {
    translation: {
      app_title:    '教学行为分析系统',
      app_subtitle: '基于本地大模型的自监督教学行为挖掘与分析',
      sidebar_title: '设置面板',
      lang_switch:  '语言',

      results_title:     '分析结果',
      tab_transcription: '语音逐字稿',
      tab_analysis:      'AI 深度分析',
      behavior_tags:     '教学行为标签：',
      btn_download_csv:  '下载 CSV',
      empty_waiting:     '等待分析完成...',

      upload_spinning:     '正在分离音频、识别语音并进行大模型分析，可能需要数分钟，请耐心等待...',
      upload_drag_text:    '点击或拖拽教学视频到此处，开始自动解析',
      upload_hint:         '支持 .mp4、.mov、.avi 等常见格式，系统将自动进行语音识别（Whisper）和动作序列提取（Ollama）。',
      upload_success:      '{{name}} 分析完成！',
      upload_error_type:   '只能上传视频文件！',
      upload_error_size:   '视频必须小于 500 MB！',
      upload_error_failed: '分析失败',
      upload_error_detail: '视频上传或分析失败，请检查后端服务日志。',

      engine_title:        '引擎管理',
      engine_stt_label:    '语音识别模型（Whisper）',
      engine_tiny:         'Tiny — 最快，精度较低',
      engine_base:         'Base — 默认平衡',
      engine_small:        'Small — 较高精度，占用内存多',
      engine_medium:       'Medium — 高精度',
      engine_llm_label:    '大语言模型（Ollama）',
      engine_temp_label:   '创意度（Temperature）',
      engine_temp_strict:  '严格',
      engine_temp_balanced:'均衡',
      engine_temp_creative:'发散',
      engine_tip:          '温度越高，分析越发散；温度越低，输出越保守一致。',

      player_empty: '暂无视频，请先上传。',
      player_title: '教学视频',

      chart_empty:           '暂无分析数据，请先上传视频。',
      chart_title:           '动作序列时序图（点击散点跳转视频）',
      chart_x_axis:          '时间（秒）',
      chart_y_axis:          '教学行为',
      chart_series:          '教学动作',
      chart_tooltip_time:    '时间',
      chart_tooltip_detail:  '详情',
      chart_tooltip_seconds: '秒',
    },
  },

  ja: {
    translation: {
      app_title:    '授業行動分析システム',
      app_subtitle: 'ローカル LLM に基づく自己教師あり授業行動マイニング',
      sidebar_title: '設定パネル',
      lang_switch:  '言語',

      results_title:     '分析結果',
      tab_transcription: '文字起こし',
      tab_analysis:      'AI 深層分析',
      behavior_tags:     '授業行動タグ：',
      btn_download_csv:  'CSV ダウンロード',
      empty_waiting:     '分析を待っています...',

      upload_spinning:     '音声分離・音声認識・LLM 分析を実行中です。数分かかる場合があります。しばらくお待ちください...',
      upload_drag_text:    '授業動画をここにクリックまたはドラッグして自動解析を開始',
      upload_hint:         '.mp4、.mov、.avi などの一般的な形式に対応。音声認識（Whisper）と動作シーケンス抽出（Ollama）が自動実行されます。',
      upload_success:      '{{name}} の分析が完了しました！',
      upload_error_type:   '動画ファイルのみアップロード可能です！',
      upload_error_size:   '動画は 500 MB 未満にしてください！',
      upload_error_failed: '分析に失敗しました',
      upload_error_detail: 'アップロードまたは分析に失敗しました。バックエンドサービスのログを確認してください。',

      engine_title:        'エンジン管理',
      engine_stt_label:    '音声認識モデル（Whisper）',
      engine_tiny:         'Tiny — 最速、精度低め',
      engine_base:         'Base — デフォルトバランス',
      engine_small:        'Small — 高精度、メモリ消費大',
      engine_medium:       'Medium — 高精度',
      engine_llm_label:    '大規模言語モデル（Ollama）',
      engine_temp_label:   '創造性（Temperature）',
      engine_temp_strict:  '厳格',
      engine_temp_balanced:'バランス',
      engine_temp_creative:'発散',
      engine_tip:          'Temperature が高いほど分析が多様になり、低いほど出力が一貫します。',

      player_empty: '動画がありません。先にアップロードしてください。',
      player_title: '授業動画',

      chart_empty:           '分析データがありません。先に動画をアップロードしてください。',
      chart_title:           '動作シーケンス時系列図（点をクリックで動画にジャンプ）',
      chart_x_axis:          '時間（秒）',
      chart_y_axis:          '授業行動',
      chart_series:          '授業アクション',
      chart_tooltip_time:    '時間',
      chart_tooltip_detail:  '詳細',
      chart_tooltip_seconds: '秒',
    },
  },
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    // [ZH] 优先读取上次用户选择的语言，默认英文
    // [JA] 前回ユーザーが選択した言語を優先し、デフォルトは英語
    // [EN] Use the previously selected language; fall back to English
    lng: localStorage.getItem('i18n_lang') || 'en',
    fallbackLng: 'en',
    interpolation: { escapeValue: false },
  });

// [ZH] 语言切换时持久化到 localStorage
// [JA] 言語変更時に localStorage へ永続化する
// [EN] Persist the selected language to localStorage on each change
i18n.on('languageChanged', (lng) => localStorage.setItem('i18n_lang', lng));

export default i18n;
