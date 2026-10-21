/*
	Dependency-free page behaviour:
	1. slide-in menu (open / close via button, Escape, backdrop, links)
	2. .is-scrolled header state
	3. nav link highlighting for the section in view
	Smooth scrolling is handled in CSS (html { scroll-behavior: smooth }).
*/
(function () {
	'use strict';

	var header = document.getElementById('header');
	var menu = document.getElementById('menu');
	var backdrop = document.querySelector('.menu-backdrop');
	var toggle = document.querySelector('.menu-toggle');
	var closeBtn = document.querySelector('.menu-close');

	function menuIsOpen() {
		return menu.classList.contains('is-open');
	}

	function setMenu(open) {
		menu.classList.toggle('is-open', open);
		backdrop.classList.toggle('is-open', open);
		toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
		if (open) {
			var firstLink = menu.querySelector('a');
			if (firstLink) { firstLink.focus(); }
		} else if (menu.contains(document.activeElement)) {
			toggle.focus();
		}
	}

	toggle.addEventListener('click', function () {
		setMenu(!menuIsOpen());
	});
	closeBtn.addEventListener('click', function () { setMenu(false); });
	backdrop.addEventListener('click', function () { setMenu(false); });
	menu.addEventListener('click', function (event) {
		if (event.target.closest('a')) { setMenu(false); }
	});
	document.addEventListener('keydown', function (event) {
		if (event.key === 'Escape' && menuIsOpen()) { setMenu(false); }
	});

	function syncHeader() {
		header.classList.toggle('is-scrolled', window.scrollY > 8);
	}
	window.addEventListener('scroll', syncHeader, { passive: true });
	syncHeader();

	var navLinks = Array.prototype.slice.call(
		document.querySelectorAll('#header .nav a[href^="#"]')
	);

	if ('IntersectionObserver' in window) {
		var observer = new IntersectionObserver(function (entries) {
			entries.forEach(function (entry) {
				if (!entry.isIntersecting) { return; }
				navLinks.forEach(function (link) {
					link.classList.toggle(
						'is-active',
						link.getAttribute('href') === '#' + entry.target.id
					);
				});
			});
		}, { rootMargin: '-40% 0px -50% 0px' });

		navLinks.forEach(function (link) {
			var target = document.getElementById(link.getAttribute('href').slice(1));
			if (target) { observer.observe(target); }
		});
	}
})();
