"use client";

import { useEffect, useCallback, useRef, useState } from "react";
import type { CandidatePost } from "@/lib/types";
import styles from "./PhoneNotePreview.module.css";

const ACCOUNT_NAME = "棱镜编辑部";

type Props = {
  post: CandidatePost;
};

export function PhoneNotePreview({ post }: Props) {
  const [index, setIndex] = useState(0);
  const startX = useRef<number | null>(null);
  const images = [...post.images].sort((a, b) => a.sortOrder - b.sortOrder);

  useEffect(() => {
    setIndex(0);
  }, [post.id]);

  const go = useCallback(
    (next: number) => {
      if (images.length === 0) return;
      const n = ((next % images.length) + images.length) % images.length;
      setIndex(n);
    },
    [images.length],
  );

  return (
    <div className={styles.phone}>
      <div className={styles.screen}>
        <div className={styles.authorRow}>
          <div className={styles.avatar} aria-hidden />
          <span className={styles.authorName}>{ACCOUNT_NAME}</span>
        </div>

        <div
          className={styles.carousel}
          onPointerDown={(e) => {
            startX.current = e.clientX;
          }}
          onPointerUp={(e) => {
            if (startX.current == null) return;
            const dx = e.clientX - startX.current;
            startX.current = null;
            if (dx < -40) go(index + 1);
            if (dx > 40) go(index - 1);
          }}
        >
          <div
            className={styles.track}
            style={{ transform: `translateX(-${index * 100}%)` }}
          >
            {images.map((img) => (
              <div className={styles.slide} key={img.id}>
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={img.url} alt="" width={img.width} height={img.height} />
              </div>
            ))}
          </div>
          <div className={styles.dots}>
            {images.map((img, i) => (
              <button
                key={img.id}
                type="button"
                className={`${styles.dot} ${i === index ? styles.dotActive : ""}`}
                aria-label={`第 ${i + 1} 张图`}
                onClick={() => setIndex(i)}
              />
            ))}
          </div>
        </div>

        <div className={styles.body}>
          <h2 className={styles.title}>{post.title}</h2>
          <p className={styles.text}>{post.body}</p>
          <div className={styles.tags}>
            {post.tags.map((t) => (
              <span className={styles.tag} key={t}>
                #{t}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
