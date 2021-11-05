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

const hamburger = document.querySelector('.index-480px-nav-container .index-hamburger');

const mobile_menu = document.querySelector('.index-480px-nav-container ul');




const header = document.querySelector('.index-header')

hamburger.addEventListener('click',()=>{
    hamburger.classList.toggle('active');
    mobile_menu.classList.toggle('active');

});



document.addEventListener('scroll',()=>{

    var scroll_position = window.scrollY;
    if(scroll_position > 250){
        header.style.backgroundColor = "#face00";
    }else{
        header.style.backgroundColor = "transparent";

    }
})