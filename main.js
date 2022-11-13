var flag = 0;
var old_time;
var new_time;
var total_seconds;

function click_Game() {
    if(flag == 0){
        document.getElementById("game-board").style.backgroundColor = "red";
        document.getElementById("game-board").textContent = "";
        setTimeout(() => {
            document.getElementById("game-board").style.backgroundColor = "green";
            old_time = new Date();
        }, Math.floor(Math.random() * 10000));
        flag = 1;
    } else if (flag == 1){
        new_time = new Date();
        total_seconds = new_time - old_time;
        if(total_seconds > 0){
            document.getElementById("game-board").style.backgroundColor = "skyblue";
            document.getElementById("game-board").textContent = total_seconds + "ms";
            flag = 2;
        }
    } else {
        
    }
  }
