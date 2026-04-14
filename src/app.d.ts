// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}
	interface Window {
		ppCelebrate: (msg: string, stars?: number, cb?: Function | null, lvMsg?: string | null) => void;
		ppBeep: (freq?: number, dur?: number, type?: OscillatorType, vol?: number) => void;
		ppSay: (txt: string) => void;
		ppBoo: () => void;
		ppWin: () => string;
		ppGetLevel: () => number;
		ppOnCorrect: (sourceEvent?: Event) => void;
		ppOnWrong: (sourceEvent?: Event) => string | null;
		ppT?: (key: string, vars?: Record<string, string | number>) => string;
		webkitAudioContext?: typeof AudioContext;
	}
}

export {};
