import { MOCK_CANDIDATES } from "./candidates";
import type {
  CandidatePost,
  CandidateRepository,
  ReviewAction,
} from "../types";

function clone(posts: CandidatePost[]): CandidatePost[] {
  return structuredClone(posts);
}

/** 内存 Mock；接口与未来 Prisma 仓储对齐 */
export class MockCandidateRepository implements CandidateRepository {
  private posts: CandidatePost[];

  constructor(seed: CandidatePost[] = MOCK_CANDIDATES) {
    this.posts = clone(seed);
  }

  async listToday(): Promise<CandidatePost[]> {
    const today = new Date().toISOString().slice(0, 10);
    return this.posts.slice(0, 3).map((p) => ({ ...p, dateBatch: today }));
  }

  async getById(id: string): Promise<CandidatePost | null> {
    return this.posts.find((p) => p.id === id) ?? null;
  }

  async applyReview(
    id: string,
    action: ReviewAction,
    rejectReason?: string,
  ): Promise<CandidatePost | null> {
    const post = this.posts.find((p) => p.id === id);
    if (!post) return null;

    if (action === "publish") {
      post.status = "published";
    } else if (action === "draft") {
      post.status = "draft";
    } else {
      post.status = "rejected";
      post.rejectReason = rejectReason ?? "rejected";
    }

    return structuredClone(post);
  }
}

let singleton: MockCandidateRepository | null = null;

export function getCandidateRepository(): CandidateRepository {
  if (!singleton) singleton = new MockCandidateRepository();
  return singleton;
}
