const prompt= require("prompt-sync")();
//Take input from user and multiple user
let DBOFSTUDENT=[];

function addUserTo_DBOFSTUDENT(student){
    DBOFSTUDENT.push(student);
}

function updateStudentDetails(student_name,newSubjectList){  
    for(let student of DBOFSTUDENT){
        if(Object.keys(student).includes("name")){
            if(student.name===student_name){
                
                student.subject=newSubjectList;
            }
        }
    }
    
    
}

function addUser(nameOfStudent,listOfSubjects){
    let student={
        name:nameOfStudent,
        subject:listOfSubjects
    };
    DBOFSTUDENT.push(student);
}

function checkStudentExits(studentName){
    if(DBOFSTUDENT.length===0)  return false;
    for(let student of DBOFSTUDENT){
        if(student["name"]===studentName){
            return true;
        }
    }
    return false;
}

function getStudentDetail(studentName){
    for(let student of DBOFSTUDENT){
        if(student["name"]===studentName){
            return student;
        }
    }
}

function main(){
    let nameOfStudent=prompt("Please Enter Name: ");
    let nameofSubject=prompt("Please enter the name of subject using , =");
    let split_nameofSubject=nameofSubject.split(",");
    addUser(nameOfStudent,split_nameofSubject);
    console.log(DBOFSTUDENT);
    let studentToUpdate=prompt("Enter the name of the Student want to update : ");
    if(checkStudentExits(studentToUpdate)){
        console.log(getStudentDetail(studentToUpdate));
        let newSubjectList=prompt("Enter the name of the subjects using , =");
        newSubjectList=newSubjectList.split(",");
        updateStudentDetails(studentToUpdate,newSubjectList);
        console.log(getStudentDetail(studentToUpdate));
    }else{
        console.log(`Student not Found:${studentToUpdate}`);
    }
    
}
main();

//getadduser
//updateUser
//addUser

//addTask
//updateTask
//getTask