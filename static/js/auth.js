/* ==========================================
   AI RESUME BUILDER FULL JS
========================================== */


/* ==========================================
   AUTH FEATURES
========================================== */


/* PASSWORD TOGGLE */

function togglePassword() {

    const field = document.getElementById("password");

    if (!field) return;

    field.type =
        field.type === "password"
        ? "text"
        : "password";
}



/* CONFIRM PASSWORD TOGGLE */

function toggleConfirmPassword() {

    const field =
    document.getElementById("confirmPassword");


    if (!field) return;


    field.type =
        field.type === "password"
        ? "text"
        : "password";

}



/* PASSWORD STRENGTH */

function passwordStrength() {


    const password =
    document.getElementById("password");


    const bar =
    document.getElementById("strengthBar");


    const text =
    document.getElementById("strengthText");


    if (!password || !bar || !text)
        return;



    let value = password.value;

    let score = 0;



    if (value.length >= 8)
        score++;

    if (/[A-Z]/.test(value))
        score++;

    if (/[a-z]/.test(value))
        score++;

    if (/[0-9]/.test(value))
        score++;

    if (/[!@#$%^&*]/.test(value))
        score++;




    if (score <= 2) {


        bar.style.width = "30%";

        bar.className =
        "progress-bar bg-danger";


        text.innerText =
        "Weak Password";


    }


    else if(score <= 4){


        bar.style.width = "70%";

        bar.className =
        "progress-bar bg-warning";


        text.innerText =
        "Medium Password";


    }


    else{


        bar.style.width = "100%";

        bar.className =
        "progress-bar bg-success";


        text.innerText =
        "Strong Password";


    }


}






/* GLOBAL TOAST */


function showToast(message, type="danger"){


    let toast =
    document.getElementById("globalToast");


    if(!toast)
        return;



    toast.innerHTML = message;



    toast.className =
    "toast-message " + type;



    toast.style.display =
    "block";



    setTimeout(function(){


        toast.style.display =
        "none";


    },3000);


}






/* EMAIL VALIDATION */


function validateEmail(email){


    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);


}





/* LOGIN VALIDATION */


function validateLoginForm(){


    const email =
    document.querySelector(
        "input[name='email']"
    );


    const password =
    document.querySelector(
        "input[name='password']"
    );



    if(!email || !password)
        return true;



    if(!validateEmail(email.value)){


        showToast(
            "Enter valid email"
        );


        return false;

    }




    if(password.value.length < 6){


        showToast(
            "Password too short"
        );


        return false;

    }



    return true;


}







/* REGISTER VALIDATION */


function validateRegisterForm(){



    const email =
    document.querySelector(
        "input[name='email']"
    );


    const password =
    document.getElementById(
        "password"
    );


    const confirm =
    document.getElementById(
        "confirmPassword"
    );




    if(!email || !password || !confirm)
        return true;





    if(!validateEmail(email.value)){


        showToast(
            "Invalid email"
        );


        return false;

    }





    if(password.value.length < 8){


        showToast(
            "Minimum 8 characters required"
        );


        return false;

    }





    if(password.value !== confirm.value){


        showToast(
            "Passwords do not match"
        );


        return false;

    }




    return true;


}






/* ==========================================
   DARK MODE
========================================== */


function toggleTheme(){


    document.body.classList.toggle(
        "dark-mode"
    );


    localStorage.setItem(

        "theme",

        document.body.classList.contains(
            "dark-mode"
        )

        ? "dark"

        : "light"

    );


}





window.addEventListener(
"load",
function(){


    if(localStorage.getItem("theme")==="dark"){

        document.body.classList.add(
            "dark-mode"
        );

    }


});







/* ==========================================
   RESUME BUILDER
========================================== */


let currentResumeId = null;

let autosaveTimer = null;



async function createResume(){


    const res =
    await fetch(
        "/resume/create",
        {

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            title:"Untitled Resume",

            template_id:"basic"

        })

    });



    const data =
    await res.json();



    currentResumeId =
    data.id;



    loadResumes();


}







async function loadResumes(){


    const res =
    await fetch("/resume/");


    const data =
    await res.json();



    const list =
    document.getElementById(
        "resumeList"
    );



    if(!list)
        return;



    list.innerHTML="";



    data.forEach(r=>{


        let div =
        document.createElement(
            "div"
        );


        div.className =
        "resume-item";


        div.innerText =
        r.title;



        div.onclick =
        ()=>loadResume(r.id);



        list.appendChild(div);



    });


}







async function loadResume(id){


    const res =
    await fetch(
        `/resume/${id}`
    );


    const data =
    await res.json();



    currentResumeId =
    data.id;



    if(document.getElementById("title"))

    document.getElementById("title").value =
    data.title || "";



    if(document.getElementById("summary"))

    document.getElementById("summary").value =
    data.summary || "";


}






function autosave(){


    if(!currentResumeId)
        return;



    clearTimeout(
        autosaveTimer
    );



    autosaveTimer =
    setTimeout(async()=>{


        await fetch(

        `/resume/${currentResumeId}/autosave`,

        {

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

        title:
        document.getElementById("title").value,


        summary:
        document.getElementById("summary").value


        })


        });



        console.log(
            "Autosaved"
        );


    },800);



}






/* ==========================================
   ATS CHECKER
========================================== */


async function checkATS(){


const file =
document.getElementById("resumeFile");


const job =
document.getElementById("jobDesc");



if(!file || !file.files[0]){


    showToast(
        "Upload resume first"
    );


    return;


}



const formData =
new FormData();



formData.append(
"resume",
file.files[0]
);



formData.append(
"job_description",
job.value
);




const res =
await fetch(
"/ats/check",
{

method:"POST",

body:formData

});



const data =
await res.json();



if(document.getElementById("score"))

document.getElementById("score").innerText =
(data.score || 0)+"%";



}







/* ==========================================
   PORTFOLIO
========================================== */


let projects=[];



function addProject(){


const title =
document.getElementById("title");


const desc =
document.getElementById("desc");


const link =
document.getElementById("link");



if(!title || !title.value){


showToast(
"Enter project title"
);


return;


}



projects.push({

title:title.value,

desc:desc.value,

link:link.value

});



renderProjects();


}






function renderProjects(){


const grid =
document.getElementById(
"portfolioGrid"
);



if(!grid)
return;



grid.innerHTML="";



projects.forEach(p=>{


let card =
document.createElement(
"div"
);


card.className =
"portfolio-card";



card.innerHTML = `

<h5>${p.title}</h5>

<p>${p.desc}</p>

<a href="${p.link}" target="_blank">
View Project
</a>

`;



grid.appendChild(card);



});


}







console.log(
"AI Resume Builder FULL JS Loaded"
);