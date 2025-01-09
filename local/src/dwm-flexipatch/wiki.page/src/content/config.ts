import { defineCollection } from 'astro:content';
import { docsSchema } from '@astrojs/starlight/schema';
import { Steps } from '@astrojs/starlight/components';

export const collections = {
	docs: defineCollection({ schema: docsSchema() }),
};
