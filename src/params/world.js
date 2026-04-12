/** @type {import('@sveltejs/kit').ParamMatcher} */
export function match(param) {
	return ['nubecitas', 'exploradores', 'aventureros', 'maestros'].includes(param);
}
