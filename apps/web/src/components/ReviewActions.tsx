"use client";

import styles from "./ReviewActions.module.css";
import type { ReviewAction } from "@/lib/types";

type Props = {
  busy: boolean;
  flash: string | null;
  canPrev: boolean;
  canNext: boolean;
  onAction: (action: ReviewAction) => void;
  onPrev: () => void;
  onNext: () => void;
};

export function ReviewActions({
  busy,
  flash,
  canPrev,
  canNext,
  onAction,
  onPrev,
  onNext,
}: Props) {
  return (
    <div className={styles.panel}>
      <button
        type="button"
        className={styles.primary}
        disabled={busy}
        aria-label="通过并立即发布"
        onClick={() => onAction("publish")}
      >
        通过并立即发布
      </button>
      <button
        type="button"
        className={styles.secondary}
        disabled={busy}
        aria-label="存草稿"
        onClick={() => onAction("draft")}
      >
        存草稿
      </button>
      <button
        type="button"
        className={styles.danger}
        disabled={busy}
        aria-label="拒绝"
        onClick={() => onAction("reject")}
      >
        拒绝
      </button>
      <div className={styles.flash} role="status">
        {flash}
      </div>
      <div className={styles.navRow}>
        <button
          type="button"
          className={styles.navBtn}
          disabled={!canPrev || busy}
          aria-label="上一条"
          onClick={onPrev}
        >
          ← 上一条
        </button>
        <button
          type="button"
          className={styles.navBtn}
          disabled={!canNext || busy}
          aria-label="下一条"
          onClick={onNext}
        >
          下一条 →
        </button>
      </div>
    </div>
  );
}
