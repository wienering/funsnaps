// Mobile menu: Lucci split nav (nav-lucci) or legacy single .nav-menu
document.addEventListener('DOMContentLoaded', function() {
    const navLucci = document.querySelector('.nav-wrapper.nav-lucci');
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');

    if (navLucci && mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', function() {
            const open = navLucci.classList.toggle('nav-open');
            mobileMenuToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
        });

        navLucci.querySelectorAll('a').forEach(function(link) {
            link.addEventListener('click', function() {
                navLucci.classList.remove('nav-open');
                mobileMenuToggle.setAttribute('aria-expanded', 'false');
            });
        });
    } else if (mobileMenuToggle) {
        const navMenu = document.querySelector('.nav-menu');
        if (navMenu) {
            mobileMenuToggle.addEventListener('click', function() {
                const open = navMenu.classList.toggle('active');
                mobileMenuToggle.classList.toggle('active');
                mobileMenuToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
            });

            navMenu.querySelectorAll('a').forEach(function(link) {
                link.addEventListener('click', function() {
                    navMenu.classList.remove('active');
                    mobileMenuToggle.classList.remove('active');
                    mobileMenuToggle.setAttribute('aria-expanded', 'false');
                });
            });
        }
    }

    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            const href = anchor.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    const offsetTop = target.offsetTop - 96;
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });

    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            const currentScroll = window.pageYOffset;
            if (currentScroll > 100) {
                navbar.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
            } else {
                navbar.style.boxShadow = 'none';
            }
        });
    }

    const copyrightYear = document.getElementById('copyright-year');
    if (copyrightYear) {
        copyrightYear.textContent = new Date().getFullYear();
    }

    var animatedHeadlines = document.querySelectorAll('.animated-headline');
    if (animatedHeadlines.length) {
        var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (reduceMotion) {
            animatedHeadlines.forEach(function (el) {
                el.classList.add('is-in-view');
            });
        } else {
            var headlineObserver = new IntersectionObserver(
                function (entries) {
                    entries.forEach(function (entry) {
                        if (entry.isIntersecting) {
                            entry.target.classList.add('is-in-view');
                            headlineObserver.unobserve(entry.target);
                        }
                    });
                },
                { root: null, rootMargin: '0px 0px -10% 0px', threshold: 0.15 }
            );
            animatedHeadlines.forEach(function (el) {
                headlineObserver.observe(el);
            });
        }
    }
});
