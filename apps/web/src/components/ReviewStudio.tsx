"use client";

import { useEffect, useState } from "react";
import type { CandidatePost, ReviewAction } from "@/lib/types";
import { PhoneNotePreview } from "./PhoneNotePreview";
import { ReviewActions } from "./ReviewActions";
import { AiNotes } from "./AiNotes";
import styles from "@/app/review/review.module.css";

type Props = {
  initialPosts: CandidatePost[];
};

export function ReviewStudio({ initialPosts }: Props) {
  const [posts, setPosts] = useState(initialPosts);
  const [cursor, setCursor] = useState(0);
  const [busy, setBusy] = useState(false);
  const [flash, setFlash] = useState<string | null>(null);
  const [animKey, setAnimKey] = useState(0);

  const post = posts[cursor] ?? null;

  useEffect(() => {
    setAnimKey((k) => k + 1);
  }, [cursor, post?.id]);

  async function onAction(action: ReviewAction) {
    if (!post) return;
    setBusy(true);
    try {
      const res = await fetch(`/api/review/${post.id}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action }),
      });
      if (!res.ok) {
        setFlash("操作失败");
        return;
      }
      const updated = (await res.json()) as CandidatePost;
      setPosts((prev) => prev.map((p) => (p.id === updated.id ? updated : p)));
      const label =
        action === "publish"
          ? "已标记发布（Mock）"
          : action === "draft"
            ? "已存草稿（Mock）"
            : "已拒绝（Mock）";
      setFlash(label);
      window.setTimeout(() => setFlash(null), 1200);
    } finally {
      setBusy(false);
    }
  }

  function selectIndex(i: number) {
    setCursor(i);
  }

  if (!post) {
    return (
      <div className={styles.empty}>
        今日暂无候选。进入内容生成阶段后将在此出现 3 条。
      </div>
    );
  }

  const cover =
    post.images.find((i) => i.sortOrder === post.coverIndex) ?? post.images[0];

  return (
    <div className={styles.shell}>
      <header className={styles.topbar}>
        <div>
          <span className={styles.brand}>棱镜</span>
          <span className={styles.brandHint}>今日 · {posts.length} 候选</span>
        </div>
        <span className={styles.navQuiet}>已发布（Phase 2 占位）</span>
      </header>

      <div className={styles.main}>
        <div className={styles.previewPane}>
          <div key={animKey} className={styles.previewAnim}>
            <PhoneNotePreview post={post} />
          </div>
          <div className={styles.thumbs}>
            {posts.map((p, i) => {
              const thumb =
                p.images.find((img) => img.sortOrder === p.coverIndex) ??
                p.images[0];
              return (
                <button
                  key={p.id}
                  type="button"
                  className={`${styles.thumb} ${i === cursor ? styles.thumbActive : ""}`}
                  aria-label={`切换到第 ${i + 1} 条`}
                  onClick={() => selectIndex(i)}
                >
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img src={thumb?.url} alt="" />
                </button>
              );
            })}
            <span className={styles.indexLabel}>
              {cursor + 1}/{posts.length}
            </span>
          </div>
        </div>

        <aside className={styles.side}>
          <AiNotes post={post} />
          <ReviewActions
            busy={busy}
            flash={flash}
            canPrev={cursor > 0}
            canNext={cursor < posts.length - 1}
            onAction={onAction}
            onPrev={() => selectIndex(Math.max(0, cursor - 1))}
            onNext={() => selectIndex(Math.min(posts.length - 1, cursor + 1))}
          />
          {cover ? (
            <p className={styles.indexLabel}>
              图源：{cover.source} · {cover.license}
            </p>
          ) : null}
        </aside>
      </div>
    </div>
  );
}
