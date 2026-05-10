import React from 'react';
import { Form, Select, Slider, Typography, Divider } from 'antd';
import { SettingOutlined, AudioOutlined, RobotOutlined } from '@ant-design/icons';
import { useTranslation } from 'react-i18next';

const { Title, Text } = Typography;

const EngineConfig = ({ config, setConfig }) => {
  const { t } = useTranslation();
  const [form] = Form.useForm();

  return (
    <div style={{ marginTop: '24px' }}>
      <Title level={5}>
        <SettingOutlined style={{ marginRight: 8 }} />
        {t('engine_title')}
      </Title>
      <Divider style={{ margin: '12px 0' }} />

      <Form
        form={form}
        layout="vertical"
        initialValues={config}
        onValuesChange={(changedValues, allValues) => {
          // [ZH] 任意表单项变动时立即同步到 App.js 的全局状态
          // [JA] フォーム項目が変更されると即座に App.js のグローバル状態へ同期する
          // [EN] Immediately sync to App.js global state on any form field change
          setConfig(allValues);
        }}
      >
        {/* Speech recognition model */}
        <Form.Item
          label={<><AudioOutlined style={{ marginRight: 4 }} /> {t('engine_stt_label')}</>}
          name="whisperModel"
        >
          <Select options={[
            { value: 'tiny',   label: t('engine_tiny')   },
            { value: 'base',   label: t('engine_base')   },
            { value: 'small',  label: t('engine_small')  },
            { value: 'medium', label: t('engine_medium') },
          ]} />
        </Form.Item>

        {/* Large language model */}
        <Form.Item
          label={<><RobotOutlined style={{ marginRight: 4 }} /> {t('engine_llm_label')}</>}
          name="ollamaModel"
        >
          <Select options={[
            { value: 'llama3.1:8b',                      label: 'Llama 3.1 (8B)'      },
            { value: 'deepseek-r1:8b',                   label: 'DeepSeek R1 (8B)'    },
            { value: 'qwen3.5:9b',                       label: 'Qwen 3.5 (9B)'       },
            { value: 'qwen3.5:2b',                       label: 'Qwen 3.5 (2B)'       },
            { value: 'phi4:14b',                         label: 'Phi-4 (14B)'         },
            { value: 'gemma4:e2b',                       label: 'Gemma 4 (E2B)'       },
            { value: 'haervwe/GLM-4.6V-Flash-9B:latest', label: 'GLM-4 Flash (9B)'   },
          ]} />
        </Form.Item>

        {/* Temperature */}
        <Form.Item label={t('engine_temp_label')} name="temperature">
          <Slider
            min={0.0}
            max={1.0}
            step={0.1}
            marks={{
              0:   t('engine_temp_strict'),
              0.5: t('engine_temp_balanced'),
              1:   t('engine_temp_creative'),
            }}
          />
        </Form.Item>
      </Form>

      <Text type="secondary" style={{ fontSize: '12px' }}>
        {t('engine_tip')}
      </Text>
    </div>
  );
};

export default EngineConfig;
