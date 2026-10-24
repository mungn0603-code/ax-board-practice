export type PolishResult = {
  interview: string;
  sns: string;
  presentation: string;
  model: string;
};

export async function POST(req: Request) {
  const { text } = (await req.json().catch(() => ({}))) as { text?: string };
  const intro = text?.trim();
  if (!intro) {
    return Response.json({ error: "자기소개를 한 줄 입력해 주세요." }, { status: 400 });
  }

  // 가짜 결과 — 화면 확인용. 다음 단계에서 OpenRouter 호출로 바꾼다.
  const result: PolishResult = {
    interview: `[면접용] ${intro}`,
    sns: `[SNS용] ${intro}`,
    presentation: `[발표용] 안녕하세요, ${intro}`,
    model: "mock (가짜 결과)",
  };
  return Response.json(result);
}
