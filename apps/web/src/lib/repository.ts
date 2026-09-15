import { getCandidateRepository } from "./mock/mock-repository";
import type { CandidateRepository } from "./types";

/** 当前固定 Mock；环境就绪后可切换 Prisma 实现 */
export function getRepository(): CandidateRepository {
  return getCandidateRepository();
}
