import { NextResponse } from "next/server";
import { getRepository } from "@/lib/repository";
import type { ReviewAction } from "@/lib/types";

type Ctx = { params: Promise<{ id: string }> };

export async function POST(req: Request, ctx: Ctx) {
  const { id } = await ctx.params;
  const body = (await req.json()) as { action?: ReviewAction; rejectReason?: string };
  const action = body.action;
  if (action !== "publish" && action !== "draft" && action !== "reject") {
    return NextResponse.json({ error: "invalid action" }, { status: 400 });
  }

  const updated = await getRepository().applyReview(
    id,
    action,
    body.rejectReason,
  );
  if (!updated) {
    return NextResponse.json({ error: "not found" }, { status: 404 });
  }
  return NextResponse.json(updated);
}
