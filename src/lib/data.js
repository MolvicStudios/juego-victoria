export const AVATARS = ['🦄','👸','🦋','🌟','🐱','🐶','🐰','🐼','🦊','🐻'];

export const STICKER_MILESTONES = [
	{s:5,e:'🌸'},{s:10,e:'🦄'},{s:20,e:'👑'},{s:35,e:'🌈'},{s:50,e:'🏰'},
	{s:75,e:'🎪'},{s:100,e:'💎'},{s:130,e:'🚀'},{s:170,e:'🌟'},{s:200,e:'🎠'},
	{s:250,e:'🦋'},{s:300,e:'🏆'},{s:400,e:'🎭'},{s:500,e:'👸'},{s:650,e:'🌍'},
	{s:800,e:'🎆'},{s:1000,e:'💫'},{s:1300,e:'🦄'},{s:1700,e:'✨'},{s:2000,e:'🥇'},
];

export const LEVEL_COLORS = [
	'#6BCB77','#6BCB77','#6BCB77',
	'#4D9FEC','#4D9FEC','#4D9FEC',
	'#FF9F43','#FF9F43','#FF9F43',
	'#A78BFA','#A78BFA','#A78BFA',
	'#FF6B6B','#FF6B6B','#FF6B6B',
];

export const GAMES = [
	{n:1, ico:'🔷',name:'Formas',       sub:'Arrastra las figuras',  col:'#FF6B6B'},
	{n:2, ico:'🍎',name:'Contar',        sub:'¿Cuántas hay?',         col:'#FF9F43'},
	{n:3, ico:'🅰️',name:'Letras',        sub:'¿Qué empieza por...?',  col:'#FFD93D'},
	{n:4, ico:'🖌️',name:'Pintar',        sub:'¡Dibuja y estampa!',    col:'#6BCB77'},
	{n:5, ico:'🃏',name:'Memoria',       sub:'Encuentra las parejas', col:'#4D9FEC'},
	{n:6, ico:'🎵',name:'Piano Mágico',  sub:'¡Haz música!',          col:'#A78BFA'},
	{n:7, ico:'🔢',name:'Números',       sub:'Ordena del 1 al...',    col:'#F472B6'},
	{n:8, ico:'🦁',name:'¿Qué Ves?',     sub:'Elige la palabra',      col:'#2DD4BF'},
	{n:9, ico:'🧩',name:'Mini Puzle',    sub:'Coloca las piezas',     col:'#FF6B6B'},
	{n:10,ico:'🎨',name:'Colores',       sub:'¡Toca el color!',       col:'#4D9FEC'},
	{n:11,ico:'🧮',name:'Sumas',         sub:'¡Suma frutitas!',       col:'#6BCB77',isNew:true},
	{n:12,ico:'✏️',name:'Traza Letras',  sub:'Conecta los puntos',    col:'#A78BFA',isNew:true},
	{n:13,ico:'🗣️',name:'¿Qué Oyes?',   sub:'Escucha y toca',        col:'#F472B6'},
	{n:14,ico:'🧭',name:'Laberinto',     sub:'Ayuda a Pingu',         col:'#2DD4BF'},
	{n:15,ico:'📏',name:'Grande/Pequeño',sub:'¿Cuál es más grande?',  col:'#FF9F43',isNew:true},
	{n:16,ico:'🔷',name:'Patrones',      sub:'¿Qué sigue después?',   col:'#A78BFA',isNew:true},
	{n:17,ico:'🎈',name:'Globos',        sub:'¡Revienta los globos!',  col:'#F472B6'},
	{n:18,ico:'🐾',name:'Animales',      sub:'¿Qué animal es?',        col:'#FF9F43'},
];

export function shuf(a) { return [...a].sort(() => Math.random() - 0.5); }

export function lerpParam(lv, minVal, maxVal) {
	return Math.round(minVal + (maxVal - minVal) * (lv - 1) / 14);
}
