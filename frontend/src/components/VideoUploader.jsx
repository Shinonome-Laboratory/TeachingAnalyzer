import React, { useState } from 'react';
import { Upload, message, Spin } from 'antd';
import { InboxOutlined } from '@ant-design/icons';
import { useTranslation } from 'react-i18next';
import axios from 'axios';

const { Dragger } = Upload;

const VideoUploader = ({ onAllDataReady, engineConfig }) => {
  const { t } = useTranslation();
  const [loading, setLoading] = useState(false);

  const customRequest = async ({ file, onSuccess, onError }) => {
    setLoading(true);

    const formData = new FormData();
    formData.append('file', file);
    // [ZH] 将侧边栏的引擎配置一并打包发送给后端
    // [JA] サイドバーのエンジン設定をまとめてバックエンドに送信する
    // [EN] Bundle the sidebar engine config and send it to the backend together
    formData.append('whisperModel', engineConfig.whisperModel);
    formData.append('ollamaModel',  engineConfig.ollamaModel);
    formData.append('temperature',  engineConfig.temperature);

    try {
      const localVideoUrl = URL.createObjectURL(file);
      const response = await axios.post('/api/upload_and_analyze', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      if (response.data.status === 'success') {
        // [ZH] 将后端完整数据和本地视频 URL 统一回传给父组件
        // [JA] バックエンドの全データとローカル動画 URL を親コンポーネントに返す
        // [EN] Pass the full backend response and local video URL up to the parent
        onAllDataReady(response.data, localVideoUrl);
        message.success(t('upload_success', { name: file.name }));
        onSuccess(response.data, file);
      } else {
        throw new Error(t('upload_error_failed'));
      }
    } catch (error) {
      console.error(error);
      const errorMsg = error.response?.data?.detail || t('upload_error_detail');
      message.error(errorMsg);
      onError(error);
    } finally {
      setLoading(false);
    }
  };

  const uploadProps = {
    name: 'file',
    multiple: false,
    accept: 'video/*',
    customRequest,
    showUploadList: false,
    beforeUpload: (file) => {
      const isVideo = file.type.startsWith('video/');
      if (!isVideo) message.error(t('upload_error_type'));

      const isLt500M = file.size / 1024 / 1024 < 500;
      if (!isLt500M) message.error(t('upload_error_size'));

      return (isVideo && isLt500M) || Upload.LIST_IGNORE;
    },
  };

  return (
    <Spin spinning={loading} tip={t('upload_spinning')} size="large">
      <div style={{ padding: '20px', background: '#fafafa', borderRadius: '8px', border: '1px dashed #d9d9d9' }}>
        <Dragger {...uploadProps}>
          <p className="ant-upload-drag-icon">
            <InboxOutlined style={{ color: '#1890ff' }} />
          </p>
          <p className="ant-upload-text">{t('upload_drag_text')}</p>
          <p className="ant-upload-hint">{t('upload_hint')}</p>
        </Dragger>
      </div>
    </Spin>
  );
};

export default VideoUploader;
