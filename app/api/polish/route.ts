export type PolishResult = {
  interview: string;
  sns: string;
  presentation: string;
  model: string;
};

const SYSTEM_PROMPT = `너는 한국어 자기소개 문장을 다듬는 편집자다.
사용자가 준 자기소개 한 줄을 세 가지 용도로 다듬어라. 사실은 바꾸거나 지어내지 말고(이름 자리에 OOO 같은 빈칸도 넣지 않는다), 각 결과는 한두 문장으로 짧게 쓴다.
- interview: 면접용. 정중하고 또렷한 "~입니다" 체.
- sns: SNS 프로필용. 짧고 가볍게, 필요하면 "|" 로 구분.
- presentation: 발표 시작용. "안녕하세요,"로 시작하는 말하듯 자연스러운 문장.
다른 설명 없이 아래 JSON 하나만 출력한다.
{"interview": "...", "sns": "...", "presentation": "..."}`;

export async function POST(req: Request) {
  const { text } = (await req.json().catch(() => ({}))) as { text?: string };
  const intro = text?.trim();
  if (!intro) {
    return Response.json({ error: "자기소개를 한 줄 입력해 주세요." }, { status: 400 });
  }

  const apiKey = process.env.OPENROUTER_API_KEY;
  if (!apiKey) {
    return Response.json(
      { error: "서버에 OPENROUTER_API_KEY가 없습니다. .env 파일을 확인해 주세요." },
      { status: 500 },
    );
  }

  // openrouter/free는 요청마다 다른 무료 모델을 고르고, 가끔 빈 답변이나 JSON이 아닌 답을 준다.
  // 그래서 실패하면 최대 3번까지 다시 묻는다.
  let lastError: unknown;
  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      return Response.json(await polish(apiKey, intro));
    } catch (err) {
      lastError = err;
      console.error(`다듬기 실패 (${attempt}/3)`, err instanceof Error ? err.message : err);
      if (err instanceof Error && err.name === "TimeoutError") break;
    }
  }

  // 예외를 그대로 던지면 Next.js가 빈 500 응답을 보내 화면에서 "Unexpected end of JSON input"이 난다.
  // 그래서 실패해도 항상 JSON 오류 메시지를 돌려준다.
  const timedOut = lastError instanceof Error && lastError.name === "TimeoutError";
  return Response.json(
    { error: timedOut ? "AI 응답이 너무 늦습니다. 다시 시도해 주세요." : "AI 답변을 읽지 못했습니다. 다시 시도해 주세요." },
    { status: 502 },
  );
}

async function polish(apiKey: string, intro: string): Promise<PolishResult> {
  const res = await fetch("https://openrouter.ai/api/v1/chat/completions", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
      "X-Title": "my-intro",
    },
    body: JSON.stringify({
      model: "openrouter/free",
      messages: [
        { role: "system", content: SYSTEM_PROMPT },
        { role: "user", content: intro.slice(0, 200) },
      ],
    }),
    signal: AbortSignal.timeout(60_000),
  });

  const raw = await res.text();
  if (!res.ok) throw new Error(`OpenRouter ${res.status}: ${raw.slice(0, 300)}`);

  const data = JSON.parse(raw);
  const model: string = data.model ?? "알 수 없음";
  const content: string = data.choices?.[0]?.message?.content ?? "";
  // 무료 모델은 JSON 앞뒤에 다른 글이나 ```json 을 붙이기도 해서 { ... } 부분만 꺼낸다.
  const json = content.match(/\{[\s\S]*\}/)?.[0];
  if (!json) throw new Error(`JSON 없는 답변 (model: ${model}): ${content.slice(0, 200)}`);

  const parsed = JSON.parse(json);
  const result: PolishResult = {
    interview: String(parsed.interview ?? ""),
    sns: String(parsed.sns ?? ""),
    presentation: String(parsed.presentation ?? ""),
    model,
  };
  if (!result.interview || !result.sns || !result.presentation) {
    throw new Error(`빠진 항목이 있는 답변 (model: ${model})`);
  }
  return result;
}
