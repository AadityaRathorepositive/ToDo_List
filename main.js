const prompt = require("prompt-sync")({ sigint: true });
function toDoList() {
  // Initial Menu and asking for input
  let input = parseInt(
    prompt(
      "Enter the value Which you want to perfome.\n 1=view ToDo List\n2=Add ToDo List\n3=Mark as Done\n4=Delete\n5=Done\n6=Quit\n"
    )
  );
  // 1: Adding new functionality- 2 times menu updated
  // 2: Adding new Functionality- Need to update conditions
  // 3: Printing List is repated
  // 4: Task Found then print

  // Validating Input Range
  if (input < 0 || input >= 7) {
    console.log("Invalid Input");
  }

  // Initializing Array to store ToDo List
  let array = [];

  // Initializing Array to store Completed Task
  let markAsDone = [];
  // Loop until user wants to quit
  while (input != 6) {
    // Checking for user input and performing respective operations
    if (input === 1) {
      // Printing ToDo List if it has any Task
      if (array) {
        // Looping through array and printing each task with its position
        for (let i = 0; i < array.length; i++) {
          console.log(`${i + 1}: ${array[i]}`);
        }
      } else {
        console.log("You don't have any Tasks.");
      }
    } else if (input === 2) {
      // Adding new Task to ToDo List array if user selects 2
      let give = prompt("Please Input your Task: ");
      array.push(give);
      console.log(array);
    } else if (input === 3) {
      //  Initializing variable position to store which user wants to mark as done
      let done = prompt("Please Input Position of your Completed Task: ");
      if (array) {
        // Removing Task from ToDo List  using a condition from a position to just 1 element from that position
        let value = array.splice(done - 1, 1);
        // Adding that removed Task to Completed Task array
        markAsDone.push(value[0]);
        console.log(markAsDone);
      } else {
        console.log("You don't have any Tasks.");
      }
    } else if (input === 4) {
      if (array) {
        // Removing last element from ToDo List which do not want to complete
        let a = array.pop();
        console.log("This task is not completed: ", a);
      } else {
        console.log("No task to Delete");
      }
    } else if (input === 5) {
      if (markAsDone) {
        // Looping through Completed Task array and printing each task with its position
        for (let i = 0; i < markAsDone.length; i++) {
          console.log(`${i + 1}: ${markAsDone[i]}`);
        }
      } else {
        console.log("No completed Task");
      }
    }

    // 1: Adding new functionality- 2 times menu updated
    // 2: Adding new Functionality- Need to update conditions
    input = parseInt(
      prompt(
        "Enter the value Which you want to perfome.\n 1=viewToDo List\n2=Add ToDo List\n3=Mark as Done\n4=Delete\n5=Done List\n6=Quit\n"
      )
    );

    //console.log("Quit");
  }
}
// Calling the main function to start the ToDo App
toDoList();
