import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';


export default defineConfig({
  site: 'https://ahmadjerjawi.github.io',
  base: '/wiki.github.io',
})


export default defineConfig({
	integrations: [
		starlight({
			title: 'My Docs',

			social: {
				github: 'https://github.com/ahmadjerjawi',
			},
			sidebar: [
				{
					label: 'Starting',
						autogenerate: { directory: 'starting' },
				},
				{
					label: 'Guides',
					autogenerate: { directory: 'guide' },
				},														{
					label: 'Reference',
					autogenerate: { directory: 'reference' },
				},
			],
		}),
	],
});
