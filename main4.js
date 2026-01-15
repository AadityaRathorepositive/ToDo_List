const prompt= require("prompt-sync")();

//User DataBase
let DBUSER=[];

//Add USER
function addUser(nameOfUser,ageOfUser,tasksOfUser){
    let user={
        id:Date.now(),
        name:nameOfUser,
        age:ageOfUser,
        task:tasksOfUser
    };
    DBUSER.push(user);
    return user;
}

//Find User in DataBase
function findThatUser(user_name){
    let chache_dataBase=[];
    for(let eachUser of DBUSER){
        if(eachUser.name === user_name){
            chache_dataBase.push(eachUser);
        }
    }
    return chache_dataBase;
}

//Find Task in DataBase
function findTask(user_task){   //User Task will come in array
    let chache_tasks=[];
    for(let user of DBUSER){
        for(let allName of user.task){
            for(let taskfromInput of user_task){
                if(allName === taskfromInput){
                    chache_tasks.push(user);
                }
            }
        }
    }
    return chache_tasks;
}

//Switch User

//Operations for Add User, Search User, Delete User, Modify User
let userMenu=new Map();
userMenu.set(1,"Add User");
userMenu.set(2,"Search User");
userMenu.set(3,"Search Task");
userMenu.set(4,"Modify Task");
userMenu.set(5,"Delete Task");
userMenu.set(6,"Delete User");
userMenu.set(7,"Quit");

let menuArray=[...userMenu];

//Main Function
function main(){
    //Format it nicely (Transform each inner array to a string)
    let startMenu=menuArray
        .map(pair => `${pair[0]}=${pair[1]}`)
        .join("\n");
    let addUserOrNo=parseInt(prompt(`Please your Task\n ${startMenu}`));
    
    while(addUserOrNo!=7){
        if(addUserOrNo===1){
            let nameOfUser=prompt("Enter the name of the User: ").toLowerCase();
            let ageOfUser=parseInt(prompt("Enter the age of the User: "));
            let taskOfUser=prompt("Enter the name of the task using , : ").toLowerCase();
            taskOfUser=taskOfUser.split(",");
            console.log(addUser(nameOfUser,ageOfUser,taskOfUser));
            
        }
        else if(addUserOrNo===2){
            let findUserName=prompt("Enter the name of the User: ").toLowerCase();
            let userFromFindUser=findThatUser(findUserName);
            console.log("User with its Tasks :", userFromFindUser);
        }
        else if(addUserOrNo===3){
            let nameOfTask=prompt("Please provide the name of the task: ").toLowerCase();
            nameOfTask=nameOfTask.split(",");
            let listOfTasks=findTask(nameOfTask);
            console.log("Name of all users with the same task Name: ",listOfTasks);
        }
        addUserOrNo=parseInt(prompt(`Please your Task\n ${startMenu}`));

    }
    
}
main();