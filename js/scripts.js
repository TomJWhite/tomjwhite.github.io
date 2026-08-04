/*
 * Lightweight navigation for the portfolio site.
 * Uses browser APIs directly, with no jQuery or Bootstrap JavaScript dependency.
 */
(function () {
    "use strict";

    const menuButton = document.querySelector(".navbar-toggler");
    const menu = document.getElementById("navbarSupportedContent");
    const navLinks = Array.from(document.querySelectorAll("#sideNav .nav-link"));

    function setMenuOpen(isOpen) {
        if (!menuButton || !menu) return;

        menu.classList.toggle("show", isOpen);
        menuButton.setAttribute("aria-expanded", String(isOpen));
    }

    if (menuButton && menu) {
        menuButton.addEventListener("click", function () {
            setMenuOpen(!menu.classList.contains("show"));
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape" && menu.classList.contains("show")) {
                setMenuOpen(false);
                menuButton.focus();
            }
        });
    }

    navLinks.forEach(function (link) {
        link.addEventListener("click", function () {
            setMenuOpen(false);
        });
    });

    const sections = navLinks
        .map(function (link) {
            return document.querySelector(link.getAttribute("href"));
        })
        .filter(Boolean);

    if ("IntersectionObserver" in window && sections.length > 0) {
        const observer = new IntersectionObserver(
            function (entries) {
                const visibleSection = entries
                    .filter(function (entry) {
                        return entry.isIntersecting;
                    })
                    .sort(function (a, b) {
                        return b.intersectionRatio - a.intersectionRatio;
                    })[0];

                if (!visibleSection) return;

                navLinks.forEach(function (link) {
                    const isActive = link.getAttribute("href") === `#${visibleSection.target.id}`;
                    link.classList.toggle("active", isActive);

                    if (isActive) {
                        link.setAttribute("aria-current", "page");
                    } else {
                        link.removeAttribute("aria-current");
                    }
                });
            },
            {
                rootMargin: "-20% 0px -55% 0px",
                threshold: [0.1, 0.35, 0.6],
            }
        );

        sections.forEach(function (section) {
            observer.observe(section);
        });
    }
})();
