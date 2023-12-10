if (typeof window.ks !== 'object')
	window.ks = {};

if (typeof window.ks.ui !== 'object')
	window.ks.ui = {};

/* Header */
window.ks.ui.header = {};
window.ks.ui.header.element = null;
window.ks.ui.header.init = () => {
	const header = document.querySelector('.ks-header');
	if (!header) return;
	window.ks.ui.header.element = header;
	const buttons = header.querySelectorAll('a.ks-header__nav-link[href]');
	const uri = window.location.pathname;
	buttons.forEach(button => {
		let href = button.getAttribute('href');
		if (href === uri) button.classList.add('active');
	});
};
document.addEventListener('DOMContentLoaded', window.ks.ui.header.init);

/* Sidebar */
window.ks.ui.sidebar = {};
window.ks.ui.sidebar.element = null;
window.ks.ui.sidebar.toggle = () => {
	document.body.classList.toggle('ks-sidebar--open');
};
window.ks.ui.sidebar.close = () => {
	document.body.classList.remove('ks-sidebar--open');
};
window.ks.ui.sidebar.open = () => {
	document.body.classList.add('ks-sidebar--open');
};
window.ks.ui.sidebar.init = () => {
	const sidebar = document.querySelector('.ks-sidebar');
	if (!sidebar) return;
	const backdrop = document.createElement('div');
	backdrop.classList.add('ks-sidebar__backdrop');
	backdrop.addEventListener('click', window.ks.ui.sidebar.close);
	sidebar.parentNode.insertBefore(backdrop, sidebar);
	window.ks.ui.sidebar.element = sidebar;
	const buttons = sidebar.querySelectorAll('a.ks-sidebar__nav-link[href]');
	const uri = window.location.pathname;
	buttons.forEach(button => {
		let href = button.getAttribute('href');
		if (href === uri) button.classList.add('active');
	});
};
document.addEventListener('DOMContentLoaded', window.ks.ui.sidebar.init);