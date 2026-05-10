import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';

// [ZH] 必须在所有组件渲染前初始化 i18n 单例
// [JA] すべてのコンポーネントレンダリング前に i18n シングルトンを初期化する
// [EN] Must initialize the i18n singleton before any component renders
import './locales/i18n';

const root = createRoot(document.getElementById('root'));

// [ZH] Ant Design 的 ConfigProvider（含动态语言包）由 App.js 内部管理
// [JA] Ant Design の ConfigProvider（動的ロケール含む）は App.js 内部で管理する
// [EN] Ant Design ConfigProvider (with dynamic locale) is managed inside App.js
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
