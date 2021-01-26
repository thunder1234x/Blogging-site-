function store() {
   all_mail=document.getElementById('mail_gain').innerHTML;
   console.log(all_mail)
   email=document.getElementById('email').value
   if(all_mail && email)
   {
      if (all_mail.includes(email)){
            localStorage.setItem('userid',email)
         }

      else{
         alert('Email id not Exists in Database')
      }
   }
}





   
   
// document.getElementById("myLink").onclick = function() {
//    get_email=localStorage.getItem('userid')
//    link="/posts/new/"+get_email
//    var link_pre = document.getElementById("mylink");
//    link_pre.setAttribute("href", link);
//    return false;
//    }

