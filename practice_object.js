let obj={
    name:"Aaditya",
    Age:25,
    place:"Samastipur"
};
console.log(obj);
//Can Be Access using . Dot notation
console.log(obj.name);
//Also can be use [] bracket notation 
console.log(obj["Age"]);

//Create Object using new Object() constructor
let object= new Object();
object.name="Aaditya";
object.age="25";
object.place="Samastipur";
console.log(object);
//Can Be Access using . Dot notation
console.log(object.name);
//Also can be use [] bracket notation 
console.log(object["age"]);

//Both are Same although they are written differently

// ## OBJECT PROPERTY
// Object properties can be change
object.age=26;
console.log(object);
// Object property DataType can also be change
object.age="Too Small";
console.log(object.age);
console.log(object.Age);
// Adding Object Property
object.habit="Bad";
console.log(object);

let arr=[1,2,3,4,5];
let result=[...arr,arr];
console.log(result);

//array of object keys
// check if a key exists in Object
//Array inside object
//Nested Object
//Nested object indexing
// Take input from user and initilize into key and pair
// Array of objects --Indexing and iteration
