import React, { useEffect, useRef } from 'react';
import { Card, Empty } from 'antd';
import { useTranslation } from 'react-i18next';

const VideoPlayer = ({ videoUrl, currentTime }) => {
  const { t } = useTranslation();

  // [ZH] 通过 useRef 获取底层 <video> DOM 节点，以便直接操控播放进度
  // [JA] useRef で <video> の DOM ノードを取得し、再生位置を直接操作する
  // [EN] Use useRef to access the underlying <video> DOM node for direct playback control
  const videoRef = useRef(null);

  // [ZH] 监听 currentTime 变化；散点图点击后立即跳转并自动播放
  // [JA] currentTime の変化を監視し、散布図クリック後に即座にシークして自動再生する
  // [EN] Watch currentTime changes; seek and auto-play as soon as a chart point is clicked
  useEffect(() => {
    if (videoRef.current && currentTime !== undefined && currentTime !== null) {
      videoRef.current.currentTime = currentTime;
      // [ZH] 部分浏览器会拦截未静音的自动播放，catch 防止未处理的 Promise rejection
      // [JA] 一部のブラウザは非ミュートの自動再生をブロックするため catch で未処理 rejection を防ぐ
      // [EN] Some browsers block unmuted autoplay; catch prevents an unhandled Promise rejection
      videoRef.current.play().catch(e => console.log('Autoplay blocked by browser:', e));
    }
  }, [currentTime]);

  if (!videoUrl) {
    return (
      <Card style={{ height: '450px', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <Empty description={t('player_empty')} />
      </Card>
    );
  }

  return (
    <Card title={t('player_title')} size="small" bodyStyle={{ padding: 0, background: '#000' }}>
      <video
        ref={videoRef}
        src={videoUrl}
        controls
        style={{
          width: '100%',
          height: '400px',
          objectFit: 'contain', // [ZH] 保持原始比例完整显示 | [JA] アスペクト比を維持して全体を表示 | [EN] Keep aspect ratio and show the full frame
          display: 'block',
        }}
      />
    </Card>
  );
};

export default VideoPlayer;
