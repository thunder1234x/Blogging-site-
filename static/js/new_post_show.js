
document.addEventListener('DOMContentLoaded', function () {
    var mb = document.getElementById("btn2");
    mb.addEventListener('click', swapper, false);
});

function swapper(){
       get_email=localStorage.getItem('userid')
   link="/posts/new/"+get_email
    window.location.replace(link)
}