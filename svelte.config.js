import adapter from '@sveltejs/adapter-static';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	compilerOptions: {
		runes: ({ filename }) => (filename.split(/[/\\]/).includes('node_modules') ? undefined : true)
	},
	warningFilter: (w) => !w.code.startsWith('a11y'),
	kit: {
		adapter: adapter({
			pages: 'build',
			assets: 'build',
			fallback: 'index.html',
			precompress: false,
			strict: false
		}),
		prerender: {
			entries: [
				'*',
				...['nubecitas', 'exploradores', 'aventureros', 'maestros'].flatMap(w =>
					Array.from({ length: 18 }, (_, i) => `/${w}/g${i + 1}`)
				)
			]
		}
	}
};

export default config;
