const mobileNav = document.querySelector('.index-nav-ul');
const navToggle = document.querySelector('.mobile-nav-toggle');
var linkToggle = document.getElementsByClassName('index-nav-links');

navToggle.addEventListener('click', () => {
    
    const visibility = mobileNav.getAttribute("data-visible");

    if (visibility === "false") {
        mobileNav.setAttribute("data-visible", true);
    }else if (visibility === "true") {
        mobileNav.setAttribute("data-visible", false);
    }
});


for (i=0; i < linkToggle.length; i++) {
    
    linkToggle[i].addEventListener('click', () => {
    
        const visibility = mobileNav.getAttribute("data-visible");
        
        if (visibility === "true") {
            mobileNav.setAttribute("data-visible", false);
        }
    });
}


const faders = document.querySelectorAll('.fade-in');

const appearOptions = {  
    threshold: 0,
    rootMargin: "0px 0px -340px 0px"};

const appearOnScroll = new IntersectionObserver(function(entries, appearOnScroll) {
    entries.forEach(entry => {
        if (!entry.isIntersecting) {
            return;
        } else {
            entry.target.classList.add("appear");
            appearOnScroll.unobserve(entry.target);
        }
    })
}, appearOptions);

faders.forEach(fader => {
    appearOnScroll.observe(fader);
});
