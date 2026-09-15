"use client";

import { useState } from "react";
import type { CandidatePost } from "@/lib/types";
import styles from "./AiNotes.module.css";

type Props = {
  post: CandidatePost;
};

export function AiNotes({ post }: Props) {
  const [open, setOpen] = useState(false);

  return (
    <div className={styles.wrap}>
      <button
        type="button"
        className={styles.toggle}
        aria-expanded={open}
        onClick={() => setOpen((v) => !v)}
      >
        {open ? "收起 AI 备注" : "展开 AI 备注"}
      </button>
      {open ? (
        <div className={styles.body}>
          <p className={styles.meta}>
            领域：{post.domainLabel ?? post.domain} · nicheScore{" "}
            {post.nicheScore} · 状态 {post.status}
          </p>
          <p className={styles.rationale}>{post.rationale ?? "（无 rationale）"}</p>
        </div>
      ) : null}
    </div>
  );
}
