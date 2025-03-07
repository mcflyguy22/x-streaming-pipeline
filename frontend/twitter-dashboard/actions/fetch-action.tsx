// actions/fetch-action.ts
import { db } from "@/db";

export async function fetchPosts() {
    const posts = await db.post.findMany(); // Changed 'posts' to 'post' to match model name
    console.log("Fetched posts:", posts); // Debug here
    return posts;
}