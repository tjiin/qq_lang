## QQLang (because _tears_)
A simple personal project creating a programming language in python. The goal was to explore language theory, parsing and syntax, something I've always been interested in,

### So...What is it good for?
"Absolutely nothing!"
In all seriousness, it's only useful as a toy or educational example. It's fun trying to define your own syntax constructs.
There are no strings, lists, objects or other datatypes currently.


### I estimate it's about 100-200 times slower than C...
That said, I learned a ton about the process of writing a programming language and indeed to purse the idea further, perhaps with a more efficient base language.


### Features
* variable types: let, const, int, float
* first-class functions
* switch statements
* conditional expressions
* self-calling functions
* goto (lol)

### Syntax Examples


```javascript

// Passing a function as an argument
f(g,x) => { return g(x) } 
g(y) => y*-10; 
f(g,2);


// Returning a function
f() => { g(x) => x*-3; return(g); } 
let h = f(); 
h(2);

// Definining a function with closures
f(x) => g(y) => x + y; 
let h = f(2); 
h(10);

// Assigning to a function definition
let f = g(x) => x*2; 
f(-1);

// factorial defined as an implicit conditional expression (note the lack of a return statement)
factorial(x) => {
        x ? x*factorial(x-1) : 1; 
}
factorial(10);

// Or how about factorial as a switch statement?
factorial(x) => {
    switch (x) {
        case 0:
            return 1;
        default:
            return x*factorial(x-1);
    }
}
factorial(10);

// And just for the fun (and horror) of it, I added goto statements..
// So here's factorial written with goto.
f(x) => {
    let p = x;
    @dec: x = x-1;
    p = p*x;
    if x != 1 { goto @dec; }
    return p;
}
f(10);
```
