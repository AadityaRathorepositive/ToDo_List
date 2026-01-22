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

//Modify Task
function modifyTask(userObj,taskInput){
    let user_task=userObj.task;
    for(let i=0;i<user_task.length;i++){
        if(user_task[i].title===taskInput){
            console.log(user_task[i]);
            //Modify Object
            let targetName=parseInt(prompt("What you want to modify: 1=Name, 2=priority, 3=status :"));
            if(targetName===1){
                let modifyName=prompt("Give the name you want to give: ");
                user_task[i].title=modifyName;
            }
            else if(targetName===2){
                let print_priorityMenu=taskPriorityMenu
                    .map(pair => `${pair[0]}=${pair[1]}`)
                    .join("\n");
                let modifyPriority=parseInt(prompt(`Please give the priority: ${print_priorityMenu}`));
                user_task[i].priority=modifyPriority;
            }
            else if(targetName===3){
                let taskStatus=prompt("Please Provide the status of task: ");
                user_task[i].status=taskStatus;
            }
        }
    }
    return userObj;
}

//Delete Task
function deleteSingleTask(userObj,task_name){
    let user_task=userObj.task;
    let revome_iteam=null;
    for(let i=0;i< user_task.length;i++){
        if(user_task[i].title ===task_name){
            revome_item=user_task.splice(i,1);
            break;
        }
    }
    return revome_item;
    
}

//Find User Index
function findUserIndex(userObj){
    for(let i=0;i<DBUSER.length;i++){
        
        if(userObj.name===DBUSER[i].name){
            return i;
        }
    }
    return -1;
}

//Delete User
function deleteUser(userObj){
    let UserIndex=findUserIndex(userObj);
    let deletedUser=DBUSER.splice(UserIndex,1);
    return deletedUser;
}

//Add Add New Task
function addNewTask(userObj){
    let NameofNewTask=prompt("Task Name: ");
    let priorityOfTask=prompt(`Task Priority: ${taskPriorityMenu}`);
    let newTask={
        title:NameofNewTask,
        priority:priorityOfTask,
        status:"to-d0"
    };
    userObj.task.push(newTask);
    console.log("Task added successfully");
}

//View Task
function viewTask(userObj){
    console.log(JSON.stringify(userObj.task,null,2));
}

//Find task using User Name
function findTaskUsingUserName(userObj,task_name){
    for(let taskName of userObj.task){
        if(taskName.title===task_name){
            return taskName;
        }
    }
    return null;
}
//Mark AS Done to the Task
function markAsDone(userObj){
    console.log(JSON.stringify(userObj.task,null,2));
    let taskToMarkAsDone=prompt("Which task do you want to mark as complete: ");
    let taskNameFound=findTaskUsingUserName(userObj,taskToMarkAsDone);
    if(taskNameFound){
        taskNameFound.status="Completed";
        console.log(`Success "${taskNameFound}" is marked as Completed`);
    }
    else{
        console.log("Task Not Found");
    }
}

//Change Priority
function changePriority(userObj){
    console.log(JSON.stringify(userObj,null,2));
    let taskNameToChangeThePriority=prompt("Enter the name of the task which you want to change the priority: ");
    let taskNameFound=findTaskUsingUserName(userObj,taskNameToChangeThePriority);
    if(taskNameFound){
        let askForConformation=prompt(`DO you want to change the priority of this ${taskNameFound} task:, Yes or No`).toLowerCase();
        if(askForConformation==="yes"){
            let printTaskPriorityMenu=taskPriorityMenu
                .map(shift=>`${shift[0]}:${shift[1]}`)
                .join("\n");
            let priorityValue=parseInt(prompt(`Enter the value of the priority: ${printTaskPriorityMenu}`));
            taskNameFound.priority=priorityValue;
            console.log(`${taskNameToChangeThePriority} priority has been changed`);
        }
        
    }
    else{
        console.log("Task Not Found");
    }
}

//Current User


//Switch User (means user want to modify the task)
let taskMenu=new Map();
taskMenu.set(1,"Add Task");
taskMenu.set(2,"View Task");
taskMenu.set(3,"Mark as Done");
taskMenu.set(4,"Delete");
taskMenu.set(5,"Change Priority");
taskMenu.set(6,"Switch User");

let taskMenuArray=[...taskMenu];


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
        else if(addUserOrNo===4){
            let nameOfUser_Input=prompt("Please enter name of the User: ");
            let doesUserExist=findThatUser(nameOfUser_Input);
            let outputOfTaskMenu=taskMenuArray
                        .map(pair=>`${pair[0]}=${pair[1]}`)
                        .join("\n");
            if(doesUserExist.length>0){
                let inputFromOptions=prompt(`Which Operation you want to perform: ${outputOfTaskMenu}`);
                while(inputFromOptions!=6){
                    
                    inputFromOptions=prompt(`Which Operation you want to perform: ${outputOfTaskMenu}`);
                    if(inputFromOptions===1){
                        addNewTask(nameOfUser_Input);
                    }
                    else if(inputFromOptions===2){
                        
                    }
                }
            }
            else{
                console.log("User Not Found.");
            }
            
            //Modify Task
            // let userInput=prompt("Please Enter the name of the user you want to modify: ");
            // let foundUser=findThatUser(userInput);
            // console.log(JSON.stringify(foundUser,null,2));
            // let taskInput=prompt("Please write which task you want to modify: ");
            // let modifiedTask=modifyTask(foundUser[0],taskInput);
            // console.log(JSON.stringify(modifiedTask,null,2));
        }
        else if(addUserOrNo===5){
            let options=parseInt(prompt("Do you want to search task from user name or from task name, Enter 1 for user name or 2 for task name: "));
            //Either find user and then delete the specific task or
            if(options===1){
                let user_name=prompt("Please enter the name of the user: ");
                let userInput=findThatUser(user_name);
                console.log(JSON.stringify(userInput,null,2));
                let taskInput=prompt("Enter the name of the task: ");
                let deletedTask;
                if(taskInput.length>0){
                   deletedTask=deleteSingleTask(userInput[0],taskInput); 
                }else{
                    console.log("User Not Found");
                }
                
                console.log(JSON.stringify(deletedTask,null,2));
                console.log(JSON.stringify(DBUSER,null,2));
            }
            //Search task directly and then delete it
            else if(options===2){
                let task_Input=prompt("Enter the name of the task: ");
                findWithTask=findTask([task_Input]);
                console.log(JSON.stringify(findWithTask,null,2));
                let user_name=prompt("Please Enter the name of the user or for all the user, write all: ").toLowerCase();
                let deletedTask;
                if(user_name==="all"){
                    for(let i=0;i<findWithTask.length;i++){
                        deletedTask=deleteSingleTask(findWithTask[i],task_Input);
                        console.log(JSON.stringify(deletedTask,null,2));
                    }
                    console.log(JSON.stringify(findWithTask,null,2));
                }else{
                    deletedTask=findWithTask.find(user=>user.name===user_name);
                    console.log(JSON.stringify(deletedTask,null,2));
                }
                
            }
            
        }
        else if(addUserOrNo===6){
            let userInput=prompt("Please enter the name of the user: ");
            let resultOfFindUser=findThatUser(userInput);
            if(resultOfFindUser){
                console.log(JSON.stringify(resultOfFindUser,null,2));
                let inputForDeleteUser=prompt("Do you want to delete this User,Reply with yes or no:").toLowerCase();
                
                if(inputForDeleteUser==="yes"){
                    console.log(JSON.stringify(deleteUser(resultOfFindUser[0])));
                }
            }else{
                console.log(`${userInput} not Found`);
            }
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