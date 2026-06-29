export type NewsItem = {
  slug: string;
  title: string;
  description: string;
  date: string;
  category: string;
  source: string;
  sourceUrl?: string;
  tags: string[];
  importance?: string;
  Content: any;
};

export async function getNewsItems(): Promise<NewsItem[]> {
  const modules = import.meta.glob('../content/news/*.md');
  const items = await Promise.all(
    Object.entries(modules).map(async ([path, load]) => {
      const mod: any = await load();
      const slug = path.split('/').pop()?.replace('.md', '') ?? '';
      return { slug, ...mod.frontmatter, Content: mod.Content } as NewsItem;
    })
  );
  return items.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
}

export async function getNewsByCategory(category: string): Promise<NewsItem[]> {
  const items = await getNewsItems();
  return items.filter((item) => item.category === category);
}
