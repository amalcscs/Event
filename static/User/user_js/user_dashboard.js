<script>
const sidebar = document.getElementById("sidebar");
const toggleBtn = document.getElementById("toggleBtn");
const closeSidebar = document.getElementById("closeSidebar");

toggleBtn.addEventListener("click", () => {
    sidebar.classList.toggle("active"); 
    $(".dropdown-menu").removeClass("show"); 
    $("#notifCard").hide(); 
});

closeSidebar.addEventListener("click", () => {
    sidebar.classList.remove("active");
    $(".dropdown-menu").removeClass("show"); 
    $("#notifCard").hide(); 
});

document.addEventListener("click", function(event) {
    const target = event.target;
    if (!target.closest(".notif-container")) {
        notifCard.style.display = "none";
    }
});

document.getElementById("notifIcon").addEventListener("click", function(){
    const card = document.getElementById("notifCard");
    card.style.display = (card.style.display === "block") ? "none" : "block";
});

document.addEventListener("click", function(e) {
    if (!e.target.closest(".notif-container")) {
        document.getElementById("notifCard").style.display = "none";
    }
});

</script>