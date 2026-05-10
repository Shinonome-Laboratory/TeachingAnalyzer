import asyncio
import json
import re
import ollama
from backend.config import LLM_CONFIG


def extract_json_objects(text: str) -> list:
    """
    [ZH] 通过追踪大括号层级从原始文本中提取所有 JSON 对象，容忍缺失逗号和多余内容
    [JA] 中括弧の深さを追跡し、欠損カンマや余分なテキストを許容しながら全 JSON オブジェクトを抽出する
    [EN] Extract all JSON objects from raw text by tracking brace depth; tolerates missing commas and extra content
    """
    objects = []
    depth = 0
    start = -1
    for i, char in enumerate(text):
        if char == '{':
            if depth == 0:
                start = i
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0 and start != -1:
                json_str = text[start:i+1]
                try:
                    # [ZH] strict=False 允许字符串内含真实换行符等控制字符
                    # [JA] strict=False で文字列内の実際の改行などの制御文字を許容する
                    # [EN] strict=False allows real newlines and control chars inside strings
                    obj = json.loads(json_str, strict=False)
                    if "tag" in obj:
                        objects.append(obj)
                except json.JSONDecodeError:
                    # [ZH] 模型使用了单引号时，替换后重试
                    # [JA] モデルがシングルクォートを使用した場合は置換して再試行する
                    # [EN] If the model used single quotes, replace and retry
                    try:
                        clean_str = json_str.replace("'", '"').replace('\n', ' ')
                        obj = json.loads(clean_str, strict=False)
                        if "tag" in obj:
                            objects.append(obj)
                    except Exception:
                        pass
    return objects


async def analyze_teaching_text(
    timestamped_text: str,
    model_name: str = LLM_CONFIG["default_model"],
    temperature: float = LLM_CONFIG["temperature"]
) -> list:
    """
    [ZH] 按固定窗口大小分批处理带时间戳的逐字稿，并发调用 LLM 为每句话生成教学行为标签
    [JA] タイムスタンプ付き文字起こしを固定ウィンドウでバッチ分割し、LLM を並列呼び出して各文に教学行動ラベルを付与する
    [EN] Split the timestamped transcript into fixed-size batches and call the LLM concurrently to label each sentence with a teaching action tag
    """
    lines = [line.strip() for line in timestamped_text.strip().split('\n') if line.strip()]
    if not lines:
        return []

    # [ZH] 每批 5 句，平衡上下文长度与模型输出格式稳定性
    # [JA] 1バッチ5文。コンテキスト長とモデル出力フォーマットの安定性を両立する
    # [EN] Process 5 sentences per batch to balance context length and output format stability
    chunk_size = 5
    chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]

    all_results = []
    print(f"识别到 {len(lines)} 句对话，正在分 {len(chunks)} 批次进行逐句挖掘...")

    # [ZH] 并发数限制为 4，防止 Ollama 本地多线程时出现输出截断
    # [JA] 並行数を4に制限し、Ollama のローカルマルチスレッドによる出力途切れを防ぐ
    # [EN] Cap concurrency at 4 to prevent output truncation from Ollama's local threading
    semaphore = asyncio.Semaphore(4)

    async def process_batch(batch_lines):
        async with semaphore:
            context_text = "\n".join(batch_lines)
            count = len(batch_lines)

            # [ZH] 要求输出独立 JSON 对象而非数组，规避模型在数组逗号上的格式错误
            # [JA] 配列ではなく独立した JSON オブジェクトを要求し、配列カンマのフォーマットエラーを回避する
            # [EN] Request independent JSON objects instead of an array to avoid comma formatting errors
            system_prompt = f"""
            You are an expert in analyzing micro-teaching behaviors. Here are {count} pieces of teaching records.
Please, based on the context, generate an appropriate action label for each sentence.
**Output Rules (Strictly Prohibited):**
1. Do not include Markdown syntax (do not use ````json```).
2. Do not use square brackets `[` or `]` for arrays.
3. Output exactly {count} independent JSON objects.
4. Tags must be 3 to 8 characters long and represent abstract teaching actions.
**Strict Output Format Demonstration:**
{{"tag": "Create Cognitive Conflict", "detail": "Break through students' existing cognition through questioning"}}
{{"tag": "Confirm Preconceived Concepts", "detail": "Check if students have mastered the basic definitions"}} """

            try:
                response = await asyncio.to_thread(
                    ollama.chat,
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Please analyze the following {count} sentences in turn:\n\n{context_text}"}
                    ],
                    options={"temperature": 0.3}  # [ZH] 低温度使输出格式更稳定 | [JA] 低温度で出力フォーマットを安定させる | [EN] Low temperature keeps output format consistent
                )

                raw_content = response['message']['content'].strip()

                # [ZH] 调用容错提取器，不依赖正则捕获完整数组
                # [JA] 正規表現の完全配列キャプチャに依存せず、耐障害性のある抽出器を使用する
                # [EN] Use the fault-tolerant extractor instead of relying on regex to capture a full array
                batch_json = extract_json_objects(raw_content)

                if not batch_json:
                    print(f"警告：模型输出格式异常，提取结果为空。原始输出: {raw_content[:50]}...")
                    return []

                valid_results = []
                # [ZH] 将提取到的 JSON 与原文逐行按时间戳绑定
                # [JA] 抽出した JSON を元のテキスト各行のタイムスタンプと 1 対 1 で紐付ける
                # [EN] Bind each extracted JSON object to its source line's timestamp
                for i in range(min(len(batch_json), len(batch_lines))):
                    item = batch_json[i]
                    time_match = re.search(r'\[(\d+):(\d+)\]', batch_lines[i])
                    if time_match:
                        m, s = map(int, time_match.groups())
                        item['time'] = m * 60 + s
                        valid_results.append(item)

                return valid_results

            except Exception as e:
                print(f"警告：批次处理失败: {str(e)}")
                return []

    tasks = [process_batch(c) for c in chunks]
    chunk_results = await asyncio.gather(*tasks)

    for res in chunk_results:
        if isinstance(res, list):
            all_results.extend(res)

    all_results.sort(key=lambda x: x.get('time', 0))
    print(f"逐句挖掘完成，共生成 {len(all_results)} 个教学行为点。")
    return all_results
