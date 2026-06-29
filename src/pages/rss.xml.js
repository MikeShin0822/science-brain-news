import rss from '@astrojs/rss';
import { getNewsItems } from '../utils/news';

export async function GET(context) {
  const items = await getNewsItems();
  return rss({
    title: 'Science Brain News',
    description: '뇌과학과 생명과학 뉴스 큐레이션',
    site: context.site,
    items: items.map((item) => ({
      title: item.title,
      description: item.description,
      pubDate: new Date(item.date),
      link: new URL(`${import.meta.env.BASE_URL}news/${item.slug}/`, context.site).href
    }))
  });
}
