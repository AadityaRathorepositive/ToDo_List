const prompt= require("prompt-sync")();

//User DataBase
let DBUSER=[];

//Add USER
function addUser(nameOfUser,ageOfUser,userTask){
    let user={
        id:Date.now(),
        name:nameOfUser,
        age:ageOfUser,
        task:userTask
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
        for(let taskObject of user.task){
            for(let taskfromInput of user_task){
                if(taskObject.title === taskfromInput){
                    chache_tasks.push(user);
                }
            }
        }
    }
    return chache_tasks;
}

//Switch User (means user want to modify the task)
let taskMenu=new Map();
taskMenu.set(1,"Add Task");
taskMenu.set(2,"View Task");
taskMenu.set(3,"Mark as Done");
taskMenu.set(4,"Delete");
taskMenu.set(5,"Set Priority");
taskMenu.set(6,"Switch User");

let taskMenuArray=[...taskMenu];

// Task of a user Function
function taskOfSingleUser(){
    
}


//Task Priority
let taskPriority=new Map();
taskPriority.set(1,"Critical");
taskPriority.set(2,"Very High");
taskPriority.set(3,"Medium");
taskPriority.set(4,"Low");

let taskPriorityMenu=[...taskPriority];


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

//User Operation Function
function user(){
    //Format it nicely (Transform each inner array to a string)
    let startMenu=menuArray
        .map(pair => `${pair[0]}=${pair[1]}`)
        .join("\n");
    let addUserOrNo=parseInt(prompt(`Please your Task\n ${startMenu}`));
    
    while(addUserOrNo!=7){
        if(addUserOrNo===1){
            // let nameOfUser=prompt("Enter the name of the User: ").toLowerCase();
            // let ageOfUser=parseInt(prompt("Enter the age of the User: "));
            // let taskOfUser=prompt("Enter the name of the task using , : ").toLowerCase();
            // taskOfUser=taskOfUser.split(",");
            // console.log(addUser(nameOfUser,ageOfUser,taskOfUser));
            main();
            
        }
        else if(addUserOrNo===2){
            let findUserName=prompt("Enter the name of the User: ").toLowerCase();
            let userFromFindUser=findThatUser(findUserName);
            console.log("User Found:");
            console.log(JSON.stringify(userFromFindUser,null,2));
        }
        else if(addUserOrNo===3){
            let nameOfTask=prompt("Please provide the name of the task: ").toLowerCase();
            nameOfTask=nameOfTask.split(",");
            let listOfTasks=findTask(nameOfTask);
            console.log("Name of all users with the same task Name: ");
            console.log(JSON.stringify(listOfTasks,null,2));
        }
        addUserOrNo=parseInt(prompt(`Please your Task\n ${startMenu}`));

    }
    
}

//Main Function
function main(){
    let askName=prompt("Enter the name of the User: ").toLowerCase();
    let askAge=parseInt(prompt("Enter the age of the user: "));
    let userTask=[];
    let askYesOrNo;
    do{
        let askTaskName=prompt("Enter the Name of the task: ");
        let setTaskPriority=taskPriorityMenu
            .map(pair =>`${pair[0]}=${pair[1]}`)                    //Need TO Understand
            .join("\n");
        let askPriority=prompt(`Enter the number of the priority ${setTaskPriority} : `);
        let assignTask={title:askTaskName,priority:askPriority,status:"To Do"};
        userTask.push(assignTask);
        askYesOrNo=prompt(`Do you want to add another task or not reply yes or no: `).toLowerCase();    
    }while(askYesOrNo==="yes");
    addUser(askName,askAge,userTask);
    console.log(JSON.stringify(DBUSER,null,2));
    user();
}
main();