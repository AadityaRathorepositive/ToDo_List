const prompt = require("prompt-sync")({ sigint: true });


// Initial Menu and asking for input

const MENU= {
  1: "view ToDo List",
  2: "Add ToDo List",
  3: "Mark as Done",
  4: "Delete",
  5: "Done",
  6: "Quit"
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
    userDB[username]={toDo:[], Done:[]};
  }else{
    console.log("Welcome back ", username);
  }
  return username;
}

// Main Function to perform ToDo List operations
function toDoList() {

  currentUser=loginUser();
  
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
    let array=userDB[currentUser].toDo; // userDB[user]['todo'] 
    let markAsDone=userDB[currentUser].Done;
    // Checking for user input and performing respective operations
    if (action === "view ToDo List") {
      // Printing ToDo List if it has any Task
      printList(array);
    } 
    
    // Adding new Task to ToDo List array if user selects 2
    else if (action === "Add ToDo List") {  
      let give = prompt("Please Input your Task: ");
      array.push(give);
      printList(array);
      
    } 
    
    //  Initializing variable position to store which user wants to mark as done
    else if (action === "Mark as Done") {
      // Printing ToDo List if it has any Task
      printList(array);
      let done = prompt("Please Input Position of your Completed Task: ");
      if (done>0 && done<=array.length) {
        // Removing Task from ToDo List  using a condition from a position to just 1 element from that position
        let value = array.splice(done - 1, 1);
        // Adding that removed Task to Completed Task array
        markAsDone.push(value[0]);
        printList(array);
        console.log(markAsDone);
      } else {
        console.log("You don't have any Tasks.");
      }
    } 
    
    else if (action === "Delete") {
      // Printing ToDo List if it has any Task
      printList(array);
      printList(markAsDone);
      let fromArray= prompt("If you want to Delete from ToDo List then type 'A' else type 'B' to delete from Completed Task List: ");
      if(fromArray==="A") {
        let deleteInput= prompt("Give Position of Task which you want to Delete: ");
        if (deleteInput>0 && deleteInput<=array.length) {
          // Removing last element from ToDo List which do not want to complete
          let a = array.splice(deleteInput-1,1);
          console.log("This task is not completed: ", a[0]);
        } else {
          console.log("Invalid Position");
        }
      } else if(fromArray==="B") {
        let deleteInput= prompt("Give Position of Task which you want to Delete: ");
        if (deleteInput>0 && deleteInput<=markAsDone.length) {
          // Removing last element from ToDo List which do not want to complete
          let a = markAsDone.splice(deleteInput-1,1);
          console.log("This completed task is deleted: ", a[0]);
        } else {
          console.log("Invalid Position");
        }
      }
      
    } 
    
    else if (action === "Done") {
      // Printing Completed Task List
      printList(markAsDone);
    }

    // 1: Adding new functionality- 2 times menu updated
    // 2: Adding new Functionality- Need to update conditions
    //input=Options();
    
    input=PrintOptions();
    action=MENU[input];
    if(!action && input!="6") {
      console.log("Invalid Input");
    }
  }
}
// Calling the main function to start the ToDo App
//let input=Options();
toDoList();
