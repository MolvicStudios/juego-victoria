import{$ as e,B as t,C as n,D as r,E as i,F as a,G as o,I as s,K as c,L as l,M as u,O as d,Q as f,R as p,S as m,_ as h,b as g,d as _,g as v,nt as y,o as b,p as x,v as S,x as C,y as w,z as T}from"./Dgde7_OJ.js";import"./Br5cJI0m.js";import{i as E,r as D,t as O}from"./B9nEVu0u.js";var k={es:`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 40" width="48" height="32" aria-hidden="true">
			<rect width="60" height="40" fill="#AA151B"/>
			<rect y="10" width="60" height="20" fill="#F1BF00"/>
		</svg>`,en:`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 40" width="48" height="32" aria-hidden="true">
			<rect width="60" height="40" fill="#012169"/>
			<path d="M0,0 L60,40 M60,0 L0,40" stroke="#fff" stroke-width="6"/>
			<path d="M0,0 L60,40 M60,0 L0,40" stroke="#C8102E" stroke-width="4"/>
			<path d="M30,0 V40 M0,20 H60" stroke="#fff" stroke-width="10"/>
			<path d="M30,0 V40 M0,20 H60" stroke="#C8102E" stroke-width="6"/>
		</svg>`,ca:`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 40" width="48" height="32" aria-hidden="true">
			<rect width="60" height="40" fill="#FCDD09"/>
			<rect y="5" width="60" height="5" fill="#DA121A"/>
			<rect y="15" width="60" height="5" fill="#DA121A"/>
			<rect y="25" width="60" height="5" fill="#DA121A"/>
			<rect y="35" width="60" height="5" fill="#DA121A"/>
		</svg>`,eu:`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 40" width="48" height="32" aria-hidden="true">
			<rect width="60" height="40" fill="#fff"/>
			<path d="M30,0 V40 M0,20 H60" stroke="#D7281F" stroke-width="10"/>
			<path d="M0,0 L60,40 M60,0 L0,40" stroke="#2B7F3B" stroke-width="6"/>
		</svg>`,gl:`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 40" width="48" height="32" aria-hidden="true">
			<rect width="60" height="40" fill="#fff"/>
			<rect y="24" width="60" height="16" fill="#009AC7"/>
			<path d="M0,0 V40 M5,0 V40" stroke="#009AC7" stroke-width="3"/>
			<path d="M60,0 V40 M55,0 V40" stroke="#009AC7" stroke-width="3"/>
		</svg>`},A=n(`<div role="radio" tabindex="0"><span class="lsel-flag svelte-19ftpm1" aria-hidden="true"></span> <span class="lsel-name svelte-19ftpm1"> </span></div>`),j=n(`<div class="lsel-onboard svelte-19ftpm1" role="radiogroup" aria-labelledby="lsel-title"><h2 class="lsel-title svelte-19ftpm1" id="lsel-title"> </h2> <div class="lsel-grid svelte-19ftpm1"></div> <button class="lsel-confirm svelte-19ftpm1"> </button></div>`),M=n(`<span class="lsel-check svelte-19ftpm1" aria-hidden="true">✓</span>`),N=n(`<div role="radio" tabindex="0"><span class="lsel-flag-sm svelte-19ftpm1" aria-hidden="true"></span> <span class="lsel-row-name svelte-19ftpm1"> </span> <!></div>`),P=n(`<div class="lsel-settings svelte-19ftpm1" role="radiogroup"></div>`);function F(n,i){e(i,!0);let F=()=>c(D,`$locale`,L),I=()=>c(E,`$t`,L),[L,R]=o(),z=b(i,`variant`,3,`onboarding`),B=b(i,`onConfirm`,3,void 0),V=Object.keys(O),H=t(p(F()));D.subscribe(e=>{T(H,e,!0)});function U(e){T(H,e,!0),z()===`settings`&&D.set(e)}function W(){D.set(d(H)),B()&&B()()}function G(){return O[d(H)]?.confirmBtn??`¡Vamos!`}var K=m(),q=s(K),J=e=>{var t=j(),n=a(t),i=a(n,!0);y(n);var o=l(n,2);h(o,21,()=>V,S,(e,t)=>{var n=A(),i=a(n);v(i,()=>k[d(t)],!0),y(i);var o=l(i,2),s=a(o,!0);y(o),y(n),u(()=>{x(n,1,`lsel-card ${d(H)===d(t)?`sel`:``}`,`svelte-19ftpm1`),_(n,`aria-checked`,d(H)===d(t)),g(s,O[d(t)].nativeName)}),r(`click`,n,()=>U(d(t))),r(`keydown`,n,e=>{(e.key===`Enter`||e.key===` `)&&(e.preventDefault(),U(d(t)))}),C(e,n)}),y(o);var s=l(o,2),c=a(s,!0);y(s),y(t),u((e,t)=>{g(i,e),g(c,t)},[()=>I()(`ui.lang.select_title`),()=>G()]),r(`click`,s,W),C(e,t)},Y=e=>{var t=P();h(t,21,()=>V,S,(e,t)=>{var n=N(),i=a(n);v(i,()=>k[d(t)],!0),y(i);var o=l(i,2),s=a(o,!0);y(o);var c=l(o,2),f=e=>{C(e,M())};w(c,e=>{d(H)===d(t)&&e(f)}),y(n),u(()=>{x(n,1,`lsel-row ${d(H)===d(t)?`sel`:``}`,`svelte-19ftpm1`),_(n,`aria-checked`,d(H)===d(t)),g(s,O[d(t)].nativeName)}),r(`click`,n,()=>U(d(t))),r(`keydown`,n,e=>{(e.key===`Enter`||e.key===` `)&&(e.preventDefault(),U(d(t)))}),C(e,n)}),y(t),u(e=>_(t,`aria-label`,e),[()=>I()(`ui.settings.language`)]),C(e,t)};w(q,e=>{z()===`onboarding`?e(J):e(Y,-1)}),C(n,K),f(),R()}i([`click`,`keydown`]);export{F as t};