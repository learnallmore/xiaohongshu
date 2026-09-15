import { getRepository } from "@/lib/repository";
import { ReviewStudio } from "@/components/ReviewStudio";

export default async function ReviewPage() {
  const posts = await getRepository().listToday();
  return <ReviewStudio initialPosts={posts} />;
}
