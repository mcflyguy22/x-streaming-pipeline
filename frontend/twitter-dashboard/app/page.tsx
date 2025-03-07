// app/page.tsx
import { fetchPosts } from "@/actions/fetch-action";
import { Post } from "@prisma/client";

export default async function Home() {
  const posts: Post[] = await fetchPosts();
  console.log("Posts in page:", posts); // Debug here

  if (!posts || posts.length === 0) {
    return <div>No posts found...</div>; // Better feedback
  }

  return (
    <div>
      <h1>Reddit Posts</h1>
      <ul>
        {posts.map((post) => (
          <li key={post.post_id}>{post.title} (Sentiment: {post.sentiment})</li>
        ))}
      </ul>
    </div>
  );
}