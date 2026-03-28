const get_navbar = document.getElementById("navbar-placeholder");


async function getNavbar() {
    // navbar載入
    let response = await fetch('/navbar.html');
    const data = await response.text();
    get_navbar.innerHTML = data;
    // logo首頁跳轉
    const logo = document.querySelector(".logo");
    logo.addEventListener("click", ()=>{
        window.location.href = "/";
    });
    // 登入框開關&跳轉&登出
    const member_btn = document.querySelector(".member_btn");
    const opacity = document.querySelector(".opacity");
    const login_box = document.getElementById("login");
    member_btn.addEventListener("click", async()=>{
        if (member_btn.textContent.includes('會員登入')){
            login_box.style.display="block";
            opacity.style.display="block";
        }
        if (member_btn.textContent.includes('會員登出')) { 
            let response=await fetch("/api/user/auth",{
                method: "DELETE",
            })
            let result=await response.json();
            if (result.ok){
                window.location.reload();
                return
            }
        }
    });
    opacity.addEventListener("click", () => {
        login_box.style.display = "none";
        sign_box.style.display = "none";
        opacity.style.display = "none";
    });
    const closes = document.querySelectorAll(".close");
    const sign_box = document.getElementById("sign");
    closes.forEach(close => {
        close.addEventListener("click", () => {
            login_box.style.display="none";
            sign_box.style.display="none";
            opacity.style.display="none";
        });
    });
    const login_word = document.getElementById("login-word");
    const sign_word = document.getElementById("sign-word");
    login_word.addEventListener('click', ()=>{
        if (login_word.textContent.includes('點此註冊')) {
            login_box.style.display = "none";
            sign_box.style.display = "block";
        }
    });
    sign_word.addEventListener('click', ()=>{
        if (sign_word.textContent.includes('點此登入')) {
            login_box.style.display = "block";
            sign_box.style.display = "none";
        }
    });
    // 登入系統
    const login_button = document.getElementById("login-button");
    const login_email = document.getElementById("login-email");
    const login_password = document.getElementById("login-password");
    login_button.addEventListener('click', async ()=>{
        let email=login_email.value
        let password=login_password.value
        if(email=="" || password==""){
            login_word.textContent="請輸入信箱和密碼或點此註冊"
            return;
        }
        let response=await fetch("/api/user/auth",{
            method:"PUT",
            headers: {"Content-Type": "application/json"},
            body:JSON.stringify({"email":email, "password":password})
        });
        let result=await response.json();
        if (result.error){
            login_word.textContent=result.message + "，或點此註冊";
            return;
        }
        if (result.ok){
            window.location.reload();
            return;
        }
    })
    // 註冊系統
    const sign_button = document.getElementById("sign-button");
    const sign_email = document.getElementById("sign-email");
    const sign_password = document.getElementById("sign-password");
    sign_button.addEventListener('click', async ()=>{
        let email=sign_email.value
        let password=sign_password.value
        if(email=="" || password==""){
            sign_word.textContent="請輸入完整資料，空白處都要填寫"
            return;
        }
        let response=await fetch("/api/user",{
            method:"POST",
            headers: {
                "Content-Type": "application/json"
            },
            body:JSON.stringify({"email":email, "password":password})
        });
        let result=await response.json();
        if (result.error){
            sign_word.textContent=result.message + "，點此登入"
        }else if(result.ok){
            sign_word.textContent="註冊成功，點此登入"
        }
    })
    // 使用者狀態
    async function check() {
        let response=await fetch("/api/user/auth",{
            method: "GET",
        })
        let result=await response.json();
        if (result.ok){
            member_btn.textContent="會員登出";
            document.body.dataset.login = "true";
        }else {
        member_btn.textContent = "會員登入";
        document.body.dataset.login = "false";
        }
        window.dispatchEvent(new CustomEvent("authStatusReady"));
        console.log("login response status:", response.status);
        console.log("login result:", result);
    }
    await check()
    // 顯示目前的頁面位置
    function staypage() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.bar');

    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (currentPath === linkPath) {
            link.classList.add('active-page');
        } else {
            link.classList.remove('active-page');
        }
    });
    }
    staypage();
}
getNavbar();
