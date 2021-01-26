
document.addEventListener('DOMContentLoaded', function () {
    var mb = document.getElementById("my_post");
    mb.addEventListener('click', my_post_show, false);
});

function my_post_show(){
    get_email=localStorage.getItem('userid')
    if(get_email!=''){
        link="/blogger/post/"+get_email
        window.location.replace(link)
    }
    else{
        alert("You haven't logged in yet")
    }
}