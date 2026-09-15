export type DomainKind =
  | "cityscape"
  | "interior"
  | "music"
  | "extended";

export type PostStatus =
  | "pending"
  | "approved"
  | "rejected"
  | "draft"
  | "published";

export type PostImage = {
  id: string;
  sortOrder: number;
  url: string;
  width: number;
  height: number;
  mimeType: string;
  source: string;
  license: string;
};

export type CandidatePost = {
  id: string;
  dateBatch: string;
  domain: DomainKind;
  domainLabel: string | null;
  status: PostStatus;
  title: string;
  body: string;
  tags: string[];
  coverIndex: number;
  rationale: string | null;
  nicheScore: number;
  images: PostImage[];
  rejectReason?: string | null;
};

export type ReviewAction = "publish" | "draft" | "reject";

export interface CandidateRepository {
  listToday(): Promise<CandidatePost[]>;
  getById(id: string): Promise<CandidatePost | null>;
  applyReview(
    id: string,
    action: ReviewAction,
    rejectReason?: string,
  ): Promise<CandidatePost | null>;
}
