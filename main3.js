const prompt = require("prompt-sync")({ sigint: true });


// Initial Menu and asking for input

const MENU= {
  1: "view ToDo List",
  2: "Add ToDo List",
  3: "Mark as Done",
  4: "Delete",
  5: "Done",
  6:"Set Priority",
  7: "Quit"
};

// Initializing Array to store ToDo List
//let array = [];
// Initializing Array to store Completed Task
//let markAsDone = [];

// Create User Database with structure Array and markAsDone Array
let userDB={};

let currentUser=null;

// Function to print the options menu and get user input
function PrintOptions() {
  console.log(`Current User: ${currentUser}`)
  let val=Object.keys(MENU).length;
  for(let i=1;i<=val;i++) {
    console.log(`${i}=${MENU[i]}`);
  }
  let userInput=prompt("Enter the value Which you want to perfome.\n");
  return userInput;
}

// Function to print the tasks in a list
function printList(list) {
  if (list.length === 0) {
    console.log("No tasks available.");
  } else {
    for (let i = 0; i < list.length; i++) {
      console.log(`${i + 1}: ${list[i]}`);
    }
  }
}

function loginUser() {
  let username=prompt("Enter your username: ");
  if(!userDB[username]){
    //userDB[username]={toDo:[], Done:[]};
    userDB[username]=[];
    //{"user1":[{"task":"sleep","priority":"High","status":"todo"}]}
  }else{
    console.log("Welcome back ", username);
  }
  return username;
}

function deleteTask(xyz){
  let deleteInput= prompt("Give Position of Task which you want to Delete: ");
  if (deleteInput>0 && deleteInput<=xyz.length) {
    let a = xyz.splice(deleteInput-1,1);
    console.log("This task is not completed: ", a[0]);
  } else {
    console.log("Invalid Position");
  }
}

// Function to Set Prority
function print_priority_of_Task(){
  let priority_bar={
    1:"Critical",
    2:"Very High",
    3:"Medium",
    4:"Low"
  }
  
  let value=Object.keys(priority_bar).length;
  for(let i=1;i<=value;i++){
    console.log(`priority Bar ${i} = ${priority_bar[i]}`);
  }
  // toDo1= {1:["eat"," High","todo"]}
  // Object.key(toDo1).arr[1]
}

function set_priority_of_task(task_not_completed_array){
  let user_to_decide_with_yes_no=prompt("Do you want to give priority to any of the task: yes or No").trim().toLowerCase();
  if(user_to_decide_with_yes_no==="yes"){
      if(task_not_completed_array.length===1){
      console.log(`This task is High on Priority : ${task_not_completed_array[0]} ${"*".repeat(5)}`);
    }else{
      printList(task_not_completed_array);
      let this_task_need_to_priority=parseInt(prompt("Which task you want to give priority: "));
      for(let i=1;i<=task_not_completed_array.length;i++){
        if(this_task_need_to_priority===i){
          print_priority_of_Task();
          let get_priority_number_from_user=parseInt(prompt("Please enter Priority bar Value : "));
          if(get_priority_number_from_user===1){
            task_not_completed_array[this_task_need_to_priority-1]=task_not_completed_array[this_task_need_to_priority-1]+" *".repeat(5);
          }
          else if(get_priority_number_from_user===2){
            task_not_completed_array[this_task_need_to_priority-1]=task_not_completed_array[this_task_need_to_priority-1]+" *".repeat(3);
          }
          else if(get_priority_number_from_user===3){
            task_not_completed_array[this_task_need_to_priority-1]=task_not_completed_array[this_task_need_to_priority-1]+" *".repeat(1);
          }
        }
      }
      printList(task_not_completed_array);
    }
  }
  
}

// Main Function to perform ToDo List operations
function toDoList(username) {

  currentUser=username;
  
  // 1: Adding new functionality- 2 times menu updated
  // 2: Adding new Functionality- Need to update conditions
  // 3: Printing List is repated
  // 4: Task Found then print
  let input=PrintOptions();
  // Validating Input Range
  let action=MENU[input];
  
  if (!action) {
    console.log("Invalid Input");
  }


  // Loop until user wants to quit
 /* The `while (input != 6)` statement is creating a loop that will continue running as long as the
 value of the `input` variable is not equal to 6. Inside this loop, the program checks the user's
 input and performs different operations based on the selected action from the menu. The loop will
 continue to run until the user chooses to quit by selecting option 6 from the menu. */
  while (action != "Quit") {
    let task_not_completed_array=userDB[currentUser].toDo;
    let completed_tasks=userDB[currentUser].Done;
    // Checking for user input and performing respective operations
    if (action === "view ToDo List") {
      // Printing ToDo List if it has any Task
      printList(task_not_completed_array);
    } 
    
    // Adding new Task to ToDo List array if user selects 2
    else if (action === "Add ToDo List") {
      
      let give = prompt("Please Input your Task: ");
      task_not_completed_array.push(give);
      printList(task_not_completed_array);
      
    } 
    
    //  Initializing variable position to store which user wants to mark as done
    else if (action === "Mark as Done") {
      // Printing ToDo List if it has any Task
      printList(task_not_completed_array);
      let done = prompt("Please Input Position of your Completed Task: ");
      if (done>0 && done<=task_not_completed_array.length) {
        // Removing Task from ToDo List  using a condition from a position to just 1 element from that position
        let value = task_not_completed_array.splice(done - 1, 1);
        // Adding that removed Task to Completed Task array
        completed_tasks.push(value[0]);
        printList(task_not_completed_array);
        console.log(completed_tasks);
      } else {
        console.log("You don't have any Tasks.");
      }
    } 
    
    else if (action === "Delete") {
      // Printing ToDo List if it has any Task
      printList(task_not_completed_array);
      printList(completed_tasks);
      let fromArray= prompt("If you want to Delete from ToDo List then type 'A' else type 'B' to delete from Completed Task List: ");
      
      if(fromArray==="A") {
        deleteTask(task_not_completed_array);
        // let deleteInput= prompt("Give Position of Task which you want to Delete: ");
        // if (deleteInput>0 && deleteInput<=array.length) {
          
        //   let a = array.splice(deleteInput-1,1);
        //   console.log("This task is not completed: ", a[0]);
        // } else {
        //   console.log("Invalid Position");
        // }
      } else if(fromArray==="B") {
        deleteTask(completed_tasks);
        // let deleteInput= prompt("Give Position of Task which you want to Delete: ");
        // if (deleteInput>0 && deleteInput<=markAsDone.length) {
          
        //   let a = markAsDone.splice(deleteInput-1,1);
        //   console.log("This completed task is deleted: ", a[0]);
        // } else {
        //   console.log("Invalid Position");
        // }
      }
      
    } 
    
    else if (action === "Done") {
      // Printing Completed Task List
      printList(completed_tasks);
    }
    
    else if(action==="Set Priority"){
      if(!task_not_completed_array.length){
        console.log("You don't have any Tasks.");
      }else{
        set_priority_of_task(task_not_completed_array);
      }
      
    }
    // 1: Adding new functionality- 2 times menu updated
    // 2: Adding new Functionality- Need to update conditions
    //input=Options();
    
    input=PrintOptions();
    action=MENU[input];
    if(!action && input!="7") {
      console.log("Invalid Input");
    }
  }
  
}
// Calling the main function to start the ToDo App
//let input=Options();
function main(){

  
  while(true){
    let userInput=loginUser();
    toDoList(userInput);
    let newUser=prompt("Do you want to switch user : yes or No= ");
    if(newUser==="yes"){
      continue;
    }else{
      break;
    }
  }

}
main();